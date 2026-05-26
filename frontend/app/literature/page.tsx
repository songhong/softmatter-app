"use client";

import { useState } from "react";

const SAMPLE_DATA = [
  { id: 1, title: "Rheological Properties of Polymer Solutions: A Comprehensive Review", authors: "Smith J., Johnson A., Williams R.", year: 2023, category: "流变学", material: "高分子溶液", journal: "Macromolecules", abstract: "本文系统综述了聚合物溶液的流变学性质，包括剪切变稀、剪切增稠、触变性等非牛顿流体行为。讨论了分子量、浓度、温度对流变行为的影响，并介绍了流变学在聚合物加工中的应用。", keywords: ["流变学", "聚合物溶液", "非牛顿流体", "剪切变稀"] },
  { id: 2, title: "Self-assembly of Block Copolymers in Selective Solvents", authors: "Zhang L., Li H., Wang X.", year: 2024, category: "自组装", material: "嵌段共聚物", journal: "ACS Nano", abstract: "研究了嵌段共聚物在选择性溶剂中的自组装行为。通过调节溶剂组成和温度，实现了从球形胶束到柱状胶束再到层状结构的形貌转变。利用SAXS和TEM表征了组装体的周期性结构。", keywords: ["自组装", "嵌段共聚物", "胶束", "SAXS"] },
  { id: 3, title: "Pickering Emulsions Stabilized by Nanoparticles: Mechanisms and Applications", authors: "Wang Y., Chen S., Liu M.", year: 2023, category: "乳液", material: "纳米粒子", journal: "Langmuir", abstract: "综述了纳米粒子稳定的Pickering乳液的稳定机制。讨论了粒子润湿性、尺寸、形状对乳液类型和稳定性的影响。介绍了Pickering乳液在食品、化妆品和药物递送中的应用。", keywords: ["Pickering乳液", "纳米粒子", "乳液稳定", "润湿性"] },
  { id: 4, title: "Hydrogel Network Structure and Mechanical Properties", authors: "Chen J., Liu W., Zhang Q.", year: 2024, category: "水凝胶", material: "聚乙烯醇", journal: "Advanced Materials", abstract: "研究了PVA水凝胶的网络结构与力学性能关系。通过冷冻解冻循环法制备了物理交联水凝胶，利用流变学和拉伸测试表征了力学性能。发现增加循环次数可显著提高凝胶强度。", keywords: ["水凝胶", "PVA", "力学性能", "冷冻解冻"] },
  { id: 5, title: "Critical Micelle Concentration of Surfactants: Measurement Methods", authors: "Johnson K., Brown T., Davis M.", year: 2022, category: "表面活性剂", material: "SDS/CTAB", journal: "Journal of Colloid and Interface Science", abstract: "比较了测量临界胶束浓度(CMC)的多种方法，包括表面张力法、电导率法、荧光探针法和光散射法。讨论了各方法的优缺点和适用范围。", keywords: ["CMC", "表面活性剂", "表面张力", "电导率"] },
  { id: 6, title: "Dynamic Light Scattering in Colloidal Systems", authors: "Brown A., Davis R.", year: 2023, category: "表征方法", material: "胶体", journal: "Nanoscale", abstract: "介绍了动态光散射(DLS)技术在胶体体系表征中的应用。讨论了粒径测量原理、PDI的意义以及Zeta电位的测量方法。提供了实验数据分析的最佳实践。", keywords: ["DLS", "胶体", "粒径分布", "Zeta电位"] },
  { id: 7, title: "Rheology of Soft Matter: From Fundamentals to Applications", authors: "Anderson P., Thompson R.", year: 2023, category: "流变学", material: "软物质", journal: "Soft Matter", abstract: "全面介绍了软物质流变学的基础理论和应用。涵盖线性粘弹性、非线性流变行为、时间依赖性流变学等内容。讨论了流变学在聚合物、胶体、液晶等软物质体系中的应用。", keywords: ["流变学", "软物质", "粘弹性", "线性粘弹"] },
  { id: 8, title: "Stimuli-Responsive Hydrogels: Design and Biomedical Applications", authors: "Kim S., Lee J., Park H.", year: 2024, category: "水凝胶", material: "智能水凝胶", journal: "Chemical Reviews", abstract: "综述了刺激响应水凝胶的设计策略和生物医学应用。讨论了温度、pH、光、电场等刺激响应机制。介绍了在药物递送、组织工程和生物传感中的应用进展。", keywords: ["智能水凝胶", "刺激响应", "药物递送", "组织工程"] },
  { id: 9, title: "Surfactant Self-Assembly: Micelles, Vesicles, and Beyond", authors: "Garcia M., Martinez L.", year: 2023, category: "自组装", material: "表面活性剂", journal: "Current Opinion in Colloid & Interface Science", abstract: "讨论了表面活性剂自组装形成的各种有序结构，包括胶束、囊泡、层状相和六方相。分析了分子结构、浓度和环境条件对自组装形貌的影响。", keywords: ["自组装", "表面活性剂", "胶束", "囊泡"] },
  { id: 10, title: "Nanoemulsions: Formation, Stability, and Applications", authors: "Robinson T., Clark D.", year: 2024, category: "乳液", material: "纳米乳液", journal: "Food Chemistry", abstract: "研究了纳米乳液的制备方法、稳定性和应用。比较了高能法和低能法制备纳米乳液的优缺点。讨论了纳米乳液在食品、化妆品和药物递送中的应用。", keywords: ["纳米乳液", "乳液稳定性", "食品", "药物递送"] },
  { id: 11, title: "Polymer Nanocomposites: Structure-Property Relationships", authors: "Wilson E., Taylor S.", year: 2023, category: "纳米粒子", material: "聚合物纳米复合材料", journal: "Polymer", abstract: "研究了聚合物纳米复合材料的结构-性能关系。讨论了纳米粒子的分散状态、界面相互作用对力学性能、热性能和阻隔性能的影响。", keywords: ["纳米复合材料", "聚合物", "结构-性能", "界面"] },
  { id: 12, title: "Colloidal Crystals: Self-Assembly and Photonic Applications", authors: "Harris J., Lewis K.", year: 2024, category: "表征方法", material: "胶体晶体", journal: "Nature Materials", abstract: "研究了胶体粒子的自组装形成光子晶体的过程。利用小角X射线散射(SAXS)和扫描电镜(SEM)表征了晶体结构。讨论了胶体晶体在光子学和传感器中的应用。", keywords: ["胶体晶体", "光子晶体", "SAXS", "SEM"] },
  { id: 13, title: "Thixotropy in Complex Fluids: Mechanisms and Rheological Models", authors: "Nelson R., Carter M.", year: 2023, category: "流变学", material: "复杂流体", journal: "Rheologica Acta", abstract: "综述了复杂流体中触变性的机制和流变学模型。讨论了结构破坏和恢复的动力学过程。介绍了触变性在涂料、食品和生物医学中的应用。", keywords: ["触变性", "复杂流体", "流变学模型", "结构恢复"] },
  { id: 14, title: "Double Network Hydrogels: Tough and Soft Materials", authors: "Yamamoto K., Tanaka M.", year: 2024, category: "水凝胶", material: "双网络水凝胶", journal: "Advanced Functional Materials", abstract: "研究了双网络水凝胶的设计原理和力学性能。第一层网络提供刚性，第二层网络提供韧性。讨论了双网络水凝胶在软骨修复和人工肌肉中的应用。", keywords: ["双网络水凝胶", "韧性", "软骨修复", "人工肌肉"] },
  { id: 15, title: "Emulsion Polymerization: Kinetics and Morphology Control", authors: "White D., Green P.", year: 2023, category: "乳液", material: "聚合物乳液", journal: "Macromolecular Rapid Communications", abstract: "研究了乳液聚合的动力学和形貌控制。讨论了乳化剂浓度、引发剂类型和温度对聚合速率和粒子形貌的影响。介绍了核壳结构粒子的制备方法。", keywords: ["乳液聚合", "动力学", "核壳结构", "形貌控制"] },
  { id: 16, title: "Surface Tension Measurement Techniques: A Comparative Study", authors: "Adams B., Baker C.", year: 2022, category: "表面活性剂", material: "表面活性剂溶液", journal: "Journal of Chemical Education", abstract: "比较了测量表面张力的多种技术，包括吊片法、吊环法、最大气泡压力法和悬滴法。讨论了各方法的精度、适用范围和操作要点。", keywords: ["表面张力", "测量方法", "吊片法", "悬滴法"] },
  { id: 17, title: "Atomic Force Microscopy of Soft Materials", authors: "Scott R., Young T.", year: 2024, category: "表征方法", material: "软物质", journal: "ACS Applied Materials & Interfaces", abstract: "介绍了原子力显微镜(AFM)在软物质表征中的应用。讨论了轻敲模式、力曲线测量和纳米压痕技术。提供了水凝胶、聚合物薄膜和生物样品的成像最佳实践。", keywords: ["AFM", "软物质", "纳米压痕", "力曲线"] },
  { id: 18, title: "Polyelectrolyte Complexes: Formation and Applications", authors: "Evans M., Turner P.", year: 2023, category: "自组装", material: "聚电解质", journal: "Biomacromolecules", abstract: "研究了聚电解质复合物的形成机制和应用。讨论了电荷比、离子强度和pH对复合物形成的影响。介绍了在药物递送和基因治疗中的应用。", keywords: ["聚电解质", "复合物", "药物递送", "基因治疗"] },
  { id: 19, title: "Microfluidic Emulsification: Droplet Generation and Control", authors: "Patel S., Kumar R.", year: 2024, category: "乳液", material: "微流控液滴", journal: "Lab on a Chip", abstract: "研究了微流控技术制备单分散乳液液滴的方法。讨论了流速比、表面活性剂浓度和通道几何对液滴尺寸和均匀性的影响。", keywords: ["微流控", "乳液", "液滴", "单分散"] },
  { id: 20, title: "Viscoelastic Properties of Polymer Melts and Solutions", authors: "King L., Hall N.", year: 2023, category: "流变学", material: "聚合物熔体", journal: "Journal of Rheology", abstract: "研究了聚合物熔体和溶液的粘弹性性质。利用振荡剪切实验表征了储能模量和损耗模量。讨论了时温等效原理和WLF方程的应用。", keywords: ["粘弹性", "聚合物", "储能模量", "时温等效"] },
  { id: 21, title: "Nanoparticle Synthesis and Surface Modification", authors: "Allen M., Wright D.", year: 2024, category: "纳米粒子", material: "功能化纳米粒子", journal: "Chemistry of Materials", abstract: "综述了纳米粒子的合成方法和表面改性技术。讨论了溶胶-凝胶法、水热法和微乳液法制备纳米粒子。介绍了硅烷化、聚合物接枝等表面改性方法。", keywords: ["纳米粒子", "表面改性", "溶胶-凝胶", "硅烷化"] },
  { id: 22, title: "Zeta Potential Measurement and Colloidal Stability", authors: "Mitchell R., Cooper J.", year: 2023, category: "表征方法", material: "胶体分散体", journal: "Langmuir", abstract: "研究了Zeta电位测量在胶体稳定性评估中的应用。讨论了电泳光散射原理和Smoluchowski模型。分析了pH、离子强度和表面活性剂对Zeta电位的影响。", keywords: ["Zeta电位", "胶体稳定性", "电泳光散射", "Smoluchowski"] },
  { id: 23, title: "Supramolecular Hydrogels: Non-covalent Crosslinking Strategies", authors: "Fujimoto Y., Sato K.", year: 2024, category: "水凝胶", material: "超分子水凝胶", journal: "Angewandte Chemie", abstract: "综述了超分子水凝胶的非共价交联策略，包括氢键、主客体相互作用、疏水作用和静电作用。讨论了超分子水凝胶的自修复、形状记忆和刺激响应特性。", keywords: ["超分子水凝胶", "非共价交联", "自修复", "形状记忆"] },
  { id: 24, title: "Polymer Brush Surfaces: Synthesis and Wettability", authors: "Clarkson P., Hughes Q.", year: 2023, category: "自组装", material: "聚合物刷", journal: "Soft Matter", abstract: "研究了聚合物刷表面的合成方法和润湿性。讨论了接枝到和接枝从两种策略。分析了刷层厚度、 grafting密度和化学组成对表面润湿性的影响。", keywords: ["聚合物刷", "润湿性", "接枝", "表面改性"] },
  { id: 25, title: "Creaming and Sedimentation in Emulsions: Theory and Practice", authors: "Edwards S., Gray W.", year: 2022, category: "乳液", material: "乳液", journal: "Food Hydrocolloids", abstract: "讨论了乳液中乳化和沉降的理论和实践。分析了Stokes定律、絮凝和 Ostwald熟化对乳液稳定性的影响。介绍了防止乳液分层的策略。", keywords: ["乳化", "沉降", "Stokes定律", "乳液稳定性"] },
  { id: 26, title: "Small Angle X-ray Scattering for Soft Matter Characterization", authors: "Morrison D., Henderson T.", year: 2024, category: "表征方法", material: "软物质", journal: "IUCrJ", abstract: "介绍了小角X射线散射(SAXS)在软物质表征中的应用。讨论了SAXS数据分析方法和模型拟合。提供了胶束、囊泡和嵌段共聚物的SAXS表征案例。", keywords: ["SAXS", "软物质", "小角散射", "模型拟合"] },
  { id: 27, title: "Smart Polymers: Thermoresponsive and pH-Responsive Systems", authors: "Campbell R., Stewart L.", year: 2024, category: "表面活性剂", material: "智能聚合物", journal: "Progress in Polymer Science", abstract: "综述了智能聚合物的温度响应和pH响应系统。讨论了PNIPAM、聚丙烯酸等典型智能聚合物的响应机制和应用。介绍了在药物递送、传感器和智能涂层中的应用。", keywords: ["智能聚合物", "温度响应", "pH响应", "PNIPAM"] },
];

const CATEGORIES = ["全部", "流变学", "自组装", "乳液", "水凝胶", "表面活性剂", "表征方法", "纳米粒子"];

const CATEGORY_COLORS: Record<string, string> = {
  "流变学": "from-indigo-500 to-purple-500",
  "自组装": "from-cyan-500 to-blue-500",
  "乳液": "from-purple-500 to-pink-500",
  "水凝胶": "from-pink-500 to-rose-500",
  "表面活性剂": "from-amber-500 to-orange-500",
  "表征方法": "from-emerald-500 to-teal-500",
  "纳米粒子": "from-rose-500 to-pink-500",
};

export default function LiteraturePage() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("全部");
  const [selectedPaper, setSelectedPaper] = useState<typeof SAMPLE_DATA[0] | null>(null);

  const filtered = SAMPLE_DATA.filter((r) => {
    const matchSearch = !search || r.title.toLowerCase().includes(search.toLowerCase()) || r.authors.toLowerCase().includes(search.toLowerCase()) || r.keywords.some(k => k.includes(search));
    const matchCat = category === "全部" || r.category === category;
    return matchSearch && matchCat;
  });

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-lit)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-lit" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-cyan">文献</span><br />
            <span className="text-gradient-white">检索</span>
          </h1>
          <p className="body-glass max-w-lg">
            结构化文献记录搜索，支持关键词、材料体系、年份筛选
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Search */}
        <div className="card-glass p-8 mb-8">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-lit2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-lit2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#06b6d4"/>
                </linearGradient>
              </defs>
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            搜索文献
          </div>
          <input
            type="text"
            className="input-glass"
            placeholder="搜索标题、作者、关键词..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Categories */}
        <div className="flex flex-wrap gap-3 mb-8">
          {CATEGORIES.map((c) => (
            <button
              key={c}
              onClick={() => setCategory(c)}
              className={`text-xs px-4 py-2 rounded-full transition-all ${
                category === c
                  ? "bg-gradient-to-r from-indigo-500 to-cyan-500 text-white shadow-lg shadow-indigo-500/20"
                  : "bg-white/[0.04] border border-white/[0.08] text-white/50 hover:border-white/[0.15] hover:text-white/70"
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* Results */}
        <div className="flex items-center gap-4 mb-8">
          <div className="caption-glass flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-lit3)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-lit3" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <path d="M14 2v6h6"/>
            </svg>
            检索结果
          </div>
          <div className="flex-1 h-px bg-white/[0.06]" />
          <div className="text-white/30 text-sm">{filtered.length} 条</div>
        </div>

        <div className="space-y-4">
          {filtered.map((paper) => {
            const color = CATEGORY_COLORS[paper.category] || "from-indigo-500 to-purple-500";
            return (
              <div
                key={paper.id}
                onClick={() => setSelectedPaper(paper)}
                className="card-glass p-6 group cursor-pointer"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center flex-shrink-0`}>
                      <span className="font-bold text-white text-sm">{paper.id}</span>
                    </div>
                    <div>
                      <span className="font-mono text-white/30 text-sm">{paper.year}</span>
                      <span className="text-white/20 mx-2">|</span>
                      <span className="text-white/40 text-sm">{paper.journal}</span>
                    </div>
                  </div>
                  <span className="tag-glass">{paper.category}</span>
                </div>
                <h3 className="text-xl font-bold mb-3 text-white/90 group-hover:text-white transition-colors">
                  {paper.title}
                </h3>
                <div className="text-white/40 text-sm">{paper.authors}</div>
                <div className="mt-4 pt-4 border-t border-white/[0.06] flex items-center justify-between">
                  <span className="text-white/30 text-xs">材料体系: {paper.material}</span>
                  <span className="text-indigo-400 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                    点击查看详情 →
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-16">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="url(#grad-empty-lit)" strokeWidth="1.5" className="mx-auto mb-4">
              <defs>
                <linearGradient id="grad-empty-lit" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#06b6d4"/>
                </linearGradient>
              </defs>
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            <div className="text-white/30">未找到匹配的文献</div>
          </div>
        )}
      </section>

      {/* Detail Modal */}
      {selectedPaper && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={() => setSelectedPaper(null)}>
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
          <div className="relative w-full max-w-2xl max-h-[80vh] overflow-y-auto card-glass p-8" onClick={(e) => e.stopPropagation()}>
            <div className="accent-top" />
            <button
              onClick={() => setSelectedPaper(null)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>

            <div className="flex items-center gap-3 mb-6">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${CATEGORY_COLORS[selectedPaper.category] || "from-indigo-500 to-purple-500"} flex items-center justify-center`}>
                <span className="font-bold text-white text-lg">{selectedPaper.id}</span>
              </div>
              <div>
                <span className="tag-glass">{selectedPaper.category}</span>
                <div className="text-white/40 text-sm mt-1">{selectedPaper.journal} · {selectedPaper.year}</div>
              </div>
            </div>

            <h2 className="text-2xl font-bold text-white/90 mb-4">{selectedPaper.title}</h2>
            <div className="text-white/50 text-sm mb-6">{selectedPaper.authors}</div>

            <div className="space-y-6">
              <div>
                <div className="caption-glass mb-2">摘要</div>
                <p className="text-white/60 text-sm leading-relaxed">{selectedPaper.abstract}</p>
              </div>

              <div>
                <div className="caption-glass mb-2">材料体系</div>
                <span className="text-white/70">{selectedPaper.material}</span>
              </div>

              <div>
                <div className="caption-glass mb-2">关键词</div>
                <div className="flex flex-wrap gap-2">
                  {selectedPaper.keywords.map((kw) => (
                    <span key={kw} className="text-xs px-3 py-1 rounded-full bg-white/[0.06] border border-white/[0.1] text-white/50">
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
