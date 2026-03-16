# 关卡 01：从 0 开始，新建仓库并 push 代码

**目标**

- 在 Web 界面上创建一个新的 Git 仓库
- 在本地 clone 仓库、添加文件、commit 并 push 回去

---

## 步骤 1：登录 / 注册 Gitea

1. 在浏览器打开 `http://localhost:3000`
2. 你有两种方式进入练习环境：
   - 直接使用 `.env` 中的默认管理员账号登录
   - 点击右上角 `Register` 注册一个普通学习账号
3. 下面示例统一用“你的用户名”指代当前登录账号，不再强制要求使用 `playground`

---

## 步骤 2：在 Web 上创建一个仓库

1. 登录后，点击右上角头像 → `New Repository`
2. 填写：
   - Repository Name：`playground-hello`
   - Visibility：Private / Public 均可
3. 创建后，你会看到仓库首页，其中包含：
   - `Clone` 地址（HTTPS / SSH）
   - 空目录提示

---

## 步骤 3：在本地克隆仓库

在你的本地终端执行（以 HTTPS 为例）：

```bash
git clone http://localhost:3000/<你的用户名>/playground-hello.git
cd playground-hello
```

---

## 步骤 4：添加第一个文件并 push

```bash
echo "# Hello Git Workflow Lab" > README.md

git add README.md
git commit -m "chore: add README"
git push origin main
```

回到浏览器刷新仓库首页，你应该能看到刚才提交的 `README.md`。

---

## 思考题

- 如果你在 push 时提示「rejected」或远程存在更新，应该怎么处理？
- 你可以再创建一个新分支 `feature/test-branch`，在其上提交并 push，观察 Web 界面中的分支变化。

