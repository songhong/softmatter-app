"""
教师统计分析模块

提供问答历史和反馈数据的统计分析功能，
支撑教师分析面板的数据展示。
所有统计均基于真实日志 / 反馈数据，不编造任何指标。
"""

import logging
from collections import Counter

import pandas as pd

from core import data_loader, qa_logger

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 问题分类关键词映射
# ---------------------------------------------------------------------------
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "流变学": ["流变", "粘度", "剪切", "触变", "粘弹性", "模量", "蠕变", "应力", "应变", "屈服"],
    "胶体科学": ["胶体", "DLVO", "Zeta", "电位", "双电层", "聚沉", "絮凝", "稳定", "分散"],
    "水凝胶": ["水凝胶", "凝胶", "交联", "溶胀", "溶胶"],
    "高分子科学": ["高分子", "聚合物", "共聚物", "嵌段", "聚合", "分子量", "链段", "单体"],
    "乳液": ["乳液", "乳化", "Pickering", "液滴", "破乳"],
    "智能材料": ["智能", "响应", "形状记忆", "LCST", "UCST", "相变"],
    "表征方法": ["表征", "AFM", "SEM", "TEM", "DSC", "TGA", "光谱", "散射", "衍射"],
    "表面活性剂": ["表面活性剂", "胶束", "CMC", "亲水", "疏水", "HLB"],
    "自组装": ["自组装", "超分子", "氢键", "主客体", "自组织"],
    "界面科学": ["界面", "表面张力", "接触角", "润湿", "吸附", "表面能"],
    "药物递送": ["药物", "递送", "缓释", "控释", "靶向", "载药"],
}


# ---------------------------------------------------------------------------
# 基础查询
# ---------------------------------------------------------------------------

def get_recent_questions(n: int = 20) -> list[dict]:
    """获取最近 n 条提问记录。"""
    df = data_loader.get_qa_history()
    if df.empty:
        return []
    recent = df.tail(n).to_dict(orient="records")
    return list(reversed(recent))


def get_question_count() -> int:
    """返回提问记录总数（避免加载全部记录）。"""
    df = data_loader.get_qa_history()
    return len(df)


def get_feedback_count() -> int:
    """返回反馈记录总数。"""
    df = data_loader.get_feedback_data()
    return len(df)


# ---------------------------------------------------------------------------
# 关键词分析
# ---------------------------------------------------------------------------

def get_keyword_frequency(top_n: int = 15) -> list[dict]:
    """统计高频关键词。

    使用 qa_logger.extract_keywords 做领域术语 + 正则分词的混合提取，
    无需外部中文分词库。
    """
    df = data_loader.get_qa_history()
    if df.empty or "question" not in df.columns:
        return []

    texts = df["question"].dropna().tolist()
    return qa_logger.extract_keywords(texts, top_n=top_n)


# ---------------------------------------------------------------------------
# 反馈分析
# ---------------------------------------------------------------------------

def get_feedback_distribution() -> dict:
    """获取反馈评分分布。

    评分映射：4-5 满意，3 中性，1-2 不满意。
    """
    df = data_loader.get_feedback_data()
    if df.empty or "rating" not in df.columns:
        return {"positive": 0, "neutral": 0, "negative": 0, "total": 0,
                "satisfaction_rate": 0.0, "ratings": []}

    ratings = df["rating"].dropna().astype(int).tolist()
    positive = sum(1 for r in ratings if r >= 4)
    neutral = sum(1 for r in ratings if 2 <= r < 4)
    negative = sum(1 for r in ratings if r < 2)
    total = len(ratings)
    return {
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "total": total,
        "satisfaction_rate": round(positive / total * 100, 1) if total > 0 else 0.0,
        "ratings": ratings,
    }


# ---------------------------------------------------------------------------
# 趋势分析
# ---------------------------------------------------------------------------

def get_daily_question_counts() -> list[dict]:
    """获取每日提问次数趋势。"""
    df = data_loader.get_qa_history()
    if df.empty or "timestamp" not in df.columns:
        return []

    df = df.copy()
    df["date"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.date.astype(str)
    daily = df.groupby("date").size().reset_index(name="count")
    return daily.to_dict(orient="records")


# ---------------------------------------------------------------------------
# 风险分析
# ---------------------------------------------------------------------------

def get_high_risk_stats() -> dict:
    """统计高风险实验方案数量。"""
    df = data_loader.get_qa_history()
    if df.empty or "risk_level" not in df.columns:
        return {"high_risk_count": 0, "total": 0}

    high_risk = int((df["risk_level"] == "高").sum())
    return {"high_risk_count": high_risk, "total": len(df)}


def get_evidence_insufficient_count() -> int:
    """统计证据不足的提问数量（evidence_count == 0 或 confidence == '低'）。"""
    df = data_loader.get_qa_history()
    if df.empty:
        return 0

    count = 0
    if "evidence_count" in df.columns:
        count += int((df["evidence_count"].fillna(0) == 0).sum())
    elif "confidence" in df.columns:
        count += int((df["confidence"] == "低").sum())
    return count


# ---------------------------------------------------------------------------
# 问题分类统计
# ---------------------------------------------------------------------------

def classify_question(question: str) -> str:
    """基于关键词匹配对单个问题分类。"""
    if not question:
        return "其他"
    q = str(question)
    scores: dict[str, int] = {}
    for category, keywords in _CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > 0:
            scores[category] = score
    if not scores:
        return "其他"
    return max(scores, key=scores.get)


def get_category_stats() -> list[dict]:
    """统计各问题分类的提问次数。"""
    df = data_loader.get_qa_history()
    if df.empty or "question" not in df.columns:
        return []

    categories = df["question"].apply(classify_question)
    counter = Counter(categories)
    total = sum(counter.values())
    result = []
    for cat, count in counter.most_common():
        result.append({
            "category": cat,
            "count": count,
            "percentage": round(count / total * 100, 1) if total > 0 else 0,
        })
    return result


# ---------------------------------------------------------------------------
# 薄弱点总结（规则化）
# ---------------------------------------------------------------------------

def generate_weak_points_summary() -> dict:
    """基于日志数据生成薄弱知识点总结。

    分析维度：
    1. 高频提问分类 = 学生关注 / 困惑的重点领域
    2. 证据不足问题 = 知识库覆盖薄弱的方向
    3. 高风险提问 = 涉及安全的实验领域

    返回 dict 含 weak_points 和 review_suggestions。
    """
    weak_points: list[str] = []
    review_suggestions: list[str] = []

    # 1. 分类统计 → 高频即薄弱
    cat_stats = get_category_stats()
    if cat_stats:
        top_cats = [c for c in cat_stats if c["count"] >= 2]
        for cat in top_cats[:3]:
            weak_points.append(f"「{cat['category']}」方向提问频繁（{cat['count']} 次），"
                               f"学生可能存在理解困难。")

    # 2. 证据不足
    insufficient = get_evidence_insufficient_count()
    if insufficient > 0:
        weak_points.append(f"有 {insufficient} 条提问缺少充分证据支持，"
                           f"知识库在相关方向需要补充。")

    # 3. 高风险
    risk = get_high_risk_stats()
    if risk.get("high_risk_count", 0) > 0:
        weak_points.append(f"出现 {risk['high_risk_count']} 条高风险实验相关提问，"
                           f"建议课堂重点讲解实验安全规范。")

    # 4. 生成复习建议
    if cat_stats:
        top_cat_names = [c["category"] for c in cat_stats[:3] if c["category"] != "其他"]
        if top_cat_names:
            review_suggestions.append(
                f"建议优先复习：{'、'.join(top_cat_names)}。"
            )
    if insufficient > 0:
        review_suggestions.append(
            "建议教师补充证据不足领域的教学材料和参考资料。"
        )
    if risk.get("high_risk_count", 0) > 0:
        review_suggestions.append(
            "建议安排一次实验安全专题课，覆盖高风险提问涉及的操作。"
        )
    if not weak_points:
        weak_points.append("当前日志数据不足，暂无法生成薄弱点总结。")
    if not review_suggestions:
        review_suggestions.append("数据量较少，建议持续积累问答记录后再生成复习建议。")

    return {
        "weak_points": weak_points,
        "review_suggestions": review_suggestions,
    }


# ---------------------------------------------------------------------------
# 汇总统计（供 API 使用）
# ---------------------------------------------------------------------------

def get_full_analysis() -> dict:
    """获取完整教师分析数据，供 /api/teacher/analysis 使用。"""
    return {
        "recent_questions": get_recent_questions(n=20),
        "keyword_frequency": get_keyword_frequency(top_n=15),
        "feedback_distribution": get_feedback_distribution(),
        "daily_question_counts": get_daily_question_counts(),
        "category_stats": get_category_stats(),
        "high_risk_stats": get_high_risk_stats(),
        "evidence_insufficient_count": get_evidence_insufficient_count(),
        "weak_points_summary": generate_weak_points_summary(),
        "question_count": get_question_count(),
        "feedback_count": get_feedback_count(),
    }
