"""
共享路径设置模块

所有需要将项目根目录加入 sys.path 的入口点（app.py、api_server.py、pages/*.py、
scripts/*.py）应使用此模块替代重复的三行样板代码。

使用方式:
    import core.path_setup  # noqa: F401 — 副作用导入，确保路径已设置
    # 或在需要显式调用的场景:
    from core import path_setup  # noqa: F401
"""

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PROJECT_ROOT_STR = str(_PROJECT_ROOT)

if _PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT_STR)
