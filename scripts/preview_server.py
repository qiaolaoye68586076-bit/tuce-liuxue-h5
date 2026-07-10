#!/usr/bin/env python3
"""本地预览服务器：模拟线上 nginx 的 `try_files $uri $uri/ $uri.html` 行为，
自动为无后缀路径补 .html，这样站内无 .html 后缀的导航链接在本地也能正常预览。

用法： python3 scripts/preview_server.py [port]
默认 http://127.0.0.1:8000/
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# web 根 = 项目下的 frontend/
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
ROOT = os.path.abspath(ROOT)


class NginxLikeHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def translate_path(self, path):
        fs_path = super().translate_path(path)
        # 若原路径不存在、非目录、且补上 .html 后存在 → 用 .html（对齐 nginx try_files）
        if not os.path.exists(fs_path) and not fs_path.endswith(".html"):
            html_candidate = fs_path + ".html"
            if os.path.isfile(html_candidate):
                return html_candidate
        return fs_path


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    httpd = ThreadingHTTPServer(("127.0.0.1", port), NginxLikeHandler)
    print(f"本地预览： http://127.0.0.1:{port}/  (web 根: {ROOT})")
    print("按 Ctrl+C 停止")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == "__main__":
    main()
