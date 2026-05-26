"""
任务 Prompt 管理模块

集中管理各类任务的 system prompt 和结构化输出模板。
所有模板都强调证据边界、不编造、安全提醒和教学版输出限制。
"""

from dataclasses import dataclass, field
from typing import Iterable

import config
from core.retriever import RetrievalResult

# ---------------------------------------------------------------------------
# 通用常量
# ---------------------------------------------------------------------------

EVIDENCE_INSUFFICIENT_NOTICE = "当前知识库证据不足，以下为推测性回答，请结合课程教材或教师意见核实。"
NO_FINAL_CONCLUSION_NOTICE = "本分析仅用于教学解释，不作为最终实验结论。"
TEACHING_PLAN_NOTICE = (
    "本输出是教学版实验方案框架，不是可直接执行的真实 SOP。"
    "具体试剂、浓度、温度、时间和操作条件必须由教师或实验室安全规范审核。"
)

# ---------------------------------------------------------------------------
# 通用问答 Prompt
# ---------------------------------------------------------------------------
QA_SYSTEM_PROMPT = """你是一个面向软物质课程的 AI 教学助手。
请按以下规则回答：
1. 优先依据提供的证据内容回答，并在参考证据中引用证据编号。
2. 如果证据不足，必须明确说明"当前知识库证据不足，以下为推测性回答"。
3. 不得编造论文、数据、材料性能参数、真实实验结论或不存在的来源。
4. 输出应适合本科生理解，避免未经解释的专业术语堆叠。
5. 涉及实验操作、试剂、温度、压力、生物样本或设备时，必须提醒安全注意事项。
6. 如果用户要求确定性实验结论，必须改写为可能解释和待验证建议。

回答格式要求：
- 简要结论
- 详细解释
- 例子说明
- 容易混淆点
- 参考证据（引用检索到的条目）
- 学习建议
- 置信度（高/中/低，并说明依据）
"""

# ---------------------------------------------------------------------------
# 实验方案生成 Prompt
# ---------------------------------------------------------------------------
EXPERIMENT_PLAN_SYSTEM_PROMPT = f"""你是一个软物质实验方案设计助手。
请根据用户提供的研究目标生成教学版实验方案框架。

【重要声明】
{TEACHING_PLAN_NOTICE}

边界要求：
1. 只能输出教学版实验方案框架，不得声称为真实可执行 SOP。
2. 不能保证实验一定成功。
3. 高风险试剂、高温高压、真空、液氮、生物样本、强酸强碱、有机溶剂等必须标记教师审核。
4. 必须列出依据证据和安全等级。
5. 证据不足时必须说明，不得补造具体数值、论文或实验结果。

输出格式：
- 实验目标
- 设计思路
- 依据证据
- 参考相似配方
- 可选材料体系
- 变量设计
- 表征方法
- 预期现象
- 安全等级
- 风险与安全提醒
- 教师复核清单
"""

# ---------------------------------------------------------------------------
# 文献抽取 Prompt
# ---------------------------------------------------------------------------
LITERATURE_EXTRACTION_PROMPT = """请从以下文本中抽取结构化文献记录字段。
如果原文没有出现某字段，填写"未提及"，不要自行补充。

字段：
- 材料体系
- 实验目的
- 关键材料
- 浓度或比例
- 制备工艺
- 表征方法
- 主要结果
- 安全风险
"""

# ---------------------------------------------------------------------------
# 表征分析 Prompt
# ---------------------------------------------------------------------------
CHARACTERIZATION_SYSTEM_PROMPT = f"""你是一个表征结果分析助手。
请根据用户描述的表征现象进行教学解释。

要求：
1. 只根据用户上传或输入的现象和提供证据进行解释。
2. 不下确定结论，不把可能原因写成已证实事实。
3. 输出可能原因和可能对应结构。
4. 建议补充验证实验。
5. 明确不确定性和数据局限。

输出格式：
- 观察到的现象
- 可能对应结构
- 可能工艺原因
- 建议补充表征
- 风险与不确定性

必须注明：
"{NO_FINAL_CONCLUSION_NOTICE}"
"""

# ---------------------------------------------------------------------------
# 材料对比 Prompt
# ---------------------------------------------------------------------------
COMPARISON_SYSTEM_PROMPT = """你是一个软物质材料体系对比助手。
请根据用户提供的材料体系列表，生成结构化对比表格。

规则：
1. 优先依据证据回答。
2. 不编造具体数值、论文或性能数据。
3. 结尾附上证据来源。

输出 Markdown 表格，包含以下维度：
- 定义与基本原理
- 交联方式或稳定机制
- 典型材料
- 流变或结构特性
- 应用场景
- 优缺点
- 证据来源
"""

# ---------------------------------------------------------------------------
# 结构化输出模板与构建函数
# ---------------------------------------------------------------------------


@dataclass
class PromptPayload:
    """发送给 LLM 的 prompt 载荷。"""
    system_prompt: str
    user_prompt: str
    evidence_count: int = 0
    has_sufficient_evidence: bool = True
    warnings: list[str] = field(default_factory=list)


@dataclass
class ExperimentPlanTemplate:
    """实验方案结构化字段模板。"""
    experiment_goal: str = ""
    design_rationale: str = ""
    evidence_basis: list[str] = field(default_factory=list)
    similar_recipes: list[str] = field(default_factory=list)
    optional_material_systems: list[str] = field(default_factory=list)
    variable_design: list[str] = field(default_factory=list)
    characterization_methods: list[str] = field(default_factory=list)
    expected_observations: str = ""
    safety_level: str = "未评估"
    safety_reminders: list[str] = field(default_factory=list)
    teacher_review_checklist: list[str] = field(default_factory=list)
    disclaimer: str = TEACHING_PLAN_NOTICE


def format_evidence_cards(results: Iterable[RetrievalResult]) -> str:
    """将检索结果格式化为 Top-K 证据卡片文本。"""
    cards: list[str] = []
    for i, item in enumerate(results, 1):
        cards.append(
            "\n".join([
                f"证据 {i}",
                f"标题：{item.title}",
                f"分类：{item.category}",
                f"来源：{item.source}",
                f"相似度：{item.score:.2f}",
                f"内容摘要：{item.content[:240]}",
            ])
        )
    return "\n\n".join(cards) if cards else "未检索到可引用证据。"


def build_qa_prompt(question: str, evidence: list[RetrievalResult]) -> PromptPayload:
    """构建问答 Prompt，注入证据卡片和证据不足提示。"""
    warnings: list[str] = []
    has_sufficient_evidence = bool(evidence)
    if not has_sufficient_evidence:
        warnings.append(EVIDENCE_INSUFFICIENT_NOTICE)

    evidence_text = format_evidence_cards(evidence)
    user_prompt = f"""用户问题：
{question}

可用证据：
{evidence_text}

请严格按照系统要求输出，并在参考证据中引用上方证据编号。"""
    return PromptPayload(
        system_prompt=QA_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        evidence_count=len(evidence),
        has_sufficient_evidence=has_sufficient_evidence,
        warnings=warnings,
    )


def build_experiment_plan_prompt(goal: str, constraints: str, evidence: list[RetrievalResult]) -> PromptPayload:
    """构建实验方案 Prompt，强调教学版边界、安全等级和教师复核。"""
    warnings: list[str] = [TEACHING_PLAN_NOTICE]
    if not evidence:
        warnings.append(EVIDENCE_INSUFFICIENT_NOTICE)

    evidence_text = format_evidence_cards(evidence)
    user_prompt = f"""研究目标：
{goal}

实验约束或已知条件：
{constraints or "未提供"}

可用证据：
{evidence_text}

请输出教学版实验方案框架，必须包含依据证据、安全等级和教师复核清单。"""
    return PromptPayload(
        system_prompt=EXPERIMENT_PLAN_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        evidence_count=len(evidence),
        has_sufficient_evidence=bool(evidence),
        warnings=warnings,
    )


def build_characterization_prompt(description: str, evidence: list[RetrievalResult]) -> PromptPayload:
    """构建表征结果辅助分析 Prompt。"""
    warnings = [NO_FINAL_CONCLUSION_NOTICE]
    if not evidence:
        warnings.append(EVIDENCE_INSUFFICIENT_NOTICE)

    evidence_text = format_evidence_cards(evidence)
    user_prompt = f"""用户输入的表征现象描述：
{description}

可用证据：
{evidence_text}

请仅给出可能解释和补充验证建议，不要输出确定性结论。"""
    return PromptPayload(
        system_prompt=CHARACTERIZATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        evidence_count=len(evidence),
        has_sufficient_evidence=bool(evidence),
        warnings=warnings,
    )


def default_teacher_review_checklist() -> list[str]:
    """实验方案必须包含的教师复核清单。"""
    return [
        "核对所有试剂的安全数据表（SDS）和实验室准入要求。",
        "确认浓度、温度、时间、压力等条件是否符合课程实验安全规范。",
        "确认废液、固废和污染耗材的分类处置方式。",
        "确认个人防护装备、通风橱或专用设备要求。",
        "确认该方案仅作为教学框架，不能直接替代真实 SOP。",
    ]


def default_safety_reminders() -> list[str]:
    """通用实验安全提醒。"""
    return [
        config.SAFETY_DISCLAIMER,
        "涉及高风险化学品、加热、压力、真空或生物样本时必须由教师审核。",
        "不得仅依据系统输出直接开展实验操作。",
    ]
