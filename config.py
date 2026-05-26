"""
SoftMatterGPT 全局配置

所有可调参数集中于此，前端和后端共享。
敏感信息（API Key 等）通过环境变量读取，不硬编码。
"""

import os
import secrets
from pathlib import Path

# ---------------------------------------------------------------------------
# 项目根目录
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 数据目录
# ---------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"
DOCS_DIR = PROJECT_ROOT / "docs"

# ---------------------------------------------------------------------------
# 数据文件路径
# ---------------------------------------------------------------------------
KNOWLEDGE_CSV = DATA_DIR / "softmatter_knowledge.csv"
LITERATURE_CSV = DATA_DIR / "literature_records.csv"
RECIPES_CSV = DATA_DIR / "experiment_recipes.csv"
SAMPLE_QUESTIONS_CSV = DATA_DIR / "sample_questions.csv"
FEEDBACK_CSV = DATA_DIR / "feedback.csv"
SETTINGS_JSON = DATA_DIR / "settings.json"
QA_HISTORY_CSV = LOGS_DIR / "qa_history.csv"

# ---------------------------------------------------------------------------
# Ollama 配置
# ---------------------------------------------------------------------------
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen2.5:7b")

# ---------------------------------------------------------------------------
# RAG 检索配置
# ---------------------------------------------------------------------------
TOP_K = int(os.getenv("TOP_K", "5"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))

# ---------------------------------------------------------------------------
# FastAPI 后端配置
# ---------------------------------------------------------------------------
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

# ---------------------------------------------------------------------------
# Streamlit 前端配置
# ---------------------------------------------------------------------------
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))

# ---------------------------------------------------------------------------
# API 认证配置
# ---------------------------------------------------------------------------
_env_key = os.getenv("SOFTMATTER_API_KEY")
if not _env_key:
    _env_key = secrets.token_urlsafe(32)
    print(f"[WARNING] SOFTMATTER_API_KEY 未设置，已生成随机密钥: {_env_key}")
    print("[WARNING] 请将此密钥设置为环境变量 SOFTMATTER_API_KEY 以保持稳定。")
API_KEY = _env_key

# ---------------------------------------------------------------------------
# 安全配置
# ---------------------------------------------------------------------------
HIGH_RISK_KEYWORDS = [
    "强酸", "强碱", "浓硫酸", "浓硝酸", "氢氟酸",
    "高压", "真空", "液氮", "有机溶剂",
    "致癌", "剧毒", "易燃易爆",
]

SAFETY_DISCLAIMER = (
    "本系统输出的教学版实验方案仅供参考，不构成可直接执行的实验操作 SOP。"
    "具体试剂选择、浓度、温度、时间和操作条件必须经教师或实验室安全规范审核后方可实施。"
)
