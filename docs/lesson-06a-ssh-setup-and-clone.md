# 关卡 06a：配置 SSH 密钥并通过 SSH 访问仓库

**所属阶段**：分支与协作扩展（SSH 与安全访问）  
**本关命令关键词**：`ssh-keygen`、`ssh -T`、`git clone git@...`、`git remote set-url`

---

## 一、本关目标

- 在本机生成一对 SSH 密钥（公钥 / 私钥）。
- 将公钥添加到 Gitea 账户中，用于身份认证。
- 使用 SSH 地址 `git@...` 的方式 clone / push 仓库，而不是每次输入用户名密码。

学完这一关，你在 GitHub / GitLab / Gitea 等平台上都可以举一反三，用 SSH 方式安全、便捷地访问仓库。

---

## 二、前置条件

- 已经可以通过 HTTP 方式正常访问 Gitea，并完成前面几关的练习。
- 确认你的系统上已安装 OpenSSH（Windows 10+ / 11 通常自带，Linux / macOS 默认自带）。

> 本关以「在本机上用一个 Gitea 账户」为例，无需额外服务器。

---

## 三、边看边做：具体步骤

### 步骤 1：检查现有 SSH 密钥（可选）

在本机终端执行：

```bash
ls ~/.ssh
```

如果你看到类似 `id_rsa` / `id_rsa.pub` 或 `id_ed25519` / `id_ed25519.pub`，说明你可能已经有现成的 SSH 密钥，可以复用。

> 注意：不要随意覆盖已有密钥，如果你不确定用途，可以新建一对不同文件名的密钥。

### 步骤 2：生成新的 SSH 密钥对

以 Ed25519 算法为例（推荐）：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

命令解释：

- `-t ed25519`：使用 Ed25519 算法。
- `-C`：注释，一般用邮箱或说明，方便辨认。

执行过程中会有几个提示：

1. **保存路径**（默认 `~/.ssh/id_ed25519`）  
   - 直接回车使用默认即可，除非你有特殊需求。
2. **输入密码短语（passphrase，可选）**  
   - 建议设置，用来保护私钥，即使私钥文件泄露，也多一层安全保障。

完成后，`~/.ssh` 目录下会出现：

- `id_ed25519`：私钥（务必保密，不要上传 / 发送给任何人）
- `id_ed25519.pub`：公钥（可以放心地复制粘贴给 Git 平台）

### 步骤 3：把公钥添加到 Gitea 账户

1. 在终端查看公钥内容：

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 复制整行输出（从 `ssh-ed25519` 开头，到最后的注释结尾）。

3. 打开浏览器登录 Gitea：
   - 右上角头像 → `Settings`（或类似）→ `SSH Keys`。
   - 点击「Add Key」。
   - Title：随便起个名字，例如 `local-dev-ed25519`。
   - Key：粘贴刚才复制的公钥内容。
   - 保存。

保存成功后，Gitea 就可以用你的 SSH 密钥来识别你。

### 步骤 4：测试 SSH 连接（可选但推荐）

在终端执行（本项目默认把 Gitea SSH 暴露在宿主机的 `2222` 端口）：

```bash
ssh -T git@localhost -p 2222
```

首次连接时，可能会提示：

```text
The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

输入 `yes` 回车。

如果一切正常，你会看到类似：

```text
Hi <your-username>! You've successfully authenticated, but Gitea does not provide shell access.
```

说明 SSH 认证已经打通。

### 步骤 5：使用 SSH 地址 clone 仓库

在 Gitea 的仓库页面（例如 `playground-hello`），找到 Clone 按钮，切换到 SSH 模式，复制类似这样的地址：

```text
ssh://git@localhost:2222/<your-username>/playground-hello.git
```

现在在一个新的目录中使用 SSH 方式 clone：

```bash
git clone ssh://git@localhost:2222/<your-username>/playground-hello.git playground-hello-ssh
cd playground-hello-ssh
git remote -v
```

确认 `origin` 的地址是 `git@...` 开头。

随便改动一个文件并推送，观察是否需要再输入用户名密码：

```bash
echo "ssh clone test" >> ssh-test.txt
git add ssh-test.txt
git commit -m "chore: test ssh clone and push"
git push origin main
```

如果推送成功且没有再要求输入 HTTP 账号密码，说明 SSH 配置已经生效。

### 步骤 6：把已有的 HTTP 远程改为 SSH（可选）

如果你之前已经有一个通过 HTTP `clone` 下来的仓库，也可以直接改成 SSH 地址，而不用重新 clone：

```bash
git remote -v

git remote set-url origin ssh://git@localhost:2222/<your-username>/playground-hello.git

git remote -v
```

再次 `git push`，确认使用 SSH 正常。

---

## 四、如何确认自己做对了

- `~/.ssh` 目录下有一对新的密钥文件（如 `id_ed25519` / `id_ed25519.pub`）。
- 在 Gitea 的 `SSH Keys` 页面能看到你添加的公钥记录。
- `ssh -T git@localhost -p 2222` 可以正常返回一条欢迎信息（或类似提示），说明认证成功。
- 使用 `git@...` 开头的地址 clone / push 仓库时，不再要求输入 HTTP 用户名密码。

---

## 五、练习题

### 练习 1：为不同平台准备不同注释的公钥

1. 再用 `ssh-keygen` 生成一对新的密钥，但注释改成例如 `gitea-only`。
2. 把这对密钥只添加到 Gitea 账户，用于本地练习平台。
3. 思考：在真实工作中，你会如何为「公司 GitLab」「个人 GitHub」「自建 Gitea」分别管理密钥？

### 练习 2：为已有多个仓库批量切换到 SSH

1. 在本地列出你目前的几个 HTTP 仓库。
2. 对每个仓库执行：

   ```bash
   git remote -v
   git remote set-url origin ssh://git@localhost:2222/<your-username>/<repo-name>.git
   git remote -v
   ```

3. 尝试分别在这些仓库中 push 一次，确认都通过 SSH 正常工作。

---

## 六、参考答案（仅供对照）

### 练习 1 参考思路

生成新密钥时：

```bash
ssh-keygen -t ed25519 -C "gitea-only"
# 保存为 ~/.ssh/id_ed25519_gitea（例如），不要覆盖默认的 id_ed25519
```

然后在 `~/.ssh/config` 中配置（可选进阶）：

```text
Host gitea-local
    HostName localhost
   Port 2222
    User git
    IdentityFile ~/.ssh/id_ed25519_gitea
```

这样你就可以用：

```bash
ssh -T gitea-local
git clone gitea-local:<your-username>/playground-hello.git
```

这种写法在管理多个平台时会更方便清晰。

> 注意：`~/.ssh/config` 的修改属于稍进阶内容，本关不强制，仅提供思路。

