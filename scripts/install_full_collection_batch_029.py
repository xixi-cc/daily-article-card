#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 029."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "doi-10.1017-jfm.2017.235",
        "source_version": "version of record",
        "source_pdf": "https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B8ED6B4C41BABE77EA7FFC6E6AA6F691/S002211201700235Xa_hi.pdf/faraday-wave-droplet-dynamics-discrete-time-analysis.pdf",
        "title_en": "Faraday wave–droplet dynamics: discrete-time analysis",
        "title_zh": "法拉第波—液滴动力学：离散时间分析",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["b9d281d536ae599d"], ["Fluid Dynamics"]),
        "verified_metadata": {"doi": "10.1017/jfm.2017.235", "version": "version of record", "title": "Faraday wave–droplet dynamics: discrete-time analysis", "authors": ["Matthew Durey", "Paul A. Milewski"], "journal": "Journal of Fluid Mechanics", "volume": "821", "pages": "296–329", "published": "2017-05-22", "abstract": "A first-principles discrete-time model couples impulsive droplet impacts to continuous Faraday-wave propagation and analyzes walking, bound states and confined dynamics.", "comment": "Open-access version of record, CC BY"},
        "sections": [
            sec("作者信息", r"作者 Matthew Durey、Paul A. Milewski；Journal of Fluid Mechanics 821, 296–329 (2017)，DOI:10.1017/jfm.2017.235，2017-05-22 首次在线。核验的是 34 页开放获取期刊版，全文同时给出模型推导、线性稳定性、双液滴态与受限混沌数值。"),
            sec("研究问题", r"受振液浴上的行走液滴每次撞击都会激发长寿命 Faraday 波，后续撞击又受到整段波场历史的反馈。论文问：能否不直接积分每个快速接触过程，而把一次撞击压缩成离散更新、把撞击间的波传播保留为连续线性动力学，并由同一模型统一解释静止弹跳、稳态行走、双液滴轨道以及谐势阱中的统计量子化？"),
            sec("背景", r"高记忆区的 pilot-wave 实验呈现 walkers、promenade modes、离散轨道半径和看似量子化的统计，但连续时模型常混合快速垂直碰撞、水平滑移和慢波场，参数作用难以分离。作者把碰撞理想化为瞬时冲量，把自由表面展开为傅里叶–贝塞尔模，并以碰撞编号 n 作为自然时间。这样，记忆不是经验性位置核，而由每个波数模在相邻撞击之间的传播与衰减直接累积。", r"Figure 5 展示双液滴轨道直径随驱动比 Γ/ΓF 的分支：同相和反相响应对应不同离散轨道，部分分支发生 wobbling。图是模型的分岔与稳定性结果，不是新实验数据。"),
            sec("模型与方法", r"一次碰撞把液滴水平速度与波模振幅/导数映射到下一时刻；撞击间用线性化自由表面方程传播。稳定行走被写为每次撞击后平移 δx 的固定点，波模满足 a_{n+1}(k)=A(k;δx)a_n(k)。作者先解自洽步长与波场，再线性化完整 transition map，以谱半径判定 bouncing/walking 分支稳定性；平移对称性必然带来一个中性特征值。", r"双液滴部分叠加两者激发的波场并求相对相位、间距或轨道半径；谐约束部分长时间迭代离散映射，对角动量和轨道半径做聚类。所谓 quantization 是稳定分支或经验分布簇，不是波函数本征值；数值中使用固定撞击相位、恢复系数与滑移摩擦参数。"),
            sec("核心结果与证据", r"单液滴分析得到静止弹跳失稳并连续分岔为 steady walking；walking threshold 由除平移中性模外的最大特征值穿过单位圆确定。模型进一步预测同相、反相双液滴的离散 bound states、圆周轨道和 promenade modes，Figure 5 给出轨道直径分支及其稳定区。", r"在各向同性谐势中，确定性轨迹可进入不规则/混沌运动；对长时间序列聚类后，角动量与平均半径在若干区域聚集，作者称为 double quantization。这里的证据是特定参数离散模型的数值统计，不能推出实验中所有能级结构，也没有建立量子动力学等价。", r"模型价值在于同一冲击—传播映射连接稳定性、相互作用与受限轨迹；Figure 5 与后续相图同时显示结果对驱动、相位和摩擦敏感，因此“离散态”不是无参数的普适常数。"),
            sec("有效性与局限", r"推导假设碰撞瞬时、垂直弹跳周期固定、液面响应在线性 Faraday 阈值以下，且撞击参数不随轨迹历史改变。真实接触时间、非线性波、空气层、液滴形变和垂直—水平耦合都被压缩进有效冲量。", r"双液滴量子化与分支稳定性依赖 impact phase 和 skidding friction；高记忆极限下有限模截断与长时间误差也需检查。谐势中的簇由数值轨迹和所选 clustering procedure 得出，未给独立实验复现或对所有初值的遍历性证明。"),
            sec("复现与资源", r"开放期刊版：https://doi.org/10.1017/jfm.2017.235；核验 PDF SHA-256：d57c6aa4678b916fb796ebb307147797fb2cc718ba35285d4d64faa456ecfb2e。复现需固定液体参数、驱动比、撞击周期/相位、恢复和滑移系数、波数积分截断、transition matrix、初值、积分精度、稳定性特征值筛选以及聚类规则。", r"应分别验证固定点残差、平移中性特征值、网格/波数收敛和长时统计稳定性，再与实验几何对照。Evidence status: full-text verified version of record; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.296–304 的冲击假设与波传播，再读 steady-walking 固定点和 pp.310–313 的 Eqs. (5.3)–(5.9)。核心图看 p.316 Figure 5；随后读双液滴稳定性和受限混沌章节。阅读时把解析/线性稳定性结论、模型数值分支与实验类比三种证据分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1017-jfm.2017.235/figure-5-orbit-quantization.webp", "label": "Figure 5", "visual_type": "bifurcation_plot", "evidence": "paper.pdf p. 21, Figure 5", "alt_text": "双液滴轨道直径随驱动比变化的分支图和摇摆轨道示意。", "caption": "离散同相/反相轨道分支及其稳定性随驱动变化。", "selection_rationale": "Figure 5 直接呈现离散时间模型最具辨识度的双液滴轨道量子化与分岔证据。"},
        "figure_refs": [figure("doi-10.1017-jfm.2017.235", "figure-5-orbit-quantization.webp", "Figure 5", 21, "show quantized two-droplet orbital branches", "轨道直径随 Γ/ΓF 的稳定和不稳定分支。", "模型产生离散轨道族及 wobbling bifurcation。", "These are model branches whose locations depend on impact phase and friction parameters.")],
        "equation_refs": [
            {"label": "Steady-walking translation map", "latex": r"a_{n+1}(k)=A(k;\delta x)a_n(k)", "role": "express the wave field as a fixed shape translated at each impact", "symbols": {"a_n": "wave-mode state", "delta_x": "horizontal step per impact", "A": "impact-to-impact propagator"}, "evidence": "paper.pdf pp. 10–11, Eqs. (5.3)–(5.4)", "interpretation": "A walking state is a fixed point only in the co-moving, impact-indexed map."},
            {"label": "Linear stability criterion", "latex": r"\rho(\mathcal T)\le 1", "role": "test perturbations of a bouncing or walking fixed point", "symbols": {"rho": "spectral radius", "T": "linearized transition map"}, "evidence": "paper.pdf pp. 11–13, Section 5", "interpretation": "One unit eigenvalue is neutral because translation leaves the unconfined system invariant."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–9: impulsive discrete-time derivation", "paper.pdf pp. 10–13: walking fixed point and spectral stability", "paper.pdf p. 21, Figure 5: orbital branches", "paper.pdf pp. 22–31: bound states and confined chaotic statistics", "source PDF SHA-256 d57c6aa4678b916fb796ebb307147797fb2cc718ba35285d4d64faa456ecfb2e", "Evidence status: full-text verified version of record; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1021-acs.langmuir.1c02581", "source_version": "version of record",
        "source_pdf": "https://europepmc.org/articles/PMC8928473?pdf=render",
        "title_en": "Field-Induced Assembly and Propulsion of Colloids", "title_zh": "外场诱导的胶体组装与推进",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["614f7945e1f9bb95"], ["Soft Matter"]),
        "verified_metadata": {"doi": "10.1021/acs.langmuir.1c02581", "version": "version of record", "title": "Field-Induced Assembly and Propulsion of Colloids", "authors": ["Ahmed Al Harraq", "Brishty Deb Choudhury", "Bhuvnesh Bharti"], "journal": "Langmuir", "volume": "38", "issue": "10", "pages": "3001–3016", "published": "2022-03-03", "abstract": "An invited feature review organizes electric- and magnetic-field-driven colloidal assembly and propulsion and emphasizes their continuum.", "comment": "Open-access invited feature article, CC BY"},
        "sections": [
            sec("作者信息", r"作者 Ahmed Al Harraq、Brishty Deb Choudhury、Bhuvnesh Bharti；Langmuir 38(10), 3001–3016 (2022)，DOI:10.1021/acs.langmuir.1c02581，在线发表于 2022-03-03。核验 16 页开放期刊版。本文是 invited feature review，主要贡献是分类、综合和前景判断，不是单一新实验。"),
            sec("研究问题", r"外加电场或磁场既可诱导胶体间各向异性作用而形成链、晶格和动态簇，也可驱动单粒子或组装体平移/转动。文章问：怎样用共同的物理语言比较电、磁响应，如何区分静态/动态组装与被动/主动推进，以及为何“先组装后推进”和“推进导致组装”在非平衡体系中构成连续谱而非互斥类别？"),
            sec("背景", r"胶体尺度上热涨落显著，外场则提供可调方向、频率和幅值。介电或磁化率反差使粒子产生诱导偶极矩；偶极—偶极能量随 r^{-3} 衰减并依赖取向，因此天然产生链状和层状结构。时间变化场还会引入相位滞后、旋转力矩、流体动力耦合与耗散，令动态簇持续重排。", r"Figure 10 以 propulsion force 与 assembly force 的相对大小画出分类示意：一端是组装主导的静态结构，另一端是推进主导的独立 swimmers，中间包含 assembly-driven propulsion 与 propulsion-driven assembly。它是概念图，不是用统一实验数据标定的相图。"),
            sec("模型与方法", r"综述先写出球形粒子的诱导电/磁偶极矩，其尺度为介质响应乘 R^3 和外场；再用标准各向异性偶极对势解释端对端吸引与侧向排斥。随后按 DC/AC 电场、均匀/梯度磁场、旋转场和组合场整理代表性实验，并按结构是否保持、是否持续耗能、是否产生净位移分类。", r"文中的图像和性能数字来自不同材料、粒径、溶剂、场频率和边界条件，不能横向视作统一 benchmark。Figure 10 是作者对文献的机制综合；推力—组装力坐标主要为定性组织框架。"),
            sec("核心结果与证据", r"静态部分显示外场可把各向同性悬浮液可逆组装为链、片层、胶体晶体和复杂簇；动态场可产生旋转链、vortices、metachronal structures 和持续重构的非平衡集合。推进部分比较磁性螺旋、表面滚动、ICEP/induced-charge electro-osmosis 等机制，强调时间反演破缺和壁面/流体耦合。", r"综合结论是 assembly 与 propulsion 不宜分开设计：粒子间作用能改变个体速度和方向，主动运动又改变碰撞、聚集和稳态结构。Figure 10 把中间区标为两种协同机制，提出通过场参数实时切换功能的材料设计路线。", r"作者列出的挑战包括亚微米尺度 Brownian force 压倒弱驱动、可用磁/介电材料与生物相容性限制、密集群体精确操控，以及非平衡态熵产生和有效相互作用的定量测量。"),
            sec("有效性与局限", r"这是选择性 feature review，不声称系统综述的完整检索或 meta-analysis；不同引用实验的几何、Reynolds 数、Péclet 数和场强不可直接比较。诱导偶极近似忽略多体极化、近场、电双层、非球形、表面粗糙和复杂流变，浓悬浮液中尤其可能失效。", r"静态/动态、被动/主动标签取决于观察时间尺度与能量核算；Figure 10 的边界没有统一量纲阈值。医学或微机器人应用仍受加热、毒性、穿透深度、控制带宽和体内环境制约，综述中的潜在应用不是临床有效性证据。"),
            sec("复现与资源", r"期刊页：https://doi.org/10.1021/acs.langmuir.1c02581；开放全文：https://pmc.ncbi.nlm.nih.gov/articles/PMC8928473/。核验 PDF SHA-256：e57543183565631176f05d12245c98466a3042e09fd3c55cd6857eeb9053de87。复核具体系统须回到原始引用，记录粒径/形状、susceptibility、溶剂、电导率、频率、场幅、边界、体积分数、温度和轨迹处理。", r"若将 Figure 10 转成定量设计图，还需独立定义并测量 propulsion/assembly forces、Brownian scale 与 hydrodynamic interactions。Evidence status: full-text verified version-of-record review; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.3002–3004 的诱导偶极和相互作用，再按兴趣选读磁场或电场实例。最后集中读 pp.3012–3014 的 Figure 10 与 outlook。将基础方程、来自被引原始实验的观察、以及作者提出的统一分类分别标注，避免把综述示意当成测量相图。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1021-acs.langmuir.1c02581/figure-10-assembly-propulsion.webp", "label": "Figure 10", "visual_type": "conceptual_diagram", "evidence": "paper.pdf p. 12, Figure 10", "alt_text": "组装力与推进力竞争下胶体行为连续谱的概念示意。", "caption": "从组装主导到推进主导，中间包含两种协同的非平衡机制。", "selection_rationale": "Figure 10 是综述的综合性结论，最直接表达 assembly 与 propulsion 不是割裂类别。"},
        "figure_refs": [figure("doi-10.1021-acs.langmuir.1c02581", "figure-10-assembly-propulsion.webp", "Figure 10", 12, "organize the assembly–propulsion continuum", "推进力与组装力竞争的概念分类。", "协同机制位于静态组装与独立推进之间。", "The axes are qualitative and do not constitute a uniformly measured phase diagram.")],
        "equation_refs": [
            {"label": "Induced electric dipole scale", "latex": r"p=4\pi\epsilon_m R^3 K E", "role": "set the field-induced polarization scale of a spherical colloid", "symbols": {"epsilon_m": "medium permittivity", "R": "particle radius", "K": "contrast factor", "E": "electric field"}, "evidence": "paper.pdf p. 3, Eq. (1)", "interpretation": "The cubic size dependence makes field response strongly particle-size dependent."},
            {"label": "Dipole-pair interaction", "latex": r"U_{dd}\propto\frac{\mathbf p_1\!\cdot\!\mathbf p_2-3(\mathbf p_1\!\cdot\!\hat{\mathbf r})(\mathbf p_2\!\cdot\!\hat{\mathbf r})}{r^3}", "role": "explain anisotropic chain-forming interactions", "symbols": {"p_i": "induced dipoles", "r": "center separation"}, "evidence": "paper.pdf p. 3, Eq. (3)", "interpretation": "Orientation determines whether the same applied field produces attraction or repulsion."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: induced dipoles and anisotropic interactions", "paper.pdf pp. 4–11: field-induced static/dynamic assembly and propulsion examples", "paper.pdf p. 12, Figure 10: conceptual continuum", "paper.pdf pp. 13–14: challenges and outlook", "source PDF SHA-256 e57543183565631176f05d12245c98466a3042e09fd3c55cd6857eeb9053de87", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-nature12673", "source_version": "arXiv v1 / version-of-record metadata", "source_pdf": "https://arxiv.org/pdf/1311.2017",
        "title_en": "Emergence of macroscopic directed motion in populations of motile colloids", "title_zh": "运动胶体群体中宏观定向运动的涌现",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8435903d8f185524"], ["Soft Matter"]),
        "verified_metadata": {"doi": "10.1038/nature12673", "arxiv_id": "1311.2017", "version": "v1 accepted manuscript / version-of-record metadata", "title": "Emergence of macroscopic directed motion in populations of motile colloids", "authors": ["Antoine Bricard", "Jean-Baptiste Caussin", "Nicolas Desreumaux", "Olivier Dauchot", "Denis Bartolo"], "journal": "Nature", "volume": "503", "pages": "95–98", "published": "2013-11", "abstract": "Quincke rollers in a racetrack undergo a density-controlled transition from an isotropic gas through polar bands to a homogeneous polar liquid.", "comment": "Full accepted manuscript and supplement on arXiv; VOR metadata checked by DOI"},
        "sections": [
            sec("作者信息", r"作者 Antoine Bricard、Jean-Baptiste Caussin、Nicolas Desreumaux、Olivier Dauchot、Denis Bartolo；Nature 503, 95–98 (2013)，DOI:10.1038/nature12673。核验 arXiv:1311.2017v1 的作者稿及补充材料，并以 DOI 核对期刊元数据；文件共 37 页。"),
            sec("研究问题", r"Vicsek 类模型预言局域趋同可使自推进粒子形成宏观极性运动，但定量实验往往受生物复杂性、边界和难以测量的相互作用限制。本文问：最小的非生物 motile colloids 是否会仅由密度增加发生从各向同性气体到定向群体运动的转变；其阈值、带状共存、涨落和速度相关能否由测得的电静力与流体相互作用解释？"),
            sec("背景", r"PMMA 球悬浮在弱导电液体中并夹在 ITO 电极之间。直流场超过 Quincke threshold 后，电极化失稳使球旋转；近壁面把旋转转换为平移。孤立粒子速度满足 v0 随 sqrt[(E0/EQ)^2−1] 增长。作者使用封闭 racetrack，使全局方向只有顺/逆时针两种并避免入口出口。", r"Figure 2 同时给出跑道、稀气体、传播 polar band、均匀 polar liquid 和全局极化 Π0 随面积分数 Φ0 的变化；临界值约 Φc=3×10^-3。"),
            sec("模型与方法", r"实验跟踪单粒子位置和速度，改变注入面积分数与场强，测量全局极化、局域密度、速度相关和数涨落。稀薄极限下先独立测量两粒子相互作用：电静力排斥控制近距离，受壁面屏蔽的流体动力耦合提供长程取向。", r"理论从位置—取向的随机动力学出发，对配对相互作用做 kinetic closure，得到密度与极化的 hydrodynamic equations，并用测量参数预测线性失稳和相关长度。模型不是仅拟合 Vicsek alignment constant；但仍采用准二维、pairwise、dilute/far-field 近似。"),
            sec("核心结果与证据", r"低于 Φc，速度方向无序且 Π0 接近零；略高于阈值，局域高密度 polar bands 在稀气体中传播；更高密度形成近乎完全极化的均匀 polar liquid。Figure 2 的连续增长和带状区构成 density-controlled transition 的直接证据，顺/逆方向在重复实验中等概率选择，显示自发对称性破缺。", r"在测试场强范围内 Φc 近似不随 E0 改变，作者将其解释为由材料参数决定的阈值。高密度 polar liquid 中测得的数涨落近似 normal，而非早期 active-matter 理论常见的 giant fluctuations；这一观察限于有限跑道、测量窗口和该相互作用机制。", r"由实测两体相互作用导出的 kinetic/hydrodynamic theory 定量再现阈值和速度相关，支持长程流体耦合提供 alignment、电静力排斥稳定间距的机制。实验与理论一致是机制证据，但不是排除全部多体或边界效应的唯一性证明。"),
            sec("有效性与局限", r"系统是准二维、近壁面、直流驱动的 Quincke rollers；racetrack 将取向约束到一个周期方向。结论不能直接外推到三维、无壁面、不同电解质或生物群体。粒子速度与相互作用随场强和高度变化，材料常数解释只在报告范围内成立。", r"理论使用 pairwise additive、far-field 和 dilute closure；接近 polar liquid 的高密度区可能需要多体电极化和 lubrication。所谓“polar liquid”依据极化、密度均匀性和涨落诊断，不等于平衡热力学液体；“首个实验”是论文当时在其定义和文献范围内的优先权陈述。"),
            sec("复现与资源", r"作者稿：https://arxiv.org/abs/1311.2017；期刊：https://doi.org/10.1038/nature12673。核验 PDF SHA-256：c56214aa095484c5bf5a3c32d01da0726ee0805de80c9e0b56a2644f2cac4b62。复现需固定 PMMA 尺寸、油/表面活性剂电导、cell gap、ITO 电压、Quincke 阈值、racetrack 尺寸、面积分数标定、tracking、polarization 定义、窗口和误差棒。", r"机制复核还需独立测量两体径向/角向响应，并在同一参数下求 kinetic closure。Evidence status: full-text verified accepted manuscript plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先读主文 pp.1–3 的 Quincke propulsion、Figure 2 和三种相；再读 pp.3–4 的相互作用与连续理论。补充材料用于核查 cell、tracking、速度标度和 closure。区分直接显微观察、由数据拟合/推断的相互作用、以及 continuum theory 的预测。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-nature12673/figure-2-collective-motion.webp", "label": "Figure 2", "visual_type": "experiment_phase_summary", "evidence": "paper.pdf p. 16, Figure 2", "alt_text": "跑道中的各向同性气体、极性带和极性液体及极化序参量。", "caption": "密度升高使 Quincke rollers 从无序气体经传播带进入均匀极性液体。", "selection_rationale": "Figure 2 将实验几何、三种集体态和密度驱动的极化转变集中在一张图中。"},
        "figure_refs": [figure("doi-10.1038-nature12673", "figure-2-collective-motion.webp", "Figure 2", 16, "show the density-driven collective-motion transition", "跑道显微图、polar band 与 Π0–Φ0 曲线。", "临界面积分数以上出现宏观极性运动。", "The phase labels and threshold apply to the finite quasi-two-dimensional racetrack protocol.")],
        "equation_refs": [
            {"label": "Quincke-roller speed", "latex": r"v_0\propto\sqrt{(E_0/E_Q)^2-1}", "role": "relate isolated-particle propulsion to the applied field above threshold", "symbols": {"E_0": "applied DC field", "E_Q": "Quincke threshold"}, "evidence": "paper.pdf main text p. 1 and Supplementary Methods", "interpretation": "The field sets the individual propulsion speed only after the polarization instability begins."},
            {"label": "Global polarization", "latex": r"\Pi_0=\left|\langle\mathbf v_i/|\mathbf v_i|\rangle_i\right|", "role": "measure macroscopic alignment", "symbols": {"v_i": "tracked particle velocity"}, "evidence": "paper.pdf main text pp. 2–3, Figure 2e", "interpretation": "Values near one indicate a population moving coherently around the racetrack."},
        ],
        "evidence_refs": ["paper.pdf main text pp. 1–3: Quincke propulsion and collective phases", "paper.pdf p. 16, Figure 2: phase summary", "paper.pdf main text pp. 3–4: measured interactions and hydrodynamic theory", "paper.pdf supplement: apparatus, tracking and theoretical derivation", "source PDF SHA-256 c56214aa095484c5bf5a3c32d01da0726ee0805de80c9e0b56a2644f2cac4b62", "Evidence status: full-text verified accepted manuscript plus VOR metadata; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-ncomms8470", "source_version": "version of record", "source_pdf": "https://www.nature.com/articles/ncomms8470.pdf",
        "title_en": "Emergent vortices in populations of colloidal rollers", "title_zh": "胶体滚子群体中的涌现涡旋",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["0a010fa07503f768"], ["Active Matter"]),
        "verified_metadata": {"doi": "10.1038/ncomms8470", "version": "version of record", "title": "Emergent vortices in populations of colloidal rollers", "authors": ["Antoine Bricard", "Jean-Baptiste Caussin", "Debasish Das", "Charles Savoie", "Vijayakumar Chikkadi", "Kyohei Shitara", "Oleksandr Chepizhko", "Fernando Peruani", "David Saintillan", "Denis Bartolo"], "journal": "Nature Communications", "volume": "6", "article": "7470", "published": "2015-06-19", "abstract": "Quincke rollers in circular confinement self-organize into a single macroscopic vortex with an ordered rim and disordered core.", "comment": "Open-access version of record, CC BY"},
        "sections": [
            sec("作者信息", r"作者 Antoine Bricard 等十人；Nature Communications 6, 7470 (2015)，DOI:10.1038/ncomms8470，发表于 2015-06-19。核验 8 页开放期刊版及方法。工作结合圆形微腔实验、粒子模拟和连续场理论。"),
            sec("研究问题", r"自推进粒子在封闭空间中会形成边界层、团簇或多涡结构。本文问：Quincke rollers 在简单圆盘约束内能否自发选择整体旋转方向并形成单一宏观涡旋；涡旋为何同时具有有序外环和稀薄无序内核；这种非均匀结构是通常的两相分离，还是一种由取向—密度耦合维持的新 active phase？"),
            sec("背景", r"单个 PMMA 球在直流场超过 Quincke threshold 后沿底面滚动。无约束时，长程流体动力相互作用促使速度对齐，短程电静力排斥防止塌缩。圆形硬壁又使外侧粒子沿切向运动，边界取向可向体内传播。", r"Figure 3 将实验显微图、径向密度与极化剖面、连续理论和粒子模拟并列；不同容器半径下剖面随 r/Rc 近似塌缩，显示界面宽度与系统尺度共同增长。"),
            sec("模型与方法", r"实验改变圆盘半径 Rc 和全局 packing fraction，跟踪位置与取向并测量方位极化、密度和角速度。粒子模型写成自推进速度、软排斥与三类取向相互作用：polar alignment、由径向结构诱导的转向和 hydrodynamic tensor coupling，再加角噪声及硬壁。", r"从粒子动力学做 mean-field/gradient expansion 得到 density 与 polarization fields 的稳态方程。多数相互作用参数由独立实验获得；排斥作用范围的一个参数按剖面调整。因而“无自由拟合参数”只适用于文中明确指出的特定比较，不应泛化到整套模型。"),
            sec("核心结果与证据", r"超过临界浓度后，全部粒子形成单个稳定旋转 vortex，顺时针和逆时针在重复制备中等概率出现。Figure 3 显示外环密度高、方位极化接近一，内核密度降低且取向无序；实验、理论和模拟对径向剖面及其 Rc 依赖总体一致。", r"若只有排斥与壁面会得到边界积聚，只有 alignment 又不能稳定实测内核；三者竞争才产生有限宽度的旋转环。剖面以 r/Rc 缩放、界面宽度随 Rc 增长，区别于具有固定微观界面宽度的常规相分离。作者据此称其为处在 phase separation 边缘的 thermodynamic active phase。", r"“thermodynamic”在这里指大系统极限下保持的宏观态和缩放结构，不意味着详细平衡或平衡自由能。证据来自有限 Rc 范围内的 collapse、模型和模拟一致性，没有直接测量熵产生。"),
            sec("有效性与局限", r"结论针对圆形、凸、准二维 confinement 和 Quincke rollers；非圆边界、障碍、三维或不同推进机制可产生多涡和缺陷。模型使用 pairwise additive effective interactions、局部 closure 与软排斥，浓密边界层中的多体流体和电极化效应可能改变参数。", r"一个排斥长度经拟合，有限尺寸 collapse 不能单独证明唯一热力学极限。文中指出其他 active suspensions 的 fluid-mediated interaction 形式可能不同，故单涡与自相似界面不是所有极性 active matter 的普适性质。"),
            sec("复现与资源", r"期刊：https://doi.org/10.1038/ncomms8470；开放全文：https://pmc.ncbi.nlm.nih.gov/articles/PMC4557359/。核验 PDF SHA-256：562177ec861e674455f4817445dd4fd03ed90b7cd25d51da508b025f56725f00。复现需固定粒径、cell gap、电场/阈值、圆盘半径、packing fraction、壁面处理、tracking、径向 binning、相互作用核、噪声、排斥范围与模拟初值。", r"应同时报告顺逆旋转频率、稳态等待时间、剖面误差和有限尺寸 collapse，而非只展示一帧涡旋。Evidence status: full-text verified version of record; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.1–3 的实验现象和浓度转变，再把 p.4 Figure 3 的实验、理论、模拟三列逐项比较；随后读 pp.4–6 的 Eqs. (1)–(3) 与 continuum closure。最后读讨论，特别核对 self-similar interface 与普通 phase separation 的区别和适用边界。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-ncomms8470/figure-3-collective-vortex.webp", "label": "Figure 3", "visual_type": "experiment_theory_comparison", "evidence": "paper.pdf p. 4, Figure 3", "alt_text": "圆形腔内胶体滚子涡旋的实验、理论与模拟径向结构。", "caption": "有序高密度外环包围稀薄无序内核，剖面随系统尺寸近似自相似。", "selection_rationale": "Figure 3 同时承载宏观涡旋结构、尺寸缩放和三种证据来源的直接对照。"},
        "figure_refs": [figure("doi-10.1038-ncomms8470", "figure-3-collective-vortex.webp", "Figure 3", 4, "compare vortex profiles across experiment, theory and simulation", "不同 Rc 下的密度与极化径向剖面。", "有序环和无序核的自相似结构在三种方法中对应。", "Finite-size collapse supports but does not uniquely prove a thermodynamic phase-separation mechanism.")],
        "equation_refs": [
            {"label": "Roller translation", "latex": r"\partial_t\mathbf r_i=v_0\mathbf p_i-\nabla_{\mathbf r_i}\sum_{j\ne i}H_{\rm rep}(\mathbf r_i-\mathbf r_j)", "role": "combine self-propulsion with short-range repulsion", "symbols": {"v_0": "single-roller speed", "p_i": "orientation", "H_rep": "repulsive potential"}, "evidence": "paper.pdf p. 4, Eq. (1)", "interpretation": "Repulsion regulates density while propulsion transports particles around the cavity."},
            {"label": "Effective orientational interaction", "latex": r"H=A(r)\mathbf p_i\cdot\mathbf p_j+B(r)\hat{\mathbf r}\cdot\mathbf p_i+C(r)\mathbf p_j\cdot(2\hat{\mathbf r}\hat{\mathbf r}-\mathbf I)\cdot\mathbf p_i", "role": "encode polar, repulsive-turning and hydrodynamic alignment effects", "symbols": {"A,B,C": "measured interaction kernels", "r_hat": "pair direction"}, "evidence": "paper.pdf p. 4, Eq. (3)", "interpretation": "The vortex requires the competition of distinct interactions rather than alignment alone."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: confined-vortex experiments", "paper.pdf p. 4, Figure 3: experiment/theory/simulation profiles", "paper.pdf pp. 4–6, Eqs. (1)–(3): particle and continuum models", "paper.pdf pp. 6–7: scaling interpretation and limitations", "source PDF SHA-256 562177ec861e674455f4817445dd4fd03ed90b7cd25d51da508b025f56725f00", "Evidence status: full-text verified version of record; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-s41467-021-26202-1", "source_version": "version of record", "source_pdf": "https://www.nature.com/articles/s41467-021-26202-1.pdf",
        "title_en": "Learning non-stationary Langevin dynamics from stochastic observations of latent trajectories", "title_zh": "从潜在轨迹的随机观测中学习非平稳朗之万动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "numerical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["6190d5a20eefd8cc"], ["Mathematical Physics"]),
        "verified_metadata": {"doi": "10.1038/s41467-021-26202-1", "version": "version of record", "title": "Learning non-stationary Langevin dynamics from stochastic observations of latent trajectories", "authors": ["Mikhail Genkin", "Owen Hughes", "Tatiana A. Engel"], "journal": "Nature Communications", "volume": "12", "article": "5986", "published": "2021-10-13", "abstract": "A nonparametric likelihood framework jointly infers a latent Langevin potential, diffusion and non-equilibrium initial distribution from stochastic Poisson observations with trial termination.", "comment": "Open-access version of record"},
        "sections": [
            sec("作者信息", r"作者 Mikhail Genkin、Owen Hughes、Tatiana A. Engel；Nature Communications 12, 5986 (2021)，DOI:10.1038/s41467-021-26202-1，发表于 2021-10-13。核验 9 页开放期刊版及 Methods。论文提出统计推断方法，并在合成神经 spike-train 数据上验证。"),
            sec("研究问题", r"许多神经决策模型用低维 diffusion/Langevin 变量表示不可直接观测的证据积累，但实验只给出由潜变量随机产生的 spikes，trial 又可能在潜变量触及边界时结束。若错误假设稳态初始分布、反射边界或忽略终止选择，就会把非平稳采样偏差误认为势垒。论文问：能否从随机观测同时恢复势 Φ(x)、diffusion D 和非平衡初始分布 p0(x)？"),
            sec("背景", r"潜变量 x∈[-1,1] 满足 overdamped Langevin equation，力 F=−dΦ/dx；神经 spike counts 条件于 x 服从已知 Poisson observation model。传统 stationary density 只约束 Φ∝−log p_eq，无法处理每个 trial 从 p0 启动、有限时长以及吸收边界造成的选择偏差。", r"Figure 3 以 ground-truth 线性势为例：只有同时包含非平衡 p0、吸收边界和 absorption operator 的完整模型恢复直线；删去任一组成都会产生虚假 valley 或 barrier。"),
            sec("模型与方法", r"作者把路径联合似然分解为初始分布、相邻时间的 Fokker–Planck transition、每个时间 bin 的 Poisson emission、末次观测到终止时刻的传播，以及表示已观测终止条件的 absorption probability。通过前向—后向递推对所有潜在轨迹积分，而非先从 spikes 点估计 x。", r"Φ(x) 和 p0(x) 在空间网格上非参数化，D 同时优化；边界可设 absorbing/reflection 并与数据生成规则一致。模型选择不只最大化训练 likelihood，而比较不同 trial subsets 推断特征的一致性，用 Jensen–Shannon divergence 和 bootstrap 评估稳定性。"),
            sec("核心结果与证据", r"Figure 3 的 200 条合成 trials 表明：完整 non-stationary model 恢复线性 ground truth；忽略 absorption、改成 reflecting boundaries 或用 equilibrium p0 都会制造并不存在的双稳/单稳结构。这是论文最关键的 failure-control，因为它显示错误机制假设可造成定性错误。", r"在 ramping 与 stepping 两类决策动力学中，方法能联合恢复 Φ、p0 和 D。Figure 4 使用 200、1600 或 400 trials 展示数据量与不同 ground truth 下的恢复；更多 trials 缩小不确定性，但有限样本仍可能让细节漂移。", r"特征一致性准则在合成数据中帮助选择合适空间分辨率和模型复杂度。所有结果都来自已知 Poisson observation function 的 synthetic datasets；本文没有在真实神经记录上验证 recovered potential 的生物解释。"),
            sec("有效性与局限", r"方法当前是一维、Markov、白噪声、时间不变势与常数 D；跨 trial 的缓慢漂移、colored noise、多维决策变量和未知 observation function 不在验证范围。吸收边界和终止时刻必须被正确记录，否则 likelihood specification 仍会偏置。", r"非参数网格提高灵活性，也带来数据量、正则化和可识别性要求；Φ 的加法常数不可识别，p0、D 与势形在短 trial 中可能互相补偿。作者提出扩展到多维和多观测流，但这属于未来方向。合成恢复不能替代真实数据的 posterior predictive checks 与干预验证。"),
            sec("复现与资源", r"期刊：https://doi.org/10.1038/s41467-021-26202-1；开放全文：https://www.nature.com/articles/s41467-021-26202-1。核验 PDF SHA-256：e962dbb8436c3396b3e8180c31499a79fdcdaaf2f506d2d8ddbb8a1f53ea2e3e。复现需固定 x-grid、time bins、boundary/absorption rule、Poisson tuning curves、trial counts、optimizer、regularization、initialization、bootstrap 与 JS-divergence split。", r"最低复核应重现 Figure 3 的四种消融，并检查概率质量、终止率、势的 gauge convention 和参数恢复区间。Evidence status: full-text verified version of record and synthetic validation; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.1–3 的 Langevin/Poisson setup 和 non-stationarity 问题，再逐项读 p.4 Figure 3 的完整模型与三种错误设定。随后看 Figure 4 的样本量、ramping/stepping 恢复；Methods 中重点核查 joint likelihood、absorption operator、Fokker–Planck solver 与模型选择。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41467-021-26202-1/figure-3-nonstationary-components.webp", "label": "Figure 3", "visual_type": "ablation_comparison", "evidence": "paper.pdf p. 4, Figure 3", "alt_text": "完整非平稳模型与三种错误设定恢复潜在势的对比。", "caption": "忽略初态、吸收边界或终止机制会把选择偏差误判为虚假势垒。", "selection_rationale": "Figure 3 直接验证方法的必要组成，并展示错误建模造成的定性失败。"},
        "figure_refs": [figure("doi-10.1038-s41467-021-26202-1", "figure-3-nonstationary-components.webp", "Figure 3", 4, "ablate non-stationary likelihood components", "线性真势下完整模型和三种误设模型的恢复结果。", "只有完整处理 p0、吸收边界和终止选择才恢复 ground truth。", "The comparison uses synthetic Poisson observations with a known observation model.")],
        "equation_refs": [
            {"label": "Latent Langevin dynamics", "latex": r"\frac{dx}{dt}=D F(x)+\sqrt{2D}\,\xi(t),\qquad F(x)=-\frac{d\Phi}{dx}", "role": "define the latent stochastic trajectory", "symbols": {"Phi": "latent potential", "D": "diffusion coefficient", "xi": "unit white noise"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "Both deterministic drift and stochastic diffusion govern the hidden decision variable."},
            {"label": "Path-and-observation likelihood", "latex": r"P(X,Y)=p(x_{t_0})\prod_i p(y_{t_i}|x_{t_i})p(x_{t_i}|x_{t_{i-1}})\,p(x_{t_E}|x_{t_N})p(A|x_{t_E})", "role": "include emissions, latent propagation, initial state and trial absorption", "symbols": {"X": "latent path", "Y": "stochastic observations", "A": "absorption event"}, "evidence": "paper.pdf p. 3, Eq. (4)", "interpretation": "Omitting the final absorption factor changes which latent paths are represented in terminated trials."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: latent Langevin and non-stationary likelihood", "paper.pdf p. 4, Figure 3: component ablation", "paper.pdf pp. 4–6, Figure 4: simultaneous recovery and sample-size tests", "paper.pdf Methods: Fokker–Planck inference and model selection", "source PDF SHA-256 e962dbb8436c3396b3e8180c31499a79fdcdaaf2f506d2d8ddbb8a1f53ea2e3e", "Evidence status: full-text verified version of record and synthetic validation; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        visual_type_map = {
            "bifurcation_plot": "phase_diagram",
            "conceptual_diagram": "schematic",
            "experiment_phase_summary": "comparison",
            "experiment_theory_comparison": "comparison",
            "ablation_comparison": "comparison",
        }
        cover = card.get("cover")
        if isinstance(cover, dict):
            cover["visual_type"] = visual_type_map.get(
                str(cover.get("visual_type")), str(cover.get("visual_type"))
            )
        card_id = str(card["arxiv_id"]).replace("/", "-")
        (OUT / f"{card_id}.json").write_text(
            json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        installed.append(card_id)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
