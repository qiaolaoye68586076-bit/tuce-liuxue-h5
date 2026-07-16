#!/usr/bin/env bash
#
# deploy.sh — 途策留学 H5 官网部署脚本
#
# 把本地 frontend/ 目录通过 rsync 同步到阿里云 ECS，并触发 Nginx 校验/重载。
#
# 用法见 ./deploy.sh --help
#
set -euo pipefail

# ---------------------------------------------------------------------------
# 默认变量（均可被同名环境变量覆盖，例如：ECS_HOST=1.2.3.4 ./deploy.sh）
# ---------------------------------------------------------------------------
: "${ECS_HOST:=121.43.101.155}"
: "${ECS_USER:=root}"
: "${ECS_PORT:=22022}"
: "${ECS_PATH:=/var/www/tuce}"
: "${LOCAL_SRC:=frontend}"
# 额外排除项（空格分隔的多个 rsync --exclude 模式）；默认空＝不额外排除。
# 例：只部署除文书训练营外的页面 → EXTRA_EXCLUDES='/writing-camp.html' ./deploy.sh
# 因未用 --delete-excluded，被排除的文件在远端会「原样保留」（既不上传新版也不删旧版）。
: "${EXTRA_EXCLUDES:=}"

# ---------------------------------------------------------------------------
# ANSI 颜色（非 TTY 环境自动降级为无色）
# ---------------------------------------------------------------------------
if [[ -t 1 ]]; then
  C_INFO=$'\033[36m'   # 青：阶段/进度
  C_OK=$'\033[32m'     # 绿：成功
  C_WARN=$'\033[33m'   # 黄：警告
  C_ERR=$'\033[31m'    # 红：失败
  C_DIM=$'\033[2m'     # 暗：次要信息
  C_RESET=$'\033[0m'
else
  C_INFO=''; C_OK=''; C_WARN=''; C_ERR=''; C_DIM=''; C_RESET=''
fi

log_info() { printf '%s▸ %s%s\n' "$C_INFO" "$*" "$C_RESET"; }
log_ok()   { printf '%s✓ %s%s\n' "$C_OK"   "$*" "$C_RESET"; }
log_warn() { printf '%s! %s%s\n' "$C_WARN" "$*" "$C_RESET"; }
log_err()  { printf '%s✗ %s%s\n' "$C_ERR"  "$*" "$C_RESET" >&2; }

# ---------------------------------------------------------------------------
# 用法
# ---------------------------------------------------------------------------
usage() {
  cat <<EOF
途策留学 H5 官网部署脚本

用法：
  ./deploy.sh [选项]

选项：
  -n, --dry-run    演练模式：rsync 只演练不传输；远端只跑 nginx -t（只读），不 reload
      --backup     部署前先在远端把 ${ECS_PATH} 打包到 /var/www/backups/
  -v, --verbose    逐文件列出变更明细（rsync --itemize-changes），配合 -n 看详细清单
  -h, --help       显示本帮助

环境变量（可覆盖默认值）：
  ECS_HOST   远端主机     (默认 ${ECS_HOST})
  ECS_USER   SSH 用户      (默认 ${ECS_USER})
  ECS_PORT   SSH 端口      (默认 ${ECS_PORT})
  ECS_PATH   远端部署目录   (默认 ${ECS_PATH})
  LOCAL_SRC  本地部署源目录 (默认 ${LOCAL_SRC})
  EXTRA_EXCLUDES  额外 rsync 排除模式，空格分隔（远端旧文件保留不删）

示例：
  ./deploy.sh              # 正式部署
  EXTRA_EXCLUDES='/writing-camp.html' ./deploy.sh   # 部署除文书训练营外的页面
  ./deploy.sh -n           # 演练
  ./deploy.sh --backup     # 部署前先备份远端
  ECS_HOST=1.2.3.4 ./deploy.sh
EOF
}

# ---------------------------------------------------------------------------
# 参数解析
# ---------------------------------------------------------------------------
DRY_RUN=false
DO_BACKUP=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dry-run) DRY_RUN=true ;;
    --backup)     DO_BACKUP=true ;;
    -v|--verbose) VERBOSE=true ;;
    -h|--help)    usage; exit 0 ;;
    *)            log_err "未知参数：$1"; echo; usage; exit 1 ;;
  esac
  shift
done

# SSH/rsync 公用连接选项（ServerAliveInterval 防止 WiFi 中途断开）
SSH_CMD=(ssh -p "$ECS_PORT" -o ServerAliveInterval=30)

# ---------------------------------------------------------------------------
# 0. 前置检查
# ---------------------------------------------------------------------------
if [[ ! -d "$LOCAL_SRC" ]]; then
  log_err "本地部署源目录不存在：$LOCAL_SRC"
  exit 1
fi

# ---------------------------------------------------------------------------
# 1. 本地校验：所有 HTML 必须含 <title> 标签
# ---------------------------------------------------------------------------
log_info "本地校验：检查 ${LOCAL_SRC}/*.html 的 <title> 标签"
missing_titles=()
shopt -s nullglob
for html in "$LOCAL_SRC"/*.html; do
  # 跳过第三方平台验证文件（Google/Baidu/Bing等）
  if [[ "$(basename "$html")" =~ ^(google|baidu_verify|BingSite|verify) ]]; then
    continue
  fi
  if ! grep -qi '<title>' "$html"; then
    missing_titles+=("$html")
  fi
done
shopt -u nullglob

if [[ ${#missing_titles[@]} -gt 0 ]]; then
  log_err "以下 HTML 缺少 <title> 标签，部署中止："
  for f in "${missing_titles[@]}"; do
    printf '    %s%s%s\n' "$C_ERR" "$f" "$C_RESET" >&2
  done
  exit 1
fi
log_ok "所有 HTML 均含 <title> 标签"

# ---------------------------------------------------------------------------
# 1.5 CSS 缓存版本号统一（内容哈希自动 bump）
#   以 style.css 的内容哈希作为 ?v=，保证：
#     ① 全站所有 HTML 的版本号始终一致（杜绝 v=23/25/28 漂移导致的缓存错配）
#     ② 仅当 style.css 内容真正变化时版本号才变（CSS 没动则命中缓存，不做无谓重下）
#   非演练：就地改写 ${LOCAL_SRC}/*.html；演练：只报告将要改写的文件，不落盘。
# ---------------------------------------------------------------------------
bump_css_version() {
  local css="$LOCAL_SRC/css/style.css"
  if [[ ! -f "$css" ]]; then
    log_warn "未找到 $css，跳过 CSS 版本号同步"
    return 0
  fi

  # 短内容哈希（兼容 macOS 的 md5 与 Linux 的 md5sum）
  local hash
  if command -v md5 >/dev/null 2>&1; then
    hash=$(md5 -q "$css")
  else
    hash=$(md5sum "$css" | cut -d' ' -f1)
  fi
  hash=${hash:0:8}

  log_info "CSS 版本号同步：style.css?v=${hash}"

  # 找出「引用了 style.css?v= 但版本号 ≠ 目标哈希」的 HTML
  local to_update=() f
  for f in "$LOCAL_SRC"/*.html; do
    if grep -qE 'style\.css\?v=' "$f" && ! grep -qE "style\.css\?v=${hash}\"" "$f"; then
      to_update+=("$f")
    fi
  done

  if [[ ${#to_update[@]} -eq 0 ]]; then
    log_ok "CSS 版本号已统一为 ${hash}，无需改写"
    return 0
  fi

  if [[ "$DRY_RUN" == true ]]; then
    log_warn "演练模式：以下 ${#to_update[@]} 个 HTML 的 CSS 版本号将更新为 ${hash}（本次不改写）"
    for f in "${to_update[@]}"; do
      printf '    %s%s%s\n' "$C_DIM" "$f" "$C_RESET"
    done
    return 0
  fi

  for f in "${to_update[@]}"; do
    sed -i.bak -E "s/style\.css\?v=[^\"']*/style.css?v=${hash}/g" "$f" && rm -f "$f.bak"
  done
  log_ok "已将 ${#to_update[@]} 个 HTML 的 CSS 版本号统一为 ${hash}"
}

bump_css_version

# ---------------------------------------------------------------------------
# 1.6 sitemap.xml lastmod 动态更新
#    每次部署时把 lastmod 全部替换为当前日期，让搜索引擎知道页面仍在维护。
# ---------------------------------------------------------------------------
bump_sitemap_lastmod() {
  local sm="$LOCAL_SRC/sitemap.xml"
  if [[ ! -f "$sm" ]]; then
    log_warn "未找到 $sm，跳过 sitemap 日期更新"
    return 0
  fi
  local today
  today=$(date +%Y-%m-%d)
  local old
  old=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$sm" | head -n1 || true)

  if [[ "$old" == "$today" ]]; then
    log_ok "sitemap lastmod 已是今日 ${today}，无需更新"
    return 0
  fi

  if [[ "$DRY_RUN" == true ]]; then
    log_warn "演练模式：sitemap.xml lastmod 将更新为 ${today}（本次不改写）"
    return 0
  fi

  sed -i.bak -E "s/[0-9]{4}-[0-9]{2}-[0-9]{2}/${today}/g" "$sm" && rm -f "$sm.bak"
  log_ok "sitemap.xml lastmod 已更新为 ${today}"
}
bump_sitemap_lastmod

# ---------------------------------------------------------------------------
# 计时开始
# ---------------------------------------------------------------------------
SECONDS=0

# ---------------------------------------------------------------------------
# 2. 可选备份（仅正式部署有意义；演练时跳过以免改动远端）
# ---------------------------------------------------------------------------
if [[ "$DO_BACKUP" == true ]]; then
  if [[ "$DRY_RUN" == true ]]; then
    log_warn "演练模式：跳过远端备份（备份会改动服务器）"
  else
    backup_name="tuce-$(date +%Y%m%d-%H%M%S).tar.gz"
    log_info "远端备份：打包 ${ECS_PATH} → /var/www/backups/${backup_name}"
    "${SSH_CMD[@]}" "$ECS_USER@$ECS_HOST" \
      "mkdir -p /var/www/backups && tar czf /var/www/backups/${backup_name} -C /var/www tuce"
    log_ok "备份完成：/var/www/backups/${backup_name}"
  fi
fi

# ---------------------------------------------------------------------------
# 3. rsync 同步
# ---------------------------------------------------------------------------
# --stats 让 rsync 输出权威统计行，正式部署据此取「实际传输文件数」
# --exclude 保护「服务器自己生成」的内容不被 --delete 清掉 / 被本地占位覆盖：
#   /articles.json     由 scripts/sync_articles.py 在服务器上生成（仓库那份只是占位种子）
#   /assets/insights/   同步脚本下载的公众号封面图
#   /_*.html           下划线前缀的预览/草稿页（如 _preview-*.html），仅本地预览，不上生产
# 详见 scripts/README.md「与 deploy.sh 的关系」。
rsync_opts=(-avz --progress --partial --timeout=120 --delete --stats
            --exclude='.DS_Store'
            --exclude='/articles.json'
            --exclude='/assets/insights/'
            --exclude='/_*.html')
# 追加来自 EXTRA_EXCLUDES 的临时排除项（空格分隔；故意不加引号以按空格拆分）
if [[ -n "$EXTRA_EXCLUDES" ]]; then
  for _pat in $EXTRA_EXCLUDES; do
    rsync_opts+=(--exclude="$_pat")
    log_warn "额外排除：$_pat（远端旧文件保留、不删除）"
  done
fi
if [[ "$VERBOSE" == true ]]; then
  rsync_opts+=(--itemize-changes)
fi
if [[ "$DRY_RUN" == true ]]; then
  rsync_opts+=(--dry-run)
  log_info "rsync 演练（--dry-run，不会实际传输/删除）"
else
  log_info "rsync 同步：${LOCAL_SRC}/ → ${ECS_USER}@${ECS_HOST}:${ECS_PATH}/"
fi

# 用临时文件捕获 rsync 输出，便于统计传输文件数
rsync_log="$(mktemp)"
trap 'rm -f "$rsync_log"' EXIT

set +e
rsync "${rsync_opts[@]}" \
  -e "ssh -p $ECS_PORT -o ServerAliveInterval=30" \
  "$LOCAL_SRC/" "$ECS_USER@$ECS_HOST:$ECS_PATH/" | tee "$rsync_log"
rsync_rc=${PIPESTATUS[0]}
set -e

if [[ $rsync_rc -ne 0 ]]; then
  log_err "rsync 失败（退出码 $rsync_rc），部署中止"
  exit "$rsync_rc"
fi

# 统计「文件级变更数」：两模式统一取 --stats 的 transferred 字段
#   - dry-run 下它就是「这次会变更/传输的文件数」（rsync 也会算）
#   - 正式部署下它就是「实际传输的文件数」
# 字段名兼容新旧 rsync：新版 "Number of regular files transferred"，
# 老版（如 macOS 自带）"Number of files transferred"。
# 注意：该统计只算 regular files，不含目录 —— 空目录的创建/删除不计入。
transferred=$(grep -E 'Number of (regular )?files transferred:' "$rsync_log" \
              | grep -oE '[0-9]+' | head -n1 || true)
[[ -z "$transferred" ]] && transferred=0
log_ok "rsync 完成"

# ---------------------------------------------------------------------------
# 4. 远端 Nginx 校验 / 重载
#    nginx -t 是只读操作 → 演练也跑；systemctl reload → 仅正式部署
# ---------------------------------------------------------------------------
log_info "远端 Nginx 配置校验（nginx -t）"
nginx_test_out="$("${SSH_CMD[@]}" "$ECS_USER@$ECS_HOST" "nginx -t" 2>&1)"
nginx_test_rc=$?
printf '%s%s%s\n' "$C_DIM" "$nginx_test_out" "$C_RESET"

if [[ $nginx_test_rc -ne 0 ]]; then
  log_err "nginx -t 失败，未执行 reload"
  exit "$nginx_test_rc"
fi
log_ok "nginx -t 通过"

if [[ "$DRY_RUN" == true ]]; then
  log_warn "演练模式：跳过 systemctl reload nginx"
else
  log_info "远端重载 Nginx（systemctl reload nginx）"
  "${SSH_CMD[@]}" "$ECS_USER@$ECS_HOST" "systemctl reload nginx"
  log_ok "Nginx 已重载"
fi

# ---------------------------------------------------------------------------
# 5. 汇总
# ---------------------------------------------------------------------------
echo
log_ok "部署流程结束"
printf '  %s耗时    :%s %ds\n'      "$C_DIM" "$C_RESET" "$SECONDS"
if [[ "$transferred" -eq 0 ]]; then
  printf '  %s文件变更:%s %s✓ 无变更，本地与远端已同步%s\n' \
         "$C_DIM" "$C_RESET" "$C_OK" "$C_RESET"
else
  printf '  %s文件变更:%s %s 个%s\n' "$C_DIM" "$C_RESET" "$transferred" \
         "$([[ "$DRY_RUN" == true ]] && echo "  ${C_WARN}(演练，将变更但未实际传输)${C_RESET}" || echo '')"
fi
printf '  %snginx -t:%s %s通过%s\n' "$C_DIM" "$C_RESET" "$C_OK" "$C_RESET"

# 演练时变更量较大，提示先看详细清单再正式部署
if [[ "$DRY_RUN" == true && "$transferred" -gt 10 ]]; then
  echo
  log_warn "变更量较大（${transferred} 个文件），建议先 ./deploy.sh -n -v 看详细清单，确认没有误带不该传的东西"
fi
