#!/usr/bin/env bash
#
# submit-indexnow.sh — 向 IndexNow API 提交 tuce.asia 页面更新通知
#
# 用法：
#   ./scripts/submit-indexnow.sh
#
# 环境变量（可覆盖默认值）：
#   INDEXNOW_KEY          API Key（默认内置）
#   INDEXNOW_KEY_LOCATION Key 文件 URL（默认 https://tuce.asia/<key>.txt）
#
# 退出码：
#   0  提交成功（HTTP 200 或 202）
#   1  提交失败（网络错误 / HTTP 4xx / 其他非成功状态码）
#
set -euo pipefail

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
API_KEY="${INDEXNOW_KEY:-6f73703620ba4c1682bb2ada9358f4ae}"
HOST="tuce.asia"
KEY_LOCATION="${INDEXNOW_KEY_LOCATION:-https://tuce.asia/${API_KEY}.txt}"
INDEXNOW_URL="https://api.indexnow.org/IndexNow"

# 需要通知 IndexNow 的页面 URL 列表
# - 不包含 www.tuce.asia（只用裸域）
# - 不包含 sitemap.xml、robots.txt、CSS、JS、图片、API 地址
URL_LIST=(
  "https://tuce.asia/"
  "https://tuce.asia/services"
  "https://tuce.asia/meiben"
  "https://tuce.asia/graduate"
  "https://tuce.asia/transfer"
  "https://tuce.asia/uk-eu"
  "https://tuce.asia/immigration"
  "https://tuce.asia/teachers"
  "https://tuce.asia/cases"
  "https://tuce.asia/blog"
  "https://tuce.asia/writing-camp"
)

# ---------------------------------------------------------------------------
# 构建 JSON：jq 保证合法转义，杜绝手工拼接导致的破损 JSON
# ---------------------------------------------------------------------------
PAYLOAD=$(jq -n \
  --arg host "$HOST" \
  --arg key "$API_KEY" \
  --arg keyLocation "$KEY_LOCATION" \
  --argjson urlList "$(printf '%s\n' "${URL_LIST[@]}" | jq -R . | jq -s .)" \
  '{host: $host, key: $key, keyLocation: $keyLocation, urlList: $urlList}')

# ---------------------------------------------------------------------------
# 提交
# ---------------------------------------------------------------------------
RESPONSE=$(curl -s -w "\n%{http_code}" \
  --max-time 30 \
  -X POST "$INDEXNOW_URL" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$PAYLOAD") || {
  echo "IndexNow: 网络请求失败（curl 退出码 $?），无法连接 api.indexnow.org" >&2
  exit 1
}

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  200|202)
    echo "IndexNow: 提交成功 (HTTP $HTTP_CODE)"
    exit 0
    ;;
  400)
    echo "IndexNow: 请求格式错误 (HTTP 400)，请检查 JSON payload 结构" >&2
    echo "$BODY" >&2
    exit 1
    ;;
  403)
    echo "IndexNow: API Key 无效或无权提交此 host (HTTP 403)" >&2
    echo "$BODY" >&2
    exit 1
    ;;
  422)
    echo "IndexNow: 请求被拒绝 (HTTP 422)，URL 可能不属于该 host 或格式不正确" >&2
    echo "$BODY" >&2
    exit 1
    ;;
  429)
    echo "IndexNow: 请求过于频繁 (HTTP 429)，请稍后再试" >&2
    exit 1
    ;;
  *)
    echo "IndexNow: 未预期的 HTTP 状态码 (HTTP $HTTP_CODE)" >&2
    echo "$BODY" >&2
    exit 1
    ;;
esac
