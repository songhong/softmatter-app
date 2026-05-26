"use client";

import { useState } from "react";

const DAILY_DATA = [
  { day: "Mon", questions: 12 },
  { day: "Tue", questions: 18 },
  { day: "Wed", questions: 15 },
  { day: "Thu", questions: 22 },
  { day: "Fri", questions: 28 },
  { day: "Sat", questions: 8 },
  { day: "Sun", questions: 5 },
];

const CATEGORY_DATA = [
  { name: "流变学", count: 45, pct: 29, color: "from-indigo-500 to-purple-500" },
  { name: "水凝胶", count: 32, pct: 21, color: "from-cyan-500 to-blue-500" },
  { name: "表面活性剂", count: 28, pct: 18, color: "from-purple-500 to-pink-500" },
  { name: "乳液", count: 22, pct: 14, color: "from-pink-500 to-rose-500" },
  { name: "表征方法", count: 18, pct: 12, color: "from-amber-500 to-orange-500" },
  { name: "其他", count: 11, pct: 7, color: "from-emerald-500 to-teal-500" },
];

const RECENT_QUESTIONS = [
  { q: "什么是剪切变稀现象？", cat: "流变学", confidence: "high", time: "14:32" },
  { q: "CMC 是什么？如何测量？", cat: "表面活性剂", confidence: "high", time: "13:45" },
  { q: "物理交联和化学交联水凝胶的区别", cat: "水凝胶", confidence: "medium", time: "11:20" },
  { q: "Pickering 乳液的稳定机制", cat: "乳液", confidence: "high", time: "10:08" },
  { q: "DLS 测量粒径的原理", cat: "表征方法", confidence: "low", time: "09:15" },
];

const CONFIDENCE_CONFIG: Record<string, { bg: string; text: string; label: string }> = {
  high: { bg: "bg-emerald-500/10", text: "text-emerald-400", label: "高" },
  medium: { bg: "bg-amber-500/10", text: "text-amber-400", label: "中" },
  low: { bg: "bg-rose-500/10", text: "text-rose-400", label: "低" },
};

export default function AnalyticsPage() {
  const [selectedDay, setSelectedDay] = useState<number | null>(null);
  const maxQ = Math.max(...DAILY_DATA.map((d) => d.questions));

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-analytics)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-analytics" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
              <path d="M18 20V10"/>
              <path d="M12 20V4"/>
              <path d="M6 20v-6"/>
            </svg>
            数据分析
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-purple">教师</span><br />
            <span className="text-gradient-cyan">分析</span>
          </h1>
          <p className="body-glass max-w-lg">
            学生问答统计、知识薄弱点分析
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16">
          {[
            { label: "总问答", value: "156", unit: "次", color: "from-indigo-500 to-purple-500" },
            { label: "本周新增", value: "23", unit: "次", color: "from-cyan-500 to-blue-500" },
            { label: "满意率", value: "87", unit: "%", color: "from-emerald-500 to-teal-500" },
            { label: "活跃学生", value: "34", unit: "人", color: "from-pink-500 to-rose-500" },
          ].map((stat) => (
            <div key={stat.label} className="card-glass p-6 text-center">
              <div className={`stat-number bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                {stat.value}
              </div>
              <div className="caption-glass mt-3">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Bar Chart */}
          <div className="card-glass p-8">
            <div className="accent-top" />
            <div className="caption-glass mb-4 flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-chart1)" strokeWidth="2">
                <defs>
                  <linearGradient id="grad-chart1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#6366f1"/>
                    <stop offset="100%" stopColor="#a855f7"/>
                  </linearGradient>
                </defs>
                <path d="M18 20V10"/>
                <path d="M12 20V4"/>
                <path d="M6 20v-6"/>
              </svg>
              每日趋势
            </div>
            <h3 className="text-xl font-bold mb-8 text-white/90">本周数据</h3>
            <div className="flex items-end gap-3 h-[220px]">
              {DAILY_DATA.map((d, i) => {
                const height = (d.questions / maxQ) * 100;
                const isSelected = selectedDay === i;
                return (
                  <div
                    key={d.day}
                    className="flex-1 flex flex-col items-center gap-2 cursor-pointer"
                    onClick={() => setSelectedDay(isSelected ? null : i)}
                  >
                    <div className={`font-mono text-xs transition-all ${isSelected ? "text-indigo-400 font-bold" : "text-white/30"}`}>
                      {d.questions}
                    </div>
                    <div className="w-full relative" style={{ height: "160px" }}>
                      <div
                        className={`absolute bottom-0 w-full rounded-t transition-all ${
                          isSelected
                            ? "bg-gradient-to-t from-indigo-400 to-purple-400 shadow-lg shadow-indigo-500/30"
                            : "bg-gradient-to-t from-indigo-500/80 to-purple-500/80 hover:from-indigo-400 hover:to-purple-400"
                        }`}
                        style={{ height: `${height}%`, minHeight: "8px" }}
                      />
                    </div>
                    <div className={`text-xs transition-all ${isSelected ? "text-indigo-400 font-semibold" : "text-white/30"}`}>
                      {d.day}
                    </div>
                  </div>
                );
              })}
            </div>
            {selectedDay !== null && (
              <div className="mt-4 p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
                <span className="text-indigo-400 text-sm font-medium">
                  {DAILY_DATA[selectedDay].day}: {DAILY_DATA[selectedDay].questions} 次问答
                </span>
              </div>
            )}
          </div>

          {/* Category Breakdown */}
          <div className="card-glass p-8">
            <div className="accent-top accent-top-cyan" />
            <div className="caption-glass mb-4 flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-chart2)" strokeWidth="2">
                <defs>
                  <linearGradient id="grad-chart2" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#06b6d4"/>
                    <stop offset="100%" stopColor="#22d3ee"/>
                  </linearGradient>
                </defs>
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <path d="M3 9h18M9 3v18"/>
              </svg>
              问题分布
            </div>
            <h3 className="text-xl font-bold mb-8 text-white/90">按知识领域</h3>
            <div className="space-y-5">
              {CATEGORY_DATA.map((c) => (
                <div key={c.name} className="group">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-white/70 group-hover:text-white/90 transition-colors">{c.name}</span>
                    <span className="font-mono text-xs text-white/30">{c.count} ({c.pct}%)</span>
                  </div>
                  <div className="w-full bg-white/[0.03] rounded-full h-3 overflow-hidden">
                    <div
                      className={`bg-gradient-to-r ${c.color} h-3 rounded-full transition-all duration-700 ease-out`}
                      style={{ width: `${c.pct}%`, minWidth: "12px" }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Questions */}
        <div>
          <div className="flex items-center gap-4 mb-8">
            <div className="caption-glass flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-recent)" strokeWidth="2">
                <defs>
                  <linearGradient id="grad-recent" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#ec4899"/>
                    <stop offset="100%" stopColor="#f472b6"/>
                  </linearGradient>
                </defs>
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
              最近问答
            </div>
            <div className="flex-1 h-px bg-white/[0.06]" />
          </div>

          <div className="card-glass overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="bg-white/[0.03]">
                  <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">问题</th>
                  <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">类别</th>
                  <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">置信度</th>
                  <th className="px-6 py-4 text-left caption-glass border-b border-white/[0.06]">时间</th>
                </tr>
              </thead>
              <tbody>
                {RECENT_QUESTIONS.map((r, i) => {
                  const conf = CONFIDENCE_CONFIG[r.confidence];
                  return (
                    <tr key={i} className="hover:bg-white/[0.02] transition-colors cursor-pointer">
                      <td className="px-6 py-4 font-medium text-white/80 border-b border-white/[0.04]">{r.q}</td>
                      <td className="px-6 py-4 border-b border-white/[0.04]">
                        <span className="tag-glass">{r.cat}</span>
                      </td>
                      <td className="px-6 py-4 border-b border-white/[0.04]">
                        <span className={`${conf.bg} ${conf.text} text-xs font-semibold px-2 py-1 rounded-full`}>
                          {conf.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 font-mono text-sm text-white/30 border-b border-white/[0.04]">{r.time}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Insights */}
        <div className="mt-16 card-glass p-8">
          <div className="accent-top accent-top-purple" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-insight)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-insight" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#f59e0b"/>
                  <stop offset="100%" stopColor="#f97316"/>
                </linearGradient>
              </defs>
              <path d="M12 2L2 7l10 5 10-5-10-5z"/>
              <path d="M2 17l10 5 10-5"/>
              <path d="M2 12l10 5 10-5"/>
            </svg>
            教学建议
          </div>
          <h3 className="text-xl font-bold mb-6 text-white/90">知识薄弱点分析</h3>
          <div className="space-y-4">
            {[
              { num: "1", title: "流变学概念需加强", desc: "29% 的问题集中在流变学领域，建议增加流变学实验演示和概念讲解", color: "from-indigo-500 to-purple-500" },
              { num: "2", title: "表征方法理解不足", desc: "部分学生对 DLS、Zeta 电位原理理解不深，建议结合实验操作教学", color: "from-cyan-500 to-blue-500" },
              { num: "3", title: "水凝胶知识掌握较好", desc: "相关问题置信度较高，可适当减少课时，将时间分配给薄弱环节", color: "from-emerald-500 to-teal-500" },
              { num: "4", title: "乳液稳定性是常见疑问", desc: "Pickering 乳液和乳液类型判断问题较多，建议增加相关案例分析", color: "from-pink-500 to-rose-500" },
            ].map((item) => (
              <div key={item.num} className="flex gap-4 items-start">
                <div className={`w-8 h-8 rounded-lg bg-gradient-to-r ${item.color} flex items-center justify-center flex-shrink-0`}>
                  <span className="font-bold text-white text-sm">{item.num}</span>
                </div>
                <div>
                  <div className="font-medium text-white/80 mb-1">{item.title}</div>
                  <p className="text-white/40 text-sm">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
