# backend/ — Flask 留资 API

接收前端 CTA 表单提交（`frontend/js/main.js` 的 `LEAD_ENDPOINT`），落库 SQLite，
可选推送微信。前端字段：`uname / type / phone / wechat / city / school / more`。

## 文件
- `app.py` — Flask 应用：`POST /api/lead` 留资、`GET /api/leads` 导出、`GET /api/health`
- `requirements.txt` — Flask + gunicorn
- `leads.db` — SQLite，运行时自动生成（已在 `.gitignore` 忽略）

## 本地运行
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py                 # 开发模式，http://127.0.0.1:5000
```

## 接口
| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/lead` | 提交留资，JSON body，返回 `{"ok":true}`；姓名/手机号服务端复校验 |
| GET | `/api/leads?token=XXX` | 导出全部留资（JSON）；加 `&format=csv` 导出 CSV（带 BOM，Excel 友好）|
| GET | `/api/health` | 健康检查 |

## 环境变量（都可选）
| 变量 | 作用 | 不配时 |
|---|---|---|
| `TUCE_DB_PATH` | SQLite 路径 | 默认 `backend/leads.db` |
| `ADMIN_TOKEN` | `/api/leads` 导出口令 | **不配则导出接口关闭（403）** |
| `SERVERCHAN_KEY` | Server酱 SendKey，推送到微信 | 不推送 |
| `PUSHPLUS_TOKEN` | pushplus token，推送到微信 | 不推送 |
| `CORS_ORIGIN` | 允许跨域来源 | `*`（同域部署可忽略）|

## 上线（配合 nginx）
1. `gunicorn -w 2 -b 127.0.0.1:5000 app:app`（建议用 systemd 守护）
2. nginx 加反代：`location /api/ { proxy_pass http://127.0.0.1:5000; }`
3. 把 `frontend/js/main.js` 第 9 行 `LEAD_ENDPOINT` 改为 `'/api/lead'`（同域，无需跨域）
4. 配 `ADMIN_TOKEN` + 至少一个推送 key，重启服务

> ⚠️ 详见 `docs/DOMAIN-CUTOVER.md`。前端 `LEAD_ENDPOINT` 在后端上线前保持留空（留空＝表单走本地兜底并模拟成功，避免线上 fetch 报错）。
