from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


REQUIRED_TEXT_FIELDS = (
    "id", "name", "source", "permission", "original_description",
    "target_customer", "buying_context", "pain", "promise", "format",
    "delivery", "duration", "boundaries", "customer_input", "pricing",
    "value_anchor", "trust_evidence", "acquisition",
    "transferable_structure", "non_transferable_conditions",
    "completeness", "confidence", "recorded_at", "updated_at",
)

SECTION_FIELDS = (
    ("原始产品描述", "original_description"),
    ("目标客户", "target_customer"),
    ("购买情境", "buying_context"),
    ("痛点", "pain"),
    ("结果承诺", "promise"),
    ("产品形态", "format"),
    ("交付机制", "delivery"),
    ("周期", "duration"),
    ("边界", "boundaries"),
    ("客户配合", "customer_input"),
    ("定价", "pricing"),
    ("价值锚点", "value_anchor"),
    ("信任证据", "trust_evidence"),
    ("获客与成交", "acquisition"),
    ("可迁移结构", "transferable_structure"),
    ("不可照搬条件", "non_transferable_conditions"),
)


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", value.lower(), flags=re.UNICODE)
    return slug.strip("-_")


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def validate_record(record: dict[str, object]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for field in REQUIRED_TEXT_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(ValidationIssue(field, "must be a non-empty string"))
    identifier = record.get("id")
    if isinstance(identifier, str) and identifier != slugify(identifier):
        issues.append(ValidationIssue("id", "must already be a lowercase slug"))
    permission = record.get("permission")
    if isinstance(permission, str) and permission.strip() in {"未确认", "未知", ""}:
        issues.append(ValidationIssue("permission", "must explicitly state save and reuse permission"))
    tags = record.get("tags")
    if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        issues.append(ValidationIssue("tags", "must be a non-empty list of strings"))
    recorded_at = _parse_date(record.get("recorded_at"))
    updated_at = _parse_date(record.get("updated_at"))
    if recorded_at is None:
        issues.append(ValidationIssue("recorded_at", "must use YYYY-MM-DD"))
    if updated_at is None:
        issues.append(ValidationIssue("updated_at", "must use YYYY-MM-DD"))
    elif recorded_at is None:
        issues.append(ValidationIssue("updated_at", "cannot be ordered until recorded_at is valid"))
    if recorded_at and updated_at and updated_at < recorded_at:
        issues.append(ValidationIssue("updated_at", "must not precede recorded_at"))
    return issues


def render_case(record: dict[str, object]) -> str:
    tags = ", ".join(str(tag) for tag in record["tags"])
    metadata = [
        "---", f'id: "{record["id"]}"', f'name: "{record["name"]}"',
        f'source: "{record["source"]}"', f'permission: "{record["permission"]}"',
        f'tags: [{", ".join(repr(tag) for tag in record["tags"])}]',
        f'completeness: "{record["completeness"]}"', f'confidence: "{record["confidence"]}"',
        f'recorded_at: "{record["recorded_at"]}"', f'updated_at: "{record["updated_at"]}"', "---", "",
        f'# {record["name"]}', "",
    ]
    sections: list[str] = []
    for title, field in SECTION_FIELDS:
        sections.extend((f"## {title}", "", str(record[field]).strip(), ""))
    sections.extend(("## 标签", "", tags, ""))
    return "\n".join(metadata + sections)


def _parse_scalar(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_case(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"{path} has no frontmatter")
    record: dict[str, object] = {}
    for line in parts[1].strip().splitlines():
        key, separator, raw_value = line.partition(":")
        if not separator:
            continue
        value = raw_value.strip()
        if key == "tags":
            record[key] = [_parse_scalar(item) for item in value.strip("[]").split(",") if item.strip()]
        else:
            record[key] = _parse_scalar(value)
    body = parts[2]
    heading_to_field = {title: field for title, field in SECTION_FIELDS}
    matches = list(re.finditer(r"^## (.+)$", body, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        field = heading_to_field.get(title)
        if field:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            record[field] = body[match.end():end].strip()
    return record


def iter_case_paths(cases_dir: Path) -> Iterable[Path]:
    return sorted(path for path in cases_dir.glob("*.md") if path.is_file())


def write_case(record: dict[str, object], cases_dir: Path) -> Path:
    issues = validate_record(record)
    if issues:
        detail = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        raise ValueError(detail)
    cases_dir.mkdir(parents=True, exist_ok=True)
    destination = cases_dir / f'{record["id"]}.md'
    if destination.exists():
        raise ValueError(f'case id {record["id"]} already exists')
    destination.write_text(render_case(record), encoding="utf-8")
    return destination


def render_index(records: list[dict[str, object]]) -> str:
    lines = [
        "# 产品案例索引", "",
        "> 本文件由 `scripts/add_case.py` 生成。检索到匹配案例后，只读取少量相关案例。", "",
        "| ID | 案例 | 目标客户 | 产品形态 | 标签 | 可信度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for record in sorted(records, key=lambda item: str(item["id"])):
        tags = "、".join(str(tag) for tag in record.get("tags", []))
        lines.append(
            f'| [{record["id"]}](cases/{record["id"]}.md) | {record["name"]} | '
            f'{record["target_customer"]} | {record["format"]} | {tags} | {record["confidence"]} |'
        )
    if not records:
        lines.append("| — | 暂无案例 | — | — | — | — |")
    return "\n".join(lines) + "\n"


def rebuild_index(cases_dir: Path, index_path: Path) -> str:
    records = [parse_case(path) for path in iter_case_paths(cases_dir)]
    content = render_index(records)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(content, encoding="utf-8")
    return content
