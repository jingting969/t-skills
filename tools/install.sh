#!/usr/bin/env bash
# install.sh — 一键安装 t-skills
# 实体落在 ~/.agents/skills/，其他 agent 工具目录全部建软链。set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${SKILLS_DIR:-$HOME/.agents/skills}"
REPO="${T_SKILLS_REPO:-jingting969/t-skills}"

# --- 检查依赖 ---
if ! command -v npx >/dev/null 2>&1; then
  echo "error: npx (Node.js) command is required" >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 command is required (used by npx skills)" >&2
  exit 1
fi

# --- 临时目录装一次拿到 skill 文件 ---
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# npx skills add 不接受自定义路径；装到默认位置后 mv 出来
echo "→ 下载 $REPO ..."
( cd "$TMP" && npx -y skills add "$REPO" ) >/dev/null

# 找到 t-* skill 实体（兼容 skills/ 子目录包裹）
extract_skills() {
  shopt -s nullglob
  # 情形 1：直接平铺
  for d in "$TMP"/t-*; do
    [ -f "$d/SKILL.md" ] && echo "$d" && return
  done
  # 情形 2：包在 skills/ 下
  for d in "$TMP"/skills/t-*; do
    [ -f "$d/SKILL.md" ] && echo "$d" && return
  done
  return 1
}

SKILL_DIRS=()
shopt -s nullglob
for d in "$TMP"/t-*; do [ -f "$d/SKILL.md" ] && SKILL_DIRS+=("$d"); done
for d in "$TMP"/skills/t-*; do [ -f "$d/SKILL.md" ] && SKILL_DIRS+=("$d"); done

if [ "${#SKILL_DIRS[@]}" -eq 0 ]; then
  echo "error: 没从 $REPO 抓到任何 skill，请检查网络或仓库是否正确" >&2
  exit 1
fi

# --- 实体搬到 ~/.agents/skills/ ---
mkdir -p "$SRC_DIR"
echo "→ 实体安装到 $SRC_DIR ..."
for d in "${SKILL_DIRS[@]}"; do
  name="$(basename "$d")"
  rm -rf "$SRC_DIR/$name"
  mv "$d" "$SRC_DIR/$name"
  echo "  ✓ $name"
done

# --- 给其他 agent 建软链 ---
declare -A AGENT_DIRS=(
  [Claude Code]="$HOME/.claude/skills"
  [Codex]="$HOME/.codex/skills"
  [Cursor]="$HOME/.cursor/skills"
  [OpenCode]="$HOME/.config/opencode/skills"
  [Windsurf]="$HOME/.windsurf/skills"
  [Gemini CLI]="$HOME/.gemini/skills"
)

echo "→ 给其他 agent 建软链 ..."
for name in "${!AGENT_DIRS[@]}"; do
  target="${AGENT_DIRS[$name]}"
  mkdir -p "$target"
  for skill in "$SRC_DIR"/t-*; do
    skill_name="$(basename "$skill")"
    ln -sfn "$skill" "$target/$skill_name"
  done
  echo "  ✓ $name → $target"
done

echo ""
echo "Done."
echo "  实体:  $SRC_DIR"
echo "  更新:  bash $ROOT_DIR/tools/install.sh  （再跑一次即可，链接自动刷新）"
echo "  卸载:  rm -rf $SRC_DIR && rm -rf ${AGENT_DIRS[*]}"