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


def test_main_js_exposes_command_palette() -> None:
    """全站命令面板应在 main.js 中定义、初始化并暴露到全局命名空间。"""
    text = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "const CommandPalette = {" in text
    assert "CommandPalette.init();" in text
    assert "CommandPalette.toggle()" in text  # 由 KeyboardShortcuts 在 Cmd/Ctrl+K 调用
    # 暴露到 GitWorkflowLab 命名空间，便于页面按需调用
    assert "CommandPalette," in text
    # 模糊匹配与键盘导航核心能力齐备
    assert "score(query, hay)" in text or "score(q, hay)" in text
    assert "ArrowDown" in text and "ArrowUp" in text and "runActive" in text


def test_command_palette_triggers_include_slash_and_k() -> None:
    """命令面板应支持 Cmd/Ctrl+K 与 / 打开、? 显示帮助。"""
    text = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "e.key === 'k'" in text and "CommandPalette.toggle()" in text
    assert "e.key === '/'" in text and "CommandPalette.open()" in text
    assert "e.key === '?'" in text and "showHelp" in text
    # 旧版「Cmd/Ctrl+K 聚焦搜索框」的行为已退役，改为打开命令面板
    assert "searchInput.focus()" not in text
    assert "searchInput.select()" not in text


def test_activity_progress_supports_backup_and_reset() -> None:
    """ActivityProgress 应提供导出 / 导入 / 清空三类数据管理方法。"""
    text = (SITE_DIR / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    assert "exportData()" in text
    assert "importFromPrompt()" in text
    assert "importData(jsonText)" in text
    assert "resetAllWithConfirm()" in text
    assert "collectData()" in text
    # 导出文件名带备份前缀，且仅导出本应用命名空间键 + 主题
    assert "git-workflow-lab-backup-" in text
    assert "this.PREFIX" in text and "git-workflow-lab-" in text
    # 清空仅作用于前缀键，不触碰主题
    reset_block = text[text.find("resetAllWithConfirm"):]
    assert "theme" in reset_block


def test_index_dashboard_has_data_management() -> None:
    """首页个人仪表盘应提供导出 / 导入 / 清空进度入口并接线。"""
    text = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    assert 'dashboard-actions--data' in text
    assert 'data-action="export"' in text
    assert 'data-action="import"' in text
    assert 'data-action="reset"' in text
    assert 'btn--danger' in text
    # 按钮点击应派发到 ActivityProgress 对应方法
    assert "AP.exportData?.()" in text
    assert "AP.importFromPrompt?.()" in text
    assert "AP.resetAllWithConfirm?.()" in text


def test_style_has_command_palette_rules() -> None:
    """样式表应包含命令面板与危险按钮样式，且尊重减少动态效果。"""
    css = (SITE_DIR / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    assert ".cmdk" in css
    assert ".cmdk__panel" in css
    assert ".cmdk__row.is-active" in css
    assert ".btn--danger" in css
    assert ".dashboard-actions--data" in css
    # 命令面板动效在减少动态效果时被禁用
    assert "prefers-reduced-motion: reduce" in css


# ============================================
# 共享 AI 客户端与集成（用户自备 Key + 注入项目知识）
# ============================================

def test_ai_client_module_exists_and_exposed() -> None:
    """共享 AI 客户端模块应存在、可拷贝，并以增强方式挂载到 GitWorkflowLab。"""
    ai = SITE_DIR / "assets" / "js" / "ai.js"
    assert ai.is_file()
    text = ai.read_text(encoding="utf-8")
    assert ".AIClient = AIClient" in text  # 挂载到命名空间（增强而非覆盖，避免抹掉 main.js 字段）
    assert "git-ai-settings" in text  # 复用现有设置键
    assert "buildSystemPrompt" in text
    assert "async ask(" in text
    # 三层上下文：静态项目自述 + 课程地图 + 页面上下文
    assert "Git Workflow Lab" in text and "48" in text and "阶段 A" in text


def test_ai_client_request_shapes_preserve_providers() -> None:
    """共享模块应忠实复刻 Anthropic / OpenAI 请求形态，并修复 system 字段丢失。"""
    text = (SITE_DIR / "assets" / "js" / "ai.js").read_text(encoding="utf-8")
    # Anthropic（Claude Messages API）
    assert "api.anthropic.com/v1/messages" in text
    assert "x-api-key" in text
    assert "anthropic-version" in text
    assert "system: systemPrompt" in text  # 修复：system 作为顶层字段传递
    # OpenAI / OpenAI 兼容（含 custom）
    assert "chat/completions" in text
    assert "Authorization" in text and "Bearer" in text
    # 旧版「删掉首条 system 消息」的实现不应残留
    assert "messages.slice(1)" not in text
    # endpoint 必须做 http(s) 校验，避免 javascript:/data: 注入
    assert "sanitizeEndpoint" in text
    assert "^https?" in text


def test_ai_client_has_shared_settings_modal() -> None:
    """约束 A：全站可用的设置弹窗与 isConfigured 守卫。"""
    text = (SITE_DIR / "assets" / "js" / "ai.js").read_text(encoding="utf-8")
    assert "openSettings(" in text
    assert "isConfigured()" in text
    assert "anthropic" in text and "openai" in text and "custom" in text


def test_ai_pages_load_module() -> None:
    """各 AI 集成页应加载共享 ai.js。"""
    pages = [
        "workspace.html",
        "quiz.html",
        "git-debugger.html",
        "docs/viewer.html",
        "ai-assistant.html",
    ]
    for name in pages:
        text = (SITE_DIR / name).read_text(encoding="utf-8")
        assert "assets/js/ai.js" in text, f"{name} missing ai.js"


def test_workspace_ai_tutor_panel() -> None:
    """工作台 AI 助教：侧滑面板 + 问题上下文组装（当前课程/正文/待运行命令）。"""
    text = (SITE_DIR / "workspace.html").read_text(encoding="utf-8")
    assert 'id="ai-tutor-panel"' in text
    assert 'id="guide-ai-toggle"' in text
    assert "assembleContext" in text
    assert "GitWorkflowLab.AIClient" in text
    # 如实告知终端跨源限制（ttyd :8080 与站点不同源，无法自动读取终端输出）
    assert "跨源" in text or "无法自动读取" in text


def test_quiz_ai_explain_on_wrong_answer() -> None:
    """测验错答时提供 AI 解析。"""
    text = (SITE_DIR / "quiz.html").read_text(encoding="utf-8")
    assert "quiz-ai-explain-btn" in text
    assert "quizExplainWithAI" in text
    assert "AI 解析" in text


def test_debugger_ai_explainer() -> None:
    """错误排查页：每条规则 + 空状态兜底均接 AI。"""
    text = (SITE_DIR / "git-debugger.html").read_text(encoding="utf-8")
    assert "explainErrorWithAI" in text
    assert "explainRawErrorWithAI" in text
    assert "ai-explain-raw" in text  # 空状态输出容器


def test_viewer_ai_qa_injects_lesson_md() -> None:
    """课程阅读器：AI 问答注入当前课程原文 md。"""
    text = (SITE_DIR / "docs" / "viewer.html").read_text(encoding="utf-8")
    assert 'id="lesson-ai-toggle"' in text
    assert 'id="lesson-ai-panel"' in text
    assert "__gwlCurrentLesson" in text
    assert "assets/js/ai.js" in text


def test_ai_assistant_delegates_and_drops_buggy_slice() -> None:
    """ai-assistant 页应委托共享模块，并移除旧版丢弃 system 的实现。"""
    text = (SITE_DIR / "ai-assistant.html").read_text(encoding="utf-8")
    assert "assets/js/ai.js" in text
    assert "AIC.ask" in text or "AIClient.ask" in text
    assert "messages.slice(1)" not in text


def test_build_ships_ai_module_and_vendor() -> None:
    """构建应拷贝 ai.js 与 vendor/marked.min.js 到 _site，并对 ai.js 做缓存破除。"""
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "scripts" / "build-site.py")], cwd=root, check=True)
    assert (root / "_site" / "assets" / "js" / "ai.js").is_file()
    assert (root / "_site" / "assets" / "js" / "vendor" / "marked.min.js").is_file()
    # 缓存破除 ?v=4 应用到 AI 页
    for name in ("workspace.html", "quiz.html", "git-debugger.html", "ai-assistant.html"):
        html = (root / "_site" / name).read_text(encoding="utf-8")
        assert "assets/js/ai.js?v=4" in html, f"{name} missing ai.js?v=4"
    # build script 递归拷贝子目录（修复 vendor 未上线的问题）
    assert "shutil.copytree" in (root / "scripts" / "build-site.py").read_text(encoding="utf-8")

