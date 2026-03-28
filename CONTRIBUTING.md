# 贡献指南

感谢你考虑为 Git Workflow Lab 做出贡献！

## 🤔 如何贡献

### 报告问题

如果你发现了 Bug 或有功能建议：

1. 在 [Issues](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues) 中搜索是否已有相同问题
2. 如果没有，创建新 Issue：
   - 使用清晰的标题描述问题
   - 提供复现步骤（如果是 Bug）
   - 说明你的环境（操作系统、Git 版本等）

### 贡献课程内容

我们欢迎新的课程贡献！请遵循以下步骤：

1. **Fork 本仓库**
2. **创建功能分支**
   ```bash
   git checkout -b feature/new-lesson
   ```
3. **创建课程文件**
   - 复制 `docs/_lesson-template.md` 作为模板
   - 命名格式：`docs/lesson-XX-topic-name.md`
   - 确保编号连续，不与现有课程冲突
4. **更新课程总览**
   - 在 `docs/lessons-overview.md` 中添加新课程信息
5. **提交更改**
   ```bash
   git commit -m "docs: add lesson XX about topic"
   ```
6. **推送并创建 Pull Request**

## 📝 课程格式规范

每个课程文件应包含：

```markdown
# 关卡 XX：课程标题

**所属阶段**：阶段名称
**本关命令关键词**：`git command`

---

## 一、本关目标
（列出学习目标）

## 二、前置条件
（需要先完成的课程或技能）

## 三、边看边做：具体步骤
（详细的实践步骤）

## 四、如何确认自己做对了
（验证学习成果）

## 五、练习题
（巩固练习）

## 六、参考答案（仅供对照）
（练习题答案）
```

## 💻 代码风格

### Markdown 规范

- 使用 ATX 风格标题（`#` 而非下划线）
- 代码块指定语言：` ```bash `
- 链接使用引用式：`[文字][ref]`
- 中文与英文之间添加空格

### 提交信息规范

使用 [约定式提交](https://www.conventionalcommits.org/)：

```
<类型>: <简短描述>

[可选的详细描述]
```

常用类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 重构
- `chore`: 杂项

示例：
```
docs: add lesson 13 about git tags
fix: correct typo in lesson 02
feat: add learning path visualization
```

## 🌿 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 新课程 | `lesson/XX-topic` | `lesson/13-tags` |
| 功能 | `feature/name` | `feature/search` |
| 修复 | `fix/issue-N` | `fix/issue-42` |
| 文档 | `docs/topic` | `docs/faq` |

## ✅ Pull Request 检查清单

提交 PR 前，请确认：

- [ ] 代码/文档已通过本地预览
- [ ] 提交信息符合规范
- [ ] 新课程已添加到 `lessons-overview.md`
- [ ] 文件命名符合规范

## 🏗️ 项目结构

```
.
├── docs/                    # 课程文档
│   ├── lessons-overview.md  # 课程总览
│   ├── _lesson-template.md  # 课程模板
│   └── lesson-*.md          # 各课程文件
├── site/                    # 静态网站
├── scripts/                 # 构建脚本
├── .github/                 # GitHub 配置
│   └── workflows/           # Actions 工作流
├── CONTRIBUTING.md          # 本文件
├── README.md                # 项目说明
└── LICENSE                  # 许可证
```

## 🙋 获取帮助

如果你有任何问题：

- 在 [Discussions](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/discussions) 中提问
- 在 Issue 中 @ 维护者
- 查看现有课程作为参考

## 📜 行为准则

请参阅 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

---

再次感谢你的贡献！🎉
