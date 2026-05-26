"""
文献知识检索页面

支持搜索文献记录、展示结构化信息（标题、年份、来源、材料体系、实验方法、
表征方式、结果摘要），支持上传 CSV / TXT / Markdown 导入文献。
"""

import core.path_setup  # noqa: F401
import core.styles; core.styles.apply()

import streamlit as st
import config
from core import literature_processor


def _render_lit_card(record, idx: int) -> None:
    """渲染单条文献记录卡片。"""
    year_display = record.year if record.year else "未知"
    with st.container(border=True):
        col_header, col_year = st.columns([4, 1])
        with col_header:
            st.markdown(f"**{idx}. {record.title}**")
        with col_year:
            st.markdown(f"`{year_display}`")

        # 字段网格
        f1, f2 = st.columns(2)
        with f1:
            st.markdown(f"**来源**: {record.source or '未标注'}")
            st.markdown(f"**材料体系**: {record.material_system or '未标注'}")
        with f2:
            st.markdown(f"**实验方法**: {record.method or '未标注'}")
            st.markdown(f"**表征方式**: {record.characterization or '未标注'}")

        if record.result_summary and record.result_summary != "nan":
            st.markdown(f"**结果摘要**: {record.result_summary}")
        if record.keywords and record.keywords != "nan":
            st.caption(f"关键词: {record.keywords}")
        if record.data_source and record.data_source not in ("unknown", "imported"):
            st.caption(f"数据来源: {record.data_source}")


def main():
    # -----------------------------------------------------------------------
    # Hero
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>文献知识检索</h1>'
        '<p>检索结构化文献记录，支持 <span class="accent">关键词、材料体系、年份</span>'
        ' 等多维筛选，并可导入 CSV / TXT / Markdown 文献数据</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 检索区域
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">文献检索</h2>', unsafe_allow_html=True)

    query = st.text_input(
        "搜索文献",
        placeholder="输入关键词、材料体系或研究方向，例如：水凝胶、Pickering 乳液、剪切变稀",
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        material_filter = st.text_input("材料体系筛选（可选）", placeholder="例如：水凝胶")
    with col2:
        year_from = st.text_input("起始年份（可选）", placeholder="例如：2020")
    with col3:
        year_to = st.text_input("截止年份（可选）", placeholder="例如：2025")

    search_clicked = st.button(
        "检索文献",
        type="primary",
        disabled=not query.strip(),
        use_container_width=True,
    )

    # -----------------------------------------------------------------------
    # 检索流程
    # -----------------------------------------------------------------------
    if search_clicked and query.strip():
        with st.spinner("正在检索文献记录..."):
            # 解析年份
            y_from = None
            y_to = None
            try:
                if year_from.strip():
                    y_from = int(year_from.strip())
            except ValueError:
                st.warning("起始年份格式不正确，已忽略。")
            try:
                if year_to.strip():
                    y_to = int(year_to.strip())
            except ValueError:
                st.warning("截止年份格式不正确，已忽略。")

            # 优先使用高级检索
            if material_filter.strip() or y_from or y_to:
                results = literature_processor.search_advanced(
                    keyword=query.strip(),
                    material=material_filter.strip() or None,
                    year_from=y_from,
                    year_to=y_to,
                )
            else:
                results = literature_processor.search(query.strip())

        if results:
            st.success(f"找到 {len(results)} 条匹配记录")
            for i, record in enumerate(results, 1):
                _render_lit_card(record, i)
        else:
            st.info("未找到匹配的文献记录。请尝试其他关键词或放宽筛选条件。")

    # -----------------------------------------------------------------------
    # 空状态提示
    # -----------------------------------------------------------------------
    elif not search_clicked:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>输入关键词后点击「检索文献」，系统将从文献数据库中检索匹配记录。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------------------------
    # 导入文献数据
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">导入文献数据</h2>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            "支持从 **CSV**、**TXT**（制表符分隔）和 **Markdown**（表格或列表格式）"
            "文件导入文献记录。CSV 文件必须包含 `title` 列。"
        )
        uploaded = st.file_uploader(
            "选择文件上传",
            type=["csv", "txt", "md"],
            accept_multiple_files=False,
            key="lit_upload",
        )

        if uploaded is not None:
            import tempfile
            from pathlib import Path

            # 保存上传文件到临时目录
            suffix = Path(uploaded.name).suffix.lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded.getvalue())
                tmp_path = Path(tmp.name)

            with st.spinner(f"正在解析 {uploaded.name} ..."):
                if suffix == ".csv":
                    result = literature_processor.import_from_csv(tmp_path)
                elif suffix == ".txt":
                    result = literature_processor.import_from_txt(tmp_path)
                elif suffix == ".md":
                    result = literature_processor.import_from_markdown(tmp_path)
                else:
                    result = {"imported": 0, "skipped": 0, "errors": ["不支持的文件格式"]}

            if result["imported"] > 0:
                st.success(
                    f"成功导入 {result['imported']} 条文献记录"
                    f"（跳过 {result['skipped']} 条重复或无效记录）"
                )
                literature_processor.reload()
            elif result["skipped"] > 0 and not result["errors"]:
                st.info(f"所有记录均为重复或无效，已跳过 {result['skipped']} 条。")
            if result["errors"]:
                for err in result["errors"]:
                    st.error(err)

    # -----------------------------------------------------------------------
    # 安全声明
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">{config.SAFETY_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
