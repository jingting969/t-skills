# t-skills

思维工具箱。用博弈论、决策科学等框架拆解真实场景，做成 Agent skill。

可在 Claude Code、Codex、Cursor、Trae Solo 等任意支持 skill / system prompt 的 Agent 上使用。

**当前版本：v1.0.0**

## 已有技能

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-game-thinking` | 博弈思维。用博弈论框架拆解真实决策场景，识别博弈结构，分析均衡与最优策略 | `/t-game-thinking`、`/博弈思维` |

## 如何安装

#### Claude Code

```
claude plugin marketplace add <your-github-username>/t-skills
claude plugin install t-skills
```

#### 通用安装方式（适用于 Codex / Claude Code）

```
npx -y skills add <your-github-username>/t-skills -g --all
```

#### Trae Solo

从 [GitHub Releases](https://github.com/<your-github-username>/t-skills/releases) 下载最新的 `t-skills-版本号.zip`，解压后里面是独立的 skill zip（每个 zip 解压后根级是 `SKILL.md`），逐个拖进 Trae Solo 的「上传技能」窗口即可。

如果想本地构建，运行 `bash tools/build-skills.sh`，产物在 `dist/skills/`。

## 项目结构

```
t-skills/
├── .claude-plugin/
│   └── plugin.json              # Claude Code 插件配置
├── skills/
│   └── t-game-thinking/
│       └── SKILL.md             # 博弈思维技能（YAML frontmatter + Markdown 正文）
├── tools/
│   └── build-skills.sh          # 构建打包脚本
├── .gitignore
├── LICENSE                      # CC BY-NC 4.0
├── README.md
└── VERSION                      # 当前版本号
```

## 如何开发新技能

1. 在 `skills/` 下创建新目录，命名为 `t-<skill-name>`
2. 在目录内创建 `SKILL.md`，包含 YAML frontmatter（`name` + `description`）和 Markdown 正文
3. 在 `.claude-plugin/plugin.json` 的 `skills` 数组中添加路径
4. 如需可选子目录，支持 `templates/`、`scaffold/`、`docs/`、`tools/`、`scripts/`
5. 运行 `bash tools/build-skills.sh` 验证构建

### SKILL.md 格式

```markdown
---
name: "<skill-name>"
description: |
  <技能做什么>。
  触发方式：<触发词和短语>
  <English description>
  Trigger: <English triggers>
---

# <Skill Title>

<正文内容>
```

## 许可证

本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可证。

- 个人使用、学习、研究、非商业项目：不需要署名，不需要申请
- 公开发布衍生作品（文章、工具、课程等）：请注明来源
- 商业用途：需要单独授权
