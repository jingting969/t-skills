# t-wechat-video-download

微信视频号视频下载的使用指引。

视频下载能力来自 [redfox-data/redfox-community](https://github.com/redfox-data/redfox-community) 仓库的 `wechat-video-downloader` skill。本仓库仅做集成指引，不复制或修改上游代码——因为上游尚未提供明确的 LICENSE 文件。

完整步骤见 [`SKILL.md`](./SKILL.md)。

## 三步上手

1. `npx skills add redfox-data/redfox-community --skill wechat-video-downloader`
2. 去 [redfox.hk/settings/api-keys](https://redfox.hk/settings/api-keys?source=github) 拿 API Key
3. `export REDFOX_API_KEY='ak_xxx'` 或写到 `~/.openclaw/openclaw.json`

## 致谢

- 上游：[redfox-data/redfox-community](https://github.com/redfox-data/redfox-community)（by [redfox-data](https://github.com/redfox-data)）
- API：[redfox.hk](https://redfox.hk/)