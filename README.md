# t-skills

净霆的创业工具箱，服务于创业、思考、决策、自媒体创作等真实场景。

可在 Claude Code、Codex、Cursor、Trae Solo 等任意支持 skill / system prompt 的 Agent 上使用。

**当前版本：v1.0.0**

**所有内容开放，可以整套装，也可以只拿一部分。单个 skill 都能独立用。**

## 如何安装 t-skills

#### Claude Code

```
claude plugin marketplace add jingting969/t-skills
claude plugin install t-skills
```

#### 通用安装方式（适用于 Codex / Claude Code）

```
npx -y skills add jingting969/t-skills -g --all
```

#### Trae Solo

Trae Solo 一个 zip 装一个 skill。从 [GitHub Releases](https://github.com/jingting969/t-skills/releases) 下载最新的 `t-skills-版本号.zip`，解压后里面是独立的 skill zip（每个 zip 解压后根级是 `SKILL.md`），逐个拖进 Trae Solo 的「上传技能」窗口即可。

如果想本地构建，运行 `bash tools/build-skills.sh`，产物在 `dist/skills/`。

## 如何更新 t-skills

#### Claude Code 插件市场安装的用户

```
claude plugin marketplace update t-skills
claude plugin update t-skills
/reload-plugins
```

#### 通过 `npx skills add` 安装的用户

重新运行一次同样的命令即可。安装和更新用的是同一条命令，不需要换成别的写法。

```
npx -y skills add jingting969/t-skills -g --all
```

## 工具箱

### 思维工具

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-game-thinking` | 博弈思考助手。用博弈论框架拆解冲突、谈判、竞争与决策场景。不适用于与挚爱至亲的日常相处 | `/t-game-thinking` |

### 工具

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-handoff` | 对话交接。把当前对话压缩成交接文档，让另一个 agent 无缝接手继续工作 | `Use Skill: t-handoff` |
| `t-productize-you` | 能力产品化。把经历和能力转成可试卖的咨询、课程、陪跑产品，含三级定价和销售验证方案 | `Use Skill: t-productize-you` |
| `t-url-to-feishu-doc` | URL → 飞书 wiki。把任意公开 URL 抓取并提取为干净 Markdown，作为子文档写入指定的飞书 wiki 父节点 | `Use Skill: t-url-to-feishu-doc` |
| `t-wechat-rewrite` | 转述型公众号长文写作。把任意原文（文章、书摘、播客逐字稿等）转成3000字以上的公众号长文，支持4种文章结构 | `Use Skill: t-wechat-rewrite` |

### 技能之间的关系

```
t-game-thinking（分析博弈局面）
 ↓
t-handoff（把分析结论交接给下一个 agent 继续工作）
 ↓
t-productize-you（把能力转成可试卖产品，验证能不能卖）
```

t-game-thinking 分析完一个博弈场景后，如果需要换一个会话继续深入，可以用 t-handoff 把当前分析结论和上下文打包成交接文档，新会话打开即可接上。

## 设计理念

1. **一个 skill 只做一件事**：每个 skill 聚焦一个思维工具，不混装。装一个用一个，不需要整套。
2. **能用就行**：skill 的价值在于帮用户做决策，不在于展示理论。每个 skill 都有明确的执行流程和输出模板。
3. **有边界**：每个 skill 都标注了"不适用"的场景。比如 t-game-thinking 明确说对挚爱至亲不博弈。
4. **可组合**：skill 之间可以串联。博弈分析完交接给下一个 agent，各司其职。
5. **面向真实场景**：创业、思考、人生成长、自媒体创作——技能不是理论展示，而是帮你在这些场景里做判断、拿结果。

## 项目结构

```
t-skills/
├── .claude-plugin/
│   └── plugin.json              # Claude Code 插件配置
├── skills/
│   ├── t-game-thinking/
│   │   └── SKILL.md             # 博弈思考助手
│   ├── t-handoff/
│   │   ├── SKILL.md             # 对话交接
│   │   └── agents/
│   │       └── openai.yaml      # OpenAI agent 配置
│   └── t-wechat-rewrite/
│       ├── SKILL.md             # 转述型公众号写作
│       └── STYLE.md             # 写作风格规则
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
4. 如需可选子目录，支持 `templates/`、`scaffold/`、`docs/`、`tools/`、`scripts/`、`agents/`
5. 运行 `bash tools/build-skills.sh` 验证构建

### SKILL.md 格式

```markdown
---
name: "<skill-name>"
description: |
  <技能做什么>。
  触发方式：<触发词和短语>
---

# <Skill Title>

<正文内容>
```

## 许可证

本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可证。

- 个人使用、学习、研究、非商业项目：不需要署名，不需要申请
- 公开发布衍生作品（文章、工具、课程等）：请注明来源
- 商业用途：需要单独授权
