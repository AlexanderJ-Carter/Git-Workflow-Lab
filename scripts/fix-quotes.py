#!/usr/bin/env python3
"""修复 HTML 文件中的中文引号问题.

本脚本用于将 HTML 文件中的中文全角引号替换为标准 ASCII 引号，
以确保跨平台兼容性和工具链支持.

使用方法:
    $ python scripts/fix-quotes.py

处理的引号类型:
    - " (U+201C) → " (U+0022) 左双引号
    - " (U+201D) → " (U+0022) 右双引号
    - ' (U+2018) → ' (U+0027) 左单引号
    - ' (U+2019) → ' (U+0027) 右单引号

Example:
    >>> from scripts.fix_quotes import fix_quotes
    >>> fix_quotes('"你好"')
    '"你好"'
"""

from pathlib import Path


def fix_quotes(content: str) -> str:
    """替换中文引号为 ASCII 引号.

    Args:
        content: 包含可能中文引号的文本内容.

    Returns:
        替换后的文本内容，所有中文引号已转换为 ASCII 引号.

    Example:
        >>> fix_quotes('他说："你好"')
        '他说："你好"'
    """
    content = content.replace("\u201c", '"')  # "
    content = content.replace("\u201d", '"')  # "
    content = content.replace("\u2018", "'")  # '
    content = content.replace("\u2019", "'")  # '
    return content


def main() -> None:
    """执行批量修复 HTML 文件中的中文引号.

    遍历 site/ 目录下的所有 HTML 文件，检查并修复中文引号问题.
    处理完成后输出统计信息.
    """
    site_dir = Path("site")
    fixed_count = 0

    for html_file in site_dir.glob("**/*.html"):
        try:
            content = html_file.read_text(encoding="utf-8")
            new_content = fix_quotes(content)

            if content != new_content:
                html_file.write_text(new_content, encoding="utf-8")
                print(f"Fixed: {html_file}")
                fixed_count += 1
            else:
                print(f"OK: {html_file}")
        except Exception as e:
            print(f"Error processing {html_file}: {e}")

    print(f"\nTotal fixed: {fixed_count} files")


if __name__ == "__main__":
    main()
