# 更新日志

所有值得注意的变更都会记录在这里。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [0.1.7] - 2026-07-14

### 新增

- `docs/retrospectives/2026-07-14-readme-facts.md` 复盘文档：v0.1.0 → v0.1.6 期间 5 次事实错误的根因、原则、自检表
- `CONTRIBUTING.md` 新增「事实纪律」章节，要求所有贡献者遵守 R1–R7 原则

## [0.1.6] - 2026-07-14

### 变更

- 删除 `agents/openai.yaml` 文件和 `agents/` 目录
- 原因：未在 Codex 官方文档（openai/codex 仓库）核实到此文件名是 Codex 运行时实际读取的约定
- README 项目结构同步移除

## [0.1.5] - 2026-07-14

### 修正

- README 大幅精简：263 → 145 行
- 删除「它解决什么问题」整节（讲故事，不是安装文档该有的内容）
- 删除 Claude Code 「关于旧的 .claude/commands/」段（兼容细节，99% 用户不关心）
- 删除 Cursor「Skills 模式 vs Rules 模式」长段（两种路径都未完全验证，先只给一种）
- 删除「为什么是通用」「好消息」「你正在看的这个」等元评论
- 工具支持矩阵合并进各工具安装小节
- Cursor `.cursor/skills/` 改为待官方文档确认（之前推断）
- 删除「Agent Skills 开放标准」tagline 段（避免重复）
- 删除项目结构里自指注释
- 设计原则「工具中立」和「遵循开放标准」合并/删除

## [0.1.4] - 2026-07-14

### 修正

- 删除 README 中「为什么是通用」整节
- 删除顶部「好消息」段落
- README 回归简洁的安装文档形态

## [0.1.3] - 2026-07-14

### 修正

- Claude Code 章节改用 Skills 路径 `~/.claude/skills/<name>/SKILL.md`
- 删除 Subagent / Slash Command 旧说法
- 顶部对齐 Agent Skills 开放标准
- Cursor 改用 `.cursor/skills/`

## [0.1.2] - 2026-07-14

### 变更

- README 重写为「先回答能不能用，再回答怎么用」
- 新增工具支持矩阵表

## [0.1.1] - 2026-07-14

### 变更

- README 从「Codex 专属」改为「跨工具通用 Skill」

## [0.1.0] - 2026-07-14

### 新增

- 能力产品化模式：9 步产品化流程
- 案例学习模式：可持续迭代的产品案例库
- 证据等级 E0–E5 与五维评分
- 三级定价（试卖 / 标准 / 升级）
- 完整产品方案 / 试卖方案 / 最小可测试产品输出模板
- 7 项单元测试 + 5 组前向行为测试
- 案例库 CLI（add / validate）和自动索引

[0.1.0]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.0
[0.1.1]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.1
[0.1.2]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.2
[0.1.3]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.3
[0.1.4]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.4
[0.1.5]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.5
[0.1.6]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.6
[0.1.7]: https://github.com/jingting969/productize-your-skills/releases/tag/v0.1.7
