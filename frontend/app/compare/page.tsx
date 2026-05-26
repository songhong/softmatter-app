"use client";

import { useState } from "react";

const PRESET_TOPICS = [
  "物理交联 vs 化学交联水凝胶",
  "阴离子 vs 阳离子表面活性剂",
  "O/W 型 vs W/O 型乳液",
  "脂质体 vs 聚合物胶束",
  "小分子凝胶 vs 高分子凝胶",
];

const SAMPLE_RESULTS = [
  { property: "交联机制", materialA: "物理缠结、氢键、疏水作用", materialB: "共价键交联" },
  { property: "可逆性", materialA: "可逆，加热可溶解", materialB: "不可逆，永久网络" },
  { property: "力学强度", materialA: "较弱", materialB: "较强" },
  { property: "溶胀性", materialA: "溶胀率较高", materialB: "溶胀率较低" },
  { property: "生物相容性", materialA: "通常较好", materialB: "取决于交联剂" },
  { property: "制备方法", materialA: "冷冻解冻、加热冷却", materialB: "化学交联剂、光交联" },
];

export default function ComparePage() {
  const [topic, setTopic] = useState("");
  const [results, setResults] = useState<any[] | null>(null);

  const handleCompare = () => {
    setTimeout(() => setResults(SAMPLE_RESULTS), 800);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-cmp)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-cmp" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#10b981"/>
                  <stop offset="100%" stopColor="#14b8a6"/>
                </linearGradient>
              </defs>
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M3 9h18M9 3v18"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-white">材料</span><br />
            <span className="text-gradient-cyan">对比</span>
          </h1>
          <p className="body-glass max-w-lg">
            对比不同材料体系的结构、性能和应用场景
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Preset Topics */}
        <div className="mb-12">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-cmp2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-cmp2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            预设对比主题
          </div>
          <div className="flex flex-wrap gap-3">
            {PRESET_TOPICS.map((t) => (
              <button
                key={t}
                onClick={() => setTopic(t)}
                className={`text-xs px-4 py-2 rounded-full transition-all ${
                  topic === t
                    ? "bg-gradient-to-r from-indigo-500 to-cyan-500 text-white shadow-lg shadow-indigo-500/20"
                    : "bg-white/[0.04] border border-white/[0.08] text-white/50 hover:border-white/[0.15] hover:text-white/70"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Custom Compare */}
        <div className="card-glass p-8 mb-12">
          <div className="accent-top accent-top-cyan" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-cmp3)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-cmp3" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M3 9h18M9 3v18"/>
            </svg>
            自定义对比
          </div>
          <h3 className="text-2xl font-bold mb-6 text-white/90">选择对比材料</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <div className="caption-glass mb-2">材料 A</div>
              <input type="text" className="input-glass" placeholder="例如：物理交联水凝胶" />
            </div>
            <div>
              <div className="caption-glass mb-2">材料 B</div>
              <input type="text" className="input-glass" placeholder="例如：化学交联水凝胶" />
            </div>
          </div>
          <button onClick={handleCompare} className="btn-glass">
            开始对比
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </button>
        </div>

        {/* Results */}
        {results && (
          <div className="animate-fade-in-up">
            <div className="flex items-center gap-4 mb-8">
              <div className="caption-glass flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-cmp4)" strokeWidth="2">
                  <defs>
                    <linearGradient id="grad-cmp4" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#10b981"/>
                      <stop offset="100%" stopColor="#14b8a6"/>
                    </linearGradient>
                  </defs>
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <path d="M14 2v6h6"/>
                </svg>
                对比结果
              </div>
              <div className="flex-1 h-px bg-white/[0.06]" />
            </div>

            <div className="card-glass overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="bg-white/[0.03]">
                    <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">对比维度</th>
                    <th className="px-6 py-4 text-left text-indigo-400 text-xs font-semibold uppercase tracking-wider border-b border-white/[0.06]">材料 A</th>
                    <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">材料 B</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((r) => (
                    <tr key={r.property} className="hover:bg-white/[0.02] transition-colors">
                      <td className="px-6 py-4 font-medium text-white/80 border-b border-white/[0.04]">{r.property}</td>
                      <td className="px-6 py-4 text-white/50 border-b border-white/[0.04]">{r.materialA}</td>
                      <td className="px-6 py-4 text-white/50 border-b border-white/[0.04]">{r.materialB}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
