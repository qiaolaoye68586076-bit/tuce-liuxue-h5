# 途策留学 H5 官网 · 部署文档

本项目为静态站点，部署方式为：本地 `frontend/` 目录通过 `rsync` 同步到阿里云 ECS，由 Nginx 提供服务。

---

## 环境信息

| 项目 | 值 |
|---|---|
| ECS 公网 IP | `121.43.101.155` |
| 操作系统 | Alibaba Cloud Linux 3 |
| SSH 端口 | `22022`（**不是 22**）|
| SSH 用户 | `root` |
| SSH alias | `tuce`（已配在 `~/.ssh/config`，可直接 `ssh tuce`）|
| 部署源（本地）| `./frontend/` |
| 部署目标（远端）| `/var/www/tuce/` |
| Nginx 站点配置 | 远端 `/etc/nginx/conf.d/tuce.conf`（版本控制副本见 `nginx.conf.example`）|
| 备份目录（远端）| `/var/www/backups/` |

> 生产访问地址：https://tuce.asia/。直接访问 IP 仅用于服务器排查，SSL 证书按域名签发。

---

## 日常操作

所有命令在仓库根目录执行。

| 操作 | 命令 |
|---|---|
| 正式部署 | `./deploy.sh` |
| 演练（不传输/不重载）| `./deploy.sh -n` |
| 演练 + 逐文件变更明细 | `./deploy.sh -n -v` |
| 部署前先备份远端 | `./deploy.sh --backup` |
| 查看帮助 | `./deploy.sh --help` |

### `deploy.sh` 做了什么

1. **本地校验**：检查 `frontend/*.html` 是否都含 `<title>` 标签，缺失则中止（不传输）。
2. **可选备份**（`--backup`）：远端把 `/var/www/tuce` 打包到 `/var/www/backups/tuce-YYYYMMDD-HHMMSS.tar.gz`。
3. **rsync 同步**：`-avz --progress --partial --timeout=120 --delete --exclude='.DS_Store'`，
   SSH 加 `-o ServerAliveInterval=30` 防止 WiFi 中途断开。
   > ⚠️ `--delete` 是镜像同步：远端 `/var/www/tuce` 里 `frontend/` 没有的文件会被删除。
4. **远端 Nginx 校验/重载**：`nginx -t`（只读，演练也会跑）→ 通过后 `systemctl reload nginx`（仅正式部署）。
5. **汇总**：耗时、文件变更数、`nginx -t` 结果。

### 读懂输出

- **文件变更数** 取自 rsync `--stats` 的 transferred 字段（兼容新旧 rsync 的
  `Number of (regular )?files transferred`）。两种模式语义统一：
  - 演练（`-n`）下 = **这次将会变更的文件数**（rsync 也会预算出来）；
  - 正式部署下 = **实际传输的文件数**。
- **`✓ 无变更，本地与远端已同步`**：transferred 为 0，本地与远端文件级内容一致。
- ⚠️ 该统计只反映**文件级**变更，**不计入空目录的创建/删除**。
  极端情况：只新增一个空目录、没有任何文件改动时，会显示「无变更」，但远端仍会建该目录。
  日常迭代不会遇到（都伴随文件改动），知道即可。
- 演练若变更 **> 10 个文件**会提示先用 `./deploy.sh -n -v` 看逐文件明细，
  确认没把 `archive/` 等不该传的东西误带进去。

### 环境变量覆盖

默认变量都可被环境变量覆盖，例如临时部署到另一台机器：

```bash
ECS_HOST=1.2.3.4 ECS_PORT=22 ./deploy.sh
```

可覆盖项：`ECS_HOST` / `ECS_USER` / `ECS_PORT` / `ECS_PATH` / `LOCAL_SRC`。

---

## 首次部署流程（历史记录）

> 以下为站点首次上线时执行过的步骤，留作参考；日常更新只需 `./deploy.sh`。

1. **服务器准备**
   ```bash
   ssh tuce                       # 等价于 ssh -p 22022 root@121.43.101.155
   yum install -y nginx rsync
   systemctl enable --now nginx
   mkdir -p /var/www/tuce /var/www/backups
   ```

2. **写 Nginx 站点配置**：把 `nginx.conf.example` 内容写入远端 `/etc/nginx/conf.d/tuce.conf`，
   然后 `nginx -t && systemctl reload nginx`。

3. **阿里云安全组放行**：开放入方向 `80`（HTTP）与 `22022`（SSH）端口。

4. **首次同步**：本地执行 `./deploy.sh`（或先 `./deploy.sh -n` 演练）。

5. **验证**：浏览器访问 https://tuce.asia/，或 `curl -I https://tuce.asia/`。

---

## 故障排查清单

基于实际踩过的坑：

| 现象 | 可能原因 | 解决 |
|---|---|---|
| `Connection refused` | 阿里云安全组没开 `22022`；或远端 sshd 没起来 | 检查安全组入方向规则；远端 `systemctl status sshd` |
| `Connection timed out` | 学校 WiFi 封了 22 端口；或本地出口网络被封 | 本项目 SSH 走 `22022` 正是为绕过封 22；换网络（手机热点）排除出口问题 |
| `curl http://IP` 80 端口超时 | 阿里云安全组没开 `80` | 安全组入方向放行 80 |
| rsync 传输卡顿 | 学校 WiFi 上行带宽慢 | 脚本已带 `--progress --partial`，可断点续传，耐心等或换网络 |
| 大文件超时中断 | 单个大文件超过 `--timeout=120` | 调大脚本里的 `--timeout`；或排查 `frontend/` 里未被引用的大图片（如超大 PNG/SVG）后删除再传 |
| `nginx -t` 失败 | 远端 `tuce.conf` 配置有误 | 脚本会打印错误并**不执行 reload**；对照 `nginx.conf.example` 修正远端配置 |

---

## 安全提醒 / TODO

⚠️ **当前服务器仍开启 root 密码登录。** 后续应加固：

- [ ] 配置 SSH 密钥登录（`ssh-copy-id` 或手动写入 `~/.ssh/authorized_keys`）
- [ ] 禁用密码登录（`/etc/ssh/sshd_config` 设 `PasswordAuthentication no` 后 `systemctl restart sshd`）
- [ ] 考虑新建非 root 部署用户，最小权限
- [x] SSL 证书已配置为 Let's Encrypt，并由 Certbot 自动续期
