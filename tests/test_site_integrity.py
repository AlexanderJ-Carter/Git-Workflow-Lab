#!/usr/bin/env python3
"""站点完整性检查：关键页面、导航脚本与测验覆盖。"""

from pathlib import Path
import json

SITE_DIR = Path(__file__).resolve().parents[1] / "site"


def test_viewer_exists_for_local_site_root() -> None:
    """本地 Nginx 从 site/ 提供服务时需要 site/docs/viewer.html。"""
    assert (SITE_DIR / "docs" / "viewer.html").is_file()


def test_docs_index_redirects_to_viewer() -> None:
    """/docs/ 与 /docs/index.html 应跳转到文档阅读器，避免 404。"""
    root = Path(__file__).resolve().parents[1]
    for path in (root / "docs/index.html", SITE_DIR / "docs/index.html"):
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert "viewer.html?file=lessons-overview.md" in text
        assert "location.replace" in text or "refresh" in text


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


def test_lesson_catalog_covers_all_lessons() -> None:
    """共享课程目录应覆盖 48 个课程关卡并保留 stage 映射。"""
    catalog_path = SITE_DIR / "assets" / "data" / "lessons.json"
    assert catalog_path.is_file()
    lessons = json.loads(catalog_path.read_text(encoding="utf-8"))
    lesson_entries = [lesson for lesson in lessons if str(lesson["id"]).startswith("lesson-")]
    ids = {lesson["id"] for lesson in lesson_entries}
    assert len(lesson_entries) == 48
    assert {
        "lesson-00b",
        "lesson-06a",
        "lesson-06b",
        "lesson-20",
        "lesson-21",
        "lesson-22",
        "lesson-23",
        "lesson-24",
        "lesson-25",
        "lesson-26",
        "lesson-27",
        "lesson-28",
        "lesson-29",
        "lesson-30",
        "lesson-31",
        "lesson-32",
        "lesson-33",
        "lesson-34",
        "lesson-35",
        "lesson-36",
        "lesson-37",
        "lesson-38",
        "lesson-39",
        "lesson-40",
        "lesson-41",
        "lesson-42",
        "lesson-43",
        "lesson-44",
    }.issubset(ids)
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 2} == {
        "lesson-07",
        "lesson-08",
        "lesson-09",
        "lesson-20",
        "lesson-21",
    }
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 3} == {
        "lesson-13",
        "lesson-14",
        "lesson-15",
        "lesson-16",
        "lesson-17",
        "lesson-22",
        "lesson-23",
    }
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 4} == {"lesson-10", "lesson-11", "lesson-12"}
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 5} == {"lesson-18", "lesson-19"}
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 6} == {
        "lesson-24",
        "lesson-25",
        "lesson-26",
        "lesson-27",
        "lesson-28",
        "lesson-29",
    }
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 7} == {
        "lesson-30",
        "lesson-31",
        "lesson-32",
        "lesson-33",
        "lesson-34",
        "lesson-35",
        "lesson-36",
        "lesson-37",
        "lesson-38",
    }
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 8} == {
        "lesson-39",
        "lesson-40",
        "lesson-41",
    }
    assert {lesson["id"] for lesson in lesson_entries if lesson["stage"] == 9} == {
        "lesson-42",
        "lesson-43",
        "lesson-44",
    }


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
    assert "LessonCatalog.load" in achievements
    assert "CATALOG_LESSONS" in achievements


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
    assert ">48<" in text or "<strong>48</strong>" in text
    assert "仅浏览 (Pages)" in text
    assert "本地 Docker 实验" in text
    assert "learning-modes.md" in text


def test_learning_path_loads_lessons_dynamically() -> None:
    """学习路径应从 lessons.json 动态渲染具体课程卡片。"""
    text = (SITE_DIR / "learning-path.html").read_text(encoding="utf-8")
    assert "loadLessonCatalog" in text
    assert 'id="path-timeline"' in text
    assert "renderTimeline" in text
    assert "path-activity-strip" in text


def test_progress_events_are_emitted() -> None:
    """课程/测验进度变更应广播统一事件。"""
    main_js = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "git-workflow-lab:progress" in main_js
    assert "ActivityProgress.notify" in main_js or "notify(type" in main_js

    gamification = (SITE_DIR / "gamification.html").read_text(encoding="utf-8")
    assert "git-workflow-lab:progress" in gamification


def test_viewer_normalizes_lesson_ids() -> None:
    """viewer 标记完成时应使用统一 lesson ID（含 lesson-00b）。"""
    text = (SITE_DIR / "docs" / "viewer.html").read_text(encoding="utf-8")
    assert "normalizeLessonId" in text
    assert "lesson-00-terminal-basics" in text
    assert "TOTAL_LESSONS: 48" in text
    assert "lesson-20-bisect.md" in text
    assert "lesson-21-worktree.md" in text
    assert "lesson-22-conventional-commits.md" in text
    assert "lesson-29-sparse-checkout.md" in text
    assert "lesson-38-json-yaml-devops.md" in text
    assert "lesson-41-cli-cross-platform.md" in text
    assert "lesson-44-gitattributes.md" in text
    assert "本课测验" in text
    assert "复习闪卡" in text
    assert "打开工作台" in text


def test_new_lessons_are_linked_from_learning_loop_pages() -> None:
    """课程中心、学习路径、搜索、测验与工作台应接入新增课程。"""
    advanced_git = (
        "lesson-20", "lesson-21", "lesson-22", "lesson-23", "lesson-24",
        "lesson-25", "lesson-26", "lesson-27", "lesson-28", "lesson-29",
    )
    computer_basics = (
        "lesson-30", "lesson-31", "lesson-32", "lesson-33", "lesson-34",
        "lesson-35", "lesson-36", "lesson-37", "lesson-38",
    )
    programming_cli = ("lesson-39", "lesson-40", "lesson-41")
    config_text = ("lesson-42", "lesson-43", "lesson-44")
    for name in ("search.html", "quiz.html", "workspace.html"):
        text = (SITE_DIR / name).read_text(encoding="utf-8")
        for lesson_id in (*advanced_git, *computer_basics, *programming_cli, *config_text):
            assert lesson_id in text, f"{name} missing {lesson_id}"

    learning_path = (SITE_DIR / "learning-path.html").read_text(encoding="utf-8")
    assert 'id="path-timeline"' in learning_path
    assert "LessonCatalog" in learning_path
    assert "renderTimeline" in learning_path

    lessons_index = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert "assets/data/lessons.json" in lessons_index
    assert 'target="_blank"' not in lessons_index
    assert "stage-7" in lessons_index
    assert "stage-8" in lessons_index
    assert "stage-9" in lessons_index
    assert "GitWorkflowLab" in lessons_index or "LearningProgress" in lessons_index

    quiz = (SITE_DIR / "quiz.html").read_text(encoding="utf-8")
    assert "docs/viewer.html?file=lesson-20-bisect.md" in quiz
    assert "docs/viewer.html?file=lesson-21-worktree.md" in quiz
    assert "docs/viewer.html?file=lesson-22-conventional-commits.md" in quiz
    assert "docs/viewer.html?file=lesson-29-sparse-checkout.md" in quiz
    assert "docs/viewer.html?file=lesson-41-cli-cross-platform.md" in quiz
    assert "docs/viewer.html?file=lesson-44-gitattributes.md" in quiz
    assert "lessons/lesson-20" not in quiz

    workspace = (SITE_DIR / "workspace.html").read_text(encoding="utf-8")
    assert "TOTAL_LESSONS: 48" in workspace
    assert "pendingCommand" in workspace
    assert "ssh -T git@localhost -p 2222" in workspace
    assert "playground-hello.git" in workspace


def test_no_8082_leftovers() -> None:
    """本地站点统一使用 8081，不应残留 8082。"""
    for path in SITE_DIR.rglob("*.html"):
        assert "8082" not in path.read_text(encoding="utf-8"), f"{path.name} contains 8082"


def test_motion_micro_interactions_exist() -> None:
    """样式系统提供轻量动效并尊重减少动态效果设置。"""
    css = (SITE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    main_js = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "--motion-duration-fast" in css
    assert ".fade-in" in css
    assert ":active" in css
    assert ".mark-complete-btn.is-done" in css
    assert "prefers-reduced-motion: reduce" in css
    assert "fade-in" in main_js


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


def test_lessons_index_has_stage_nine() -> None:
    """课程中心应包含阶段 K 配置与文本处理区块。"""
    text = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert 'id="stage-9"' in text
    assert "配置与文本处理" in text


def test_lessons_index_has_stage_eight() -> None:
    """课程中心应包含阶段 J 编程与跨平台 CLI 区块。"""
    text = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert 'id="stage-8"' in text
    assert "编程与跨平台" in text


def test_lessons_index_has_stage_seven() -> None:
    """课程中心应包含阶段 I 计算机基础区块。"""
    text = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert 'id="stage-7"' in text
    assert "计算机基础" in text
    assert "learning-modes.md" in text


def test_build_site_includes_v3_assets() -> None:
    """GitHub Pages 构建应包含 pages.css、lessons.json，且 style.css 已合并布局样式。"""
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "scripts" / "build-site.py")], cwd=root, check=True)
    assert (root / "_site" / "assets" / "css" / "pages.css").is_file()
    style_css = (root / "_site" / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    assert (root / "_site" / "assets" / "data" / "lessons.json").is_file()
    assert ".hero-v3" in style_css
    assert "bundled pages.css" in style_css
    index = (root / "_site" / "index.html").read_text(encoding="utf-8")
    assert "assets/css/style.css?v=4" in index
    assert "assets/css/pages.css" not in index
    assert "asset-base.js" in index


def test_lessons_index_asset_paths_are_parent_relative() -> None:
    """课程中心位于 lessons/ 下，静态资源必须用 ../assets。"""
    text = (SITE_DIR / "lessons" / "index.html").read_text(encoding="utf-8")
    assert 'href="../assets/css/style.css"' in text
    assert 'src="../assets/js/asset-base.js"' in text
    assert 'src="../assets/js/main.js"' in text
    assert 'href="assets/css/style.css"' not in text


def test_all_user_facing_pages_load_main_js() -> None:
    """除明确重定向页外，站点根目录用户页均应加载 main.js。"""
    skip = {
        "cheatsheet.html",  # redirect to command-sheet
    }
    missing = []
    for path in sorted(SITE_DIR.glob("*.html")):
        if path.name in skip:
            continue
        text = path.read_text(encoding="utf-8")
        if "assets/js/main.js" not in text:
            missing.append(path.name)
    assert missing == [], f"pages missing main.js: {missing}"


def test_quiz_does_not_auto_complete_lessons() -> None:
    """测验通过只写入 QuizProgress，不再自动标记课程阅读完成。"""
    text = (SITE_DIR / "quiz.html").read_text(encoding="utf-8")
    assert "LearningProgress.saveProgress" not in text
    assert "saveLessonProgressFallback" not in text
    assert "测验已通过" in text or "测验进度" in text


def test_achievements_use_lesson_catalog_not_hardcoded_20() -> None:
    """成就页应从 LessonCatalog / lessons.json 派生课程数，而非硬编码约 20 课。"""
    text = (SITE_DIR / "achievements.html").read_text(encoding="utf-8")
    assert "LessonCatalog.load" in text
    assert "CATALOG_LESSONS" in text
    assert "{ stage: 0, id: 'lesson-00' }" not in text
    assert "AchievementStore" in text


def test_main_js_exposes_progress_api_and_streak() -> None:
    """main.js 应暴露统一进度 API 与活跃日 streak 计算。"""
    text = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "toggleComplete(lessonId)" in text
    assert "normalizeLessonId" in text
    assert "calculateStreak()" in text
    assert "getActiveDateStrings()" in text


def test_gamification_disables_manual_task_clicks() -> None:
    """游戏化每日任务不可点击刷分。"""
    text = (SITE_DIR / "gamification.html").read_text(encoding="utf-8")
    assert "handleTaskClick" not in text
    assert "toggleTask" not in text
    assert "通过完成课程、测验、挑战或闪卡自动完成" in text
    assert "ActivityProgress?.calculateStreak" in text or "ActivityProgress.calculateStreak" in text


def test_skill_tree_has_no_progress_polling() -> None:
    """技能树不应每 5 秒轮询并清空派生进度。"""
    text = (SITE_DIR / "skill-tree.html").read_text(encoding="utf-8")
    assert "setInterval" not in text
    assert "removeItem('git-workflow-lab-skill-tree-progress')" not in text
    assert "assets/js/main.js" in text


def test_viewer_uses_vendored_marked() -> None:
    """文档阅读器应优先使用本地 marked，避免纯 CDN 依赖。"""
    text = (SITE_DIR / "docs" / "viewer.html").read_text(encoding="utf-8")
    assert "assets/js/vendor/marked.min.js" in text
    assert (SITE_DIR / "assets" / "js" / "vendor" / "marked.min.js").is_file()


def test_workspace_service_urls_are_configurable() -> None:
    """工作台终端/Gitea 地址应支持 query 与 localStorage 覆盖。"""
    text = (SITE_DIR / "workspace.html").read_text(encoding="utf-8")
    assert "resolveServiceUrl" in text
    assert "sanitizeServiceUrl" in text
    assert "git-workflow-lab-terminal-url" in text
    assert "本地实验模式" in text


def test_check_env_script_exists() -> None:
    """环境校验脚本应存在且可执行。"""
    script = Path(__file__).resolve().parents[1] / "scripts" / "check-env.sh"
    assert script.is_file()
    text = script.read_text(encoding="utf-8")
    assert "--generate" in text
    assert "GITEA_SECRET_KEY" in text
