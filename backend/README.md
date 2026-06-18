# backend/ — Flask API（预留）

后续在此开发表单留资与数据存储服务：

- `app.py` — Flask 应用入口，处理 `LEAD_ENDPOINT` 留资表单提交
- `leads.db` — SQLite 数据库（运行时生成，已在 .gitignore 忽略）

部署时让 `../frontend/` 作为静态 web 根目录，本服务提供 `/api/*` 接口。
