"""
实验安全审核模块

负责检测实验方案、配方和自由文本中的高风险内容，标记需要教师复核的部分。
本模块只做教学软件中的风险提示，不替代实验室正式安全审查。
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

import config
from core import data_loader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 风险规则
# ---------------------------------------------------------------------------

HIGH_RISK_PATTERNS = {
    "强酸/强腐蚀": ["强酸", "浓硫酸", "浓硝酸", "氢氟酸", "王水", "硫酸水解", "H2SO4", "HF"],
    "强碱/强腐蚀": ["强碱", "氢氧化钠", "NaOH", "KOH"],
    "高压/真空": ["高压", "压力釜", "高压釜", "真空", "抽真空"],
    "极端温度": ["液氮", "超低温", "高温", "灼烧", "煅烧"],
    "有机溶剂/易燃": ["有机溶剂", "苯乙烯", "甲苯", "THF", "丙酮", "乙醇", "易燃", "易燃易爆"],
    "毒性/致癌": ["致癌", "剧毒", "有毒", "丙烯酰胺", "甲醛", "戊二醛"],
    "生物安全": ["细胞", "细菌", "病毒", "血清", "生物样本", "动物实验"],
}

MEDIUM_RISK_PATTERNS = {
    "加热/光照引发": ["加热", "升温", "紫外", "UV", "光引发", "引发剂", "聚合"],
    "纳米材料": ["纳米", "SiO2", "氧化石墨烯", "GO", "碳纳米管", "CNC"],
    "实验设备": ["流变仪", "高速乳化", "离心", "透析", "SEM", "TEM"],
}

SAFETY_LEVEL_ORDER = {"低": 0, "low": 0, "中": 1, "medium": 1, "高": 2, "high": 2}

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class RiskFinding:
    """单条安全风险发现。"""
    category: str
    keyword: str
    severity: str
    message: str


@dataclass
class SafetyCheckResult:
    """安全审核结果。"""
    is_safe: bool = True
    risk_level: str = "低"  # 低 / 中 / 高
    warnings: list[str] = field(default_factory=list)
    requires_teacher_review: bool = False
    findings: list[RiskFinding] = field(default_factory=list)
    teacher_review_checklist: list[str] = field(default_factory=list)
    teaching_boundary: str = field(default_factory=lambda: config.SAFETY_DISCLAIMER)

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "risk_level": self.risk_level,
            "warnings": self.warnings,
            "requires_teacher_review": self.requires_teacher_review,
            "findings": [f.__dict__ for f in self.findings],
            "teacher_review_checklist": self.teacher_review_checklist,
            "teaching_boundary": self.teaching_boundary,
        }


# ---------------------------------------------------------------------------
# 内部工具
# ---------------------------------------------------------------------------


def _normalize_text(text: str | None) -> str:
    return (text or "").strip()


def _contains_keyword(text: str, keyword: str) -> bool:
    if not keyword:
        return False
    # 中文/英文混合：大小写不敏感，同时避免正则特殊字符误伤
    return re.search(re.escape(keyword), text, flags=re.IGNORECASE) is not None


def _risk_level_from_score(score: int) -> str:
    if score >= 2:
        return "高"
    if score == 1:
        return "中"
    return "低"


def _merge_level(current: str, incoming: str) -> str:
    reverse = {0: "低", 1: "中", 2: "高"}
    cur_score = SAFETY_LEVEL_ORDER.get(current, 0)
    inc_score = SAFETY_LEVEL_ORDER.get(incoming, 0)
    return reverse[max(cur_score, inc_score)]


def _base_teacher_review_checklist() -> list[str]:
    return [
        "核对试剂安全数据表（SDS）和课程实验室准入要求。",
        "确认浓度、温度、时间、压力、光照、真空等条件是否符合实验室规范。",
        "确认个人防护装备、通风橱、废弃物处置和应急预案。",
        "确认学生不能将教学版方案直接作为真实 SOP 执行。",
    ]


def _add_finding(result: SafetyCheckResult, category: str, keyword: str, severity: str) -> None:
    message = f"检测到{severity}风险项：{category}（关键词：{keyword}）。"
    result.findings.append(RiskFinding(category=category, keyword=keyword, severity=severity, message=message))
    result.warnings.append(message)
    result.risk_level = _merge_level(result.risk_level, severity)


# ---------------------------------------------------------------------------
# 公开接口
# ---------------------------------------------------------------------------


def check_text(text: str) -> SafetyCheckResult:
    """对文本进行安全关键词和操作风险检测。

    Args:
        text: 待检测文本（实验方案、问答内容等）。

    Returns:
        SafetyCheckResult 包含风险等级、警告信息和教师复核清单。
    """
    normalized = _normalize_text(text)
    result = SafetyCheckResult(teacher_review_checklist=_base_teacher_review_checklist())

    if not normalized:
        result.warnings.append("未提供可审核文本，无法完成安全风险判断。")
        result.requires_teacher_review = True
        result.risk_level = "中"
        result.is_safe = False
        return result

    # 兼容 config 中配置的高风险关键词
    for keyword in config.HIGH_RISK_KEYWORDS:
        if _contains_keyword(normalized, keyword):
            _add_finding(result, "配置高风险关键词", keyword, "高")

    for category, keywords in HIGH_RISK_PATTERNS.items():
        for keyword in keywords:
            if _contains_keyword(normalized, keyword):
                _add_finding(result, category, keyword, "高")

    for category, keywords in MEDIUM_RISK_PATTERNS.items():
        for keyword in keywords:
            if _contains_keyword(normalized, keyword):
                _add_finding(result, category, keyword, "中")

    # 结果汇总
    if result.risk_level == "高":
        result.is_safe = False
        result.requires_teacher_review = True
        result.warnings.append("该内容包含高风险因素，必须提交教师或实验室安全负责人复核。")
    elif result.risk_level == "中":
        result.is_safe = True
        result.requires_teacher_review = True
        result.warnings.append("该内容包含中等风险因素，建议教师复核后再用于课程实验讨论。")
    else:
        result.is_safe = True
        result.requires_teacher_review = False
        result.warnings.append("未检测到明显高风险关键词；仍需遵守课程实验室安全规范。")

    # 去重但保持顺序
    result.warnings = list(dict.fromkeys(result.warnings))
    result.teacher_review_checklist = list(dict.fromkeys(result.teacher_review_checklist))

    if result.findings:
        logger.info("安全审核发现风险项: %s", [f.keyword for f in result.findings])

    return result


def check_recipe_record(recipe: dict | pd.Series) -> SafetyCheckResult:
    """对单条实验配方记录进行安全审核。

    支持读取配方自带 safety_level，同时结合工艺文本二次判断。
    """
    if isinstance(recipe, pd.Series):
        recipe_data = recipe.to_dict()
    else:
        recipe_data = recipe or {}

    text = " ".join(str(v) for v in recipe_data.values() if pd.notna(v))
    result = check_text(text)

    raw_level = str(recipe_data.get("safety_level", "")).strip().lower()
    if raw_level in ("high", "高"):
        result.risk_level = _merge_level(result.risk_level, "高")
        result.requires_teacher_review = True
        result.is_safe = False
        result.warnings.append("配方库将该配方标记为高安全等级风险，必须教师复核。")
    elif raw_level in ("medium", "中"):
        result.risk_level = _merge_level(result.risk_level, "中")
        result.requires_teacher_review = True
        result.warnings.append("配方库将该配方标记为中等安全风险，建议教师复核。")

    result.warnings = list(dict.fromkeys(result.warnings))
    return result


def check_recipe(recipe: dict | pd.Series | str) -> SafetyCheckResult:
    """统一配方安全审核入口。

    支持 dict、pandas Series 或配方 ID 字符串输入。该函数只返回教学软件中的
    风险提示、教师复核建议和安全边界，不替代正式实验室安全审查。
    """
    if isinstance(recipe, str):
        return check_recipe_by_id(recipe)
    return check_recipe_record(recipe)


def check_recipe_by_id(recipe_id: str) -> SafetyCheckResult:
    """按配方 ID 从配方库中读取并审核。"""
    df = data_loader.get_recipes_data()
    if df.empty or "id" not in df.columns:
        result = SafetyCheckResult(
            is_safe=False,
            risk_level="中",
            warnings=["配方库为空或缺少 id 字段，无法完成配方安全审核。"],
            requires_teacher_review=True,
            teacher_review_checklist=_base_teacher_review_checklist(),
        )
        return result

    matched = df[df["id"].astype(str) == str(recipe_id)]
    if matched.empty:
        result = SafetyCheckResult(
            is_safe=False,
            risk_level="中",
            warnings=[f"未找到配方 ID：{recipe_id}，无法完成配方安全审核。"],
            requires_teacher_review=True,
            teacher_review_checklist=_base_teacher_review_checklist(),
        )
        return result

    return check_recipe_record(matched.iloc[0])


def generate_teacher_review_checklist(risk_level: str = "低", findings: list[RiskFinding] | None = None) -> list[str]:
    """根据风险等级和发现项生成教师复核清单。"""
    checklist = _base_teacher_review_checklist()
    findings = findings or []
    categories = {f.category for f in findings}

    if risk_level == "高":
        checklist.append("高风险内容必须由教师或实验室安全负责人书面确认后才可进入实验教学。")
    if "强酸/强腐蚀" in categories or "强碱/强腐蚀" in categories:
        checklist.append("确认腐蚀性试剂的稀释顺序、防护面罩、耐酸碱手套和泄漏处置流程。")
    if "高压/真空" in categories:
        checklist.append("确认压力/真空设备资质、耐压范围、泄压和防爆措施。")
    if "有机溶剂/易燃" in categories:
        checklist.append("确认通风橱、火源隔离、易燃液体储存和废液桶标签。")
    if "生物安全" in categories:
        checklist.append("确认生物样本来源、灭菌、伦理合规和生物安全等级要求。")

    return list(dict.fromkeys(checklist))


def add_safety_disclaimer(text: str) -> str:
    """在文本末尾追加安全免责声明，避免重复追加。"""
    if config.SAFETY_DISCLAIMER in text:
        return text
    return f"{text}\n\n---\n{config.SAFETY_DISCLAIMER}"
