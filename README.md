# SoftMatterGPT

面向软物质课程与实验教学的 AI 教学工作台。

## 项目简介

SoftMatterGPT 是一个面向软物质科学课程的智能教学辅助系统。系统基于公开大语言模型（Ollama），结合检索增强生成（RAG）技术，为师生提供课程知识问答、文献检索、实验配方查询、实验方案生成、表征结果辅助分析、材料体系对比以及教学数据分析等功能。

系统采用 Streamlit 前端与 FastAPI 后端分离架构，支持离线环境下优雅降级，在 Ollama 服务不可用时仍可使用知识检索和规则分析功能。

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| 前端 | Streamlit 多页面应用 |
| 后端 | FastAPI RESTful API |
| 数据校验 | Pydantic v2 |
| 大语言模型 | Ollama（支持 Qwen、DeepSeek、Gemma、Llama 等开源模型） |
| 数据处理 | Pandas、NumPy |
| 文本检索 | scikit-learn（TF-IDF 向量化） |
| 可视化 | Plotly、Matplotlib |
| 运行环境 | Python >= 3.9 |

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/songhong/softmatter-app.git
cd softmatter-app
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 安装 Ollama（可选）

如需使用大语言模型功能，请安装 Ollama 并拉取模型：

```bash
# 安装 Ollama（参考 https://ollama.com）
curl -fsSL https://ollama.com/install.sh | sh

# 拉取推荐模型
ollama pull qwen2.5:7b
```

未安装 Ollama 时，系统仍可正常运行，但涉及 LLM 生成的功能（智能问答、实验方案、材料对比）将返回提示信息。

### 4. 配置环境变量（可选）

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 服务地址 |
| `DEFAULT_MODEL` | `qwen2.5:7b` | 默认模型名称 |
| `TOP_K` | `5` | RAG 检索返回条数 |
| `SIMILARITY_THRESHOLD` | `0.3` | 检索相似度阈值 |
| `API_HOST` | `127.0.0.1` | 后端监听地址 |
| `API_PORT` | `8000` | 后端监听端口 |
| `SOFTMATTER_API_KEY` | 自动生成 | API 认证密钥 |

## 启动方法

### 启动后端服务

```bash
python api_server.py
```

后端默认运行在 `http://127.0.0.1:8000`，提供 13 个业务 API 端点（15 个独立路径）。

### 启动前端页面

```bash
streamlit run app.py
```

前端默认运行在 `http://localhost:8501`，在浏览器中打开即可使用。

## 功能概述

| 功能模块 | 页面 | 说明 |
|----------|------|------|
| 系统总览 | 首页 | 模型状态、数据统计卡片、系统架构图、安全声明 |
| 智能问答 | 软物质智能问答 | 基于 RAG 的课程问答，展示证据来源与置信度 |
| 文献检索 | 文献知识检索 | 结构化文献记录搜索，支持 CSV/TXT/Markdown 导入 |
| 配方查询 | 实验配方库 | 实验配方检索、安全等级标注、教师复核提示 |
| 方案生成 | 实验方案助手 | 输入研究目标，生成教学版实验方案框架 |
| 表征分析 | 表征结果分析 | 文字描述分析，基于规则匹配给出结构解释建议 |
| 材料对比 | 材料体系对比 | 预设主题与自定义材料对比，输出对比表格 |
| 教师面板 | 教师分析面板 | 高频关键词、反馈统计、弱点总结、复习建议 |
| 系统设置 | 系统设置 | Ollama 连接检测、模型管理、服务地址配置 |

## 目录结构

```
softmatter-gpt/
├── app.py                  # Streamlit 前端入口
├── api_server.py           # FastAPI 后端入口
├── config.py               # 全局配置
├── requirements.txt        # Python 依赖清单
├── core/                   # 核心业务模块
│   ├── data_loader.py      # 数据加载
│   ├── retriever.py        # 课程知识库检索
│   ├── literature_processor.py  # 文献记录解析与检索
│   ├── recipe_extractor.py # 实验配方抽取与检索
│   ├── characterization.py # 表征结果辅助分析
│   ├── llm_client.py       # Ollama / LLM 调用
│   ├── prompt_templates.py # Prompt 模板管理
│   ├── safety_checker.py   # 实验安全审核
│   ├── qa_logger.py        # 问答日志与反馈
│   └── analytics.py        # 教师统计分析
├── pages/                  # Streamlit 多页面
│   ├── 1_首页.py
│   ├── 2_软物质智能问答.py
│   ├── 3_文献知识检索.py
│   ├── 4_实验配方库.py
│   ├── 5_实验方案助手.py
│   ├── 6_表征结果分析.py
│   ├── 7_材料体系对比.py
│   ├── 8_教师分析面板.py
│   └── 9_系统设置.py
├── data/                   # 数据文件
│   ├── softmatter_knowledge.csv
│   ├── literature_records.csv
│   ├── experiment_recipes.csv
│   ├── sample_questions.csv
│   ├── feedback.csv
│   └── settings.json
├── logs/                   # 运行日志
│   └── qa_history.csv
├── assets/                 # 静态资源
│   ├── architecture.png    # 系统架构图
│   └── rag_flow.png        # RAG 流程图
└── docs/                   # 项目文档
    ├── 软件说明书.md
    ├── 演示流程.md
    └── 答辩讲稿.md
```

## API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/system/status` | GET | 系统状态信息 |
| `/api/models` | GET | 获取 Ollama 模型列表 |
| `/api/model/current` | GET/POST | 获取或设置当前模型 |
| `/api/model/test` | POST | 测试当前模型 |
| `/api/ollama/status` | GET | Ollama 服务连接状态 |
| `/api/ollama/url` | POST | 设置 Ollama 服务地址 |
| `/api/ask` | POST | 软物质智能问答 |
| `/api/search` | POST | 课程知识库检索 |
| `/api/literature/search` | POST | 文献记录检索 |
| `/api/recipe/search` | POST | 实验配方检索 |
| `/api/experiment-plan` | POST | 实验方案生成 |
| `/api/characterization/analyze` | POST | 表征结果辅助分析 |
| `/api/compare` | POST | 材料体系对比 |
| `/api/feedback` | POST | 保存用户反馈 |
| `/api/teacher/analysis` | GET | 教师分析数据 |

所有 API 端点均需 `X-API-Key` 请求头认证。

## 数据说明

| 数据源 | 当前条数 | 说明 |
|--------|----------|------|
| 课程知识库 | 60 条 | 人工编写的软物质教学知识条目 |
| 文献记录 | 27 条 | 教学示例数据，标注为 curated_example |
| 实验配方 | 30 条 | 教学示例数据，标记 is_example=true |
| 测试问题 | 25 条 | 覆盖流变学、胶体、高分子、乳液等方向 |
| 反馈记录 | 6 条 | 包含 5 条演示反馈和 1 条测试记录 |

文献记录和实验配方当前为教学示例数据，非真实文献解析结果。系统支持后续导入真实数据以扩充知识库。

## 安全声明

- 本系统输出的实验方案仅为教学参考框架，不构成可直接执行的实验操作 SOP。
- 涉及高风险试剂（强酸、强碱、液氮等）、高温高压等实验条件时，系统会自动标记需教师复核。
- 所有基于 LLM 生成的回答均附带证据来源和置信度标注，证据不足时系统会明确提示。
- API 端点采用密钥认证，Ollama 地址设置包含 SSRF 防护。
- 输入参数经 Pydantic 校验，防止非法数据注入。

## 已知限制

1. Ollama 需要在本地安装并启动后才能使用 LLM 生成功能，离线状态下仅可使用检索和规则分析功能。
2. 当前数据为教学示例规模（共 122 条），系统已预留批量导入接口，支持后续扩展至数百条规模。
3. 表征结果分析基于规则匹配实现，未接入多模态视觉模型，暂不支持直接分析图片文件。
4. PDF 批量解析脚本已预留接口，当前未执行大规模 PDF 解析任务。

## 致谢

- 课程知识库内容参考了软物质科学领域经典教材与公开文献。
- 大语言模型能力由 Ollama 项目提供，支持 Qwen、DeepSeek、Gemma、Llama 等开源模型。
- 前端界面基于 Streamlit 框架构建，数据可视化使用 Plotly 和 Matplotlib。
- 项目开发过程中得到了课程教师的指导和建议。

## 许可证

本项目仅用于教学目的。项目代码、文档和数据集均以教学示例形式提供，不对外发布为正式软件产品。如需二次开发或引用，请注明出处并遵守相关开源组件的许可协议。
