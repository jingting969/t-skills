#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-"$ROOT_DIR/dist/skills"}"
VERSION="$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 command is required" >&2
  exit 1
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

INNER_DIR="$(mktemp -d)"
trap 'rm -rf "$INNER_DIR"' EXIT

# skill 名 -> 分组目录
group_for() {
  case "$1" in
    t-game-thinking)
      echo "思维工具" ;;
    t-handoff)
      echo "工具" ;;
    *)
      echo "未分组" ;;
  esac
}

build_one() {
  local skill_dir="$1"
  local name
  local group
  local stage_dir
  local target_dir
  name="$(basename "$skill_dir")"
  group="$(group_for "$name")"
  target_dir="$INNER_DIR/$group"
  mkdir -p "$target_dir"

  stage_dir="$(mktemp -d)"
  cp "$skill_dir/SKILL.md" "$stage_dir/SKILL.md"

  # 复制可选子目录
  for subdir in templates scaffold docs tools scripts; do
    if [ -d "$skill_dir/$subdir" ]; then
      mkdir -p "$stage_dir/$subdir"
      cp -R "$skill_dir/$subdir/." "$stage_dir/$subdir/"
    fi
  done

  python3 - "$stage_dir" "$target_dir/${name}.zip" <<'PY'
import os
import sys
import zipfile

source_dir, archive_path = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for root, _, files in os.walk(source_dir):
        for filename in files:
            path = os.path.join(root, filename)
            archive.write(path, os.path.relpath(path, source_dir))
PY

  rm -rf "$stage_dir"
  echo "built $group/${name}.zip"
}

for skill_md in "$ROOT_DIR"/skills/*/SKILL.md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  if [[ "$skill_name" == *beta* ]]; then
    echo "skipped local-only beta skill: $skill_name"
    continue
  fi
  build_one "$skill_dir"
done

cat > "$INNER_DIR/README.md" <<EOF
# t-skills ${VERSION}

Trae Solo 一个 zip 装一个 skill。本压缩包按使用场景分了几个文件夹，按需把里面的 zip 逐个拖进 Trae Solo 的「上传技能」窗口即可。

## 思维工具
- **t-game-thinking** — 博弈思维。用博弈论框架拆解真实决策场景，识别博弈结构，分析均衡与最优策略。

---
每个 zip 解压后根级是 SKILL.md（带 YAML frontmatter，含 name + description），格式遵循 Anthropic Skills 规范。
EOF

python3 - "$INNER_DIR" "$OUT_DIR/t-skills-${VERSION}.zip" <<'PY'
import os
import sys
import zipfile

inner_dir, archive_path = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for root, _, files in os.walk(inner_dir):
        for filename in sorted(files):
            path = os.path.join(root, filename)
            archive.write(path, os.path.relpath(path, inner_dir))
PY

echo
echo "done: $OUT_DIR/t-skills-${VERSION}.zip"
