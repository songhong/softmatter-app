"use client";

import Link from "next/link";

const STATS = [
  { value: "60", label: "知识条目", color: "from-indigo-500 to-purple-500", icon: "📚" },
  { value: "27", label: "文献记录", color: "from-cyan-500 to-blue-500", icon: "📄" },
  { value: "30", label: "实验配方", color: "from-purple-500 to-pink-500", icon: "🧪" },
  { value: "9", label: "功能模块", color: "from-pink-500 to-rose-500", icon: "⚙️" },
];

const FEATURES = [
  {
    number: "01",
    title: "智能问答",
    description: "基于 RAG 检索增强生成，回答课程概念问题，展示证据来源",
    href: "/qa",
    tag: "RAG",
    gradient: "from-indigo-500 to-purple-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    ),
  },
  {
    number: "02",
    title: "文献检索",
    description: "结构化文献库检索，支持材料体系、实验方法、表征技术",
    href: "/literature",
    tag: "27 篇",
    gradient: "from-cyan-500 to-blue-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
      </svg>
    ),
  },
  {
    number: "03",
    title: "实验配方",
    description: "查询配方材料、浓度、工艺、表征结果，标注安全等级",
    href: "/recipes",
    tag: "30 条",
    gradient: "from-purple-500 to-pink-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9 3h6v8l5 8H4l5-8V3z"/>
        <path d="M9 3h6"/>
      </svg>
    ),
  },
  {
    number: "04",
    title: "实验方案",
    description: "输入研究目标，生成教学版实验方案框架",
    href: "/experiment",
    tag: "AI",
    gradient: "from-pink-500 to-rose-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
      </svg>
    ),
  },
  {
    number: "05",
    title: "表征分析",
    description: "基于规则库分析表征结果，给出结构解释建议",
    href: "/characterization",
    tag: "9 规则",
    gradient: "from-amber-500 to-orange-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M12 2v4m0 12v4m-10-10h4m12 0h4"/>
      </svg>
    ),
  },
  {
    number: "06",
    title: "材料对比",
    description: "对比不同材料体系的结构、性能和应用场景",
    href: "/compare",
    tag: "结构化",
    gradient: "from-emerald-500 to-teal-500",
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="M3 9h18M9 3v18"/>
      </svg>
    ),
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="section-glass pt-24 pb-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div className="animate-fade-in">
            <div className="caption-glass mb-6 flex items-center gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" strokeWidth="2">
                <defs>
                  <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#6366f1"/>
                    <stop offset="100%" stopColor="#06b6d4"/>
                  </linearGradient>
                </defs>
                <path d="M9 3h6v8l5 8H4l5-8V3z"/>
              </svg>
              AI 教学工作台
            </div>
            <h1 className="headline-glass text-6xl lg:text-7xl mb-8">
              <span className="text-gradient-white">探索</span><br />
              <span className="text-gradient-purple">软物质</span><br />
              <span className="text-gradient-cyan">的奥秘</span>
            </h1>
            <p className="body-glass max-w-lg mb-10">
              面向软物质课程与实验教学的智能辅助系统。基于 RAG 检索增强生成技术，
              让每一个回答都有据可依。
            </p>
            <div className="flex gap-4">
              <Link href="/qa" className="btn-glass">
                开始体验
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              <Link href="/settings" className="btn-glass-outline">
                系统设置
              </Link>
            </div>
          </div>

          <div className="animate-fade-in-up delay-200">
            <div className="grid grid-cols-2 gap-4">
              {STATS.map((stat, i) => (
                <div key={stat.label} className="card-glass p-6 text-center">
                  <div className="text-2xl mb-2">{stat.icon}</div>
                  <div className={`stat-number bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                    {stat.value}
                  </div>
                  <div className="caption-glass mt-3 text-xs">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Divider */}
      <div className="divider-glass mx-8" />

      {/* Features Section */}
      <section className="section-glass">
        <div className="mb-16">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <path d="M3 9h18M9 3v18"/>
            </svg>
            核心功能
          </div>
          <h2 className="headline-glass text-4xl lg:text-5xl">
            <span className="text-gradient-white">六大模块</span>
          </h2>
          <p className="body-glass mt-6 max-w-2xl">
            覆盖软物质课程学习的完整场景，从概念理解到实验设计
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature, i) => (
            <Link
              key={feature.number}
              href={feature.href}
              className="card-glass p-8 group relative overflow-hidden"
            >
              {/* Top accent bar */}
              <div className={`accent-top bg-gradient-to-r ${feature.gradient}`} />

              {/* Background number */}
              <div className="absolute top-6 right-6 text-7xl font-bold text-white/[0.03] group-hover:text-white/[0.06] transition-colors">
                {feature.number}
              </div>

              <div className="relative">
                {/* Icon */}
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.gradient} bg-opacity-20 flex items-center justify-center mb-6 text-white/80`}
                  style={{ background: `linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(6, 182, 212, 0.2))` }}>
                  {feature.icon}
                </div>

                {/* Tag */}
                <span className="tag-glass mb-4 inline-block">{feature.tag}</span>

                <h3 className="text-xl font-bold mb-3 text-white group-hover:text-white/90 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-white/40 text-sm leading-relaxed">
                  {feature.description}
                </p>

                <div className="mt-6 flex items-center gap-2 text-white/50 group-hover:text-white/70 transition-colors">
                  <span className="text-xs font-semibold uppercase tracking-wider">了解更多</span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Architecture Section */}
      <section className="section-glass">
        <div className="card-glass p-8">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad3)" strokeWidth="2">
              <defs>
                <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 2v4m0 12v4m-10-10h4m12 0h4"/>
            </svg>
            系统架构
          </div>
          <h2 className="headline-glass text-3xl mb-8">
            <span className="text-gradient-cyan">技术栈</span>
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: "Next.js", role: "前端框架", color: "from-indigo-500 to-purple-500" },
              { name: "FastAPI", role: "后端服务", color: "from-cyan-500 to-blue-500" },
              { name: "Ollama", role: "大语言模型", color: "from-purple-500 to-pink-500" },
              { name: "TF-IDF", role: "文本检索", color: "from-pink-500 to-rose-500" },
            ].map((tech) => (
              <div key={tech.name} className="text-center p-4 rounded-xl bg-white/[0.03] border border-white/[0.06] hover:border-white/[0.12] transition-all">
                <div className={`text-xl font-bold bg-gradient-to-r ${tech.color} bg-clip-text text-transparent mb-1`}>
                  {tech.name}
                </div>
                <div className="caption-glass text-[10px]">{tech.role}</div>
              </div>
            ))}
          </div>

          <div className="mt-8 p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
            <div className="flex items-center justify-between flex-wrap gap-4 text-xs text-white/40">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500" />
                <span>请求流：用户 → 前端 → 后端 → 模型</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500" />
                <span>响应流：模型 → 后端 → 前端 → 用户</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500" />
                <span>数据流：后端 ↔ CSV</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="section-glass">
        <div className="border-l-4 border-gradient-to-b from-indigo-500 to-cyan-500 p-6 rounded-r-xl bg-white/[0.02]">
          <div className="caption-glass text-amber-400 mb-3 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            安全声明
          </div>
          <p className="text-white/50 text-sm leading-relaxed">
            本系统输出的实验方案仅为教学参考框架，不构成可直接执行的实验操作 SOP。
            具体试剂选择、浓度、温度、时间和操作条件必须经教师或实验室安全规范审核后方可实施。
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/[0.06] py-8 px-8">
        <div className="max-w-[1400px] mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-indigo-500 to-cyan-500 flex items-center justify-center">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5">
                <path d="M9 3h6v8l5 8H4l5-8V3z"/>
              </svg>
            </div>
            <span className="font-bold text-sm">SoftMatterGPT</span>
          </div>
          <div className="text-white/30 text-xs">
            © 2026 人工智能导论课程项目
          </div>
        </div>
      </footer>
    </div>
  );
}
