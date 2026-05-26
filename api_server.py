"""
SoftMatterGPT - FastAPI 后端服务入口

提供 13 个 RESTful API 端点，覆盖系统状态、模型管理、知识检索、智能问答、
文献检索、配方检索、实验方案生成、表征分析、材料对比、反馈保存和教师分析。

运行方式:
    python api_server.py
    或
    uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
"""

import core.path_setup  # noqa: F401 — 确保项目根目录在 sys.path 中

import ipaddress
import logging
import uuid
from datetime import datetime
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
from core import (
    analytics,
    characterization,
    llm_client,
    qa_logger,
    recipe_extractor,
    retriever,
    safety_checker,
)
from core import literature_processor as lit_proc
from core import prompt_templates as prompts

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pydantic 请求模型
# ---------------------------------------------------------------------------


class ModelRequest(BaseModel):
    """设置当前模型。"""
    model: str = Field(..., min_length=1, max_length=200, description="模型名称")


class OllamaUrlRequest(BaseModel):
    """设置 Ollama 服务地址。"""
    url: str = Field(..., min_length=1, max_length=500, description="Ollama 服务地址")


class QueryRequest(BaseModel):
    """通用查询请求（问答、知识检索、文献检索、配方检索）。"""
    query: str = Field(..., min_length=1, max_length=5000, description="查询文本")


class ExperimentPlanRequest(BaseModel):
    """生成实验方案请求。"""
    research_goal: str = Field(..., min_length=1, max_length=5000, description="研究目标")


class CharacterizationRequest(BaseModel):
    """表征结果分析请求。"""
    description: str = Field(..., min_length=1, max_length=10000, description="表征描述")


class CompareRequest(BaseModel):
    """材料体系对比请求。"""
    materials: list[str] = Field(..., min_length=1, max_length=10, description="待对比材料列表")


class FeedbackRequest(BaseModel):
    """用户反馈请求。"""
    question_id: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., ge=0, le=5, description="评分 0-5")
    comment: str = Field(default="", max_length=2000)


# ---------------------------------------------------------------------------
# 认证依赖
# ---------------------------------------------------------------------------


async def verify_api_key(x_api_key: str = Header(default="")):
    """简单 API Key 认证（本地教学工具级别）。"""
    if config.API_KEY and x_api_key != config.API_KEY:
        raise HTTPException(status_code=401, detail="无效的 API Key")


# ---------------------------------------------------------------------------
# SSRF 防护：URL 白名单校验
# ---------------------------------------------------------------------------

_ALLOWED_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


def _validate_local_url(url: str) -> str:
    """验证 URL 是否指向本地地址，防止 SSRF 攻击。"""
    try:
        parsed = urlparse(url)
    except Exception:
        raise HTTPException(status_code=400, detail="无效的 URL 格式。")

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="仅支持 http/https 协议。")

    hostname = parsed.hostname or ""
    if hostname in _ALLOWED_HOSTNAMES:
        return url

    # 允许 127.0.0.0/8 和 10.0.0.0/8 等私有地址段
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_loopback or addr.is_private:
            return url
    except ValueError:
        pass

    raise HTTPException(
        status_code=400,
        detail="出于安全考虑，Ollama 地址仅允许本地或私有网络地址（localhost、127.x、10.x、172.16-31.x、192.168.x）。",
    )


# ---------------------------------------------------------------------------
# 内部辅助函数
# ---------------------------------------------------------------------------


def _evidence_to_dict(evidence) -> dict:
    """将 RetrievalResult 转为前端可直接使用的字典。"""
    return {
        "id": evidence.id,
        "title": evidence.title,
        "category": evidence.category,
        "content": evidence.content,
        "source": evidence.source,
        "score": evidence.score,
        "data_type": evidence.data_type,
    }


def _retrieval_to_dict(result) -> dict:
    """将知识库检索结果转为字典（与 _evidence_to_dict 相同结构，保持接口一致）。"""
    return _evidence_to_dict(result)


# ---------------------------------------------------------------------------
# 应用实例
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SoftMatterGPT API",
    description="软物质科学实验方案生成与文献挖掘助手后端服务",
    version="0.1.0",
)

# CORS 中间件 - 允许 Streamlit 前端跨域调用
_allowed_origins = [
    f"http://localhost:{config.STREAMLIT_PORT}",
    f"http://127.0.0.1:{config.STREAMLIT_PORT}",
    f"http://localhost:{config.API_PORT}",
    f"http://127.0.0.1:{config.API_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# 健康检查与系统状态
# ---------------------------------------------------------------------------
@app.get("/api/system/status", dependencies=[Depends(verify_api_key)])
def system_status():
    """返回系统基本状态信息，包含 Ollama 真实连接状态和数据统计。"""
    ollama_status = llm_client.check_ollama_status()
    stats = retriever.get_stats()

    # 获取今日问答次数
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily = analytics.get_daily_question_counts()
    today_count = 0
    for item in daily:
        if item.get("date") == today_str:
            today_count = item.get("count", 0)
            break

    # 反馈满意率
    feedback_dist = analytics.get_feedback_distribution()

    return {
        "status": "running",
        "version": "0.1.0",
        "default_model": llm_client.get_current_model(),
        "ollama_url": llm_client.get_ollama_url(),
        "ollama_online": ollama_status.online,
        "ollama_model_count": ollama_status.model_count,
        "ollama_message": ollama_status.message,
        "knowledge_count": stats.get("knowledge", {}).get("total", 0),
        "literature_count": stats.get("literature", {}).get("total", 0),
        "recipe_count": stats.get("recipes", {}).get("total", 0),
        "today_questions": today_count,
        "total_questions": analytics.get_question_count(),
        "feedback_satisfaction_rate_percent": feedback_dist.get("satisfaction_rate", 0),
    }


# ---------------------------------------------------------------------------
# 模型管理接口
# ---------------------------------------------------------------------------
@app.get("/api/models", dependencies=[Depends(verify_api_key)])
def list_models():
    """获取 Ollama 可用模型列表（来自 /api/tags 真实数据）。"""
    models, error = llm_client.list_models()
    if error:
        return {"models": [], "error": error, "ollama_online": False}
    return {"models": models, "error": "", "ollama_online": True}


@app.get("/api/model/current", dependencies=[Depends(verify_api_key)])
def get_current_model():
    """获取当前选定模型。"""
    return {"model": llm_client.get_current_model()}


@app.post("/api/model/current", dependencies=[Depends(verify_api_key)])
def set_current_model(body: ModelRequest):
    """设置当前模型并持久化到 settings.json。"""
    success, message = llm_client.set_current_model(body.model)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"model": body.model, "message": message}


@app.post("/api/model/test", dependencies=[Depends(verify_api_key)])
def test_model():
    """测试当前模型是否可用。"""
    result = llm_client.test_model()
    return {
        "success": result.success,
        "model": result.model,
        "message": result.message,
        "latency_ms": result.latency_ms,
    }


@app.get("/api/ollama/status", dependencies=[Depends(verify_api_key)])
def ollama_status():
    """检测 Ollama 服务连接状态。"""
    status = llm_client.check_ollama_status()
    return {
        "online": status.online,
        "model_count": status.model_count,
        "message": status.message,
    }


@app.post("/api/ollama/url", dependencies=[Depends(verify_api_key)])
def set_ollama_url(body: OllamaUrlRequest):
    """设置 Ollama 服务地址并持久化。仅允许本地/私有网络地址。"""
    safe_url = _validate_local_url(body.url)
    success, message = llm_client.set_ollama_url(safe_url)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"url": safe_url, "message": message}


# ---------------------------------------------------------------------------
# 问答与检索接口
# ---------------------------------------------------------------------------
@app.post("/api/ask", dependencies=[Depends(verify_api_key)])
def ask_question(body: QueryRequest):
    """软物质智能问答（RAG）。

    流程：检索知识库 → 构建 prompt → 调用 LLM → 记录日志。
    使用 def 而非 async def，因为 llm_client.generate() 内部使用同步 requests，
    声明为 async 会阻塞事件循环。
    """
    question = body.query.strip()

    # 1. 检索证据
    bundle = retriever.search_all(question)
    evidence_list = bundle.results

    # 2. 构建 prompt
    prompt_payload = prompts.build_qa_prompt(question, evidence_list)

    # 3. 调用 LLM
    llm_resp = llm_client.generate(
        prompt=prompt_payload.user_prompt,
        system=prompt_payload.system_prompt,
    )

    if not llm_resp.success:
        # LLM 不可用时仍返回证据摘要
        evidence_cards = [_evidence_to_dict(e) for e in evidence_list]
        return {
            "answer": None,
            "evidence": evidence_cards,
            "question_id": "",
            "confidence": "无法评估",
            "has_sufficient_evidence": bundle.has_sufficient_evidence,
            "warnings": prompt_payload.warnings + (bundle.evidence_gap_message and [bundle.evidence_gap_message] or []),
            "error": llm_resp.error,
            "model": llm_resp.model or llm_client.get_current_model(),
        }

    # 4. 安全审核答案文本
    safety = safety_checker.check_text(llm_resp.content)

    # 5. 记录问答日志
    question_id = f"q-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    qa_logger.log_qa(
        question=question,
        answer=llm_resp.content,
        model=llm_resp.model,
        evidence_count=len(evidence_list),
        confidence="高" if bundle.has_sufficient_evidence else "低",
        risk_level=safety.risk_level,
        question_id=question_id,
    )

    # 6. 组装响应
    evidence_cards = [_evidence_to_dict(e) for e in evidence_list]
    return {
        "answer": llm_resp.content,
        "evidence": evidence_cards,
        "question_id": question_id,
        "confidence": "高" if bundle.has_sufficient_evidence else "低",
        "has_sufficient_evidence": bundle.has_sufficient_evidence,
        "warnings": prompt_payload.warnings,
        "safety": safety.to_dict(),
        "model": llm_resp.model,
        "error": "",
    }


@app.post("/api/search", dependencies=[Depends(verify_api_key)])
def search_knowledge(body: QueryRequest):
    """课程知识库检索。"""
    results = retriever.search(body.query)
    return {
        "results": [_retrieval_to_dict(r) for r in results],
        "total": len(results),
        "query": body.query,
        "error": "",
    }


@app.post("/api/literature/search", dependencies=[Depends(verify_api_key)])
def search_literature(body: QueryRequest):
    """文献记录检索。"""
    records = lit_proc.search(body.query)
    results = []
    for rec in records:
        results.append({
            "id": rec.id,
            "title": rec.title,
            "year": rec.year,
            "source": rec.source,
            "material_system": rec.material_system,
            "method": rec.method,
            "characterization": rec.characterization,
            "result_summary": rec.result_summary,
            "keywords": rec.keywords,
            "data_source": rec.data_source,
        })
    return {
        "results": results,
        "total": len(results),
        "query": body.query,
        "error": "",
    }


@app.post("/api/recipe/search", dependencies=[Depends(verify_api_key)])
def search_recipes(body: QueryRequest):
    """实验配方检索。"""
    recipes = recipe_extractor.search(body.query)
    results = []
    for rec in recipes:
        results.append({
            "id": rec.id,
            "material": rec.material,
            "concentration": rec.concentration,
            "process": rec.process,
            "temperature": rec.temperature,
            "time": rec.time,
            "characterization": rec.characterization,
            "result": rec.result,
            "safety_level": rec.safety_level,
            "source": rec.source,
            "is_example": rec.is_example,
        })
    return {
        "results": results,
        "total": len(results),
        "query": body.query,
        "error": "",
    }


@app.post("/api/experiment-plan", dependencies=[Depends(verify_api_key)])
def generate_experiment_plan(body: ExperimentPlanRequest):
    """生成教学版实验方案。

    流程：检索相关配方和知识 → 构建实验方案 prompt → 调用 LLM → 安全审核。
    使用 def 而非 async def，因为 llm_client.generate() 是同步调用。
    """
    goal = body.research_goal.strip()

    # 1. 检索相关证据
    evidence_bundle = retriever.search_all(goal)
    evidence_list = evidence_bundle.results

    # 2. 构建实验方案 prompt
    prompt_payload = prompts.build_experiment_plan_prompt(
        goal=goal, constraints="", evidence=evidence_list,
    )

    # 3. 调用 LLM
    llm_resp = llm_client.generate(
        prompt=prompt_payload.user_prompt,
        system=prompt_payload.system_prompt,
    )

    if not llm_resp.success:
        return {
            "plan": None,
            "safety": None,
            "evidence": [_evidence_to_dict(e) for e in evidence_list],
            "warnings": prompt_payload.warnings,
            "error": llm_resp.error,
        }

    # 4. 安全审核方案文本
    safety = safety_checker.check_text(llm_resp.content)
    # 补充教师复核清单
    safety.teacher_review_checklist = safety_checker.generate_teacher_review_checklist(
        risk_level=safety.risk_level, findings=safety.findings,
    )

    # 5. 组装结构化方案
    plan = {
        "content": llm_resp.content,
        "experiment_goal": goal,
        "evidence_basis": [_evidence_to_dict(e) for e in evidence_list],
        "safety_level": safety.risk_level,
        "requires_teacher_review": safety.requires_teacher_review,
        "teacher_review_checklist": safety.teacher_review_checklist,
        "disclaimer": prompts.TEACHING_PLAN_NOTICE,
    }

    return {
        "plan": plan,
        "safety": safety.to_dict(),
        "warnings": prompt_payload.warnings,
        "model": llm_resp.model,
        "error": "",
    }


@app.post("/api/characterization/analyze", dependencies=[Depends(verify_api_key)])
def analyze_characterization(body: CharacterizationRequest):
    """表征结果辅助分析（基于规则 + RAG 证据，不调用 LLM）。"""
    result = characterization.analyze_text(body.description)
    return {
        "analysis": result.to_dict(),
        "error": "",
    }


@app.post("/api/compare", dependencies=[Depends(verify_api_key)])
def compare_materials(body: CompareRequest):
    """材料体系对比。

    检索各材料的证据，构建对比 prompt，调用 LLM 生成 Markdown 对比表。
    """
    materials = body.materials

    # 1. 为每个材料检索证据
    all_evidence = []
    for mat in materials:
        mat_results = retriever.search(mat, top_k=config.TOP_K)
        all_evidence.extend(mat_results)

    # 2. 构建对比 prompt
    materials_text = "、".join(materials)
    evidence_text = prompts.format_evidence_cards(all_evidence)
    user_prompt = (
        f"请对比以下材料体系：{materials_text}\n\n"
        f"可用证据：\n{evidence_text}\n\n"
        "请输出 Markdown 对比表格，并在表格后附上证据来源。"
    )

    # 3. 调用 LLM（同步调用，用 def）
    llm_resp = llm_client.generate(
        prompt=user_prompt,
        system=prompts.COMPARISON_SYSTEM_PROMPT,
    )

    if not llm_resp.success:
        return {
            "comparison": None,
            "materials": materials,
            "evidence": [_evidence_to_dict(e) for e in all_evidence],
            "error": llm_resp.error,
        }

    return {
        "comparison": llm_resp.content,
        "materials": materials,
        "evidence": [_evidence_to_dict(e) for e in all_evidence],
        "model": llm_resp.model,
        "error": "",
    }


@app.post("/api/feedback", dependencies=[Depends(verify_api_key)])
def save_feedback(body: FeedbackRequest):
    """保存用户反馈到 feedback.csv。"""
    success = qa_logger.log_feedback(
        question_id=body.question_id,
        rating=body.rating,
        comment=body.comment,
    )
    if not success:
        raise HTTPException(status_code=500, detail="保存反馈失败，请稍后重试。")
    return {
        "status": "saved",
        "question_id": body.question_id,
        "rating": body.rating,
        "message": "反馈已保存，感谢您的评价。",
        "error": "",
    }


@app.get("/api/teacher/analysis", dependencies=[Depends(verify_api_key)])
def teacher_analysis():
    """教师分析面板数据。

    汇总以下统计信息（全部来自真实日志和反馈数据）：
    - 最近提问记录
    - 高频关键词
    - 反馈评分分布
    - 每日提问趋势
    - 高风险实验方案统计
    - 各数据源条数
    """
    try:
        recent_questions = analytics.get_recent_questions(n=20)
        keywords = analytics.get_keyword_frequency(top_n=15)
        feedback_dist = analytics.get_feedback_distribution()
        daily_counts = analytics.get_daily_question_counts()
        high_risk = analytics.get_high_risk_stats()
        stats = retriever.get_stats()
    except Exception as exc:
        logger.error("教师分析数据加载失败: %s", exc)
        return {
            "analytics": None,
            "error": f"分析数据加载失败: {exc}",
        }

    return {
        "analytics": {
            "recent_questions": recent_questions,
            "keyword_frequency": keywords,
            "feedback_distribution": feedback_dist,
            "daily_question_counts": daily_counts,
            "high_risk_stats": high_risk,
            "data_stats": stats,
            "total_questions": analytics.get_question_count(),
        },
        "error": "",
    }


# ---------------------------------------------------------------------------
# 启动入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api_server:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )
