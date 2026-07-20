# 关卡 29：Sparse Checkout 与部分克隆

**所属阶段**：进阶实用 / 大仓库  
**难度**：🟡 进阶  
**预估时间**：35 分钟  
**本关命令关键词**：`git sparse-checkout`、`git clone --filter`、cone mode

---

> 💡 **学习提示**： monorepo 或文档站仓库往往很大，但你可能只需要 `docs/` 或 `site/`。Sparse checkout 让你工作区只检出需要的目录。

---

## 一、本关目标

- [ ] 理解 sparse checkout cone mode 与「只检出部分路径」
- [ ] 能在现有 clone 上启用 `git sparse-checkout set`
- [ ] 了解 partial clone（`--filter=blob:none`）减少下载体积
- [ ] 能在本 Lab 仓库或 `playground-hello` 上完成一次 sparse 练习

**前置知识：** 大仓库 clone 慢、`git status` 卡时，sparse + partial clone 是常用组合（关卡 16 延伸）。

---

## 二、前置条件

- [ ] 已完成关卡 16（大仓库）或关卡 01（clone）
- [ ] 本地实验环境已启动：`docker compose up -d`
- [ ] 磁盘上有足够空间做第二次 clone

---

## 三、边看边做：具体步骤

### 步骤 1：对比完整 clone 与 sparse 目标

本教学仓库结构含 `docs/`、`site/`、`_site/` 等。练习只检出 `docs/`：

```bash
cd ~
rm -rf git-workflow-lab-sparse
git clone http://localhost:3000/playground/playground-hello.git git-workflow-lab-sparse
cd git-workflow-lab-sparse
ls
```

若 `playground-hello` 较小，可改用本 Lab 的 GitHub 镜像或本地 `/workspace` 的 remote（在实验容器内）：

```bash
cd ~
rm -rf lab-sparse-demo
git clone --no-checkout http://localhost:3000/playground/playground-hello.git lab-sparse-demo
cd lab-sparse-demo
```

---

### 步骤 2：启用 cone mode sparse checkout

Git 2.25+ 推荐 cone 模式：

```bash
cd ~/lab-sparse-demo
git sparse-checkout init --cone
git sparse-checkout set README.md docs 2>/dev/null || git sparse-checkout set README.md
git checkout main
ls
```

**说明：** 若仓库无 `docs/` 目录，改为只 sparse `README.md` 或你仓库中存在的路径：

```bash
git sparse-checkout set README.md
git checkout main
ls
```

**预期：** 工作区 primarily 可见 `README.md`（及 sparse 列表中的目录），其他路径不在工作树中。

查看 sparse 配置：

```bash
cat .git/info/sparse-checkout
git sparse-checkout list
```

---

### 步骤 3：添加路径并拉取

```bash
git sparse-checkout add LICENSE 2>/dev/null || true
git sparse-checkout list
ls
```

从远程拉更新时，sparse 配置保留：

```bash
git pull origin main
```

---

### 步骤 4：Partial clone（按需下载 blob）

新目录练习 partial clone：

```bash
cd ~
rm -rf lab-partial-demo
git clone --filter=blob:none --no-checkout \
  http://localhost:3000/playground/playground-hello.git lab-partial-demo
cd lab-partial-demo
git sparse-checkout init --cone
git sparse-checkout set README.md
git checkout main
du -sh .git
```

**解读：** `--filter=blob:none` 延迟下载文件内容，直到 checkout 该路径时才拉 blob，适合超大仓库。

---

### 步骤 5：关闭 sparse 恢复完整工作区

```bash
git sparse-checkout disable
git checkout .
ls
```

**预期：** 所有 tracked 文件回到工作区。

---

### 步骤 6：在本 Lab 仓库练习（容器内可选）

若 `/workspace` 可 clone：

```bash
cd /tmp
rm -rf gwl-sparse
git clone --no-checkout file:///workspace gwl-sparse 2>/dev/null || \
  git clone --depth 1 --no-checkout https://github.com/AlexanderJ-Carter/Git-Workflow-Lab.git gwl-sparse
cd gwl-sparse
git sparse-checkout init --cone
git sparse-checkout set docs
git checkout main 2>/dev/null || git checkout master 2>/dev/null || git checkout HEAD
ls
find . -maxdepth 2 -type d
```

**预期：**  primarily 看到 `docs/` 与少量根文件。

---

## 四、如何确认自己做对了

```bash
cd ~/lab-sparse-demo
git sparse-checkout list
git status
test -f README.md && echo "README ok"
```

- [ ] ✓ `git sparse-checkout list` 显示你设置的路径
- [ ] ✓ 工作区未包含未 sparse 的大目录（相对完整 clone 更少文件）
- [ ] ✓ `git pull` 后 sparse 规则仍生效
- [ ] ✓ `git sparse-checkout disable` 后能恢复完整检出

---

## 五、常见错误与排查

### ❌ 情况 1：`error: sparse-checkout was set but no sparse directories`

**可能原因：** 未 `set` 任何路径就 checkout

**解决方法：**

```bash
git sparse-checkout set README.md
git checkout main
```

---

### ❌ 情况 2：cone mode 下 add 的路径不生效

**可能原因：** cone 模式只允许目录级或根文件规则

**解决方法：** 使用目录如 `docs/` 而非深层单文件规则；非 cone 用 `git sparse-checkout init --no-cone`（高级）。

---

### ❌ 情况 3：partial clone 后某些命令报 missing blob

**可能原因：** 尚未 fetch 该对象

**解决方法：**

```bash
git fetch origin
git checkout <path>
```

---

### ❌ 情况 4：CI 需要全量文件但本地 sparse

**可能原因：** 本地优化与 CI 全量构建策略不同

**解决方法：** CI 机器做 full checkout；本地开发可 sparse。

---

## 六、扩展练习

- [ ] **练习 1：** `git clone --depth 1` 与 `--filter=blob:none` 组合对比 clone 时间
- [ ] **练习 2：** sparse 只检出 `site/`，在 http://localhost:8081 预览是否仍需全 repo
- [ ] **练习 3：** 阅读 `git sparse-checkout reapply` 在 merge 后的用途

---

## 七、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 28：Blame 与历史考古](./lesson-28-blame-and-archaeology.md) | [关卡总览](./lessons-overview.md) |
