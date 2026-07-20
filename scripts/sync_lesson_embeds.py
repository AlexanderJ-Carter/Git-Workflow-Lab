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
    "lesson-39": 40,
    "lesson-40": 35,
    "lesson-41": 30,
    "lesson-42": 35,
    "lesson-43": 30,
    "lesson-44": 35,
}

STAGE_META = {
    7: ("I", "阶段 I：计算机基础", "9 个关卡 · 约 5 小时", "#fef3c7", "#b45309"),
    8: ("J", "阶段 J：编程与跨平台 CLI", "3 个关卡 · 约 2.5 小时", "#ede9fe", "#6d28d9"),
    9: ("K", "阶段 K：配置与文本处理", "3 个关卡 · 约 1.75 小时", "#ccfbf1", "#0f766e"),
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


def max_stage(catalog: list[dict]) -> int:
    stages = [lesson.get("stage", 0) for lesson in catalog if lesson["id"].startswith("lesson-")]
    return max(stages) if stages else 0


def stage_thresholds(max_index: int) -> list[float]:
    if max_index <= 0:
        return [1.0]
    step = 1 / (max_index + 1)
    return [round(step * (index + 1), 3) for index in range(max_index + 1)]


def ensure_learning_path_stage(text: str, stage_index: int) -> str:
    if f'id="stage-{stage_index}"' in text:
        return text
    letter, title, meta, bg, fg = STAGE_META.get(
        stage_index,
        (chr(ord("A") + stage_index), f"阶段 {stage_index}", "若干关卡", "#e2e8f0", "#334155"),
    )
    stage_block = f"""
            <div class="path-stage" id="path-stage-{stage_index}">
                <div class="path-stage-header">
                <div class="path-stage-icon stage-{stage_index}" id="stage-icon-{stage_index}">{letter}</div>
                <div class="path-stage-title">{title}</div>
                <div class="path-stage-meta">{meta}</div>
            </div>
            <div class="path-cards" id="stage-{stage_index}"></div>
        </div>
"""
    anchor = f'            <div class="path-cards" id="stage-{stage_index - 1}"></div>\n        </div>'
    if anchor not in text:
        raise RuntimeError(f"无法在 learning-path 中插入 stage-{stage_index}")
    return text.replace(anchor, anchor + stage_block, 1)


def sync_learning_path(path: Path, catalog: list[dict]) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_js_const(text, "LESSONS", build_learning_path_lessons(catalog), decl="let")
    last_stage = max_stage(catalog)
    stage_loop = ", ".join(str(index) for index in range(last_stage + 1))
    text = re.sub(
        r"\[[0-9,\s]+\]\.forEach\(stageIndex => \{",
        f"[{stage_loop}].forEach(stageIndex => {{",
        text,
        count=1,
    )
    thresholds = stage_thresholds(last_stage)
    text = re.sub(
        r"const stageThresholds = \[[^\]]+\];",
        f"const stageThresholds = {json.dumps(thresholds)};",
        text,
        count=1,
    )
    for stage_index in range(7, last_stage + 1):
        text = ensure_learning_path_stage(text, stage_index)
        if stage_index in STAGE_META:
            _, _, _, bg, fg = STAGE_META[stage_index]
            css_rule = f".path-stage-icon.stage-{stage_index} {{ background: {bg}; color: {fg}; }}"
            if css_rule not in text:
                text = text.replace(
                    f".path-stage-icon.stage-{stage_index - 1}",
                    f".path-stage-icon.stage-{stage_index - 1}",
                    1,
                )
                text = text.replace(
                    f".path-stage-icon.stage-{stage_index - 1} {{",
                    f".path-stage-icon.stage-{stage_index - 1} {{\n        {css_rule}",
                    1,
                )
    if "阶段 J：编程与跨平台" not in text.split("function renderCards")[0]:
        text = text.replace(
            "<li>阶段 I 计算机基础：Shell、管道、环境变量、Docker、HTTP、文本处理、网络排查、YAML/JSON</li>",
            "<li>阶段 I 计算机基础：Shell、管道、环境变量、Docker、HTTP、文本处理、网络排查、YAML/JSON</li>\n                <li>阶段 J 编程与跨平台：Python 入门、PowerShell、Bash/PowerShell 对照</li>",
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
    sync_search(ROOT / "site" / "search.html", catalog)

    print(f"Synced {total} lessons from {CATALOG}")


if __name__ == "__main__":
    main()
