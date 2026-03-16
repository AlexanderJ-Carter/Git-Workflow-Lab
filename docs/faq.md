# 常见问题解答（FAQ）

本文档收集了 Git Workflow Lab 学习过程中的常见问题和解决方案。

---

## 🐳 环境搭建问题

### Q: Docker 启动失败怎么办？

**A:** 常见原因和解决方案：

1. **端口被占用**
   ```bash
   # 检查端口占用
   # Windows
   netstat -ano | findstr :3000

   # macOS/Linux
   lsof -i :3000

   # 解决：修改 docker-compose.yml 中的端口映射
   ports:
     - "3001:3000"  # 改用 3001 端口
   ```

2. **Docker 未启动**
   - 确保 Docker Desktop 正在运行
   - 检查 Docker 图标是否显示在系统托盘

3. **权限问题（Linux）**
   ```bash
   sudo usermod -aG docker $USER
   # 重新登录后生效
   ```

### Q: Gitea 初始化向导怎么填？

**A:** 当前项目默认已经跳过安装向导并完成初始化，不需要你手工填写数据库连接信息。

首次访问 `http://localhost:3000` 时，直接登录或注册即可：

- 默认管理员账号来自 `.env` 中的 `GITEA_ADMIN_USER`
- 默认管理员密码来自 `.env` 中的 `GITEA_ADMIN_PASSWORD`
- 如果你只是学习，可以直接注册一个普通账号，再按课程练习

### Q: 如何重置整个环境？

**A:** 完全清理并重新开始：

```bash
# 停止并删除容器和卷
docker compose down -v

# 重新启动
docker compose up -d --build
```

---

## 🔧 Git 操作问题

### Q: git push 报错 "rejected"？

**A:** 这通常是因为远程有新的提交，需要先拉取：

```bash
# 先拉取远程更新
git pull origin main --rebase

# 再推送
git push origin main
```

### Q: 合并冲突怎么解决？

**A:** 冲突解决步骤：

1. 查看 `git status` 找到冲突文件
2. 打开冲突文件，找到 `<<<<<<<` 和 `>>>>>>>` 标记
3. 编辑文件，保留正确的内容
4. 删除冲突标记
5. `git add <文件>`
6. `git commit`

详细教程请看 [关卡 05：解决合并冲突](lesson-05-merge-conflict.md)

### Q: 如何撤销最近的提交？

**A:** 分情况处理：

```bash
# 情况1：还没 push，想保留修改
git reset --soft HEAD~1

# 情况2：还没 push，想丢弃修改（危险！）
git reset --hard HEAD~1

# 情况3：已经 push 了，需要用 revert
git revert HEAD
```

### Q: 误删分支怎么恢复？

**A:** 使用 reflog 恢复：

```bash
# 查看 reflog
git reflog

# 找到删除前的提交，重建分支
git branch branch-name <commit-hash>
```

详细教程请看 [关卡 08：reflog 恢复](lesson-08-reflog-and-recovery.md)

### Q: .gitignore 不生效？

**A:** 这是因为文件已经被跟踪了：

```bash
# 清除缓存
git rm -r --cached .
git add .
git commit -m "chore: update .gitignore"
```

---

## 🌐 Gitea 使用问题

### Q: 如何创建 Pull Request？

**A:** 步骤：

1. 在 Web 界面创建分支或推送分支到远程
2. 进入仓库页面，会看到 "Create Pull Request" 提示
3. 点击进入，填写标题和描述
4. 选择目标分支（通常是 main）
5. 点击 "Create Pull Request"

### Q: SSH 连接失败？

**A:** 检查清单：

1. SSH 密钥已生成：`ls ~/.ssh/id_*.pub`
2. 公钥已添加到 Gitea：Settings → SSH Keys
3. 端口正确（默认 2222）：`ssh -p 2222 git@localhost`
4. 测试连接：`ssh -T git@localhost -p 2222`

### Q: CI/CD 不运行？

**A:** 检查：

1. Gitea Actions 是否启用
2. Runner 是否配置并在线
3. 工作流文件路径是否正确（`.gitea/workflows/` 或 `.github/workflows/`）
4. 触发条件是否满足

---

## 📚 课程学习问题

### Q: 课程顺序可以跳过吗？

**A:** 部分可以，但建议：

- **阶段 0-1**：不要跳过，是后续基础
- **阶段 2**：至少完成关卡 04、05，其他可选
- **阶段 3**：可按需学习，遇到问题时再看
- **阶段 4-5**：有 CI 需求再学

详细的学习路径请看 [学习路径指南](learning-path.md)

### Q: 练习题做不出来怎么办？

**A:** 建议：

1. 仔细阅读题目要求
2. 回顾课程中的相关步骤
3. 查看参考答案（但要自己先尝试）
4. 在终端中多尝试不同的命令

### Q: 命令执行结果和课程不一样？

**A:** 可能原因：

1. Git 版本不同：`git --version` 检查
2. 当前分支不同：`git branch` 检查
3. 工作区状态不同：`git status` 检查

解决方案：按照课程的"前置条件"确保环境一致。

---

## 🐛 报错排查

### `fatal: not a git repository`

**原因**：当前目录不是 Git 仓库

**解决**：
```bash
git init  # 初始化仓库
# 或
cd your-repo  # 进入已有仓库目录
```

### `error: Your local changes would be overwritten`

**原因**：有未提交的修改会丢失

**解决**：
```bash
# 方案1：提交修改
git add . && git commit -m "save changes"

# 方案2：暂存修改
git stash

# 方案3：强制覆盖（危险）
git checkout -- .
```

### `Permission denied (publickey)`

**原因**：SSH 密钥未配置或无效

**解决**：
```bash
# 生成密钥
ssh-keygen -t ed25519 -C "your@email.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 Gitea/GitHub
```

### `LF will be replaced by CRLF`

**原因**：Windows 和 Unix 换行符不同

**解决**：这只是警告，不影响使用。如果想关闭：
```bash
git config --global core.autocrlf false
```

---

## 💡 其他问题

### Q: 如何在实际项目中应用所学？

**A:** 建议：

1. 从小项目开始练习
2. 养成频繁提交的习惯
3. 使用分支开发新功能
4. 遇到问题回顾课程内容
5. 在团队中分享 Git 技巧

### Q: 推荐的 Git 工作流？

**A:** 对于大多数项目，推荐 GitHub Flow：

1. main 分支永远可部署
2. 从 main 创建功能分支
3. 开发完成后创建 PR
4. Review 通过后合并
5. 删除功能分支

### Q: 还想学习更多？

**A:** 推荐资源：

- [Pro Git 中文版](https://git-scm.com/book/zh/v2)
- [GitHub 技能学习](https://skills.github.com/)
- [Learn Git Branching](https://learngitbranching.js.org/)（可视化学习）

---

## 🙋 没找到答案？

- 在 [Discussions](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/discussions) 中提问
- 提交 [Issue](https://github.com/AlexanderJ-Carter/Git-Workflow-Lab/issues) 反馈
