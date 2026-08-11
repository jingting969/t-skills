---
name: t-wechat-video-download
description: |
  微信视频号视频下载的使用指引。本 skill 不自带可执行代码——它告诉用户如何安装上游的 redfox-data/redfox-community 仓库的 wechat-video-downloader skill、如何获取 redfox.hk API Key、如何完成配置。当用户说「视频号下载」「wechat 视频号」「视频号无水印下载」时触发。
---

# t-wechat-video-download

## 这是什么

这是一个**使用指引型** skill，不包含可执行代码。它的作用是：把"微信视频号视频下载"这件事拆成"装上游 skill + 拿 API Key + 配上环境变量"三步，告诉您怎么做。

## 为什么是「指引」而不是 fork

视频下载能力来自 [redfox-data/redfox-community](https://github.com/redfox-data/redfox-community) 仓库的 `wechat-video-downloader` skill，由 redfox-data 团队开发维护。

该上游仓库**未提供明确的 LICENSE 文件**（截至本 skill 创建时）。在 LICENSE 明确之前，把上游代码按本仓库的 CC BY-NC 4.0 协议再分发存在法律不确定性。所以本 skill 选择**只做指引，不复制代码**。

## 三步上手

### 1. 装上游 skill

```bash
npx skills add redfox-data/redfox-community --skill wechat-video-downloader
```

装上之后，您机器上的 `~/.agents/skills/wechat-video-downloader/` 会有 skill 文件。Claude Code / Codex / Cursor / Gemini CLI 等支持 skills 协议的 agent 都能识别。

### 2. 拿 API Key

视频解析需要 redfox.hk 的 API：

1. 打开 [https://redfox.hk/settings/api-keys?source=github](https://redfox.hk/settings/api-keys?source=github)
2. 注册 / 登录
3. 创建 API Key（新用户约 10000 次免费额度）

### 3. 配 API Key

**方式 A：环境变量**（推荐）

```bash
export REDFOX_API_KEY='ak_您的Key'
```

放到 `~/.zshrc` 或 `~/.bashrc` 让所有新 shell 自动加载。

**方式 B：配置文件**（持久化）

写到 `~/.openclaw/openclaw.json`：

```json
{
  "redfox_api_key": "ak_您的Key"
}
```

**方式 C：macOS Keychain**（最安全）

```bash
security add-generic-password -a redfox_api_key -s redfox -w 'ak_您的Key'
```

Key 只在 Keychain 加密存储，shell history / 配置文件都看不到。

## 用法

安装并配置完成后，粘贴视频号分享链接给 agent：

```
Use Skill: wechat-video-downloader
https://weixin.qq.com/sph/xxxxxx
```

支持的链接格式：`https://weixin.qq.com/sph/xxxxxx`

## 不适用

- 不是视频号平台（抖音/小红书/B 站/快手）：需要装上游仓库对应的 `video-downloader` 或 `xiaohongshu-video-downloader` 等其他 skill
- 没有 redfox.hk API Key：跑不通，会报「未配置 API Key」

## 致谢

视频下载能力由 [redfox-data](https://github.com/redfox-data) 团队的 [redfox-community](https://github.com/redfox-data/redfox-community) 仓库提供。本仓库仅做集成指引，未修改或分发上游代码。