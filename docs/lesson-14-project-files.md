# 关卡 14：GitHub/Gitea 项目文件规范

**所属阶段**：进阶操作
**本关关键词**：README、CONTRIBUTING、LICENSE、SECURITY、CODEOWNERS、.github

---

## 一、本关目标

- 学会编写规范的 README.md。
- 理解 CONTRIBUTING.md、SECURITY.md 等文件的作用。
- 了解开源许可证的选择。
- 掌握 `.github` 目录结构和特殊文件。

学完这一关，你就能为项目添加完善的文档，让它更专业、更受欢迎。

---

## 二、前置条件

- 已完成关卡 01-03（Git 基础操作）。
- 熟悉 Markdown 语法。
- 有一个 GitHub 或 Gitea 仓库用于练习。

---

## 三、边看边做前先理解的项目文件概览

| 文件                 | 作用       | 显示位置           |
| -------------------- | ---------- | ------------------ |
| `README.md`          | 项目说明   | 仓库首页           |
| `CONTRIBUTING.md`    | 贡献指南   | 创建 PR 时显示链接 |
| `LICENSE`            | 许可证     | 仓库侧边栏         |
| `SECURITY.md`        | 安全政策   | 安全报告页面       |
| `CODEOWNERS`         | 代码所有者 | 自动分配 Reviewer  |
| `CODE_OF_CONDUCT.md` | 行为准则   | 社区页面           |

### `.github` 目录结构

```
.github/
├── CONTRIBUTING.md      # 贡献指南
├── SECURITY.md          # 安全政策
├── CODEOWNERS           # 代码所有者
├── CODE_OF_CONDUCT.md   # 行为准则
├── ISSUE_TEMPLATE/      # Issue 模板
│   ├── bug_report.md
│   └── feature_request.md
├── PULL_REQUEST_TEMPLATE.md  # PR 模板
├── FUNDING.yml          # 赞助信息
└── workflows/           # GitHub Actions
    └── ci.yml
```

---

## 四、边看边做：README.md 编写规范

### 步骤 1：创建基础 README

```bash
# 在项目根目录创建 README.md
```

README.md 标准结构：

```markdown
# 项目名称

简短的项目描述（1-2 句话）

## 徽章

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)
[![Build](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)

## 特性

- 特性 1
- 特性 2
- 特性 3

## 快速开始

### 安装

```bash
npm install my-project
```

### 使用

```javascript
const myProject = require('my-project');
myProject.doSomething();
```

## 文档

详细文档请访问 [Documentation](https://example.com/docs)

## 贡献

欢迎贡献！请阅读 [贡献指南](CONTRIBUTING.md)

## 许可证

[MIT](../LICENSE) © Your Name
```

### 步骤 2：添加徽章

常用徽章来源：

- [shields.io](https://shields.io/) - 自定义徽章
- GitHub Actions 构建状态
- npm 包版本
- 许可证类型

示例：

```markdown
[![GitHub Actions](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)
[![npm version](https://badge.fury.io/js/package.svg)](https://badge.fury.io/js/package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

---

## 五、CONTRIBUTING.md 贡献指南

### 步骤 3：创建贡献指南

```markdown
# 贡献指南

感谢你考虑为本项目做出贡献！

## 如何贡献

### 报告 Bug

1. 在 Issues 中搜索是否已有相同问题
2. 如果没有，创建新 Issue，包含：
   - 清晰的标题
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息

### 提交代码

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

## 代码规范

- 使用 2 空格缩进
- 遵循 ESLint 规则
- 为新功能添加测试

## 提交信息规范

使用约定式提交：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 重构

## 开发环境设置

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
npm install
npm test
\`\`\`
```

---

## 六、LICENSE 许可证选择

### 步骤 4：选择并添加许可证

常见开源许可证对比：

| 许可证       | 商用 | 修改 | 专利 | 声明     | 推荐场景     |
| ------------ | ---- | ---- | ---- | -------- | ------------ |
| MIT          | ✅    | ✅    | ❌    | 保留声明 | 最宽松，推荐 |
| Apache 2.0   | ✅    | ✅    | ✅    | 保留声明 | 企业项目     |
| GPL 3.0      | ✅    | ✅    | ❌    | 必须开源 | 开源项目     |
| BSD 3-Clause | ✅    | ✅    | ❌    | 保留声明 | 类似 MIT     |

### 添加 MIT 许可证

```text
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 七、SECURITY.md 安全政策

### 步骤 5：创建安全政策

```markdown
# 安全政策

## 支持的版本

| 版本  | 支持状态     |
| ----- | ------------ |
| 2.x   | ✅ 支持       |
| 1.x   | ⚠️ 仅安全更新 |
| < 1.0 | ❌ 不再支持   |

## 报告安全漏洞

如果你发现了安全漏洞，请**不要**在公开 Issue 中报告。

请发送邮件至：security@example.com

包含以下信息：
- 漏洞描述
- 复现步骤
- 可能的影响
- 建议的修复方案（如果有）

我们承诺：
- 48 小时内确认收到
- 7 天内评估严重程度
- 90 天内修复或发布缓解措施
```

---

## 八、CODEOWNERS 代码所有者

### 步骤 6：创建 CODEOWNERS

```text
# CODEOWNERS 文件
# 每行格式：pattern @owner1 @owner2

# 默认所有者
* @maintainer

# 前端代码
/frontend/ @frontend-team @alice

# 后端代码
/backend/ @backend-team @bob

# 文档
/docs/ @documentation-team

# CI 配置
.github/ @devops-team
```

效果：
- 自动为 PR 分配 Reviewer
- 文件变更时会通知对应的 Owner

---

## 九、Issue 和 PR 模板

### 步骤 7：创建 Issue 模板

创建 `.github/ISSUE_TEMPLATE/bug_report.md`：

```markdown
---
name: Bug 报告
about: 报告一个 Bug
title: '[Bug] '
labels: bug
assignees: ''
---

## Bug 描述
清晰简洁地描述这个 Bug。

## 复现步骤
1. 打开 '...'
2. 点击 '...'
3. 滚动到 '...'
4. 看到错误

## 期望行为
描述你期望发生什么。

## 实际行为
描述实际发生了什么。

## 截图
如果适用，添加截图帮助解释。

## 环境信息
- OS: [e.g. Windows, macOS]
- 浏览器: [e.g. Chrome, Firefox]
- 版本: [e.g. 1.0.0]

## 其他信息
添加其他相关信息。
```

### 步骤 8：创建 PR 模板

创建 `.github/PULL_REQUEST_TEMPLATE.md`：

```markdown
## 变更描述
简述这个 PR 做了什么。

## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 相关 Issue
Closes #

## 测试情况
描述如何测试这些变更。

## 检查清单
- [ ] 代码已自测
- [ ] 已添加/更新测试
- [ ] 已更新文档
- [ ] CI 检查通过

## 截图（如适用）
```

---

## 十、如何确认自己做对了

- 仓库首页显示 README.md 内容。
- 创建 Issue 时能看到模板选项。
- 创建 PR 时能看到模板内容。
- LICENSE 在仓库侧边栏显示。
- 提交代码后能自动分配 Reviewer。

---

## 十一、练习题

### 练习 1：完善项目文档

1. 为你的练习仓库创建完整的 README.md（包含徽章、安装、使用说明）。
2. 创建 CONTRIBUTING.md。
3. 添加 MIT LICENSE。

### 练习 2：创建 Issue 和 PR 模板

1. 创建 `.github/ISSUE_TEMPLATE/` 目录。
2. 添加 Bug 报告模板和功能请求模板。
3. 创建 PR 模板。
4. 测试模板是否生效。

### 练习 3：配置 CODEOWNERS

1. 创建 CODEOWNERS 文件。
2. 配置不同目录的所有者。
3. 创建 PR 验证自动分配。

---

## 十二、延伸阅读

- [GitHub Docs - Community Profile](https://docs.github.com/en/communities)
- [Choose a License](https://choosealicense.com/)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
