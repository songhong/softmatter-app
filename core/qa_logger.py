"""
问答日志与反馈模块

记录用户问答历史和反馈信息到 CSV 文件。
提供中文关键词提取工具函数，供 analytics 模块使用。
"""

import logging
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CSV 列定义
# ---------------------------------------------------------------------------
_QA_COLUMNS = [
    "timestamp", "question_id", "question", "answer",
    "model", "evidence_count", "confidence", "risk_level",
]

_FEEDBACK_COLUMNS = [
    "timestamp", "question_id", "rating", "comment",
]

# ---------------------------------------------------------------------------
# 中文停用词（高频虚词 / 标点 / 数字 / 单字）
# ---------------------------------------------------------------------------
_STOPWORDS = frozenset(
    "的 了 是 在 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 "
    "没有 看 好 自己 这 他 她 它 们 那 些 什么 怎么 如何 为什么 请 可以 哪 "
    "如果 但 因为 所以 而 或 与 对 把 被 从 向 让 给 以 于 等 这个 那个 "
    "吗 呢 吧 啊 哦 嗯 嘛 啦 呀 哪 些 每 各 再 又 才 已 正 将 能 可 应 "
    "比较 说明 解释 简述 介绍 描述 列举 列出 简要 详细 简单 具体 "
    "什么 什么样 哪些 哪个 怎样 怎么样 多少 几".split()
)

# 软物质领域常见术语词典（用于关键词提取的优先匹配）
_DOMAIN_TERMS = [
    # 核心概念
    "剪切变稀", "剪切增稠", "触变性", "流变学", "流变", "粘弹性", "粘度",
    "胶体", "胶体科学", "胶体稳定性", "Zeta电位", "DLVO理论", "双电层",
    "水凝胶", "高分子", "高分子科学", "嵌段共聚物", "接枝共聚物",
    "自组装", "微相分离", "胶束", "囊泡", "液晶",
    "乳液", "Pickering乳液", "表面活性剂", "界面", "界面科学",
    "表面张力", "接触角", "润湿", "吸附",
    "智能材料", "形状记忆", "响应性", "温度响应", "pH响应",
    "相变", "LCST", "UCST", "玻璃化转变", "熔点",
    "交联", "化学交联", "物理交联", "凝胶化", "溶胀",
    "纳米粒子", "纳米颗粒", "碳纳米管", "石墨烯",
    "药物递送", "缓释", "控释", "靶向",
    "表征", "表征方法", "原子力显微镜", "AFM", "SEM", "TEM",
    "DSC", "TGA", "红外光谱", "拉曼光谱", "XRD",
    "流变仪", "旋转流变仪", "毛细管流变仪",
    "动态光散射", "DLS", "粒径分析",
    "表面张力仪", "接触角测量",
    "软物质", "聚合物", "单体", "引发剂", "链段",
    "氢键", "静电作用", "疏水作用", "范德华力",
    "扩散", "渗透", "膜", "分离",
    "弹性", "塑性", "韧性", "强度", "模量",
    "稳定性", "聚沉", "絮凝", "分散",
    "浓度", "温度", "压力", "pH值",
    "溶液", "悬浊液", "胶体溶液",
    "均聚物", "共聚物", "聚合度", "分子量",
    "结晶", "非晶", "半结晶", "球晶",
    "纤维", "薄膜", "涂层", "复合材料",
    "降解", "生物降解", "生物相容性",
]


def _append_to_csv(file_path: Path, row: dict, columns: list[str]) -> bool:
    """向 CSV 文件追加一行记录。"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame([row], columns=columns)

        if file_path.exists():
            df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")
        else:
            df.to_csv(file_path, mode="w", header=True, index=False, encoding="utf-8-sig")
        return True
    except Exception as exc:
        logger.error("写入 CSV 失败: %s - %s", file_path, exc)
        return False


def log_qa(question: str, answer: str, model: str = "",
           evidence_count: int = 0, confidence: str = "",
           risk_level: str = "", question_id: str = "") -> bool:
    """记录一次问答。

    Args:
        question: 用户提问。
        answer: AI 回答。
        model: 使用的模型名称。
        evidence_count: 证据条数。
        confidence: 置信度标签（高/低）。
        risk_level: 风险等级（高/中/低）。
        question_id: 问题唯一 ID，为空时自动生成。

    Returns:
        是否写入成功。
    """
    row = {
        "timestamp": datetime.now().isoformat(),
        "question_id": question_id or f"q-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "question": question,
        "answer": answer,
        "model": model,
        "evidence_count": evidence_count,
        "confidence": confidence,
        "risk_level": risk_level,
    }
    return _append_to_csv(config.QA_HISTORY_CSV, row, _QA_COLUMNS)


def log_feedback(question_id: str, rating: int, comment: str = "") -> bool:
    """记录用户反馈。

    Args:
        question_id: 关联的问题 ID。
        rating: 评分（1-5）。
        comment: 用户评论。

    Returns:
        是否写入成功。
    """
    row = {
        "timestamp": datetime.now().isoformat(),
        "question_id": question_id,
        "rating": rating,
        "comment": comment,
    }
    return _append_to_csv(config.FEEDBACK_CSV, row, _FEEDBACK_COLUMNS)


def extract_keywords(texts: list[str], top_n: int = 20) -> list[dict]:
    """从文本列表中提取高频关键词。

    采用领域术语优先匹配 + 正则分词的混合策略，
    无需外部中文分词库（如 jieba）。

    Args:
        texts: 待分析的文本列表。
        top_n: 返回前 N 个高频词。

    Returns:
        关键词-频次列表，形如 [{"keyword": "水凝胶", "count": 5}, ...]。
    """
    counter: Counter = Counter()

    for text in texts:
        if not text:
            continue
        text = str(text)

        # 第一轮：匹配领域术语
        matched_spans: list[tuple[int, int]] = []
        for term in _DOMAIN_TERMS:
            idx = text.find(term)
            while idx != -1:
                matched_spans.append((idx, idx + len(term)))
                counter[term] += 1
                idx = text.find(term, idx + len(term))

        # 第二轮：对未被领域术语覆盖的区域做正则分词
        # 中文 2-6 字连续序列
        for m in re.finditer(r"[一-鿿]{2,6}", text):
            start, end = m.start(), m.end()
            # 跳过与领域术语有任何重叠的区域
            if any(start < e and end > s for s, e in matched_spans):
                continue
            word = m.group()
            if word not in _STOPWORDS:
                counter[word] += 1

        # 英文词（保留 3 字母以上的）
        for m in re.finditer(r"[a-zA-Z]{3,}", text):
            word = m.group()
            if word.lower() not in {"the", "and", "for", "are", "but", "not", "you", "all",
                                     "can", "had", "her", "was", "one", "our", "out", "day",
                                     "get", "has", "him", "his", "how", "its", "may", "new",
                                     "now", "old", "see", "way", "who", "did", "got",
                                     "let", "say", "too", "use"}:
                counter[word] += 1

    return [{"keyword": word, "count": count} for word, count in counter.most_common(top_n)]
