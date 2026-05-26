"""
文献记录解析与检索模块

负责从 literature_records.csv 加载文献记录，支持按关键词、材料体系、
年份等字段检索。支持从 CSV / TXT / Markdown 文件导入新的文献记录。

字段规范（对应任务书 4.4 / 7.3）：
    id, title, year, source, material_system, method,
    characterization, result_summary, keywords, data_source
"""

import csv
import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path

import pandas as pd

import config
from core import data_loader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 文献记录字段定义
# ---------------------------------------------------------------------------
LITERATURE_COLUMNS = [
    "id", "title", "year", "source", "material_system",
    "method", "characterization", "result_summary", "keywords", "data_source",
]


@dataclass
class LiteratureRecord:
    """单条文献记录。"""
    id: str
    title: str
    year: int | None
    source: str
    material_system: str
    method: str
    characterization: str
    result_summary: str
    keywords: str
    data_source: str = "imported"


_literature_df: pd.DataFrame | None = None


def _ensure_loaded() -> pd.DataFrame:
    """惰性加载文献数据。"""
    global _literature_df
    if _literature_df is None:
        _literature_df = data_loader.get_literature_data()
    return _literature_df


def reload() -> pd.DataFrame:
    """强制重新加载文献数据（用于导入后刷新缓存）。"""
    global _literature_df
    data_loader.invalidate_csv_cache(config.LITERATURE_CSV)
    _literature_df = None
    return _ensure_loaded()


def _next_id(df: pd.DataFrame) -> str:
    """生成下一个文献 ID（L + 三位数字）。"""
    if df.empty or "id" not in df.columns:
        return "L001"
    nums = []
    for raw in df["id"]:
        m = re.search(r"(\d+)", str(raw))
        if m:
            nums.append(int(m.group(1)))
    nxt = max(nums, default=0) + 1
    return f"L{nxt:03d}"


# ---------------------------------------------------------------------------
# 搜索
# ---------------------------------------------------------------------------
def search(query: str, top_k: int | None = None) -> list[LiteratureRecord]:
    """检索与 query 匹配的文献记录。

    在 title, material_system, method, characterization, result_summary,
    keywords 列中进行子串匹配（大小写不敏感）。
    """
    if top_k is None:
        top_k = config.TOP_K

    df = _ensure_loaded()
    if df.empty:
        logger.info("文献数据为空，无法检索。")
        return []

    query_lower = query.lower()
    search_cols = [
        "title", "material_system", "method",
        "characterization", "result_summary", "keywords",
    ]
    mask = pd.Series(False, index=df.index)
    for col in search_cols:
        if col in df.columns:
            mask |= df[col].astype(str).str.lower().str.contains(
                query_lower, regex=False, na=False
            )

    matched = df[mask].head(top_k)
    return _df_to_records(matched)


def search_advanced(
    keyword: str | None = None,
    material: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    source: str | None = None,
    top_k: int | None = None,
) -> list[LiteratureRecord]:
    """高级检索：可按多个条件组合过滤。"""
    if top_k is None:
        top_k = config.TOP_K

    df = _ensure_loaded()
    if df.empty:
        return []

    mask = pd.Series(True, index=df.index)

    if keyword:
        kw = keyword.lower()
        text_mask = pd.Series(False, index=df.index)
        for col in ["title", "material_system", "method",
                     "characterization", "result_summary", "keywords"]:
            if col in df.columns:
                text_mask |= df[col].astype(str).str.lower().str.contains(
                    kw, regex=False, na=False
                )
        mask &= text_mask

    if material and "material_system" in df.columns:
        mask &= df["material_system"].astype(str).str.lower().str.contains(
            material.lower(), regex=False, na=False
        )

    if year_from and "year" in df.columns:
        mask &= pd.to_numeric(df["year"], errors="coerce") >= year_from

    if year_to and "year" in df.columns:
        mask &= pd.to_numeric(df["year"], errors="coerce") <= year_to

    if source and "source" in df.columns:
        mask &= df["source"].astype(str).str.lower().str.contains(
            source.lower(), regex=False, na=False
        )

    return _df_to_records(df[mask].head(top_k))


def get_by_id(record_id: str) -> LiteratureRecord | None:
    """按 ID 精确获取单条文献记录。"""
    df = _ensure_loaded()
    if df.empty or "id" not in df.columns:
        return None
    matches = df[df["id"] == record_id]
    if matches.empty:
        return None
    recs = _df_to_records(matches)
    return recs[0] if recs else None


# ---------------------------------------------------------------------------
# 导入
# ---------------------------------------------------------------------------
def import_from_csv(file_path: str | Path) -> dict:
    """从 CSV 文件导入文献记录。

    CSV 文件必须包含 title 列；其他列可选，缺失列自动补空。
    导入后追加到 literature_records.csv 并刷新缓存。

    Returns:
        {"imported": int, "skipped": int, "errors": list[str]}
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return {"imported": 0, "skipped": 0, "errors": [f"文件不存在: {file_path}"]}

    try:
        incoming = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as exc:
        return {"imported": 0, "skipped": 0, "errors": [f"读取 CSV 失败: {exc}"]}

    if "title" not in incoming.columns:
        return {"imported": 0, "skipped": 0, "errors": ["CSV 缺少 title 列"]}

    return _merge_records(incoming, source_label=f"csv:{file_path.name}")


def import_from_txt(file_path: str | Path) -> dict:
    """从 TXT 文件导入文献记录。

    TXT 格式：每行一条记录，字段以制表符分隔：
        title<TAB>year<TAB>source<TAB>material_system<TAB>keywords

    或：每行一条记录，仅 title（其他字段留空）。

    Returns:
        {"imported": int, "skipped": int, "errors": list[str]}
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return {"imported": 0, "skipped": 0, "errors": [f"文件不存在: {file_path}"]}

    rows = []
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) == 1:
                    rows.append({"title": parts[0].strip()})
                elif len(parts) >= 2:
                    rows.append({
                        "title": parts[0].strip(),
                        "year": parts[1].strip() if len(parts) > 1 else "",
                        "source": parts[2].strip() if len(parts) > 2 else "",
                        "material_system": parts[3].strip() if len(parts) > 3 else "",
                        "keywords": parts[4].strip() if len(parts) > 4 else "",
                    })
                else:
                    errors.append(f"行 {lineno}: 格式异常")
    except Exception as exc:
        return {"imported": 0, "skipped": 0, "errors": [f"读取 TXT 失败: {exc}"]}

    if not rows:
        return {"imported": 0, "skipped": 0, "errors": errors or ["文件为空或无有效记录"]}

    incoming = pd.DataFrame(rows)
    result = _merge_records(incoming, source_label=f"txt:{file_path.name}")
    result["errors"].extend(errors)
    return result


def import_from_markdown(file_path: str | Path) -> dict:
    """从 Markdown 文件导入文献记录。

    支持两种格式：

    1. 表格格式（Markdown Table）：
        | title | year | source | material_system | keywords |
        |-------|------|--------|-----------------|----------|
        | ...   | ...  | ...    | ...             | ...      |

    2. 列表格式（每条以 - 或 * 开头）：
        - **Title**: Some Paper Title
          - Year: 2023
          - Material: PNIPAM hydrogel

    Returns:
        {"imported": int, "skipped": int, "errors": list[str]}
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return {"imported": 0, "skipped": 0, "errors": [f"文件不存在: {file_path}"]}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        return {"imported": 0, "skipped": 0, "errors": [f"读取 Markdown 失败: {exc}"]}

    # 尝试表格格式
    rows = _parse_markdown_table(content)
    if rows:
        incoming = pd.DataFrame(rows)
        return _merge_records(incoming, source_label=f"md:{file_path.name}")

    # 尝试列表格式
    rows = _parse_markdown_list(content)
    if rows:
        incoming = pd.DataFrame(rows)
        return _merge_records(incoming, source_label=f"md:{file_path.name}")

    return {"imported": 0, "skipped": 0, "errors": ["无法从 Markdown 中解析出文献记录"]}


def _parse_markdown_table(content: str) -> list[dict]:
    """解析 Markdown 表格格式的文献记录。"""
    lines = content.strip().splitlines()
    table_lines = [l.strip() for l in lines if "|" in l]
    if len(table_lines) < 3:
        return []

    # 找到表头
    header_line = table_lines[0]
    headers = [h.strip().lower() for h in header_line.split("|") if h.strip()]

    # 跳过分隔线
    rows = []
    for line in table_lines[2:]:
        cells = [c.strip() for c in line.split("|") if c.strip() != ""]
        # 如果用 | 分割后数量和表头一致
        if len(cells) < len(headers):
            # 尝试带首尾空元素的分割
            all_cells = line.split("|")
            cells = [c.strip() for c in all_cells[1:-1]]  # 去掉首尾空
        if len(cells) >= len(headers):
            row = {}
            for i, h in enumerate(headers):
                if i < len(cells):
                    row[h] = cells[i]
            if "title" in row or "标题" in row:
                mapped = {}
                title = row.get("title") or row.get("标题", "")
                mapped["title"] = title
                mapped["year"] = row.get("year", row.get("年份", ""))
                mapped["source"] = row.get("source", row.get("来源", ""))
                mapped["material_system"] = row.get(
                    "material_system", row.get("材料体系", row.get("材料", ""))
                )
                mapped["method"] = row.get("method", row.get("实验方法", ""))
                mapped["characterization"] = row.get(
                    "characterization", row.get("表征方式", row.get("表征", ""))
                )
                mapped["result_summary"] = row.get(
                    "result_summary", row.get("结果摘要", row.get("结果", ""))
                )
                mapped["keywords"] = row.get("keywords", row.get("关键词", ""))
                if mapped["title"]:
                    rows.append(mapped)
    return rows


def _parse_markdown_list(content: str) -> list[dict]:
    """解析 Markdown 列表格式的文献记录。"""
    rows = []
    current: dict | None = None
    field_map = {
        "title": "title", "标题": "title",
        "year": "year", "年份": "year",
        "source": "source", "来源": "source",
        "material": "material_system", "材料": "material_system",
        "material_system": "material_system", "材料体系": "material_system",
        "method": "method", "实验方法": "method",
        "characterization": "characterization", "表征": "characterization",
        "result": "result_summary", "结果": "result_summary",
        "keywords": "keywords", "关键词": "keywords",
    }

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        # 顶层列表项
        if re.match(r"^[-*+]\s+", line):
            text = re.sub(r"^[-*+]\s+", "", line)
            # 去掉 Markdown 加粗
            text_clean = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
            if current is not None and current.get("title"):
                rows.append(current)
            current = {"title": text_clean}
        elif current is not None:
            # 子列表项
            m = re.match(r"^\s+[-*+]\s*\*?\*?(.+?)\*?\*?\s*[:：]\s*(.+)", line)
            if m:
                key_raw = m.group(1).strip().lower()
                val = m.group(2).strip()
                for pat, field in field_map.items():
                    if pat in key_raw:
                        current[field] = val
                        break

    if current and current.get("title"):
        rows.append(current)
    return rows


def _merge_records(incoming: pd.DataFrame, source_label: str) -> dict:
    """将新记录合并到 literature_records.csv。"""
    errors = []
    imported = 0
    skipped = 0

    df = _ensure_loaded().copy()

    for col in LITERATURE_COLUMNS:
        if col not in incoming.columns:
            incoming[col] = ""
        if col not in df.columns:
            df[col] = ""

    for _, row in incoming.iterrows():
        title = str(row.get("title", "")).strip()
        if not title or title == "nan":
            skipped += 1
            continue

        # 去重：标题完全一致则跳过
        if not df.empty and "title" in df.columns:
            if (df["title"].astype(str).str.strip() == title).any():
                skipped += 1
                continue

        new_id = _next_id(df)
        new_row = {}
        for col in LITERATURE_COLUMNS:
            if col == "id":
                new_row[col] = new_id
            elif col == "data_source":
                new_row[col] = source_label
            elif col in incoming.columns:
                val = row.get(col, "")
                new_row[col] = str(val) if pd.notna(val) else ""
            else:
                new_row[col] = ""
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        imported += 1

    if imported > 0:
        try:
            df.to_csv(config.LITERATURE_CSV, index=False, encoding="utf-8-sig")
            global _literature_df
            _literature_df = df
            data_loader.invalidate_csv_cache(config.LITERATURE_CSV)
            logger.info("成功导入 %d 条文献记录（跳过 %d 条）", imported, skipped)
        except Exception as exc:
            errors.append(f"保存 CSV 失败: {exc}")

    return {"imported": imported, "skipped": skipped, "errors": errors}


# ---------------------------------------------------------------------------
# 统计
# ---------------------------------------------------------------------------
def get_stats() -> dict:
    """返回文献数据统计（真实数量，不含虚构成分）。"""
    df = _ensure_loaded()
    total = len(df)
    by_source: dict[str, int] = {}
    if "data_source" in df.columns and total > 0:
        by_source = df["data_source"].value_counts().to_dict()
    by_year: dict[str, int] = {}
    if "year" in df.columns and total > 0:
        year_series = pd.to_numeric(df["year"], errors="coerce")
        by_year = year_series.dropna().astype(int).value_counts().sort_index().to_dict()
        by_year = {str(k): v for k, v in by_year.items()}
    return {
        "total": total,
        "columns": list(df.columns) if not df.empty else [],
        "by_data_source": by_source,
        "by_year": by_year,
    }


def get_all_records() -> list[LiteratureRecord]:
    """返回所有文献记录。"""
    df = _ensure_loaded()
    return _df_to_records(df)


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------
def _df_to_records(df: pd.DataFrame) -> list[LiteratureRecord]:
    """将 DataFrame 转为 LiteratureRecord 列表。"""
    records = []
    for _, row in df.iterrows():
        try:
            year_val = row.get("year")
            if pd.isna(year_val) or str(year_val).strip() in ("", "nan"):
                year_int = None
            else:
                year_int = int(float(year_val))
        except (ValueError, TypeError):
            year_int = None
        records.append(LiteratureRecord(
            id=str(row.get("id", "")),
            title=str(row.get("title", "")),
            year=year_int,
            source=str(row.get("source", "")),
            material_system=str(row.get("material_system", "")),
            method=str(row.get("method", "")),
            characterization=str(row.get("characterization", "")),
            result_summary=str(row.get("result_summary", "")),
            keywords=str(row.get("keywords", "")),
            data_source=str(row.get("data_source", "unknown")),
        ))
    return records
