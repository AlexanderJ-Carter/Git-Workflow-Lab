#!/usr/bin/env python3
"""从 site/assets/data/lessons.json 同步嵌入到 viewer、workspace、search、learning-path。"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "site" / "assets" / "data" / "lessons.json"

STAGE_MINUTES = {
    "lesson-30": 35,
    "lesson-31": 30,
    "lesson-32": 30,
    "lesson-33": 35,
    "lesson-34": 40,
    "lesson-35": 35,
    "lesson-36": 35,
    "lesson-37": 30,
    "lesson-38": 35,
}


def load_catalog() -> list[dict]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def viewer_title(lesson: dict) -> str:
    if lesson["id"] == "lessons-overview":
        return "总览：课程和阶段规划"
    badge = lesson.get("badge", "")
    return f"关卡 {badge}：{lesson['title']}"


def build_viewer_lessons(catalog: list[dict]) -> list[dict]:
    groups: list[dict] = []
    seen: set[str] = set()
    for lesson in catalog:
        group = lesson.get("group", "其他")
        if group not in seen:
            seen.add(group)
            groups.append({"group": group, "items": []})
        groups[-1]["items"].append(
            {
                "id": lesson["id"],
                "file": lesson["file"],
                "title": viewer_title(lesson),
                "badge": lesson.get("badge", ""),
            }
        )
    return groups


def build_lesson_details(catalog: list[dict]) -> dict[str, str]:
    details: dict[str, str] = {}
    for lesson in catalog:
        file_name = lesson["file"]
        group = lesson.get("group", "").split("·")[-1].strip() if "·" in lesson.get("group", "") else lesson.get("group", "")
        minutes = STAGE_MINUTES.get(lesson["id"], 30)
        desc = lesson.get("desc", "")
        if lesson["id"] == "lessons-overview":
            details[file_name] = "课程总览 · 建议先通读一遍"
        else:
            details[file_name] = f"{group} · {minutes}分钟 · {desc}"
    return details


def build_workspace_lessons(catalog: list[dict]) -> list[dict]:
    rows = []
    for lesson in catalog:
        if not lesson["id"].startswith("lesson-"):
            continue
        rows.append(
            {
                "id": lesson["id"],
                "file": lesson["file"],
                "title": lesson["title"],
                "badge": lesson.get("badge", ""),
                "quizId": lesson.get("quizId", lesson["id"]),
            }
        )
    return rows


def build_learning_path_lessons(catalog: list[dict]) -> list[dict]:
    rows = []
    for lesson in catalog:
        if not lesson["id"].startswith("lesson-"):
            continue
        rows.append(
            {
                "stage": lesson.get("stage", 0),
                "id": lesson["id"],
                "file": lesson["file"],
                "title": lesson["title"],
                "desc": lesson.get("desc", ""),
            }
        )
    return rows


def build_search_lessons(catalog: list[dict]) -> list[dict]:
    rows = []
    for lesson in catalog:
        if not lesson["id"].startswith("lesson-"):
            continue
        rows.append(
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "desc": lesson.get("desc", ""),
                "url": f"docs/viewer.html?file={lesson['file']}",
            }
        )
    return rows


def lesson_count(catalog: list[dict]) -> int:
    return sum(1 for lesson in catalog if lesson["id"].startswith("lesson-"))


def replace_js_const(text: str, name: str, value, decl: str = "const") -> str:
    payload = json.dumps(value, ensure_ascii=False, indent=2)
    opener = "{" if isinstance(value, dict) else "["
    pattern = rf"({decl} {re.escape(name)} = ){re.escape(opener)}[\s\S]*?\];"
    replacement = rf"\g<1>{payload};"
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise RuntimeError(f"无法替换 {decl} {name}")
    return updated


def replace_total_lessons(text: str, total: int) -> str:
    updated, count = re.subn(
        r"TOTAL_LESSONS: \d+",
        f"TOTAL_LESSONS: {total}",
        text,
    )
    if count < 1:
        raise RuntimeError("无法替换 TOTAL_LESSONS")
    return updated


def replace_progress_label(text: str, total: int) -> str:
    return text.replace("0/33 完成", f"0/{total} 完成").replace("0/33", f"0/{total}")


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start + len(start_marker))
    return text[: start + len(start_marker)] + replacement + text[end:]


def sync_viewer(path: Path, catalog: list[dict], total: int) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_total_lessons(text, total)
    lessons_payload = json.dumps(build_viewer_lessons(catalog), ensure_ascii=False, indent=2)
    details_payload = json.dumps(build_lesson_details(catalog), ensure_ascii=False, indent=2)
    text = replace_between(
        text,
        "const LESSONS = ",
        ";\n      \n      const LESSON_DETAILS",
        lessons_payload,
    )
    text = replace_between(
        text,
        "const LESSON_DETAILS = ",
        ";\n\n      function getQueryParam",
        details_payload,
    )
    path.write_text(text, encoding="utf-8")


def sync_workspace(path: Path, catalog: list[dict], total: int) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_total_lessons(text, total)
    text = replace_progress_label(text, total)
    text = replace_js_const(text, "FALLBACK_LESSONS", build_workspace_lessons(catalog))
    path.write_text(text, encoding="utf-8")


def sync_learning_path(path: Path, catalog: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_js_const(text, "LESSONS", build_learning_path_lessons(catalog), decl="let")
  # stage loop
    text = text.replace(
        "[0, 1, 2, 3, 4, 5, 6].forEach(stageIndex => {",
        "[0, 1, 2, 3, 4, 5, 6, 7].forEach(stageIndex => {",
    )
    text = text.replace(
        "const stageThresholds = [0.14, 0.28, 0.42, 0.56, 0.70, 0.84, 1];",
        "const stageThresholds = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1];",
    )
    if 'id="stage-7"' not in text:
        stage_block = """
            <div class="path-stage" id="path-stage-7">
                <div class="path-stage-header">
                <div class="path-stage-icon stage-7" id="stage-icon-7">I</div>
                <div class="path-stage-title">阶段 I：计算机基础</div>
                <div class="path-stage-meta">9 个关卡 · 约 5 小时</div>
            </div>
            <div class="path-cards" id="stage-7"></div>
        </div>
"""
        text = text.replace(
            '            <div class="path-cards" id="stage-6"></div>\n        </div>',
            '            <div class="path-cards" id="stage-6"></div>\n        </div>' + stage_block,
        )
    if ".path-stage-icon.stage-7" not in text:
        text = text.replace(
            ".path-stage-icon.stage-6 { background: #cffafe; color: #0e7490; }",
            ".path-stage-icon.stage-6 { background: #cffafe; color: #0e7490; }\n        .path-stage-icon.stage-7 { background: #fef3c7; color: #b45309; }",
        )
        text = text.replace(
            "[data-theme=\"dark\"] .path-stage-icon.stage-6 { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }",
            "[data-theme=\"dark\"] .path-stage-icon.stage-6 { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }\n        [data-theme=\"dark\"] .path-stage-icon.stage-7 { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }",
        )
    if "阶段 I：计算机基础" not in text.split("function renderCards")[0]:
        text = text.replace(
            "<li>阶段 H 进阶实用：Fork、hotfix、submodule、历史整理、考古与 sparse checkout</li>",
            "<li>阶段 H 进阶实用：Fork、hotfix、submodule、历史整理、考古与 sparse checkout</li>\n                <li>阶段 I 计算机基础：Shell、管道、环境变量、Docker、HTTP、文本处理、网络排查、YAML/JSON</li>",
        )
    path.write_text(text, encoding="utf-8")


def sync_search(path: Path, catalog: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    lessons = build_search_lessons(catalog)
    pattern = r"(courses:\s*\[)[\s\S]*?(\],\s*// Git 命令)"
    payload = json.dumps(lessons, ensure_ascii=False, indent=12)
    replacement = rf"\g<1>\n{payload}\n            \2"
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise RuntimeError("无法替换 search courses 数组")
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    catalog = load_catalog()
    total = lesson_count(catalog)

    sync_viewer(ROOT / "docs" / "viewer.html", catalog, total)
    sync_viewer(ROOT / "site" / "docs" / "viewer.html", catalog, total)
    sync_workspace(ROOT / "site" / "workspace.html", catalog, total)
    sync_learning_path(ROOT / "site" / "learning-path.html", catalog)
    sync_search(ROOT / "site" / "search.html", catalog)

    print(f"Synced {total} lessons from {CATALOG}")


if __name__ == "__main__":
    main()
