"use client";

import { useState } from "react";

const SAMPLE_QUESTIONS = [
  { text: "什么是剪切变稀现象？", icon: "🔬" },
  { text: "CMC 是什么？", icon: "💧" },
  { text: "物理交联和化学交联水凝胶区别？", icon: "🧪" },
  { text: "Pickering 乳液稳定机制？", icon: "⚗️" },
  { text: "DLS 测量粒径原理？", icon: "📐" },
];

export default function QAPage() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = () => {
    if (!query.trim()) return;
    setLoading(true);
    setTimeout(() => {
      setResult({
        answer: "剪切变稀是指流体的表观粘度随剪切速率增加而降低的现象，是软物质中常见的非牛顿流体行为。",
        detail: "在高分子溶液、胶体悬浮液等软物质体系中，分子或颗粒在静止状态下形成网络结构。当施加剪切力时，这些结构被破坏或重新排列，导致流动阻力减小。",
        confidence: "high",
        evidence: [
          { title: "流变学基本概念", score: 0.89, category: "基本概念" },
          { title: "高分子溶液流变行为", score: 0.76, category: "高分子科学" },
        ],
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-qa)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-qa" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#06b6d4"/>
                </linearGradient>
              </defs>
              <path d="M9 3h6v8l5 8H4l5-8V3z"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-purple">智能</span><br />
            <span className="text-gradient-cyan">问答</span>
          </h1>
          <p className="body-glass max-w-lg">
            基于 RAG 检索增强生成技术，回答课程概念问题
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Quick Questions */}
        <div className="mb-12">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-qa2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-qa2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            快速提问
          </div>
          <div className="flex flex-wrap gap-3">
            {SAMPLE_QUESTIONS.map((q) => (
              <button
                key={q.text}
                onClick={() => setQuery(q.text)}
                className="btn-glass-outline text-xs py-2 px-4 flex items-center gap-2"
              >
                <span>{q.icon}</span>
                {q.text}
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <div className="card-glass p-8 mb-12">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-qa3)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-qa3" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            输入问题
          </div>
          <textarea
            className="input-glass min-h-[140px] resize-y"
            placeholder="输入你的问题，例如：什么是剪切变稀？"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSubmit()}
          />
          <div className="mt-6 flex items-center justify-between">
            <div className="text-white/30 text-sm">按 Enter 发送</div>
            <button
              onClick={handleSubmit}
              disabled={!query.trim() || loading}
              className="btn-glass disabled:opacity-50"
            >
              {loading ? (
                <>
                  <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" strokeDasharray="31.416" strokeDashoffset="10" />
                  </svg>
                  思考中...
                </>
              ) : (
                <>
                  提交
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M22 2L11 13" />
                    <path d="M22 2l-7 20-4-9-9-4 20-7z" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Result */}
        {result && (
          <div className="animate-fade-in-up">
            <div className="card-glass p-8 mb-8">
              {/* Top accent */}
              <div className="accent-top accent-top-purple" />

              <div className="flex items-center gap-4 mb-6">
                <span className="tag-glass">
                  {result.confidence === "high" ? "✓ 高置信度" : "○ 中置信度"}
                </span>
                <span className="text-white/30 text-sm">证据来源: {result.evidence.length} 条</span>
              </div>

              <div className="mb-6">
                <div className="caption-glass mb-3 flex items-center gap-2">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#a855f7" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 16v-4m0-4h.01"/>
                  </svg>
                  简要结论
                </div>
                <p className="text-lg text-white/90">{result.answer}</p>
              </div>

              <div className="mb-8">
                <div className="caption-glass mb-3 flex items-center gap-2">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" strokeWidth="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                  详细解释
                </div>
                <p className="text-white/50 leading-relaxed">{result.detail}</p>
              </div>

              <div className="border-t border-white/[0.06] pt-6">
                <div className="caption-glass mb-4 flex items-center gap-2">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ec4899" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <path d="M14 2v6h6"/>
                  </svg>
                  证据来源
                </div>
                <div className="space-y-3">
                  {result.evidence.map((ev: any) => (
                    <div key={ev.title} className="flex items-center justify-between p-4 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                      <div>
                        <div className="font-medium text-white/80">{ev.title}</div>
                        <div className="text-white/30 text-xs mt-1">{ev.category}</div>
                      </div>
                      <div className="font-mono text-sm bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
                        {ev.score.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Feedback */}
            <div className="flex items-center gap-4">
              <span className="text-white/40 text-sm">这个回答有帮助吗？</span>
              <button className="btn-glass-outline text-xs py-2 px-4 hover:border-emerald-500 hover:text-emerald-400">
                👍 有帮助
              </button>
              <button className="btn-glass-outline text-xs py-2 px-4 hover:border-rose-500 hover:text-rose-400">
                👎 需改进
              </button>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && (
          <div className="text-center py-24">
            <div className="text-6xl mb-6">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="url(#grad-empty)" strokeWidth="1.5" className="mx-auto">
                <defs>
                  <linearGradient id="grad-empty" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#6366f1"/>
                    <stop offset="50%" stopColor="#a855f7"/>
                    <stop offset="100%" stopColor="#06b6d4"/>
                  </linearGradient>
                </defs>
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <circle cx="9" cy="10" r="1" fill="url(#grad-empty)"/>
                <circle cx="12" cy="10" r="1" fill="url(#grad-empty)"/>
                <circle cx="15" cy="10" r="1" fill="url(#grad-empty)"/>
              </svg>
            </div>
            <div className="headline-glass text-2xl text-white/30 mb-4">开始提问</div>
            <p className="text-white/30 max-w-md mx-auto">
              输入问题，系统将从知识库中检索证据并生成回答
            </p>
          </div>
        )}
      </section>
    </div>
  );
}
