"use client";

import { useState } from "react";

const RULES = [
  { id: 1, keyword: "剪切变稀", method: "流变学", interpretation: "表观粘度随剪切速率增加而降低，表明体系具有非牛顿流体行为。常见于聚合物溶液、悬浮液等体系，由分子取向或结构破坏引起。", application: "聚合物加工、涂料喷涂、血液流动", detail: "在流变学测试中，通过稳态剪切实验测量不同剪切速率下的粘度。当粘度随剪切速率增加而降低时，称为剪切变稀行为。这是由于高分子链在剪切场中沿流动方向取向，或胶体粒子的结构破坏导致的。" },
  { id: 2, keyword: "剪切增稠", method: "流变学", interpretation: "高剪切速率下粒子簇形成导致粘度上升。常见于浓悬浮液体系，由流体力学相互作用引起粒子聚集。", application: "防弹衣、智能流体、食品加工", detail: "剪切增稠现象通常在高剪切速率下出现，当粒子间的流体力学相互作用超过热运动时，粒子形成水动力簇(hydroclusters)，导致流动阻力急剧增加。这一现象在浓悬浮液(如二氧化硅/聚乙二醇体系)中尤为明显。" },
  { id: 3, keyword: "粒径分布窄", method: "DLS", interpretation: "PDI<0.3 表明粒子均一性好，体系稳定。动态光散射通过分析散射光的自相关函数获得粒径分布信息。", application: "纳米粒子质量控制、药物载体评价", detail: "动态光散射(DLS)测量粒子的扩散系数，通过Stokes-Einstein方程计算流体力学半径。多分散系数(PDI)反映粒径分布的宽度，PDI<0.1为单分散，0.1-0.3为中等分散，>0.3为宽分布。" },
  { id: 4, keyword: "凝胶化", method: "流变学", interpretation: "G'=G'' 交叉点对应凝胶点，储能模量>损耗模量表明凝胶形成。凝胶化是溶胶-凝胶转变的关键标志。", application: "水凝胶制备、食品凝胶、混凝土固化", detail: "在小振幅振荡剪切实验中，当储能模量(G')等于损耗模量(G'')时，对应凝胶点。凝胶化后，G'>G''且两者对频率的依赖性减弱，表明形成弹性固体网络。这一方法广泛用于监测交联反应和凝胶化动力学。" },
  { id: 5, keyword: "CMC", method: "表面张力", interpretation: "表面张力-浓度曲线拐点即为临界胶束浓度。CMC 是表面活性剂的重要参数，反映其自组装能力。", application: "洗涤剂配方、乳液稳定、药物增溶", detail: "临界胶束浓度(CMC)是表面活性剂分子开始形成胶束的最低浓度。通过测量不同浓度下的表面张力，绘制γ-lgc曲线，曲线的转折点即为CMC。常用的测量方法还包括电导率法、荧光探针法等。" },
  { id: 6, keyword: "层状结构", method: "XRD", interpretation: "出现周期性衍射峰表明有序层状排列。层间距可通过布拉格方程计算。", application: "液晶表征、层状材料、薄膜结构", detail: "小角X射线衍射(SAXS/XRD)中，当样品具有周期性层状结构时，会出现一系列等间距的衍射峰。通过布拉格方程 2d sinθ = nλ 可以计算层间距d。峰的数量和宽度反映结构的有序度和缺陷。" },
  { id: 7, keyword: "球形形貌", method: "SEM/TEM", interpretation: "电镜下观察到规则球形粒子，粒径均一。扫描电镜(SEM)和透射电镜(TEM)是表征纳米粒子形貌的金标准。", application: "纳米粒子合成表征、胶体粒子质量控制", detail: "SEM通过聚焦电子束扫描样品表面，获取表面形貌信息；TEM通过电子束穿透超薄样品，获取内部结构信息。对于纳米粒子，SEM分辨率约1-10 nm，TEM可达原子级分辨率(0.1 nm)。" },
  { id: 8, keyword: "溶胀平衡", method: "重量法", interpretation: "溶胀率趋于恒定值表明达到溶胀平衡。溶胀率是水凝胶的重要性能参数。", application: "水凝胶性能评价、药物缓释研究", detail: "将干凝胶置于溶剂中，定时称量质量变化。溶胀率SR = (Wt - W0)/W0 × 100%，其中Wt为t时刻质量，W0为干凝胶质量。当连续两次测量的溶胀率变化<5%时，认为达到溶胀平衡。" },
  { id: 9, keyword: "Zeta电位", method: "电泳光散射", interpretation: "Zeta电位绝对值>30mV表明胶体体系稳定。Zeta电位反映粒子表面电荷状态。", application: "胶体稳定性预测、蛋白质溶液稳定性", detail: "Zeta电位是剪切面(shear plane)处的电位，通过电泳光散射测量。|ζ|>30 mV 表示体系稳定，|ζ|>60 mV 表示高度稳定。pH对Zeta电位有显著影响，等电点(IEP)处ζ=0，胶体最不稳定。" },
  { id: 10, keyword: "粘弹性", method: "流变学", interpretation: "储能模量(G')和损耗模量(G'')同时存在，表明体系兼具弹性和粘性特征。G'/G''比值反映体系的固液特性。", application: "食品质构、涂料流挂、生物材料力学", detail: "粘弹性材料在振荡剪切中表现出弹性和粘性的双重特征。G'反映弹性(可恢复的形变)，G''反映粘性(不可恢复的形变)。当G'>G''时，体系以弹性为主(类固体)；当G''>G''时，以粘性为主(类液体)。" },
  { id: 11, keyword: "乳液类型", method: "电导率", interpretation: "O/W型乳液电导率高(水连续相)，W/O型电导率低(油连续相)。电导率法是判断乳液类型的经典方法。", application: "乳液配方优化、化妆品稳定性", detail: "乳液类型可通过电导率法快速判断。水包油(O/W)型乳液以水为连续相，电导率较高(μS/cm级)；油包水(W/O)型乳液以油为连续相，电导率很低(nS/cm级)。稀释法和染色法也可用于乳液类型判断。" },
  { id: 12, keyword: "结晶度", method: "DSC", interpretation: "DSC曲线上出现尖锐的吸热峰表明结晶态存在。熔融焓与结晶度成正比。", application: "聚合物结晶研究、药物多晶型筛选", detail: "差示扫描量热法(DSC)通过测量样品与参比物的热流差来分析热转变。结晶聚合物在升温时出现熔融吸热峰，峰温对应熔点(Tm)，峰面积对应熔融焓(ΔHm)。结晶度Xc = ΔHm/ΔHm0 × 100%，ΔHm0为完全结晶样品的熔融焓。" },
  { id: 13, keyword: "分子量分布", method: "GPC/SEC", interpretation: "凝胶渗透色谱(GPC)可获得数均分子量(Mn)、重均分子量(Mw)和多分散系数(PDI=Mw/Mn)。", application: "聚合物质量控制、合成反应监控", detail: "GPC/SEC基于分子在多孔凝胶中的体积排阻效应分离不同分子量的聚合物。大分子先流出，小分子后流出。通过标准曲线可计算分子量分布。PDI越接近1，分子量分布越窄。" },
  { id: 14, keyword: "接触角", method: "接触角测量", interpretation: "接触角<90°为亲水表面，>90°为疏水表面。接触角反映固体表面的润湿性。", application: "表面改性评价、涂层性能测试", detail: "将液滴置于固体表面，测量气-液-固三相接触点处的夹角即为接触角(θ)。θ<90°表示表面亲水，θ>90°表示表面疏水，θ>150°为超疏水。Young方程描述了接触角与表面张力的关系：γSV - γSL = γLV cosθ。" },
  { id: 15, keyword: "荧光光谱", method: "荧光光谱", interpretation: "荧光发射峰位置和强度反映荧光团的微环境变化。荧光猝灭可用于研究分子间相互作用。", application: "蛋白质构象研究、CMC测定、传感器", detail: "荧光光谱通过测量分子吸收激发光后发射的荧光来分析物质性质。荧光探针(如芘、尼罗红)对微环境极性敏感，可用于研究胶束形成、蛋白质折叠等过程。荧光猝灭实验(如碘离子猝灭)可提供分子可及性信息。" },
  { id: 16, keyword: "红外光谱", method: "FTIR", interpretation: "特征吸收峰对应特定化学键振动模式。红外光谱是化学结构鉴定的重要工具。", application: "聚合物鉴定、反应监控、表面分析", detail: "傅里叶变换红外光谱(FTIR)通过测量样品对红外光的吸收来分析化学结构。常见特征峰：O-H伸缩(3200-3600 cm⁻¹)、C=O伸缩(1700 cm⁻¹)、C-H伸缩(2800-3000 cm⁻¹)等。ATR模式可直接测量固体和液体样品。" },
  { id: 17, keyword: "核磁共振", method: "NMR", interpretation: "化学位移反映原子核的化学环境。NMR可提供分子结构、动力学和分子间相互作用信息。", application: "聚合物结构鉴定、反应机理研究", detail: "核磁共振(NMR)通过测量原子核在磁场中的共振吸收来分析分子结构。¹H NMR可提供氢原子的化学环境信息，¹³C NMR提供碳骨架信息。二维NMR(如COSY、NOESY)可揭示原子间的连接和空间距离。" },
  { id: 18, keyword: "热重分析", method: "TGA", interpretation: "质量随温度变化的曲线反映样品的热稳定性和组成。失重台阶对应特定的热分解过程。", application: "聚合物热稳定性评价、填料含量测定", detail: "热重分析(TGA)在程序升温条件下测量样品质量变化。不同温度区间的失重对应不同的分解过程：吸附水(<100°C)、有机物分解(200-600°C)、无机物分解(>600°C)。残余质量可计算填料或灰分含量。" },
];

const METHOD_COLORS: Record<string, string> = {
  "流变学": "from-indigo-500 to-purple-500",
  "DLS": "from-cyan-500 to-blue-500",
  "表面张力": "from-purple-500 to-pink-500",
  "XRD": "from-pink-500 to-rose-500",
  "SEM/TEM": "from-amber-500 to-orange-500",
  "重量法": "from-emerald-500 to-teal-500",
  "电泳光散射": "from-rose-500 to-pink-500",
  "DSC": "from-orange-500 to-amber-500",
  "GPC/SEC": "from-blue-500 to-indigo-500",
  "接触角测量": "from-teal-500 to-emerald-500",
  "荧光光谱": "from-violet-500 to-purple-500",
  "FTIR": "from-sky-500 to-cyan-500",
  "NMR": "from-fuchsia-500 to-pink-500",
  "TGA": "from-red-500 to-orange-500",
  "电导率": "from-lime-500 to-green-500",
};

export default function CharacterizationPage() {
  const [search, setSearch] = useState("");
  const [selectedRule, setSelectedRule] = useState<typeof RULES[0] | null>(null);

  const filtered = RULES.filter((r) => !search || r.keyword.includes(search) || r.method.includes(search) || r.interpretation.includes(search));

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-char)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-char" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#f59e0b"/>
                  <stop offset="100%" stopColor="#f97316"/>
                </linearGradient>
              </defs>
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 2v4m0 12v4m-10-10h4m12 0h4"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-white">表征</span><br />
            <span className="text-gradient-cyan">分析</span>
          </h1>
          <p className="body-glass max-w-lg">
            基于规则库分析表征结果，给出结构解释建议
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Search */}
        <div className="card-glass p-8 mb-8">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-char2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-char2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#06b6d4"/>
                </linearGradient>
              </defs>
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            搜索规则
          </div>
          <input
            type="text"
            className="input-glass"
            placeholder="搜索关键词、表征方法..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Rules */}
        <div className="flex items-center gap-4 mb-8">
          <div className="caption-glass flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-char3)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-char3" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            分析规则库
          </div>
          <div className="flex-1 h-px bg-white/[0.06]" />
          <div className="text-white/30 text-sm">{filtered.length} 条</div>
        </div>

        <div className="space-y-4">
          {filtered.map((rule) => {
            const color = METHOD_COLORS[rule.method] || "from-indigo-500 to-purple-500";
            return (
              <div
                key={rule.id}
                onClick={() => setSelectedRule(rule)}
                className="card-glass p-6 group cursor-pointer"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${color} flex items-center justify-center flex-shrink-0`}>
                      <span className="font-bold text-white text-sm">{rule.id}</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-white/90 group-hover:text-white transition-colors">
                        {rule.keyword}
                      </h3>
                      <span className="tag-glass mt-1 inline-block">{rule.method}</span>
                    </div>
                  </div>
                  <span className="text-indigo-400 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                    点击查看详情 →
                  </span>
                </div>
                <p className="text-white/40 text-sm leading-relaxed pl-[52px]">
                  {rule.interpretation.length > 80 ? rule.interpretation.slice(0, 80) + "..." : rule.interpretation}
                </p>
              </div>
            );
          })}
        </div>

        {/* Custom Analysis */}
        <div className="mt-12 card-glass p-8">
          <div className="accent-top accent-top-cyan" />
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-char4)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-char4" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4"/>
                  <stop offset="100%" stopColor="#22d3ee"/>
                </linearGradient>
              </defs>
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            自定义分析
          </div>
          <h3 className="text-2xl font-bold mb-6 text-white/90">输入表征数据</h3>
          <textarea
            className="input-glass min-h-[140px] resize-y mb-6"
            placeholder="粘贴表征数据或描述结果..."
          />
          <button className="btn-glass">
            分析结果
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </button>
        </div>
      </section>

      {/* Detail Modal */}
      {selectedRule && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={() => setSelectedRule(null)}>
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
          <div className="relative w-full max-w-2xl max-h-[80vh] overflow-y-auto card-glass p-8" onClick={(e) => e.stopPropagation()}>
            <div className="accent-top accent-top-cyan" />
            <button
              onClick={() => setSelectedRule(null)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>

            <div className="flex items-center gap-3 mb-6">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${METHOD_COLORS[selectedRule.method] || "from-indigo-500 to-purple-500"} flex items-center justify-center`}>
                <span className="font-bold text-white text-lg">{selectedRule.id}</span>
              </div>
              <div>
                <h2 className="text-xl font-bold text-white/90">{selectedRule.keyword}</h2>
                <span className="tag-glass mt-1 inline-block">{selectedRule.method}</span>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <div className="caption-glass mb-2">结果解释</div>
                <p className="text-white/60 text-sm leading-relaxed">{selectedRule.interpretation}</p>
              </div>

              <div>
                <div className="caption-glass mb-2">详细说明</div>
                <p className="text-white/60 text-sm leading-relaxed">{selectedRule.detail}</p>
              </div>

              <div>
                <div className="caption-glass mb-2">应用场景</div>
                <p className="text-white/60 text-sm">{selectedRule.application}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
