"""
实验配方字段抽取与检索模块

负责加载 experiment_recipes.csv，支持按材料体系、工艺类型检索。
提供从自由文本中抽取结构化配方字段的功能。

字段规范（对应任务书 4.5 / 7.3）：
    id, material, concentration, process, temperature, time,
    characterization, result, safety_level, source, is_example
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

import config
from core import data_loader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 配方记录字段定义
# ---------------------------------------------------------------------------
RECIPE_COLUMNS = [
    "id", "material", "concentration", "process", "temperature",
    "time", "characterization", "result", "safety_level", "source", "is_example",
]

# 安全等级关键词映射
_SAFETY_KEYWORDS = {
    "high": [
        "浓硫酸", "浓硝酸", "氢氟酸", "强酸", "强碱", "剧毒",
        "致癌", "易燃易爆", "液氮", "高压", "真空",
        "KMnO4", "H2SO4", "HF", "NaN3",
    ],
    "medium": [
        "有机溶剂", "氯仿", "丙酮", "DMF", "DMSO", "DCM",
        "甲苯", "乙醚", "引发剂", "交联剂", "KPS", "APS",
        "过硫酸", "光引发", "紫外",
    ],
}


@dataclass
class Recipe:
    """单条实验配方记录。"""
    id: str
    material: str
    concentration: str
    process: str
    temperature: str
    time: str
    characterization: str
    result: str
    safety_level: str
    source: str
    is_example: bool = True


_recipes_df: pd.DataFrame | None = None


def _ensure_loaded() -> pd.DataFrame:
    """惰性加载配方数据。"""
    global _recipes_df
    if _recipes_df is None:
        _recipes_df = data_loader.get_recipes_data()
    return _recipes_df


def reload() -> pd.DataFrame:
    """强制重新加载配方数据。"""
    global _recipes_df
    data_loader.invalidate_csv_cache(config.RECIPES_CSV)
    _recipes_df = None
    return _ensure_loaded()


def _next_id(df: pd.DataFrame) -> str:
    """生成下一个配方 ID（R + 三位数字）。"""
    if df.empty or "id" not in df.columns:
        return "R001"
    nums = []
    for raw in df["id"]:
        m = re.search(r"(\d+)", str(raw))
        if m:
            nums.append(int(m.group(1)))
    nxt = max(nums, default=0) + 1
    return f"R{nxt:03d}"


# ---------------------------------------------------------------------------
# 搜索
# ---------------------------------------------------------------------------
def search(query: str, top_k: int | None = None) -> list[Recipe]:
    """检索与 query 匹配的实验配方。

    在 material, process, characterization, result 列中进行子串匹配。
    """
    if top_k is None:
        top_k = config.TOP_K

    df = _ensure_loaded()
    if df.empty:
        logger.info("配方数据为空，无法检索。")
        return []

    query_lower = query.lower()
    search_cols = ["material", "concentration", "process",
                   "characterization", "result"]
    mask = pd.Series(False, index=df.index)
    for col in search_cols:
        if col in df.columns:
            mask |= df[col].astype(str).str.lower().str.contains(
                query_lower, regex=False, na=False
            )

    matched = df[mask].head(top_k)
    return _df_to_recipes(matched)


def search_by_material(material: str, top_k: int | None = None) -> list[Recipe]:
    """按材料名称精确/模糊检索。"""
    if top_k is None:
        top_k = config.TOP_K
    df = _ensure_loaded()
    if df.empty or "material" not in df.columns:
        return []
    mask = df["material"].astype(str).str.lower().str.contains(
        material.lower(), regex=False, na=False
    )
    return _df_to_recipes(df[mask].head(top_k))


def search_by_safety(level: str, top_k: int | None = None) -> list[Recipe]:
    """按安全等级检索（low / medium / high）。"""
    if top_k is None:
        top_k = config.TOP_K
    df = _ensure_loaded()
    if df.empty or "safety_level" not in df.columns:
        return []
    mask = df["safety_level"].astype(str).str.lower() == level.lower()
    return _df_to_recipes(df[mask].head(top_k))


def get_by_id(recipe_id: str) -> Recipe | None:
    """按 ID 精确获取单条配方。"""
    df = _ensure_loaded()
    if df.empty or "id" not in df.columns:
        return None
    matches = df[df["id"] == recipe_id]
    if matches.empty:
        return None
    recs = _df_to_recipes(matches)
    return recs[0] if recs else None


def get_all_recipes() -> list[Recipe]:
    """返回所有配方记录。"""
    df = _ensure_loaded()
    return _df_to_recipes(df)


# ---------------------------------------------------------------------------
# 文本配方抽取
# ---------------------------------------------------------------------------
def extract_recipe_from_text(text: str) -> dict:
    """从自由文本中抽取结构化配方字段。

    使用正则模式匹配常见格式，不依赖 LLM。
    返回一个包含所有配方字段的字典（缺失字段为空字符串）。

    Args:
        text: 实验描述文本，可以包含多行。

    Returns:
        结构化配方字典，键对应 RECIPE_COLUMNS（除 id, is_example）。
    """
    result = {
        "material": "",
        "concentration": "",
        "process": "",
        "temperature": "",
        "time": "",
        "characterization": "",
        "result": "",
        "safety_level": "low",
        "source": "text_extraction",
    }

    if not text or not text.strip():
        return result

    lines = text.strip().splitlines()

    # 逐行解析 key: value 或 key：value 格式
    field_patterns = {
        "material": [r"(?:材料|material|材料体系)\s*[:：]\s*(.+)"],
        "concentration": [r"(?:浓度|比例|concentration|配比)\s*[:：]\s*(.+)"],
        "process": [r"(?:工艺|制备|process|方法|合成)\s*[:：]\s*(.+)"],
        "temperature": [r"(?:温度|temperature)\s*[:：]\s*(.+)"],
        "time": [r"(?:时间|time|反应时间)\s*[:：]\s*(.+)"],
        "characterization": [r"(?:表征|characterization|测试|表征方法)\s*[:：]\s*(.+)"],
        "result": [r"(?:结果|result|效果|主要结果)\s*[:：]\s*(.+)"],
    }

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        for field, patterns in field_patterns.items():
            for pat in patterns:
                m = re.search(pat, line_s, re.IGNORECASE)
                if m:
                    result[field] = m.group(1).strip()

    # 若未匹配到结构化格式，尝试整体作为 material
    if not any(result[f] for f in ["material", "concentration", "process"]):
        result["material"] = text.strip()[:200]

    # 自动推断安全等级
    result["safety_level"] = infer_safety_level(
        text + " " + result.get("material", "") + " " + result.get("process", "")
    )

    return result


def infer_safety_level(text: str) -> str:
    """根据文本中的关键词推断安全等级。

    Returns:
        "high", "medium", 或 "low"
    """
    text_lower = text.lower()
    for kw in _SAFETY_KEYWORDS["high"]:
        if kw.lower() in text_lower:
            return "high"
    for kw in _SAFETY_KEYWORDS["medium"]:
        if kw.lower() in text_lower:
            return "medium"
    return "low"


def add_recipe(recipe_dict: dict, mark_as_example: bool = True) -> str | None:
    """将抽取的配方添加到 experiment_recipes.csv。

    Args:
        recipe_dict: 包含配方字段的字典。
        mark_as_example: 是否标记为教学示例。

    Returns:
        新配方 ID，失败返回 None。
    """
    df = _ensure_loaded().copy()
    new_id = _next_id(df)

    new_row = {"id": new_id, "is_example": str(mark_as_example).lower()}
    for col in RECIPE_COLUMNS:
        if col in ("id", "is_example"):
            continue
        new_row[col] = str(recipe_dict.get(col, ""))

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    try:
        df.to_csv(config.RECIPES_CSV, index=False, encoding="utf-8-sig")
        global _recipes_df
        _recipes_df = df
        data_loader.invalidate_csv_cache(config.RECIPES_CSV)
        logger.info("添加配方 %s 成功", new_id)
        return new_id
    except Exception as exc:
        logger.error("保存配方 CSV 失败: %s", exc)
        return None


# ---------------------------------------------------------------------------
# 统计
# ---------------------------------------------------------------------------
def get_stats() -> dict:
    """返回配方数据统计（真实数量）。"""
    df = _ensure_loaded()
    total = len(df)
    by_safety: dict[str, int] = {}
    if "safety_level" in df.columns and total > 0:
        by_safety = df["safety_level"].value_counts().to_dict()
    example_count = 0
    non_example_count = 0
    if "is_example" in df.columns and total > 0:
        example_count = int(
            df["is_example"].astype(str).str.lower().isin(["true", "1", "yes"]).sum()
        )
        non_example_count = total - example_count
    return {
        "total": total,
        "by_safety_level": by_safety,
        "example_count": example_count,
        "non_example_count": non_example_count,
        "columns": list(df.columns) if not df.empty else [],
    }


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------
def _df_to_recipes(df: pd.DataFrame) -> list[Recipe]:
    """将 DataFrame 转为 Recipe 列表。"""
    recipes = []
    for _, row in df.iterrows():
        is_ex = str(row.get("is_example", "true")).lower() in ("true", "1", "yes")
        recipes.append(Recipe(
            id=str(row.get("id", "")),
            material=str(row.get("material", "")),
            concentration=str(row.get("concentration", "")),
            process=str(row.get("process", "")),
            temperature=str(row.get("temperature", "")),
            time=str(row.get("time", "")),
            characterization=str(row.get("characterization", "")),
            result=str(row.get("result", "")),
            safety_level=str(row.get("safety_level", "low")),
            source=str(row.get("source", "")),
            is_example=is_ex,
        ))
    return recipes
