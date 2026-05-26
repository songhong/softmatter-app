"""
课程知识库检索模块

基于 TF-IDF 和轻量词面重合度实现语义检索，从 softmatter_knowledge.csv、
literature_records.csv、experiment_recipes.csv 中返回最相关的知识条目。
当 sentence-transformers 可用时可升级为 embedding 检索，但当前默认使用轻量本地检索。
"""

import logging
import re
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import config
from core import data_loader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 检索结果数据结构
# ---------------------------------------------------------------------------


@dataclass
class RetrievalResult:
    """单条检索结果。"""
    id: str
    title: str
    category: str
    content: str
    source: str
    score: float
    data_type: str = "knowledge"  # knowledge / literature / recipe


@dataclass
class RetrievalBundle:
    """一次检索返回的完整结果包。"""
    query: str
    results: list[RetrievalResult] = field(default_factory=list)
    total_candidates: int = 0
    has_sufficient_evidence: bool = True
    evidence_gap_message: str = ""

    @property
    def top_scores(self) -> list[float]:
        return [r.score for r in self.results]

    def summary_text(self) -> str:
        """生成检索摘要文本，供 prompt 注入。"""
        if not self.results:
            return "未检索到相关证据。"
        lines = []
        for i, r in enumerate(self.results, 1):
            lines.append(
                f"证据{i} [{r.data_type}] (相似度 {r.score:.2f}): "
                f"{r.title} - {r.content[:200]}"
            )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 内部索引缓存
# ---------------------------------------------------------------------------


@dataclass
class _TfIdfIndex:
    """一个数据源的 TF-IDF 索引。"""
    vectorizer: TfidfVectorizer
    tfidf_matrix: np.ndarray
    texts: list[str]
    df: pd.DataFrame


# 各数据源的索引缓存
_knowledge_index: _TfIdfIndex | None = None
_literature_index: _TfIdfIndex | None = None
_recipe_index: _TfIdfIndex | None = None

_TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9'\-]*|\d+(?:\.\d+)?|[一-鿿]{2,}")
_ALIAS_GROUPS = [
    ("CMC", "临界胶束浓度", "胶束浓度"),
    ("G'", "储能模量", "弹性模量"),
    ("G''", "损耗模量", "粘性模量", "黏性模量"),
    ("流变", "流变仪", "流变测量", "粘弹性", "黏弹性"),
    ("水凝胶", "凝胶", "hydrogel"),
    ("胶束", "micelle", "micellar"),
    ("DLS", "动态光散射", "粒径"),
]


def _normalize_text(text: str) -> str:
    """标准化检索文本，补齐中英文/缩写别名，改善中文短查询召回。"""
    normalized = (text or "").strip()
    additions: list[str] = []
    for aliases in _ALIAS_GROUPS:
        if any(alias.lower() in normalized.lower() for alias in aliases):
            additions.extend(aliases)
    if additions:
        normalized = f"{normalized} {' '.join(dict.fromkeys(additions))}"
    return normalized


def _extract_tokens(text: str) -> set[str]:
    """抽取中英文关键词 token；中文连续词作为短查询词面召回信号。"""
    normalized = _normalize_text(text).lower()
    tokens = {m.group(0) for m in _TOKEN_PATTERN.finditer(normalized)}
    # 对中文长串补充二字滑窗，兼容 CSV 中未分词的术语片段。
    for token in list(tokens):
        if re.fullmatch(r"[一-鿿]{3,}", token):
            tokens.update(token[i:i + 2] for i in range(len(token) - 1))
    return {t for t in tokens if t.strip()}


def _lexical_overlap_score(query: str, text: str) -> float:
    """计算轻量词面重合度，作为 TF-IDF 分数的召回补充。"""
    query_tokens = _extract_tokens(query)
    if not query_tokens:
        return 0.0
    text_lower = _normalize_text(text).lower()
    matched = [token for token in query_tokens if token in text_lower]
    return len(matched) / len(query_tokens)


def _build_index(df: pd.DataFrame, text_columns: list[str]) -> _TfIdfIndex | None:
    """为 DataFrame 构建 TF-IDF 索引。

    Args:
        df: 数据 DataFrame。
        text_columns: 用于构建检索文本的列名列表。

    Returns:
        _TfIdfIndex 对象；数据为空时返回 None。
    """
    if df.empty:
        return None

    # 拼接文本列作为检索语料
    texts: list[str] = []
    for _, row in df.iterrows():
        parts = []
        for col in text_columns:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                parts.append(str(val).strip())
        texts.append(_normalize_text(" ".join(parts)))

    if not any(texts):
        return None

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        max_features=10000,
        ngram_range=(2, 4),
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    return _TfIdfIndex(
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        texts=texts,
        df=df,
    )


def _ensure_knowledge_index() -> _TfIdfIndex | None:
    global _knowledge_index
    if _knowledge_index is None:
        df = data_loader.get_knowledge_data()
        _knowledge_index = _build_index(df, ["title", "category", "content", "keywords"])
    return _knowledge_index


def _ensure_literature_index() -> _TfIdfIndex | None:
    global _literature_index
    if _literature_index is None:
        df = data_loader.get_literature_data()
        _literature_index = _build_index(
            df,
            ["title", "material_system", "method", "characterization", "result_summary", "keywords"],
        )
    return _literature_index


def _ensure_recipe_index() -> _TfIdfIndex | None:
    global _recipe_index
    if _recipe_index is None:
        df = data_loader.get_recipes_data()
        _recipe_index = _build_index(
            df,
            ["material", "concentration", "process", "characterization", "result"],
        )
    return _recipe_index


def _search_index(
    index: _TfIdfIndex | None,
    query: str,
    top_k: int,
    data_type: str,
    id_field: str = "id",
    title_field: str = "title",
    category_field: str = "category",
    content_fields: list[str] | None = None,
    source_field: str = "source",
) -> list[RetrievalResult]:
    """在指定索引上执行 TF-IDF 检索。"""
    if index is None:
        return []

    query_vec = index.vectorizer.transform([_normalize_text(query)])
    tfidf_scores = cosine_similarity(query_vec, index.tfidf_matrix).flatten()
    lexical_scores = np.array([
        _lexical_overlap_score(query, text) for text in index.texts
    ])
    scores = np.maximum(tfidf_scores, lexical_scores)

    # 取 Top-K（按分数降序）
    top_indices = scores.argsort()[::-1][:top_k]

    results: list[RetrievalResult] = []
    for idx in top_indices:
        score = float(scores[idx])
        if score < config.SIMILARITY_THRESHOLD:
            continue
        row = index.df.iloc[idx]

        # 组装 content 字段
        if content_fields:
            content_parts = []
            for cf in content_fields:
                val = row.get(cf, "")
                if pd.notna(val) and str(val).strip():
                    content_parts.append(str(val).strip())
            content = "；".join(content_parts) if content_parts else ""
        else:
            content = str(row.get("content", ""))

        results.append(RetrievalResult(
            id=str(row.get(id_field, f"U{idx}")),
            title=str(row.get(title_field, "")),
            category=str(row.get(category_field, data_type)),
            content=content[:500],
            source=str(row.get(source_field, "")),
            score=round(score, 4),
            data_type=data_type,
        ))

    return results


# ---------------------------------------------------------------------------
# 公开接口
# ---------------------------------------------------------------------------


def search(query: str, top_k: int | None = None) -> list[RetrievalResult]:
    """从课程知识库检索与 query 最相关的条目。

    Args:
        query: 用户查询文本。
        top_k: 返回结果数量上限，默认使用 config.TOP_K。

    Returns:
        按相关性排序的 RetrievalResult 列表。
    """
    if top_k is None:
        top_k = config.TOP_K

    index = _ensure_knowledge_index()
    return _search_index(
        index, query, top_k,
        data_type="knowledge",
        title_field="title",
        category_field="category",
        content_fields=["title", "category", "content"],
        source_field="source",
    )


def search_literature(query: str, top_k: int | None = None) -> list[RetrievalResult]:
    """从文献记录中检索相关条目。"""
    if top_k is None:
        top_k = config.TOP_K

    index = _ensure_literature_index()
    return _search_index(
        index, query, top_k,
        data_type="literature",
        title_field="title",
        category_field="material_system",
        content_fields=["title", "material_system", "method", "characterization", "result_summary"],
        source_field="source",
    )


def search_recipes(query: str, top_k: int | None = None) -> list[RetrievalResult]:
    """从实验配方中检索相关条目。"""
    if top_k is None:
        top_k = config.TOP_K

    index = _ensure_recipe_index()
    return _search_index(
        index, query, top_k,
        data_type="recipe",
        title_field="material",
        category_field="safety_level",
        content_fields=["material", "concentration", "process", "characterization", "result"],
        source_field="source",
    )


def search_all(query: str, top_k: int | None = None) -> RetrievalBundle:
    """跨知识库、文献和配方统一检索，返回合并后的 Top-K 结果。

    同时计算证据充分性：若最高分低于阈值或结果数不足，标记为证据不足。
    """
    if top_k is None:
        top_k = config.TOP_K

    knowledge_results = search(query, top_k)
    literature_results = search_literature(query, top_k)
    recipe_results = search_recipes(query, top_k)

    # 合并并按 score 排序
    all_results = knowledge_results + literature_results + recipe_results
    all_results.sort(key=lambda r: r.score, reverse=True)
    merged = all_results[:top_k]

    bundle = RetrievalBundle(
        query=query,
        results=merged,
        total_candidates=len(knowledge_results) + len(literature_results) + len(recipe_results),
    )

    # 证据充分性判断
    if not merged:
        bundle.has_sufficient_evidence = False
        bundle.evidence_gap_message = "当前知识库中未找到与该问题相关的证据，以下回答为推测性内容，仅供参考。"
    elif merged[0].score < config.SIMILARITY_THRESHOLD:
        bundle.has_sufficient_evidence = False
        bundle.evidence_gap_message = (
            f"检索到的最相关证据相似度仅为 {merged[0].score:.2f}，"
            "低于可靠阈值，以下回答可能不够准确，建议结合教材核实。"
        )

    return bundle


def get_stats() -> dict:
    """返回各数据源的统计信息。"""
    knowledge_df = data_loader.get_knowledge_data()
    literature_df = data_loader.get_literature_data()
    recipes_df = data_loader.get_recipes_data()
    return {
        "knowledge": {
            "total": len(knowledge_df),
            "columns": list(knowledge_df.columns) if not knowledge_df.empty else [],
        },
        "literature": {
            "total": len(literature_df),
            "columns": list(literature_df.columns) if not literature_df.empty else [],
        },
        "recipes": {
            "total": len(recipes_df),
            "columns": list(recipes_df.columns) if not recipes_df.empty else [],
        },
    }


def invalidate_cache() -> None:
    """清除所有检索索引缓存，在数据更新后调用。"""
    global _knowledge_index, _literature_index, _recipe_index
    _knowledge_index = None
    _literature_index = None
    _recipe_index = None
    data_loader.invalidate_csv_cache()
    logger.info("检索索引缓存已清除。")
