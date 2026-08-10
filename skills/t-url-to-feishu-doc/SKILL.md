---
name: t-url-to-feishu-doc
description: 把任意 URL 的内容（HTML 页面、官方文档等）提取为干净 Markdown，并在指定的飞书 wiki 父节点下新建一个子文档。触发场景：用户提供一个 URL + 飞书 wiki 父目录链接/节点 token，并要求把页面内容沉淀到飞书，例如"把这个链接提取出来写到飞书目录底下""把官方页存到 wiki 里""抓这个页面 push 到我的知识库"。
metadata:
  author: dashuai
  version: 0.1.0
---

# t-url-to-feishu-doc

> URL → 干净 Markdown → 飞书 wiki 子文档

## When to use

- 用户给一个 URL（必须是公开可抓的静态页）+ 飞书 wiki 父节点链接/token
- 用户说"提取这页内容写到飞书" / "push 到 wiki" / "存到我的知识库"
- **不适用**：需要登录的页面（用 web-access skill 走浏览器 CDP）；纯文本笔记/clipping（直接 `lark-cli docs +create`）

## Workflow

1. **确认 lark-cli user 身份**：跑 `lark-cli auth status`。如果 `user.status != "ready"`，先 `lark-cli auth login --no-wait --json` 启动设备流，把 URL/二维码给用户扫，授权完再 `lark-cli auth login --device-code <code>`。**bot 身份不能写文档**。
2. **拉取 URL 并提取**：直接跑 `scripts/publish.sh --url <URL> --parent <wiki-url-or-token>`。脚本会：
   - `curl` 抓 HTML → `.raw/pages/<slug>.html`
   - `scripts/extract.py` 转 Markdown → `.raw/text/<slug>.md`（自动剥本地 front matter）
   - 从 H1 推断标题
   - `lark-cli docs +create --parent-token <parent> --title <h1> --doc-format markdown --content -`
   - 抓父 wiki 确认新子页出现
3. **回报新子页 URL** 给用户。

**可选参数**：`--title` 覆盖默认 H1 标题；`--raw-dir` 改留底目录（默认 `./.raw`）；`--keep-front-matter` 不剥 front matter。

## Required env

- `lark-cli` 已装并在 PATH（`brew install lark-cli` 或 `npm i -g @larksuite/cli`），且 user 身份已授权 `wiki:node:*` / `docx:document:*` scopes
- `curl`、`python3`（stdlib only）

首次安装/授权步骤见 `references/setup.md`。

## Verification

- 脚本结束时打印 `new doc: https://my.feishu.cn/docx/...` 且父 wiki 子页列表里能看到新标题
- 本地留底：`.raw/pages/<slug>.html` + `.raw/text/<slug>.md` 双留底，可对照复核

## Notes

- 默认用 `curl` 抓静态页（Docusaurus/MkDocs/普通 HTML 都能处理）；如要 JS 渲染或登录态，请改用 `web-access` skill 走 CDP
- 单 block 写 4 KB / 整段 ~50 KB 限制，超长内容（如长 FAQ）需手动分段 append
- 飞书 Markdown 解析对表格/嵌套列表支持有限，提取后会简化排版——重要排版请发完手动调
- 父节点：传完整 wiki URL（`https://my.feishu.cn/wiki/...`）或 token 都行，lark-cli 会自动解析
