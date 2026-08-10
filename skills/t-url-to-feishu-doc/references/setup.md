# lark-cli 安装与授权

## 安装

任选一种：

```bash
# Homebrew（macOS）
brew install lark-cli

# npm（任何平台）
npm install -g @larksuite/cli
```

验证：

```bash
lark-cli --version   # 期望 1.0.x 或更新
```

## 授权（user 身份）

`lark-cli docs +create / +update` 等写操作需要 **user 身份**（bot 身份只能做租户级 API 调用）。首次使用：

```bash
# 1. 启动设备流（立即返回 URL + 二维码）
lark-cli auth login --no-wait --json --domain wiki,docs

# 2. 拿返回的 verification_url 转成二维码给用户扫
lark-cli auth qrcode <verification_url> --output /tmp/qr.png

# 3. 用户在飞书 App 扫码授权后，跑：
lark-cli auth login --device-code <上一步返回的 device_code>

# 4. 验证
lark-cli auth status | grep '"user"' -A3   # 期望 status: ready
```

## Token 失效

`user.tokenStatus == "expired"` 时：

- refresh token 还在（expiresAt 内）：直接重跑 `lark-cli auth login --device-code ...` 即可续期
- refresh token 也过期了：必须重新走设备流

## 权限范围

最少需要：

- `docx:document:create` / `docx:document:write_only`
- `wiki:node:read` / `wiki:node:create` / `wiki:node:retrieve`
- `wiki:space:read`
- `offline_access`（拿 refresh token）

`--domain wiki,docs` 会自动请求 wiki + docs 域下推荐的 scopes，够用。

## 常见问题

| 错误 | 原因 | 修法 |
|---|---|---|
| `invalid value "md" for --doc-format` | lark-cli 只认 `xml` 或 `markdown` | 用 `--doc-format markdown` |
| `User identity: missing (refresh token expired)` | refresh token 过期 | 重跑设备流 |
| `parent_token 解析失败` | token 拼错或无权限 | 确认 `--parent-token` 用 wiki node token（`VmvDwCY8ei8grpkpFegcxgkLn7e` 这种），不是 docx token |
| 写入报 content too long | 单段超长 | 先确认内容 < 50 KB；超长改用 `+create` 一次写后 `+update append` 分段补 |
