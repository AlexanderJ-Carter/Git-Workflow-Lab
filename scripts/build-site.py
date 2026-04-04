#!/usr/bin/env python3
"""Git Workflow Lab 静态网站构建脚本.

本模块负责将 Markdown 格式的课程文档转换为静态 HTML 网站。
主要功能包括:

- Markdown 到 HTML 的转换
- 自动生成课程索引页面
- 处理文档间的相对链接
- 复制静态资源文件

使用方法:
    $ python scripts/build-site.py

输出目录:
    _site/ - 构建后的静态网站

Example:
    >>> from scripts.build_site import build_site
    >>> build_site()
    🏗️  Building Git Workflow Lab website...
    ✅ Built 17 lesson pages
"""

import posixpath
import re
import shutil
from pathlib import Path, PurePosixPath
from typing import Dict, List, Tuple

import markdown
from markdown.extensions.toc import TocExtension

# 项目配置
PROJECT_NAME = "Git Workflow Lab"
REPO_URL = "https://github.com/AlexanderJ-Carter/Git-Workflow-Lab"

# 公开页面列表
PUBLIC_PAGES: List[str] = [
    "lessons-overview.md",
    "learning-path.md",
    "faq.md",
]

# 目录配置
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
    """从 Markdown 内容中提取标题.

    Args:
        content: Markdown 格式的文档内容.

    Returns:
        提取到的标题文本，如果未找到则返回项目名称.

    Example:
        >>> extract_title('# Git 基础\\n\\n内容...')
        'Git 基础'
    """
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1) if match else PROJECT_NAME


def convert_markdown_to_html(md_content: str) -> str:
    """将 Markdown 转换为 HTML.

    Args:
        md_content: Markdown 格式的文本内容.

    Returns:
        转换后的 HTML 字符串.

    Note:
        支持以下 Markdown 扩展:
        - fenced_code: 代码块
        - codehilite: 代码高亮
        - tables: 表格
        - toc: 目录生成
    """
    extensions = [
        "fenced_code",
        "codehilite",
        "tables",
        "toc",
        TocExtension(anchorlink=True),
    ]

    md = markdown.Markdown(extensions=extensions)
    return md.convert(md_content)


def get_output_rel_path(md_path: Path) -> PurePosixPath:
    """根据源 Markdown 路径返回站点中的输出相对路径.

    Args:
        md_path: Markdown 源文件的路径.

    Returns:
        输出 HTML 文件的相对路径.

    Example:
        >>> get_output_rel_path(Path('docs/lesson-01.md'))
        PurePosixPath('lessons/lesson-01.html')
    """
    if md_path.name.startswith("lesson-"):
        return PurePosixPath("lessons") / f"{md_path.stem}.html"
    return PurePosixPath("pages") / f"{md_path.stem}.html"


def rewrite_markdown_links(content: str, md_path: Path) -> str:
    """将文档中的 Markdown 链接重写为 HTML 链接.

    Args:
        content: Markdown 文档内容.
        md_path: 当前文档的路径，用于计算相对路径.

    Returns:
        重写链接后的 Markdown 内容.

    Note:
        - 保留外部链接（http://, https://, mailto:）不变
        - 保留锚点链接（#）不变
        - 将 .md 链接转换为对应的 .html 链接
    """
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


def process_lesson_file(md_path: Path) -> Tuple[str, str]:
    """处理单个课程文件.

    Args:
        md_path: 课程 Markdown 文件的路径.

    Returns:
        元组 (标题, 完整HTML内容).

    Example:
        >>> title, html = process_lesson_file(Path('docs/lesson-01.md'))
        >>> print(title)
        'Git 基础'
    """
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


def process_public_page(md_path: Path) -> Tuple[str, str]:
    """处理公开说明页面.

    Args:
        md_path: 页面 Markdown 文件的路径.

    Returns:
        元组 (标题, 完整HTML内容).
    """
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


def get_lesson_info(md_path: Path) -> Dict[str, str]:
    """获取课程元信息.

    Args:
        md_path: 课程 Markdown 文件的路径.

    Returns:
        包含课程信息的字典，包括:
        - number: 课程编号
        - title: 课程标题
        - description: 课程描述
        - filename: 文件名（不含扩展名）
    """
    content = md_path.read_text(encoding="utf-8")
    title = extract_title(content)

    match = re.search(r"lesson-(\d+)", md_path.name)
    number = match.group(1) if match else "?"

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


def build_site() -> None:
    """构建静态网站.

    主要步骤:
        1. 创建输出目录结构
        2. 复制静态资源（CSS/JS）
        3. 复制站点 HTML 页面
        4. 转换 Markdown 课程文档
        5. 生成课程索引页面

    输出目录结构:
        _site/
        ├── index.html
        ├── assets/
        │   ├── css/style.css
        │   └── js/main.js
        ├── lessons/
        │   ├── index.html
        │   └── lesson-*.html
        └── pages/
            └── *.html
    """
    print(f"Building {PROJECT_NAME} website...")

    SITE_DIR.mkdir(exist_ok=True)
    LESSONS_DIR.mkdir(exist_ok=True)
    PAGES_DIR.mkdir(exist_ok=True)
    (ASSETS_DIR / "css").mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "js").mkdir(parents=True, exist_ok=True)

    if Path("site/assets/css/style.css").exists():
        shutil.copy("site/assets/css/style.css", ASSETS_DIR / "css" / "style.css")
    if Path("site/assets/js/main.js").exists():
        shutil.copy("site/assets/js/main.js", ASSETS_DIR / "js" / "main.js")

    # 复制docs目录到_site/docs/
    if DOCS_DIR.exists():
        docs_output = SITE_DIR / "docs"
        if docs_output.exists():
            shutil.rmtree(docs_output)
        shutil.copytree(DOCS_DIR, docs_output)
        print(f"  Copied docs/ directory")

    for html_file in Path("site").glob("*.html"):
        shutil.copy(html_file, SITE_DIR / html_file.name)
        print(f"  Copied {html_file.name}")

    if Path("site/index.html").exists():
        shutil.copy("site/index.html", SITE_DIR / "index.html")

    for page_name in PUBLIC_PAGES:
        page_path = DOCS_DIR / page_name
        if page_path.exists():
            title, html = process_public_page(page_path)
            output_path = PAGES_DIR / f"{page_path.stem}.html"
            output_path.write_text(html, encoding="utf-8")
            print(f"  Built page {title} -> {output_path.name}")

    lessons = []
    for md_file in sorted(DOCS_DIR.glob("lesson-*.md")):
        print(f"  Processing {md_file.name}...")

        title, html = process_lesson_file(md_file)
        output_path = LESSONS_DIR / f"{md_file.stem}.html"
        output_path.write_text(html, encoding="utf-8")

        lessons.append(get_lesson_info(md_file))

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

    print(f"Built {len(lessons)} lesson pages")
    print(f"Output: {SITE_DIR.absolute()}")


if __name__ == "__main__":
    build_site()
