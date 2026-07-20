# 关卡 26：Git Submodule 子模块

**所属阶段**：进阶实用  
**难度**：🔴 高级  
**预估时间**：40 分钟  
**本关命令关键词**：`git submodule add`、`git submodule update`、`git status`

---

> 💡 **学习提示**：Submodule 把另一个 Git 仓库固定在某个 commit 上，嵌进主仓库。本关用 `playground-ci` 作为子模块，挂到本地新建的 `playground-meta` 仓库。

---

## 一、本关目标

- [ ] 理解 submodule：主仓库只记录「子仓库路径 + commit SHA」
- [ ] 能用 `git submodule add` 添加 `playground-ci`
- [ ] 会 `git submodule update --init --recursive` 克隆后初始化
- [ ] 知道常见坑：detached HEAD、忘记推送子模块、CI 未递归 clone

**前置知识：** 微服务、文档站引用另一 repo、vendor 第三方库时可能遇到 submodule。

---

## 二、前置条件

- [ ] 已完成关卡 01–03（clone、remote、push）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] Gitea 上已有 `playground-ci` 仓库
- [ ] 在 Gitea 创建空仓库 `playground-meta`（或用本地 bare 仓库练习）

---

## 三、边看边做：具体步骤

### 步骤 1：创建主仓库并 clone

在 Gitea（http://localhost:3000）创建仓库 `playground/playground-meta`，然后：

```bash
cd ~
git clone http://localhost:3000/playground/playground-meta.git
cd playground-meta
echo "# Meta project with CI submodule" > README.md
git add README.md
git commit -m "docs: init meta repository"
git push origin main
```

---

### 步骤 2：添加 submodule

```bash
cd ~/playground-meta
git submodule add http://localhost:3000/playground/playground-ci.git ci
git status
```

**预期输出要点：**

```text
new file:   .gitmodules
new file:   ci
```

查看 `.gitmodules`：

```bash
cat .gitmodules
```

**预期：**

```ini
[submodule "ci"]
	path = ci
	url = http://localhost:3000/playground/playground-ci.git
```

提交 submodule 引用：

```bash
git add .gitmodules ci
git commit -m "chore: add playground-ci as submodule at ci/"
git push origin main
```

---

### 步骤 3：克隆含 submodule 的仓库（模拟新同事）

```bash
cd ~
rm -rf playground-meta-clone
git clone http://localhost:3000/playground/playground-meta.git playground-meta-clone
ls playground-meta-clone/ci
```

**预期：** `ci` 目录可能是空的——子模块未初始化。

初始化并拉取：

```bash
cd ~/playground-meta-clone
git submodule update --init --recursive
ls ci/
```

或一步克隆：

```bash
cd ~
rm -rf playground-meta-clone2
git clone --recurse-submodules http://localhost:3000/playground/playground-meta.git playground-meta-clone2
```

---

### 步骤 4：在子模块内修改并更新主仓库指针

```bash
cd ~/playground-meta/ci
git switch main 2>/dev/null || true
echo "# submodule bump" >> SUBMODULE.md
git add SUBMODULE.md
git commit -m "docs: submodule test change"
git push origin main

cd ~/playground-meta
git status
```

**预期：** `git status` 显示 `ci (new commits)`——主仓库检测到子模块 SHA 变了。

更新主仓库记录的 commit：

```bash
git add ci
git commit -m "chore: bump ci submodule pointer"
git push origin main
```

---

### 步骤 5：查看 submodule 状态

```bash
git submodule status
git diff --submodule
```

---

## 四、如何确认自己做对了

```bash
cd ~/playground-meta
test -f .gitmodules && cat .gitmodules
git submodule status
cd ~/playground-meta-clone2/ci && git log --oneline -1
```

- [ ] ✓ 存在 `.gitmodules` 且 `path = ci`
- [ ] ✓ 新 clone 用 `--recurse-submodules` 后 `ci/` 有完整内容
- [ ] ✓ 子模块内 push 后，主仓库有「bump pointer」提交
- [ ] ✓ `git submodule status` 无前导 `-`（未初始化）或 `+`（不同步）异常

---

## 五、常见错误与排查

### ❌ 情况 1：clone 后 ci 目录为空

**可能原因：** 未 `--recurse-submodules` 或未 `submodule update --init`

**解决方法：**

```bash
git submodule update --init --recursive
```

---

### ❌ 情况 2：在子模块里 commit 了，主仓库没 bump，同事仍看到旧版

**可能原因：** 只 push 了子模块 remote，没在主仓库提交新 SHA

**解决方法：** 在主仓库 `git add ci && git commit && git push`。

---

### ❌ 情况 3：子模块处于 detached HEAD

**可能原因：** submodule 默认 checkout 到主仓库记录的精确 commit

**解决方法：** 进子模块后 `git switch main` 开发，完成后回主仓库 bump；或接受 detached 仅做只读引用。

---

### ❌ 情况 4：CI 克隆失败

**可能原因：** CI 未递归 clone

**解决方法：** workflow 里加 `submodules: recursive` 或 `git submodule update --init`。

---

## 六、扩展练习

- [ ] **练习 1：** `git submodule deinit -f ci` 再重新 init
- [ ] **练习 2：** 对比 subtree（`git subtree add`）与 submodule 的优劣
- [ ] **练习 3：** 在 `playground-ci` 的 workflow 里检测 submodule 克隆（若已有 Actions）

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 25：Hotfix 工作流](./lesson-25-hotfix-workflow.md) | [关卡 27：交互式 rebase 进阶](./lesson-27-interactive-rebase-fixup.md) |
