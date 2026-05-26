"""
材料体系对比页面

支持预设对比主题和自定义对比输入，生成结构化 Markdown 表格，
展示对比结果和证据来源。
"""

import core.path_setup  # noqa: F401

import streamlit as st
import config
from core import llm_client, retriever
from core import prompt_templates as presets


PRESET_COMPARISONS = [
    "物理交联水凝胶 vs 化学交联水凝胶",
    "表面活性剂乳液 vs Pickering 乳液",
    "牛顿流体 vs 非牛顿流体",
    "胶体凝胶 vs 高分子凝胶",
    "剪切变稀 vs 触变性",
]

PRESET_DESCRIPTIONS = {
    "物理交联水凝胶 vs 化学交联水凝胶": "对比物理交联（氢键、离子键等可逆交联）与化学交联（共价键不可逆交联）水凝胶的结构、力学和应用差异。",
    "表面活性剂乳液 vs Pickering 乳液": "对比传统表面活性剂稳定的乳液与固体颗粒稳定的 Pickering 乳液的稳定机制和特性。",
    "牛顿流体 vs 非牛顿流体": "对比粘度不随剪切速率变化的牛顿流体与表现出剪切变稀/增稠等行为的非牛顿流体。",
    "胶体凝胶 vs 高分子凝胶": "对比胶体颗粒通过物理相互作用形成的凝胶与高分子链交联形成的凝胶。",
    "剪切变稀 vs 触变性": "对比剪切变稀（粘度随剪切速率降低）与触变性（结构随时间恢复）的机理和表征方法。",
}


def _render_evidence_sources(results) -> None:
    """渲染证据来源列表。"""
    if not results:
        st.caption("当前知识库中未找到直接相关证据。")
        return

    st.markdown('<h2 class="smg-section-title">证据来源</h2>', unsafe_allow_html=True)
    for i, ev in enumerate(results[:5], 1):
        with st.container(border=True):
            col_header, col_score = st.columns([3, 1])
            with col_header:
                st.markdown(f"**{i}. {ev.title}**")
            with col_score:
                st.markdown(f"`相似度 {ev.score:.2f}`")
            st.caption(f"分类: {ev.category} | 来源: {ev.source} | 类型: {ev.data_type}")
            if ev.content:
                st.markdown(ev.content[:200] + "..." if len(ev.content) > 200 else ev.content)


def main():
    # -----------------------------------------------------------------------
    # Hero
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>材料体系对比</h1>'
        '<p>对比不同软物质材料体系的 <span class="accent">结构、特性、流变行为和应用场景</span>，'
        '生成结构化对比表格并展示证据来源</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 预设对比主题
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">预设对比主题</h2>', unsafe_allow_html=True)

    preset_cols = st.columns(len(PRESET_COMPARISONS))
    selected_preset = None
    for i, (col, topic) in enumerate(zip(preset_cols, PRESET_COMPARISONS)):
        with col:
            if st.button(topic, key=f"preset_{i}", use_container_width=True):
                selected_preset = topic

    # -----------------------------------------------------------------------
    # 对比输入
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">对比配置</h2>', unsafe_allow_html=True)

    # 预设选择器
    preset_select = st.selectbox(
        "选择预设对比主题",
        ["自定义输入"] + PRESET_COMPARISONS,
        key="preset_select",
    )

    # 确定默认值
    default_value = ""
    if selected_preset:
        default_value = selected_preset
    elif preset_select != "自定义输入":
        default_value = preset_select

    custom_input = st.text_input(
        "对比主题",
        placeholder="例如：物理交联水凝胶 vs 化学交联水凝胶",
        value=default_value,
    )

    # 显示预设说明
    if custom_input in PRESET_DESCRIPTIONS:
        st.info(PRESET_DESCRIPTIONS[custom_input])

    compare_clicked = st.button(
        "生成对比分析",
        type="primary",
        disabled=not custom_input.strip(),
        use_container_width=True,
    )

    # -----------------------------------------------------------------------
    # 对比流程
    # -----------------------------------------------------------------------
    if compare_clicked and custom_input.strip():
        topic = custom_input.strip()

        # 1. 检索相关证据
        with st.spinner("正在从知识库中检索相关证据..."):
            bundle = retriever.search_all(topic)
            evidence_list = bundle.results

        # 2. 构建带证据的 prompt
        evidence_context = ""
        if evidence_list:
            evidence_parts = []
            for i, ev in enumerate(evidence_list[:5], 1):
                evidence_parts.append(
                    f"证据 {i}: {ev.title}（{ev.category}，相似度 {ev.score:.2f}）\n{ev.content[:300]}"
                )
            evidence_context = "\n\n".join(evidence_parts)

        user_prompt = f"请对比以下材料体系: {topic}"
        if evidence_context:
            user_prompt += f"\n\n可用证据:\n{evidence_context}"
        user_prompt += "\n\n请输出 Markdown 格式的对比表格，并在末尾附上证据来源。"

        # 3. 调用 LLM
        with st.spinner("正在生成对比分析..."):
            response = llm_client.generate(
                prompt=user_prompt,
                system=presets.COMPARISON_SYSTEM_PROMPT,
            )

        if response.success:
            st.markdown(
                '<h2 class="smg-section-title">对比结果</h2>',
                unsafe_allow_html=True,
            )

            # 对比结果
            with st.container(border=True):
                st.markdown(response.content)

            # 证据来源
            _render_evidence_sources(evidence_list)

            # 数据声明
            st.caption(
                "以上对比基于知识库证据和模型推理生成，"
                "如涉及具体数值或性能参数请以原始文献为准。"
            )
        else:
            st.error(f"生成失败: {response.error}")
            st.info(
                "请检查 Ollama 服务是否已启动，并前往 **系统设置** 页面确认模型配置。"
            )

    # -----------------------------------------------------------------------
    # 空状态
    # -----------------------------------------------------------------------
    elif not compare_clicked:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>选择预设对比主题或输入自定义对比后点击「生成对比分析」，系统将生成结构化对比表格。</p>
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
