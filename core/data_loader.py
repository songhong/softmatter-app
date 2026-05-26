"""
数据加载与管理模块

负责加载和管理 CSV / JSON 数据文件，提供统一的数据访问接口。
内置简单内存缓存，避免 Streamlit 重复运行时反复读磁盘。
"""

import json
import logging
import time
from pathlib import Path

import pandas as pd

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 简单内存缓存（避免 Streamlit 频繁 rerun 时重复读磁盘）
# ---------------------------------------------------------------------------
_csv_cache: dict[str, tuple[float, pd.DataFrame]] = {}
_CACHE_TTL_SECONDS = 30


def _get_cached_csv(file_path: Path) -> pd.DataFrame | None:
    """从缓存中获取 CSV DataFrame，过期返回 None。"""
    key = str(file_path)
    if key in _csv_cache:
        ts, df = _csv_cache[key]
        if time.time() - ts < _CACHE_TTL_SECONDS:
            return df
    return None


def _set_cached_csv(file_path: Path, df: pd.DataFrame) -> None:
    """将 DataFrame 写入缓存。"""
    _csv_cache[str(file_path)] = (time.time(), df)


def invalidate_csv_cache(file_path: Path | None = None) -> None:
    """使缓存失效。file_path 为 None 时清空全部缓存。"""
    if file_path is None:
        _csv_cache.clear()
    else:
        _csv_cache.pop(str(file_path), None)


def load_csv(file_path: Path, required_columns: list[str] | None = None) -> pd.DataFrame:
    """加载 CSV 文件并返回 DataFrame。

    Args:
        file_path: CSV 文件路径。
        required_columns: 必须包含的列名列表，缺失时记录警告。

    Returns:
        包含数据的 DataFrame；文件不存在时返回空 DataFrame。
    """
    cached = _get_cached_csv(file_path)
    if cached is not None:
        return cached

    if not file_path.exists():
        logger.warning("数据文件不存在: %s", file_path)
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
    except Exception as exc:
        logger.error("读取 CSV 失败: %s - %s", file_path, exc)
        return pd.DataFrame()

    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            logger.warning("CSV %s 缺失列: %s", file_path, missing)

    _set_cached_csv(file_path, df)
    return df


def load_json(file_path: Path) -> dict:
    """加载 JSON 文件并返回字典。"""
    if not file_path.exists():
        logger.warning("配置文件不存在: %s", file_path)
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error("读取 JSON 失败: %s - %s", file_path, exc)
        return {}


def save_json(file_path: Path, data: dict) -> bool:
    """将字典保存到 JSON 文件。"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as exc:
        logger.error("保存 JSON 失败: %s - %s", file_path, exc)
        return False


def get_knowledge_data() -> pd.DataFrame:
    """加载课程知识库数据。"""
    return load_csv(config.KNOWLEDGE_CSV)


def get_literature_data() -> pd.DataFrame:
    """加载文献记录数据。"""
    return load_csv(config.LITERATURE_CSV)


def get_recipes_data() -> pd.DataFrame:
    """加载实验配方数据。"""
    return load_csv(config.RECIPES_CSV)


def get_feedback_data() -> pd.DataFrame:
    """加载反馈数据。"""
    return load_csv(config.FEEDBACK_CSV)


def get_qa_history() -> pd.DataFrame:
    """加载问答历史数据。"""
    return load_csv(config.QA_HISTORY_CSV)
