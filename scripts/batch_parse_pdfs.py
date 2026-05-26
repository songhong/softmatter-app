"""
PDF 批量解析脚本

功能：
- 扫描 data/pdfs/ 目录下的 PDF 文件
- 尝试提取文本（使用 PyPDF2 / pdfplumber，可选依赖）
- 将抽取结果保存到 literature_records.csv 和 experiment_recipes.csv
- 记录解析失败的文件到 logs/pdf_parse_errors.csv
- 输出处理统计

使用方式：
    python scripts/batch_parse_pdfs.py [--pdf-dir PATH] [--dry-run]

注意：
    PDF 解析需要安装 PyPDF2 或 pdfplumber（可选）。
    未安装时脚本仅扫描并记录文件列表，不实际解析。
"""

import argparse
import csv
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# 确保项目根目录在 sys.path 中（脚本可直接 python scripts/xxx.py 运行）
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from core import literature_processor, recipe_extractor

logger = logging.getLogger("batch_parse_pdfs")

# ---------------------------------------------------------------------------
# PDF 解析依赖（可选）
# ---------------------------------------------------------------------------
_PDF_BACKEND = None

try:
    import pdfplumber  # type: ignore[import-untyped]
    _PDF_BACKEND = "pdfplumber"
except ImportError:
    pass

if _PDF_BACKEND is None:
    try:
        import PyPDF2  # type: ignore[import-untyped]
        _PDF_BACKEND = "PyPDF2"
    except ImportError:
        pass


def extract_text_from_pdf(pdf_path: Path) -> str:
    """从 PDF 文件提取全文文本。

    Returns:
        提取的文本内容。

    Raises:
        RuntimeError: 没有可用的 PDF 解析库。
        Exception: PDF 解析失败。
    """
    if _PDF_BACKEND is None:
        raise RuntimeError(
            "未安装 PDF 解析库。请安装 pdfplumber 或 PyPDF2：\n"
            "  pip install pdfplumber\n"
            "  pip install PyPDF2"
        )

    if _PDF_BACKEND == "pdfplumber":
        texts = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
        return "\n\n".join(texts)

    if _PDF_BACKEND == "PyPDF2":
        texts = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
        return "\n\n".join(texts)

    raise RuntimeError("未知的 PDF 后端")


def identify_sections(text: str) -> dict:
    """从全文中粗略识别章节（Abstract / Experimental / Results）。

    Returns:
        {"abstract": str, "experimental": str, "results": str, "full": str}
    """
    sections = {"abstract": "", "experimental": "", "results": "", "full": text}
    text_lower = text.lower()

    # 提取 Abstract
    for marker in ["abstract", "摘要"]:
        idx = text_lower.find(marker)
        if idx >= 0:
            # 取 marker 之后到下一个常见章节标题之间的文本
            end_markers = ["introduction", "1.", "keywords", "引言", "experimental",
                           "materials and methods", "results"]
            end_idx = len(text)
            for em in end_markers:
                ei = text_lower.find(em, idx + len(marker) + 10)
                if 0 < ei < end_idx:
                    end_idx = ei
            sections["abstract"] = text[idx:end_idx].strip()[:2000]
            break

    # 提取 Experimental Section
    for marker in ["experimental section", "experimental",
                   "materials and methods", "实验部分", "实验方法"]:
        idx = text_lower.find(marker)
        if idx >= 0:
            end_markers = ["results and discussion", "results",
                           "conclusion", "references", "结论"]
            end_idx = len(text)
            for em in end_markers:
                ei = text_lower.find(em, idx + len(marker) + 10)
                if 0 < ei < end_idx:
                    end_idx = ei
            sections["experimental"] = text[idx:end_idx].strip()[:3000]
            break

    # 提取 Results and Discussion
    for marker in ["results and discussion", "results", "结果与讨论", "结果"]:
        idx = text_lower.find(marker)
        if idx >= 0:
            end_markers = ["conclusion", "references", "acknowledgment",
                           "参考文献", "结论"]
            end_idx = len(text)
            for em in end_markers:
                ei = text_lower.find(em, idx + len(marker) + 10)
                if 0 < ei < end_idx:
                    end_idx = ei
            sections["results"] = text[idx:end_idx].strip()[:3000]
            break

    return sections


def extract_title_from_text(text: str) -> str:
    """尝试从 PDF 文本开头提取标题（启发式）。"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # 通常标题是前几行中最长的非空行
    candidates = []
    for line in lines[:10]:
        # 跳过过短或纯数字/符号行
        if len(line) < 5:
            continue
        if line[0].isdigit() and "." in line[:3]:
            continue
        # 跳过常见非标题行
        skip_words = ["journal", "doi", "http", "www.", "volume", "issue",
                       "received", "accepted", "published", "copyright",
                       "article", "communication", "letter"]
        if any(w in line.lower() for w in skip_words):
            continue
        candidates.append(line)
    if candidates:
        # 取最长的候选行作为标题
        return max(candidates, key=len)[:300]
    return ""


def parse_single_pdf(pdf_path: Path) -> dict:
    """解析单个 PDF 文件，返回结构化结果。

    Returns:
        {
            "title": str,
            "year": str,
            "abstract": str,
            "experimental": str,
            "results": str,
            "full_text_length": int,
        }
    """
    text = extract_text_from_pdf(pdf_path)
    sections = identify_sections(text)
    title = extract_title_from_text(text)

    # 尝试从文件名提取年份
    year = ""
    fname = pdf_path.stem
    import re
    m = re.search(r"(20\d{2})", fname)
    if m:
        year = m.group(1)

    return {
        "title": title,
        "year": year,
        "source": f"PDF:{pdf_path.name}",
        "material_system": "",
        "method": "",
        "characterization": "",
        "result_summary": sections["results"][:500] if sections["results"] else "",
        "keywords": "",
        "abstract": sections["abstract"],
        "experimental": sections["experimental"],
        "full_text_length": len(text),
    }


# ---------------------------------------------------------------------------
# 错误日志
# ---------------------------------------------------------------------------
ERROR_LOG_COLUMNS = [
    "timestamp", "file_name", "file_path", "error_type", "error_message",
    "pdf_backend",
]

ERROR_LOG_PATH = config.LOGS_DIR / "pdf_parse_errors.csv"


def _init_error_log():
    """确保错误日志文件存在且包含表头。"""
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not ERROR_LOG_PATH.exists():
        with open(ERROR_LOG_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(ERROR_LOG_COLUMNS)


def log_error(file_name: str, file_path: str, error_type: str, error_msg: str):
    """记录一条解析错误到 csv。"""
    _init_error_log()
    with open(ERROR_LOG_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            file_name,
            file_path,
            error_type,
            error_msg,
            _PDF_BACKEND or "none",
        ])


# ---------------------------------------------------------------------------
# 统计
# ---------------------------------------------------------------------------
def get_pdf_stats() -> dict:
    """返回 PDF 处理统计（基于实际存在的文件和日志）。

    不虚构数据，仅报告可验证的数量。
    """
    pdf_dir = config.PROJECT_ROOT / "data" / "pdfs"
    pdf_files = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []

    error_count = 0
    if ERROR_LOG_PATH.exists():
        try:
            err_df = pd.read_csv(ERROR_LOG_PATH, encoding="utf-8-sig")
            error_count = len(err_df)
        except Exception:
            error_count = 0

    lit_stats = literature_processor.get_stats()
    recipe_stats = recipe_extractor.get_stats()

    return {
        "pdf_dir": str(pdf_dir),
        "pdf_dir_exists": pdf_dir.exists(),
        "pdf_file_count": len(pdf_files),
        "pdf_files": [f.name for f in pdf_files[:10]],  # 最多展示10个
        "parse_errors": error_count,
        "pdf_backend": _PDF_BACKEND or "not_installed",
        "literature_total": lit_stats["total"],
        "recipe_total": recipe_stats["total"],
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def batch_parse(
    pdf_dir: Path | None = None,
    dry_run: bool = False,
    save_results: bool = True,
) -> dict:
    """批量解析 PDF 文件。

    Args:
        pdf_dir: PDF 目录，默认为 data/pdfs/。
        dry_run: 仅扫描不解析。
        save_results: 是否将结果写入 CSV。

    Returns:
        {
            "total": int,
            "success": int,
            "failed": int,
            "skipped": int,
            "errors": list[dict],
            "pdf_backend": str,
        }
    """
    if pdf_dir is None:
        pdf_dir = config.PROJECT_ROOT / "data" / "pdfs"

    if not pdf_dir.exists():
        pdf_dir.mkdir(parents=True, exist_ok=True)
        logger.info("已创建 PDF 目录: %s", pdf_dir)

    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    total = len(pdf_files)

    result = {
        "total": total,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "errors": [],
        "pdf_backend": _PDF_BACKEND or "not_installed",
    }

    if total == 0:
        logger.info("data/pdfs/ 目录下未找到 PDF 文件。")
        print("data/pdfs/ 目录下未找到 PDF 文件。请将 PDF 放入此目录。")
        return result

    if dry_run:
        print(f"[dry-run] 找到 {total} 个 PDF 文件:")
        for f in pdf_files:
            print(f"  - {f.name}")
        result["skipped"] = total
        return result

    if _PDF_BACKEND is None:
        logger.warning(
            "未安装 PDF 解析库，仅记录文件列表。"
            "请安装 pdfplumber: pip install pdfplumber"
        )
        print("警告: 未安装 PDF 解析库（pdfplumber / PyPDF2）。")
        print("将仅记录文件列表，不进行实际解析。")
        print(f"共找到 {total} 个 PDF 文件。")
        for f in pdf_files:
            log_error(f.name, str(f), "MISSING_DEPENDENCY", "未安装 PDF 解析库")
            result["errors"].append({"file": f.name, "error": "未安装 PDF 解析库"})
        result["failed"] = total
        return result

    print(f"使用 {_PDF_BACKEND} 解析 {total} 个 PDF 文件...")
    start_time = time.time()

    for i, pdf_path in enumerate(pdf_files, 1):
        try:
            parsed = parse_single_pdf(pdf_path)
            print(f"  [{i}/{total}] 成功: {pdf_path.name} "
                  f"(标题: {parsed['title'][:50]}..., "
                  f"文本长度: {parsed['full_text_length']})")

            if save_results and parsed["title"]:
                # 添加到文献记录
                lit_row = {k: parsed.get(k, "") for k in [
                    "title", "year", "source", "material_system",
                    "method", "characterization", "result_summary", "keywords",
                ]}
                lit_row["data_source"] = f"pdf:{pdf_path.name}"
                literature_processor.import_from_csv  # 确保模块已加载
                # 直接合并单条记录
                import pandas as pd
                df = literature_processor._ensure_loaded().copy()
                new_id = literature_processor._next_id(df)
                lit_row["id"] = new_id
                for col in literature_processor.LITERATURE_COLUMNS:
                    if col not in lit_row:
                        lit_row[col] = ""
                df = pd.concat([df, pd.DataFrame([lit_row])], ignore_index=True)
                df.to_csv(config.LITERATURE_CSV, index=False, encoding="utf-8-sig")
                literature_processor._literature_df = df

            result["success"] += 1

        except Exception as exc:
            error_type = type(exc).__name__
            error_msg = str(exc)[:500]
            print(f"  [{i}/{total}] 失败: {pdf_path.name} - {error_type}: {error_msg}")
            log_error(pdf_path.name, str(pdf_path), error_type, error_msg)
            result["errors"].append({
                "file": pdf_path.name,
                "error_type": error_type,
                "error": error_msg,
            })
            result["failed"] += 1

    elapsed = time.time() - start_time
    print(f"\n处理完成: 成功 {result['success']}, 失败 {result['failed']}, "
          f"耗时 {elapsed:.1f} 秒")
    print(f"错误日志: {ERROR_LOG_PATH}")

    return result


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="SoftMatterGPT PDF 批量解析")
    parser.add_argument(
        "--pdf-dir", type=str, default=None,
        help="PDF 文件目录，默认 data/pdfs/",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="仅扫描文件，不实际解析",
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="仅显示统计信息",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    if args.stats:
        stats = get_pdf_stats()
        print("=== PDF 处理统计 ===")
        print(f"PDF 目录: {stats['pdf_dir']}")
        print(f"目录存在: {stats['pdf_dir_exists']}")
        print(f"PDF 文件数: {stats['pdf_file_count']}")
        print(f"解析后端: {stats['pdf_backend']}")
        print(f"解析错误数: {stats['parse_errors']}")
        print(f"文献记录总数: {stats['literature_total']}")
        print(f"配方记录总数: {stats['recipe_total']}")
        if stats["pdf_files"]:
            print(f"PDF 文件列表（前10）: {', '.join(stats['pdf_files'])}")
        return

    pdf_dir = Path(args.pdf_dir) if args.pdf_dir else None
    batch_parse(pdf_dir=pdf_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
