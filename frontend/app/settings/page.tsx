"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [ollamaUrl, setOllamaUrl] = useState("http://localhost:11434");
  const [model, setModel] = useState("qwen3.5:9b");
  const [status, setStatus] = useState<"online" | "offline" | "checking">("online");
  const [testPrompt, setTestPrompt] = useState("请用一句话介绍软物质科学。");
  const [testResult, setTestResult] = useState<string | null>(null);
  const [testLoading, setTestLoading] = useState(false);
  const [modelSaved, setModelSaved] = useState(false);
  const [modelTesting, setModelTesting] = useState(false);
  const [modelTestResult, setModelTestResult] = useState<string | null>(null);

  const handleDetect = () => {
    setStatus("checking");
    setTimeout(() => setStatus("online"), 1500);
  };

  const handleSetModel = () => {
    setModelSaved(true);
    setModelTestResult(null);
    setTimeout(() => setModelSaved(false), 2000);
  };

  const handleTestModel = () => {
    setModelTesting(true);
    setModelTestResult(null);
    setTimeout(() => {
      setModelTestResult(`模型 ${model} 响应正常。平均延迟 1.2s，首次 Token 延迟 0.3s，吞吐量 45 tokens/s。`);
      setModelTesting(false);
    }, 2000);
  };

  const handleTest = () => {
    if (!testPrompt.trim()) return;
    setTestLoading(true);
    setTestResult(null);
    setTimeout(() => {
      setTestResult("软物质科学是研究处于热力学平衡态附近、受热涨落显著影响的柔软物质（如聚合物、胶体、液晶、表面活性剂、生物大分子等）的结构、性质与运动规律的交叉学科。");
      setTestLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-settings)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-settings" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#06b6d4"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            系统管理
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-white">系统</span><br />
            <span className="text-gradient-purple">设置</span>
          </h1>
          <p className="body-glass max-w-lg">
            Ollama 服务检测、模型管理与连接测试
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Ollama Connection */}
        <div className="card-glass p-8 mb-12">
          <div className="accent-top" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-conn)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-conn" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            服务连接
          </div>
          <h3 className="text-xl font-bold mb-8 text-white/90">Ollama 服务配置</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="md:col-span-2">
              <div className="caption-glass mb-2">服务地址</div>
              <input
                type="text"
                value={ollamaUrl}
                onChange={(e) => setOllamaUrl(e.target.value)}
                className="input-glass font-mono"
              />
            </div>
            <div className="flex items-end gap-3">
              <button onClick={handleDetect} className="btn-glass-outline flex-1">
                {status === "checking" ? "检测中..." : "检测连接"}
              </button>
              <button className="btn-glass flex-1">保存</button>
            </div>
          </div>

          {/* Status */}
          <div className={`flex items-center gap-3 p-4 rounded-xl ${
            status === "online"
              ? "bg-emerald-500/10 border border-emerald-500/20"
              : status === "offline"
              ? "bg-rose-500/10 border border-rose-500/20"
              : "bg-amber-500/10 border border-amber-500/20"
          }`}>
            <div className={`w-3 h-3 rounded-full ${
              status === "online"
                ? "bg-emerald-500"
                : status === "offline"
                ? "bg-rose-500"
                : "bg-amber-500 animate-pulse"
            }`} />
            <span className={`text-sm font-medium ${
              status === "online"
                ? "text-emerald-400"
                : status === "offline"
                ? "text-rose-400"
                : "text-amber-400"
            }`}>
              {status === "online"
                ? "Ollama 服务在线，已安装 4 个模型。"
                : status === "offline"
                ? "Ollama 服务离线，请检查连接。"
                : "正在检测..."}
            </span>
          </div>
        </div>

        {/* Model Management */}
        <div className="card-glass p-8 mb-12">
          <div className="accent-top accent-top-cyan" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-model)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-model" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            模型管理
          </div>
          <h3 className="text-xl font-bold mb-2 text-white/90">选择模型</h3>
          <p className="text-white/40 mb-8">
            当前使用模型: <span className="font-mono font-medium text-indigo-400">{model}</span>
          </p>

          <div className="space-y-3 mb-8">
            {[
              { name: "qwen3.5:9b", size: "5.2 GB", family: "Qwen", params: "9B" },
              { name: "qwen2.5:7b", size: "4.1 GB", family: "Qwen", params: "7B" },
              { name: "llama3.1:8b", size: "4.5 GB", family: "Llama", params: "8B" },
              { name: "mistral:7b", size: "3.8 GB", family: "Mistral", params: "7B" },
            ].map((m) => (
              <div
                key={m.name}
                onClick={() => setModel(m.name)}
                className={`flex items-center justify-between p-5 rounded-xl cursor-pointer transition-all ${
                  m.name === model
                    ? "bg-gradient-to-r from-indigo-500/10 to-cyan-500/10 border border-indigo-500/20"
                    : "bg-white/[0.03] border border-white/[0.06] hover:border-white/[0.12]"
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full ${m.name === model ? "bg-gradient-to-r from-indigo-500 to-cyan-500" : "bg-white/10"}`} />
                  <span className="font-mono font-medium text-white/80">{m.name}</span>
                </div>
                <div className="flex items-center gap-6 text-xs text-white/30">
                  <span>{m.size}</span>
                  <span>{m.family}</span>
                  <span>{m.params}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-4">
            <button onClick={handleSetModel} className="btn-glass disabled:opacity-50">
              {modelSaved ? "已保存!" : "设为当前模型"}
            </button>
            <button onClick={handleTestModel} disabled={modelTesting} className="btn-glass-outline disabled:opacity-50">
              {modelTesting ? (
                <>
                  <svg className="animate-spin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" strokeDasharray="31.416" strokeDashoffset="10" />
                  </svg>
                  测试中...
                </>
              ) : "测试当前模型"}
            </button>
          </div>

          {modelTestResult && (
            <div className="mt-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <div className="flex items-center gap-2 mb-1">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-emerald-400 text-sm font-semibold">测试通过</span>
              </div>
              <p className="text-white/50 text-sm">{modelTestResult}</p>
            </div>
          )}
        </div>

        {/* Quick Test */}
        <div className="card-glass p-8 mb-12">
          <div className="accent-top accent-top-purple" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-test)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-test" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <path d="M22 2L11 13"/>
              <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
            快速测试
          </div>
          <h3 className="text-xl font-bold mb-8 text-white/90">测试模型响应</h3>

          <div className="mb-6">
            <div className="caption-glass mb-2">测试 Prompt</div>
            <input
              type="text"
              value={testPrompt}
              onChange={(e) => setTestPrompt(e.target.value)}
              className="input-glass"
            />
          </div>

          <button onClick={handleTest} disabled={testLoading} className="btn-glass disabled:opacity-50">
            {testLoading ? (
              <>
                <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" strokeDasharray="31.416" strokeDashoffset="10" />
                </svg>
                生成中...
              </>
            ) : (
              <>
                发送测试请求
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 2L11 13"/>
                  <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
                </svg>
              </>
            )}
          </button>

          {testResult && (
            <div className="mt-6 p-4 rounded-xl bg-white/[0.03] border border-white/[0.06]">
              <div className="caption-glass mb-2">模型响应</div>
              <p className="text-white/60 text-sm leading-relaxed">{testResult}</p>
            </div>
          )}
        </div>

        {/* System Info */}
        <div className="card-glass p-8">
          <div className="accent-top accent-top-cyan" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-info)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-info" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            系统信息
          </div>
          <h3 className="text-xl font-bold mb-8 text-white/90">技术栈</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { name: "前端框架", value: "Next.js 15 + React 19", color: "from-indigo-500 to-purple-500" },
              { name: "UI 框架", value: "Tailwind CSS", color: "from-cyan-500 to-blue-500" },
              { name: "后端服务", value: "FastAPI", color: "from-purple-500 to-pink-500" },
              { name: "大语言模型", value: "Ollama", color: "from-pink-500 to-rose-500" },
              { name: "检索技术", value: "TF-IDF + 余弦相似度", color: "from-amber-500 to-orange-500" },
              { name: "数据存储", value: "CSV 文件", color: "from-emerald-500 to-teal-500" },
            ].map((info) => (
              <div key={info.name} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                <span className="caption-glass">{info.name}</span>
                <span className={`font-mono text-sm bg-gradient-to-r ${info.color} bg-clip-text text-transparent`}>
                  {info.value}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-12 border-l-4 border-amber-500/50 p-6 rounded-r-xl bg-amber-500/[0.05]">
          <div className="flex items-center gap-2 mb-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth="2">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <span className="text-amber-400 text-sm font-semibold">安全声明</span>
          </div>
          <p className="text-white/40 text-sm leading-relaxed">
            本系统输出的实验方案仅为教学参考框架，不构成可直接执行的实验操作 SOP。具体试剂选择、浓度、温度、时间和操作条件必须经教师或实验室安全规范审核后方可实施。
          </p>
        </div>
      </section>
    </div>
  );
}
