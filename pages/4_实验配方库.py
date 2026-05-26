"""
实验配方库页面

支持检索实验配方、展示材料-浓度-工艺-表征-安全等级-来源，
支持按材料和安全等级筛选，显示教师复核提示。
"""

import core.path_setup  # noqa: F401

from dataclasses import asdict

import streamlit as st
import config
from core import recipe_extractor, safety_checker


def _render_safety_badge(level: str) -> None:
    """渲染安全等级标签。"""
    level_lower = level.lower() if level else "low"
    if level_lower in ("high", "高"):
        st.error("安全等级: 高 -- 需教师复核后方可使用")
    elif level_lower in ("medium", "中"):
        st.warning("安全等级: 中 -- 请注意安全操作规范")
    else:
        st.success("安全等级: 低 -- 但仍需遵守实验室基本安全规范")


def _render_recipe_card(recipe, idx: int) -> None:
    """渲染单条配方记录卡片。"""
    with st.container(border=True):
        col_header, col_safety = st.columns([3, 1])
        with col_header:
            st.markdown(f"**{idx}. {recipe.material}** -- {recipe.process}")
        with col_safety:
            _render_safety_badge(recipe.safety_level)

        # 字段网格
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(f"**浓度**: {recipe.concentration or '未标注'}")
            st.markdown(f"**温度**: {recipe.temperature or '未标注'}")
        with f2:
            st.markdown(f"**时间**: {recipe.time or '未标注'}")
            st.markdown(f"**表征方法**: {recipe.characterization or '未标注'}")
        with f3:
            st.markdown(f"**来源**: {recipe.source or '未标注'}")

        if recipe.result and recipe.result != "nan":
            st.markdown(f"**结果**: {recipe.result}")

        # 教学示例标记
        if recipe.is_example:
            st.caption("该记录标记为「教学示例」，浓度、温度、时间等数据非来自真实文献。")

        # 安全审核详情
        if recipe.safety_level.lower() in ("high", "高", "medium", "中"):
            with st.expander("查看安全审核详情"):
                check_result = safety_checker.check_recipe_record(asdict(recipe))
                for w in check_result.warnings:
                    st.markdown(f"- {w}")
                if check_result.teacher_review_checklist:
                    st.markdown("**教师复核清单:**")
                    for item in check_result.teacher_review_checklist:
                        st.markdown(f"  - {item}")


def main():
    # -----------------------------------------------------------------------
    # Hero
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>实验配方库</h1>'
        '<p>检索实验配方，了解 <span class="accent">材料体系、制备工艺和表征结果</span>'
        '，查看安全等级与教师复核提示</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 检索区域
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">配方检索</h2>', unsafe_allow_html=True)

    query = st.text_input(
        "搜索配方",
        placeholder="输入材料名称、工艺类型或研究目标，例如：水凝胶、乳化、3D 打印",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        material_filter = st.text_input("材料名称筛选（可选）", placeholder="例如：聚乙烯醇")
    with col2:
        safety_filter = st.selectbox(
            "安全等级筛选（可选）",
            ["全部", "低", "中", "高"],
        )

    search_clicked = st.button(
        "检索配方",
        type="primary",
        disabled=not query.strip(),
        use_container_width=True,
    )

    # -----------------------------------------------------------------------
    # 检索流程
    # -----------------------------------------------------------------------
    if search_clicked and query.strip():
        with st.spinner("正在检索实验配方..."):
            results = recipe_extractor.search(query.strip())

            # 应用筛选
            if material_filter.strip():
                results = [
                    r for r in results
                    if material_filter.strip().lower() in r.material.lower()
                ]
            if safety_filter != "全部":
                results = [
                    r for r in results
                    if r.safety_level.lower() == safety_filter.lower()
                ]

        if results:
            st.success(f"找到 {len(results)} 条匹配配方")
            for i, recipe in enumerate(results, 1):
                _render_recipe_card(recipe, i)
        else:
            st.info("未找到匹配的实验配方。请尝试其他关键词或放宽筛选条件。")

    # -----------------------------------------------------------------------
    # 空状态
    # -----------------------------------------------------------------------
    elif not search_clicked:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>输入关键词后点击「检索配方」，系统将从配方数据库中检索匹配记录。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # 数据说明
    # -----------------------------------------------------------------------
    st.markdown(
        '<h2 class="smg-section-title">数据说明</h2>',
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown(
            "- 配方数据中的 **浓度、温度、时间** 等参数如非来自真实文献资料，"
            "均已标注为「教学示例」，不得伪装成真实文献数据。\n"
            "- **安全等级** 由关键词规则自动推断，仅作为教学软件中的风险提示，"
            "不替代实验室正式安全审查。\n"
            "- 涉及高风险试剂、极端温度或压力的配方，必须经教师复核后方可讨论。"
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
