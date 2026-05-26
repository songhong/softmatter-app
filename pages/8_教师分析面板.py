"""
教师分析面板页面

展示学生学习数据、高频问题、薄弱知识点和反馈统计。
所有图表和统计均基于真实日志和反馈数据，不编造任何指标。
"""

import core.path_setup  # noqa: F401
import core.styles; core.styles.apply()

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import config
from core import analytics


# ---------------------------------------------------------------------------
# 配色方案 -- 映射 app.py 全局 :root CSS 变量
# ---------------------------------------------------------------------------
# VIS-001 fix: 使用与 --smg-* 变量一致的色值，而非独立硬编码蓝色系
_PRIMARY = "#0d9488"       # --smg-teal
_SECONDARY = "#7C3AED"    # --smg-* 中无紫色，保留辅助色
_SUCCESS = "#16a34a"       # --smg-green
_WARNING = "#d97706"       # --smg-amber
_DANGER = "#dc2626"        # --smg-red
_NEUTRAL = "#64748b"       # --smg-gray-400

_PIE_COLORS = [_SUCCESS, _WARNING, _DANGER]


def _render_metric_card(label: str, value: str | int, delta: str = "",
                        color: str = _PRIMARY) -> None:
    """渲染一个数据指标卡片（使用 .smg-card 全局类）。"""
    # VIS-003 fix: 使用 .smg-card / .smg-card-label / .smg-card-value 全局类
    # A11Y-001 fix: delta 文本改用 #64748b (对比度 >= 4.6:1 on white)
    delta_html = (
        f"<div style='font-size: 0.78rem; color: #64748b; margin-top: 4px;'>"
        f"{delta}</div>"
        if delta else ""
    )
    st.markdown(
        f"""
        <div class="smg-card" style="border-left: 4px solid {color};">
            <div class="smg-card-label">{label}</div>
            <div class="smg-card-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_section_header(title: str, subtitle: str = "") -> None:
    """渲染板块标题。"""
    # A11Y-003 fix: 使用 ## (H2) 而非 ### (H3)，避免从 H1 直接跳到 H3
    # VIS-003 fix: 使用 .smg-section-title 全局类
    st.markdown(f'<h2 class="smg-section-title">{title}</h2>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


def _render_empty_state(message: str) -> None:
    """渲染空状态提示（使用 .smg-empty-state 全局类）。"""
    st.markdown(
        f'<div class="smg-empty-state"><p>{message}</p></div>',
        unsafe_allow_html=True,
    )


def main():
    # -----------------------------------------------------------------------
    # VIS-002 fix: 使用 .smg-hero 渐变背景横幅，与其他页面一致
    # -----------------------------------------------------------------------
    st.markdown(
        '<div class="smg-hero">'
        '<h1>教师分析面板</h1>'
        '<p>基于真实问答日志和反馈数据的 <span class="accent">教学分析统计</span></p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # 数据加载（一次性）
    # -----------------------------------------------------------------------
    qa_count = analytics.get_question_count()
    fb_count = analytics.get_feedback_count()
    risk_stats = analytics.get_high_risk_stats()
    insufficient_count = analytics.get_evidence_insufficient_count()

    # -----------------------------------------------------------------------
    # 顶部数据总览卡片
    # -----------------------------------------------------------------------
    card_cols = st.columns(5)
    with card_cols[0]:
        _render_metric_card("累计提问", qa_count, color=_PRIMARY)
    with card_cols[1]:
        _render_metric_card("反馈条数", fb_count, color=_SECONDARY)
    with card_cols[2]:
        _render_metric_card("高风险方案", risk_stats.get("high_risk_count", 0),
                            color=_DANGER)
    with card_cols[3]:
        _render_metric_card("证据不足", insufficient_count, color=_WARNING)
    with card_cols[4]:
        fb_dist = analytics.get_feedback_distribution()
        sat = fb_dist.get("satisfaction_rate", 0.0)
        if fb_count > 0:
            _render_metric_card("正面反馈率", f"{sat}%",
                                f"{fb_dist['positive']} / {fb_count} 条",
                                color=_SUCCESS)
        else:
            _render_metric_card("正面反馈率", "--", "暂无数据", color=_NEUTRAL)

    st.divider()

    # -----------------------------------------------------------------------
    # 最近提问记录
    # -----------------------------------------------------------------------
    _render_section_header("最近提问记录", "按时间倒序展示最近 20 条学生提问")
    recent = analytics.get_recent_questions(n=20)
    if recent:
        df_recent = pd.DataFrame(recent)
        display_cols = [c for c in ["timestamp", "question", "model", "confidence",
                                     "evidence_count", "risk_level"]
                        if c in df_recent.columns]
        if display_cols:
            st.dataframe(
                df_recent[display_cols],
                use_container_width=True,
                column_config={
                    "timestamp": st.column_config.TextColumn("时间"),
                    "question": st.column_config.TextColumn("提问内容"),
                    "model": st.column_config.TextColumn("模型"),
                    "confidence": st.column_config.TextColumn("置信度"),
                    "evidence_count": st.column_config.NumberColumn("证据数"),
                    "risk_level": st.column_config.TextColumn("风险等级"),
                },
                hide_index=True,
            )
        else:
            st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        # VIS-003 fix: 使用 .smg-empty-state 替代 st.info
        _render_empty_state("暂无提问记录。学生使用智能问答功能后，记录将在此显示。")

    st.divider()

    # -----------------------------------------------------------------------
    # 图表区域：左关键词柱状图 | 右反馈饼图
    # -----------------------------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        _render_section_header("高频关键词 Top 15", "从学生提问中提取的高频领域术语")
        keywords = analytics.get_keyword_frequency(top_n=15)
        if keywords:
            df_kw = pd.DataFrame(keywords)
            fig_kw = px.bar(
                df_kw, x="keyword", y="count",
                title="",
                labels={"keyword": "关键词", "count": "出现次数"},
                color="count",
                color_continuous_scale="Blues",
            )
            fig_kw.update_layout(
                xaxis_tickangle=-45,
                margin=dict(t=10, b=40),
                coloraxis_showscale=False,
                height=400,
            )
            st.plotly_chart(fig_kw, use_container_width=True)
            # A11Y-002 fix: 为图表添加文字描述，辅助无障碍阅读
            st.caption("柱状图：展示学生提问中出现频率最高的 15 个领域关键词。")
        else:
            _render_empty_state("暂无关键词数据。")

    with col_right:
        _render_section_header("反馈评分分布", "学生对 AI 回答的满意度分布")
        fb = analytics.get_feedback_distribution()
        if fb.get("total", 0) > 0:
            labels = ["满意 (4-5)", "中性 (3)", "不满意 (1-2)"]
            values = [fb["positive"], fb["neutral"], fb["negative"]]
            # 过滤零值
            filtered = [(l, v) for l, v in zip(labels, values) if v > 0]
            if filtered:
                f_labels, f_values = zip(*filtered)
                fig_pie = go.Figure(data=[go.Pie(
                    labels=f_labels,
                    values=f_values,
                    hole=0.4,
                    marker=dict(colors=_PIE_COLORS[:len(f_labels)]),
                    textinfo="label+percent",
                    textfont_size=13,
                )])
                fig_pie.update_layout(
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=400,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15,
                                xanchor="center", x=0.5),
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                # A11Y-002 fix
                st.caption("饼图：展示学生对 AI 回答的满意、中性和不满意反馈分布。")
            else:
                _render_empty_state("反馈数据不足。")
        else:
            _render_empty_state("暂无反馈数据。学生提交反馈后将在此显示分布。")

    # -----------------------------------------------------------------------
    # 每日提问趋势
    # -----------------------------------------------------------------------
    _render_section_header("每日提问趋势", "学生提问频次随时间的变化")
    daily = analytics.get_daily_question_counts()
    if daily:
        df_daily = pd.DataFrame(daily)
        fig_line = px.line(
            df_daily, x="date", y="count",
            title="",
            labels={"date": "日期", "count": "提问次数"},
            markers=True,
        )
        fig_line.update_traces(line_color=_PRIMARY)
        fig_line.update_layout(
            margin=dict(t=10, b=40),
            height=350,
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_line, use_container_width=True)
        # A11Y-002 fix
        st.caption("折线图：展示学生每日提问次数随时间的变化趋势。")
    else:
        _render_empty_state("暂无趋势数据。")

    st.divider()

    # -----------------------------------------------------------------------
    # 问题分类统计 + 证据不足 & 高风险
    # -----------------------------------------------------------------------
    col_cat, col_risk = st.columns(2)

    with col_cat:
        _render_section_header("问题分类统计", "基于关键词匹配的自动分类")
        cat_stats = analytics.get_category_stats()
        if cat_stats:
            df_cat = pd.DataFrame(cat_stats)
            fig_cat = px.bar(
                df_cat, x="category", y="count",
                title="",
                labels={"category": "分类", "count": "提问次数"},
                color="count",
                color_continuous_scale="Purples",
            )
            fig_cat.update_layout(
                xaxis_tickangle=-45,
                margin=dict(t=10, b=40),
                coloraxis_showscale=False,
                height=380,
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            # A11Y-002 fix
            st.caption("柱状图：展示各问题分类的提问次数统计。")
        else:
            _render_empty_state("暂无分类数据。")

    with col_risk:
        _render_section_header("证据不足与高风险统计", "需要教师关注的特殊提问")

        # 证据不足
        insuf = analytics.get_evidence_insufficient_count()
        high_risk = risk_stats.get("high_risk_count", 0)

        fig_gauge = go.Figure()

        fig_gauge.add_trace(go.Indicator(
            mode="number",
            value=insuf,
            title={"text": "证据不足提问", "font": {"size": 14}},
            number={"font": {"size": 36, "color": _WARNING}},
            domain={"row": 0, "column": 0},
        ))

        fig_gauge.add_trace(go.Indicator(
            mode="number",
            value=high_risk,
            title={"text": "高风险方案", "font": {"size": 14}},
            number={"font": {"size": 36, "color": _DANGER}},
            domain={"row": 0, "column": 1},
        ))

        fig_gauge.update_layout(
            grid={"rows": 1, "columns": 2, "pattern": "independent"},
            margin=dict(t=40, b=20, l=40, r=40),
            height=200,
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        # A11Y-002 fix
        st.caption("指标卡：展示证据不足提问数和高风险方案数。")

        # 高风险问题详情
        if qa_count > 0:
            risk_total = risk_stats.get("total", 0)
            risk_pct = round(high_risk / risk_total * 100, 1) if risk_total > 0 else 0
            st.markdown(
                f"高风险占比: **{risk_pct}%** "
                f"({high_risk} / {risk_total} 条提问)"
            )
        else:
            _render_empty_state("暂无足够数据。")

    st.divider()

    # -----------------------------------------------------------------------
    # 薄弱点总结与课堂复习建议
    # -----------------------------------------------------------------------
    _render_section_header("薄弱知识点总结与复习建议",
                           "基于日志数据的规则化分析，帮助教师把握教学重点")

    summary = analytics.generate_weak_points_summary()

    wp_col, rs_col = st.columns(2)

    with wp_col:
        st.markdown("### 薄弱知识点")
        for i, point in enumerate(summary.get("weak_points", []), 1):
            st.markdown(f"{i}. {point}")

    with rs_col:
        st.markdown("### 课堂复习建议")
        for i, suggestion in enumerate(summary.get("review_suggestions", []), 1):
            st.markdown(f"{i}. {suggestion}")

    # -----------------------------------------------------------------------
    # VIS-003 fix: 使用 .smg-disclaimer 全局类，与其他页面一致
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">'
        f'{config.SAFETY_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
