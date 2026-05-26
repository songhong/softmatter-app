"use client";

import { useState } from "react";

const SAMPLE_RECIPES = [
  { id: 1, name: "PVA 水凝胶制备", materials: "聚乙烯醇(PVA, Mw=130000)、去离子水", procedure: "1. 将 PVA 粉末溶于 80°C 去离子水中，配制 10 wt% 溶液\n2. 搅拌 2h 至完全溶解\n3. 倒入模具，-20°C 冷冻 12h\n4. 室温解冻 4h\n5. 重复冷冻解冻循环 3 次", safety: "low", category: "水凝胶", temp: "80°C / -20°C", time: "3天", result: "透明水凝胶，含水率 85%，压缩模量 0.3 MPa" },
  { id: 2, name: "SDS 胶束溶液配制", materials: "十二烷基硫酸钠(SDS)、去离子水", procedure: "1. 称取 SDS 粉末\n2. 加入去离子水，室温搅拌至完全溶解\n3. 配制不同浓度系列(0.1-10 mM)\n4. 静置脱气", safety: "low", category: "表面活性剂", temp: "室温", time: "30min", result: "透明溶液，CMC ≈ 8.2 mM" },
  { id: 3, name: "SiO2 纳米粒子合成(Stöber法)", materials: "正硅酸乙酯(TEOS)、氨水(25%)、无水乙醇", procedure: "1. 将氨水和去离子水加入乙醇中，搅拌均匀\n2. 逐滴加入 TEOS\n3. 室温反应 24h\n4. 离心洗涤 3 次\n5. 60°C 真空干燥", safety: "medium", category: "纳米粒子", temp: "室温", time: "24h", result: "单分散 SiO2 粒子，粒径 100-500 nm，PDI < 0.1" },
  { id: 4, name: "Pickering 乳液制备", materials: "改性 SiO2 粒子、石蜡油、去离子水", procedure: "1. 将 SiO2 粒子分散在水相中(1 wt%)\n2. 加入石蜡油(油水比 3:7)\n3. 高速剪切乳化 10000 rpm, 5min\n4. 室温储存", safety: "low", category: "乳液", temp: "室温", time: "10min", result: "白色乳液，液滴粒径 10-50 μm，稳定 > 30天" },
  { id: 5, name: "聚丙烯酰胺凝胶电泳(PAGE)", materials: "丙烯酰胺(30%)、甲叉双丙烯酰胺(1%)、APS(10%)、TEMED、Tris-甘氨酸缓冲液", procedure: "1. 配制分离胶(12% Acrylamide)\n2. 灌胶，覆盖异丙醇\n3. 聚合 30min 后配制浓缩胶(5%)\n4. 插入梳子，聚合 30min\n5. 上样，电泳 120V, 1.5h\n6. 染色、脱色", safety: "high", category: "凝胶电泳", temp: "室温", time: "3h", result: "清晰蛋白条带，分辨率 < 5 kDa" },
  { id: 6, name: "脂质体制备(薄膜水化法)", materials: "卵磷脂、胆固醇、氯仿、PBS 缓冲液", procedure: "1. 将卵磷脂和胆固醇溶于氯仿\n2. 旋转蒸发除去有机溶剂，形成薄膜\n3. 加入 PBS 缓冲液水化\n4. 超声处理 10min\n5. 过滤(0.45 μm)除去大粒子", safety: "medium", category: "脂质体", temp: "40°C", time: "2h", result: "脂质体粒径 100-200 nm，包封率 60%" },
  { id: 7, name: "聚丙烯酸(PAA)水凝胶制备", materials: "丙烯酸、N,N'-亚甲基双丙烯酰胺(MBA)、APS、TEMED", procedure: "1. 将丙烯酸部分中和(中和度 70%)\n2. 加入交联剂 MBA\n3. 加入引发剂 APS 和促进剂 TEMED\n4. 倒入模具，室温聚合 2h\n5. 取出凝胶，去离子水浸泡除去未反应物", safety: "medium", category: "水凝胶", temp: "室温", time: "4h", result: "透明水凝胶，pH 响应性，溶胀率 200-800%" },
  { id: 8, name: "CTAB 胶束溶液配制", materials: "十六烷基三甲基溴化铵(CTAB)、去离子水", procedure: "1. 称取 CTAB 粉末\n2. 加入温热去离子水(40°C)\n3. 搅拌至完全溶解\n4. 配制浓度系列(0.1-20 mM)\n5. 室温平衡 24h", safety: "low", category: "表面活性剂", temp: "40°C", time: "30min", result: "透明溶液，CMC ≈ 0.9 mM" },
  { id: 9, name: "W/O 型乳液制备", materials: "Span 80、液体石蜡、去离子水", procedure: "1. 将 Span 80 溶于液体石蜡(5 wt%)\n2. 逐滴加入去离子水(水相体积分数 30%)\n3. 搅拌乳化 5000 rpm, 10min\n4. 室温储存", safety: "low", category: "乳液", temp: "室温", time: "15min", result: "白色粘稠乳液，液滴粒径 1-10 μm" },
  { id: 10, name: "金纳米粒子合成(Turkevich法)", materials: "氯金酸(HAuCl4)、柠檬酸三钠、去离子水", procedure: "1. 将氯金酸溶于去离子水，加热至沸腾\n2. 快速加入柠檬酸三钠溶液\n3. 继续加热搅拌 15min\n4. 溶液颜色变化：淡黄→紫红\n5. 冷却至室温", safety: "medium", category: "纳米粒子", temp: "100°C", time: "30min", result: "酒红色金纳米粒子胶体，粒径 ~15 nm，SPR 峰 520 nm" },
  { id: 11, name: "O/W 型乳液制备", materials: "Tween 80、液体石蜡、去离子水", procedure: "1. 将 Tween 80 溶于水相(3 wt%)\n2. 加入液体石蜡(油相体积分数 20%)\n3. 高速剪切乳化 10000 rpm, 5min\n4. 室温储存", safety: "low", category: "乳液", temp: "室温", time: "10min", result: "白色乳液，液滴粒径 1-5 μm，稳定 > 7天" },
  { id: 12, name: "壳聚糖/海藻酸钠聚电解质复合物", materials: "壳聚糖、海藻酸钠、氯化钙、醋酸", procedure: "1. 将壳聚糖溶于 1% 醋酸溶液\n2. 将海藻酸钠溶于去离子水\n3. 将壳聚糖溶液逐滴加入海藻酸钠溶液\n4. 加入 CaCl2 溶液交联\n5. 离心收集，洗涤", safety: "low", category: "聚电解质", temp: "室温", time: "2h", result: "白色微球，粒径 200-500 μm，载药率 30%" },
  { id: 13, name: "聚苯乙烯微球乳液聚合", materials: "苯乙烯、十二烷基硫酸钠(SDS)、过硫酸钾(KPS)、去离子水", procedure: "1. 将苯乙烯单体纯化除去阻聚剂\n2. 将 SDS 溶于去离子水\n3. 加入苯乙烯，氮气保护下搅拌乳化\n4. 升温至 70°C，加入 KPS 溶液\n5. 聚合反应 8h\n6. 冷却，过滤除去凝聚物", safety: "medium", category: "乳液聚合", temp: "70°C", time: "8h", result: "白色乳液，单分散 PS 微球，粒径 100-500 nm" },
  { id: 14, name: "温敏水凝胶(PNIPAM)制备", materials: "N-异丙基丙烯酰胺(NIPAM)、MBA、APS、TEMED", procedure: "1. 将 NIPAM 和 MBA 溶于去离子水\n2. 通氮气除氧 30min\n3. 加入 APS 和 TEMED\n4. 室温聚合 24h\n5. 取出凝胶，去离子水浸泡纯化", safety: "medium", category: "水凝胶", temp: "室温", time: "24h", result: "透明水凝胶，LCST ≈ 32°C，温度响应性溶胀/收缩" },
  { id: 15, name: "荧光纳米粒子制备", materials: "罗丹明B、正硅酸乙酯(TEOS)、氨水、乙醇", procedure: "1. 将罗丹明B溶于乙醇\n2. 加入 TEOS 和氨水\n3. 室温搅拌反应 12h\n4. 离心洗涤 3 次\n5. 真空干燥", safety: "medium", category: "纳米粒子", temp: "室温", time: "12h", result: "粉色荧光纳米粒子，粒径 50-100 nm，荧光量子产率 30%" },
  { id: 16, name: "纤维素纳米晶(CNC)制备", materials: "微晶纤维素、硫酸(64%)、去离子水", procedure: "1. 将微晶纤维素加入预热的硫酸溶液\n2. 45°C 搅拌水解 2h\n3. 加入去离子水终止反应\n4. 离心洗涤至中性\n5. 超声分散", safety: "high", category: "纳米粒子", temp: "45°C", time: "4h", result: "白色 CNC 悬浮液，棒状形貌，长度 100-300 nm" },
  { id: 17, name: "聚多巴胺纳米粒子制备", materials: "盐酸多巴胺、Tris-HCl 缓冲液(pH 8.5)", procedure: "1. 将盐酸多巴胺溶于 Tris-HCl 缓冲液\n2. 室温搅拌反应 24h\n3. 溶液颜色变化：无色→棕色→黑色\n4. 离心洗涤 3 次\n5. 冷冻干燥", safety: "low", category: "纳米粒子", temp: "室温", time: "24h", result: "黑色聚多巴胺纳米粒子，粒径 50-200 nm，表面富含儿茶酚基团" },
  { id: 18, name: "琼脂糖凝胶电泳", materials: "琼脂糖、TAE 缓冲液、溴化乙锭(EB)", procedure: "1. 配制 1% 琼脂糖/TAE 溶液\n2. 微波加热溶解\n3. 冷却至 60°C，加入 EB\n4. 倒入凝胶模具，插入梳子\n5. 凝固后上样，电泳 100V, 30min\n6. 紫外灯下观察", safety: "high", category: "凝胶电泳", temp: "60°C", time: "1h", result: "清晰 DNA 条带，分辨率 100 bp" },
  { id: 19, name: "海藻酸钙微球制备", materials: "海藻酸钠、氯化钙、去离子水", procedure: "1. 将海藻酸钠溶于去离子水(2 wt%)\n2. 用注射器将溶液逐滴加入 CaCl2 溶液(2 wt%)\n3. 接触即形成凝胶微球\n4. 固化 30min\n5. 收集微球，去离子水洗涤", safety: "low", category: "水凝胶", temp: "室温", time: "1h", result: "透明微球，粒径 1-3 mm，离子交联凝胶" },
  { id: 20, name: "聚乳酸-羟基乙酸共聚物(PLGA)微球制备", materials: "PLGA、二氯甲烷(DCM)、聚乙烯醇(PVA)、去离子水", procedure: "1. 将 PLGA 溶于 DCM(5 wt%)\n2. 将 PVA 溶于去离子水(1 wt%)\n3. 将 PLGA/DCM 溶液加入 PVA 水溶液\n4. 高速剪切乳化\n5. 挥发除去 DCM\n6. 离心收集微球", safety: "medium", category: "药物载体", temp: "室温", time: "4h", result: "白色微球，粒径 10-100 μm，载药率 10-20%" },
  { id: 21, name: "碳量子点水热合成", materials: "柠檬酸、乙二胺、去离子水", procedure: "1. 将柠檬酸和乙二胺溶于去离子水\n2. 转移至水热反应釜\n3. 180°C 反应 6h\n4. 冷却，透析纯化\n5. 冷冻干燥", safety: "medium", category: "纳米粒子", temp: "180°C", time: "6h", result: "黄色碳量子点溶液，粒径 3-8 nm，荧光量子产率 50%" },
  { id: 22, name: "聚氨酯水凝胶制备", materials: "聚乙二醇(PEG)、异佛尔酮二异氰酸酯(IPDI)、二月桂酸二丁基锡(DBTDL)、去离子水", procedure: "1. 将 PEG 和 IPDI 混合\n2. 加入催化剂 DBTDL\n3. 60°C 反应 2h\n4. 加入去离子水分散\n5. 室温固化 24h", safety: "medium", category: "水凝胶", temp: "60°C", time: "26h", result: "透明水凝胶，力学强度可调，生物相容性好" },
  { id: 23, name: "聚苯胺纳米纤维制备", materials: "苯胺、过硫酸铵(APS)、盐酸", procedure: "1. 将苯胺溶于盐酸溶液\n2. 将 APS 溶于盐酸溶液\n3. 快速混合，冰浴搅拌\n4. 反应 12h\n5. 过滤洗涤，真空干燥", safety: "medium", category: "纳米粒子", temp: "0°C", time: "12h", result: "深绿色聚苯胺纳米纤维，直径 50-100 nm，导电性良好" },
  { id: 24, name: "微凝胶制备(PNIPAM微球)", materials: "NIPAM、MBA、SDS、KPS、去离子水", procedure: "1. 将 NIPAM、MBA、SDS 溶于去离子水\n2. 通氮气除氧\n3. 升温至 70°C\n4. 加入 KPS 溶液引发聚合\n5. 反应 4h\n6. 透析纯化", safety: "medium", category: "微凝胶", temp: "70°C", time: "4h", result: "白色微凝胶悬浮液，粒径 200-500 nm，温敏性" },
  { id: 25, name: "聚电解质多层膜制备", materials: "聚丙烯酸(PAA)、聚烯丙胺盐酸盐(PAH)、NaCl、去离子水", procedure: "1. 配制 PAA 和 PAH 溶液(1 mg/mL, 含 0.15M NaCl)\n2. 将基底交替浸入 PAA 和 PAH 溶液\n3. 每次浸入 10min，中间用水洗涤\n4. 重复 10 个循环\n5. 氮气吹干", safety: "low", category: "聚电解质", temp: "室温", time: "4h", result: "透明薄膜，厚度 ~100 nm，均匀平整" },
  { id: 26, name: "有机凝胶制备", materials: "二苄叉山梨醇(DBS)、环己烷", procedure: "1. 将 DBS 加入环己烷(2 wt%)\n2. 加热至 80°C 溶解\n3. 冷却至室温\n4. 静置形成凝胶\n5. 倒置不流动即为凝胶", safety: "low", category: "有机凝胶", temp: "80°C → 室温", time: "1h", result: "透明有机凝胶，纤维网络结构，凝胶强度 0.5 kPa" },
  { id: 27, name: "聚丙烯酰胺微球反相乳液聚合", materials: "丙烯酰胺、Span 80、Tween 80、液体石蜡、APS、TEMED", procedure: "1. 将丙烯酰胺溶于去离子水\n2. 将 Span 80 和 Tween 80 溶于液体石蜡\n3. 将水相加入油相，搅拌乳化\n4. 通氮气除氧\n5. 加入 APS 和 TEMED\n6. 室温聚合 4h", safety: "medium", category: "乳液聚合", temp: "室温", time: "4h", result: "白色微球悬浮液，粒径 1-10 μm，吸水倍率 500-1000" },
  { id: 28, name: "壳聚糖纳米粒子制备", materials: "壳聚糖、三聚磷酸钠(TPP)、醋酸", procedure: "1. 将壳聚糖溶于 1% 醋酸溶液\n2. 将 TPP 溶于去离子水\n3. 将 TPP 溶液逐滴加入壳聚糖溶液\n4. 磁力搅拌 30min\n5. 离心收集，洗涤", safety: "low", category: "纳米粒子", temp: "室温", time: "1h", result: "白色壳聚糖纳米粒子，粒径 100-300 nm，表面正电荷" },
  { id: 29, name: "聚丙烯酸-丙烯酰胺共聚物水凝胶", materials: "丙烯酸、丙烯酰胺、MBA、APS、TEMED", procedure: "1. 将丙烯酸部分中和\n2. 加入丙烯酰胺和 MBA\n3. 加入 APS 和 TEMED\n4. 室温聚合 24h\n5. 取出凝胶，浸泡纯化", safety: "medium", category: "水凝胶", temp: "室温", time: "24h", result: "透明水凝胶，高吸水性，溶胀率 500-1500%" },
  { id: 30, name: "聚苯乙烯-b-聚丙烯酸嵌段共聚物自组装", materials: "PS-b-PAA 嵌段共聚物、THF、去离子水", procedure: "1. 将 PS-b-PAA 溶于 THF\n2. 逐滴加入去离子水\n3. 透析除去 THF\n4. 形成胶束或囊泡\n5. 表征形貌和尺寸", safety: "low", category: "自组装", temp: "室温", time: "2天", result: "球形胶束或囊泡，粒径 50-200 nm，核壳结构" },
];

const SAFETY_CONFIG: Record<string, { bg: string; text: string; label: string; gradient: string }> = {
  low: { bg: "bg-emerald-500/10", text: "text-emerald-400", label: "低风险", gradient: "from-emerald-500 to-teal-500" },
  medium: { bg: "bg-amber-500/10", text: "text-amber-400", label: "中风险", gradient: "from-amber-500 to-orange-500" },
  high: { bg: "bg-rose-500/10", text: "text-rose-400", label: "高风险", gradient: "from-rose-500 to-pink-500" },
};

export default function RecipesPage() {
  const [search, setSearch] = useState("");
  const [safetyFilter, setSafetyFilter] = useState("all");
  const [selectedRecipe, setSelectedRecipe] = useState<typeof SAMPLE_RECIPES[0] | null>(null);

  const filtered = SAMPLE_RECIPES.filter((r) => {
    const matchSearch = !search || r.name.includes(search) || r.materials.includes(search) || r.category.includes(search);
    const matchSafety = safetyFilter === "all" || r.safety === safetyFilter;
    return matchSearch && matchSafety;
  });

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="section-glass pt-24 pb-16">
        <div className="animate-fade-in">
          <div className="caption-glass mb-6 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="url(#grad-recipe)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-recipe" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <path d="M9 3h6v8l5 8H4l5-8V3z"/>
            </svg>
            AI 工具
          </div>
          <h1 className="headline-glass text-6xl mb-8">
            <span className="text-gradient-purple">实验</span><br />
            <span className="text-gradient-pink">配方</span>
          </h1>
          <p className="body-glass max-w-lg">
            查询实验配方，安全等级标注
          </p>
        </div>
      </section>

      <div className="divider-glass mx-8" />

      {/* Content */}
      <section className="section-glass">
        {/* Search */}
        <div className="card-glass p-8 mb-8">
          <div className="caption-glass mb-4 flex items-center gap-2">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="url(#grad-recipe2)" strokeWidth="2">
              <defs>
                <linearGradient id="grad-recipe2" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#6366f1"/>
                  <stop offset="100%" stopColor="#a855f7"/>
                </linearGradient>
              </defs>
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            搜索配方
          </div>
          <input
            type="text"
            className="input-glass"
            placeholder="搜索配方名称、材料、类别..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Safety Filter */}
        <div className="flex flex-wrap gap-3 mb-8">
          {[
            { value: "all", label: "全部" },
            { value: "low", label: "低风险" },
            { value: "medium", label: "中风险" },
            { value: "high", label: "高风险" },
          ].map((s) => (
            <button
              key={s.value}
              onClick={() => setSafetyFilter(s.value)}
              className={`text-xs px-4 py-2 rounded-full transition-all ${
                safetyFilter === s.value
                  ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg shadow-indigo-500/20"
                  : "bg-white/[0.04] border border-white/[0.08] text-white/50 hover:border-white/[0.15] hover:text-white/70"
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>

        {/* Recipes */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((recipe) => {
            const safety = SAFETY_CONFIG[recipe.safety];
            return (
              <div
                key={recipe.id}
                onClick={() => setSelectedRecipe(recipe)}
                className="card-glass p-6 group cursor-pointer"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-r ${safety.gradient} flex items-center justify-center flex-shrink-0`}>
                      <span className="font-bold text-white text-sm">{recipe.id}</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-white/90 group-hover:text-white transition-colors">
                        {recipe.name}
                      </h3>
                      <div className="text-white/30 text-xs mt-1">{recipe.category}</div>
                    </div>
                  </div>
                  <span className={`${safety.bg} ${safety.text} text-xs font-semibold px-3 py-1 rounded-full`}>
                    {safety.label}
                  </span>
                </div>
                <div className="space-y-2 text-sm">
                  <div>
                    <span className="text-white/30">材料：</span>
                    <span className="text-white/50">{recipe.materials.length > 40 ? recipe.materials.slice(0, 40) + "..." : recipe.materials}</span>
                  </div>
                </div>
                <div className="mt-4 pt-3 border-t border-white/[0.04] flex items-center justify-between">
                  <div className="flex gap-4 text-xs text-white/30">
                    <span>{recipe.temp}</span>
                    <span>{recipe.time}</span>
                  </div>
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
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="url(#grad-empty-recipe)" strokeWidth="1.5" className="mx-auto mb-4">
              <defs>
                <linearGradient id="grad-empty-recipe" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#a855f7"/>
                  <stop offset="100%" stopColor="#ec4899"/>
                </linearGradient>
              </defs>
              <path d="M9 3h6v8l5 8H4l5-8V3z"/>
            </svg>
            <div className="text-white/30">未找到匹配的配方</div>
          </div>
        )}

        {/* Safety Notice */}
        <div className="mt-12 border-l-4 border-amber-500/50 p-6 rounded-r-xl bg-amber-500/[0.05]">
          <div className="flex items-center gap-2 mb-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" strokeWidth="2">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <span className="text-amber-400 text-sm font-semibold">安全提示</span>
          </div>
          <p className="text-white/40 text-sm leading-relaxed">
            高风险配方需要教师在场指导方可实施。所有实验操作前请确认安全防护措施到位。
          </p>
        </div>
      </section>

      {/* Detail Modal */}
      {selectedRecipe && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4" onClick={() => setSelectedRecipe(null)}>
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
          <div className="relative w-full max-w-2xl max-h-[80vh] overflow-y-auto card-glass p-8" onClick={(e) => e.stopPropagation()}>
            <div className="accent-top accent-top-pink" />
            <button
              onClick={() => setSelectedRecipe(null)}
              className="absolute top-4 right-4 w-8 h-8 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>

            <div className="flex items-center gap-3 mb-6">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${SAFETY_CONFIG[selectedRecipe.safety].gradient} flex items-center justify-center`}>
                <span className="font-bold text-white text-lg">{selectedRecipe.id}</span>
              </div>
              <div>
                <h2 className="text-xl font-bold text-white/90">{selectedRecipe.name}</h2>
                <div className="flex items-center gap-2 mt-1">
                  <span className="tag-glass">{selectedRecipe.category}</span>
                  <span className={`${SAFETY_CONFIG[selectedRecipe.safety].bg} ${SAFETY_CONFIG[selectedRecipe.safety].text} text-xs font-semibold px-2 py-0.5 rounded-full`}>
                    {SAFETY_CONFIG[selectedRecipe.safety].label}
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <div className="caption-glass mb-2">实验材料</div>
                <p className="text-white/60 text-sm">{selectedRecipe.materials}</p>
              </div>

              <div>
                <div className="caption-glass mb-2">实验步骤</div>
                <div className="text-white/60 text-sm whitespace-pre-line leading-relaxed">{selectedRecipe.procedure}</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                  <div className="caption-glass mb-1">温度条件</div>
                  <div className="text-white/70 text-sm">{selectedRecipe.temp}</div>
                </div>
                <div className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                  <div className="caption-glass mb-1">反应时间</div>
                  <div className="text-white/70 text-sm">{selectedRecipe.time}</div>
                </div>
              </div>

              <div>
                <div className="caption-glass mb-2">预期结果</div>
                <p className="text-white/60 text-sm">{selectedRecipe.result}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
