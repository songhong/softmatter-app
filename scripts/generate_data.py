"""
Generate all data files for SoftMatterGPT task-SW-002.

All data is based on publicly available soft matter science concepts.
Literature entries are curated examples (not from actual PDF extraction).
Recipe entries with is_example=true are teaching demonstrations.
No real PDFs are downloaded or parsed.
"""

import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filepath: Path, fieldnames: list[str], rows: list[dict]):
    """Write rows to a CSV file with utf-8-sig encoding."""
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written {len(rows)} rows -> {filepath}")


# =========================================================================
# 1. softmatter_knowledge.csv
# =========================================================================
def generate_knowledge():
    fieldnames = ["id", "title", "category", "content", "source", "keywords"]
    rows = [
        # --- Basic Concepts ---
        {
            "id": "K001",
            "title": "软物质的定义与特征",
            "category": "基本概念",
            "content": "软物质是指由大分子或胶体粒子等组成的一类材料，其特征能量尺度在室温热能(kT)附近，因此受热涨落影响显著。典型的软物质包括高分子、表面活性剂、胶体、液晶和生物大分子等。软物质的核心特征是自组装性和对外界刺激的敏感性。",
            "source": "课程讲义",
            "keywords": "软物质,定义,自组装,热涨落,kT"
        },
        {
            "id": "K002",
            "title": "高分子的基本概念",
            "category": "高分子科学",
            "content": "高分子是由重复单体单元通过共价键连接而成的大分子。按来源分为天然高分子(如纤维素、蛋白质)和合成高分子(如聚乙烯、聚苯乙烯)。高分子的关键参数包括分子量(数均分子量Mn和重均分子量Mw)、多分散性指数(PDI=Mw/Mn)和链构象。",
            "source": "课程讲义",
            "keywords": "高分子,单体,分子量,多分散性,链构象"
        },
        {
            "id": "K003",
            "title": "Flory-Huggins 理论",
            "category": "高分子科学",
            "content": "Flory-Huggins 理论描述高分子溶液的混合自由能: ΔG_mix/(kT) = n_1 ln φ_1 + n_2 ln φ_2 + n_1 φ_2 χ。其中χ为Flory-Huggins相互作用参数，反映高分子-溶剂相互作用。χ>0.5时倾向于相分离，χ<0.5时混合性较好。",
            "source": "课程讲义",
            "keywords": "Flory-Huggins,混合自由能,相互作用参数,相分离,高分子溶液"
        },
        {
            "id": "K004",
            "title": "胶体分散体系",
            "category": "胶体科学",
            "content": "胶体是分散相尺寸在1nm-1μm范围内的分散体系。按分散介质分类: 溶胶(液态)、气溶胶(气态)、固溶胶(固态)。胶体粒子的稳定性由DLVO理论描述，考虑van der Waals引力和双电层排斥力的平衡。",
            "source": "课程讲义",
            "keywords": "胶体,分散体系,DLVO理论,van der Waals,双电层"
        },
        {
            "id": "K005",
            "title": "表面活性剂与胶束",
            "category": "表面活性剂",
            "content": "表面活性剂是同时含有亲水头基和疏水尾链的两亲分子。在水中超过临界胶束浓度(CMC)后自组装形成胶束。按头基类型分为阴离子型(如SDS)、阳离子型(如CTAB)、非离子型(如Triton X-100)和两性型(如卵磷脂)。",
            "source": "课程讲义",
            "keywords": "表面活性剂,胶束,CMC,两亲分子,SDS,CTAB"
        },
        {
            "id": "K006",
            "title": "牛顿流体与非牛顿流体",
            "category": "流变学",
            "content": "牛顿流体的粘度不随剪切速率变化(如水、甘油)。非牛顿流体包括: 剪切变稀(假塑性)流体(粘度随剪切速率增大而降低，如番茄酱)、剪切增稠(胀流性)流体(如玉米淀粉悬浮液)、宾汉流体(存在屈服应力，如牙膏)。",
            "source": "课程讲义",
            "keywords": "牛顿流体,非牛顿流体,剪切变稀,剪切增稠,宾汉流体,屈服应力"
        },
        {
            "id": "K007",
            "title": "剪切变稀现象",
            "category": "流变学",
            "content": "剪切变稀是非牛顿流体最常见的行为，表现为表观粘度随剪切速率增大而降低。在高分子溶液中，原因是高分子链沿流动方向取向排列，减少了链间缠结。日常例子包括洗发水、番茄酱和油漆的流动行为。",
            "source": "课程讲义",
            "keywords": "剪切变稀,假塑性,粘度,高分子取向,缠结"
        },
        {
            "id": "K008",
            "title": "触变性",
            "category": "流变学",
            "content": "触变性是指材料在剪切作用下结构被破坏(粘度降低)，静置后结构逐渐恢复(粘度升高)的时间依赖性行为。与单纯剪切变稀不同，触变性涉及时间维度。典型例子是酸奶: 搅拌后变稀，静置后恢复。",
            "source": "课程讲义",
            "keywords": "触变性,时间依赖,结构恢复,剪切历史"
        },
        {
            "id": "K009",
            "title": "水凝胶基础",
            "category": "水凝胶",
            "content": "水凝胶是能吸收大量水分而不溶解的三维交联网络。按交联方式分为: 物理交联(氢键、离子相互作用、疏水缔合)和化学交联(共价键)。物理交联水凝胶通常可自修复和可注射，化学交联水凝胶更稳定但不可逆。",
            "source": "课程讲义",
            "keywords": "水凝胶,交联,物理交联,化学交联,自修复,可注射"
        },
        {
            "id": "K010",
            "title": "乳液类型与稳定",
            "category": "乳液",
            "content": "乳液是两种不相溶液体形成的分散体系。水包油型(O/W)乳液如牛奶，油包水型(W/O)乳液如黄油。乳化剂降低界面张力并阻止液滴聚并。Pickering乳液使用固体粒子(如SiO2纳米粒子)代替传统表面活性剂稳定乳液。",
            "source": "课程讲义",
            "keywords": "乳液,O/W,W/O,乳化剂,Pickering乳液,界面张力"
        },
        {
            "id": "K011",
            "title": "液晶的基本分类",
            "category": "液晶",
            "content": "液晶是介于液体和晶体之间的中间态。按形成条件分为热致液晶和溶致液晶。按分子排列分为: 向列相(分子取向有序但位置无序)、近晶相(分子取向和层内位置有序)、胆甾相(分子排列呈螺旋结构，可选择性反射特定波长光)。",
            "source": "课程讲义",
            "keywords": "液晶,向列相,近晶相,胆甾相,热致,溶致"
        },
        {
            "id": "K012",
            "title": "自组装原理",
            "category": "基本概念",
            "content": "自组装是分子或纳米结构通过非共价相互作用(氢键、疏水作用、静电作用、van der Waals力等)自发形成有序结构的过程。驱动力是系统自由能最小化。典型例子: 表面活性剂形成胶束、脂质双分子层、嵌段共聚物微相分离。",
            "source": "课程讲义",
            "keywords": "自组装,非共价相互作用,自由能最小化,胶束,微相分离"
        },
        {
            "id": "K013",
            "title": "DLVO理论",
            "category": "胶体科学",
            "content": "DLVO(Deryaguin-Landau-Verwey-Overbeek)理论描述胶体粒子间的相互作用势能，是van der Waals吸引势和双电层排斥势的叠加。势能曲线有两个极小值(主极小和次极小)和一个势垒。势垒高度决定胶体稳定性。",
            "source": "课程讲义",
            "keywords": "DLVO,van der Waals,双电层,势能曲线,胶体稳定性"
        },
        {
            "id": "K014",
            "title": "嵌段共聚物微相分离",
            "category": "高分子科学",
            "content": "嵌段共聚物由两种或多种不相容的聚合物链段通过共价键连接。由于链段间不相容但被共价键束缚，会发生微相分离形成周期性纳米结构(球、柱、层、双连续等)。相结构取决于各嵌段的体积分数f和Flory-Huggins参数χ与聚合度N的乘积χN。",
            "source": "课程讲义",
            "keywords": "嵌段共聚物,微相分离,纳米结构,χN,体积分数"
        },
        {
            "id": "K015",
            "title": "蠕虫状胶束",
            "category": "表面活性剂",
            "content": "蠕虫状胶束是表面活性剂分子自组装形成的柔性棒状结构，类似柔性高分子链。它们在水中可以缠结形成瞬态网络，表现出类似高分子溶液的粘弹性。蠕虫状胶束的长度由弯曲能和端盖能的平衡决定，可被剪切断链和自修复。",
            "source": "课程讲义",
            "keywords": "蠕虫状胶束,粘弹性,瞬态网络,柔性链,自修复"
        },
        {
            "id": "K016",
            "title": "表面张力与界面能",
            "category": "基本概念",
            "content": "表面张力是液体表面层分子受内部分子吸引而产生的收缩趋势，单位为N/m或mN/m。Young方程描述接触角与各界面张力的关系: γ_SG = γ_SL + γ_LG cosθ。表面活性剂通过降低表面张力改变润湿性。",
            "source": "课程讲义",
            "keywords": "表面张力,界面能,Young方程,接触角,润湿性"
        },
        {
            "id": "K017",
            "title": "高分子溶液的 θ 条件",
            "category": "高分子科学",
            "content": "在θ条件下，高分子链的排斥体积效应为零，链的行为类似于理想链(高斯链)。θ温度是χ=0.5对应的温度。在良溶剂(χ<0.5)中链舒展，在不良溶剂(χ>0.5)中链塌缩。均方回转半径Rg与聚合度N的关系: Rg ~ N^ν，ν在θ条件下为0.5，良溶剂中为0.588。",
            "source": "课程讲义",
            "keywords": "θ条件,θ温度,排斥体积,高斯链,良溶剂,不良溶剂"
        },
        {
            "id": "K018",
            "title": "凝胶渗透色谱(GPC)",
            "category": "表征方法",
            "content": "GPC/SEC是测定高分子分子量分布的标准方法。原理是不同大小的分子在多孔凝胶柱中的保留时间不同: 大分子先流出，小分子后流出。需要使用已知分子量的标准样品(如聚苯乙烯标准品)校准。可测得Mn、Mw和PDI。",
            "source": "课程讲义",
            "keywords": "GPC,SEC,分子量分布,保留时间,校准曲线,PDI"
        },
        {
            "id": "K019",
            "title": "流变测量基础",
            "category": "表征方法",
            "content": "流变测量研究材料的变形和流动行为。主要模式包括: 稳态剪切(测粘度曲线)、小振幅振荡剪切SAOS(测储能模量G'和损耗模量G'')、大振幅振荡剪切LAOS(测非线性响应)、蠕变与回复(测时间依赖行为)。G'>G''时材料表现为固体，G''>G'时表现为流体。",
            "source": "课程讲义",
            "keywords": "流变测量,SAOS,G',G'',粘度,蠕变"
        },
        {
            "id": "K020",
            "title": "SEM与TEM电子显微镜",
            "category": "表征方法",
            "content": "SEM(扫描电子显微镜)利用聚焦电子束扫描样品表面，通过二次电子成像观察表面形貌，分辨率可达nm级。TEM(透射电子显微镜)利用透射电子成像，可观察内部结构，分辨率更高(亚nm)。软物质样品通常需要冷冻或染色处理。",
            "source": "课程讲义",
            "keywords": "SEM,TEM,电子显微镜,形貌,分辨率,冷冻"
        },
        {
            "id": "K021",
            "title": "动态光散射(DLS)",
            "category": "表征方法",
            "content": "DLS通过测量散射光强度的时间涨落来确定胶体粒子或多分子聚集体的扩散系数，从而计算流体力学半径Rh。适用于1nm-1μm范围的粒子。可获得粒径分布信息。对于多分散体系需要使用CONTIN算法反演。",
            "source": "课程讲义",
            "keywords": "DLS,动态光散射,流体力学半径,扩散系数,粒径分布"
        },
        {
            "id": "K022",
            "title": "小角X射线散射(SAXS)",
            "category": "表征方法",
            "content": "SAXS用于表征1-100nm尺度的结构。通过分析散射强度I(q)与散射矢量q的关系获得结构信息。可用于测定纳米粒子尺寸、形状、胶束结构、嵌段共聚物微相分离周期等。Guinier分析可得到回转半径Rg。",
            "source": "课程讲义",
            "keywords": "SAXS,小角散射,纳米结构,Guinier分析,回转半径"
        },
        {
            "id": "K023",
            "title": "接触角测量",
            "category": "表征方法",
            "content": "接触角测量表征固体表面的润湿性。液滴与固体表面形成的夹角θ反映亲疏水性: θ<90°为亲水，θ>90°为疏水，θ>150°为超疏水。Young方程将接触角与各界面张力联系起来。可用于评价表面改性效果。",
            "source": "课程讲义",
            "keywords": "接触角,润湿性,亲水,疏水,超疏水,表面改性"
        },
        {
            "id": "K024",
            "title": "高分子的玻璃化转变温度",
            "category": "高分子科学",
            "content": "玻璃化转变温度Tg是高分子从玻璃态转变为高弹态的温度。Tg以下链段运动被冻结，材料呈硬而脆的玻璃态; Tg以上链段可以运动，材料呈软而韧的橡胶态。影响Tg的因素包括主链刚性、侧基体积、交联密度和增塑剂含量。常用DSC测定。",
            "source": "课程讲义",
            "keywords": "玻璃化转变温度,Tg,链段运动,DSC,玻璃态,高弹态"
        },
        {
            "id": "K025",
            "title": "聚合反应类型",
            "category": "高分子科学",
            "content": "主要聚合反应类型: 加成聚合(链式聚合，单体逐一加到活性链端，如乙烯聚合)、缩合聚合(逐步聚合，每步都生成小分子副产物，如聚酯合成)、开环聚合(环状单体开环后连接，如己内酰胺聚合)。活性聚合可精确控制分子量和PDI。",
            "source": "课程讲义",
            "keywords": "加成聚合,缩合聚合,开环聚合,活性聚合,分子量控制"
        },
        {
            "id": "K026",
            "title": "胶体粒子的Zeta电位",
            "category": "胶体科学",
            "content": "Zeta电位是胶体粒子剪切面处的电位，可通过电泳光散射测量。Zeta电位绝对值>30mV通常表示胶体体系稳定。pH值、离子强度和表面活性剂都会影响Zeta电位。等电点是Zeta电位为零时的pH值，此时胶体最不稳定。",
            "source": "课程讲义",
            "keywords": "Zeta电位,电泳,胶体稳定性,等电点,离子强度"
        },
        {
            "id": "K027",
            "title": "Pickering乳液",
            "category": "乳液",
            "content": "Pickering乳液是由固体粒子(而非传统表面活性剂)稳定的乳液。固体粒子吸附在油水界面上形成机械屏障阻止液滴聚并。常用粒子包括SiO2纳米粒子、粘土、淀粉颗粒和蛋白质聚集体。粒子的接触角决定乳液类型: 亲水粒子倾向稳定O/W，疏水粒子倾向稳定W/O。",
            "source": "课程讲义",
            "keywords": "Pickering乳液,固体粒子,界面吸附,接触角,SiO2"
        },
        {
            "id": "K028",
            "title": "高分子凝胶的溶胀行为",
            "category": "水凝胶",
            "content": "高分子凝胶的溶胀平衡由Flory-Rehner理论描述，是混合渗透压和弹性回缩力的平衡。交联密度越高溶胀度越低。在良溶剂中溶胀度大，不良溶剂中凝胶塌缩。聚N-异丙基丙烯酰胺(PNIPAM)在约32°C发生LCST相转变，由溶胀变为塌缩。",
            "source": "课程讲义",
            "keywords": "凝胶溶胀,Flory-Rehner理论,渗透压,交联密度,PNIPAM,LCST"
        },
        {
            "id": "K029",
            "title": "蛋白质作为软物质",
            "category": "生物软物质",
            "content": "蛋白质是天然的软物质，具有层次化结构(一级氨基酸序列、二级α螺旋和β折叠、三级三维折叠、四级多亚基组装)。蛋白质的自组装形成病毒外壳、淀粉样纤维等结构。蛋白质溶液的流变行为对生物加工很重要。",
            "source": "课程讲义",
            "keywords": "蛋白质,层次结构,自组装,α螺旋,β折叠,淀粉样纤维"
        },
        {
            "id": "K030",
            "title": "双亲分子的HLD方程",
            "category": "表面活性剂",
            "content": "HLD(Hydrophilic-Lipophilic Deviation)方程用于预测表面活性剂在油水体系中的相行为: HLD = ln(S) - k*ACN - α*ΔT + c_T + c_A。其中S为盐度，ACN为油相碳数，ΔT为温度偏移。HLD=0时表面活性剂亲水亲油平衡，形成最优微乳液。",
            "source": "课程讲义",
            "keywords": "HLD方程,亲水亲油平衡,微乳液,盐度,ACN"
        },
        {
            "id": "K031",
            "title": "增稠剂的流变调控",
            "category": "流变学",
            "content": "增稠剂通过不同机理调控体系流变行为: 高分子增稠剂(如卡波姆、HEC)通过链缠结增加粘度; 无机增稠剂(如膨润土)通过吸水膨胀和卡屋结构增稠; 纳米粒子增稠剂(如纳米纤维素)通过形成网络结构。不同增稠剂对剪切变稀和屈服应力的影响不同。",
            "source": "课程讲义",
            "keywords": "增稠剂,卡波姆,膨润土,纳米纤维素,流变调控"
        },
        {
            "id": "K032",
            "title": "表面活性剂的HLB值",
            "category": "表面活性剂",
            "content": "HLB(亲水-亲油平衡)值衡量表面活性剂的亲水性。HLB范围1-40: 低HLB(3-6)亲油，适合W/O乳液; 高HLB(8-18)亲水，适合O/W乳液。HLB=7附近适合润湿。HLB值可用Davies公式估算，但不如HLD方法精确。",
            "source": "课程讲义",
            "keywords": "HLB值,亲水亲油平衡,乳化剂选择,Davies公式"
        },
        {
            "id": "K033",
            "title": "刺激响应性高分子",
            "category": "智能材料",
            "content": "刺激响应性高分子能对外界刺激(pH、温度、光、电场、磁场、离子强度等)产生显著的结构或性质变化。典型例子: PNIPAM(温度响应，LCST约32°C)、聚丙烯酸(pH响应)、偶氮苯高分子(光响应)。在药物递送、传感器和智能涂层中有广泛应用。",
            "source": "课程讲义",
            "keywords": "刺激响应性,PNIPAM,pH响应,光响应,智能材料"
        },
        {
            "id": "K034",
            "title": "纳米粒子的表面改性",
            "category": "纳米材料",
            "content": "纳米粒子的表面改性改变其在不同介质中的分散性和相容性。方法包括: 配体交换(用新配体替换原有配体)、聚合物接枝(grafting-to和grafting-from)、表面硅烷化、层层自组装(LbL)。改性后的纳米粒子可用于复合材料、催化和生物医学。",
            "source": "课程讲义",
            "keywords": "纳米粒子,表面改性,配体交换,聚合物接枝,硅烷化"
        },
        {
            "id": "K035",
            "title": "两亲性嵌段共聚物胶束",
            "category": "自组装",
            "content": "两亲性嵌段共聚物在选择性溶剂中自组装形成胶束。疏水嵌段形成核，亲水嵌段形成壳。临界胶束浓度(CMC)远低于小分子表面活性剂。胶束形态可通过改变嵌段比、溶剂条件和温度调控: 球形、蠕虫状、囊泡等。用于药物递送和纳米材料模板。",
            "source": "课程讲义",
            "keywords": "嵌段共聚物胶束,CMC,自组装,药物递送,纳米模板"
        },
        {
            "id": "K036",
            "title": "胶体晶体",
            "category": "胶体科学",
            "content": "胶体晶体是单分散胶体粒子自发排列形成的三维有序结构，类似原子晶体但周期在光学波长尺度(100-1000nm)。由于布拉格衍射可呈现结构色(不使用染料的颜色)。制备方法包括重力沉降、蒸发诱导自组装和旋涂。用于光子晶体和传感器。",
            "source": "课程讲义",
            "keywords": "胶体晶体,结构色,布拉格衍射,光子晶体,单分散"
        },
        {
            "id": "K037",
            "title": "高分子共混物的相容性",
            "category": "高分子科学",
            "content": "大多数高分子对在热力学上不相容(χ>0)，会发生宏观相分离。提高相容性的方法: 加入嵌段或接枝共聚物作为相容剂、在界面处形成共价键(反应增容)、加入纳米粒子。共混物的形态(海岛结构、双连续等)取决于组成比、粘度比和加工条件。",
            "source": "课程讲义",
            "keywords": "高分子共混,相容性,相分离,相容剂,反应增容"
        },
        {
            "id": "K038",
            "title": "生物降解高分子",
            "category": "高分子科学",
            "content": "生物降解高分子可在微生物或酶作用下分解为小分子。常见的有: 聚乳酸(PLA，可水解降解)、聚己内酯(PCL)、聚羟基丁酸酯(PHB)、聚丁二酸丁二醇酯(PBS)。降解速率受结晶度、分子量、亲水性和环境条件影响。在包装、医疗和环保领域有重要应用。",
            "source": "课程讲义",
            "keywords": "生物降解,PLA,PCL,PHB,水解降解"
        },
        {
            "id": "K039",
            "title": "界面聚合",
            "category": "高分子科学",
            "content": "界面聚合是在两种不相溶液体界面上进行的聚合反应。经典例子是尼龙66的界面合成: 己二胺溶于水相，己二酰氯溶于有机相，在界面处快速缩聚形成薄膜。界面聚合法用于制备纳滤膜、微胶囊和中空纤维。反应速率极快，受扩散控制。",
            "source": "课程讲义",
            "keywords": "界面聚合,纳滤膜,微胶囊,尼龙,扩散控制"
        },
        {
            "id": "K040",
            "title": "DNA折纸术",
            "category": "生物软物质",
            "content": "DNA折纸术利用DNA碱基互补配对原理，将长链DNA折叠成预设的纳米结构。通过设计数百条短链DNA(staples)将长链(M13噬菌体基因组)精确折叠。可制备2D和3D纳米结构，分辨率约6nm。在纳米器件、药物递送和生物传感中有应用前景。",
            "source": "课程讲义",
            "keywords": "DNA折纸,碱基配对,纳米结构,staples,M13"
        },
        {
            "id": "K041",
            "title": "反蛋白石结构",
            "category": "纳米材料",
            "content": "反蛋白石是利用胶体晶体模板制备的三维有序多孔结构。先组装胶体晶体模板(如PS微球)，然后用前驱体填充间隙，最后去除模板得到反相结构。常用前驱体包括SiO2溶胶、金属氧化物和高分子。反蛋白石具有结构色和光子带隙特性。",
            "source": "课程讲义",
            "keywords": "反蛋白石,胶体晶体模板,光子带隙,结构色,多孔结构"
        },
        {
            "id": "K042",
            "title": "微流控技术制备乳液",
            "category": "乳液",
            "content": "微流控技术可精确控制液滴生成，制备高度单分散的乳液。基于流聚焦和液滴破裂原理，可控制液滴尺寸(10-500μm)和多级结构(如双重乳液、Janus液滴)。相比传统乳化方法，微流控乳液的CV值可低至2%。用于药物递送、微反应器和数字PCR。",
            "source": "课程讲义",
            "keywords": "微流控,单分散乳液,流聚焦,双重乳液,Janus液滴"
        },
        {
            "id": "K043",
            "title": "形状记忆高分子",
            "category": "智能材料",
            "content": "形状记忆高分子可在外部刺激(通常是温度)下从临时形状恢复到永久形状。机制: 永久形状由化学或物理交联网络固定，临时形状由可逆相(如结晶区或Tg转变)锁定。加热到转变温度以上后，熵弹性驱动形状恢复。典型体系包括PU、环氧树脂和PLA基形状记忆高分子。",
            "source": "课程讲义",
            "keywords": "形状记忆,高分子,可逆相,熵弹性,形状恢复"
        },
        {
            "id": "K044",
            "title": "高分子纳米复合材料",
            "category": "纳米材料",
            "content": "高分子纳米复合材料是将纳米填料(CNT、石墨烯、纳米粘土、纳米SiO2等)分散在高分子基体中。即使极低添加量(<5 wt%)也能显著改善力学、热学、阻隔和电学性能。关键是填料的分散性和界面相互作用。剥离型纳米粘土可使气体阻隔性提高一个数量级。",
            "source": "课程讲义",
            "keywords": "纳米复合材料,碳纳米管,石墨烯,纳米粘土,分散性"
        },
        {
            "id": "K045",
            "title": "软物质的标度律",
            "category": "基本概念",
            "content": "标度律是软物质物理学的核心概念，揭示了物理量之间的幂律关系。例如: 高分子均方末端距 R^2 ~ N^(2ν)，胶体粒子扩散系数 D ~ R^(-1)，蠕虫状胶束零剪切粘度 η0 ~ c^(3.7)。标度分析忽略预因子，只关注指数关系，为理解软物质行为提供了简洁的理论框架。",
            "source": "课程讲义",
            "keywords": "标度律,幂律,标度分析,高分子,胶体"
        },
        {
            "id": "K046",
            "title": "界面活性聚合物",
            "category": "高分子科学",
            "content": "界面活性聚合物是在链中同时含有亲水和疏水段的聚合物，类似小分子表面活性剂。可在油水界面自组装，降低界面张力。用于高分子共混物的增容、乳液稳定和涂层。疏水改性乙基羟乙基纤维素(HM-EHEC)是典型例子。",
            "source": "课程讲义",
            "keywords": "界面活性聚合物,增容,乳液稳定,疏水改性"
        },
        {
            "id": "K047",
            "title": "超分子聚合物",
            "category": "自组装",
            "content": "超分子聚合物通过非共价相互作用(氢键、金属配位、主客体作用、π-π堆积等)将单体连接成聚合物链。具有自修复、可回收、刺激响应等优点。UPy(脲基嘧啶酮)四重氢键是最常用的超分子聚合物构建基元，结合常数高达10^7 M^-1。",
            "source": "课程讲义",
            "keywords": "超分子聚合物,非共价键,自修复,UPy,氢键"
        },
        {
            "id": "K048",
            "title": "Janus粒子",
            "category": "纳米材料",
            "content": "Janus粒子是表面具有两种不同化学性质区域的粒子，类似于古罗马双面神Janus。例如一亲水一疏水、一正一负电荷、一荧光一暗等。Janus粒子具有独特的界面活性和自组装行为，可用于Pickering乳液稳定、表面活性剂替代和纳米马达。",
            "source": "课程讲义",
            "keywords": "Janus粒子,双面性,界面活性,Pickering乳液"
        },
        {
            "id": "K049",
            "title": "胶体凝胶",
            "category": "胶体科学",
            "content": "胶体凝胶是胶体粒子在吸引力作用下形成的贯穿网络结构，可以支撑自身重量。粒子浓度高于凝胶点时，粒子间的短程吸引力导致分形聚集体的形成。胶体凝胶具有屈服应力和时间依赖性(老化)行为。常见例子包括硅胶、粘土悬浮液和蛋白质聚集体凝胶。",
            "source": "课程讲义",
            "keywords": "胶体凝胶,凝胶点,分形聚集体,屈服应力,老化"
        },
        {
            "id": "K050",
            "title": "高分子共混物的流变学",
            "category": "流变学",
            "content": "高分子共混物的流变行为受各组分的粘弹性、组成比和形态影响。低频区域可观察到第二个松弛平台(由分散相液滴形变和松弛贡献)。Palierne模型可预测乳液型共混物的线性粘弹性。共混物的稳态粘度通常低于加权平均值(协同效应)或出现正偏差(相容性差)。",
            "source": "课程讲义",
            "keywords": "共混物流变,Palierne模型,松弛,协同效应"
        },
        {
            "id": "K051",
            "title": "静电纺丝",
            "category": "制备方法",
            "content": "静电纺丝利用高压电场将高分子溶液或熔体拉伸形成纳米纤维。纤维直径范围从几十nm到几μm，受溶液浓度、电压、流速和接收距离影响。可制备功能化纳米纤维膜，用于过滤、伤口敷料和组织工程支架。加入纳米粒子可赋予导电、抗菌等功能。",
            "source": "课程讲义",
            "keywords": "静电纺丝,纳米纤维,高压电场,纤维膜"
        },
        {
            "id": "K052",
            "title": "层层自组装(LbL)",
            "category": "制备方法",
            "content": "层层自组装通过交替沉积带相反电荷的物质(聚电解质、纳米粒子、蛋白质等)在基底上构建多层膜。每层厚度可精确控制(1-100nm)。驱动力包括静电作用、氢键、配位键等。用于制备功能涂层、药物缓释膜和传感器。",
            "source": "课程讲义",
            "keywords": "LbL,层层自组装,聚电解质,多层膜,功能涂层"
        },
        {
            "id": "K053",
            "title": "软物质的安全考量",
            "category": "实验安全",
            "content": "软物质实验中常见的安全隐患: 有机溶剂(甲苯、氯仿等)的毒性和易燃性; 强酸强碱(浓硫酸、氢氟酸等)的腐蚀性; 纳米材料的潜在吸入风险; 高压静电设备的安全; 液氮的低温冻伤。必须在通风橱中操作有机溶剂，佩戴防护装备，了解MSDS。",
            "source": "课程讲义",
            "keywords": "实验安全,有机溶剂,强酸强碱,纳米材料,MSDS"
        },
        {
            "id": "K054",
            "title": "光散射技术",
            "category": "表征方法",
            "content": "光散射技术包括静态光散射(SLS)和动态光散射(DLS)。SLS测量散射光的平均强度，可获得粒子的重均分子量Mw和回转半径Rg。DLS测量散射光强度的时间涨落，可获得扩散系数和粒径。Zimm图是SLS数据分析的经典方法。两者都适用于1nm-1μm尺寸范围。",
            "source": "课程讲义",
            "keywords": "光散射,SLS,DLS,Zimm图,分子量,粒径"
        },
        {
            "id": "K055",
            "title": "原子力显微镜(AFM)",
            "category": "表征方法",
            "content": "AFM利用微悬臂末端的尖锐探针扫描样品表面，通过针尖-样品间的相互作用力获得表面形貌。分辨率可达亚nm级。除形貌外，还可测量力曲线(粘附力、弹性模量)和导电性。软物质样品常使用轻敲模式以减少损伤。峰值力定量纳米力学模式可同时获得模量和形貌。",
            "source": "课程讲义",
            "keywords": "AFM,原子力显微镜,力曲线,峰值力,形貌"
        },
        {
            "id": "K056",
            "title": "高分子的结晶行为",
            "category": "高分子科学",
            "content": "半结晶高分子(如PE、PP、PET)同时包含结晶区和非晶区。结晶度影响材料的力学、热学和阻隔性能。结晶过程包括成核和生长两个阶段。Avrami方程描述等温结晶动力学。球晶是最常见的结晶形态，尺寸可达数十微米，可用偏光显微镜观察。",
            "source": "课程讲义",
            "keywords": "高分子结晶,结晶度,Avrami方程,球晶,偏光显微镜"
        },
        {
            "id": "K057",
            "title": "微乳液",
            "category": "乳液",
            "content": "微乳液是热力学稳定的透明或半透明分散体系，液滴尺寸10-100nm。与普通乳液不同，微乳液可自发形成且长期稳定。需要在最优配方下形成(通常需要助表面活性剂如醇类)。微乳液在三次采油、药物递送和纳米粒子合成中有重要应用。",
            "source": "课程讲义",
            "keywords": "微乳液,热力学稳定,助表面活性剂,三次采油,纳米粒子合成"
        },
        {
            "id": "K058",
            "title": "仿生矿化",
            "category": "生物软物质",
            "content": "生物矿化是生物体在有机基质(蛋白质、多糖等)调控下形成无机矿物(如骨骼中的羟基磷灰石、贝壳中的碳酸钙)的过程。有机基质提供成核位点和生长限域。仿生矿化利用有机模板(如高分子、脂质体)在温和条件下合成具有特殊形貌的无机材料。",
            "source": "课程讲义",
            "keywords": "生物矿化,羟基磷灰石,有机模板,仿生合成"
        },
        {
            "id": "K059",
            "title": "软物质实验的统计方法",
            "category": "数据分析",
            "content": "软物质实验中常用的统计方法: t检验(比较两组均值)、方差分析ANOVA(比较多组均值)、线性回归(拟合线性关系)、非线性最小二乘拟合(拟合指数、幂律等)。每次实验至少重复3次，报告均值和标准偏差。流变数据拟合时需注意参数物理意义的合理性。",
            "source": "课程讲义",
            "keywords": "统计方法,t检验,ANOVA,回归分析,标准偏差"
        },
        {
            "id": "K060",
            "title": "柔性链的蠕虫状链模型",
            "category": "高分子科学",
            "content": "蠕虫状链模型(Kratky-Porod模型)描述半柔性链的构象，通过持续长度lp衡量链的柔性。lp远小于链长L时为柔性链(高斯链行为)，lp与L相当为半柔性链，lp远大于L为刚性棒。该模型适用于DNA、肌动蛋白丝和高分子主链的描述。",
            "source": "课程讲义",
            "keywords": "蠕虫状链,持续长度,Kratky-Porod,半柔性链,DNA"
        },
    ]
    write_csv(DATA_DIR / "softmatter_knowledge.csv", fieldnames, rows)
    return len(rows)


# =========================================================================
# 2. literature_records.csv
# =========================================================================
def generate_literature():
    fieldnames = ["id", "title", "year", "source", "material_system",
                  "method", "characterization", "result_summary", "keywords",
                  "data_source"]
    rows = [
        {
            "id": "L001",
            "title": "Curated example: PNIPAM-based thermo-responsive hydrogel swelling behavior",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚N-异丙基丙烯酰胺(PNIPAM)水凝胶",
            "method": "自由基聚合制备PNIPAM水凝胶，交联剂为N,N'-亚甲基双丙烯酰胺(BIS)",
            "characterization": "流变仪测量储能模量; DLS测量粒径; 称重法测量溶胀比",
            "result_summary": "PNIPAM水凝胶在32°C附近发生LCST相转变，低温下溶胀比约15，高温下塌缩至约3。储能模量在LCST以下约500Pa，以上增大约一个数量级。",
            "keywords": "PNIPAM,水凝胶,LCST,溶胀,温度响应",
            "data_source": "curated_example"
        },
        {
            "id": "L002",
            "title": "Curated example: SDS micelle structure studied by SANS",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "十二烷基硫酸钠(SDS)/水体系",
            "method": "配制不同浓度的SDS水溶液，加入NaCl调节离子强度",
            "characterization": "小角中子散射(SANS)表征胶束结构; 电导率法测定CMC",
            "result_summary": "在0.1M NaCl条件下，SDS形成半径约2.5nm的球形胶束，聚集数约70。加入盐后CMC从8.2mM降至1.5mM。高浓度下转变为蠕虫状胶束。",
            "keywords": "SDS,胶束,SANS,CMC,聚集数",
            "data_source": "curated_example"
        },
        {
            "id": "L003",
            "title": "Curated example: PLA/PEG blend morphology and degradation",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚乳酸(PLA)/聚乙二醇(PEG)共混物",
            "method": "溶液共混法制备PLA/PEG共混物薄膜，PEG含量5-30 wt%",
            "characterization": "DSC测量Tg和Tm; SEM观察断面形貌; 称重法测量降解率",
            "result_summary": "PEG的加入降低了PLA的Tg(从60°C降至45°C)，提高了材料的柔韧性。PEG含量>15wt%时出现明显相分离。在PBS缓冲液中37°C降解60天后质量损失约20%。",
            "keywords": "PLA,PEG,共混,Tg,生物降解",
            "data_source": "curated_example"
        },
        {
            "id": "L004",
            "title": "Curated example: SiO2 nanoparticle-stabilized Pickering emulsion",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "SiO2纳米粒子/正辛烷/水体系",
            "method": "硅烷化处理SiO2粒子(接触角约90度)，高速乳化制备Pickering乳液",
            "characterization": "接触角测量; 光学显微镜观察液滴形貌; DLS测量粒径",
            "result_summary": "硅烷化SiO2粒子可稳定O/W型Pickering乳液，液滴平均粒径约50μm。乳液在室温下稳定超过30天。粒子浓度从0.5wt%增至2wt%时液滴尺寸从80μm降至30μm。",
            "keywords": "Pickering乳液,SiO2,硅烷化,稳定性",
            "data_source": "curated_example"
        },
        {
            "id": "L005",
            "title": "Curated example: Block copolymer PS-b-P4VP self-assembly thin film",
            "year": 2020,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚苯乙烯-b-聚4-乙烯基吡啶(PS-b-P4VP)",
            "method": "旋涂法制备薄膜，退火处理(溶剂退火和热退火)",
            "characterization": "AFM观察表面形貌; GISAXS测量周期结构",
            "result_summary": "PS-b-P4VP在不同嵌段比下形成球形(15nm周期)、柱形(25nm周期)和层状(35nm周期)结构。THF溶剂退火比热退火获得更好的长程有序性。",
            "keywords": "嵌段共聚物,PS-b-P4VP,自组装,薄膜,退火",
            "data_source": "curated_example"
        },
        {
            "id": "L006",
            "title": "Curated example: Worm-like micelle rheology in CTAB/NaSal system",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "十六烷基三甲基溴化铵(CTAB)/水杨酸钠(NaSal)体系",
            "method": "配制CTAB/NaSal水溶液，CTAB浓度50-200mM，NaSal与CTAB摩尔比0.5",
            "characterization": "旋转流变仪测量稳态和动态流变行为",
            "result_summary": "CTAB/NaSal体系形成蠕虫状胶束，表现出明显的剪切变稀和粘弹性。零剪切粘度随CTAB浓度快速增大(η0~c^3.5)。Maxwell模型拟合得到单一松弛时间，表明线性蠕虫状胶束行为。",
            "keywords": "蠕虫状胶束,CTAB,NaSal,粘弹性,Maxwell模型",
            "data_source": "curated_example"
        },
        {
            "id": "L007",
            "title": "Curated example: Polyacrylamide hydrogel with high toughness",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚丙烯酰胺(PAM)/聚乙烯醇(PVA)双网络水凝胶",
            "method": "两步法制备双网络凝胶: 第一网络PAM化学交联，第二网络PVA物理交联(冻融循环)",
            "characterization": "万能试验机拉伸测试; 流变仪测量力学性能; SEM观察网络结构",
            "result_summary": "双网络凝胶的断裂伸长率约2000%，拉伸强度约2MPa，远高于单网络PAM凝胶(断裂伸长率约500%，强度约0.1MPa)。能量耗散机制为第一网络的牺牲键断裂。",
            "keywords": "双网络水凝胶,PAM,PVA,韧性,牺牲键",
            "data_source": "curated_example"
        },
        {
            "id": "L008",
            "title": "Curated example: Graphene oxide liquid crystal behavior",
            "year": 2020,
            "source": "教学示例(非真实PDF)",
            "material_system": "氧化石墨烯(GO)水分散液",
            "method": "改良Hummers法制备GO纳米片，配制不同浓度的水分散液",
            "characterization": "偏光显微镜观察液晶织构; XRD测量层间距; 流变仪测量粘弹性",
            "result_summary": "GO分散液在浓度约0.5wt%时出现向列型液晶相，偏光下可观察到特征指纹织构。临界浓度与GO纳米片的纵横比有关。液晶相表现出明显的剪切取向行为。",
            "keywords": "氧化石墨烯,液晶,向列相,偏光显微镜",
            "data_source": "curated_example"
        },
        {
            "id": "L009",
            "title": "Curated example: Cellulose nanocrystal film iridescence",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "纤维素纳米晶(CNC)悬浮液",
            "method": "硫酸水解法制备CNC，蒸发诱导自组装制备手性向列型薄膜",
            "characterization": "偏光显微镜; UV-Vis光谱; SEM; 圆二色谱",
            "result_summary": "CNC悬浮液蒸发自组装形成手性向列型结构，薄膜呈现虹彩结构色。反射波长由螺距决定，可通过CNC浓度和添加剂(如NaCl、PEG)调控。薄膜干燥后螺距约200nm。",
            "keywords": "纤维素纳米晶,手性向列,结构色,自组装",
            "data_source": "curated_example"
        },
        {
            "id": "L010",
            "title": "Curated example: Responsive microgel colloidal crystal",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "PNIPAM微凝胶胶体晶体",
            "method": "乳液聚合法制备单分散PNIPAM微凝胶，自组装形成胶体晶体",
            "characterization": "DLS测量粒径; UV-Vis反射光谱; 光学显微镜",
            "result_summary": "单分散PNIPAM微凝胶(26°C时粒径约300nm)自组装形成面心立方胶体晶体，呈现明亮结构色。温度从25°C升至35°C时，微凝胶收缩(粒径降至约150nm)，光子带隙蓝移，薄膜颜色从红色变为蓝色。",
            "keywords": "PNIPAM微凝胶,胶体晶体,结构色,温度响应",
            "data_source": "curated_example"
        },
        {
            "id": "L011",
            "title": "Curated example: CNT/PDMS conductive composite strain sensor",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "碳纳米管(CNT)/聚二甲基硅氧烷(PDMS)复合材料",
            "method": "溶液混合法制备CNT/PDMS复合材料，CNT含量0.5-5wt%",
            "characterization": "四探针法测电阻率; 万能试验机测力学性能; 循环拉伸测传感稳定性",
            "result_summary": "CNT/PDMS复合材料在CNT含量约1wt%时达到渗流阈值，电阻率从10^12降至10^4 Ω·cm。复合材料在0-50%应变范围内GF(gauge factor)约5，可用于柔性应变传感器。",
            "keywords": "CNT,PDMS,导电复合材料,渗流阈值,应变传感器",
            "data_source": "curated_example"
        },
        {
            "id": "L012",
            "title": "Curated example: Liposome encapsulation for drug delivery",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "磷脂酰胆碱/胆固醇脂质体",
            "method": "薄膜水化法制备脂质体，挤出法控制粒径，透析法去除游离药物",
            "characterization": "DLS测量粒径和PDI; 荧光光谱测定包封率; TEM观察形态",
            "result_summary": "脂质体平均粒径约120nm，PDI<0.2，包封率约65%。胆固醇含量20mol%时膜稳定性最佳。体外释放24小时累计释放约40%，表现出缓释特征。",
            "keywords": "脂质体,药物递送,包封率,胆固醇,缓释",
            "data_source": "curated_example"
        },
        {
            "id": "L013",
            "title": "Curated example: Colloidal gel aging and yielding",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "胶体二氧化硅粒子分散液",
            "method": "调节离子强度诱导胶体粒子形成凝胶网络",
            "characterization": "流变仪测量屈服应力和蠕变; 光散射测量微观结构演化",
            "result_summary": "胶体凝胶在老化过程中屈服应力逐渐增大(与时间呈对数关系)。分形维数约2.1，表明反应限制聚集。蠕变测试表明凝胶在小应力下长时间后会发生突然断裂(延迟弹性失效)。",
            "keywords": "胶体凝胶,老化,屈服应力,分形,蠕变",
            "data_source": "curated_example"
        },
        {
            "id": "L014",
            "title": "Curated example: Electrospun PVA nanofiber membrane for water treatment",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚乙烯醇(PVA)/壳聚糖(CS)复合纳米纤维",
            "method": "静电纺丝法制备PVA/CS纳米纤维膜，PVA/CS质量比9:1至7:3",
            "characterization": "SEM测量纤维直径; 接触角测量; 过滤效率测试",
            "result_summary": "PVA/CS纳米纤维平均直径约200nm。加入壳聚糖后接触角从40°降至25°，亲水性增强。对亚甲基蓝的吸附量达180mg/g。水通量约500L/(m2·h)，对0.5μm PS微球截留率>95%。",
            "keywords": "静电纺丝,PVA,壳聚糖,纳米纤维,水处理",
            "data_source": "curated_example"
        },
        {
            "id": "L015",
            "title": "Curated example: Self-healing polyurethane elastomer",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "含UPy氢键的聚氨酯弹性体",
            "method": "预聚体法合成含UPy侧基的聚氨酯，浇铸成型",
            "characterization": "万能试验机拉伸测试; 流变仪测量自修复效率; FTIR确认氢键",
            "result_summary": "UPy-PU弹性体拉伸强度约15MPa，断裂伸长率约600%。切开后在60°C热处理2小时可恢复约85%的力学性能。自修复效率随UPy含量增加而增大。多次切割-修复循环后性能衰减<10%。",
            "keywords": "自修复,聚氨酯,UPy氢键,弹性体",
            "data_source": "curated_example"
        },
        {
            "id": "L016",
            "title": "Curated example: Double network hydrogel as cartilage substitute",
            "year": 2020,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚2-丙烯酰胺-2-甲基丙磺酸(PAMPS)/聚丙烯酰胺(PAAm)双网络凝胶",
            "method": "两步光引发聚合制备DN凝胶",
            "characterization": "压缩和摩擦测试; 生物相容性测试; SEM",
            "result_summary": "PAMPS/PAAm DN凝胶压缩强度约60MPa，含水率>70%，摩擦系数约0.01(与关节软骨相当)。在模拟体液中30天性能稳定。细胞毒性测试表明良好的生物相容性。",
            "keywords": "双网络凝胶,人工软骨,摩擦系数,生物相容性",
            "data_source": "curated_example"
        },
        {
            "id": "L017",
            "title": "Curated example: Magnetic responsive elastomer for soft actuator",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "铁氧体纳米粒子/PDMS磁响应弹性体",
            "method": "混合磁性纳米粒子于PDMS预聚体中，磁场下固化形成各向异性结构",
            "characterization": "VSM测量磁性能; 数字图像相关(DIC)测量变形; 流变测量",
            "result_summary": "含30vol% Fe3O4的PDMS弹性体在200mT磁场下可在1秒内产生约30%的弯曲变形。磁场撤除后形状恢复。循环测试100次后变形量衰减<5%。可用于软体机器人和智能阀门。",
            "keywords": "磁响应弹性体,PDMS,Fe3O4,软体机器人",
            "data_source": "curated_example"
        },
        {
            "id": "L018",
            "title": "Curated example: Nanocellulose reinforced starch biocomposite",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "纤维素纳米纤丝(CNF)/热塑性淀粉(TPS)复合材料",
            "method": "溶液浇铸法制备CNF/TPS复合膜，甘油作为增塑剂",
            "characterization": "万能试验机拉伸测试; TGA热重分析; DMA动态力学分析",
            "result_summary": "添加5wt% CNF使TPS拉伸强度从5MPa提高到18MPa，杨氏模量提高3倍。CNF与淀粉之间形成氢键网络，限制了淀粉链的运动。TGA显示热分解温度提高约15°C。",
            "keywords": "纳米纤维素,淀粉,生物复合材料,力学增强",
            "data_source": "curated_example"
        },
        {
            "id": "L019",
            "title": "Curated example: Photonic crystal hydrogel sensor for pH detection",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚丙烯酸(PAA)/SiO2光子晶体水凝胶",
            "method": "将SiO2胶体晶体模板嵌入PAA水凝胶中，去除模板得到反蛋白石结构",
            "characterization": "UV-Vis反射光谱; 光学显微镜; 原位pH响应测试",
            "result_summary": "PAA反蛋白石光子晶体凝胶在pH 4-8范围内反射峰位移约100nm，对应颜色从蓝色变为红色。响应时间约5分钟。凝胶可逆循环10次后反射峰位置偏差<5nm。可用于pH快速检测。",
            "keywords": "光子晶体,水凝胶,pH传感,反蛋白石,PAA",
            "data_source": "curated_example"
        },
        {
            "id": "L020",
            "title": "Curated example: Polymer brush-modified surface for anti-fouling",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚乙二醇甲基丙烯酸酯(PEGMA)聚合物刷",
            "method": "SI-ATRP法在硅片表面接枝PEGMA聚合物刷",
            "characterization": "椭偏仪测量膜厚; 接触角; XPS确认表面化学; 蛋白吸附实验",
            "result_summary": "PEGMA聚合物刷厚度约30nm，水接触角约35°。蛋白质(牛血清白蛋白)吸附量比未修饰表面减少约95%。聚合物刷密度约0.5链/nm2时抗蛋白吸附效果最佳。",
            "keywords": "聚合物刷,PEGMA,抗蛋白吸附,SI-ATRP",
            "data_source": "curated_example"
        },
        {
            "id": "L021",
            "title": "Curated example: Shape memory polymer for deployable structures",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "环氧树脂基形状记忆高分子",
            "method": "浇铸固化法制备环氧树脂试样，编程形状记忆循环",
            "characterization": "DSC测定Tg; DMA测量形状固定率和恢复率; 视频记录形状恢复",
            "result_summary": "环氧树脂Tg约120°C，形状固定率>98%，形状恢复率>95%。可编程多个临时形状(两段式恢复)。循环10次后形状恢复率衰减<2%。适合航天可展开结构。",
            "keywords": "形状记忆,环氧树脂,形状固定率,形状恢复率",
            "data_source": "curated_example"
        },
        {
            "id": "L022",
            "title": "Curated example: Supramolecular hydrogel based on host-guest interaction",
            "year": 2022,
            "source": "教学示例(非真实PDF)",
            "material_system": "β-环糊精(β-CD)/金刚烷(Ad)超分子水凝胶",
            "method": "将β-CD改性透明质酸和Ad改性透明质酸混合，形成超分子交联凝胶",
            "characterization": "流变仪测量粘弹性; 倒置法测定凝胶-溶胶转变; 荧光光谱",
            "result_summary": "β-CD/Ad超分子水凝胶G'约1000Pa，可注射性良好(注射后G'恢复>90%)。添加竞争客体分子可实现凝胶-溶胶转变。37°C下凝胶缓慢降解(约7天)。可用于细胞包封和药物缓释。",
            "keywords": "超分子水凝胶,环糊精,金刚烷,可注射",
            "data_source": "curated_example"
        },
        {
            "id": "L023",
            "title": "Curated example: Janus particle synthesis and interfacial activity",
            "year": 2020,
            "source": "教学示例(非真实PDF)",
            "material_system": "PS/SiO2 Janus粒子",
            "method": "Pickering乳液保护的半面功能化法: PS微球一侧沉积SiO2纳米粒子",
            "characterization": "TEM和SEM观察形貌; 接触角测量; 界面张力测量",
            "result_summary": "制备的Janus粒子尺寸约500nm，一侧为PS(疏水)另一侧为SiO2(亲水)。界面活性是均质粒子的约10倍(更低的界面张力)。可稳定O/W和W/O乳液，取决于添加到哪一相。",
            "keywords": "Janus粒子,PS/SiO2,界面活性,半面功能化",
            "data_source": "curated_example"
        },
        {
            "id": "L024",
            "title": "Curated example: Layer-by-layer assembly for corrosion protection",
            "year": 2021,
            "source": "教学示例(非真实PDF)",
            "material_system": "聚乙烯亚胺(PEI)/聚丙烯酸(PAA)多层膜",
            "method": "交替浸涂法在铝合金基底上沉积PEI/PAA多层膜(10-50个双层)",
            "characterization": "EIS电化学阻抗谱; 盐雾测试; 椭偏仪测膜厚",
            "result_summary": "20个双层的PEI/PAA多层膜使铝合金的腐蚀电流密度降低约3个数量级。盐雾试验48小时后划痕处腐蚀扩展<2mm。多层膜厚度约500nm，在pH 3-11范围内稳定。",
            "keywords": "LbL,防腐,PEI,PAA,多层膜",
            "data_source": "curated_example"
        },
        {
            "id": "L025",
            "title": "Curated example: Microfluidic preparation of double emulsion for encapsulation",
            "year": 2023,
            "source": "教学示例(非真实PDF)",
            "material_system": "氟化油/水/油(W/O/W)双重乳液",
            "method": "同轴毛细管微流控装置制备双重乳液液滴",
            "characterization": "光学显微镜观察液滴结构; 荧光成像; DLS测内液滴尺寸",
            "result_summary": "微流控制备的W/O/W双重乳液CV<5%，外液滴直径约100μm，内液滴数可控(1-5个)。在液滴内进行模型反应(酶催化)，转化率>90%。双重乳液稳定时间>7天。",
            "keywords": "微流控,双重乳液,毛细管,微反应器",
            "data_source": "curated_example"
        },
    ]
    write_csv(DATA_DIR / "literature_records.csv", fieldnames, rows)
    return len(rows)


# =========================================================================
# 3. experiment_recipes.csv
# =========================================================================
def generate_recipes():
    fieldnames = ["id", "material", "concentration", "process", "temperature",
                  "time", "characterization", "result", "safety_level", "source",
                  "is_example"]
    rows = [
        {
            "id": "R001",
            "material": "聚N-异丙基丙烯酰胺(PNIPAM)水凝胶",
            "concentration": "NIPAM单体10wt%，BIS交联剂0.5wt%",
            "process": "自由基聚合，APS引发，TEMED催化，氮气保护",
            "temperature": "25°C引发聚合",
            "time": "聚合反应24小时",
            "characterization": "流变仪测G'/G''，DLS测粒径，称重法测溶胀比",
            "result": "制得透明水凝胶，32°C附近发生LCST转变，溶胀比约15:1",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R002",
            "material": "SDS胶束溶液",
            "concentration": "SDS 50mM，NaCl 100mM",
            "process": "磁力搅拌溶解SDS于去离子水中，加入NaCl调节离子强度",
            "temperature": "25°C",
            "time": "搅拌1小时直至完全溶解",
            "characterization": "电导率法测CMC，DLS测粒径",
            "result": "形成球形胶束，平均直径约5nm，CMC约1.5mM(含盐)",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R003",
            "material": "聚乙烯醇(PVA)水凝胶",
            "concentration": "PVA 10wt%(分子量约89000)",
            "process": "PVA溶于去离子水(90°C加热溶解)，冻融循环法交联",
            "temperature": "-20°C冷冻，25°C解冻",
            "time": "每次冻融循环: 冷冻12小时+解融4小时，共3-5个循环",
            "characterization": "流变仪测力学性能，称重法测含水率",
            "result": "制得白色不透明水凝胶，3次冻融后G'约10kPa，含水率约85%",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R004",
            "material": "CTAB蠕虫状胶束溶液",
            "concentration": "CTAB 100mM，NaSal 50mM",
            "process": "先溶解CTAB，再加入NaSal，缓慢搅拌避免产生气泡",
            "temperature": "25°C",
            "time": "搅拌4小时，静置过夜",
            "characterization": "旋转流变仪测稳态和振荡流变",
            "result": "形成蠕虫状胶束网络，零剪切粘度约50Pa·s，表现出Maxwell流体行为",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R005",
            "material": "壳聚糖/甘油磷酸钠温敏凝胶",
            "concentration": "壳聚糖 2wt%，β-甘油磷酸钠 5.6wt%",
            "process": "壳聚糖溶于0.1M HCl，冷却后缓慢加入β-甘油磷酸钠溶液",
            "temperature": "4°C配制，37°C凝胶化",
            "time": "配制后4°C保存，升温至37°C后约30分钟凝胶化",
            "characterization": "流变仪测温度扫描，倒置法验证凝胶化",
            "result": "室温下为溶液态，37°C下转变为半透明凝胶，G'约500Pa",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R006",
            "material": "SiO2纳米粒子Pickering乳液",
            "concentration": "SiO2纳米粒子 1wt%，正辛烷 30vol%",
            "process": "硅烷化SiO2粒子分散于水中，加入油相，高速乳化(10000rpm)",
            "temperature": "25°C",
            "time": "乳化10分钟",
            "characterization": "光学显微镜观察液滴，接触角测量，稳定性观察",
            "result": "形成O/W型乳液，液滴平均直径约50μm，室温下稳定>30天",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R007",
            "material": "聚苯乙烯微球(乳液聚合)",
            "concentration": "苯乙烯单体 10vol%，SDS 0.5wt%，KPS引发剂 0.3wt%",
            "process": "乳液聚合法: SDS溶于水，加入苯乙烯单体，预乳化后升温引发聚合",
            "temperature": "70°C聚合",
            "time": "聚合反应8小时",
            "characterization": "DLS/SEM测粒径，Zeta电位",
            "result": "制得单分散PS微球，平均直径约300nm，PDI<0.05，Zeta电位约-40mV",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R008",
            "material": "聚丙烯酰胺/聚乙烯醇双网络水凝胶",
            "concentration": "AM单体 2M，BIS 0.5mol%(相对AM)，PVA 5wt%",
            "process": "两步法: 先光引发聚合PAM第一网络，再浸泡PVA溶液后冻融形成第二网络",
            "temperature": "紫外光引发室温聚合",
            "time": "紫外照射30分钟，冻融循环3次",
            "characterization": "万能试验机拉伸测试，流变测量",
            "result": "双网络凝胶断裂伸长率>1500%，拉伸强度约1.5MPa",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R009",
            "material": "纤维素纳米晶(CNC)悬浮液",
            "concentration": "CNC 3wt%水悬浮液",
            "process": "硫酸水解微晶纤维素(64wt% H2SO4, 45°C)，稀释终止反应，透析纯化",
            "temperature": "水解45°C",
            "time": "水解反应45分钟，透析3天(换水多次)",
            "characterization": "TEM测粒径，偏光显微镜观察液晶态，Zeta电位",
            "result": "制得棒状CNC(长约200nm，直径约15nm)，分散液呈乳光，高浓度下出现手性向列液晶",
            "safety_level": "high",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R010",
            "material": "聚乳酸(PLA)薄膜",
            "concentration": "PLA 10wt%(溶于氯仿)",
            "process": "溶液浇铸法: PLA溶于氯仿，倒入培养皿中，通风橱内蒸发溶剂",
            "temperature": "25°C通风橱中蒸发",
            "time": "溶剂蒸发24小时",
            "characterization": "DSC测Tg和Tm，拉伸测试",
            "result": "制得透明PLA薄膜，Tg约58°C，Tm约170°C，拉伸强度约50MPa",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R011",
            "material": "超分子水凝胶(UPy基)",
            "concentration": "UPy-PEG 10wt%",
            "process": "UPy改性PEG溶于热水，冷却至室温形成物理交联凝胶",
            "temperature": "80°C溶解，25°C凝胶化",
            "time": "冷却约30分钟凝胶化",
            "characterization": "流变仪温度扫描，FTIR确认氢键",
            "result": "室温下形成透明凝胶，G'约500Pa，加热至60°C以上变为溶液(可逆)",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R012",
            "material": "聚多巴胺(PDA)涂层",
            "concentration": "盐酸多巴胺 2mg/mL，Tris缓冲液 pH 8.5",
            "process": "将基底浸入碱性多巴胺溶液中，多巴胺在基底表面氧化自聚合",
            "temperature": "25°C",
            "time": "浸泡24小时",
            "characterization": "椭偏仪测膜厚，接触角，XPS确认表面化学",
            "result": "形成约30nm厚的PDA涂层，水接触角约55°，涂层均匀致密",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R013",
            "material": "PLGA微球(乳液溶剂蒸发法)",
            "concentration": "PLGA 200mg(溶于2mL DCM)，PVA 1wt%水溶液",
            "process": "W/O乳液法: PLGA/DCM溶液为油相，PVA水溶液为外水相，高速乳化后蒸发DCM",
            "temperature": "25°C乳化，室温蒸发溶剂",
            "time": "乳化3分钟，溶剂蒸发4小时",
            "characterization": "SEM测形貌和粒径，DLS测粒径分布",
            "result": "制得球形PLGA微球，平均直径约10μm，表面有微孔结构",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R014",
            "material": "SiO2反蛋白石光子晶体",
            "concentration": "SiO2微球(直径250nm)悬浮液 0.5wt%",
            "process": "垂直沉积法: 玻璃基底垂直浸入SiO2悬浮液中，缓慢蒸发组装",
            "temperature": "55°C烘箱",
            "time": "蒸发组装3-5天",
            "characterization": "SEM观察有序结构，UV-Vis反射光谱",
            "result": "形成面心立方有序排列的SiO2胶体晶体薄膜，反射峰约550nm(绿色)",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R015",
            "material": "聚氨酯形状记忆弹性体",
            "concentration": "MDI/BDO/PTMG摩尔比 3:2:1",
            "process": "预聚体法: MDI与PTMG反应形成预聚体，BDO扩链，浇铸固化",
            "temperature": "80°C预聚，100°C后固化",
            "time": "预聚2小时，扩链浇铸后固化4小时",
            "characterization": "DSC测Tg，DMA测形状记忆性能",
            "result": "Tg约55°C，形状固定率>97%，形状恢复率>95%",
            "safety_level": "high",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R016",
            "material": "疏水缔合水凝胶",
            "concentration": "丙烯酰胺 2M，十六烷基二甲基烯丙基氯化铵 0.5mol%(相对AM)",
            "process": "胶束聚合法: 先配制表面活性剂胶束溶液，再加入AM单体和引发剂聚合",
            "temperature": "50°C聚合",
            "time": "聚合反应12小时",
            "characterization": "流变仪测粘弹性，拉伸测试",
            "result": "制得透明水凝胶，断裂伸长率约3000%，具有优异的自修复能力(24小时修复效率>90%)",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R017",
            "material": "离子液体凝胶电解质",
            "concentration": "PVDF-HFP 15wt%，离子液体[BMIM][BF4] 60wt%，DMF溶剂 25wt%",
            "process": "溶液浇铸法: PVDF-HFP溶于DMF，加入离子液体，浇铸成膜后真空干燥",
            "temperature": "60°C真空干燥",
            "time": "干燥24小时",
            "characterization": "电化学阻抗谱测离子电导率，拉伸测试",
            "result": "制得透明凝胶膜，室温离子电导率约10^-3 S/cm，拉伸强度约5MPa",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R018",
            "material": "海藻酸钙水凝胶微球",
            "concentration": "海藻酸钠 2wt%，CaCl2 2wt%",
            "process": "注射器将海藻酸钠溶液逐滴滴入CaCl2溶液中，钙离子交联形成微球",
            "temperature": "25°C",
            "time": "交联30分钟",
            "characterization": "光学显微镜测尺寸，流变仪测力学",
            "result": "制得球形微球，直径约2mm(可通过针头尺寸控制)，含水率>95%",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R019",
            "material": "介电弹性体驱动器(DEA)",
            "concentration": "VHB 4910丙烯酸弹性体薄膜",
            "process": "预拉伸VHB薄膜(3x3倍)，两侧涂抹碳脂柔性电极，叠层组装",
            "temperature": "25°C",
            "time": "组装约1小时",
            "characterization": "高压测试驱动应变，激光测距仪测位移",
            "result": "施加4kV电压时面积应变约100%，响应时间约10ms",
            "safety_level": "high",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R020",
            "material": "纳米粘土(Laponite)物理水凝胶",
            "concentration": "Laponite 3wt%",
            "process": "将Laponite粉末缓慢加入去离子水中，高速搅拌分散",
            "temperature": "25°C",
            "time": "搅拌2小时，静置过夜",
            "characterization": "流变仪测屈服应力和触变性",
            "result": "形成透明触变性凝胶，屈服应力约10Pa，可注射，静置后结构恢复",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R021",
            "material": "核壳结构纳米粒子(SiO2@PNIPAM)",
            "concentration": "SiO2核(100nm)，NIPAM单体 0.5wt%",
            "process": "在SiO2种子粒子表面进行NIPAM的沉淀聚合",
            "temperature": "70°C聚合",
            "time": "聚合反应4小时",
            "characterization": "DLS测温度响应粒径变化，TEM观察核壳结构",
            "result": "25°C时粒径约200nm(PNIPAM壳膨胀)，35°C时约130nm(壳塌缩)，温度响应可逆",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R022",
            "material": "甲基纤维素热可逆凝胶",
            "concentration": "甲基纤维素(MC) 2wt%",
            "process": "MC在冷水中分散(0°C)，缓慢升温至室温溶解，继续升温形成凝胶",
            "temperature": "0°C分散，25°C溶解，50-60°C凝胶化",
            "time": "溶解过夜，升温后约30分钟凝胶化",
            "characterization": "流变仪温度扫描测G'/G''交叉温度",
            "result": "约50°C时G'=G''(凝胶点)，60°C时G'约1kPa。冷至室温后可逆回到溶液态",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R023",
            "material": "壳聚糖/明胶复合支架",
            "concentration": "壳聚糖 2wt%，明胶 5wt%，京尼平交联剂 0.5wt%",
            "process": "壳聚糖和明胶分别溶于醋酸溶液，混合后加入京尼平交联，冷冻干燥",
            "temperature": "37°C交联，-80°C冷冻后冻干",
            "time": "交联6小时，冷冻干燥48小时",
            "characterization": "SEM观察孔结构，力学测试，细胞毒性测试",
            "result": "制得多孔支架(孔径100-300μm，孔隙率>85%)，压缩模量约50kPa，细胞存活率>90%",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R024",
            "material": "光固化水凝胶(PEGDA)",
            "concentration": "PEGDA(700Da) 10wt%，光引发剂Irgacure 2959 0.05wt%",
            "process": "PEGDA和光引发剂溶于PBS缓冲液，紫外光照射固化",
            "temperature": "25°C",
            "time": "365nm紫外光照射5分钟",
            "characterization": "流变仪测G'，溶胀实验，细胞包封活力测试",
            "result": "固化后G'约2kPa，溶胀比约10:1，包封细胞存活率>80%",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R025",
            "material": "导电水凝胶(PEDOT:PSS/PVA)",
            "concentration": "PEDOT:PSS分散液 1.1wt%，PVA 5wt%",
            "process": "将PEDOT:PSS与PVA溶液混合，浇铸成膜后DMSO后处理提高导电性",
            "temperature": "25°C浇铸，120°C DMSO蒸汽处理",
            "time": "浇铸干燥12小时，DMSO处理30分钟",
            "characterization": "四探针法测电导率，拉伸测试",
            "result": "电导率约10 S/cm(DMSO处理后提高约100倍)，拉伸强度约2MPa，断裂伸长率约50%",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R026",
            "material": "磁性纳米粒子(Fe3O4)共沉淀法制备",
            "concentration": "FeCl3 0.2M，FeCl2 0.1M，NH3·H2O",
            "process": "共沉淀法: 混合Fe3+/Fe2+溶液，在碱性条件下沉淀生成Fe3O4纳米粒子",
            "temperature": "80°C反应",
            "time": "反应30分钟",
            "characterization": "XRD确认晶相，TEM测粒径，VSM测磁性能",
            "result": "制得超顺磁Fe3O4纳米粒子，平均直径约12nm，饱和磁化强度约60emu/g",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R027",
            "material": "静电纺丝PVA纳米纤维膜",
            "concentration": "PVA 8wt%(溶于去离子水)",
            "process": "静电纺丝: 注射泵推进PVA溶液，施加15kV高压，接收距离15cm",
            "temperature": "25°C，相对湿度<50%",
            "time": "纺丝2小时",
            "characterization": "SEM测纤维直径，BET测比表面积",
            "result": "制得均匀PVA纳米纤维膜，平均纤维直径约200nm，比表面积约15m2/g",
            "safety_level": "medium",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R028",
            "material": "脂质体薄膜水化法制备",
            "concentration": "卵磷脂 10mg/mL，胆固醇 4mg/mL(氯仿溶液)",
            "process": "薄膜水化法: 旋转蒸发去除氯仿形成脂质薄膜，PBS水化，挤出控制粒径",
            "temperature": "40°C旋转蒸发，水化室温",
            "time": "旋转蒸发30分钟，水化2小时，挤出21次",
            "characterization": "DLS测粒径，荧光法测包封率",
            "result": "制得单层脂质体，平均直径约120nm，PDI<0.2",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R029",
            "material": "氧化石墨烯(GO)液晶",
            "concentration": "GO 1wt%水分散液",
            "process": "改良Hummers法制备GO: 石墨+KMnO4+浓H2SO4氧化，透析纯化至中性",
            "temperature": "冰浴(<5°C)氧化反应",
            "time": "氧化反应2小时，透析5天",
            "characterization": "AFM测片层厚度，偏光显微镜观察液晶态，XRD",
            "result": "制得单层GO(厚约1nm，横向尺寸约1μm)，1wt%分散液呈向列型液晶",
            "safety_level": "high",
            "source": "课程实验讲义",
            "is_example": "true"
        },
        {
            "id": "R030",
            "material": "温度/pH双响应微凝胶",
            "concentration": "NIPAM 0.5M，丙烯酸(AA) 0.05M，BIS 5mol%",
            "process": "无皂乳液聚合: NIPAM和AA共聚，BIS交联",
            "temperature": "70°C聚合",
            "time": "聚合反应4小时",
            "characterization": "DLS测粒径温度和pH响应，Zeta电位",
            "result": "微凝胶LCST约35°C(比纯PNIPAM略高)，pH>5时因AA去离子化而溶胀。可用于多重响应药物释放。",
            "safety_level": "low",
            "source": "课程实验讲义",
            "is_example": "true"
        },
    ]
    write_csv(DATA_DIR / "experiment_recipes.csv", fieldnames, rows)
    return len(rows)


# =========================================================================
# 4. sample_questions.csv
# =========================================================================
def generate_questions():
    fieldnames = ["id", "question", "expected_answer", "category",
                  "difficulty", "data_source"]
    rows = [
        {
            "id": "Q001",
            "question": "什么是剪切变稀？为什么洗发水和番茄酱会表现出类似行为？",
            "expected_answer": "剪切变稀是指流体的表观粘度随剪切速率增大而降低的现象。洗发水中的高分子增稠剂在静止时形成缠结网络，剪切时链沿流动方向取向，缠结减少，粘度降低。番茄酱中的果胶网络在剪切下被破坏，释放出被捕获的水分，降低了有效粘度。",
            "category": "流变学",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q002",
            "question": "解释胶体稳定性的DLVO理论，并说明如何通过Zeta电位判断胶体稳定性。",
            "expected_answer": "DLVO理论认为胶体粒子间的总相互作用势能是van der Waals吸引势和双电层排斥势的叠加。当Zeta电位绝对值大于30mV时，双电层排斥力足以克服van der Waals吸引力，胶体体系通常是稳定的。加入电解质会压缩双电层，降低排斥势垒，导致聚沉。",
            "category": "胶体科学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q003",
            "question": "比较物理交联水凝胶和化学交联水凝胶的优缺点。",
            "expected_answer": "物理交联水凝胶: 优点是可自修复、可注射、生物降解性好、无需化学引发剂; 缺点是力学强度较低、稳定性较差。化学交联水凝胶: 优点是力学强度高、稳定性好、溶胀行为可预测; 缺点是不可逆、降解困难、可能有未反应交联剂残留。",
            "category": "水凝胶",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q004",
            "question": "嵌段共聚物在什么条件下会形成柱状微相分离结构？",
            "expected_answer": "嵌段共聚物的微相分离结构取决于χN(相互作用参数与聚合度的乘积)和各嵌段的体积分数f。当χN>10.5(强分离极限)且某一嵌段的体积分数f在约0.2-0.35范围内时，形成柱状结构。在弱分离极限(χN约10.5-20)附近，相图边界略有不同。",
            "category": "高分子科学",
            "difficulty": "hard",
            "data_source": "curated_example"
        },
        {
            "id": "Q005",
            "question": "Pickering乳液与传统表面活性剂稳定的乳液有何区别？",
            "expected_answer": "Pickering乳液由固体粒子(如SiO2纳米粒子)稳定，传统乳液由表面活性剂稳定。Pickering乳液的优势: 热力学更稳定(粒子脱附能高)、无表面活性剂残留(食品和化妆品友好)、稳定性好。缺点是粒子制备和功能化成本较高。粒子的接触角决定乳液类型。",
            "category": "乳液",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q006",
            "question": "解释PNIPAM水凝胶的LCST行为及其应用。",
            "expected_answer": "PNIPAM在约32°C(低临界溶解温度LCST)发生亲水-疏水转变。低于LCST时PNIPAM链与水形成氢键，水凝胶溶胀; 高于LCST时疏水相互作用占主导，凝胶塌缩排出水分。应用包括: 温度响应药物释放、智能阀门、细胞片层回收和温度传感器。",
            "category": "智能材料",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q007",
            "question": "高分子溶液的Flory-Huggins相互作用参数χ的物理意义是什么？",
            "expected_answer": "χ参数反映高分子链段与溶剂分子间的相互作用与同种分子间相互作用的差异。χ<0.5时，高分子-溶剂相互作用有利(良溶剂)，溶液混合性好。χ=0.5是θ条件，排斥体积效应为零。χ>0.5时高分子-溶剂相互作用不利(不良溶剂)，倾向于相分离。χ=kT·z·Δw/(kT)与交换能有关。",
            "category": "高分子科学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q008",
            "question": "如何用流变学方法区分粘弹性固体和粘弹性流体？",
            "expected_answer": "通过小振幅振荡剪切(SAOS)测试: 在宽频率范围内测量储能模量G'和损耗模量G''。粘弹性固体: G'>G''在整个频率范围内，低频区G'趋于平台值(不趋于零)。粘弹性流体: 低频区G''>G'(流动主导)，高频区G'>G''(弹性主导)，存在G'=G''的交叉频率(反比于松弛时间)。",
            "category": "流变学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q009",
            "question": "什么是凝胶渗透色谱(GPC)的原理？它能提供哪些分子量信息？",
            "expected_answer": "GPC/SEC的原理是基于体积排阻: 多孔凝胶填料中的孔洞只允许小于一定尺寸的分子进入，大分子先流出，小分子后流出。通过标准品校准保留时间-分子量关系，可得到数均分子量Mn、重均分子量Mw、Z均分子量Mz和多分散性指数PDI=Mw/Mn，以及完整的分子量分布曲线。",
            "category": "表征方法",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q010",
            "question": "对比加成聚合和缩合聚合的主要区别。",
            "expected_answer": "加成聚合: 链式反应机理，活性中心(自由基、离子)逐一加成单体，不生成小分子副产物，高分子量产物在低转化率时就已形成。缩合聚合: 逐步反应机理，任何两个带有可反应官能团的分子都可反应，每步生成小分子(如水)，高分子量产物仅在高转化率(>99%)时形成。",
            "category": "高分子科学",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q011",
            "question": "解释为什么玉米淀粉和水的混合物在快速搅拌时变硬(剪切增稠)。",
            "expected_answer": "玉米淀粉悬浮液是剪切增稠(胀流性)流体。在低剪切速率下，淀粉粒子间有足够的水作为润滑层，粒子可以相互滑动。高剪切速率下，粒子被迫紧密堆积，水被挤出粒子间隙，粒子直接接触形成摩擦阻塞(jamming)，宏观表现为粘度急剧增大甚至固体化。",
            "category": "流变学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q012",
            "question": "如何设计一个自修复高分子材料？主要有哪些策略？",
            "expected_answer": "自修复策略包括: (1)外援型: 在基体中包封修复剂(如微胶囊、中空纤维)，破裂时释放修复剂; (2)本征型: 利用可逆化学键(如Diels-Alder反应、二硫键交换、UPy四重氢键、金属配位)在损伤后重新形成连接。本征型可多次修复但力学强度通常低于外援型。温度、光或湿度等外部刺激可加速修复。",
            "category": "智能材料",
            "difficulty": "hard",
            "data_source": "curated_example"
        },
        {
            "id": "Q013",
            "question": "什么是表面活性剂的HLB值？如何用它选择乳化剂？",
            "expected_answer": "HLB(亲水-亲油平衡)值是表面活性剂亲水性的量化指标，范围约1-40。HLB 3-6适合W/O乳液(如Span类)，HLB 8-18适合O/O乳液(如Tween类)。选择乳化剂的原则: 油相所需HLB值匹配。混合乳化剂的HLB值可加权计算。HLB方法是经验性的，不如HLD方法精确但更简便。",
            "category": "表面活性剂",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q014",
            "question": "SEM和TEM在软物质表征中各自的优缺点是什么？",
            "expected_answer": "SEM: 观察表面形貌，景深大(三维感)，样品制备相对简单(喷金即可)，分辨率约1nm。TEM: 观察内部结构/截面，分辨率更高(亚nm)，但样品制备复杂(超薄切片或负染色)，只能观察薄膜或极小样品。软物质对电子束敏感，SEM需低加速电压，TEM需冷冻(cryo-TEM)以减少损伤。",
            "category": "表征方法",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q015",
            "question": "嵌段共聚物自组装与小分子表面活性剂自组装有何异同？",
            "expected_answer": "相同点: 都是两亲分子在选择性溶剂中自发组装，驱动力是疏水效应等非共价相互作用。不同点: (1)嵌段共聚物CMC极低，更稳定; (2)嵌段共聚物组装体更大(10-100nm vs 1-10nm); (3)嵌段共聚物可形成更多样化的形貌(球、柱、层、囊泡等); (4)嵌段共聚物组装体的动力学更慢(冻结态)。",
            "category": "自组装",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q016",
            "question": "什么是静电纺丝？影响纤维形貌的因素有哪些？",
            "expected_answer": "静电纺丝利用高压电场(10-30kV)将高分子溶液或熔体拉伸成纳米纤维。影响因素: (1)溶液参数: 浓度(决定粘度)、分子量、导电性; (2)工艺参数: 电压、流速、接收距离; (3)环境参数: 温度、湿度。浓度过低形成珠串(beads-on-string)，浓度过高难以启动泰勒锥。最佳条件获得均匀纤维。",
            "category": "制备方法",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q017",
            "question": "胶体晶体为什么能呈现结构色？与染料着色有何不同？",
            "expected_answer": "结构色源于光子晶体结构的布拉格衍射: 当光的波长与胶体晶体的周期性间距匹配时发生相干散射。与染料不同: (1)不依赖化学发色团，颜色不会褪色; (2)颜色随观察角度变化; (3)可通过改变粒子间距(如温度、pH响应)调控颜色。自然界中蝴蝶翅膀、蛋白石等都是结构色的例子。",
            "category": "胶体科学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q018",
            "question": "解释聚合物刷的抗蛋白吸附机制。",
            "expected_answer": "聚合物刷(如PEG刷)的抗蛋白吸附机制主要有两种: (1)体积排斥效应(熵排斥): 蛋白进入刷层会压缩聚合物链，减少链构象熵，产生排斥力; (2)水化层效应: PEG的醚氧原子与水分子形成氢键，形成紧密的水化层，蛋白要接近表面必须脱水(热力学不利)。刷密度和链长是关键参数。",
            "category": "界面科学",
            "difficulty": "hard",
            "data_source": "curated_example"
        },
        {
            "id": "Q019",
            "question": "在设计药物递送系统时，如何选择合适的载体材料？",
            "expected_answer": "选择依据: (1)生物相容性和降解性(PLGA、脂质体、壳聚糖等); (2)药物亲疏水性决定载体类型(疏水药用聚合物胶束或脂质体，亲水药用凝胶); (3)释放动力学需求(快速释放用凝胶，缓释用聚合物微球); (4)靶向需求(表面修饰靶向配体); (5)给药途径(口服需耐酸，注射需纳米级)。",
            "category": "药物递送",
            "difficulty": "hard",
            "data_source": "curated_example"
        },
        {
            "id": "Q020",
            "question": "如何区分触变性和简单的剪切变稀？",
            "expected_answer": "触变性涉及时间维度，而简单剪切变稀是瞬时响应。区分方法: (1)阶跃剪切测试: 施加恒定剪切速率，触变性流体的粘度随时间持续下降直至平衡，而简单剪切变稀流体的粘度几乎不随时间变化; (2)滞后环测试: 上行和下行流动曲线不重合的是触变性; (3)振荡时间扫描: 触变性材料的G'在恒定应变下持续下降。",
            "category": "流变学",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q021",
            "question": "双网络水凝胶为什么比单网络水凝胶更坚韧？",
            "expected_answer": "双网络(DN)凝胶包含一个刚而脆的第一网络(牺牲网络)和一个柔而韧的第二网络。受力时第一网络优先断裂(牺牲键断裂)，消耗大量能量，保护第二网络完整性。断裂的第一网络碎片仍存在于第二网络中，维持材料的完整性。这种能量耗散机制使DN凝胶兼具高强度和高韧性，类似天然软骨。",
            "category": "水凝胶",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
        {
            "id": "Q022",
            "question": "为什么聚乳酸(PLA)被认为是一种环境友好材料？它的局限性是什么？",
            "expected_answer": "PLA的环保性: 来源于可再生资源(玉米淀粉发酵得到乳酸)，可在工业堆肥条件下水解降解为CO2和水。局限性: (1)降解需要特定条件(工业堆肥58°C，湿度>80%)，自然环境中降解很慢; (2)脆性大(断裂伸长率<10%); (3)热稳定性差(使用温度<Tg约58°C); (4)与其他塑料回收流混合会造成污染。",
            "category": "高分子科学",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q023",
            "question": "解释蠕虫状胶束与柔性高分子链在流变行为上的相似性和差异。",
            "expected_answer": "相似性: 低浓度下都表现出粘弹性，可用Rouse或Zimm模型描述，松弛时间谱相似。差异: (1)蠕虫状胶束是瞬态网络，可以被剪切断链和重新连接(reptation+breaking机制)，导致在高剪切下粘度快速下降; (2)高分子链是永久共价键连接，不会在剪切中断裂; (3)蠕虫状胶束长度随浓度和温度变化(活的聚合物)。",
            "category": "流变学",
            "difficulty": "hard",
            "data_source": "curated_example"
        },
        {
            "id": "Q024",
            "question": "列举三种常见的软物质表征方法，说明它们分别能提供什么信息。",
            "expected_answer": "示例: (1)动态光散射(DLS): 测量流体力学半径和粒径分布，适用于胶体粒子和纳米聚集体; (2)小角X射线散射(SAXS): 测量1-100nm尺度的内部结构(形状、尺寸、周期性排列); (3)旋转流变仪: 测量粘度、模量、松弛时间等流变学参数，反映材料的宏观力学行为。三者分别提供尺寸、结构和力学信息。",
            "category": "表征方法",
            "difficulty": "easy",
            "data_source": "curated_example"
        },
        {
            "id": "Q025",
            "question": "在什么情况下你应该拒绝回答学生关于实验方案的问题？",
            "expected_answer": "当问题涉及: (1)高危试剂(浓硫酸、氢氟酸、氰化物等)的具体操作细节且缺乏安全防护说明时; (2)要求提供超出教学范围的具体处方(如药品精确剂量)时; (3)证据不足时编造实验数据或论文; (4)声称系统输出可直接作为实验操作SOP。应提醒教师复核和安全审核。",
            "category": "幻觉防护",
            "difficulty": "medium",
            "data_source": "curated_example"
        },
    ]
    write_csv(DATA_DIR / "sample_questions.csv", fieldnames, rows)
    return len(rows)


# =========================================================================
# 5. feedback.csv
# =========================================================================
def generate_feedback():
    fieldnames = ["timestamp", "question_id", "rating", "comment"]
    rows = [
        {
            "timestamp": "2025-05-20 09:15:00",
            "question_id": "Q001",
            "rating": 5,
            "comment": "解释清楚，洗发水的例子很好理解"
        },
        {
            "timestamp": "2025-05-20 10:30:00",
            "question_id": "Q003",
            "rating": 4,
            "comment": "对比表格很有帮助，希望能补充更多例子"
        },
        {
            "timestamp": "2025-05-21 14:20:00",
            "question_id": "Q006",
            "rating": 5,
            "comment": "LCST解释得很好，应用举例很实用"
        },
        {
            "timestamp": "2025-05-21 16:45:00",
            "question_id": "Q011",
            "rating": 3,
            "comment": "能回答但缺少图示，理解起来还是有困难"
        },
        {
            "timestamp": "2025-05-22 08:50:00",
            "question_id": "Q002",
            "rating": 4,
            "comment": "DLVO理论解释到位，但希望能画势能曲线图"
        },
    ]
    write_csv(DATA_DIR / "feedback.csv", fieldnames, rows)
    return len(rows)


# =========================================================================
# 6. settings.json
# =========================================================================
def generate_settings():
    settings = {
        "current_model": "qwen2.5:7b",
        "ollama_url": "http://localhost:11434",
        "top_k": 5,
        "similarity_threshold": 0.3,
        "language": "zh-CN",
        "safety_level": "standard",
        "show_evidence_cards": True,
        "show_confidence_score": True,
        "max_response_length": 2000,
        "teacher_review_enabled": True,
        "feedback_enabled": True,
        "data_stats": {
            "knowledge_count": 60,
            "literature_count": 25,
            "recipe_count": 30,
            "question_count": 25,
            "data_status": "curated_teaching_examples",
            "note": "所有文献记录和部分配方为教学示例(curated_example)，非真实PDF解析结果。系统支持后续导入真实PDF数据。"
        }
    }
    filepath = DATA_DIR / "settings.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    print(f"  Written settings -> {filepath}")
    return 1


# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    print("Generating SoftMatterGPT data files...")
    print()

    n_k = generate_knowledge()
    n_l = generate_literature()
    n_r = generate_recipes()
    n_q = generate_questions()
    n_f = generate_feedback()
    n_s = generate_settings()

    print()
    print("Summary:")
    print(f"  softmatter_knowledge.csv : {n_k} records")
    print(f"  literature_records.csv   : {n_l} records")
    print(f"  experiment_recipes.csv   : {n_r} records")
    print(f"  sample_questions.csv     : {n_q} records")
    print(f"  feedback.csv             : {n_f} records")
    print(f"  settings.json            : {n_s} file")
    print()
    print("All data marked as curated teaching examples.")
    print("No real PDFs downloaded or parsed.")
