"""
共享全局样式 - 所有页面统一导入

使用方式:
    import core.styles
    core.styles.apply()
"""

import streamlit as st

GLOBAL_CSS = """
<style>
/* ---- 全局字体与配色 ---- */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
}

:root {
    --smg-navy: #0f172a;
    --smg-slate: #1e293b;
    --smg-teal: #0d9488;
    --smg-teal-light: #14b8a6;
    --smg-teal-bg: #f0fdfa;
    --smg-amber: #d97706;
    --smg-red: #dc2626;
    --smg-green: #15803d;
    --smg-gray-50: #f8fafc;
    --smg-gray-100: #f1f5f9;
    --smg-gray-200: #e2e8f0;
    --smg-gray-400: #64748b;
    --smg-gray-600: #475569;
    --smg-gray-800: #1e293b;
    --smg-radius: 10px;
    --smg-shadow: 0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.06);
    --smg-shadow-md: 0 4px 6px rgba(15, 23, 42, 0.07), 0 2px 4px rgba(15, 23, 42, 0.06);
}

/* ---- 侧边栏 ---- */
[data-testid="stSidebar"] {
    background: #f8fafc;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] {
    color: #334155;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdown"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdown"] h3 {
    color: #0f172a;
}
[data-testid="stSidebar"] .stCaption {
    color: #64748b !important;
}
[data-testid="stSidebar"] code {
    background: #e2e8f0;
    color: #0d9488;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
}

/* ---- 侧边栏导航链接 ---- */
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    color: #0f172a !important;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.3rem 0;
    font-weight: 500;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    color: #0f172a !important;
    background: #e2e8f0;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] li > a[aria-selected="true"] {
    color: #ffffff !important;
    background: #0d9488;
    border: 1px solid #0d9488;
    font-weight: 600;
}

/* ---- 侧边栏所有文字 ---- */
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li,
[data-testid="stSidebar"] .stMarkdown span {
    color: #334155;
}

/* ---- 主内容区 ---- */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* ---- 状态卡片 ---- */
.smg-card {
    background: #ffffff;
    border: 1px solid var(--smg-gray-200);
    border-radius: var(--smg-radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--smg-shadow);
    transition: box-shadow 0.2s ease, transform 0.15s ease;
    height: 100%;
}
.smg-card:hover {
    box-shadow: var(--smg-shadow-md);
    transform: translateY(-1px);
}
.smg-card-label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--smg-gray-400);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.35rem;
}
.smg-card-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--smg-gray-800);
    line-height: 1.2;
}
.smg-card-value.online { color: var(--smg-green); }
.smg-card-value.offline { color: var(--smg-red); }

/* ---- Hero 区域 ---- */
.smg-hero {
    background: linear-gradient(135deg, var(--smg-navy) 0%, #1a2744 50%, #0c3d3d 100%);
    border-radius: 14px;
    padding: 2.5rem 3rem;
    color: #f1f5f9;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.smg-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(20, 184, 166, 0.12) 0%, transparent 70%);
    pointer-events: none;
}
.smg-hero h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0;
    color: #ffffff;
    letter-spacing: -0.02em;
}
.smg-hero p {
    font-size: 1.05rem;
    color: #94a3b8;
    margin: 0;
    line-height: 1.6;
}
.smg-hero .accent {
    color: var(--smg-teal-light);
    font-weight: 500;
}

/* ---- 分区标题 ---- */
h2.smg-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--smg-gray-800);
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--smg-teal);
    display: inline-block;
}

/* ---- 架构图 ---- */
.smg-arch-flow {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    justify-content: center;
    margin: 1.5rem 0;
}
.smg-arch-node {
    background: var(--smg-gray-50);
    border: 1.5px solid var(--smg-gray-200);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    text-align: center;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--smg-gray-800);
    min-width: 120px;
}
.smg-arch-node.highlight {
    border-color: var(--smg-teal);
    background: var(--smg-teal-bg);
    color: var(--smg-teal);
    font-weight: 600;
}
.smg-arch-arrow {
    color: var(--smg-gray-400);
    font-size: 1.2rem;
    padding: 0 0.4rem;
}

/* ---- 证据卡片 ---- */
.smg-evidence-card {
    background: #ffffff;
    border: 1px solid var(--smg-gray-200);
    border-left: 4px solid var(--smg-teal);
    border-radius: 0 var(--smg-radius) var(--smg-radius) 0;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: var(--smg-shadow);
}
.smg-evidence-card .ev-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}
.smg-evidence-card .ev-title {
    font-weight: 600;
    color: var(--smg-gray-800);
    font-size: 0.95rem;
}
.smg-evidence-card .ev-score {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--smg-teal);
    background: var(--smg-teal-bg);
    padding: 2px 8px;
    border-radius: 4px;
}
.smg-evidence-card .ev-meta {
    font-size: 0.8rem;
    color: var(--smg-gray-400);
    margin-bottom: 0.4rem;
}
.smg-evidence-card .ev-content {
    font-size: 0.88rem;
    color: var(--smg-gray-600);
    line-height: 1.6;
}

/* ---- 回答区块 ---- */
.smg-answer-block {
    background: #ffffff;
    border: 1px solid var(--smg-gray-200);
    border-radius: var(--smg-radius);
    padding: 1.5rem 2rem;
    box-shadow: var(--smg-shadow);
    margin-bottom: 1.5rem;
}
.smg-answer-block h1,
.smg-answer-block h2,
.smg-answer-block h3 {
    color: var(--smg-navy);
    border-bottom: 1px solid var(--smg-gray-200);
    padding-bottom: 0.4rem;
}

/* ---- 设置页面表单 ---- */
.smg-settings-group {
    background: #ffffff;
    border: 1px solid var(--smg-gray-200);
    border-radius: var(--smg-radius);
    padding: 1.5rem 2rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--smg-shadow);
}
.smg-settings-group h3 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--smg-gray-800);
    margin: 0 0 1rem 0;
}

/* ---- 安全声明 ---- */
.smg-disclaimer {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: var(--smg-radius);
    padding: 1rem 1.5rem;
    margin-top: 2rem;
    font-size: 0.85rem;
    color: #92400e;
    line-height: 1.7;
}
.smg-disclaimer::before {
    content: '';
    display: inline-block;
    width: 0;
    height: 0;
}

/* ---- 置信度标签 ---- */
.smg-confidence-high {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.82rem;
    font-weight: 600;
}
.smg-confidence-low {
    display: inline-block;
    background: #fef3c7;
    color: #92400e;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.82rem;
    font-weight: 600;
}

/* ---- Streamlit metric 覆写 ---- */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--smg-gray-200);
    border-radius: var(--smg-radius);
    padding: 1rem 1.25rem;
    box-shadow: var(--smg-shadow);
}
[data-testid="stMetric"] label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--smg-gray-400) !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-weight: 700 !important;
    color: var(--smg-gray-800) !important;
}

/* ---- 隐藏 Streamlit 默认页脚 ---- */
footer {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}

/* ---- 空状态 ---- */
.smg-empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--smg-gray-400);
}
.smg-empty-state p {
    font-size: 1rem;
    margin: 0;
}

/* ---- 测试结果块 ---- */
.smg-test-result {
    background: var(--smg-gray-50);
    border: 1px solid var(--smg-gray-200);
    border-radius: var(--smg-radius);
    padding: 1rem 1.25rem;
    margin-top: 0.75rem;
}
.smg-test-result strong {
    color: var(--smg-gray-800);
}
</style>
"""


def apply():
    """应用全局样式到当前页面。"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
