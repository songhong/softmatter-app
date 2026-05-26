"use client";

import { useState } from "react";

export default function ExperimentPage() {
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState<string | null>(null);

  const handleGenerate = () => {
    if (!goal.trim()) return;
    setLoading(true);
    setTimeout(() => {
      setPlan(`实验方案框架

研究目标：${goal}

实验材料：
- 聚乙烯醇 (PVA, Mw=130000)
- 去离子水
- 磷酸盐缓冲液 (PBS)

实验步骤：
1. 溶液配制：将 PVA 溶于 80°C 去离子水，配制 10 wt% 溶液
2. 交联处理：冷冻解冻循环法，-20°C 冷冻 12h，室温解冻 4h
3. 重复循环：重复 3 次以获得足够力学强度
4. 表征测试：流变学测试、溶胀率测量、SEM 形貌观察

预期结果：
- 水凝胶含水率 80-90%
- 压缩模量 0.1-1 MPa
- 三维多孔网络结构

安全提示：操作加热设备时注意防烫，使用液氮时佩戴防护手套`);
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-exp)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-exp" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ec4899"/>
                  <stop offset="100%" stopColor="#f472b6"/>
                </linearGradient>
              </defs>
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-pink">实验</span><br />
            <span className="text-gradient-purple">方案</span>
          </h1>
          <p className="body-glass max-w-lg">
            输入研究目标，生成教学版实验方案框架
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Input */}
        <div className="card-glass p-8 mb-12">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-exp2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-exp2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 16v-4m0-4h.01"/>
            </svg>
            研究目标
          </div>
          <textarea
            className="input-glass min-h-[120px] resize-y"
            placeholder="描述你的研究目标，例如：制备具有自修复性能的水凝胶..."
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          />
          <div className="mt-6 flex items-center justify-between">
            <div className="text-white/30 text-sm">AI 将生成实验方案框架</div>
            <button
              onClick={handleGenerate}
              disabled={!goal.trim() || loading}
              className="btn-glass disabled:opacity-50"
            >
              {loading ? (
                <>
                  <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" strokeDasharray="31.416" strokeDashoffset="10" />
                  </svg>
                  生成中...
                </>
              ) : (
                <>
                  生成方案
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Result */}
        {plan && (
          <div className="animate-fade-in-up">
            <div className="card-glass p-8">
              <div className="accent-top accent-top-pink" />
              <div className="flex items-center gap-4 mb-6">
                <span className="tag-glass">✓ 方案已生成</span>
                <span className="text-white/30 text-sm">仅供参考，需教师审核</span>
              </div>
              <div className="whitespace-pre-wrap text-white/60 leading-relaxed">
                {plan}
              </div>
            </div>

            <div className="mt-8 border-l-4 border-amber-500/50 p-6 rounded-r-xl bg-amber-500/[0.05]">
              <div className="flex items-center gap-2 mb-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth="2">
                  <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                <span className="text-amber-400 text-sm font-semibold">安全声明</span>
              </div>
              <p className="text-white/40 text-sm leading-relaxed">
                该实验方案仅为教学讨论框架，不构成可直接执行的实验操作 SOP。具体条件必须经教师审核后方可实施。
              </p>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!plan && !loading && (
          <div className="text-center py-24">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="url(#grad-empty-exp)" strokeWidth="1.5" className="mx-auto mb-6">
              <defs>
                <linearGradient id="grad-empty-exp" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#ec4899"/>
                  <stop offset="100%" stopColor="#f472b6"/>
                </linearGradient>
              </defs>
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
            </svg>
            <div className="headline-glass text-2xl text-white/30 mb-4">生成实验方案</div>
            <p className="text-white/30 max-w-md mx-auto">输入研究目标，系统将生成教学版实验方案框架</p>
          </div>
        )}
      </section>
    </div>
  );
}
