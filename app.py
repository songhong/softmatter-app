"""
SoftMatterGPT - Streamlit 前端入口

面向软物质课程与实验教学的 AI 教学工作台。
运行方式:
    streamlit run app.py
"""

import core.path_setup  # noqa: F401 -- 确保项目根目录在 sys.path 中

import streamlit as st

import config
import core.styles; core.styles.apply()


# ---------------------------------------------------------------------------
# 页面配置（必须在最顶部，任何 st 调用之前）
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="SoftMatterGPT",
    page_icon=":material/science:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# 侧边栏
# ---------------------------------------------------------------------------

def _render_sidebar():
    """渲染侧边栏导航与信息。"""
    with st.sidebar:
        st.markdown(
            '<div style="padding: 0.5rem 0 0.25rem 0;">'
            '<span style="font-size:1.5rem; font-weight:700; color:#f1f5f9; '
            'letter-spacing:-0.02em;">SoftMatterGPT</span></div>',
            unsafe_allow_html=True,
        )
        st.caption("面向软物质课程与实验教学的 AI 教学工作台")

        st.markdown("---")

        # 模型状态（真实读取，不伪造）
        try:
            from core import llm_client
            current_model = llm_client.get_current_model()
            ollama_url = llm_client.get_ollama_url()
            status = llm_client.check_ollama_status()
            ollama_label = "在线" if status.online else "离线"
        except Exception:
            current_model = config.DEFAULT_MODEL
            ollama_url = config.OLLAMA_BASE_URL
            ollama_label = "未知"

        st.markdown(
            f"**当前模型**\n`{current_model}`\n\n"
            f"**Ollama 服务**\n`{ollama_url}`\n\n"
            f"**连接状态**: {ollama_label}"
        )

        st.markdown("---")
        st.markdown(
            '<div style="font-size:0.78rem; color:#cbd5e1; line-height:1.6;">'
            f'{config.SAFETY_DISCLAIMER}</div>',
            unsafe_allow_html=True,
        )


_render_sidebar()


# ---------------------------------------------------------------------------
# 主页内容
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="smg-hero">
        <h1>SoftMatterGPT</h1>
        <p>
            面向软物质课程与实验教学的 <span class="accent">AI 教学工作台</span> --<br>
            基于 RAG 检索增强生成，支持课程问答、文献挖掘、实验方案与教师分析。
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "请使用左侧导航栏进入各功能页面。首次使用建议先前往 **系统设置** 页面检测 Ollama 服务连接状态。"
)
