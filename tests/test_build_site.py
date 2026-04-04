#!/usr/bin/env python3
"""Tests for build-site.py module.

Unit tests for the static site building functionality.
"""

import pytest
from pathlib import Path

from build_site import (
    extract_title,
    convert_markdown_to_html,
    fix_quotes,
    get_output_rel_path,
)


class TestExtractTitle:
    """Test cases for extract_title function."""

    def test_extract_title_basic(self) -> None:
        """Test basic title extraction."""
        content = "# Git Basics\n\nContent here."
        assert extract_title(content) == "Git Basics"

    def test_extract_title_no_heading(self) -> None:
        """Test extraction when no heading exists."""
        content = "No heading here."
        assert extract_title(content) == "Git Workflow Lab"

    def test_extract_title_multiple_headings(self) -> None:
        """Test extraction with multiple headings."""
        content = "# Main Title\n\n## Subtitle\n\nContent."
        assert extract_title(content) == "Main Title"

    def test_extract_title_with_formatting(self) -> None:
        """Test extraction with inline formatting."""
        content = "# Git **Basics** and *More*\n\nContent."
        assert extract_title(content) == "Git **Basics** and *More*"


class TestConvertMarkdownToHtml:
    """Test cases for convert_markdown_to_html function."""

    def test_convert_basic_markdown(self) -> None:
        """Test basic Markdown conversion."""
        content = "# Heading\n\nParagraph text."
        html = convert_markdown_to_html(content)
        assert "<h1" in html
        assert "Heading" in html
        assert "<p>" in html
        assert "Paragraph text." in html

    def test_convert_code_block(self) -> None:
        """Test code block conversion."""
        content = "```bash\ngit status\n```"
        html = convert_markdown_to_html(content)
        assert "<pre>" in html or "<code>" in html

    def test_convert_links(self) -> None:
        """Test link conversion."""
        content = "[Link](https://example.com)"
        html = convert_markdown_to_html(content)
        assert '<a href="https://example.com">Link</a>' in html

    def test_convert_lists(self) -> None:
        """Test list conversion."""
        content = "- Item 1\n- Item 2\n"
        html = convert_markdown_to_html(content)
        assert "<ul>" in html
        assert "<li>" in html


class TestFixQuotes:
    """Test cases for fix_quotes function."""

    def test_fix_chinese_double_quotes(self) -> None:
        """Test Chinese double quote replacement."""
        content = '"你好世界"'
        result = fix_quotes(content)
        assert result == '"你好世界"'

    def test_fix_chinese_single_quotes(self) -> None:
        """Test Chinese single quote replacement."""
        content = "'你好'"
        result = fix_quotes(content)
        assert result == "'你好'"

    def test_mixed_quotes(self) -> None:
        """Test mixed quote types."""
        content = '他说："你好"，她回答\'谢谢\''
        result = fix_quotes(content)
        assert result == '他说："你好"，她回答\'谢谢\''

    def test_no_change_needed(self) -> None:
        """Test content that doesn't need changes."""
        content = 'Already "correct" quotes'
        result = fix_quotes(content)
        assert result == content


class TestGetOutputRelPath:
    """Test cases for get_output_rel_path function."""

    def test_lesson_file_path(self) -> None:
        """Test path for lesson files."""
        md_path = Path("docs/lesson-01-intro.md")
        result = get_output_rel_path(md_path)
        assert str(result) == "lessons/lesson-01-intro.html"

    def test_non_lesson_file_path(self) -> None:
        """Test path for non-lesson files."""
        md_path = Path("docs/faq.md")
        result = get_output_rel_path(md_path)
        assert str(result) == "pages/faq.html"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
