#!/usr/bin/env python3
"""站点完整性检查：关键页面、导航脚本与测验覆盖。"""

from pathlib import Path

SITE_DIR = Path(__file__).resolve().parents[1] / "site"


def test_viewer_exists_for_local_site_root() -> None:
    """本地 Nginx 从 site/ 提供服务时需要 site/docs/viewer.html。"""
    assert (SITE_DIR / "docs" / "viewer.html").is_file()


def test_cheatsheet_redirects_to_command_sheet() -> None:
    """旧速查表入口应跳转到完整命令表。"""
    text = (SITE_DIR / "cheatsheet.html").read_text(encoding="utf-8")
    assert "command-sheet.html" in text
    assert "location.replace" in text or "refresh" in text


def test_user_pages_load_main_js_for_global_nav() -> None:
    """面向用户的页面应加载 main.js，以便注入/初始化全局导航。"""
    required = [
        "command-builder.html",
        "command-sheet.html",
        "search.html",
        "reference.html",
        "quick-start.html",
        "git-debugger.html",
        "interview.html",
        "workspace.html",
        "status.html",
        "diagnostics.html",
    ]
    for name in required:
        text = (SITE_DIR / name).read_text(encoding="utf-8")
        assert "assets/js/main.js" in text, f"{name} missing main.js"


def test_quiz_bank_covers_lesson_00b() -> None:
    """终端基础课应有独立测验题库。"""
    text = (SITE_DIR / "quiz.html").read_text(encoding="utf-8")
    assert "'lesson-00b'" in text
    assert "命令行与工作目录基础" in text


def test_command_builder_has_no_replacement_chars() -> None:
    """命令生成器页面不应再残留 UTF-8 截断替换符。"""
    text = (SITE_DIR / "command-builder.html").read_text(encoding="utf-8")
    assert "\ufffd" not in text


def test_global_navbar_can_self_inject() -> None:
    """main.js 应提供导航自动注入能力。"""
    text = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "ensure()" in text
    assert "data-no-global-nav" in text or "noGlobalNav" in text


def test_lessons_index_uses_parent_relative_links() -> None:
    """课程中心位于 lessons/ 下，链接需回到站点根。"""
    text = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert "../docs/viewer.html" in text
    assert "../workspace.html" in text
    assert 'href="docs/viewer.html' not in text


def test_search_and_reference_have_no_legacy_header() -> None:
    """搜索/参考页不应再保留旧 header，避免与全局导航叠层。"""
    for name in ("search.html", "reference.html"):
        text = (SITE_DIR / name).read_text(encoding="utf-8")
        assert '<header class="header">' not in text
        assert "assets/js/main.js" in text


def test_viewer_loads_markdown_via_relative_url() -> None:
    """viewer 应使用相对 URL 拉取 markdown，避免绝对 /docs 在 Pages 子路径失效。"""
    text = (SITE_DIR / "docs" / "viewer.html").read_text(encoding="utf-8")
    assert "new URL(file, window.location.href)" in text
    assert "fetch(`/docs/" not in text


def test_search_results_link_out() -> None:
    """搜索结果中的命令/概念应可跳转到对应页面。"""
    text = (SITE_DIR / "search.html").read_text(encoding="utf-8")
    assert "command-sheet.html?q=" in text
    assert "reference.html?q=" in text


def test_reference_supports_query_search() -> None:
    """参考页应支持 URL ?q= 与页面内搜索。"""
    text = (SITE_DIR / "reference.html").read_text(encoding="utf-8")
    assert "refSearchInput" in text
    assert "applyReferenceSearch" in text
    assert "URLSearchParams" in text


def test_activity_progress_keys_are_namespaced() -> None:
    """跨页活动进度应使用统一前缀，便于成就页汇总。"""
    main_js = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "ActivityProgress" in main_js
    assert "git-workflow-lab-challenge-progress" in main_js
    assert "git-workflow-lab-flashcard-stats" in main_js

    challenges = (SITE_DIR / "challenges.html").read_text(encoding="utf-8")
    assert "git-workflow-lab-challenge-progress" in challenges
    assert "challengeProgress" not in challenges

    achievements = (SITE_DIR / "achievements.html").read_text(encoding="utf-8")
    assert "ActivityProgress" in achievements
    assert "quiz-starter" in achievements
    assert "lesson-18" in achievements
    assert "lesson-19" in achievements


def test_gamification_syncs_from_activity_progress() -> None:
    """游戏化系统应从全站进度增量同步经验与每日任务。"""
    text = (SITE_DIR / "gamification.html").read_text(encoding="utf-8")
    assert "syncFromActivity" in text
    assert "git-workflow-lab-game-activity-sync" in text
    assert "ActivityProgress" in text


def test_index_has_personal_learning_dashboard() -> None:
    """首页应能在有学习记录时切换到个人仪表盘。"""
    text = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    assert "personal-dashboard" in text
    assert "dash-lessons" in text
    assert "ActivityProgress" in text
    assert ">23<" in text


def test_progress_events_are_emitted() -> None:
    """课程/测验进度变更应广播统一事件。"""
    main_js = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "git-workflow-lab:progress" in main_js
    assert "ActivityProgress.notify" in main_js or "notify(type" in main_js

    gamification = (SITE_DIR / "gamification.html").read_text(encoding="utf-8")
    assert "git-workflow-lab:progress" in gamification

    learning_path = (SITE_DIR / "learning-path.html").read_text(encoding="utf-8")
    assert "path-activity-strip" in learning_path
    assert "lesson-18" in learning_path
    assert "lesson-19" in learning_path
    assert "docs/viewer.html?file=" in learning_path


def test_viewer_normalizes_lesson_ids() -> None:
    """viewer 标记完成时应使用统一 lesson ID（含 lesson-00b）。"""
    text = (SITE_DIR / "docs" / "viewer.html").read_text(encoding="utf-8")
    assert "normalizeLessonId" in text
    assert "lesson-00-terminal-basics" in text
    assert "TOTAL_LESSONS: 23" in text


def test_shared_static_chrome_styles_exist() -> None:
    """静态壳层应提供统一页头、页脚与焦点样式。"""
    css = (SITE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    assert ".page-header" in css
    assert ".site-footer" in css
    assert ":focus-visible" in css
    assert "@import url('https://fonts.googleapis.com" not in css

    main_js = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "SiteChrome" in main_js
    assert "ensureFooter" in main_js


def test_diagnostics_uses_design_system() -> None:
    """诊断页应接入站点设计系统，并使用正确端口 8081。"""
    text = (SITE_DIR / "diagnostics.html").read_text(encoding="utf-8")
    assert "page-header" in text
    assert "assets/css/style.css" in text
    assert "8081" in text
    assert "8082" not in text
