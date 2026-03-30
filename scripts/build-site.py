#!/usr/bin/env python3
"""Git Workflow Lab - 静态网站构建脚本。"""

import posixpath
import re
import shutil
from pathlib import Path, PurePosixPath
import markdown
from markdown.extensions.toc import TocExtension

PROJECT_NAME = "Git Workflow Lab"
REPO_URL = "https://github.com/AlexanderJ-Carter/Git-Workflow-Lab"
PUBLIC_PAGES = [
    "lessons-overview.md",
    "learning-path.md",
    "faq.md",
]

# 配置
DOCS_DIR = Path("docs")
SITE_DIR = Path("_site")
LESSONS_DIR = SITE_DIR / "lessons"
PAGES_DIR = SITE_DIR / "pages"
ASSETS_DIR = SITE_DIR / "assets"

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Git Workflow Lab</title>
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
                <li><a href="../index.html#highlights">亮点</a></li>
                <li><a href="../lessons/index.html">课程</a></li>
                <li><a href="../pages/learning-path.html">学习路径</a></li>
                <li><a href="{repo_url}" target="_blank" rel="noreferrer">GitHub</a></li>
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
                <li><a href="../index.html#highlights">亮点</a></li>
                <li><a href="index.html">课程</a></li>
                <li><a href="../pages/learning-path.html">学习路径</a></li>
                <li><a href="{repo_url}" target="_blank" rel="noreferrer">GitHub</a></li>
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


def get_output_rel_path(md_path: Path) -> PurePosixPath:
    """根据源 Markdown 路径返回站点中的输出相对路径。"""
    if md_path.name.startswith("lesson-"):
        return PurePosixPath("lessons") / f"{md_path.stem}.html"
    return PurePosixPath("pages") / f"{md_path.stem}.html"


def rewrite_markdown_links(content: str, md_path: Path) -> str:
    """把 docs 中的 .md 链接改写为生成后的 HTML 路径。"""
    current_output = get_output_rel_path(md_path)
    docs_root = DOCS_DIR.resolve()

    def replace_link(match: re.Match) -> str:
        text = match.group("text")
        target = match.group("target").strip()

        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        base_target, anchor = (target.split("#", 1) + [""])[:2]
        if not base_target.endswith(".md"):
            return match.group(0)

        target_path = (md_path.parent / base_target).resolve()
        try:
            target_path.relative_to(docs_root)
        except ValueError:
            return match.group(0)

        target_output = get_output_rel_path(target_path)
        href = posixpath.relpath(
            target_output.as_posix(),
            start=current_output.parent.as_posix(),
        )

        if anchor:
            href = f"{href}#{anchor}"

        return f"[{text}]({href})"

    return re.sub(
        r"(?P<image>!?)\[(?P<text>[^\]]+)\]\((?P<target>[^)]+)\)",
        lambda match: (
            match.group(0) if match.group("image") == "!" else replace_link(match)
        ),
        content,
    )


def process_lesson_file(md_path: Path) -> tuple:
    """处理单个课程文件"""
    content = md_path.read_text(encoding="utf-8")
    title = extract_title(content)
    content = rewrite_markdown_links(content, md_path)
    html_content = convert_markdown_to_html(content)

    # 生成完整 HTML
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        repo_url=REPO_URL,
    )

    return title, full_html


def process_public_page(md_path: Path) -> tuple:
    """处理公开说明页面。"""
    content = md_path.read_text(encoding="utf-8")
    title = extract_title(content)
    content = rewrite_markdown_links(content, md_path)
    html_content = convert_markdown_to_html(content)
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
    PAGES_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "css").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "js").mkdir(parents=True, exist_ok=True)

    # 复制静态资源
    if Path("site/assets/css/style.css").exists():
        shutil.copy("site/assets/css/style.css", ASSETS_DIR / "css" / "style.css")
    if Path("site/assets/js/main.js").exists():
        shutil.copy("site/assets/js/main.js", ASSETS_DIR / "js" / "main.js")

    # 复制所有 site 目录下的 HTML 页面（除了 docs 和 lessons 子目录）
    for html_file in Path("site").glob("*.html"):
        shutil.copy(html_file, SITE_DIR / html_file.name)
        print(f"  Copied {html_file.name}")

    # 复制 site/index.html 作为主页面
    if Path("site/index.html").exists():
        shutil.copy("site/index.html", SITE_DIR / "index.html")

    for page_name in PUBLIC_PAGES:
        page_path = DOCS_DIR / page_name
        if page_path.exists():
            title, html = process_public_page(page_path)
            output_path = PAGES_DIR / f"{page_path.stem}.html"
            output_path.write_text(html, encoding="utf-8")
            print(f"  Built page {title} -> {output_path.name}")

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
