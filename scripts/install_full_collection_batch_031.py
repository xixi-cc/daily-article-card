#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 031."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "doi-10.1038-s41467-026-73117-w", "source_version": "version of record",
        "source_pdf": "https://www.nature.com/articles/s41467-026-73117-w.pdf",
        "title_en": "Gauge-field-induced duality group in metamaterials", "title_zh": "规范场诱导的超材料对偶群",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["4348d7c4202f4a9e"], ["Condensed Matter"]),
        "verified_metadata": {"doi": "10.1038/s41467-026-73117-w", "version": "version of record", "title": "Gauge-field-induced duality group in metamaterials", "authors": ["Yan Meng", "Hong-yu Zou", "Naifu Zheng", "Linyun Yang", "Ruo-Yang Zhang", "Jingming Chen", "Xiang Xi", "Bei Yan", "Yong Ge", "Yi-jun Guan", "Hong-xiang Sun", "Gui-Geng Liu", "Zhenxiao Zhu", "Shou-qi Yuan", "Ce Shang", "Hongsheng Chen", "Qihang Liu", "Yihao Yang", "Zhen Gao"], "journal": "Nature Communications", "volume": "17", "article": "6520", "published": "2026-05-18", "abstract": "Artificial gauge fields enlarge pairwise duality into multi-element duality groups and enforce extended band degeneracies in acoustic metamaterials.", "comment": "Open-access version of record; no Crossref update relation found"},
        "sections": [
            sec("作者信息", r"作者 Yan Meng、Hong-yu Zou、Naifu Zheng 等；Nature Communications 17, 6520 (2026)，DOI:10.1038/s41467-026-73117-w，发表于 2026-05-18。核验9页开放期刊版、Methods、Data availability 与 Crossref 元数据；未发现关联更正或撤稿记录。"),
            sec("研究问题", r"通常的对偶性把两个看似不同的晶格或哈密顿量映射为同一谱，对应最简单的 Z2 结构。论文问：人工规范场能否把这种一对一关系扩展为多个不等价构型之间的有限对偶群，并让“自对偶”不只固定临界点，而是在整个 Brillouin zone 强制高重简并？"),
            sec("背景", r"作者把局域耦合的符号翻转写成 Z2 gauge transformations；在不改变 gauge flux 的条件下，不同符号构型可被 unitary operators 相互映射。二维方格的独立符号自由度产生 Z2×Z2 对偶群，三维立方格在去除全局冗余后形成六个生成元的 (Z2)^6。", r"自对偶构型还允许把对偶算符与时间反演、空间反演组合成 projective antiunitary symmetry。关键不是普通空间群给出的简并，而是 gauge-sector mapping 在整个动量空间对能带施加约束。"),
            sec("模型与方法", r"理论先枚举二维和三维最近邻 hopping signs，按 flux sector 与全局 sign flip 商掉冗余，再构造满足 UHU^{-1}=H' 的对偶算符。对 self-dual configuration，组合算符平方为负，从而得到 Kramers-like degeneracy；三维还用立方 Oh symmetry 分析 R 点的 double-Dirac structure。", r"实验以声学谐振器和连接管实现正负有效耦合；逐点声压扫描并 Fourier transform 得到投影 band structure。作者比较解析线、全波模拟色图和实测谱，同时改变若干连接但保持相同 gauge sector，检验多构型同谱。"),
            sec("核心结果与证据", r"Figure 2 在二维展示两个对偶样品和一个 self-dual π-flux 样品：对偶构型的测量能带相同，而自对偶构型在整个 BZ 呈两重简并。该结果是有限频率分辨率下的声学实现，不是对任意扰动均成立；保持相关 gauge symmetry 是前提。", r"Figure 4 把结论扩展到三维：两个不同构型给出相同投影谱；6π self-dual lattice 的四重能带贯穿整个三维 BZ，并在 R 点合并成八重 double Dirac point。正文通过三个正交切片的 iso-frequency cones 与测量/模拟吻合支持该识别。", r"数学上群的阶数与格点连接的独立 sign flips 有关；所谓“multi-to-multi”是同一 flux sector 内的等谱映射。它不表示所有不同超材料都等价，也不自动保护边界态；保护只覆盖由具体 projective symmetry 强制的 bulk degeneracy。"),
            sec("有效性与局限", r"声学系统是 tight-binding mapping 的经典波模拟；有效负 hopping、on-site frequency matching 和弱损耗近似需要校准。结构制造误差、远邻耦合、吸收和 transducer selectivity 会展宽或偏移谱线。实验展示代表性群元素而非穷举64个三维构型。", r"高重简并依赖 self-duality、时间反演/反演与指定 gauge flux；破坏这些条件可解除简并。论文证明给定模型中的群结构并用声学样品验证谱，不等同于电子材料中的费米能级、相互作用或输运观测。"),
            sec("复现与资源", r"期刊：https://doi.org/10.1038/s41467-026-73117-w。核验PDF SHA-256：4073f9f7d3ca08751231c9bb0027a00cffcbc677a4992503fc4ea9778f2909ba。复现需固定 resonator geometry、连接管截面/长度、正负耦合标定、boundary、source/receiver grid、Fourier window、损耗和本征频率偏移。", r"理论复现还需记录 sign convention、flux definition、生成元、商群冗余、momentum path 与 degeneracy tolerance。Evidence status: full-text verified version of record with acoustic experiment; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.2–3 Figure 1 与 Eqs. (1)–(4)，理解构型、flux 和 duality operator；再看 pp.3–4 Figure 2 的二维实验。核心三维结果看 pp.5–6 Figures 3–4，最后读 Discussion/Methods，把模型内严格群论、数值 band calculation 与有限分辨率实验分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41467-026-73117-w/figure-4-3d-duality.webp", "label": "Figure 4", "visual_type": "comparison", "evidence": "paper.pdf p. 6, Figure 4", "alt_text": "三种三维声学超材料及其测量、模拟能带和八重 double Dirac cone。", "caption": "三维对偶构型保持同谱；6π自对偶样品展示贯穿BZ的四重带与R点八重double Dirac简并。", "selection_rationale": "Figure 4 同时承载三维群映射、实验谱和最高重简并，是全文主结果。"},
        "figure_refs": [figure("doi-10.1038-s41467-026-73117-w", "figure-4-3d-duality.webp", "Figure 4", 6, "show the 3D duality and self-dual degeneracies", "三维样品、投影能带及R点锥面。", "对偶样品同谱，自对偶6π结构产生四重带和八重交叉。", "The degeneracies require the specified gauge and projective symmetries.")],
        "equation_refs": [
            {"label": "Duality transformation", "latex": r"\hat U\hat H_1(t,\mathbf k)\hat U^{-1}=\hat H_2(t',\mathbf k)", "role": "map inequivalent coupling configurations inside one gauge sector", "symbols": {"U": "duality operator", "t": "signed hopping configuration"}, "evidence": "paper.pdf p. 3, Eq. (4)", "interpretation": "Unitary equivalence enforces identical bulk spectra even when the real-space sign patterns differ."},
            {"label": "Kramers-like condition", "latex": r"\Theta_U^2=-1", "role": "enforce double degeneracy in a self-dual sector", "symbols": {"Theta_U": "antiunitary combination of duality and time reversal"}, "evidence": "paper.pdf pp. 3–4, self-duality discussion", "interpretation": "The degeneracy follows from the projective antiunitary representation, not ordinary spinful time reversal."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–3: 2D duality-group construction", "paper.pdf pp. 3–4, Figure 2: 2D acoustic validation", "paper.pdf pp. 4–6, Figures 3–4: 3D group and double-Dirac evidence", "source PDF SHA-256 4073f9f7d3ca08751231c9bb0027a00cffcbc677a4992503fc4ea9778f2909ba", "Evidence status: full-text verified version of record; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-s41567-018-0081-4", "source_version": "arXiv v2",
        "source_pdf": "https://arxiv.org/pdf/1704.06279v2", "title_en": "Mutual information, neural networks and the renormalization group", "title_zh": "互信息、神经网络与重整化群",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["511d970684a27575"], ["Renormalization Group"]),
        "verified_metadata": {"doi": "10.1038/s41567-018-0081-4", "arxiv_id": "1704.06279", "version": "v2", "title": "Mutual information, neural networks and the renormalization group", "authors": ["Maciej Koch-Janusz", "Zohar Ringel"], "journal": "Nature Physics", "volume": "14", "pages": "578–582", "published": "2018-03-26", "abstract": "A neural estimator maximizes real-space mutual information to identify coarse variables and build real-space RG transformations.", "comment": "arXiv v2 full text cross-checked against version-of-record metadata; no Crossref update relation found"},
        "sections": [
            sec("作者信息", r"作者 Maciej Koch-Janusz、Zohar Ringel；Nature Physics 14, 578–582 (2018)，DOI:10.1038/s41567-018-0081-4；全文取 arXiv:1704.06279v2，共18页并含补充材料。核验 Crossref 元数据；未发现关联更正或撤稿记录。"),
            sec("研究问题", r"实空间RG需要选择少数 coarse variables，保留长程物理同时丢掉局域噪声；传统选择依赖人为洞察。论文问：能否把“相关自由度”定义为局域块 V 与远处环境 E 之间互信息最大的隐变量 H，并用神经网络从 Monte Carlo 样本自动学习 coarse-graining map？"),
            sec("背景", r"在缓冲区 B 隔开 V 与 E 后，短程相关被屏蔽；最大化 I(H:E) 倾向保留对长距离行为有预测力的成分。RSMI network 以 restricted Boltzmann machine 表示 PΛ(H|V)，另两个 RBM 近似 P(V,E) 与 P(V)，从而估计互信息并对Λ求梯度。", r"Figure 1 是方法关键：H只直接连接V，但优化目标来自H与远处E的信息；缓冲区避免网络靠复制最近邻噪声获得高分。训练后的H再作为下一RG层的visible variables，重复迭代形成flow。"),
            sec("模型与方法", r"作者在二维 Ising 与 fully packed dimer 两个经典模型上用 Monte Carlo 配置训练。Ising 以2×2 block和不同hidden-unit数测试；dimer中真实长程自由度与height/electric fields有关，局域dimer本身含大量无关涨落。", r"互信息本身通过变分/对比散度近似，优化不是解析精确最大值。RG后的分布由训练RBM采样，逐层比较权重图、关联函数和temperature flow；critical exponent由临界点附近相关长度/热方向的线性化得到。"),
            sec("核心结果与证据", r"Figure 2 显示 Ising 的一个hidden unit学习到四自旋多数规则；四个hidden units则分别跟踪局域自旋，说明容量约束会影响“相关”表示。迭代后得到有序/无序流与中间不稳定临界点，并提取与二维Ising一致的thermal critical exponent。", r"dimer模型的RSMI filters学习到水平/垂直electric-field combinations，而普通contrastive-divergence RBM更容易重构局部细节。Figure 4/5表明这些filters与已知height-field coarse variables相符，支持互信息准则能滤除短程冗余。", r"这些是两个可控平衡模型上的数值验证。算法没有证明对任意量子场论、连续自由度或无尺度分离系统都能找到唯一RG；同一互信息上限可能对应等价编码，network capacity与buffer size决定可辨识内容。"),
            sec("有效性与局限", r"互信息估计和RBM训练存在Monte Carlo误差、mixing与局部最优；临界附近长相关使采样更难。有限block、环境和system size限制渐近指数精度，补充材料中的网络超参数与restart是结果组成部分。", r"最大化长程信息只在采用的locality、buffer和bottleneck约束下对应合适RG。若有多个慢变量、拓扑信息或非局域约束，hidden dimension不足会丢信息，过大又可复制局域细节。所谓自动发现仍需要选择分块、体系、温度扫描和可用网络族。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/1704.06279；期刊：https://doi.org/10.1038/s41567-018-0081-4。核验PDF SHA-256：2400bace9b755c9d209394a152d4c6687b41eec624ea1120d66fafebd5c13949。复现需固定lattice size、boundary、MC sampler、temperature grid、V/B/E geometry、Nh、RBM width、CD steps、learning rate、epochs与random seeds。", r"指数复现还需公开RG iteration、temperature reparameterization、linear-fit window和error bars。Evidence status: full-text verified arXiv v2 plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.2–3 Figure 1 与 Eq. (1)，明确RSMI目标；再看 p.3 Figure 2 的Ising majority-rule恢复。随后读 pp.3–4 dimer filters 与RG flow，最后看补充材料的互信息proxy、网络训练和critical exponent提取，避免把近似优化写成RG定理。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41567-018-0081-4/figure-1-rsmi.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "局域块V、缓冲区B、远处环境E和隐变量H，以及RSMI训练流程。", "caption": "RSMI以H和远处环境E的互信息为目标，使局域coarse variable保留长程相关而非短程噪声。", "selection_rationale": "Figure 1 完整解释信息论目标、空间分区和神经网络实现。"},
        "figure_refs": [figure("doi-10.1038-s41567-018-0081-4", "figure-1-rsmi.webp", "Figure 1", 2, "explain the RSMI coarse-graining objective", "V、B、E、H及三个RBM的训练关系。", "通过缓冲区隔离局域涨落并最大化H与E的互信息。", "The objective is estimated variationally and depends on the chosen bottleneck and geometry.")],
        "equation_refs": [
            {"label": "Real-space mutual information", "latex": r"I_\Lambda(H:E)=\sum_{H,E}P_\Lambda(E,H)\log\frac{P_\Lambda(E,H)}{P_\Lambda(H)P(E)}", "role": "select coarse variables that retain distant information", "symbols": {"H": "coarse variable", "E": "distant environment", "Lambda": "neural coarse-graining parameters"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "The bottleneck favors long-distance relevance once the buffer removes direct short-range correlations."},
            {"label": "Ising Hamiltonian", "latex": r"H_I=\sum_{\langle i,j\rangle}s_i s_j", "role": "define the benchmark whose block spin and flow are known", "symbols": {"s_i": "binary lattice spin"}, "evidence": "paper.pdf p. 3, Eq. (3)", "interpretation": "The learned majority-like filter is checked against a model with established real-space RG structure."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–3: RSMI objective and architecture", "paper.pdf pp. 3–4: Ising and dimer filters", "paper.pdf pp. 9–18: mutual-information estimator and RG validation", "source PDF SHA-256 2400bace9b755c9d209394a152d4c6687b41eec624ea1120d66fafebd5c13949", "Evidence status: full-text verified arXiv v2; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-s41567-021-01442-6", "source_version": "accepted manuscript",
        "source_pdf": "https://www.osti.gov/servlets/purl/1868355", "title_en": "Polar state reversal in active fluids", "title_zh": "活性流体中的极性态反转",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["18c4ab021b9922e3"], ["Fluid Dynamics"]),
        "verified_metadata": {"doi": "10.1038/s41567-021-01442-6", "version": "accepted manuscript", "title": "Polar state reversal in active fluids", "authors": ["Bo Zhang", "Hang Yuan", "Andrey Sokolov", "Monica Olvera de la Cruz", "Alexey Snezhko"], "journal": "Nature Physics", "volume": "18", "pages": "154–159", "published": "2021-12-23", "abstract": "Temporarily switching off activity makes a confined Quincke-roller vortex reverse its chirality through positional memory and hydrodynamic interactions.", "comment": "OSTI accepted manuscript cross-checked against version-of-record metadata; no Crossref update relation found"},
        "sections": [
            sec("作者信息", r"作者 Bo Zhang、Hang Yuan、Andrey Sokolov、Monica Olvera de la Cruz、Alexey Snezhko；Nature Physics 18, 154–159 (2022)，DOI:10.1038/s41567-021-01442-6，在线发表于2021-12-23。全文取OSTI合法accepted manuscript，共10页。"),
            sec("研究问题", r"圆形约束中的Quincke rollers自组织为顺时针或逆时针极性涡旋，两个手性态在静态驱动下等价。论文问：短暂关闭再开启活性能否可靠翻转全局极性，而不是随机重选；若能，断电期间保留下来的何种位置非对称性为重新启动提供方向记忆？"),
            sec("背景", r"实验将绝缘液体中的微米球置于圆形well并施加直流电场。通电时Quincke rotation驱动粒子滚动并通过长程electrohydrodynamic interactions形成单涡旋；断电后速度很快消失，但粒子扩散与静电松弛具有不同时间尺度。", r"Figure 1 将protocol、240次循环的手性时间序列和尺寸/面积分数依赖放在一起。在合适τoff下，每次重新通电都选择与上一周期相反的旋转方向，说明不是独立50/50抽样。"),
            sec("模型与方法", r"作者以高速显微镜和粒子跟踪测量角速度、密度与径向/方位位置分布，定义P=Nr/Nt统计反转概率。扫描well直径D、面积分数ϕ、τoff与τon，并比较场方向反转等controls。", r"数值模型含短程排斥、dipolar electrostatic interaction、远程hydrodynamic interaction和边界。通过分别关闭各相互作用，检验重新启动时rolls的径向排列不对称如何转化为定向azimuthal flow。"),
            sec("核心结果与证据", r"Figure 1 报告ϕ≈0.08时连续240个activity cycles均反转；在较宽的D与ϕ区间P接近1，而太小体系或粒子过稀时涡旋形成/反转不稳。时间窗要求τoff足以抹掉速度方向、又不能长到位置结构完全扩散。", r"Figure 2 显示重新加场后，靠近边界与中心的粒子速度响应不同，原涡旋留下的radial density/positional asymmetry先诱发与原方向相反的局部流，随后并合成全局反向涡旋。Figure 3以非对称量An量化这种记忆并显示其随断电衰减。", r"Figure 4的ablation simulations表明只含排斥或静电相互作用不足以给出稳健反转；加入hydrodynamic interactions可重现反转趋势。该结论支持模型中的必要作用，但未直接测量每对粒子的流体核，也不证明所有实验参数下机制唯一。"),
            sec("有效性与局限", r"确定性反转依赖圆形约束、Quincke roller特定时间尺度、面积分数和pulse window；外推到细菌、细胞或无边界active fluids需要重新验证。240次记录证明该条件下稳健，不等于无限周期或所有sample的概率保证。", r"粒子模型使用近似的pair interactions和二维边界，忽略部分多体/三维电流体效应。interaction ablation会同时改变稳态结构，因而是机制支持而非严格因果分解。Accepted manuscript的排版页码与正式版可能不同，本卡页级引用以该全文为准。"),
            sec("复现与资源", r"期刊：https://doi.org/10.1038/s41567-021-01442-6；accepted manuscript：https://www.osti.gov/servlets/purl/1868355。核验PDF SHA-256：f610543f61e97a8c1c1bbe2f8adf2fc502f02430b1bb40fc98ddda0492b57a58。复现需固定粒径、fluid conductivity、gap、field amplitude、D、ϕ、τon/τoff、camera rate、tracking与chirality threshold。", r"模拟需固定interaction kernels、boundary、time step、initial ensemble与ablation protocol。Evidence status: full-text verified accepted manuscript plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先看 pp.1–2 Figure 1 的protocol和240-cycle证据；再读 p.3 Figure 2 的反转时间序列与p.4 Figure 3的位置记忆。最后看 pp.4–5 Figure 4的interaction controls，并把观察到的高P、模型ablation和一般机制主张分层理解。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41567-021-01442-6/figure-1-vortex-reversal.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "脉冲电场诱导Quincke roller涡旋反转的装置、速度图、240周期轨迹和概率曲线。", "caption": "短暂关闭再开启活性后，受限roller涡旋在适当参数区稳定选择相反手性。", "selection_rationale": "Figure 1 同时给出protocol、代表场和统计稳健性，是主结论的最完整证据。"},
        "figure_refs": [figure("doi-10.1038-s41567-021-01442-6", "figure-1-vortex-reversal.webp", "Figure 1", 2, "show robust pulse-induced chirality reversal", "实验装置、速度场、连续循环与P(D,phi)。", "特定pulse window内上一周期的手性被可靠翻转。", "Robustness is parameter- and confinement-specific, not universal active-fluid control.")],
        "equation_refs": [
            {"label": "Reversal probability", "latex": r"P=N_r/N_t", "role": "quantify cycle-to-cycle chirality reversal", "symbols": {"N_r": "number of observed reversals", "N_t": "number of activity cycles"}, "evidence": "paper.pdf p. 2, Figure 1 caption", "interpretation": "P separates deterministic reversal from random re-selection across repeated cycles."},
            {"label": "Polar alignment measure", "latex": r"\mathbf P=N^{-1}\sum_i \mathbf v_i/|\mathbf v_i|", "role": "track collective orientation during reactivation", "symbols": {"v_i": "tracked roller velocity"}, "evidence": "paper.pdf pp. 2–3, analysis definitions", "interpretation": "The sign of azimuthal collective motion identifies the vortex chirality after startup."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2, Figure 1: protocol and reversal statistics", "paper.pdf p. 3, Figure 2: startup dynamics", "paper.pdf pp. 3–4, Figure 3: positional memory", "paper.pdf pp. 4–5, Figure 4: interaction ablations", "source PDF SHA-256 f610543f61e97a8c1c1bbe2f8adf2fc502f02430b1bb40fc98ddda0492b57a58", "Evidence status: full-text verified accepted manuscript; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-s41567-023-02301-2", "source_version": "arXiv v1",
        "source_pdf": "https://arxiv.org/pdf/2305.06078", "title_en": "Active hydraulics laws from frustration principles", "title_zh": "由阻挫原理导出的主动水力学定律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["210d221340cda74a"], ["Active Matter"]),
        "verified_metadata": {"doi": "10.1038/s41567-023-02301-2", "arxiv_id": "2305.06078", "version": "v1", "title": "Active hydraulics laws from frustration principles", "authors": ["Camille Jorge", "Amélie Chardac", "Alexis Poncet", "Denis Bartolo"], "journal": "Nature Physics", "volume": "20", "pages": "303–311", "published": "2024-01-09", "abstract": "Colloidal rollers in trivalent microfluidic networks realize frustrated active flows described by spin-ice and loop-model mappings.", "comment": "arXiv full text cross-checked against version-of-record metadata; no Crossref update relation found"},
        "sections": [
            sec("作者信息", r"作者 Camille Jorge、Amélie Chardac、Alexis Poncet、Denis Bartolo；Nature Physics 20, 303–311 (2024)，DOI:10.1038/s41567-023-02301-2；全文取arXiv:2305.06078，共29页含补充材料。"),
            sec("研究问题", r"被动水力网络中给定边界压差通常唯一决定流量。主动流体却能在没有外加压差时自发选择通道方向。论文问：奇数配位节点的质量守恒与局域极性是否必然阻挫，从而产生多重稳定streamline patterns；能否用spin ice与loop models给出可预测的“active hydraulics laws”？"),
            sec("背景", r"实验用Quincke rollers填充蜂窝状微流道网络。每条窄通道内滚子形成近单向polar flow，可用边spin σ=±1表示；三价节点不可能让三条等幅流同时满足零净流量，因此必须有two-in/one-out或反之的ice rule。", r"Figure 1 从宏观蜂窝网络、局域涡旋、通道流到spin mapping逐层连接实验与模型。重复相同protocol得到不同但都满足局域规则的图样，故“非确定性”指微观streamline realization退化，不是质量守恒失效。"),
            sec("模型与方法", r"作者改变channel aspect ratio，使用PIV/粒子轨迹识别edge current与node circulation，并把streamlines转为topographic height/loop representation。相同网络重复多次，比较nesting height、current correlations与defect statistics。", r"理论以spin-1 node variables和edge Ising spins建立frustrated Blume–Capel-like model；在maximal-flow limit映射为fully packed loops，并区分短loop与嵌套system-spanning loop两类。对loop O(n)模型的精确结果只在对应极限与统计权重假设下成立。"),
            sec("核心结果与证据", r"Figure 2显示同一装置、同一控制参数的两次实验形成不同streamline topology，同时edge-current statistics相近，直接展示degeneracy。局域threefold nodes几乎总遵循two-in/one-out或one-in/two-out，支持spin-ice constraint。", r"Figure 3随aspect ratio出现两类自相似loop morphology：一类由许多短、弱嵌套loops组成，另一类具有深度嵌套的大loops；topographic height差在转变附近跃升。粒子模拟复现几何趋势，但转变位置和有限尺寸依赖模型。", r"Figure 4及补充推导把邻接streamline的parallel-flow preference与fractionalized topological defects联系起来。spin/loop模型能预测loop fractal dimensions与几何统计；“exact”限定在映射后的平衡loop model，不表示耗散active experiment具有平衡Boltzmann分布或所有时间动力学被精确求解。"),
            sec("有效性与局限", r"实验对象是特定Quincke-roller网络、固定三价几何和近饱和通道流；节点附近三维电流体作用被有效化。edge spin丢掉速度幅值、横向涡结构和时间波动；不同实验realizations也未遍历全部退化态。", r"double-spin Hamiltonian是最小统计模型，couplings由现象学匹配而非独立测量。平衡spin/loop universality可解释几何，不自动给出active switching rates、entropy production或响应。对偶数配位、非规则网络、开放边界和弱极性通道需重新推导。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2305.06078；期刊：https://doi.org/10.1038/s41567-023-02301-2。核验PDF SHA-256：269bbf613db562a710d17ff4eb869350859bf8495dbc446bb9abcd0a331b4814。复现需固定channel width/depth/aspect ratio、field、roller density、network size/boundary、PIV、edge-current threshold与realization count。", r"理论需固定spin convention、couplings、maximal-flow limit、loop tracing、finite-size estimator和defect definition。Evidence status: full-text verified arXiv manuscript plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先看 pp.1–2 Figure 1 建立edge spin与三价阻挫；p.3 Figure 2验证退化。再读 pp.4–5 Figure 3 的loop polymorphism和pp.5–6 Figure 4的相互作用/缺陷；最后用补充材料核查spin与O(n)映射，并严格保留其成立条件。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41567-023-02301-2/figure-1-active-hydraulics.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "蜂窝微流道中的roller流、节点涡旋、edge currents与spin-ice映射。", "caption": "三价节点无法同时容纳三条等幅polar flow，质量守恒迫使局域ice rule并产生全局阻挫。", "selection_rationale": "Figure 1 最完整地连接装置、流线、守恒约束和spin语言。"},
        "figure_refs": [figure("doi-10.1038-s41567-023-02301-2", "figure-1-active-hydraulics.webp", "Figure 1", 2, "connect active microfluidics to a frustrated spin representation", "蜂窝网络、局域涡旋、edge currents和two-in/one-out规则。", "奇数配位使极性流与质量守恒不能同时无挫满足。", "The mapping retains flow directions but coarse-grains amplitudes and dissipative dynamics.")],
        "equation_refs": [
            {"label": "Passive hydraulic law", "latex": r"\Phi_{ij}=-K_{ij}(P_i-P_j)", "role": "contrast deterministic passive flow with active edge currents", "symbols": {"Phi_ij": "mass flux", "K_ij": "hydraulic conductance", "P_i": "node pressure"}, "evidence": "paper.pdf p. 1, introduction", "interpretation": "Active flows need not be uniquely fixed by imposed node pressures because channels spontaneously choose polarity."},
            {"label": "Trivalent ice rule", "latex": r"\sum_{e\in\partial i}\sigma_e=\pm1", "role": "encode the minimally frustrated current balance at a threefold node", "symbols": {"sigma_e": "oriented edge current", "partial_i": "three incident edges"}, "evidence": "paper.pdf pp. 2–3, Figure 1g and text", "interpretation": "Odd coordination prevents a zero sum for equal-magnitude binary currents and leaves a degenerate set of allowed vertices."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2, Figure 1: experiment and ice-rule mapping", "paper.pdf p. 3, Figure 2: repeated-realization degeneracy", "paper.pdf pp. 4–6, Figures 3–4: loop classes and defects", "paper.pdf pp. 14–29: spin and loop-model derivations", "source PDF SHA-256 269bbf613db562a710d17ff4eb869350859bf8495dbc446bb9abcd0a331b4814", "Evidence status: full-text verified arXiv manuscript; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1038-s41567-025-02957-y", "source_version": "arXiv v1",
        "source_pdf": "https://arxiv.org/pdf/2608.03560", "title_en": "Control of collective activity to crystallize an oscillator gas", "title_zh": "控制集体活性以结晶振子气体",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["e0a58066cf5e1151"], ["Complex Systems"]),
        "verified_metadata": {"doi": "10.1038/s41567-025-02957-y", "arxiv_id": "2608.03560", "version": "v1", "title": "Control of collective activity to crystallize an oscillator gas", "authors": ["Marine Le Blay", "Joshua H. K. Saldi", "Alexandre Morin"], "journal": "Nature Physics", "volume": "21", "pages": "1412–1419", "published": "2025-08-04", "abstract": "Contact-charge electrophoretic oscillators acquire collective in-plane activity through super-elastic collisions and can be reversibly crystallized by modulating the drive.", "comment": "arXiv v1 full text posted after publication and cross-checked against version-of-record metadata; no Crossref update relation found"},
        "sections": [
            sec("作者信息", r"作者 Marine Le Blay、Joshua H. K. Saldi、Alexandre Morin；Nature Physics 21, 1412–1419 (2025)，DOI:10.1038/s41567-025-02957-y，在线发表于2025-08-04。全文取arXiv:2608.03560v1，共33页含Methods/补充内容。"),
            sec("研究问题", r"单个contact-charge electrophoretic particle只在上下电极间自持振荡，平均没有平面推进。论文问：高密度下碰撞能否把这种内部振荡转化为集体平面active gas；若activity随碰撞率和密度正反馈，能否通过调制外场频率降低碰撞增益并可逆地把气体结晶？"),
            sec("背景", r"毫米级conducting spheres在两个电极间由接触充放电往返；孤立振子沿垂直方向周期运动。密集时，不同相位粒子发生倾斜碰撞，把垂直动量转成平面运动。不同于通常activity抑制相分离的负耦合，这里collision rate随密度增加，super-elastic events又向平面自由度注能。", r"Figure 1 展示从单振子到active gas的跃迁；Figure 2把平面动能、碰撞前后速度和耗散标度关联起来，建立正density–activity coupling的实验基础。"),
            sec("模型与方法", r"作者用双相机stereo reconstruction恢复三维轨迹，测量oscillation frequency、kinetic energy、pair distribution、collision in/out velocities和collision rate。有限元计算给出两个带电振子在不同相位/间距下的电相互作用，最小two-body oscillator model描述同步依赖碰撞。", r"控制阶段保持峰值场幅并改变square-wave modulation frequency ωE。频率改变有效phase locking与碰撞restitution；以orientational order ψ6、pair correlation、collision rate与maximum displacement δ评价fluid–crystal transition和可逆切换。"),
            sec("核心结果与证据", r"Figure 2显示群体平面动能随粒子数/密度增长；联合分布P(vin,vout)中大量事件满足vout>vin，即有效super-elastic collision。能量注入与oscillator frequency的标度和碰撞率共同解释active gas，而不是单粒子自推进。", r"Figure 3的有限元与two-body model把collision outcome关联到相位同步和距离依赖耦合。该模型说明一种可行微观机制，但参数化、墙面接触与多体碰撞意味着它不是完整第一性原理动力学。", r"Figure 4中直流驱动给无序gas；提高ωE后先形成更有序fluid，超过约25.1 rad s−1后出现六角crystal。ψ6在临界附近急升，collision rate下降至近零，maximum displacement减小；交替13与57 rad s−1可重复熔化/结晶。数值two-body threshold约20.5 rad s−1与集体实验同量级，不是精确相变预测。"),
            sec("有效性与局限", r"体系是有限二维cell中的毫米级接触充电振子；gravity、electrode roughness、humidity、charge leakage和边界会影响动力学。晶体由外场调制抑制碰撞activity而形成，不能直接等同于热平衡结晶；ψ6与g(r)显示结构序，但有限系统未给出热力学极限或universality class。", r"positive density–activity coupling是由碰撞统计、能量balance和模型共同支持的解释，未排除所有长程电场/边界机制。所谓super-elastic是平面动能在碰撞后增加，能量来自持续电驱动，并不违反总能量守恒。原始数据规模很大，部分需向作者请求。"),
            sec("复现与资源", r"期刊：https://doi.org/10.1038/s41567-025-02957-y；Source Data：https://doi.org/10.6084/m9.figshare.28661015。核验PDF SHA-256：1e805898f8ab11ea6491adc75cc1af04adcae85f4c9f9af27e258e484ffdc121。复现需固定sphere/electrode materials、gap、humidity、E、ωE、density、camera calibration、stereo matching、collision definition和finite-cell geometry。", r"模型需固定charge law、contact restitution、phase coupling、integration step与initial phases。Evidence status: full-text verified arXiv v1 plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先看 pp.2–4 Figure 1理解单体振荡如何变成集体gas；再看 pp.4–5 Figure 2核查super-elastic statistics。p.6 Figure 3给机制模型，核心控制证据在 pp.7–9 Figure 4。阅读时将结构转变、非平衡能量来源和two-body解释分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1038-s41567-025-02957-y/figure-4-crystallization-control.webp", "label": "Figure 4", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 9, Figure 4", "alt_text": "不同调制频率下振子气体、流体与晶体图像及有序度、碰撞率和可逆切换。", "caption": "提高外场调制频率抑制碰撞活性，使active gas经有序fluid进入晶体，并可通过频率切换反复熔化。", "selection_rationale": "Figure 4 直接呈现题目所称的activity control、结构转变和可逆性。"},
        "figure_refs": [figure("doi-10.1038-s41567-025-02957-y", "figure-4-crystallization-control.webp", "Figure 4", 9, "show control of activity and reversible crystallization", "驱动信号、实空间结构、ψ6、碰撞率、位移和切换轨迹。", "调制频率提高时碰撞率下降且六角序形成。", "The finite driven transition is not identified as an equilibrium thermodynamic phase transition.")],
        "equation_refs": [
            {"label": "Driven oscillator phase", "latex": r"\ddot\theta_i+\omega_0\dot\theta_i=\sum_j K_{ij}\sin(\theta_j-\theta_i)", "role": "model synchronization-dependent interactions", "symbols": {"theta_i": "oscillator phase", "K_ij": "distance-dependent coupling", "omega_0": "single-particle oscillation scale"}, "evidence": "paper.pdf p. 6, Eqs. (1)–(2), schematic form", "interpretation": "Drive modulation changes phase relations and therefore the collision channel available to nearby oscillators."},
            {"label": "Orientational order", "latex": r"\psi_6=\left|N^{-1}\sum_j e^{6i\theta_j}\right|", "role": "quantify sixfold crystalline order", "symbols": {"theta_j": "bond-orientation angle"}, "evidence": "paper.pdf p. 9, Figure 4c and Methods", "interpretation": "The sharp rise of sixfold order operationally locates the finite-system fluid-to-crystal crossover."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4, Figure 1: single oscillators and active gas", "paper.pdf pp. 4–5, Figure 2: collision energetics", "paper.pdf p. 6, Figure 3: synchronization-dependent interaction model", "paper.pdf pp. 7–9, Figure 4: controlled reversible crystallization", "source PDF SHA-256 1e805898f8ab11ea6491adc75cc1af04adcae85f4c9f9af27e258e484ffdc121", "Evidence status: full-text verified arXiv v1; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        card_id = str(card["arxiv_id"]).replace("/", "-")
        (OUT / f"{card_id}.json").write_text(
            json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        installed.append(card_id)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
