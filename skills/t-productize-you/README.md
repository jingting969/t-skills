# productize-your-skills

> 从个人经历与能力证据生成可试卖产品、三级定价和首批销售验证方案。

![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue)

## 安装

### Codex

```bash
git clone https://github.com/jingting969/productize-your-skills.git
cp -R productize-your-skills ~/.codex/skills/
```

Skill 根目录：

- 全局：`~/.codex/skills/`
- 项目：`<project>/.codex/skills/`
- Desktop：`~/Library/Application Support/Codex/skills/`

### Claude Code

Claude Code Skills 路径：`~/.claude/skills/<name>/SKILL.md`。

```bash
# 全局
mkdir -p ~/.claude/skills
cp -R productize-your-skills ~/.claude/skills/productize-your-skills

# 项目
mkdir -p .claude/skills
cp -R productize-your-skills .claude/skills/productize-your-skills
```

### Cursor

Cursor 规则是「每次回答都自动读取」，所以**只复制 `SKILL.md` 主入口**。

```bash
# 项目
mkdir -p .cursor/rules
cp productize-your-skills/SKILL.md .cursor/rules/productize.mdc

# 全局
mkdir -p ~/.cursor/rules
cp productize-your-skills/SKILL.md ~/.cursor/rules/productize.mdc
```

> Cursor 是否支持 `.cursor/skills/` 目录待官方文档确认。如果你已在 Cursor 实测可用，欢迎开 PR 补全 README。

### Trae

```bash
# 项目
mkdir -p .trae/skills
cp -R productize-your-skills .trae/skills/

# 全局
mkdir -p ~/.trae/skills
cp -R productize-your-skills ~/.trae/skills/
```

### OpenCode

```bash
mkdir -p ~/.opencode/skills
cp -R productize-your-skills ~/.opencode/skills/
```

### 其他工具

如果你的工具支持"自定义系统提示"或"项目规则"，把 `SKILL.md` 粘进去即可：

```bash
cat productize-your-skills/SKILL.md
```

参考位置：

- GitHub Copilot → 仓库 Settings → Copilot → Instructions
- Windsurf → Settings → Rules → Global Rules
- ChatGPT → Custom GPT / Project → Instructions
- Cline / Continue → `.clinerules` / `.continuerules`
- Zed → `.zed/rules`
- JetBrains AI → Settings → AI Assistant → 项目规则

## 使用

### 能力产品化模式

对 AI 说：

- 我不知道自己能卖什么
- 我会很多事但不知道怎么收费
- 帮我设计咨询 / 陪跑 / 课程 / 订阅

Skill 按 9 步走：建立目标 → 广泛盘点 → 证据提取 → 候选方向（最多 3 个）→ 五维评分 → 选择并产品化 → 三级定价 → 首次销售验证 → 分级交付。

### 案例学习模式

对 AI 说：**这是我设计好的产品，帮我拆解并加入案例库。**

Skill 流程：确认来源和许可 → 按 16 字段模板拆解 → 区分可迁移结构与不可照搬条件 → 写入 `references/cases/` 并重建索引。

### 案例库 CLI（可选）

```bash
python3 scripts/add_case.py /path/to/case.json
python3 scripts/validate_case.py
```

## 项目结构

```text
productize-your-skills/
├── SKILL.md                    # 主入口（所有 AI 工具都读这个）
├── references/                 # 按需读取的方法论
├── scripts/                    # 案例库 CLI（跨工具）
├── tests/                      # 单元测试 + 前向测试
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── .gitignore
```

## 开发与验证

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_case.py
```

前向行为测试用例见 `tests/prompts.md`。

## 贡献

见 `CONTRIBUTING.md`。欢迎补充新工具的实测安装路径或新案例。

## License

MIT
