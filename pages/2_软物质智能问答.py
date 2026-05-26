"""
软物质智能问答页面

基于 RAG 检索增强生成的课程知识问答。
检索全知识库证据 → 构建结构化 prompt → 调用 LLM → 展示结构化回答与 Top-K 证据卡片。
输出风格为正式教学软件，非普通聊天框。
"""

import core.path_setup  # noqa: F401
import core.styles; core.styles.apply()

import uuid
from datetime import datetime

import streamlit as st
import config
from core import (
    retriever,
    llm_client,
    safety_checker,
    qa_logger,
)
from core import prompt_templates as prompts


def _render_evidence_card(idx: int, ev) -> None:
    """渲染单张证据卡片（使用 Streamlit 原生组件，避免 XSS 风险）。"""
    with st.container(border=True):
        col_header, col_score = st.columns([3, 1])
        with col_header:
            st.markdown(f"**证据 {idx} -- {ev.title}**")
        with col_score:
            st.markdown(f"`相似度 {ev.score:.2f}`")
        st.caption(f"分类: {ev.category} | 来源: {ev.source} | 类型: {ev.data_type}")
        st.markdown(ev.content)


def _render_confidence(confidence: str) -> None:
    """渲染置信度标签。"""
    if confidence == "高":
        css = "smg-confidence-high"
    else:
        css = "smg-confidence-low"
    st.markdown(
        f'<span class="{css}">置信度: {confidence}</span>',
        unsafe_allow_html=True,
    )


def main():
    st.markdown(
        '<div class="smg-hero">'
        '<h1>软物质智能问答</h1>'
        '<p>基于 <span class="accent">RAG 检索增强生成</span>，从课程知识库、文献记录和实验配方中'
        '检索证据，生成结构化教学回答</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 问题输入
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">输入问题</h2>', unsafe_allow_html=True)

    # 示例问题
    examples = [
        "什么是剪切变稀？为什么洗发水和番茄酱会表现出类似行为？",
        "CMC（临界胶束浓度）的物理意义是什么？如何测量？",
        "物理交联水凝胶和化学交联水凝胶有什么区别？",
        "DLS（动态光散射）的原理和适用范围是什么？",
        "Pickering 乳液与传统表面活性剂乳液有何不同？",
    ]

    if "qa_text_area" not in st.session_state:
        st.session_state["qa_text_area"] = ""

    with st.expander("示例问题（点击填入）"):
        for i, ex in enumerate(examples):
            if st.button(ex, key=f"ex_{i}"):
                st.session_state["qa_text_area"] = ex
                st.rerun()

    question = st.text_area(
        "请输入你的问题",
        placeholder="例如：什么是剪切变稀？为什么洗发水和番茄酱会表现出类似行为？",
        height=120,
        key="qa_text_area",
    )

    ask_disabled = not question.strip()
    ask_clicked = st.button(
        "提交问题",
        type="primary",
        disabled=ask_disabled,
        use_container_width=True,
    )

    # -----------------------------------------------------------------------
    # 问答流程
    # -----------------------------------------------------------------------
    if ask_clicked and question.strip():
        q = question.strip()

        # 1. 检索证据（跨全部知识库）
        with st.spinner("正在从课程知识库、文献记录和实验配方中检索相关证据..."):
            bundle = retriever.search_all(q)
            evidence_list = bundle.results

        # 2. 构建带证据的 QA prompt
        prompt_payload = prompts.build_qa_prompt(q, evidence_list)

        # 3. 调用 LLM
        with st.spinner("正在调用语言模型生成结构化回答..."):
            response = llm_client.generate(
                prompt=prompt_payload.user_prompt,
                system=prompt_payload.system_prompt,
            )

        if response.success:
            # 4. 安全审核
            safety_result = safety_checker.check_text(response.content)

            # 5. 记录日志
            question_id = f"q-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
            qa_logger.log_qa(
                question=q,
                answer=response.content,
                model=response.model,
                evidence_count=len(evidence_list),
                confidence="高" if bundle.has_sufficient_evidence else "低",
                risk_level=safety_result.risk_level,
                question_id=question_id,
            )

            # -------------------------------------------------------------------
            # 展示回答
            # -------------------------------------------------------------------
            st.markdown('<h2 class="smg-section-title">回答</h2>', unsafe_allow_html=True)

            # 置信度与模型信息
            conf_col, model_col, evidence_col = st.columns([1, 1, 1])
            with conf_col:
                _render_confidence("高" if bundle.has_sufficient_evidence else "低")
            with model_col:
                st.markdown(
                    f'<span style="font-size:0.82rem; color:#64748b;">'
                    f'模型: {response.model}</span>',
                    unsafe_allow_html=True,
                )
            with evidence_col:
                st.markdown(
                    f'<span style="font-size:0.82rem; color:#64748b;">'
                    f'检索证据: {len(evidence_list)} 条</span>',
                    unsafe_allow_html=True,
                )

            # 证据不足警告
            if prompt_payload.warnings:
                for w in prompt_payload.warnings:
                    st.warning(w)

            # 结构化回答（使用 Streamlit 原生 markdown 渲染，确保列表/标题正常显示）
            with st.container(border=True):
                st.markdown(response.content)

            # 安全提示
            if not safety_result.is_safe:
                st.error(
                    f"安全检测: {safety_result.warnings[0] if safety_result.warnings else '检测到风险内容'}"
                )
            elif safety_result.requires_teacher_review:
                st.warning(
                    f"安全提示: {safety_result.warnings[0] if safety_result.warnings else '建议教师复核'}"
                )

            # -------------------------------------------------------------------
            # Top-K 证据卡片
            # -------------------------------------------------------------------
            if evidence_list:
                st.markdown(
                    '<h2 class="smg-section-title">参考证据 (Top-K)</h2>',
                    unsafe_allow_html=True,
                )
                for i, ev in enumerate(evidence_list, 1):
                    _render_evidence_card(i, ev)
            else:
                st.info("当前知识库中未找到与该问题直接相关的证据。回答基于模型通用知识，建议结合教材核实。")

            # -------------------------------------------------------------------
            # 反馈区域
            # -------------------------------------------------------------------
            st.markdown('<h2 class="smg-section-title">回答反馈</h2>', unsafe_allow_html=True)

            fb_cols = st.columns([1, 1, 1, 3])
            with fb_cols[0]:
                if st.button("满意", key="fb_good", use_container_width=True):
                    qa_logger.log_feedback(question_id=question_id, rating=5, comment="")
                    st.success("感谢反馈！")
            with fb_cols[1]:
                if st.button("一般", key="fb_ok", use_container_width=True):
                    qa_logger.log_feedback(question_id=question_id, rating=3, comment="")
                    st.success("感谢反馈！")
            with fb_cols[2]:
                if st.button("不满意", key="fb_bad", use_container_width=True):
                    qa_logger.log_feedback(question_id=question_id, rating=1, comment="")
                    st.success("感谢反馈，我们会改进。")

        else:
            # LLM 调用失败
            st.error(f"模型调用失败: {response.error}")
            st.info("请检查 Ollama 服务是否已启动，并前往 **系统设置** 页面确认模型配置。")

            # 即使 LLM 失败也展示检索到的证据
            if evidence_list:
                st.markdown(
                    '<h2 class="smg-section-title">已检索到的证据（模型未响应）</h2>',
                    unsafe_allow_html=True,
                )
                for i, ev in enumerate(evidence_list, 1):
                    _render_evidence_card(i, ev)

    # -----------------------------------------------------------------------
    # 页面说明（首次进入时）
    # -----------------------------------------------------------------------
    elif not ask_clicked:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>输入问题后点击「提交问题」，系统将从知识库中检索证据并生成结构化回答。</p>
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
