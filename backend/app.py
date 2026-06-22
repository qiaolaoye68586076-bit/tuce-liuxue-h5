#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
途策留学 H5 — 留资后端（零依赖标准库版）

服务器是 Python 3.6.8，装不了 Flask 3.x，故用标准库 http.server + sqlite3 实现，
不依赖任何第三方包，systemd 守护即可，省去在生产装 pip 包的风险。

接收前端 CTA 表单（frontend/js/main.js 的 LEAD_ENDPOINT）提交的留资数据，
落库到 SQLite，并（可选）通过 Server酱 / pushplus 推送到微信。

接口：
  POST /api/lead          提交留资（字段：uname/type/phone/wechat/city/school/more/ts/source）
  GET  /api/leads         导出全部留资（需 ?token= 或 X-Admin-Token；加 &format=csv 导 CSV）
  GET  /api/health        健康检查

环境变量（均可选，不配也能跑）：
  TUCE_DB_PATH      SQLite 路径，默认 backend/leads.db
  TUCE_PORT         监听端口，默认 5000（仅本机，由 nginx 反代 /api/）
  ADMIN_TOKEN       /api/leads 导出口令；未设置则导出接口关闭
  SERVERCHAN_KEY    Server酱 SendKey（配了就推送，sctapi.ftqq.com）
  PUSHPLUS_TOKEN    pushplus token
  CORS_ORIGIN       允许的跨域来源，默认 *（同域部署可忽略）

本地/服务器运行：
  python3 app.py
"""

import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
import logging
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("TUCE_DB_PATH", os.path.join(HERE, "leads.db"))
PORT = int(os.environ.get("TUCE_PORT", "5000"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
SERVERCHAN_KEY = os.environ.get("SERVERCHAN_KEY", "")
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN", "")
CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "*")

# 与前端 frontend/js/main.js collect() 一致的字段
FIELDS = ["uname", "type", "phone", "wechat", "city", "school", "more"]
PHONE_RE = re.compile(r"^1[3-9]\d{9}$")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tuce")


# ----------------------------- 数据库 -----------------------------
def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            uname      TEXT NOT NULL,
            type       TEXT,
            phone      TEXT NOT NULL,
            wechat     TEXT,
            city       TEXT,
            school     TEXT,
            more       TEXT,
            source     TEXT,
            client_ts  TEXT,
            ip         TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    db.commit()
    db.close()


def insert_lead(lead):
    # 每个请求一条新连接：留资量极小，无需连接池，且天然线程安全
    db = sqlite3.connect(DB_PATH)
    try:
        db.execute(
            """INSERT INTO leads
               (uname, type, phone, wechat, city, school, more, source, client_ts, ip, created_at)
               VALUES (:uname, :type, :phone, :wechat, :city, :school, :more,
                       :source, :client_ts, :ip, :created_at)""",
            lead,
        )
        db.commit()
    finally:
        db.close()


def fetch_leads():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        rows = db.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


# ----------------------------- 微信推送 -----------------------------
def _http_post(url, data):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            return resp.status == 200
    except Exception as e:  # 推送失败绝不影响留资落库
        log.warning("push failed: %s", e)
        return False


def notify(lead):
    title = "途策新留资：%s（%s）" % (lead["uname"], lead.get("type") or "未选方向")
    body = "\n".join([
        "姓名：%s" % lead["uname"],
        "电话：%s" % lead["phone"],
        "方向：%s" % (lead.get("type") or "-"),
        "微信：%s" % (lead.get("wechat") or "-"),
        "城市：%s" % (lead.get("city") or "-"),
        "在读/目标：%s" % (lead.get("school") or "-"),
        "补充：%s" % (lead.get("more") or "-"),
        "来源：%s" % (lead.get("source") or "h5"),
        "时间：%s" % lead["created_at"],
    ])
    if SERVERCHAN_KEY:
        _http_post("https://sctapi.ftqq.com/%s.send" % SERVERCHAN_KEY,
                   {"title": title, "desp": body})
    if PUSHPLUS_TOKEN:
        _http_post("https://www.pushplus.plus/send",
                   {"token": PUSHPLUS_TOKEN, "title": title, "content": body})


# ----------------------------- HTTP 处理 -----------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "tuce-lead/1.0"

    def _send(self, status, payload, content_type="application/json; charset=utf-8",
              extra_headers=None):
        if isinstance(payload, (dict, list)):
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        elif isinstance(payload, str):
            body = payload.encode("utf-8")
        else:
            body = payload or b""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", CORS_ORIGIN)
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Admin-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _client_ip(self):
        xff = self.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0].strip()
        return self.client_address[0] if self.client_address else ""

    def do_OPTIONS(self):
        self._send(204, b"")

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path != "/api/lead":
            return self._send(404, {"ok": False, "error": "not found"})

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b""
        ctype = self.headers.get("Content-Type", "")
        try:
            if "application/json" in ctype:
                data = json.loads(raw.decode("utf-8") or "{}")
            else:
                parsed = urllib.parse.parse_qs(raw.decode("utf-8"))
                data = {k: v[0] for k, v in parsed.items()}
        except Exception:
            return self._send(400, {"ok": False, "error": "请求格式有误"})
        if not isinstance(data, dict):
            return self._send(400, {"ok": False, "error": "请求格式有误"})

        lead = {k: (str(data.get(k) or "")).strip() for k in FIELDS}

        # 服务端复校验（前端可被绕过，必须复核）
        if not lead["uname"]:
            return self._send(400, {"ok": False, "error": "请填写姓名"})
        if not PHONE_RE.match(lead["phone"]):
            return self._send(400, {"ok": False, "error": "请输入有效的 11 位手机号"})

        lead["source"] = (str(data.get("source") or "h5")).strip()
        lead["client_ts"] = (str(data.get("ts") or "")).strip()
        lead["created_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        lead["ip"] = self._client_ip()

        try:
            insert_lead(lead)
        except Exception as e:
            log.error("db insert failed: %s", e)
            return self._send(500, {"ok": False, "error": "服务器繁忙，请稍后重试"})

        notify(lead)  # 内部已吞掉异常，不影响返回
        log.info("new lead: %s %s", lead["uname"], lead["phone"])
        self._send(200, {"ok": True})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/api/health":
            return self._send(200, {"ok": True})
        if path == "/api/leads":
            return self._handle_export(urllib.parse.parse_qs(parsed.query))
        return self._send(404, {"ok": False, "error": "not found"})

    def _handle_export(self, query):
        if not ADMIN_TOKEN:
            return self._send(403, {"ok": False, "error": "导出接口未启用（未配置 ADMIN_TOKEN）"})
        token = (query.get("token", [""])[0]) or self.headers.get("X-Admin-Token", "")
        if token != ADMIN_TOKEN:
            return self._send(401, {"ok": False, "error": "无权访问"})

        items = fetch_leads()
        if query.get("format", [""])[0] == "csv":
            cols = ["id", "created_at", "uname", "phone", "type", "wechat",
                    "city", "school", "more", "source", "client_ts", "ip"]
            out = [",".join(cols)]
            for it in items:
                out.append(",".join(
                    '"%s"' % str(it.get(c, "")).replace('"', '""') for c in cols))
            csv = "﻿" + "\n".join(out)  # BOM 便于 Excel 识别 UTF-8
            return self._send(200, csv, content_type="text/csv; charset=utf-8",
                              extra_headers={"Content-Disposition": "attachment; filename=leads.csv"})
        self._send(200, {"ok": True, "count": len(items), "items": items})

    def log_message(self, fmt, *args):  # 收敛默认 stderr 噪声，走 logging
        log.info("%s - %s", self.address_string(), fmt % args)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    init_db()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    log.info("途策留资后端启动 http://127.0.0.1:%d  db=%s  推送=%s",
             PORT, DB_PATH,
             "/".join([n for n, v in
                       (("Server酱", SERVERCHAN_KEY), ("pushplus", PUSHPLUS_TOKEN)) if v]) or "未配置")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
