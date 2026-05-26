"""
实验方案助手页面

输入研究目标、材料体系、期望性能、实验约束和安全等级，
生成教学版实验方案框架，包含教师复核清单和安全提醒。
"""

import core.path_setup  # noqa: F401

import streamlit as st
import config
from core import llm_client, safety_checker, prompt_templates as prompts


def _render_teacher_checklist(checklist: list[str]) -> None:
    """渲染教师复核清单。"""
    with st.container(border=True):
        st.markdown("**教师复核清单**")
        for item in checklist:
            st.markdown(f"- [ ] {item}")


def _render_safety_findings(result) -> None:
    """渲染安全审核详情。"""
    if result.findings:
        st.markdown("**检测到的风险项:**")
        for f in result.findings:
            st.markdown(f"- [{f.severity}] {f.category}（关键词: `{f.keyword}`）")


def main():
    # -----------------------------------------------------------------------
    # Hero
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>实验方案助手</h1>'
        '<p>基于研究目标生成 <span class="accent">教学版实验方案框架</span>，'
        '包含设计思路、变量设计、表征方法和教师复核清单</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 教学边界声明
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">{prompts.TEACHING_PLAN_NOTICE}</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 输入表单
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">输入研究需求</h2>', unsafe_allow_html=True)

    with st.form("experiment_plan_form"):
        research_goal = st.text_area(
            "研究目标 *",
            placeholder="例如：制备一种具有剪切变稀特性的水凝胶用于 3D 打印",
            height=100,
        )

        col1, col2 = st.columns(2)
        with col1:
            material_system = st.text_input(
                "材料体系（可选）",
                placeholder="例如：聚乙烯醇水凝胶",
            )
            expected_property = st.text_input(
                "期望性能（可选）",
                placeholder="例如：剪切变稀、快速凝胶化",
            )
        with col2:
            constraints = st.text_input(
                "实验约束（可选）",
                placeholder="例如：室温操作、无有毒试剂",
            )
            safety_level = st.selectbox(
                "安全等级预估",
                ["低", "中", "高"],
                help="选择您对该实验风险等级的初步判断",
            )

        need_references = st.checkbox("需要文献依据", value=True)

        submitted = st.form_submit_button(
            "生成实验方案",
            type="primary",
            use_container_width=True,
        )

    # -----------------------------------------------------------------------
    # 生成流程
    # -----------------------------------------------------------------------
    if submitted and research_goal.strip():
        with st.spinner("正在检索证据并生成教学版实验方案..."):
            # 构建 prompt
            parts = [f"研究目标: {research_goal.strip()}"]
            if material_system.strip():
                parts.append(f"材料体系: {material_system.strip()}")
            if expected_property.strip():
                parts.append(f"期望性能: {expected_property.strip()}")
            if constraints.strip():
                parts.append(f"实验约束: {constraints.strip()}")
            parts.append(f"安全等级预估: {safety_level}")
            if need_references:
                parts.append("需要文献依据: 是")

            user_prompt = "\n".join(parts)

            response = llm_client.generate(
                prompt=user_prompt,
                system=prompts.EXPERIMENT_PLAN_SYSTEM_PROMPT,
            )

        if response.success:
            st.markdown('<h2 class="smg-section-title">生成结果</h2>', unsafe_allow_html=True)

            # 安全审核
            safety_result = safety_checker.check_text(response.content)

            # 置信度和模型信息
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.caption(f"生成模型: {response.model}")
            with info_col2:
                if safety_result.risk_level == "高":
                    st.markdown(
                        '<span class="smg-confidence-low">风险等级: 高</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<span class="smg-confidence-high">风险等级: {safety_result.risk_level}</span>',
                        unsafe_allow_html=True,
                    )

            # 方案正文
            with st.container(border=True):
                st.markdown(response.content)

            # 安全提示
            if not safety_result.is_safe:
                st.error(
                    f"安全检测: {safety_result.warnings[0] if safety_result.warnings else '检测到高风险内容'}"
                )
                _render_safety_findings(safety_result)

            if safety_result.requires_teacher_review:
                st.warning(
                    "该方案包含需要教师复核的内容，请在教师确认后再用于课程实验讨论。"
                )
                _render_teacher_checklist(safety_result.teacher_review_checklist)

            # 通用教师复核清单
            st.markdown('<h2 class="smg-section-title">教师复核清单</h2>', unsafe_allow_html=True)
            _render_teacher_checklist(prompts.default_teacher_review_checklist())

        else:
            st.error(f"生成失败: {response.error}")
            st.info(
                "请检查 Ollama 服务是否已启动，并前往 **系统设置** 页面确认模型配置。"
            )

    # -----------------------------------------------------------------------
    # 使用说明
    # -----------------------------------------------------------------------
    elif not submitted:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>填写研究目标和相关信息后点击「生成实验方案」，系统将生成教学版实验方案框架。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # 安全声明
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">{config.SAFETY_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
