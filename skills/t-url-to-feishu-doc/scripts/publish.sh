#!/usr/bin/env bash
# Publish a URL's content as a new sub-document under a Feishu wiki node.
#
# Usage:
#   publish.sh --url <URL> --parent <wiki-url-or-token> [--title "Custom Title"]
#              [--raw-dir ./.raw] [--keep-front-matter]
#
# What it does:
#   1. curl the URL -> .raw/pages/<slug>.html
#   2. extract.py -> .raw/text/<slug>.md (clean Markdown, front matter stripped)
#   3. derive title from first H1 (or use --title)
#   4. lark-cli docs +create --parent-token <parent> --doc-format markdown
#   5. verify the new doc appears in the parent's sub-page list
#
# Requires: lark-cli (auth user identity), curl, python3.

set -euo pipefail

URL=""
PARENT=""
TITLE=""
RAW_DIR="./.raw"
KEEP_FRONT=0
SLUG=""

usage() {
  sed -n '2,12p' "$0"
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --url) URL="$2"; shift 2 ;;
    --parent) PARENT="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    --raw-dir) RAW_DIR="$2"; shift 2 ;;
    --slug) SLUG="$2"; shift 2 ;;
    --keep-front-matter) KEEP_FRONT=1; shift ;;
    -h|--help) usage ;;
    *) echo "unknown flag: $1" >&2; usage ;;
  esac
done

[ -n "$URL" ] || { echo "error: --url required" >&2; usage; }
[ -n "$PARENT" ] || { echo "error: --parent required" >&2; usage; }

# Derive slug from URL path if not given
if [ -z "$SLUG" ]; then
  SLUG=$(printf '%s' "$URL" | sed -E 's|https?://||; s|/|__|g; s|[?#].*||; s|_+|_|g')
  SLUG=$(printf '%s' "$SLUG" | tr -c '[:alnum:]_.-' '_')
fi

HTML="$RAW_DIR/pages/${SLUG}.html"
MD="$RAW_DIR/text/${SLUG}.md"

mkdir -p "$(dirname "$HTML")" "$(dirname "$MD")"

# 1. fetch
echo "==> fetching $URL"
curl -fsSL --compressed -A "Mozilla/5.0" "$URL" -o "$HTML"
echo "    saved $HTML ($(wc -c < "$HTML") bytes)"

# 2. extract
echo "==> extracting Markdown"
EXTRACT_FLAGS=()
[ "$KEEP_FRONT" -eq 0 ] && EXTRACT_FLAGS+=(--strip-front-matter)
python3 "$(dirname "$0")/extract.py" "$HTML" "$MD" "${EXTRACT_FLAGS[@]}"

# 3. derive title
if [ -z "$TITLE" ]; then
  TITLE=$(grep -m1 -E '^# ' "$MD" | sed -E 's|^# +||')
fi
[ -n "$TITLE" ] || { echo "error: could not derive title; pass --title" >&2; exit 2; }
echo "    title: $TITLE"

# 4. check lark-cli auth
echo "==> checking lark-cli auth"
if ! command -v lark-cli >/dev/null 2>&1; then
  echo "error: lark-cli not installed. See references/setup.md" >&2
  exit 3
fi
lark-cli auth status >/dev/null || {
  echo "error: lark-cli user identity not ready. Run: lark-cli auth login" >&2
  exit 3
}

# 5. create sub-doc
echo "==> creating sub-doc under $PARENT"
CREATE_OUT=$(tail -n +2 "$MD" | lark-cli docs +create \
  --parent-token "$PARENT" \
  --title "$TITLE" \
  --doc-format markdown \
  --content -)
echo "$CREATE_OUT" | python3 -m json.tool >/dev/null 2>&1 || {
  echo "error: lark-cli create returned non-JSON:" >&2
  echo "$CREATE_OUT" >&2
  exit 4
}

NEW_URL=$(printf '%s' "$CREATE_OUT" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['document']['url'])")
echo "    new doc: $NEW_URL"

# 6. verify parent now lists the new sub-page
echo "==> verifying parent wiki sub-page list"
PARENT_FETCH=$(lark-cli docs +fetch --doc "$PARENT")
if printf '%s' "$PARENT_FETCH" | grep -qF "$TITLE"; then
  echo "    ✅ parent wiki lists the new sub-page"
else
  echo "    ⚠️  parent wiki does not yet list '$TITLE' (may need a moment)"
fi

echo ""
echo "✅ done"
echo "   archive:   $HTML / $MD"
echo "   new doc:   $NEW_URL"
echo "   parent:    $PARENT"
