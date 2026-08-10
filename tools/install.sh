#!/usr/bin/env bash
# install.sh — 一键安装 t-skills
# 不依赖 npx：直接 git clone 仓库，把 skill 实体落到 ~/.agents/skills/，
# 给 6 个 agent 工具建软链。
#
# 用法：
#   curl -fsSL https://raw.githubusercontent.com/jingting969/t-skills/main/tools/install.sh | bash
#   SKILLS_DIR=~/my-skills bash install.sh
#   T_SKILLS_REPO=fork/your-fork bash install.sh

set -euo pipefail

SRC_DIR="${SKILLS_DIR:-$HOME/.agents/skills}"
REPO="${T_SKILLS_REPO:-jingting969/t-skills}"

# --- 检查依赖 ---
if ! command -v git >/dev/null 2>&1; then
  echo "error: git command is required" >&2
  exit 1
fi

# --- clone 仓库到临时目录 ---
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ 克隆 $REPO ..."
git clone --depth=1 --quiet "https://github.com/$REPO.git" "$TMP/repo"

# --- 把每个 t-* skill 实体搬到 ~/.agents/skills/ ---
mkdir -p "$SRC_DIR"
echo "→ 实体安装到 $SRC_DIR ..."
shopt -s nullglob
installed=0
for skill_dir in "$TMP/repo"/skills/t-*; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name="$(basename "$skill_dir")"
  rm -rf "$SRC_DIR/$name"
  cp -R "$skill_dir" "$SRC_DIR/$name"
  echo "  ✓ $name"
  installed=$((installed + 1))
done

if [ "$installed" -eq 0 ]; then
  echo "error: 仓库里没找到任何 skill（skills/t-*/SKILL.md），请检查仓库结构" >&2
  exit 1
fi

# --- 给其他 agent 建软链 ---
# universal agent 的 skills 目录：~/.agents/skills/ 已经是事实标准，
# 每个 agent 工具的本地目录放软链，指向 universal 实体。
# 用平行数组而不是关联数组（关联数组的 key 在 declare -A 里也会被
# bash 当变量名求值，遇到带连字符/下划线的 key 容易触发 set -u）。
AGENT_NAMES=(
  "Claude Code"
  "Codex"
  "Cursor"
  "OpenCode"
  "Windsurf"
  "Gemini CLI"
)
AGENT_DIRS=(
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  "$HOME/.cursor/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.windsurf/skills"
  "$HOME/.gemini/skills"
)

echo "→ 给其他 agent 建软链 ..."
for i in "${!AGENT_DIRS[@]}"; do
  name="${AGENT_NAMES[$i]}"
  target="${AGENT_DIRS[$i]}"
  mkdir -p "$target"
  for skill in "$SRC_DIR"/t-*; do
    skill_name="$(basename "$skill")"
    ln -sfn "$skill" "$target/$skill_name"
  done
  echo "  ✓ $name → $target"
done

echo ""
echo "Done."
echo "  实体:    $SRC_DIR"
echo "  已安装:  $installed 个 skill"
echo "  更新:    重跑这条命令即可（链接会自动刷新）"
echo "  卸载:    rm -rf $SRC_DIR && rm -rf ~/.claude/skills/t-* ~/.codex/skills/t-* ~/.cursor/skills/t-* ~/.config/opencode/skills/t-* ~/.windsurf/skills/t-* ~/.gemini/skills/t-*"