# 发布清单 — jingting969/productize-your-skills v0.1.0

> 你只要复制粘贴，按步骤走完，5 分钟内仓库就能上线。

## 第 0 步：解压包

我已经把整个仓库打包成 `productize-your-skills.zip`（26 KB，28 个文件）。

```bash
mkdir -p ~/Projects
cd ~/Projects
# 把 zip 拖进 ~/Projects 后：
unzip productize-your-skills.zip
mv productize-your-skills-pkg productize-your-skills
cd productize-your-skills
```

或者直接双击 zip，把解压出的 `productize-your-skills-pkg` 改名成 `productize-your-skills` 放到任意位置。

## 第 1 步：本地初始化并推送

```bash
cd ~/Projects/productize-your-skills

git init
git add .
git commit -m "feat: initial productize-your-skills skill v0.1.0"
git branch -M main
git remote add origin https://github.com/jingting969/productize-your-skills.git
git push -u origin main
```

预期结果：

- `git push` 成功
- 浏览器刷新仓库页能看到 22 个文件

## 第 2 步：配置仓库 Topics

打开 https://github.com/jingting969/productize-your-skills

点击右上角的 ⚙️ **Settings** → 左侧 **General** → 找到 **Topics** 字段，输入（一个一个回车添加）：

```
ai-agent-skills
codex
product-design
solopreneur
open-source
```

预期结果：仓库首页右上角出现 5 个蓝色标签。

## 第 3 步：配置 About（右上角齿轮）

同样在 General 页面，找到 **About** 区右侧的 ⚙️ 按钮，填入：

- **Description**：
  ```
  从个人经历与能力证据生成可试卖产品、三级定价和首批销售验证方案。Codex Agent Skill。
  ```
- **Website**：留空
- **Social preview**：先跳过，后续可上传
- 勾选 ✅ **Releases**
- 勾选 ✅ **Packages**
- 勾选 ❌ **Deployments**（不需要）
- 勾选 ❌ **Environments**（不需要）
- 勾选 ✅ **Discussions**（强烈建议，方便用户提问）

保存。

## 第 4 步：创建 v0.1.0 Release

打开 https://github.com/jingting969/productize-your-skills/releases/new

- **Choose a tag**：输入 `v0.1.0` → 点 **Create new tag: v0.1.0 on publish**
- **Target**：`main`
- **Release title**：`v0.1.0 — initial public release`
- **Description**（直接复制粘贴）：

````markdown
# v0.1.0 — initial public release

第一个公开版本。包含 9 步能力产品化流程和可持续迭代的案例库。

## ✨ 核心功能

- **能力产品化模式**：从"我觉得自己会"到"这是能卖的产品"
  - 9 步流程：建立目标 → 广泛盘点 → 证据提取 → 候选方向 → 五维评分 → 选择并产品化 → 三级定价 → 首次销售验证 → 分级交付
- **案例学习模式**：把你看到的成熟产品拆解并归档
  - 16 字段统一模板
  - 自动索引和校验
  - 案例库 CLI：`add_case.py` / `validate_case.py`
- **证据驱动**：E0–E5 证据等级 + 五维评分（能力证据、客户痛点、支付意愿、个人意愿、交付可控性）
- **三级定价**：试卖价 / 标准价 / 升级价，未经验证价格标为测试假设

## 📦 安装

把 `productize-your-skills/` 复制到 Codex 的 Skill 根目录之一：

- 全局：`~/.codex/skills/`
- 项目：`<project>/.codex/skills/`
- Codex desktop：`~/Library/Application Support/Codex/skills/`

重启 Codex 即可看到「能力产品化」Skill。

## 🧪 验证

```bash
python3 -m unittest discover -s tests -v   # 7/7 PASS
python3 scripts/validate_case.py            # Validated N case file(s)
```

## 📚 文档

- [README](https://github.com/jingting969/productize-your-skills/blob/main/README.md)
- [CONTRIBUTING](https://github.com/jingting969/productize-your-skills/blob/main/CONTRIBUTING.md)
- [CHANGELOG](https://github.com/jingting969/productize-your-skills/blob/main/CHANGELOG.md)

## 🤝 贡献

欢迎提交：

- 新的产品案例（按 `references/case-template.md` 提供 JSON）
- 改进证据评分规则
- 前向测试用例
- Bug 修复

详见 [CONTRIBUTING.md](https://github.com/jingting969/productize-your-skills/blob/main/CONTRIBUTING.md)。

## ⚖️ License

MIT
````

- 勾选 ✅ **Set as the latest release**
- 点 **Publish release**

预期结果：仓库首页出现 v0.1.0 Release 徽章。

## 第 5 步：发第一条 Discussion / 社交

打开仓库的 **Discussions** 标签 → **New discussion** → 选 **Show and tell** 类目：

标题：**征集 3 个真实可复盘的能力产品**

正文：

````markdown
## 为什么

这个 Skill 最缺的不是框架，是真实案例。

你有一个跑通过的能力产品（咨询 / 陪跑 / 课程 / 订阅 / 任何付费形式），愿意公开拆解吗？

## 我需要你提供

按 `references/case-template.md` 的 16 个字段填一份 JSON：

- 目标客户 + 购买情境
- 痛点 + 结果承诺
- 产品形态 + 交付机制 + 周期 + 边界
- 定价 + 价值锚点 + 信任证据
- 获客方式
- **可迁移结构**（别人能在不同背景上借鉴什么）
- **不可照搬条件**（避免误导）

## 收录标准

- 来源清晰：你自己的产品，或你拆解过的公开产品
- 字段完整
- 诚实标注可信度（高 / 中 / 低）

## 提交流程

1. 在本贴下回复贴出 JSON
2. 我会跑 `python3 scripts/validate_case.py` 校验
3. 通过后合并到 `references/cases/`

前 3 个有效案例会被收录到 README 的 "Featured Cases" 区。
````

---

## ✅ 全部完成后，你的仓库会有

- ✅ 22 个文件，README 带图片级项目结构
- ✅ 5 个 Topics：ai-agent-skills / codex / product-design / solopreneur / open-source
- ✅ About 描述 + Discussions 启用
- ✅ v0.1.0 Release 带详细说明
- ✅ 第一条 Discussion 征集案例
- ✅ 7/7 单元测试全绿
- ✅ Codex 官方 Skill 校验通过

预估时间：5 分钟。
