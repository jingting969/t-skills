# t-skills

净霆的个人成长技能箱。把"思考、决策、变现、写作"这些事，做成 Claude / Cursor / Trae Solo 能直接调用的 skill。

**作者**：[X](https://x.com/jingting969)

**当前版本：v1.1.0**

**所有内容开放，可以整套装，也可以只拿一部分。单个 skill 都能独立用。**

---

## 最新更新（v1.1.0）

**新增**：
- `t-url-to-feishu-doc` — 把任意公开 URL 抓取并提取为干净 Markdown，作为子文档写入飞书 wiki

**修复**：
- `tools/build-skills.sh` 修复 `references/` 子目录未被打包的 bug（顺带让 `t-productize-you` 的 references 也能正确打包）

## 最新更新（v1.0.0）

**首发 5 个 skill**：
- `t-game-thinking` — 博弈论思考助手
- `t-handoff` — 对话交接
- `t-productize-you` — 能力产品化
- `t-wechat-rewrite` — 转述型公众号写作
- `t-url-to-feishu-doc` — URL → 飞书 wiki（在 v1.1.0 正式入库）

---

## 我适合谁？

你大概率需要 t-skills，如果你符合下面任意一条：

- **每次遇到重大决策都在原地打转** → 用 `t-game-thinking` 拆局
- **能力很强但不知道怎么卖** → 用 `t-productize-you` 做产品设计
- **想持续做公众号但每周选题就是噩梦** → 用 `t-wechat-rewrite` 转述你读到的内容
- **收藏了一堆网页/文档，想沉到自己的飞书知识库** → 用 `t-url-to-feishu-doc` 一键入库
- **和 AI 聊到一半被迫换 session，重要上下文全丢了** → 用 `t-handoff` 做交接

你不一定需要，如果你符合下面任意一条：

- 你只用 ChatGPT 网页版，没用过 Claude Code / Cursor / Trae Solo
- 你不需要 AI 帮你做决策/写作/整理资料，只需要它回答问题
- 你对 "skill" 这个概念没兴趣

---

## 工具箱（按使用场景分组）

### 做决策

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-game-thinking` | 博弈思考助手。用博弈论框架拆解冲突、谈判、竞争与决策场景。**不适用**：与挚爱至亲的日常相处 | `/t-game-thinking`、`Use Skill: t-game-thinking` |

### 把能力变成钱

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-productize-you` | 能力产品化。从证据出发，把经历和能力转成可试卖的咨询、课程、陪跑产品 | `Use Skill: t-productize-you` |

### 写东西

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-wechat-rewrite` | 转述型公众号长文写作。把任意原文（文章、书摘、播客逐字稿）转成 3000 字以上的公众号长文 | `Use Skill: t-wechat-rewrite` |
| `t-url-to-feishu-doc` | URL → 飞书 wiki。把任意公开 URL 抓取并提取为干净 Markdown，作为子文档写入飞书 wiki 父节点 | `Use Skill: t-url-to-feishu-doc` |

### 跨会话协作

| Skill | 做什么 | 触发方式 |
| --- | --- | --- |
| `t-handoff` | 对话交接。把当前对话压缩成交接文档，让另一个 agent 无缝接手继续工作 | `Use Skill: t-handoff` |

---

## 技能之间的关系

```
你遇到一个决策  →  t-game-thinking（拆局）
                        ↓ 拆完想换一个 agent 继续深入
                    t-handoff（打包当前上下文）
                        ↓ 想把"会拆局"这件事变现
                    t-productize-you（设计产品）

你读了一篇文章  →  t-wechat-rewrite（转述成公众号）
你看到一个 URL  →  t-url-to-feishu-doc（写到飞书）
```

不同 skill 之间可以串联，但**不强制**。你只用其中一个也完全 OK。

---

## 一键安装（不用懂技术）

如果你只是想用、不想折腾，挑一个最适合你的安装方式：

### 方式 1：Claude Code 插件市场（推荐，自动更新）

```bash
claude plugin marketplace add jingting969/t-skills
claude plugin install t-skills@t-skills
```

装完重启 Claude Code，输入 `Use Skill: t-...` 即可。

### 方式 2：一键安装到所有 agent（推荐，跨平台通用）

```bash
npx -y skills add jingting969/t-skills --all
```

**这会做什么**：
- 5 个 skill 全部装到 `~/.agents/skills/`（agent skills 通用目录）
- 自动给 73 个 agent 建软链（包括 Claude Code / Codex / Cursor / OpenCode / Windsurf / Gemini CLI 等），全部指向 `~/.agents/skills/`
- 也就是说：**装一次，所有 agent 都能用**

**支持的 flag**（`skills add --help`）：
- `--all`：= `-s '*' -a '*' -y`，跳过选 skill / 选 agent / 确认
- `-s <name>`：只装指定 skill（如 `-s t-game-thinking`）
- `-a <agent>`：只装到指定 agent
- `--copy`：复制文件而不是建软链

### 方式 3：Trae Solo

从 [GitHub Releases](https://github.com/jingting969/t-skills/releases) 下载最新的 `t-skills-版本号.zip`，解压后里面是独立的 skill zip（每个 zip 解压后根级是 `SKILL.md`），逐个拖进 Trae Solo 的「上传技能」窗口即可。

如果想本地构建：`bash tools/build-skills.sh`，产物在 `dist/skills/`。

### 怎么更新？

- **Claude Code 用户**：`claude plugin update t-skills@t-skills`，然后 `/reload-plugins`
- **方式 2 用户**：再跑一次 `npx -y skills add jingting969/t-skills --all` 即可

---

## 设计理念

1. **一个 skill 只做一件事**：装一个用一个，不需要整套。
2. **能用就行**：skill 的价值在于帮你做决策，不在于展示理论。每个 skill 都有明确的执行流程和输出模板。
3. **有边界**：每个 skill 都标注了"不适用"的场景。比如 `t-game-thinking` 明确说对挚爱至亲不博弈。
4. **可组合**：skill 之间可以串联，博弈分析完交接给下一个 agent，各司其职。
5. **普通用户也能装**：一键安装，不用懂代码、不用 clone 仓库。

---

## 项目结构

```
t-skills/
├── .claude-plugin/
│   └── plugin.json              # Claude Code 插件配置
├── skills/
│   ├── t-game-thinking/         # 博弈思考助手
│   ├── t-handoff/               # 对话交接
│   ├── t-productize-you/        # 能力产品化（含 references/ 案例库）
│   ├── t-url-to-feishu-doc/     # URL → 飞书 wiki
│   └── t-wechat-rewrite/        # 转述型公众号写作
├── tools/
│   └── build-skills.sh          # 构建打包脚本
├── .gitignore
├── LICENSE                      # CC BY-NC 4.0
├── README.md
└── VERSION                      # 当前版本号
```

---

## 如何开发新技能

1. 在 `skills/` 下创建新目录，命名为 `t-<skill-name>`
2. 在目录内创建 `SKILL.md`，包含 YAML frontmatter（`name` + `description`）和 Markdown 正文
3. 在 `.claude-plugin/plugin.json` 的 `skills` 数组中添加路径
4. 如需可选子目录，支持 `templates/`、`scaffold/`、`docs/`、`tools/`、`scripts/`、`references/`、`agents/`
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

---

## 许可证

本项目采用 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) 许可证。

- 个人使用、学习、研究、非商业项目：不需要署名，不需要申请
- 公开发布衍生作品（文章、工具、课程等）：请注明来源
- 商业用途：需要单独授权