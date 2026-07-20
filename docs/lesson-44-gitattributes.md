# 关卡 44：.gitattributes 与合并策略

**所属阶段**：配置与文本处理 / 仓库策略  
**本关关键词**：`.gitattributes`、`text`、`eol`、`binary`、`merge`、`linguist`、`CRLF`

---

## 一、本关目标

- 理解 `.gitattributes` 与 `.gitignore` 的分工：前者控制**已跟踪文件**的 Git 行为，后者决定**是否跟踪**。
- 配置 `text`、`eol`、`binary`，与 [关卡 41](./lesson-41-cli-cross-platform.md) 的 `core.autocrlf` 形成完整行尾策略。
- 为特定文件类型设置合并驱动（如 `merge=union`），减少无意义冲突。
- 了解 `linguist-*` 属性对 GitHub/Gitea 语言统计的影响。

---

## 二、前置条件

**学习模式：**

- 🌐 **在线可学**：阅读属性语法与场景说明。
- 🐳 **建议本地实验**：在 `playground-hello` 或本地测试仓库修改 `.gitattributes`。

**环境要求：**

- [ ] 已完成 [关卡 00](./lesson-00-install-and-config.md) 与 [关卡 41](./lesson-41-cli-cross-platform.md)。
- [ ] 了解 LF 与 CRLF 的区别。

---

## 三、边看边做

### 步骤 1：创建练习仓库

```bash
mkdir -p ~/projects/attrs-demo
cd ~/projects/attrs-demo
git init
echo "# attrs demo" > README.md
git add README.md && git commit -m "chore: init"
```

### 步骤 2：添加基础 `.gitattributes`

创建 `.gitattributes`：

```gitattributes
# 默认：文本文件自动规范化行尾
* text=auto

# 明确 LF 的源码与配置
*.sh text eol=lf
*.py text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.md text eol=lf

# 二进制：不做行尾转换、不尝试合并文本 diff
*.png binary
*.jpg binary
*.ico binary
*.woff binary

# 生成物：合并时保留双方（示例）
CHANGELOG.md merge=union
```

提交：

```bash
git add .gitattributes README.md
git commit -m "chore: add gitattributes"
```

### 步骤 3：验证行尾规范化

```bash
git add --renormalize .
git status
```

`text=auto` 让 Git 根据内容检测文本/二进制；`eol=lf` 强制检出与提交时使用 LF。

查看某文件在索引中的行尾属性：

```bash
git check-attr -a README.md
git check-attr eol -- README.md
```

### 步骤 4：对比 `core.autocrlf`

| 层级 | 作用范围 | 典型用途 |
|------|----------|----------|
| `core.autocrlf` | 本机全局/本地用户偏好 | Windows 开发者个人设置 |
| `.gitattributes` | 仓库内所有协作者 | 团队统一策略（推荐） |

推荐：**团队以 `.gitattributes` 为准**，个人 `core.autocrlf` 设为 `false` 或 `input`，避免双重转换。

```bash
git config --global core.autocrlf false
```

### 步骤 5：`merge=union` 场景

当两个分支都修改了 `CHANGELOG.md` 的不同段落，默认合并可能冲突。`merge=union` 会保留双方内容（顺序不保证，需人工整理）。

实验（可选，需两个分支）：

```bash
git checkout -b feature-a
echo "Feature A entry" >> CHANGELOG.md
git commit -am "docs: changelog a"

git checkout main
git checkout -b feature-b
echo "Feature B entry" >> CHANGELOG.md
git commit -am "docs: changelog b"

git checkout main
git merge feature-a
git merge feature-b
```

观察 `CHANGELOG.md` 合并结果；若无 `merge=union`，可能需手动解冲突。

### 步骤 6：Linguist 与统计

在文档站或大型 monorepo 中，常排除 vendor、生成代码：

```gitattributes
docs/_site/** linguist-generated
package-lock.json linguist-generated
*.min.js linguist-generated
```

Gitea/GitHub 语言栏会据此调整统计，**不影响构建**，仅影响展示。

### 步骤 7：与本仓库对照

查看 Git Workflow Lab 根目录是否已有 `.gitattributes`（若有）：

```bash
curl -s https://raw.githubusercontent.com/AlexanderJ-Carter/Git-Workflow-Lab/main/.gitattributes 2>/dev/null | head -20
```

或克隆后：

```bash
cat .gitattributes 2>/dev/null || echo "本练习仓库可自建"
```

---

## 四、验收清单

- [ ] ✓ 能说明 `.gitattributes` 与 `.gitignore` 的区别
- [ ] ✓ 能编写 `* text=auto` 与 `*.sh text eol=lf`
- [ ] ✓ 能用 `git check-attr` 查看文件属性
- [ ] ✓ 理解 `binary` 与 `merge=union` 的用途
- [ ] ✓ 知道团队行尾策略应优先写入仓库而非仅靠个人配置

---

## 五、常见错误

### ❌ 修改 `.gitattributes` 后行尾仍混乱

**原因：** 已入库文件未重新规范化。

**解决：** `git add --renormalize .` 后提交；协作者拉取后同样执行一次。

### ❌ Shell 脚本报 `bad interpreter`

**原因：** `*.sh` 未设 `eol=lf`，Windows 检出为 CRLF。

**解决：** `.gitattributes` 中 `*.sh text eol=lf`，并 `renormalize`。

### ❌ `merge=union` 产生重复或乱序内容

**原因：** union 合并不保证语义正确，只减少冲突标记。

**解决：** 合并后人工编辑 CHANGELOG；或改用专用工具/分支策略。

---

## 六、练习/思考题

1. 为 `*.bat` 和 `*.ps1` 分别设置合适的 `eol` 策略并说明理由。
2. 对 `vendor/` 目录设置 `linguist-vendored`（若使用 GitHub Linguist）。
3. 在 `attrs-demo` 故意制造 CRLF 的 `.sh` 文件，用 `check-attr` 与 `file` 命令观察差异。
4. **思考题**：为什么 `.gitattributes` 应该提交到仓库，而 `.git/config` 里的 alias 通常不提交？

**延伸阅读：**

- [关卡 41：跨平台命令行对照](./lesson-41-cli-cross-platform.md)
- [关卡 43：Git 别名与配置进阶](./lesson-43-git-config-advanced.md)
- [Git 文档：gitattributes](https://git-scm.com/docs/gitattributes)
