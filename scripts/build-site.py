#!/usr/bin/env python3
"""Git Workflow Lab - 静态网站构建脚本。"""

import os
import re
import shutil
from pathlib import Path
import markdown
from markdown.extensions.toc import TocExtension

PROJECT_NAME = "Git Workflow Lab"
REPO_URL = "https://github.com/AlexanderJ-Carter/Git-Workflow-Lab"

# 配置
DOCS_DIR = Path("docs")
SITE_DIR = Path("_site")
LESSONS_DIR = SITE_DIR / "lessons"
ASSETS_DIR = SITE_DIR / "assets"

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Git Workflow Lab</title>
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="icon" href="../assets/favicon.ico" type="image/x-icon">
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="../index.html" class="logo">
                <span class="logo-icon">📚</span>
                Git Workflow Lab
            </a>
            <ul class="nav-links">
                <li><a href="../index.html#features">特性</a></li>
                <li><a href="index.html">课程</a></li>
                <li><a href="../index.html#setup-note">快速开始</a></li>
            </ul>
            <button class="theme-toggle" id="themeToggle" aria-label="切换主题">🌙</button>
        </nav>
    </header>

    <main class="lesson-layout container">
        <aside class="lesson-sidebar">
            <h4>本页目录</h4>
            <nav class="lesson-nav">
                <ul class="lesson-nav-list" id="toc"></ul>
            </nav>
        </aside>

        <article class="lesson-content">
            {content}
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Git Workflow Lab. MIT License. <a href="{repo_url}" target="_blank" rel="noreferrer">GitHub</a></p>
            </div>
        </div>
    </footer>

    <script src="../assets/js/main.js"></script>
    <script>
        // 生成目录
        document.querySelectorAll('.lesson-content h2').forEach(h2 => {{
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + h2.id;
            a.textContent = h2.textContent;
            li.appendChild(a);
            document.getElementById('toc').appendChild(li);
        }});
    </script>
</body>
</html>
"""

LESSONS_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>课程目录 - Git Workflow Lab</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="../index.html" class="logo">
                <span class="logo-icon">📚</span>
                Git Workflow Lab
            </a>
            <ul class="nav-links">
                <li><a href="../index.html#features">特性</a></li>
                <li><a href="index.html">课程</a></li>
                <li><a href="../index.html#setup-note">快速开始</a></li>
            </ul>
            <button class="theme-toggle" id="themeToggle">🌙</button>
        </nav>
    </header>

    <main class="container" style="padding: 48px 0;">
        <h1>📚 课程目录</h1>
        <p style="color: var(--text-secondary); margin-bottom: 32px;">
            从基础到进阶，循序渐进掌握 Git 和 CI/CD
        </p>

        <div class="lessons-grid">
            {lessons_list}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-bottom">
                <p>&copy; 2026 Git Workflow Lab. MIT License. <a href="{repo_url}" target="_blank" rel="noreferrer">GitHub</a></p>
            </div>
        </div>
    </footer>

    <script src="../assets/js/main.js"></script>
</body>
</html>
"""


def extract_title(content: str) -> str:
    """从 Markdown 内容中提取标题"""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1)
    return PROJECT_NAME


def convert_markdown_to_html(md_content: str) -> str:
    """将 Markdown 转换为 HTML"""
    # 配置 Markdown 扩展
    extensions = [
        "fenced_code",
        "codehilite",
        "tables",
        "toc",
        TocExtension(anchorlink=True),
    ]

    md = markdown.Markdown(extensions=extensions)
    html = md.convert(md_content)

    return html


def process_lesson_file(md_path: Path) -> tuple:
    """处理单个课程文件"""
    content = md_path.read_text(encoding="utf-8")
    title = extract_title(content)
    html_content = convert_markdown_to_html(content)

    # 生成完整 HTML
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        repo_url=REPO_URL,
    )

    return title, full_html


def get_lesson_info(md_path: Path) -> dict:
    """获取课程信息"""
    content = md_path.read_text(encoding="utf-8")
    title = extract_title(content)

    # 提取课程编号
    match = re.search(r"lesson-(\d+)", md_path.name)
    number = match.group(1) if match else "?"

    # 提取描述
    desc_match = re.search(
        r"\*\*所属阶段\*\*[：:].+\n\n(.+?)(?:\n\n|$)", content, re.DOTALL
    )
    description = desc_match.group(1).strip() if desc_match else ""

    return {
        "number": number,
        "title": title,
        "description": (
            description[:100] + "..." if len(description) > 100 else description
        ),
        "filename": md_path.stem,
    }


def build_site():
    """构建静态网站"""
    print(f"🏗️  Building {PROJECT_NAME} website...")

    # 创建目录
    SITE_DIR.mkdir(exist_ok=True)
    LESSONS_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "css").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "js").mkdir(parents=True, exist_ok=True)

    # 复制静态资源
    if Path("site/assets/css/style.css").exists():
        shutil.copy("site/assets/css/style.css", ASSETS_DIR / "css" / "style.css")
    if Path("site/assets/js/main.js").exists():
        shutil.copy("site/assets/js/main.js", ASSETS_DIR / "js" / "main.js")
    if Path("site/index.html").exists():
        shutil.copy("site/index.html", SITE_DIR / "index.html")

    # 处理课程文件
    lessons = []
    for md_file in sorted(DOCS_DIR.glob("lesson-*.md")):
        print(f"  Processing {md_file.name}...")

        title, html = process_lesson_file(md_file)
        output_path = LESSONS_DIR / f"{md_file.stem}.html"
        output_path.write_text(html, encoding="utf-8")

        lessons.append(get_lesson_info(md_file))

    # 创建课程索引页
    lessons_html = ""
    for lesson in sorted(
        lessons, key=lambda x: int(x["number"]) if x["number"].isdigit() else 999
    ):
        lessons_html += f"""
            <a href="{lesson['filename']}.html" class="lesson-card">
                <span class="lesson-number">{lesson['number']}</span>
                <h3>{lesson['title']}</h3>
                <p>{lesson['description']}</p>
            </a>
        """

    index_html = LESSONS_INDEX_TEMPLATE.format(
        lessons_list=lessons_html,
        repo_url=REPO_URL,
    )
    (LESSONS_DIR / "index.html").write_text(index_html, encoding="utf-8")

    print(f"✅ Built {len(lessons)} lesson pages")
    print(f"📁 Output: {SITE_DIR.absolute()}")


if __name__ == "__main__":
    build_site()
