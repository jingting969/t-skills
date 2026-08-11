# 视频号视频下载 / wechat-video-downloader

---

## ⚠️ 来源与许可声明

本 skill 的代码（`SKILL.md`、`scripts/parse_video_download.py`、`references/`）**完整复制自** [redfox-data/redfox-community](https://github.com/redfox-data/redfox-community) 仓库的 `skills/wechat-video-downloader/`。

**重要事实：**

- 上游仓库**未提供明确的 LICENSE 文件**（截至本 skill 创建时）
- 按 [GitHub 默认规则](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)，未声明 LICENSE = **"All rights reserved"**
- 本仓库作者**未获得上游作者 [redfox-data](https://github.com/redfox-data) 团队的明确书面许可**
- 本仓库作者保留一切权利，但**不主张**对上游代码的任何权利
- 本仓库的**仓库级 LICENSE**（CC BY-NC 4.0）**仅约束本仓库作者新增的部分**（如有），**不延伸至上游复制的代码**

**风险与责任：**

- 如果您（使用者）需要在本仓库使用这些代码，请自行评估与 redfox-data 之间的合规问题
- 上游作者可能随时提 DMCA / 公开要求移除
- 推荐用法是**直接通过 `npx skills add redfox-data/redfox-community --skill wechat-video-downloader` 安装上游原版**——本仓库的存在仅为个人学习与备份用途

**改动记录：**

- `SKILL.md` 正文、description、references/、scripts/ 均为上游原文
- `SKILL.md` 字段 `name` 从上游 `wechat-video-downloader` 改名为 `t-wechat-video-download`（与本地安装目录名一致）
- `README.md` 顶部加本声明段；其余内容为上游原文

---

## 简介

粘贴一条视频号分享链接，直接拿到视频的真实下载地址，同时返回视频标题和封面图，方便归档管理。

**核心价值**

- **一键获取**：粘贴链接即可拿到高清无水印视频直链，无需额外操作
- **信息完整**：视频标题、封面图同步返回，便于素材归类与检索
- **批量支持**：一次可提交多条链接，提升素材收集效率

**适用对象**

- 🎬 **内容创作者** — 快速下载视频号素材用于二创剪辑
- 📊 **运营人员** — 保存竞品视频，分析内容策略
- ✂️ **剪辑师** — 高效获取高清源文件，提升工作流效率

---

## 功能特性

### 核心功能

- **直链解析**：获取视频的真实下载地址，可直接在浏览器打开或下载到本地
- **元信息附带**：自动返回视频标题和封面图，无需手动记录
- **即提即得**：提交链接后即时返回结果，无需排队等待

---

## 密钥获取与安全说明

- 本技能需要使用环境变量：`REDFOX_API_KEY`。
- `REDFOX_API_KEY` 由 [红狐 hub](https://redfox.hk/settings/api-keys?source=github) (`https://redfox.hk`)提供。
- 请前往 [红狐 hub](https://redfox.hk?source=github) 注册账号，获取 `REDFOX_API_KEY`。
- 配置设备环境变量 `REDFOX_API_KEY` 后使用本技能。
- 在提供密钥前，请先确认密钥来源、可用范围、有效期及是否支持重置/撤销。
- 禁止在代码、提示词、日志或输出文件中硬编码/明文暴露密钥。

---

## 使用指南

直接用自然语言描述需求，无需记忆命令。

### 常用说法速查

| 意图 | 示例话术 | 效果 |
| ---- | -------- | ---- |
| 解析单个视频 | 「帮我解析这个视频号链接：https://weixin.qq.com/sph/xxxx」 | 返回视频标题、封面图和下载地址 |
| 批量解析 | 「帮我解析这几个视频号链接」并粘贴多个链接 | 一次性返回所有视频的下载信息 |
| 下载视频 | 「下载这个视频号视频：https://weixin.qq.com/sph/xxxx」 | 直接给出可用的下载地址 |

### 输出示例

提交链接后，你将收到如下格式的结果：

**1. 标题**：视频标题
   **封面图**：[封面图](封面链接)
   **下载地址**：视频直链
   **操作**：[查看视频](视频直链)

> ⚠️ 视频号下载链接有效期约 **5 分钟**，请及时保存。

---

## 使用场景

| 场景 | 角色 | 示例问法 | 收益 |
| ---- | ---- | -------- | ---- |
| 素材收集 | 内容创作者 | 「帮我把这几个热门视频号的视频下载下来，我要做混剪」 | 批量获取高清素材，节省逐个下载时间 |
| 竞品分析 | 运营人员 | 「解析这个竞品视频号链接，保存视频和封面」 | 快速留存竞品内容，便于策略复盘 |
| 源文件获取 | 剪辑师 | 「下载这个视频号视频的原片，我要做后期处理」 | 直接拿到无水印高清源文件 |
| 日常归档 | 自媒体博主 | 「帮我把今天发的视频号视频下载备份」 | 一键归档，不丢失原始素材 |

---
