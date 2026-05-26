"""
logger - qa_logger 的兼容别名模块。

原始模块命名为 qa_logger 以避免与标准库 logging.getLogger 冲突。
本文件仅做 re-export，保持向后兼容。
"""

from core.qa_logger import (  # noqa: F401
    extract_keywords,
    log_feedback,
    log_qa,
)
