#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 008."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_id: str, topic: str) -> dict[str, object]:
    return {
        "program": "Collection", "catalog": "Paper Collection",
        "catalog_record_id": record_id, "catalog_record_ids": [record_id],
        "catalog_topic": topic, "collection_date": "2026-08-23",
        "sampled_at": "2026-08-27", "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection", "candidate_count": 452,
    }


def meta(arxiv_id: str, version: str, title: str, authors: list[str], categories: list[str],
         primary: str, published: str, abstract: str) -> dict[str, object]:
    return {"arxiv_id": arxiv_id, "version": version, "title": title, "authors": authors,
            "categories": categories, "primary_category": primary, "published": published,
            "abstract": abstract, "comment": ""}


def figure(arxiv_id: str, filename: str, label: str, page: int, role: str,
           alt: str, caption: str, interpretation: str) -> dict[str, object]:
    return {"label": label, "asset_path": f"assets/collection-figures/{arxiv_id}/{filename}",
            "section": "核心结果与证据", "role": role,
            "evidence": f"paper.pdf p. {page}, {label}", "alt_text": alt,
            "caption": caption, "interpretation": interpretation}


CARDS = [
    {
        "arxiv_id": "2304.02637", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2304.02637",
        "title_en": "GenPhys: From Physical Processes to Generative Models", "title_zh": "GenPhys：从物理过程到生成模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("cb87befa0c182aa1", "Generative Models"),
        "verified_metadata": meta("2304.02637", "v1", "GenPhys: From Physical Processes to Generative Models", ["Ziming Liu", "Di Luo", "Yilun Xu", "Tommi Jaakkola", "Max Tegmark"], ["cs.LG", "cs.AI", "physics.comp-ph", "physics.data-an", "quant-ph"], "cs.LG", "2023-04-05T17:58:16Z", "A framework maps physical PDEs to generative density flows and identifies a dispersion-relation criterion for smoothing processes."),
        "sections": [
            sec("作者信息", r"作者：Ziming Liu、Di Luo、Yilun Xu、Tommi Jaakkola、Max Tegmark；arXiv:2304.02637v1。全文 22 页。"),
            sec("研究问题", r"扩散模型和 Poisson flow 都来自物理演化。论文问：一个偏微分方程何时能把任意数据密度连续输运到简单先验，并可逆地生成样本？目标不是再为某个模型寻找类比，而是给物理过程到生成模型的映射规定可检验条件。"),
            sec("背景", r"生成模型可写成概率密度的连续流：守恒情形满足连续性方程；有源汇时再加入 birth/death 项。只要物理场给出的密度演化足够光滑，而且长时间极限遗忘初态的非零 Fourier 模式，就可能从简单先验反演回数据。", r"物理语言中，这要求耗散抑制短波涨落，同时保留零模归一化。纯振荡动力学只搬运相位而不抹去结构，因此理想波动和 Schrödinger 演化默认不属于这一类。"),
            sec("模型与方法", r"作者提出 s-generative 两个条件：物理 PDE 能等价改写为良态 density flow；其解随时间平滑到与数据无关的先验。对常系数线性 PDE，代入平面波 \(\phi\propto e^{-i\omega t+i k\cdot x}\)，把是否平滑化化为色散关系虚部的比较。", r"扩散方程给出 \(\omega=-i k^2\)，Poisson 分支给出随 \(k\) 衰减的虚频，因此可用；理想波和 Schrödinger 方程的 \(\omega\) 为实数，不能自动抹去非零模。Helmholtz/Yukawa 型过程则提供新的候选族。"),
            sec("核心结果与证据", r"Figure 1 把 diffusion、electrostatics、wave、Helmholtz、Yukawa 与 Schrödinger/Dirac 过程排在同一“物理—生成”对应图中；已解锁的只有 diffusion 与 Poisson，图中锁标记的是待检验而非已经训练成功的新模型。", r"线性判据为所有 \(k>0\) 满足 \(\operatorname{Im}\omega(k)<\operatorname{Im}\omega(0)\)：非零空间频率比零模衰减得更快。若多分支色散中至少一支满足条件，就可构造相应的平滑流。", r"论文由该判据回收 diffusion/PFGM，并指出 screened-Poisson/Yukawa 家族可行；它提供的是结构性设计空间，没有训练新模型或报告 FID，因此不能把“可构造”写成经验性能改进。"),
            sec("有效性与局限", r"严格推导集中在线性、常系数 PDE 与自由边界条件；非线性、多场耦合、有限域边界和奇异解可能破坏 Fourier 模式判据或 density-flow 的良定性。", r"渐近平滑只保证先验化方向，不保证有限时间可采样、逆问题数值稳定或神经网络 score/velocity 易学。Yukawa generative model 在本文是理论候选，尚无相同预算的生成质量、速度或稳定性实验。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2304.02637。全文 22 页，PDF SHA-256：e41ca586c62bd67f58e0d090114344bac8870ebe6eb5b8e8214ea3b518fe7dae。", r"复核新 PDE 时应先写明场、边界条件、守恒/源汇项与色散分支，再验证 density 非负、归一化、长时先验和反向数值稳定性。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 确认论文在定义一张候选地图；再读 Eq. (2) 的连续性方程和 Eq. (16) 的色散判据。最后逐个检查 diffusion、wave、Schrödinger 与 Yukawa 的 \(\omega(k)\)，把“物理类比”与“满足生成条件”分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2304.02637/figure-1-physics-duality.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "从多种物理过程到已解锁和待解锁生成模型的对应图。", "caption": "GenPhys 把生成模型设计写成对物理 PDE 的筛选：只有能平滑非零模式并形成良态密度流的过程才可解锁。", "selection_rationale": "该图是论文最重要的概念可视化，直接呈现已建立与仍是假设的物理—生成对应关系。"},
        "figure_refs": [figure("2304.02637", "figure-1-physics-duality.webp", "Figure 1", 1, "map physical processes to generative-model candidates", "物理过程与生成模型之间的对应关系及锁定状态。", "图中的锁表示待验证设计空间，不表示已达到经验性能。", "The figure organizes hypotheses; the dispersion criterion decides which links are admissible.")],
        "equation_refs": [
            {"label": "Density-flow continuity equation", "latex": r"\partial_t p(x,t)+\nabla\!\cdot\!\left[p(x,t)v(x,t)\right]=0", "role": "express a conservative physical evolution as probability transport", "symbols": {"p": "probability density", "v": "density velocity field", "t": "flow time"}, "evidence": "paper.pdf p. 3, Eq. (2)", "interpretation": "A physical PDE must induce a well-defined transport of normalized probability."},
            {"label": "s-generative dispersion criterion", "latex": r"\operatorname{Im}\omega(k)<\operatorname{Im}\omega(0)\quad\text{for all }k>0", "role": "test whether nonzero spatial modes decay relative to the zero mode", "symbols": {"omega": "complex dispersion relation", "k": "spatial wavenumber"}, "evidence": "paper.pdf p. 8, Eq. (16)", "interpretation": "Relative damping of every nonzero Fourier mode makes the terminal density independent of data details."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: density-flow construction", "paper.pdf pp. 6–9: smoothing and dispersion criterion", "source PDF SHA-256 e41ca586c62bd67f58e0d090114344bac8870ebe6eb5b8e8214ea3b518fe7dae", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2304.09355", "source_version": "v5", "source_pdf": "https://arxiv.org/pdf/2304.09355",
        "title_en": "To Compress or Not to Compress- Self-Supervised Learning and Information Theory: A Review", "title_zh": "压缩还是不压缩：自监督学习与信息论综述",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("dcd7f7faced75f74", "Information Theory"),
        "verified_metadata": meta("2304.09355", "v5", "To Compress or Not to Compress- Self-Supervised Learning and Information Theory: A Review", ["Ravid Shwartz-Ziv", "Yann LeCun"], ["cs.LG", "cs.IT"], "cs.LG", "2023-04-19T00:33:59Z", "A review unifies information-bottleneck, multiview, contrastive, and noncontrastive views of self-supervised representation learning."),
        "sections": [
            sec("作者信息", r"作者：Ravid Shwartz-Ziv、Yann LeCun；arXiv:2304.09355v5。全文 39 页；这是综述与统一框架，不是一项新算法 benchmark。"),
            sec("研究问题", r"监督学习里，标签 \(Y\) 定义了“相关信息”；自监督学习训练时没有 \(Y\)。论文问：表征 \(Z\) 应压缩输入 \(X\) 的多少信息，才能既避免记住 nuisance，又不丢失未知下游任务需要的自由度？"),
            sec("背景", r"监督 information bottleneck 在预测信息与输入压缩之间取舍。分解 \(I(X;Z)=I(X;Z\mid Y)+I(Z;Y)\) 后，第一项可视为对该任务多余的信息，第二项是预测相关信息。", r"SSL 以两个 views \(X_1,X_2\) 替代标签：若共享信息足以预测下游任务，压掉每个 view 的独有部分可能有益；若 multiview assumption 失效，同一操作会删除真实信号。"),
            sec("模型与方法", r"Figure 1 用统一图表示监督、无监督和自监督：两个 encoder 产生 \(Z_1,Z_2\)，监督路径解码 \(Y\)，无监督路径重构输入，SSL 路径则让一个 view 的表示预测另一个。", r"综述比较 contrastive InfoNCE、variational bottleneck 与 noncontrastive joint-embedding architectures。InfoNCE 用 negatives 避免坍缩但依赖大 batch；BYOL/SimSiam/VICReg 一类用 stop-gradient、predictor 或协方差正则抑制坍缩。"),
            sec("核心结果与证据", r"Figure 1 最重要的结论不是某条 loss，而是相关性的来源发生了变化：标签定义、重构定义和跨 view 预测定义对应不同 sufficient statistic，因此不存在脱离任务假设的“最佳压缩量”。", r"监督 IB 目标 \(I(X;Z)-\beta I(Z;Y)\) 把 \(\beta\) 作为压缩—预测权衡；但深度线性网络等研究表明 compression 并非一般化的必要条件，文献证据并不支持单一普适机制。", r"连续输入和 deterministic encoder 下 \(I(X;Z)\) 可为无穷或对离散化尺度敏感；高维 MI estimator 的样本复杂度与偏差又很差。因此许多“information plane”结论同时依赖噪声模型、binning 或 variational bound。"),
            sec("有效性与局限", r"这是广泛文献的组织性综述，不能把不同数据、网络和 estimator 下的结果当成同一受控实验。多视图框架的结论依赖 views 共享任务相关信息并把 nuisance 分开；基础模型服务多任务时，这一假设更容易失效。", r"MI 在 deterministic continuous networks 中的定义与估计是核心技术限制。添加噪声、离散化或改用 surrogate 可令量有限，却也改变了被测对象；因此数值 MI 不应被当成不依赖 estimator 的观测量。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2304.09355。全文 39 页，PDF SHA-256：a8d77a13588d4ecfe0bc4671b11619931c8112d1f5f06c27b68277bef8a3283b。", r"复核具体 SSL 信息论论断时，应记录 view construction、encoder 是否随机、MI estimator/bound、negative 数、batch、下游任务和 collapse 指标。", r"Evidence status: full-text verified review; no independent reproduction performed."),
            sec("阅读指南", r"先用 Figure 1 区分三种 relevance 定义，再读 Eq. (3)–(4) 的 IB 分解。随后跳到第 5 节，先处理 deterministic network 与高维估计的病态性，再回看具体 SSL objective；否则很容易把 estimator 的几何效应误读成网络中的真实信息流。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2304.09355/figure-1-multiview-ib.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 12, Figure 1", "alt_text": "监督、无监督和自监督多视图信息瓶颈的统一框图。", "caption": "是否压缩取决于什么变量定义“相关”：标签、输入重构与跨 view 预测对应三种不同的信息约束。", "selection_rationale": "该图是综述的统一坐标系，能替代对大量 SSL 方法逐项罗列的冗长文字。"},
        "figure_refs": [figure("2304.09355", "figure-1-multiview-ib.webp", "Figure 1", 12, "unify relevance definitions across learning paradigms", "两个输入视图、编码表示与不同解码路径组成的统一框架。", "SSL 用跨视图可预测性替代训练标签来定义相关信息。", "Compression is beneficial only relative to the assumed downstream-relevance structure.")],
        "equation_refs": [
            {"label": "Supervised information bottleneck", "latex": r"\mathcal L_{\mathrm{IB}}=I(X;Z)-\beta I(Z;Y)", "role": "trade input compression against task-predictive information", "symbols": {"X": "input", "Z": "representation", "Y": "target", "beta": "relevance weight"}, "evidence": "paper.pdf p. 8, Eq. (3)", "interpretation": "The meaning of compression is task-relative because relevance is supplied by Y."},
            {"label": "Representation-information decomposition", "latex": r"I(X;Z)=I(X;Z\mid Y)+I(Z;Y)", "role": "separate task-superfluous and predictive information", "symbols": {"I(X;Z|Y)": "information not needed once Y is known", "I(Z;Y)": "predictive information"}, "evidence": "paper.pdf p. 8, Eq. (4)", "interpretation": "Without labels, this decomposition requires an assumption about which cross-view information stands in for Y."},
        ],
        "evidence_refs": ["paper.pdf pp. 7–12: IB and unified multiview framework", "paper.pdf pp. 20–22: deterministic-network and high-dimensional MI limitations", "source PDF SHA-256 a8d77a13588d4ecfe0bc4671b11619931c8112d1f5f06c27b68277bef8a3283b", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2304.14772", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2304.14772",
        "title_en": "Multisample Flow Matching: Straightening Flows with Minibatch Couplings", "title_zh": "多样本流匹配：用小批量耦合拉直生成流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("00472db0f830a014", "Flow Matching"),
        "verified_metadata": meta("2304.14772", "v2", "Multisample Flow Matching: Straightening Flows with Minibatch Couplings", ["Aram-Alexandre Pooladian", "Heli Ben-Hamu", "Carles Domingo-Enrich", "Brandon Amos", "Yaron Lipman", "Ricky T. Q. Chen"], ["cs.LG"], "cs.LG", "2023-04-28T11:33:08Z", "Minibatch couplings replace independent endpoint pairing in flow matching to reduce conditional-target variance and straighten probability paths."),
        "sections": [
            sec("作者信息", r"作者：Aram-Alexandre Pooladian、Heli Ben-Hamu、Carles Domingo-Enrich、Brandon Amos、Yaron Lipman、Ricky T. Q. Chen；arXiv:2304.14772v2。全文 30 页。"),
            sec("研究问题", r"Flow Matching 常把噪声样本 \(x_0\) 与数据样本 \(x_1\) 独立配对。宏观边缘分布正确，但单条条件路径可能交叉、弯曲，导致同一 \((x,t)\) 处的 velocity targets 方差大，并需要更多 ODE function evaluations。论文问：能否只改变 minibatch 内的端点耦合，把流拉直而不破坏两端边缘？"),
            sec("背景", r"连续 normalizing flow 由 \(\dot x_t=v_t(x_t)\) 输运密度。Conditional Flow Matching 用易计算的条件速度监督全局 velocity field；训练噪声来自不同 endpoint pairs 在相同区域给出冲突方向。", r"最优传输耦合倾向于把近邻质量配对，减少路径交叉。关键约束是耦合 \(q(x_0,x_1)\) 的两个 marginals 必须仍为 \(q_0,q_1\)，否则训练目标会偷偷改变 prior 或 data distribution。"),
            sec("模型与方法", r"作者将 joint CFM 从独立 \(q_0q_1\) 推广到任意合法 coupling。每步抽取 \(k\) 个噪声和 \(k\) 个数据点，以 doubly stochastic 矩阵 \(\pi_{ij}\) 组成经验耦合；Lemma 4.1 保证对 minibatch 随机性平均后 marginals 不变。", r"BatchOT 用 Hungarian/network-simplex 求精确 batch assignment，成本约 \(O(k^3)\)；BatchEOT 用 Sinkhorn 熵正则，Stable 与 Heuristic couplings 更便宜。模型结构与 ODE 不变，只替换训练 pair sampler。"),
            sec("核心结果与证据", r"Figure 1 在相同模型的不同 NFE 下比较样本：标准 Flow Matching 从 400 步降到 12/8/6 步时身份和构图明显漂移，Multisample Flow Matching 在低 NFE 下仍保持更一致的样本，直观显示轨迹被拉直。", r"二维 toy example 的 conditional-objective/variance proxy 从 CondOT 的 10.72 降到 Stable 1.60、Heuristic 1.56、BatchEOT 0.57、BatchOT 0.24。极限定理在假设下给出 \(k\to\infty\) 时 BatchOT objective 与 straightness 趋零、transport cost 趋于 \(W_2^2\)。", r"ImageNet 64×64 中 CondOT/BatchOT 的 FID 为 13.93/12.37，NFE 为 131/135，variance proxy 为 1880/1733；Stable coupling 的 FID 11.82。改进真实但不统一支配所有指标，也不是理论极限的直接验证。"),
            sec("有效性与局限", r"BatchOT 的 \(O(k^3)\) pairing 增加训练开销，且 minibatch OT 只是 population coupling 的有限样本近似；Sinkhorn 正则与 batch size 会改变路径。", r"渐近直线化定理需要理想假设并取 \(k\to\infty\)，不能推出有限网络、有限 batch 的 FID 单调改善。NFE 还依赖数值求解器与误差容限，视觉一致性不等价于 likelihood 或分布覆盖。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2304.14772；代码：https://github.com/atong01/conditional-flow-matching。全文 30 页，PDF SHA-256：dd7b47857205b6e5f26ac9650ba1647e2152e34d450534249ede3258ffb220a3。", r"复现需固定 batch size、coupling solver、cost metric、Sinkhorn 正则、ODE solver/tolerance、NFE 统计口径与图像随机种子。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 理解“直”意味着低步数下轨迹一致；再读 Eq. (13) 的 marginal 条件、Eq. (15) 的 joint objective 与 Lemma 4.1。最后对照 Table 6，把训练 target variance、求解 NFE 和 FID 当成三个不同观测量。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2304.14772/figure-1-nfe-consistency.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "Flow Matching 与 Multisample Flow Matching 在不同 ODE 步数下的样本比较。", "caption": "minibatch coupling 减少相互冲突的端点配对，使少量 ODE evaluations 仍沿近似相同的生成轨迹。", "selection_rationale": "该图直接可视化论文的核心物理几何——流线弯曲度与低 NFE 一致性——优先于单独数据表。"},
        "figure_refs": [figure("2304.14772", "figure-1-nfe-consistency.webp", "Figure 1", 1, "show low-NFE consistency from straighter flows", "两种 flow-matching 训练在 400、12、8、6 个函数求值下的样本。", "MSFM 的样本随积分步数减少变化较小，符合更直轨迹的解释。", "The visual demonstrates solver robustness, not by itself exact optimal transport.")],
        "equation_refs": [
            {"label": "Valid endpoint coupling", "latex": r"\int q(x_0,x_1)\,dx_1=q_0(x_0),\qquad \int q(x_0,x_1)\,dx_0=q_1(x_1)", "role": "preserve prior and data marginals while changing pair geometry", "symbols": {"q": "endpoint coupling", "q_0": "source marginal", "q_1": "data marginal"}, "evidence": "paper.pdf p. 5, Eq. (13)", "interpretation": "Coupling changes conditional paths without changing either endpoint distribution."},
            {"label": "Joint conditional flow-matching objective", "latex": r"\mathcal L_{\mathrm{JCFM}}=\mathbb E_{t,\,q(x_0,x_1)}\!\left[\left\|v_t(x_t;\theta)-u_t(x_t\mid x_1)\right\|_2^2\right]", "role": "train the global velocity field under a chosen endpoint coupling", "symbols": {"v_t": "learned velocity", "u_t": "conditional target velocity", "q": "endpoint coupling"}, "evidence": "paper.pdf p. 5, Eq. (15)", "interpretation": "Better-aligned endpoint pairs reduce conflicting velocity targets at fixed model capacity."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–7: generalized coupling and multisample construction", "paper.pdf pp. 8–12 and appendices: theory and image experiments", "source PDF SHA-256 dd7b47857205b6e5f26ac9650ba1647e2152e34d450534249ede3258ffb220a3", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2305.13266", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2305.13266",
        "title_en": "Coarse-to-Fine: a Hierarchical Diffusion Model for Molecule Generation in 3D", "title_zh": "从粗到细：用于三维分子生成的层级扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("500a6d5ef3a90190", "Generative Models"),
        "verified_metadata": meta("2305.13266", "v2", "Coarse-to-Fine: a Hierarchical Diffusion Model for Molecule Generation in 3D", ["Bo Qiang", "Yuxuan Song", "Minkai Xu", "Jingjing Gong", "Bowen Gao", "Hao Zhou", "Weiying Ma", "Yanyan Lan"], ["q-bio.BM", "cs.AI", "cs.LG"], "q-bio.BM", "2023-05-05T13:08:38Z", "A fragment-level equivariant diffusion model generates coarse molecular geometry before iterative fine-grained atom and bond assembly."),
        "sections": [
            sec("作者信息", r"作者：Bo Qiang、Yuxuan Song、Minkai Xu、Jingjing Gong、Bowen Gao、Hao Zhou、Weiying Ma、Yanyan Lan；arXiv:2305.13266v2。全文 24 页。"),
            sec("研究问题", r"原子级三维扩散必须同时学全局骨架、局部键合和环结构，微小几何误差会产生断环或不合理价态。论文问：能否先在化学 fragment 的粗自由度上生成全局构象，再以受约束的细化过程组装原子和键？"),
            sec("背景", r"这类似物理中的 coarse graining：粗变量保留 fragment 类型与质心位置，积分掉的内部自由度在条件 fine model 中恢复。层级分解降低全局搜索维数，但如果 coarse map 丢失关键信息，细模型不能唯一重建微观结构。", r"fragment graph 的边表示共享原子或键；价态冲突具有组合约束，仅靠一次独立预测容易选中局部容易拼接、全局却不合法的片段。"),
            sec("模型与方法", r"粗状态 \(H=[H_f,H_p]\) 包含旋转/平移不变的化学特征与等变的 fragment-center 坐标。E(3)-equivariant diffusion 在去质心空间生成 \(H\)；随后 iterative message passing 在邻接候选之间反复更新，恢复原子、键与局部构象。", r"生成分解为 \(P_{\theta,\phi}(V,E)=P_\theta(H)P_\phi(V,E\mid H)\)。训练下界把 coarse diffusion loss、fine reconstruction/message-passing loss 与固定分解项分开。"),
            sec("核心结果与证据", r"Figure 7 将 HierDiff 与 atom-based EDM 的生成分子并列：HierDiff 的环与骨架更连贯，EDM 中明显扭曲或断裂的 substructures 用红框和红线标出。它比单个 validity 数字更直接显示层级表示修复的几何模式。", r"GEOMDRUG conformation 评估中，EDM 的 atom-level COV/MAT 为 0.489/1.349，HierDiff-E 为 0.546/1.121；fragment-level COV/MAT 从 0.097/3.234 改善到 0.153/2.583。HierDiff-P 的 fragment COV 0.202、MAT 2.431 更好，但 atom COV 0.490，说明不同层级指标并非一致支配。", r"drug-likeness Table 1 中 HierDiff-E/P 的 QED 为 0.632/0.639，高于 EDM 0.608；RA 为 0.548/0.639，高于 0.441。训练数据 GEOMDRUG 的 QED/RA 仍为 0.658/0.915，表明生成分布尚未达到数据统计。"),
            sec("有效性与局限", r"fragment vocabulary 与 decomposition 决定 coarse variables；罕见基团、宏环或超出词表的化学空间可能被截断。消融显示没有 iterative refinement 时模型偏向容易组装的 fragments，说明粗粒化本身不够。", r"实验集中在 GEOMDRUG、CrossDocked2020 与 QM9 尺度；MD/force-field conformation metric、QED 和结构 validity 不证明可合成性、稳定性或真实 binding affinity。层级模型还引入词表构建和多阶段误差传播。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2305.13266；代码：https://github.com/qiangbo1222/HierDiff。全文 24 页，PDF SHA-256：de07508e421b3968d4fdda0d5e59961c2894a36a9a252df9a9fbe68e5c7c77be。", r"复现需固定 fragment vocabulary/decomposition、E(3) coordinate convention、diffusion schedule、refinement 轮数、RDKit/MD 与 force-field 版本，以及 COV/MAT 阈值。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 7 识别 atom-level baseline 的具体失效模式；再读 Eq. (5) 的层级概率分解和 fine refinement。最后对照 Table 1/2，分别判断化学统计、原子构象和 fragment 构象，避免用单一 validity 概括模型。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2305.13266/figure-7-molecule-comparison.webp", "label": "Figure 7", "visual_type": "comparison", "evidence": "paper.pdf p. 8, Figure 7", "alt_text": "HierDiff 与 EDM 生成的二维分子图和三维构象，EDM 破损结构以红色标记。", "caption": "先生成 fragment 骨架再细化原子，使环和连接关系更连贯；红色标记展示 atom-level EDM 的典型几何与拓扑失效。", "selection_rationale": "这是论文最重要且最具可视性的分子图，直接解释层级模型为何改善结构，而不是只展示汇总数据。"},
        "figure_refs": [figure("2305.13266", "figure-7-molecule-comparison.webp", "Figure 7", 8, "compare molecular topology and geometry failure modes", "两种方法的分子图和三维构象对比。", "HierDiff 的 fragment-first 生成减少断环和扭曲连接。", "Visual coherence supports the hierarchical mechanism but does not establish synthesizability.")],
        "equation_refs": [{"label": "Coarse-to-fine factorization", "latex": r"P_{\theta,\phi}(V,E)=P_\theta(H)\,P_\phi(V,E\mid H)", "role": "separate global fragment generation from atom-and-bond refinement", "symbols": {"H": "coarse fragment graph and coordinates", "V": "atoms", "E": "bonds", "theta,phi": "coarse and fine model parameters"}, "evidence": "paper.pdf p. 5, Eq. (5)", "interpretation": "The coarse latent fixes global organization while the conditional fine model restores microscopic chemistry."}],
        "evidence_refs": ["paper.pdf pp. 3–6: hierarchical representation and objective", "paper.pdf pp. 7–8, Tables 1–2 and Figure 7: molecule and conformation results", "source PDF SHA-256 de07508e421b3968d4fdda0d5e59961c2894a36a9a252df9a9fbe68e5c7c77be", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2306.10404", "source_version": "v6", "source_pdf": "https://arxiv.org/pdf/2306.10404",
        "title_en": "The RL Perceptron: Generalisation Dynamics of Policy Learning in High Dimensions", "title_zh": "RL 感知机：高维策略学习的泛化动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("718dc1ac444b3183", "Control & Reinforcement Learning"),
        "verified_metadata": meta("2306.10404", "v6", "The RL Perceptron: Generalisation Dynamics of Policy Learning in High Dimensions", ["Nishil Patel", "Sebastian Lee", "Stefano Sarao Mannelli", "Sebastian Goldt", "Andrew Saxe"], ["cs.LG", "cond-mat.dis-nn"], "cs.LG", "2023-06-17T18:16:51Z", "A teacher-student RL perceptron yields closed order-parameter ODEs for policy-gradient learning and exposes learnability phases and speed-accuracy tradeoffs."),
        "sections": [
            sec("作者信息", r"作者：Nishil Patel、Sebastian Lee、Stefano Sarao Mannelli、Sebastian Goldt、Andrew Saxe；arXiv:2306.10404v6。全文 22 页。"),
            sec("研究问题", r"高维 policy gradient 的理论通常给 worst-case bounds，却很少描述完整学习轨迹。论文问：对延迟稀疏奖励的序列决策，能否像统计物理中的 teacher–student perceptron 一样，把 \(D\) 维随机更新压缩成少数序参量的确定性动力学？"),
            sec("背景", r"teacher 权重 \(w^*\) 规定每个随机输入上的正确二元动作，student 权重 \(w\) 通过一段 \(T\) 步 episode 后的 reward 更新。热力学极限 \(D\to\infty\) 下，局部场变成联合 Gaussian，宏观状态由 \(Q=w\cdot w/D\)、\(R=w\cdot w^*/D\) 与固定 \(S=w^*\cdot w^*/D=1\) 封闭。", r"归一化重叠 \(\rho=R/\sqrt Q\) 相当于磁化方向的一致度；泛化误差为两个感知机在新输入上符号不一致的概率。"),
            sec("模型与方法", r"作者对在线 REINFORCE 更新做典型平均，得到 \(R,Q\) 的闭合 ODE；reward functional \(G_t\) 可表示存活奖励、失败惩罚、中间奖励与不同 episode length。Figure 2 显示 \(D=900\) 的 simulation 与 ODE 在多种协议下吻合。", r"低维方程随后用于解析/数值优化学习率与任务长度 curriculum，并追踪 fixed points、first-order learnability transition 和 critical slowing。"),
            sec("核心结果与证据", r"Figure 1 串联 teacher–student 几何、长度 \(T\) 的 RL episode 和 ODE/simulation 对比：微观权重更新最终只需跟踪 \(Q,R\)，图中 \(D=900,T=12\) 已显示有限维曲线逼近理论。", r"一般化误差精确写成 \(\epsilon_g=\pi^{-1}\arccos(R/\sqrt Q)\)。改变 reward/penalty 会产生 easy 与 hybrid-hard 区域；靠近临界奖励强度时出现长平台和临界变慢，有限 \(D\) 涨落偶尔可越过亚稳 fixed point。", r"Figure 5 显示 speed–accuracy tradeoff：放宽一局中正确动作数阈值可加快早期学习，却降低渐近重叠。Bossfight 的 6720 维像素实验在 10 次重复中复现该趋势；Pong 用 20 agents、\(T=30,50,70,90\)，但作者明确说明 \(T=90\) 在预算内尚未训练到反超。"),
            sec("有效性与局限", r"可解性依赖二元动作、随机 Gaussian 输入、线性 perceptron teacher/student 与特定 policy-gradient 更新；真实环境的状态转移、深层表征和非平稳数据会增加序参量并破坏闭合。", r"ODE 在 \(D\to\infty\) 渐近精确，有限维 escape 与噪声可能改变亚稳寿命。Bossfight/Pong 是修改后的经验探针，不能证明解析最优 curriculum 直接适用于通用深度 RL；Pong 最难设置还没有达到渐近区。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2306.10404；代码：https://github.com/SaxeLab/RL_perceptron。全文 22 页，PDF SHA-256：0d8eb8cbe3e9a17d7c08b00419b3c67a151284f21056aa5ac280628e6f36a101。", r"复现理论应固定 \(D,T,\eta_1,\eta_2\)、学习率缩放、初始 \(Q,R\) 与时间变量 \(\alpha\)；经验实验还需记录环境修改、网络、并行 agents、训练预算和 repetitions。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 Eqs. (8)–(9)，把高维权重映射到 \(Q,R,\rho\) 与泛化误差；再比较 Figure 2 的 ODE/finite-\(D\) 曲线。最后读 learnability phase diagram 与 Figure 5，并用 Bossfight/Pong 只检验定性机制，不把它们当成一般深度 RL 定理。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2306.10404/figure-1-rl-perceptron.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "teacher-student 感知机、序列 RL episode 和 ODE 与仿真曲线的总览。", "caption": "高维 policy learning 被压缩为少数重叠序参量的 ODE；episode reward 决定宏观流场与可学习相。", "selection_rationale": "该图同时展示微观模型、决策序列和宏观动力学，是全文最完整且最直观的理论可视化。"},
        "figure_refs": [figure("2306.10404", "figure-1-rl-perceptron.webp", "Figure 1", 2, "connect microscopic RL updates to macroscopic order parameters", "teacher-student 模型、RL episode 和 ODE/仿真的组合图。", "统计平均把高维随机学习轨迹约化为低维确定性流。", "Agreement at finite D supports the asymptotic closure within this idealized model.")],
        "equation_refs": [
            {"label": "Order parameters", "latex": r"Q=\frac{w\cdot w}{D},\qquad R=\frac{w\cdot w^*}{D},\qquad S=\frac{w^*\cdot w^*}{D}=1", "role": "close the high-dimensional learning dynamics on macroscopic overlaps", "symbols": {"w": "student weights", "w*": "teacher weights", "D": "input dimension", "Q,R,S": "norm and overlap order parameters"}, "evidence": "paper.pdf p. 5, Eq. (8)", "interpretation": "In the thermodynamic limit, these overlaps determine the Gaussian local fields and average learning trajectory."},
            {"label": "Generalisation error", "latex": r"\epsilon_g=\frac{1}{\pi}\arccos\!\left(\frac{R}{\sqrt Q}\right)=\frac{1}{\pi}\arccos\rho", "role": "translate student-teacher alignment into policy disagreement", "symbols": {"epsilon_g": "generalisation error", "rho": "normalized overlap", "R": "alignment", "Q": "student norm"}, "evidence": "paper.pdf p. 5, Eq. (9)", "interpretation": "Policy accuracy is a geometric angle between teacher and student weight vectors."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: model, order parameters and ODE closure", "paper.pdf pp. 6–10: curricula, learnability phases and speed–accuracy tradeoff", "paper.pdf pp. 10–12: Bossfight and Pong probes", "source PDF SHA-256 0d8eb8cbe3e9a17d7c08b00419b3c67a151284f21056aa5ac280628e6f36a101", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
