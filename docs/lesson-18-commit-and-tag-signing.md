# 关卡 18：提交签名与标签签名

**所属阶段**：安全与规范
**难度**：🟡 进阶
**预估时间**：30 分钟
**本关命令关键词**：`git commit -S`、`git tag -s`、`git log --show-signature`、`gpg`

---

> 💡 **学习提示**：左边打开本文件，右边同时打开浏览器 + 终端，按照步骤逐条执行。完成每步后记得验证结果。

---

## 一、本关目标

- [ ] **目标 1**：理解为什么需要对提交和标签进行签名
- [ ] **目标 2**：学会生成 GPG 密钥并配置 Git
- [ ] **目标 3**：掌握对提交和标签进行签名的方法
- [ ] **目标 4**：学会验证签名的有效性

**前置知识：** 学完这一关，你将能够在团队协作中使用签名来验证代码来源，防止身份冒充。

---

## 二、前置条件

在开始本关之前，请确保：

- [ ] 已完成关卡 06a（SSH 密钥配置）
- [ ] 本地实验环境已启动（`docker-compose up -d`）
- [ ] 可访问 http://localhost:8080 (终端)

---

## 三、边看边做：具体步骤

### 步骤 1：生成 GPG 密钥

> **为什么要做这个步骤：** GPG 密钥用于对你的提交和标签进行数字签名，证明代码确实是你本人提交的。

```bash
# 生成 GPG 密钥（使用 RSA 4096 位）
gpg --full-generate-key
```

**交互式选择：**
```
请选择密钥类型：1（RSA 和 RSA）
请选择密钥长度：4096
密钥有效期：0（永不过期）
确认创建：y
输入姓名：Your Name
输入邮箱：your@email.com
输入密码：（设置一个密码）
```

**预期输出：**
```
gpg: 密钥 XXXXXXXX 已被标记为最终信任
```

---

### 步骤 2：查看并复制密钥 ID

```bash
# 列出所有密钥
gpg --list-keys --keyid-format=long
```

**输出解读：**
```
pub   rsa4096/XXXXXXXX 2024-01-01 [SC]      # XXXXXXXX 是密钥ID
      A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8
uid                 [ultimate] Your Name <your@email.com>
sub   rsa4096/YYYYYYYY 2024-01-01 [E]
```

---

### 步骤 3：配置 Git 使用 GPG 签名

```bash
# 设置 Git 使用的 GPG 密钥
git config --global user.signingkey XXXXXXXX

# 启用自动签名（可选，按需开启）
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

**验证配置：**
```bash
git config --global user.signingkey
# 输出：XXXXXXXX
```

---

### 步骤 4：创建签名提交

```bash
# 进入测试仓库
cd ~/playground-hello

# 创建一个新文件
echo "Signed commit test" > signed-test.txt
git add signed-test.txt

# 创建签名提交（-S 参数）
git commit -S -m "feat: 添加签名提交测试"
```

**预期输出：**
```
[main XXXXXXX] feat: 提交签名测试测试
 1 file changed, 1 insertion(+)
```

---

### 步骤 5：验证签名

```bash
# 查看提交日志（显示签名状态）
git log --show-signature -1
```

**输出解读：**
```
commit XXXXXXX...
gpg: 签名于 2024-01-01T00:00:00Z
gpg:                使用 RSA 密钥 XXXXXXXXXX
gpg: 好的签名，来自 "Your Name" <your@email.com>
Author: Your Name <your@email.com>
Date:   Mon Jan 1 00:00:00 2024 +0000

    feat: 添加签名提交测试
```

---

### 步骤 6：创建签名标签

```bash
# 先创建一个普通标签
git tag v1.0.0

# 删除普通标签
git tag -d v1.0.0

# 创建签名标签（-s 参数）
git tag -s v1.0.0 -m "Release version 1.0.0"
```

---

### 步骤 7：验证标签签名

```bash
# 查看标签签名
git tag -v v1.0.0
```

**预期输出：**
```
object XXXXXXXXXX
type commit
tag v1.0.0
tagger Your Name <your@email.com> 2024-01-01T00:00:00+0000

Release version 1.0.0
gpg: 签名于 2024-01-01T00:00:00Z
gpg:                使用 RSA 密钥 XXXXXXXXXX
gpg: 好的签名，来自 "Your Name" <your@email.com>
```

---

## 四、如何确认自己做对了

运行以下命令验证：

```bash
# 检查提交签名
git log --show-signature -1

# 检查标签签名
git tag -v v1.0.0

# 检查 GPG 配置
git config --global user.signingkey
git config --global commit.gpgsign
```

- [ ] ✓ `git log --show-signature` 显示 "good signature"
- [ ] ✓ `git tag -v` 验证签名有效
- [ ] ✓ 在 Gitea Web 界面能看到签名标记

---

## 五、常见错误与排查

### ❌ 情况 1：gpg: signing failed: secret key not available

**可能原因：**
- 密钥 ID 配置错误
- GPG 密钥未正确生成

**解决方法：**
```bash
# 检查密钥列表
gpg --list-keys --keyid-format=long

# 重新配置正确的密钥 ID
git config --global user.signingkey <正确的密钥ID>
```

---

### ❌ 情况 2：gpg: no default secret key: Inappropriate ioctl for device

**可能原因：**
- 需要输入密码但终端无法交互

**解决方法：**
```bash
# 使用 pinentry-curses 或配置 gpg-agent
export GPG_TTY=$(tty)
gpg-connect-agent reloadagent /bye
gpg-agent --daemon
```

---

## 六、知识扩展（可选）

### 为什么需要签名？

1. **身份验证**：证明代码确实是你本人提交的
2. **完整性保护**：确保提交内容未被篡改
3. **不可否认性**：你无法否认自己签署过的提交
4. **团队信任**：在开源项目中建立信任链

### 签名与 SSH 密钥的区别

| 特性 | GPG 签名 | SSH 密钥 |
|------|----------|----------|
| 用途 | 提交/标签签名 | 身份认证 |
| 生成方式 | gpg --full-generate-key | ssh-keygen |
| 配置位置 | user.signingkey | SSH 配置文件 |
| 验证方式 | gpg --verify | ssh -T |

---

## 七、思考题

1. **问题 1：** 如果团队中有人忘记配置 GPG 签名，他们的提交会怎样？
2. **问题 2：** 在开源项目中，签名的重要性体现在哪里？

---

## 八、扩展练习

- [ ] **练习 1：** 尝试创建多个签名标签并验证
- [ ] **练习 2：** 在 GitHub/Gitea 上配置签名显示
- [ ] **练习 3：** 研究如何使用硬件安全模块（HSM）存储密钥

---

## 九、下一步

| 上一关 | 下一关 |
|--------|--------|
| [关卡 17：自动维护版本与 Changelog](./lesson-17-release-automation.md) | [关卡 19：Secrets 与安全实践](./lesson-19-secrets-and-security.md) |
