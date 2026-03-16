# 关卡 17：用 Release Please 自动维护版本与 Changelog

**所属阶段**：CI/CD 进阶 / 发布自动化  
**本关命令关键词**：`git commit`、`gh release view`、`release-please`、SemVer、Changelog

---

## 一、本关目标

- 理解为什么要把版本号、Release 和 Changelog 交给自动化处理。
- 学会为 GitHub 仓库接入 Release Please。
- 知道约定式提交如何驱动自动版本号和发布说明。
- 能判断 Release PR、正式 Release 和容器发布三者之间的关系。

学完这一关，你就能把“手工写版本号、手工抄修改日志、手工打标签”的重复劳动交给流水线。

---

## 二、前置条件

- 已完成关卡 10-13，知道 CI Workflow、Release、Tag 和语义化版本号的基本概念。
- 已有一个 GitHub 仓库，并且默认分支为 `main`。
- 仓库中已经配置好基础 GitHub Actions 权限。

---

## 三、边看边做：具体步骤

### 步骤 1：理解自动发布链路

这套链路通常由 4 个动作构成：

1. 开发者按约定式提交推送代码。
2. Release Please 检查提交历史，生成一个 Release PR。
3. 你合并 Release PR 后，GitHub 自动创建 Tag 和 Release。
4. 其他工作流根据正式 Release 去发布镜像、文档或制品。

可以把它理解成：

```text
commit -> release PR -> merge -> tag/release -> deploy/publish
```

### 步骤 2：检查仓库里的自动发布文件

本项目已经内置了 3 个关键文件：

- `release-please-config.json`
- `.release-please-manifest.json`
- `.github/workflows/release-please.yml`

你可以在仓库根目录快速确认：

```bash
ls release-please-config.json .release-please-manifest.json .github/workflows/release-please.yml
```

### 步骤 3：按约定式提交一次真实变更

例如，你新增一个文档说明：

```bash
git add README.md
git commit -m "docs: clarify release automation flow"
git push origin main
```

这里的 `docs:` 很重要，因为 Release Please 会根据提交类型决定 changelog 分类和版本策略。

### 步骤 4：观察 Release Please 工作流

推送后进入 GitHub 仓库的 Actions 页面：

1. 找到 `Release Please` 工作流。
2. 打开最近一次运行记录。
3. 如果仓库里已经累计了足够的变更，通常会生成一个新的 Release PR。

这个 PR 一般会包含：

- 更新后的 `CHANGELOG.md`
- 新版本号
- 自动生成的发布标题

### 步骤 5：合并 Release PR

当 Release PR 看起来没问题时：

1. Review 它生成的版本号是否合理。
2. Review changelog 分类是否符合预期。
3. 合并这个 PR。

合并后，Release Please 会再跑一次，并自动：

- 创建新的 Git tag
- 创建 GitHub Release
- 触发依赖 Release 的其他工作流

### 步骤 6：观察镜像发布链路

本项目的镜像发布工作流监听的是正式 Release 事件，因此当 GitHub Release 被创建后：

1. `.github/workflows/docker.yml` 会开始运行。
2. Gitea 和 terminal 两个镜像会分别构建。
3. 镜像会发布到 GHCR。

你后续就可以在 Packages 或 Release 页确认发布结果。

---

## 四、如何确认自己做对了

- GitHub Actions 中能看到 `Release Please` 工作流正常运行。
- 仓库里出现了 Release PR，而不是你手工去写版本更新提交。
- `CHANGELOG.md` 的新增条目来自自动生成，而不是手工复制粘贴。
- 合并 Release PR 后，仓库里自动出现新 Tag 和 GitHub Release。
- `docker.yml` 在 Release 创建后自动开始构建镜像。

---

## 五、常见错误与排查

### 情况 1：没有生成 Release PR

可能原因：

- 提交信息不符合约定式提交规范。
- `release-please.yml` 没有运行成功。
- 仓库默认分支不是 `main`。

优先检查：

```bash
git log --oneline -5
```

看看最近的提交前缀是不是 `feat:`、`fix:`、`docs:` 这一类。

### 情况 2：版本号不符合预期

常见原因：

- 提交类型和你想表达的变更级别不一致。
- Manifest 里的当前版本基线不对。

记住一个简单规则：

- `fix:` 通常推动 PATCH
- `feat:` 通常推动 MINOR
- 破坏性变更会推动 MAJOR

### 情况 3：Release 创建了，但镜像没发布

优先检查：

- `docker.yml` 是否监听 `release.published`
- GHCR 权限是否开启
- 仓库 Packages 权限是否正常

---

## 六、思考题 / 扩展练习

- 如果一个 PR 同时包含 `feat:` 和 `fix:` 类型的提交，最终版本号应该怎么变化？
- 你是否要把 `docs:` 变更也写入正式 changelog？为什么？
- 如果未来要同时发布站点、镜像和课程包，应该让哪些工作流监听 Release，哪些只监听 push？
