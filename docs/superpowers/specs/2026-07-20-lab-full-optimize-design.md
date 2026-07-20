# Git Workflow Lab 全面优化设计

**日期：** 2026-07-20  
**状态：** 已批准（用户授权全面落地，无需逐步确认）

## 目标

修复运行缺陷、清理仓库结构、打通教学闭环、扩展课程（含 Linux 命令精选）、并提升 UX/微交互；Pages 与 Docker 双轨对等。

## 范围

### A. 基础设施与目录

1. 启用 Gitea SSH：`START_SSH_SERVER=true`，映射 `2222:2222`
2. 统一 Gitea 初始化：仅保留 `docker/gitea/entrypoint.sh` 为运行时真相源；创建 `playground-hello`、`playground-ci`；移除死挂载；对齐 `welcome.sh` / 手动脚本 / 课程文档
3. 修 nginx / terminal healthcheck（`wget`）；`depends_on` 使用 `service_healthy`
4. 终端以非 root 运行 ttyd；`.env` 启动预检；收紧 `.dockerignore`
5. 可选 GHCR 镜像拉取；CI 增加 pytest + compose smoke；修正 check-lessons 编号逻辑
6. 清理：`test-iframe.html`、重复 viewer 策略、双 cspell、过时端口/模板链接、开发残留

### B. 教学闭环

1. 单一课时目录：`site/assets/data/lessons.json`
2. viewer 页脚：完成 → 测验 → 闪卡 → 下一课 / 工作台
3. 修复 quiz 返回链接、learning-path 阶段、search 漏课、`pendingCommand`
4. 首页双轨向导（Pages / Docker）
5. 闪卡按 `lessonId` 过滤 + 轻量 SRS

### C. 内容扩展

1. 强化 `lesson-00-terminal-basics`：精选 Linux 常用命令，外链 `https://linux-command.alexander.xin/`
2. 速查表增加「终端常用」分区
3. 新课：`lesson-20-bisect.md`、`lesson-21-worktree.md`；SSH 指引与 06a 对齐
4. 补齐缺失的「如何确认 / 常见错误」

### D. UX

1. 保留现有视觉语言；克制微交互（淡入、进度过渡、按钮 press、完成确认）
2. workspace：课时选择器、步骤提示条、SSH 连接说明
3. 窄屏工作台上下叠放

## 明确不做

- 不整库搬入 600+ linux-command
- 不做 AI 后端 / ttyd 自动判题
- 不重做品牌或暗黑大改

## 验收

- `docker compose config` 合法；SSH 端口映射存在；demo 仓名与课程一致
- pytest 通过；viewer→quiz 链路可点；无 8082 残留
- 新课与 Linux 精选可在课程中心打开
