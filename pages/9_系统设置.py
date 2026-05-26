"""
系统设置页面

Ollama 模型检测、刷新、选择和测试。
所有状态数据来自真实 Ollama 服务，不伪造在线状态。
设置变更持久化到 data/settings.json。
"""

import core.path_setup  # noqa: F401

import streamlit as st
import config
from core import llm_client


def main():
    st.markdown(
        '<div class="smg-hero">'
        '<h1>系统设置</h1>'
        '<p>Ollama 服务检测、<span class="accent">模型管理</span>与连接测试</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ===================================================================
    # 第一部分: Ollama 服务连接
    # ===================================================================
    st.markdown('<h2 class="smg-section-title">Ollama 服务连接</h2>', unsafe_allow_html=True)

    # 读取当前地址（优先 settings.json，其次环境变量）
    current_url = llm_client.get_ollama_url()

    # 可编辑的地址输入
    col_url, col_btn_detect, col_btn_save = st.columns([3, 1, 1])
    with col_url:
        ollama_url_input = st.text_input(
            "Ollama 服务地址",
            value=current_url,
            help="默认为 http://localhost:11434，如有自定义部署请修改此处。",
        )
    with col_btn_detect:
        st.markdown('<div style="padding-top: 1.65rem;">', unsafe_allow_html=True)
        detect_clicked = st.button("检测连接", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_btn_save:
        st.markdown('<div style="padding-top: 1.65rem;">', unsafe_allow_html=True)
        save_url_clicked = st.button("保存地址", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 检测连接
    if detect_clicked:
        with st.spinner("正在检测 Ollama 服务连接..."):
            status = llm_client.check_ollama_status()
        if status.online:
            st.success(f"{status.message}")
        else:
            st.error(f"{status.message}")

    # 保存地址
    if save_url_clicked:
        url_clean = ollama_url_input.strip().rstrip("/")
        if not url_clean:
            st.error("Ollama 地址不能为空。")
        elif not url_clean.startswith(("http://", "https://")):
            st.error("Ollama 地址必须以 http:// 或 https:// 开头。")
        else:
            ok, msg = llm_client.set_ollama_url(url_clean)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    # 显示当前连接状态概要
    status = llm_client.check_ollama_status()
    if status.online:
        st.info(f"当前状态: **在线** -- {status.message}")
    else:
        st.warning(f"当前状态: **离线** -- {status.message}")

    st.markdown("")

    # ===================================================================
    # 第二部分: 模型管理
    # ===================================================================
    st.markdown('<h2 class="smg-section-title">模型管理</h2>', unsafe_allow_html=True)

    current_model = llm_client.get_current_model()
    st.markdown(
        f"当前使用模型: **`{current_model}`**"
    )

    col_refresh, col_space = st.columns([1, 3])
    with col_refresh:
        refresh_clicked = st.button("刷新本地模型列表", use_container_width=True)

    # 初始化 session state
    if "available_models" not in st.session_state:
        st.session_state["available_models"] = []

    if refresh_clicked:
        with st.spinner("正在从 Ollama 获取已安装模型..."):
            models, error = llm_client.list_models()
        if error:
            st.error(error)
            st.session_state["available_models"] = []
        elif not models:
            st.warning("未找到已安装模型，请先使用 `ollama pull <模型名>` 下载模型。")
            st.session_state["available_models"] = []
        else:
            st.session_state["available_models"] = models
            st.success(f"找到 {len(models)} 个已安装模型。")

    # 模型列表与选择
    available = st.session_state.get("available_models", [])
    if available:
        model_names = [m.get("name", "unknown") for m in available]

        # 显示模型表格
        with st.expander("查看已安装模型详情", expanded=True):
            for m in available:
                name = m.get("name", "unknown")
                size_bytes = m.get("size", 0)
                size_mb = size_bytes / (1024 * 1024)
                modified = m.get("modified_at", "")[:19] if m.get("modified_at") else ""
                details = m.get("details", {})
                family = details.get("family", "")
                param_size = details.get("parameter_size", "")

                parts = [f"**{name}**"]
                if size_mb > 0:
                    parts.append(f"{size_mb:.0f} MB")
                if family:
                    parts.append(family)
                if param_size:
                    parts.append(param_size)
                if modified:
                    parts.append(modified)
                st.markdown(" &nbsp;|&nbsp; ".join(parts))

        # 选择并设置模型
        selected = st.selectbox(
            "选择模型",
            model_names,
            index=model_names.index(current_model) if current_model in model_names else 0,
        )

        col_set, col_test = st.columns(2)
        with col_set:
            if st.button("设为当前模型", type="primary", use_container_width=True):
                ok, msg = llm_client.set_current_model(selected)
                if ok:
                    st.success(f"已将当前模型设为: **{selected}**（已持久化到 settings.json）")
                    st.rerun()
                else:
                    st.error(msg)
        with col_test:
            if st.button("测试当前模型", use_container_width=True):
                with st.spinner(f"正在测试模型 {current_model}..."):
                    result = llm_client.test_model()
                if result.success:
                    st.markdown(
                        f'<div class="smg-test-result">'
                        f'<strong>测试通过</strong><br>'
                        f'模型: {result.model}<br>'
                        f'延迟: {result.latency_ms} ms<br>'
                        f'{result.message}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.error(f"测试失败: {result.message}")
    else:
        st.markdown(
            """
            <div class="smg-empty-state">
                <p>点击「刷新本地模型列表」获取已安装的 Ollama 模型。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ===================================================================
    # 第三部分: 快速测试
    # ===================================================================
    st.markdown('<h2 class="smg-section-title">快速测试</h2>', unsafe_allow_html=True)

    test_prompt = st.text_input(
        "测试 Prompt",
        value="请用一句话介绍软物质科学。",
        help="输入任意文本，测试当前模型是否能正常响应。",
    )

    if st.button("发送测试请求", disabled=not test_prompt.strip(), use_container_width=True):
        with st.spinner("正在调用模型..."):
            response = llm_client.generate(prompt=test_prompt.strip())

        if response.success:
            st.markdown(f"**模型响应** ({response.model})")
            st.markdown(response.content)
        else:
            st.error(f"调用失败: {response.error}")

    # -----------------------------------------------------------------------
    # 安全声明
    # -----------------------------------------------------------------------
    st.markdown(
        f'<div class="smg-disclaimer">{config.SAFETY_DISCLAIMER}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
