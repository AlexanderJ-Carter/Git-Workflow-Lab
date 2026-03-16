# 关卡 16：Git 性能优化与大仓库处理

**所属阶段**：进阶操作
**本关关键词**：浅克隆、Git LFS、.gitignore 优化、性能调优

---

## 一、本关目标

- 掌握处理大型仓库的技巧。
- 学会使用 Git LFS 管理大文件。
- 优化 .gitignore 配置。
- 了解 Git 性能调优选项。

学完这一关，你就能高效处理大型项目和二进制文件了。

---

## 二、前置条件

- 已完成关卡 01-03（Git 基础操作）。
- 了解 Git 内部原理（可选）。
- 有一个可用的 Git 仓库用于练习。

---

## 三、核心概念

### 大仓库的问题

当仓库变得很大时，会遇到：

- `git clone` 耗时很长
- `git status` 变慢
- `git log` 卡顿
- 磁盘占用过大

### 常见原因

1. **历史提交太多**：多年开发积累
2. **大文件**：图片、视频、二进制文件
3. **频繁变更的大文件**：每次提交都产生新副本
4. **过多的小文件**：数万个文件

### 解决方案概览

| 问题 | 解决方案 |
|------|---------|
| 仓库太大 | 浅克隆、单分支克隆 |
| 大文件 | Git LFS |
| 无用文件 | 优化 .gitignore |
| 性能问题 | Git 配置调优 |

---

## 四、浅克隆与部分克隆

### 步骤 1：浅克隆（Shallow Clone）

只克隆最近的 N 次提交：

```bash
# 只克隆最近 1 次提交
git clone --depth 1 https://github.com/user/large-repo.git

# 克隆最近 10 次提交
git clone --depth 10 https://github.com/user/large-repo.git
```

**优点**：
- 克隆速度快很多
- 占用磁盘空间小

**缺点**：
- 无法查看完整历史
- 某些操作受限

### 步骤 2：单分支克隆

只克隆单个分支：

```bash
# 只克隆 main 分支
git clone --single-branch --branch main https://github.com/user/repo.git
```

### 步骤 3：稀疏检出（Sparse Checkout）

只检出部分目录：

```bash
# 初始化
git clone --filter=blob:none --sparse https://github.com/user/monorepo.git
cd monorepo

# 只检出特定目录
git sparse-checkout set packages/core packages/utils

# 查看当前配置
git sparse-checkout list
```

### 步骤 4：获取更多历史

浅克隆后，如需更多历史：

```bash
# 获取更多历史
git fetch --deepen=10

# 获取完整历史
git fetch --unshallow
```

---

## 五、Git LFS 大文件管理

### 什么是 Git LFS？

Git LFS（Large File Storage）将大文件存储在单独的位置，仓库中只保留指针文件。

```
# 普通方式：大文件直接提交
仓库大小 = 所有历史版本的大文件大小总和

# LFS 方式：只存指针
仓库大小 = 指针文件大小（几字节）
```

### 步骤 5：安装 Git LFS

```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Windows（Git for Windows 自带）
# 或从 https://git-lfs.github.com/ 下载

# 初始化
git lfs install
```

### 步骤 6：配置 LFS 跟踪

```bash
# 跟踪特定类型文件
git lfs track "*.psd"
git lfs track "*.mp4"
git lfs track "*.zip"

# 跟踪特定目录
git lfs track "assets/**"

# 查看跟踪规则
git lfs track

# 规则保存在 .gitattributes
cat .gitattributes
```

### 步骤 7：提交大文件

```bash
# 正常提交即可
git add large-image.psd
git commit -m "feat: add design file"
git push
```

LFS 会自动处理大文件的上传。

### 步骤 8：克隆包含 LFS 的仓库

```bash
# 克隆时会自动下载 LFS 文件
git clone https://github.com/user/repo-with-lfs.git

# 只下载 LFS 指针，不下载实际文件
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/user/repo-with-lfs.git

# 后续需要时再下载
git lfs pull
```

### 步骤 9：迁移已有文件到 LFS

```bash
# 将历史中的大文件迁移到 LFS
git lfs migrate import --include="*.psd" --everything
```

---

## 六、.gitignore 优化

### 步骤 10：检查仓库大小

```bash
# 查看仓库大小
du -sh .git

# 查看哪些文件占用最多空间
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sed -n 's/^blob //p' | \
  sort --numeric-sort --key=2 | \
  tail -20
```

### 步骤 11：完善的 .gitignore 模板

```gitignore
# 操作系统
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# 依赖目录
node_modules/
vendor/
venv/
__pycache__/

# 构建产物
dist/
build/
*.o
*.class
*.exe
*.dll

# 日志和缓存
*.log
*.cache
.cache/

# 环境配置
.env
.env.local
.env.*.local

# 测试覆盖率
coverage/
.coverage

# 大文件（应使用 LFS）
# *.psd
# *.mp4
```

### 步骤 12：使用 gitignore 模板

GitHub 提供了大量模板：https://github.com/github/gitignore

---

## 七、Git 性能调优

### 步骤 13：检查当前配置

```bash
git config --global --list | grep -E 'pack|diff|gc'
```

### 步骤 14：优化配置

```bash
# 提高压缩效率（多核并行）
git config --global pack.threads 4
git config --global pack.windowMemory 256m

# 加速 diff
git config --global diff.algorithm histogram

# 加速 status（文件系统监控）
git config --global core.fsmonitor true
git config --global core.untrackedCache true

# 更激进的 GC
git config --global gc.auto 256
git config --global gc.autoDetach false
```

### 步骤 15：执行垃圾回收

```bash
# 手动执行 GC
git gc

# 更彻底的 GC（耗时更长）
git gc --aggressive

# 清理无法访问的对象
git prune
```

### 步骤 16：清理历史中的大文件

如果大文件已经提交到历史中：

```bash
# 使用 git-filter-repo（推荐）
pip install git-filter-repo
git filter-repo --path large-file.psd --invert-paths

# 或使用 BFG Repo-Cleaner
java -jar bfg.jar --strip-blobs-bigger-than 100M
```

> ⚠️ **警告**：这会改写历史，需要强制推送。

---

## 八、最佳实践总结

### 仓库大小管理

| 阶段 | 建议 |
|------|------|
| 项目初期 | 配置好 .gitignore，使用 LFS |
| 项目中期 | 定期检查仓库大小 |
| 仓库过大 | 考虑浅克隆、历史清理 |

### 协作建议

1. **大文件**：统一使用 LFS
2. **敏感信息**：永远不要提交（使用 .gitignore）
3. **构建产物**：不要提交，在 CI 中生成
4. **依赖**：不要提交（node_modules、venv 等）

---

## 九、如何确认自己做对了

- 浅克隆能显著减少下载时间。
- LFS 正确跟踪大文件，`.gitattributes` 配置正确。
- `.gitignore` 排除了所有不需要跟踪的文件。
- `git gc` 后仓库体积减小。

---

## 十、练习题

### 练习 1：浅克隆对比

1. 找一个大型开源项目。
2. 对比普通克隆和 `--depth 1` 浅克隆的时间和空间差异。
3. 尝试在浅克隆中查看历史，观察结果。

### 练习 2：配置 Git LFS

1. 创建一个新仓库。
2. 配置 LFS 跟踪 `.zip` 文件。
3. 提交一个 zip 文件，观察是否使用 LFS。
4. 检查 `.gitattributes` 内容。

### 练习 3：仓库瘦身

1. 创建一个仓库，提交一些大文件。
2. 使用 `git filter-repo` 或 BFG 清理历史。
3. 对比清理前后的仓库大小。

---

## 十一、参考答案（仅供对照）

### 练习 1 参考命令

```bash
# 普通克隆
time git clone https://github.com/torvalds/linux.git linux-full

# 浅克隆
time git clone --depth 1 https://github.com/torvalds/linux.git linux-shallow

# 对比大小
du -sh linux-full linux-shallow
```

### 练习 2 参考命令

```bash
git init lfs-demo
cd lfs-demo
git lfs install
git lfs track "*.zip"
git add .gitattributes
git commit -m "chore: setup LFS"

# 创建并提交 zip
dd if=/dev/zero of=test.zip bs=1M count=10
git add test.zip
git commit -m "feat: add zip file"

# 验证
git lfs ls-files
```

### 练习 3 参考命令

```bash
# 安装工具
pip install git-filter-repo

# 清理大文件
git filter-repo --path large-file.bin --invert-paths

# 强制 GC
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## 十二、常见问题与排查

### 问题 1：克隆超时

**解决**：
- 使用浅克隆
- 使用单分支克隆
- 使用镜像站点

### 问题 2：LFS 文件下载失败

```bash
# 检查 LFS 配置
git lfs env

# 手动拉取
git lfs fetch --all
git lfs checkout
```

### 问题 3：仓库越来越慢

```bash
# 诊断
git count-objects -vH

# 执行维护
git gc --aggressive
git repack -a -d
```

---

## 十三、延伸阅读

- [Git LFS 官方文档](https://git-lfs.github.com/)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [Git 性能优化](https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery)
