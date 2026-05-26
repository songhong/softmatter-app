"""
表征结果辅助分析页面

支持文字描述分析和图片上传入口，基于 RAG 证据和规则库
进行教学解释，输出可能结构、工艺原因和补充表征建议。
"""

import core.path_setup  # noqa: F401
import core.styles; core.styles.apply()

import streamlit as st
import config
from core import characterization


def _render_analysis_result(result) -> None:
    """渲染表征分析结果。"""
    # 置信度
    if result.confidence in ("中", "高"):
        st.markdown(
            f'<span class="smg-confidence-high">置信度: {result.confidence}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<span class="smg-confidence-low">置信度: {result.confidence}</span>',
            unsafe_allow_html=True,
        )

    # 结构化输出
    with st.container(border=True):
        st.markdown(f"**观察到的现象**\n\n{result.observation}")

        st.markdown("---")
        st.markdown(f"**可能对应结构**\n\n{result.possible_structure}")

        st.markdown("---")
        st.markdown(f"**可能工艺原因**\n\n{result.possible_cause}")

        st.markdown("---")
        st.markdown("**建议补充表征**")
        for test in result.suggested_tests:
            st.markdown(f"- {test}")

        st.markdown("---")
        st.markdown(f"**风险与不确定性**\n\n{result.uncertainty}")

    # 教学解释声明
    st.info(result.disclaimer)

    # 证据来源
    if result.evidence:
        st.markdown('<h2 class="smg-section-title">参考证据</h2>', unsafe_allow_html=True)
        for i, ev in enumerate(result.evidence[:5], 1):
            with st.container(border=True):
                col_header, col_score = st.columns([3, 1])
                with col_header:
                    st.markdown(f"**证据 {i} -- {ev.title}**")
                with col_score:
                    st.markdown(f"`相似度 {ev.score:.2f}`")
                st.caption(f"分类: {ev.category} | 来源: {ev.source}")
                st.markdown(ev.content[:300] + "..." if len(ev.content) > 300 else ev.content)
    else:
        st.caption("当前知识库中未找到直接相关证据，分析结果主要基于表征规则。")


def main():
    # -----------------------------------------------------------------------
    # Hero
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>表征结果辅助分析</h1>'
        '<p>上传表征图片或输入文字描述，获取 <span class="accent">教学辅助解读</span>，'
        '包含可能结构、工艺原因和补充表征建议</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 教学解释声明（必须明显）
    # -----------------------------------------------------------------------
    st.error(
        "**重要声明**: 图像和数据分析结果仅作为教学解释，不作为最终实验结论。"
        "所有「可能原因」均为推测性分析，需要结合原始数据和重复实验验证。"
    )

    # -----------------------------------------------------------------------
    # 分析模式切换
    # -----------------------------------------------------------------------
    tab_text, tab_image = st.tabs(["文字描述分析", "图片上传"])

    # --- 文字描述分析 ---
    with tab_text:
        st.markdown('<h2 class="smg-section-title">输入表征现象描述</h2>', unsafe_allow_html=True)

        # 常见表征类型提示
        with st.expander("常见表征类型示例（点击查看）"):
            st.markdown(
                "- **流变测试**: 剪切变稀、剪切增稠、G' 与 G'' 交叉、触变恢复\n"
                "- **SEM/TEM 显微**: 多孔结构、相分离、表面形貌\n"
                "- **FTIR/红外**: 峰位移动、新峰出现、氢键变化\n"
                "- **DLS 粒度**: 粒径分布、PDI 变化、胶束聚集\n"
                "- **温敏行为**: LCST 溶胀/塌缩、相转变"
            )

        description = st.text_area(
            "请描述观察到的表征现象",
            placeholder=(
                "例如：SEM 图像显示表面存在大量不规则孔洞，孔径约 10-50 微米，"
                "断面可见层状结构；流变测试中粘度随剪切速率增加而降低..."
            ),
            height=150,
        )

        analyze_clicked = st.button(
            "开始分析",
            type="primary",
            disabled=not description.strip(),
            use_container_width=True,
            key="text_analyze",
        )

        if analyze_clicked and description.strip():
            with st.spinner("正在基于规则库和知识库证据进行分析..."):
                result = characterization.analyze_text(description.strip())

            st.markdown('<h2 class="smg-section-title">分析结果</h2>', unsafe_allow_html=True)
            _render_analysis_result(result)

    # --- 图片上传 ---
    with tab_image:
        st.markdown('<h2 class="smg-section-title">上传表征图片</h2>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "上传 SEM / TEM / 流变数据图片",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=False,
            key="char_upload",
        )

        if uploaded is not None:
            st.image(uploaded, caption="上传的表征图片", use_container_width=True)

            st.info(
                "图片分析功能将在增强版中接入多模态模型。"
                "当前 MVP 阶段请结合图片在「文字描述分析」标签页中输入文字描述进行分析。"
            )

            # 提供图片描述输入框
            st.markdown("---")
            img_desc = st.text_area(
                "请描述图片中的关键现象",
                placeholder="例如：图片显示不规则多孔结构，孔径分布不均匀...",
                height=100,
                key="img_desc",
            )
            if st.button(
                "基于描述分析",
                type="primary",
                disabled=not img_desc.strip(),
                use_container_width=True,
                key="img_analyze",
            ):
                with st.spinner("正在分析..."):
                    result = characterization.analyze_text(img_desc.strip())

                st.markdown(
                    '<h2 class="smg-section-title">分析结果</h2>',
                    unsafe_allow_html=True,
                )
                _render_analysis_result(result)

        else:
            st.markdown(
                """
                <div class="smg-empty-state">
                    <p>上传 SEM、TEM 或流变数据图片后，可查看图片并输入文字描述进行教学辅助分析。</p>
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
