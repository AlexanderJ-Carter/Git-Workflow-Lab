#!/usr/bin/env python3
"""为关键静态页补齐 description / theme-color，并规范化首页 lab-meta。"""

from __future__ import annotations

import re
from pathlib import Path

SITE = Path("site")
THEME = '<meta name="theme-color" content="#6366f1">'

DESCRIPTIONS = {
    "playground.html": "在浏览器中练习 Git 命令，可视化工作区、暂存区与提交历史。",
    "quiz.html": "按课程检验 Git 与 CI/CD 知识，巩固学习成果。",
    "flashcards.html": "用间隔重复记忆 Git 命令与核心概念。",
    "challenges.html": "在真实协作场景中练习冲突解决、恢复与协作流程。",
    "learning-path.html": "可视化 Git 学习路线，按阶段跟踪进度。",
    "ai-assistant.html": "基于课程上下文的 AI 问答助手（需自备 API Key）。",
    "interview.html": "Git 与 CI/CD 高频面试题，含解析与练习。",
    "projects.html": "通过完整项目实践掌握 Git 协作与发布流程。",
    "workspace.html": "本地 Docker 学习工作台：左侧课程，右侧终端。",
    "quick-start.html": "五分钟上手 Git Workflow Lab 本地实验环境。",
    "lessons/index.html": "系统化 Git 与 CI/CD 课程目录，含进度追踪。",
    "gamification.html": "积分、等级与每日任务，让 Git 学习更有动力。",
    "achievements.html": "完成课程与测验解锁成就徽章。",
    "skill-tree.html": "以技能树展示 Git 能力成长路径。",
    "best-practices.html": "Git 分支策略、提交规范与安全实践指南。",
    "search.html": "搜索课程、命令与概念，一键直达目标内容。",
}


def ensure_meta(html: str, description: str | None) -> str:
    if 'name="theme-color"' not in html:
        html = html.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    ' + THEME,
            1,
        )
    if description and 'name="description"' not in html:
        html = html.replace(
            THEME if THEME in html else '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            (THEME if THEME in html else '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
            + f'\n    <meta name="description" content="{description}">',
            1,
        )
    return html


def polish_index_lab_meta(html: str) -> str:
    replacements = [
        (r'class="lab-meta" style="background: #dbeafe; color: #1d4ed8;"', 'class="lab-meta lab-meta--learn"'),
        (r'class="lab-meta" style="background: #ede9fe; color: #6d28d9;"', 'class="lab-meta lab-meta--new"'),
        (r'class="lab-meta" style="background: #dcfce7; color: #166534;"', 'class="lab-meta lab-meta--practice"'),
        (r'class="lab-meta" style="background: #e0e7ff; color: #4338ca;"', 'class="lab-meta lab-meta--new"'),
        (r'class="lab-meta" style="background: #fef3c7; color: #92400e;"', 'class="lab-meta lab-meta--local"'),
        (r'class="lab-meta" style="background: #fef08a; color: #a16207;"', 'class="lab-meta lab-meta--quiz"'),
        (r'class="lab-meta" style="background: #d1fae5; color: #065f46;"', 'class="lab-meta lab-meta--practice"'),
        (r'class="lab-meta" style="background: #e0f2fe; color: #0369a1;"', 'class="lab-meta lab-meta--tool"'),
        (r'class="lab-meta" style="background: #fce7f3; color: #9d174d;"', 'class="lab-meta lab-meta--challenge"'),
        (r'class="lab-meta" style="background: #fee2e2; color: #dc2626;"', 'class="lab-meta lab-meta--challenge"'),
        (r'class="lab-meta">本地入口</span>', 'class="lab-meta lab-meta--local">本地入口</span>'),
    ]
    for old, new in replacements:
        html = re.sub(old, new, html)
    # 去掉过时的 NEW 标签文案，改为语义标签（保留 class）
    html = html.replace(">NEW</span>", ">精选</span>")
    return html


def main() -> None:
    for rel, desc in DESCRIPTIONS.items():
        path = SITE / rel
        if not path.exists():
            print("skip missing", rel)
            continue
        text = path.read_text(encoding="utf-8")
        updated = ensure_meta(text, desc)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print("meta:", rel)

    index = SITE / "index.html"
    text = index.read_text(encoding="utf-8")
    updated = ensure_meta(text, None)
    updated = polish_index_lab_meta(updated)
    if 'name="theme-color"' not in text:
        print("meta: index.html")
    index.write_text(updated, encoding="utf-8")
    print("polished index lab-meta")


if __name__ == "__main__":
    main()
