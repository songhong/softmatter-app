"""
Ollama / 公开 LLM 调用客户端模块

封装与 Ollama 服务的 HTTP 通信，包括：
- 连接状态检测
- 模型列表获取（/api/tags）
- 当前模型持久化（settings.json 读写）
- 模型可用性测试
- 文本生成调用

设计原则：
- 所有 Ollama 通信失败时返回友好错误，不导致应用崩溃
- 模型状态来自真实 Ollama 服务，不硬编码虚假在线状态
- 内部异常细节记录到日志，不泄露给调用者
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
_REQUEST_TIMEOUT = 30
_STATUS_CHECK_TIMEOUT = 5
_LIST_MODELS_TIMEOUT = 5
_TEST_TIMEOUT = 10
_SETTINGS_PATH: Path = config.SETTINGS_JSON

# ---------------------------------------------------------------------------
# 状态检查 TTL 缓存（避免 Ollama 离线时每次请求阻塞 5 秒）
# ---------------------------------------------------------------------------
_STATUS_CACHE_TTL = 30  # 秒
_status_cache: dict[str, Any] = {"result": None, "timestamp": 0.0}


# ---------------------------------------------------------------------------
# 数据类
# ---------------------------------------------------------------------------
@dataclass
class OllamaStatus:
    """Ollama 服务连接检测结果。"""
    online: bool = False
    model_count: int = 0
    message: str = ""


@dataclass
class LLMResponse:
    """LLM 调用响应。"""
    content: str = ""
    model: str = ""
    success: bool = False
    error: str = ""


@dataclass
class ModelTestResult:
    """模型测试结果。"""
    success: bool = False
    model: str = ""
    message: str = ""
    latency_ms: int = 0


# ---------------------------------------------------------------------------
# Settings 读写
# ---------------------------------------------------------------------------
def _read_settings() -> dict[str, Any]:
    """读取 settings.json，返回字典。文件不存在或损坏时返回空字典。"""
    try:
        if _SETTINGS_PATH.exists():
            return json.loads(_SETTINGS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("读取 settings.json 失败: %s", exc)
    return {}


def _write_settings(settings: dict[str, Any]) -> bool:
    """写入 settings.json，成功返回 True。"""
    try:
        _SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        _SETTINGS_PATH.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return True
    except OSError as exc:
        logger.error("写入 settings.json 失败: %s", exc)
        return False


# ---------------------------------------------------------------------------
# Ollama 地址获取
# ---------------------------------------------------------------------------
def get_ollama_url() -> str:
    """获取 Ollama 服务地址。

    优先级：settings.json > 环境变量(config.OLLAMA_BASE_URL)
    """
    settings = _read_settings()
    return settings.get("ollama_url") or config.OLLAMA_BASE_URL


# ---------------------------------------------------------------------------
# 连接检测
# ---------------------------------------------------------------------------
def check_ollama_status() -> OllamaStatus:
    """检测 Ollama 服务是否在线，并返回模型数量。

    结果在 _STATUS_CACHE_TTL 秒内缓存，避免 Ollama 离线时反复阻塞。

    Returns:
        OllamaStatus 包含在线状态、模型数量和友好提示。
    """
    import time

    now = time.monotonic()
    if _status_cache["result"] is not None and now - _status_cache["timestamp"] < _STATUS_CACHE_TTL:
        return _status_cache["result"]

    def _cache_and_return(status: OllamaStatus) -> OllamaStatus:
        _status_cache["result"] = status
        _status_cache["timestamp"] = time.monotonic()
        return status

    url = get_ollama_url()
    try:
        resp = requests.get(f"{url}/api/tags", timeout=_STATUS_CHECK_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            models = data.get("models", [])
            count = len(models)
            return _cache_and_return(OllamaStatus(
                online=True,
                model_count=count,
                message=f"Ollama 服务在线，已安装 {count} 个模型。",
            ))
        return _cache_and_return(OllamaStatus(
            online=False,
            message=f"Ollama 返回异常状态码 {resp.status_code}，请检查服务是否正常运行。",
        ))
    except requests.ConnectionError as exc:
        logger.error("check_ollama_status 连接失败: %s | URL: %s", exc, url)
        return _cache_and_return(OllamaStatus(
            online=False,
            message=f"无法连接 Ollama 服务（{url}），请确认 Ollama 已启动且地址正确。",
        ))
    except requests.Timeout:
        return _cache_and_return(OllamaStatus(
            online=False,
            message="连接 Ollama 服务超时，请检查网络或服务状态。",
        ))
    except requests.RequestException:
        return _cache_and_return(OllamaStatus(
            online=False,
            message="检测 Ollama 服务时发生未知错误，请稍后重试。",
        ))


# ---------------------------------------------------------------------------
# 模型列表
# ---------------------------------------------------------------------------
def list_models() -> tuple[list[dict[str, Any]], str]:
    """获取 Ollama 已安装模型列表。

    Returns:
        (models, error) 元组。成功时 models 为模型字典列表，error 为空字符串；
        失败时 models 为空列表，error 为友好错误信息。
    """
    url = get_ollama_url()
    try:
        resp = requests.get(f"{url}/api/tags", timeout=_LIST_MODELS_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            raw_models = data.get("models", [])
            # 标准化输出格式
            models = []
            for m in raw_models:
                models.append({
                    "name": m.get("name", ""),
                    "size": m.get("size", 0),
                    "modified_at": m.get("modified_at", ""),
                    "details": m.get("details", {}),
                })
            return models, ""
        return [], f"Ollama 返回异常状态码 {resp.status_code}。"
    except requests.ConnectionError as exc:
        logger.error("连接 Ollama 失败: %s | URL: %s", exc, url)
        return [], f"无法连接 Ollama 服务（{url}），请确认 Ollama 已启动。"
    except requests.Timeout:
        return [], "连接 Ollama 服务超时，请检查网络。"
    except requests.RequestException as exc:
        logger.error("获取模型列表失败: %s", exc)
        return [], "获取模型列表时发生错误，请稍后重试。"


# ---------------------------------------------------------------------------
# 当前模型管理
# ---------------------------------------------------------------------------
def get_current_model() -> str:
    """获取当前选择的模型名称。

    优先级：settings.json > config.DEFAULT_MODEL
    """
    settings = _read_settings()
    return settings.get("current_model") or config.DEFAULT_MODEL


def set_current_model(model_name: str) -> tuple[bool, str]:
    """设置当前模型并持久化到 settings.json。

    Args:
        model_name: 模型名称，如 "qwen2.5:7b"。

    Returns:
        (success, message) 元组。
    """
    if not model_name or not model_name.strip():
        return False, "模型名称不能为空。"

    model_name = model_name.strip()
    settings = _read_settings()
    settings["current_model"] = model_name
    if _write_settings(settings):
        logger.info("当前模型已设置为: %s", model_name)
        return True, f"当前模型已设置为 {model_name}。"
    return False, "保存模型设置失败，请检查文件权限。"


def set_ollama_url(url: str) -> tuple[bool, str]:
    """设置 Ollama 服务地址并持久化到 settings.json。

    Args:
        url: Ollama 服务地址，如 "http://localhost:11434"。

    Returns:
        (success, message) 元组。
    """
    if not url or not url.strip():
        return False, "Ollama 地址不能为空。"

    url = url.strip().rstrip("/")
    # 基本格式校验
    if not url.startswith(("http://", "https://")):
        return False, "Ollama 地址必须以 http:// 或 https:// 开头。"

    settings = _read_settings()
    settings["ollama_url"] = url
    if _write_settings(settings):
        logger.info("Ollama 地址已设置为: %s", url)
        return True, f"Ollama 地址已设置为 {url}。"
    return False, "保存 Ollama 地址失败，请检查文件权限。"


# ---------------------------------------------------------------------------
# 模型测试
# ---------------------------------------------------------------------------
def test_model(model_name: str | None = None) -> ModelTestResult:
    """测试指定模型是否可用。

    向 Ollama 发送一条简短测试 prompt，验证模型可正常响应。

    Args:
        model_name: 要测试的模型名称。为 None 时使用当前模型。

    Returns:
        ModelTestResult 包含测试状态、模型名和提示信息。
    """
    if model_name is None:
        model_name = get_current_model()

    url = get_ollama_url()
    payload = {
        "model": model_name,
        "prompt": "你好，请用一句话介绍你自己。",
        "stream": False,
    }

    try:
        resp = requests.post(
            f"{url}/api/generate",
            json=payload,
            timeout=_TEST_TIMEOUT,
        )
        if resp.status_code == 200:
            data = resp.json()
            response_text = data.get("response", "").strip()
            if response_text:
                total_ns = data.get("total_duration", 0)
                latency_ms = total_ns // 1_000_000 if total_ns else 0
                return ModelTestResult(
                    success=True,
                    model=model_name,
                    message=f"模型 {model_name} 响应正常。",
                    latency_ms=latency_ms,
                )
            return ModelTestResult(
                success=False,
                model=model_name,
                message=f"模型 {model_name} 返回了空响应，请检查模型是否完整下载。",
            )
        elif resp.status_code == 404:
            return ModelTestResult(
                success=False,
                model=model_name,
                message=f"模型 {model_name} 未找到，请先通过 ollama pull {model_name} 下载。",
            )
        else:
            return ModelTestResult(
                success=False,
                model=model_name,
                message=f"模型测试失败（状态码 {resp.status_code}），请检查 Ollama 服务状态。",
            )
    except requests.ConnectionError:
        return ModelTestResult(
            success=False,
            model=model_name,
            message="无法连接 Ollama 服务，请确认 Ollama 已启动。",
        )
    except requests.Timeout:
        return ModelTestResult(
            success=False,
            model=model_name,
            message=f"模型 {model_name} 测试超时，模型可能正在加载中，请稍后重试。",
        )
    except requests.RequestException as exc:
        logger.error("模型测试失败: %s", exc)
        return ModelTestResult(
            success=False,
            model=model_name,
            message="模型测试时发生错误，请稍后重试。",
        )


# ---------------------------------------------------------------------------
# 文本生成
# ---------------------------------------------------------------------------
def generate(
    prompt: str,
    model: str | None = None,
    system: str = "",
) -> LLMResponse:
    """调用 Ollama 生成文本。

    Args:
        prompt: 用户输入的 prompt。
        model: 模型名称，None 时使用当前选择的模型。
        system: 系统 prompt（可选）。

    Returns:
        LLMResponse 包含生成内容或友好错误信息。
    """
    if not prompt or not prompt.strip():
        return LLMResponse(error="输入内容不能为空。")

    if model is None:
        model = get_current_model()

    url = get_ollama_url()
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system

    try:
        resp = requests.post(
            f"{url}/api/generate",
            json=payload,
            timeout=_REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            data = resp.json()
            return LLMResponse(
                content=data.get("response", ""),
                model=data.get("model", model),
                success=True,
            )
        elif resp.status_code == 404:
            return LLMResponse(
                error=f"模型 {model} 未找到，请在系统设置中选择可用模型。",
            )
        else:
            logger.error("Ollama 返回状态码 %d", resp.status_code)
            return LLMResponse(error="模型服务响应异常，请稍后重试。")
    except requests.ConnectionError:
        return LLMResponse(
            error="无法连接模型服务，请确认 Ollama 已启动并在系统设置中检查服务地址。",
        )
    except requests.Timeout:
        return LLMResponse(error="模型响应超时，请稍后重试或尝试更小的输入。")
    except requests.RequestException as exc:
        logger.error("LLM 调用失败: %s", exc)
        return LLMResponse(error="模型服务暂时不可用，请稍后重试或检查 Ollama 服务状态。")
