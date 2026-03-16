# 关卡 01：从 0 开始，新建仓库并 push 代码

**所属阶段**：Git 基础操作  
**本关命令关键词**：`git clone`、`git add`、`git commit`、`git push`

---

## 一、本关目标

- 在 Gitea Web 界面中创建一个新的远程仓库。
- 把远程仓库 clone 到本地练习环境。
- 完成一次最基础的新增文件、提交和 push。

学完这一关，你就会建立起最核心的 Git 闭环：远程建仓库，本地写内容，再把结果推回去。

---

## 二、前置条件

- 已完成关卡 00 或至少知道如何打开 Web 终端。
- 本地实验环境已经启动成功。
- 能访问 `http://localhost:3000` 和 `http://localhost:8080`。

---

## 三、边看边做：具体步骤

### 步骤 1：登录或注册 Gitea 账号

1. 在浏览器打开 `http://localhost:3000`。
2. 你有两种方式进入练习环境：
   - 直接使用 `.env` 中的默认管理员账号登录。
   - 点击右上角 `Register` 注册一个普通学习账号。
3. 后续命令中的 `<你的用户名>` 都替换成你当前登录的用户名。

### 步骤 2：在 Web 上创建第一个仓库

1. 登录后，点击右上角头像旁的 `+` 或 `New Repository`。
2. 填写以下信息：
   - Repository Name：`playground-hello`
   - Visibility：Private 或 Public 都可以
3. 创建完成后，确认仓库首页已经出现 Clone 地址。

### 步骤 3：在终端 clone 仓库

在 Web 终端或你本机终端里执行：

```bash
git clone http://localhost:3000/<你的用户名>/playground-hello.git
cd playground-hello
```

执行后你应该已经进入新仓库目录。

### 步骤 4：添加第一个文件

```bash
echo "# Hello Git Workflow Lab" > README.md
git status
```

此时 `git status` 应该会显示一个未跟踪的新文件 `README.md`。

### 步骤 5：提交并推送

```bash
git add README.md
git commit -m "chore: add README"
git push origin main
```

如果这是你的第一次 push，Git 可能会要求你输入账号密码或令牌；在本地 Gitea 实验环境中，按你当前登录账号填写即可。

---

## 四、如何确认自己做对了

- `git status` 在提交后显示工作区干净。
- `git log --oneline` 至少能看到一条 `chore: add README` 提交。
- 刷新 Gitea 仓库首页后，能看到刚才推送的 `README.md` 文件。

你可以用下面两个命令快速复查：

```bash
git status
git log --oneline -3
```

---

## 五、常见错误与排查

### 情况 1：`fatal: repository not found`

通常说明 clone 地址里的用户名或仓库名写错了。请回到 Gitea 仓库首页，重新复制仓库地址。

### 情况 2：`src refspec main does not match any`

通常说明你还没有真正创建提交。先执行：

```bash
git add README.md
git commit -m "chore: add README"
```

然后再 push。

### 情况 3：push 被拒绝

如果远程仓库已经有更新，而本地分支落后，可以先执行：

```bash
git pull origin main --rebase
git push origin main
```

---

## 六、思考题 / 扩展练习

- 如果你想把这一步改成 SSH clone，后续需要补哪些配置？
- 试着再创建一个分支 `feature/test-branch`，提交一个文件并 push，观察 Gitea 界面的分支变化。
- 把 `README.md` 改成两次提交，再用 `git log --oneline` 观察历史是否更清晰。

