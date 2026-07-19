#!/usr/bin/env python3
"""修复 site/command-builder.html 中的 UTF-8 截断乱码。"""

from pathlib import Path

REPLACEMENTS: list[tuple[str, str]] = [
    ("/* 工具标签\ufffd?*/", "/* 工具标签页 */"),
    ("/* .gitignore 生成\ufffd?*/", "/* .gitignore 生成器 */"),
    ("/* Commit Message 生成\ufffd?*/", "/* Commit Message 生成器 */"),
    ("<!-- 导航\ufffd?-->", "<!-- 导航栏由 main.js 注入 -->"),
    ('<span class="logo-icon">\ufffd?/span>', '<span class="logo-icon">📖</span>'),
    (
        '<li><a href="playground.html">实验\ufffd?/a></li>',
        '<li><a href="playground.html">练习场</a></li>',
    ),
    (
        '<li><a href="command-sheet.html">命令\ufffd?/a></li>',
        '<li><a href="command-sheet.html">命令表</a></li>',
    ),
    ("<h1>Git 命令生成\ufffd?/h1>", "<h1>Git 命令生成器</h1>"),
    (
        "<p>可视化构\ufffd?Git 命令，支持多种操作类型，实时预览，一键复\ufffd?/p>",
        "<p>可视化构建 Git 命令，支持多种操作类型，实时预览，一键复制</p>",
    ),
    ("<!-- git add 配置\ufffd?-->", "<!-- git add 配置区 -->"),
    ("强制添加忽略的文\ufffd?/p>", "强制添加忽略的文件</p>"),
    ("交互式选择每个补丁\ufffd?/p>", "交互式选择每个补丁</p>"),
    ("只添加已跟踪文件的修\ufffd?/p>", "只添加已跟踪文件的修改</p>"),
    ("留空则添加当前目录所有内\ufffd?/p>", "留空则添加当前目录所有内容</p>"),
    ("<!-- git commit 配置\ufffd?-->", "<!-- git commit 配置区 -->"),
    ('placeholder="描述本次提交的更\ufffd?>', 'placeholder="描述本次提交的更改">'),
    ("修改最后一次提\ufffd?/p>", "修改最后一次提交</p>"),
    ("使用上次提交信息（与 --amend 配合\ufffd?/p>", "使用上次提交信息（与 --amend 配合）</p>"),
    ('placeholder="补充说明本次更改的详细内\ufffd?>', 'placeholder="补充说明本次更改的详细内容">'),
    ("<!-- git branch 配置\ufffd?-->", "<!-- git branch 配置区 -->"),
    (
        '<option value="create">创建新分\ufffd?/option>',
        '<option value="create">创建新分支</option>',
    ),
    (
        '<option value="rename">重命名分\ufffd?/option>',
        '<option value="rename">重命名分支</option>',
    ),
    (
        '<option value="checkout">检出分\ufffd?/option>',
        '<option value="checkout">检出分支</option>',
    ),
    (
        '<label class="form-label">目标分支（创\ufffd?重命名时\ufffd?/label>',
        '<label class="form-label">目标分支（创建/重命名时）</label>',
    ),
    ('placeholder="例如: main \ufffd?develop">', 'placeholder="例如: main 或 develop">'),
    ("<span>-m (重命\ufffd?</span>", "<span>-m (重命名)</span>"),
    ("<!-- git merge 配置\ufffd?-->", "<!-- git merge 配置区 -->"),
    (
        '<label class="form-label">源分\ufffd?*</label>',
        '<label class="form-label">源分支 *</label>',
    ),
    ("强制创建合并提交，即使可以快进合\ufffd?/p>", "强制创建合并提交，即使可以快进合并</p>"),
    ("将所有合并的提交压缩为一\ufffd?/p>", "将所有合并的提交压缩为一个</p>"),
    ("中止当前合并（撤销合并\ufffd?/p>", "中止当前合并（撤销合并）</p>"),
    ('placeholder="自定义合并提交信\ufffd?>', 'placeholder="自定义合并提交信息">'),
    ("<!-- git log 配置\ufffd?-->", "<!-- git log 配置区 -->"),
    ("简洁格式，每行显示一个提\ufffd?/p>", "简洁格式，每行显示一个提交</p>"),
    ("显示分支和标签引\ufffd?/p>", "显示分支和标签引用</p>"),
    ("显示完整的补丁内\ufffd?/p>", "显示完整的补丁内容</p>"),
    ('placeholder="作者过\ufffd?>', 'placeholder="作者过滤">'),
    (
        'placeholder="提交信息关键词搜\ufffd? style="margin-top: 10px;">',
        'placeholder="提交信息关键词搜索" style="margin-top: 10px;">',
    ),
    ("<!-- git remote 配置\ufffd?-->", "<!-- git remote 配置区 -->"),
    (
        '<option value="rename">重命名远程仓\ufffd?/option>',
        '<option value="rename">重命名远程仓库</option>',
    ),
    ("获取所有标\ufffd?/p>", "获取所有标签</p>"),
    ("<!-- 工具标签页导\ufffd?-->", "<!-- 工具标签页导航 -->"),
    (
        "将所有修改、新增和删除的文件添加到暂存区。这是使\ufffd?git commit 前的必要步骤\ufffd?                </p>",
        "将所有修改、新增和删除的文件添加到暂存区。这是使用 git commit 前的必要步骤。</p>",
    ),
    (
        '<span class="ignore-category-title">编辑\ufffd?IDE</span>',
        '<span class="ignore-category-title">编辑器 / IDE</span>',
    ),
    (
        '<div class="commit-type-icon">\ufffd?/div>\n                                <div class="commit-type-name">新功\ufffd?/div>',
        '<div class="commit-type-icon">✨</div>\n                                <div class="commit-type-name">新功能</div>',
    ),
    ('<div class="commit-type-icon">\ufffd?/div>', '<div class="commit-type-icon">⚡</div>'),
    (
        '<label class="form-label">简短描\ufffd?*</label>',
        '<label class="form-label">简短描述 *</label>',
    ),
    (
        '<span class="type">feat</span>: 简短描\ufffd?                        </div>',
        '<span class="type">feat</span>: 简短描述</div>',
    ),
    ("<h4>添加\ufffd?SSH Agent</h4>", "<h4>添加到 SSH Agent</h4>"),
    ("<h4>添加公钥\ufffd?Git 服务</h4>", "<h4>添加公钥到 Git 服务</h4>"),
    (
        "Ed25519 算法被推荐使用，\ufffd?RSA 更安全且密钥更短。如果你的系统不支持，可以使\ufffd?rsa 算法\ufffd?code>",
        "Ed25519 算法被推荐使用，比 RSA 更安全且密钥更短。如果你的系统不支持，可以使用 rsa 算法：<code>",
    ),
    (
        "// 命令类型和配置映\ufffd?        const commandConfigs",
        "// 命令类型和配置映射\n        const commandConfigs",
    ),
    (
        "desc: '将所有修改、新增和删除的文件添加到暂存区。这是使\ufffd?git commit 前的必要步骤\ufffd?",
        "desc: '将所有修改、新增和删除的文件添加到暂存区。这是使用 git commit 前的必要步骤。'",
    ),
    (
        "desc: '将暂存区的更改提交到本地仓库。每次提交都会创建一个快照，记录项目的当前状态\ufffd?",
        "desc: '将暂存区的更改提交到本地仓库。每次提交都会创建一个快照，记录项目的当前状态。'",
    ),
    (
        "desc: '用于列出、创建、删除或重命名分支。分支是 Git 最强大的功能之一，让你可以在不影响主线的情况下开发新功能\ufffd?",
        "desc: '用于列出、创建、删除或重命名分支。分支是 Git 最强大的功能之一，让你可以在不影响主线的情况下开发新功能。'",
    ),
    (
        "desc: '将一个分支的更改合并到当前分支。合并可能会产生冲突，需要手动解决\ufffd?",
        "desc: '将一个分支的更改合并到当前分支。合并可能会产生冲突，需要手动解决。'",
    ),
    (
        "desc: '查看项目的提交历史。可以使用各种选项来过滤和格式化输出\ufffd?",
        "desc: '查看项目的提交历史。可以使用各种选项来过滤和格式化输出。'",
    ),
    (
        "desc: '管理远程仓库连接。可以添加、删除或修改远程仓库\ufffd?URL\ufffd?",
        "desc: '管理远程仓库连接。可以添加、删除或修改远程仓库的 URL。'",
    ),
    (
        "// 显示对应的配置面\ufffd?                document.querySelectorAll",
        "// 显示对应的配置面板\n                document.querySelectorAll",
    ),
    ("// 切换\ufffd?Git 命令工具", "// 切换到 Git 命令工具"),
    (
        "// 隐藏 Git 命令配置，显示工具面\ufffd?                    document.querySelector",
        "// 隐藏 Git 命令配置，显示工具面板\n                    document.querySelector",
    ),
    ("btn.textContent = '已复\ufffd?;", "btn.textContent = '已复制';"),
    (
        "preview += `: ${shortDesc || '简短描\ufffd?'}`;",
        "preview += `: ${shortDesc || '简短描述'}`;",
    ),
    (
        "// 监听所有输入变\ufffd?        document.querySelectorAll",
        "// 监听所有输入变化\n        document.querySelectorAll",
    ),
    ("// 初始\ufffd?        generateCommand();", "// 初始化\n        generateCommand();"),
]


def main() -> None:
    path = Path("site/command-builder.html")
    text = path.read_text(encoding="utf-8")
    remaining = text.count("\ufffd")
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # 去掉旧版局部导航，改由全局导航注入
    old_header_start = text.find("<!-- 导航栏由 main.js 注入 -->")
    old_header_end = text.find("<!-- 页面头部 -->")
    if old_header_start != -1 and old_header_end != -1:
        text = (
            text[:old_header_start]
            + "<!-- 导航栏由 main.js 注入 -->\n\n    "
            + text[old_header_end:]
        )
    if "assets/js/main.js" not in text:
        text = text.replace(
            "</body>", '    <script src="assets/js/main.js" defer></script>\n</body>'
        )
    path.write_text(text, encoding="utf-8")
    left = text.count("\ufffd")
    print(f"fixed {path}: fffd {remaining} -> {left}")


if __name__ == "__main__":
    main()
