#!/usr/bin/env python3
"""为缺少 main.js 的用户页面补齐脚本，并统一速查表链接。"""

from __future__ import annotations

import re
from pathlib import Path

SITE = Path("site")
SCRIPT = '    <script src="assets/js/main.js" defer></script>\n'
STYLE = '    <link rel="stylesheet" href="assets/css/style.css">\n'

NEED_MAIN = [
    "command-builder.html",
    "daily-plan.html",
    "diagnostics.html",
    "git-debugger.html",
    "gitflow-simulator.html",
    "interview.html",
    "notes.html",
    "projects.html",
    "search.html",
    "status.html",
    "workspace.html",
]


def ensure_main_js() -> None:
    for name in NEED_MAIN:
        path = SITE / name
        text = path.read_text(encoding="utf-8")
        if "assets/js/main.js" not in text:
            if "</body>" in text:
                text = text.replace("</body>", SCRIPT + "</body>", 1)
            else:
                text += "\n" + SCRIPT
        if name == "diagnostics.html" and "assets/css/style.css" not in text:
            text = text.replace("</head>", STYLE + "</head>", 1)
        path.write_text(text, encoding="utf-8")
        print(f"ensured main.js: {name}")


def rewrite_cheatsheet_links() -> None:
    updated = 0
    for path in SITE.rglob("*.html"):
        if path.name == "cheatsheet.html":
            continue
        text = path.read_text(encoding="utf-8")
        if "cheatsheet.html" not in text:
            continue
        path.write_text(text.replace("cheatsheet.html", "command-sheet.html"), encoding="utf-8")
        updated += 1
        print(f"updated cheatsheet refs: {path.relative_to(SITE)}")
    print(f"files updated for cheatsheet->command-sheet: {updated}")


def report_command_builder() -> None:
    text = (SITE / "command-builder.html").read_text(encoding="utf-8")
    print(f"command-builder fffd left: {text.count(chr(0xfffd))}")
    if chr(0xFFFD) in text:
        for i, line in enumerate(text.splitlines(), 1):
            if chr(0xFFFD) in line:
                print(f"  L{i}: {line}")


def main() -> None:
    ensure_main_js()
    mark_test_iframe()
    rewrite_cheatsheet_links()
    report_command_builder()


if __name__ == "__main__":
    main()
