"""
表征结果辅助分析模块

提供表征数据（显微图、流变曲线等）的教学辅助分析功能。
MVP 阶段基于文本描述和 RAG 证据进行规则化分析，不接入真实图像识别。
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from core import retriever
from core.retriever import RetrievalResult

logger = logging.getLogger(__name__)

DISCLAIMER = "图像和数据分析结果仅作为教学解释，不作为最终实验结论。"

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class CharacterizationResult:
    """表征分析结果。"""
    observation: str = ""
    possible_structure: str = ""
    possible_cause: str = ""
    suggested_tests: list[str] = field(default_factory=list)
    uncertainty: str = ""
    evidence: list[RetrievalResult] = field(default_factory=list)
    confidence: str = "低"
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation": self.observation,
            "possible_structure": self.possible_structure,
            "possible_cause": self.possible_cause,
            "suggested_tests": self.suggested_tests,
            "uncertainty": self.uncertainty,
            "evidence": [e.__dict__ for e in self.evidence],
            "confidence": self.confidence,
            "disclaimer": self.disclaimer,
        }


@dataclass
class CharacterizationRule:
    """表征现象规则。"""
    keywords: list[str]
    possible_structure: str
    possible_cause: str
    suggested_tests: list[str]


# ---------------------------------------------------------------------------
# 规则库：只输出可能性，不输出确定结论
# ---------------------------------------------------------------------------

RULES: list[CharacterizationRule] = [
    CharacterizationRule(
        keywords=["剪切变稀", "粘度降低", "黏度降低", "shear thinning"],
        possible_structure="可能存在可取向的高分子链、胶束网络或可被剪切破坏的弱物理网络。",
        possible_cause="剪切作用下链段取向、缠结减少或弱相互作用网络暂时解体，可能导致表观粘度降低。",
        suggested_tests=["稳态剪切流变曲线", "触变三段测试", "振荡频率扫描", "重复升降剪切速率测试"],
    ),
    CharacterizationRule(
        keywords=["剪切增稠", "粘度升高", "黏度升高", "shear thickening"],
        possible_structure="可能存在高浓度颗粒悬浮体系或剪切诱导的瞬态颗粒接触网络。",
        possible_cause="高剪切下颗粒间润滑层失效或形成水动力团簇，可能造成阻力上升。",
        suggested_tests=["不同固含量流变测试", "粒径分布测试", "显微观察剪切前后结构", "重复性和边界滑移排查"],
    ),
    CharacterizationRule(
        keywords=["G'", "G''", "储能模量", "损耗模量", "凝胶点"],
        possible_structure="可能涉及粘弹性网络、凝胶化过程或溶胶-凝胶转变。",
        possible_cause="交联密度、物理缔合、温度响应或浓度变化可能改变储能模量与损耗模量关系。",
        suggested_tests=["小振幅振荡剪切（SAOS）", "应变扫描确定线性粘弹区", "频率扫描", "温度扫描或时间扫描"],
    ),
    CharacterizationRule(
        keywords=["孔", "多孔", "SEM", "断面", "粗糙", "塌陷"],
        possible_structure="可能存在多孔网络、相分离结构、干燥塌陷或冻干引入的孔结构。",
        possible_cause="溶剂交换、冻干、相分离、交联不均或样品制备过程可能影响显微形貌。",
        suggested_tests=["重复 SEM 样品制备", "冷冻干燥条件对照", "溶胀率测试", "孔径统计", "力学或流变测试"],
    ),
    CharacterizationRule(
        keywords=["相分离", "岛状", "海岛", "不均匀", "浑浊", "白色"],
        possible_structure="可能出现微相分离、宏观相分离或组分分散不均。",
        possible_cause="组分相容性不足、溶剂挥发速率、浓度过高或混合过程不足可能导致不均匀结构。",
        suggested_tests=["光学显微镜观察", "DSC 测 Tg 变化", "FTIR 或 Raman 组分分析", "不同配比对照实验"],
    ),
    CharacterizationRule(
        keywords=["胶束", "CMC", "DLS", "粒径", "聚集"],
        possible_structure="可能存在胶束、胶体聚集体或粒径分布变化。",
        possible_cause="浓度、盐浓度、pH 或表面活性剂结构变化可能影响自组装和聚集状态。",
        suggested_tests=["DLS 粒径和 PDI 测试", "电导率法测 CMC", "Zeta 电位测试", "SANS/SAXS 结构表征"],
    ),
    CharacterizationRule(
        keywords=["FTIR", "红外", "傅里叶红外", "峰位", "新峰", "氢键峰", "特征峰"],
        possible_structure="可能涉及氢键、配位作用、官能团环境变化或组分间相互作用导致的光谱特征变化。",
        possible_cause="FTIR/红外峰位移动或新峰可能与氢键强弱改变、官能团参与非共价相互作用、组分复合、样品含水量或基线/扣背景处理有关；不能仅凭峰位变化下最终结构结论。",
        suggested_tests=["重复 FTIR 并进行空白/基线/扣背景对照", "对比纯组分与共混/反应后样品的 FTIR 特征峰", "变温 FTIR 或氘代/干燥对照验证氢键贡献", "结合 Raman、XPS、DSC 或流变测试交叉验证相互作用与结构变化"],
    ),
    CharacterizationRule(
        keywords=["LCST", "温敏", "升温", "塌缩", "溶胀"],
        possible_structure="可能涉及温度响应高分子链的亲水-疏水转变和凝胶网络体积变化。",
        possible_cause="温度跨越相转变区间时，链-水相互作用改变可能导致溶胀或塌缩。",
        suggested_tests=["温度扫描流变", "不同温度溶胀比测试", "DSC", "DLS 随温度变化测试"],
    ),
    CharacterizationRule(
        keywords=["Pickering", "乳液", "液滴", "破乳", "稳定"],
        possible_structure="可能存在颗粒吸附界面稳定的乳液液滴结构。",
        possible_cause="颗粒润湿性、粒径、浓度、油水比或乳化能量可能影响液滴尺寸和稳定性。",
        suggested_tests=["光学显微镜液滴尺寸统计", "接触角测试", "离心稳定性测试", "储存稳定性观察"],
    ),
]

# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------


def _match_rules(description: str) -> list[CharacterizationRule]:
    lowered = description.lower()
    matches: list[CharacterizationRule] = []
    for rule in RULES:
        if any(k.lower() in lowered for k in rule.keywords):
            matches.append(rule)
    return matches


def _combine_unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys([i for i in items if i]))


def _confidence_from_evidence(evidence: list[RetrievalResult], matched_rules: list[CharacterizationRule]) -> str:
    if evidence and matched_rules and evidence[0].score >= 0.5:
        return "中"
    if evidence or matched_rules:
        return "低-中"
    return "低"

# ---------------------------------------------------------------------------
# 公开接口
# ---------------------------------------------------------------------------


def analyze_text(description: str, top_k: int | None = None) -> CharacterizationResult:
    """基于文本描述分析表征结果。

    Args:
        description: 用户描述的表征现象（如 SEM 形貌描述、流变曲线趋势等）。
        top_k: 检索证据数量。

    Returns:
        CharacterizationResult 包含教学分析、证据和不确定性说明。
    """
    cleaned = (description or "").strip()
    if not cleaned:
        return CharacterizationResult(
            observation="未提供表征现象描述。",
            possible_structure="无法判断。",
            possible_cause="缺少现象描述，不能进行合理解释。",
            suggested_tests=["请补充表征类型、样品体系、关键趋势和实验条件。"],
            uncertainty="输入为空，所有分析均不可用。",
            confidence="低",
        )

    matched_rules = _match_rules(cleaned)
    bundle = retriever.search_all(cleaned, top_k=top_k)
    evidence = bundle.results

    if matched_rules:
        possible_structures = _combine_unique([r.possible_structure for r in matched_rules])
        possible_causes = _combine_unique([r.possible_cause for r in matched_rules])
        suggested_tests = _combine_unique([test for r in matched_rules for test in r.suggested_tests])
    else:
        possible_structures = ["可能涉及软物质体系的形貌、流变或自组装结构变化，但现有规则无法直接匹配。"]
        possible_causes = ["可能与材料组成、浓度、温度、制备工艺或样品前处理有关，需要结合更多实验信息判断。"]
        suggested_tests = ["补充样品配方和制备条件", "重复表征以确认现象稳定性", "选择流变、显微、光谱或散射表征进行交叉验证"]

    if evidence:
        evidence_titles = "；".join([f"{e.title}（相似度 {e.score:.2f}）" for e in evidence[:3]])
        evidence_note = f"可参考的课程/文献/配方证据包括：{evidence_titles}。"
    else:
        evidence_note = "当前知识库证据不足，以下解释主要为基于表征规则的教学性可能分析。"

    uncertainty_parts = [
        "该结果不能证明单一结构或工艺原因，只能给出可能解释。",
        evidence_note,
        "需要结合原始图像、仪器参数、样品制备条件和重复实验进行验证。",
        DISCLAIMER,
    ]

    result = CharacterizationResult(
        observation=cleaned,
        possible_structure="；".join(possible_structures),
        possible_cause="；".join(possible_causes),
        suggested_tests=suggested_tests,
        uncertainty=" ".join(uncertainty_parts),
        evidence=evidence,
        confidence=_confidence_from_evidence(evidence, matched_rules),
    )

    logger.info("表征分析完成，匹配规则数=%d，证据数=%d", len(matched_rules), len(evidence))
    return result


def analyze_characterization(description: str, top_k: int | None = None) -> CharacterizationResult:
    """表征分析兼容入口。"""
    return analyze_text(description, top_k=top_k)


def analyze_rheology_trend(trend_description: str) -> CharacterizationResult:
    """流变趋势分析快捷入口。"""
    return analyze_text(f"流变结果：{trend_description}")


def analyze_microscopy_description(description: str) -> CharacterizationResult:
    """显微形貌文本描述分析快捷入口。"""
    return analyze_text(f"显微形貌：{description}")
