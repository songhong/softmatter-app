"""
首页 - 系统总览与状态面板

展示项目定位、系统架构、模型状态、数据统计和安全声明。
所有状态数据来自真实后端模块，不伪造任何在线状态或统计数据。
"""

import core.path_setup  # noqa: F401

import streamlit as st
import config
from core import (
    retriever,
    literature_processor,
    recipe_extractor,
    llm_client,
    analytics,
)


def _render_card(label: str, value: str, css_class: str = "") -> None:
    """渲染自定义状态卡片。"""
    cls_extra = f" {css_class}" if css_class else ""
    st.markdown(
        f'<div class="smg-card">'
        f'<div class="smg-card-label">{label}</div>'
        f'<div class="smg-card-value{cls_extra}">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def main():
    # -----------------------------------------------------------------------
    # 页面标题
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>SoftMatterGPT</h1>'
        '<p>面向软物质课程与实验教学的 <span class="accent">AI 教学工作台</span><br>'
        '基于 RAG 检索增强生成，集成课程问答、文献挖掘、实验配方、方案生成与教师分析</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 系统架构流程图
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">系统架构</h2>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="smg-arch-flow">
            <div class="smg-arch-node">用户浏览器</div>
            <div class="smg-arch-arrow">&#8594;</div>
            <div class="smg-arch-node highlight">Streamlit 前端</div>
            <div class="smg-arch-arrow">&#8594;</div>
            <div class="smg-arch-node highlight">FastAPI 后端</div>
            <div class="smg-arch-arrow">&#8594;</div>
            <div class="smg-arch-node">核心业务模块</div>
            <div class="smg-arch-arrow">&#8594;</div>
            <div class="smg-arch-node">数据层 + Ollama</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("查看核心模块详情"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                "- `retriever.py` -- 课程知识库检索\n"
                "- `literature_processor.py` -- 文献记录解析与检索\n"
                "- `recipe_extractor.py` -- 实验配方字段抽取\n"
                "- `llm_client.py` -- Ollama / 公开 LLM 调用\n"
                "- `prompt_templates.py` -- 任务 Prompt 管理"
            )
        with col_b:
            st.markdown(
                "- `safety_checker.py` -- 实验安全审核\n"
                "- `qa_logger.py` -- 问答日志与反馈\n"
                "- `analytics.py` -- 教师统计分析\n"
                "- `characterization.py` -- 表征结果辅助分析\n"
                "- `data_loader.py` -- 数据加载与缓存"
            )

    st.markdown("")

    # -----------------------------------------------------------------------
    # 系统状态卡片
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">系统状态</h2>', unsafe_allow_html=True)

    # 获取真实状态数据
    ollama_status = llm_client.check_ollama_status()
    current_model = llm_client.get_current_model()
    kb_stats = retriever.get_stats()
    lit_stats = literature_processor.get_stats()
    recipe_stats = recipe_extractor.get_stats()
    feedback_dist = analytics.get_feedback_distribution()
    total_questions = analytics.get_question_count()
    daily_counts = analytics.get_daily_question_counts()

    # 今日提问次数
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_count = 0
    for item in daily_counts:
        if item.get("date") == today_str:
            today_count = item.get("count", 0)
            break

    # Ollama 状态样式
    if ollama_status.online:
        ollama_display = "在线"
        ollama_css = "online"
    else:
        ollama_display = "离线"
        ollama_css = "offline"

    # 第一行: 模型与连接
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _render_card("当前模型", current_model)
    with c2:
        _render_card("Ollama 状态", ollama_display, ollama_css)
    with c3:
        _render_card("课程知识库", f'{kb_stats.get("knowledge", {}).get("total", 0)} 条')
    with c4:
        _render_card("文献记录", f'{lit_stats.get("total", 0)} 条')

    # 第二行: 配方、问答、反馈
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        _render_card("实验配方", f'{recipe_stats.get("total", 0)} 条')
    with c6:
        _render_card("今日问答", f"{today_count} 次")
    with c7:
        _render_card("累计问答", f"{total_questions} 次")
    with c8:
        sat = feedback_dist.get("satisfaction_rate", 0)
        _render_card("反馈满意率", f"{sat}%")

    # -----------------------------------------------------------------------
    # Ollama 连接详情
    # -----------------------------------------------------------------------
    if not ollama_status.online:
        st.warning(
            f"Ollama 服务当前不可达：{ollama_status.message}\n\n"
            "请确认 Ollama 已启动，并前往 **系统设置** 页面检查服务地址和模型配置。"
        )
    else:
        st.success(
            f"{ollama_status.message}  当前使用模型: **{current_model}**"
        )

    # -----------------------------------------------------------------------
    # 数据说明
    # -----------------------------------------------------------------------
    st.markdown('<h2 class="smg-section-title">数据概览</h2>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(
            f"""
            | 数据源 | 条数 |
            |--------|------|
            | 课程知识库 | {kb_stats.get("knowledge", {}).get("total", 0)} |
            | 文献记录 | {lit_stats.get("total", 0)} |
            | 实验配方 | {recipe_stats.get("total", 0)} |
            | 问答历史 | {total_questions} |
            """
        )
    with col_right:
        # 读取 settings.json 中的数据说明
        from core import data_loader
        settings = data_loader.load_json(config.SETTINGS_JSON)
        data_note = settings.get("data_stats", {}).get("note", "")
        if data_note:
            st.info(data_note)

    # -----------------------------------------------------------------------
    # 安全声明
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">{config.SAFETY_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
