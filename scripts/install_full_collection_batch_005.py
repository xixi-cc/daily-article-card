#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 005."""

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
        "sampled_at": "2026-08-26", "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection", "candidate_count": 452,
    }


def meta(arxiv_id: str, version: str, title: str, authors: list[str], categories: list[str],
         primary: str, published: str, abstract: str) -> dict[str, object]:
    return {"arxiv_id": arxiv_id, "version": version, "title": title, "authors": authors,
            "categories": categories, "primary_category": primary, "published": published,
            "abstract": abstract}


CARDS = [
    {
        "arxiv_id": "2101.08176", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2101.08176",
        "title_en": "Introduction to Normalizing Flows for Lattice Field Theory",
        "title_zh": "面向格点场论的正规化流入门",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("ed189695c2b2b746", "Field Theory"),
        "verified_metadata": meta("2101.08176", "v3", "Introduction to Normalizing Flows for Lattice Field Theory",
            ["Michael S. Albergo", "Denis Boyda", "Daniel C. Hackett", "Gurtej Kanwar", "Kyle Cranmer", "Sébastien Racanière", "Danilo Jimenez Rezende", "Phiala E. Shanahan"],
            ["hep-lat", "cond-mat.stat-mech", "cs.LG"], "hep-lat", "2021-01-20T15:16:28Z",
            "An executable tutorial on flow-based sampling for scalar lattice theory and gauge-equivariant U(1) theory."),
        "sections": [
            sec("作者信息", "作者：Michael S. Albergo、Denis Boyda、Daniel C. Hackett、Gurtej Kanwar、Kyle Cranmer、Sébastien Racanière、Danilo Jimenez Rezende、Phiala E. Shanahan；arXiv:2101.08176v3。", "本卡核对 40 页全文。原文是与 Jupyter notebook 配套的可执行教程，重点是从概率恒等式到可检验代码的完整链条，而不是提出新的 benchmark。"),
            sec("研究问题", "格点场论需要从玻尔兹曼权重抽样；临界慢化、拓扑冻结和高维强关联会使局域 Markov 更新产生很长自相关。正规化流能直接生成全局 proposal，但只有结合精确接受拒绝或重加权后才保持目标分布无偏。", "教程问的是：怎样把可逆映射、Jacobian、反向 KL 训练、independence Metropolis 和有效样本量组织成一套物理上可审计的采样器，并在 U(1) 格点规范理论中把规范对称性直接编码进网络？"),
            sec("背景", r"可逆流 \(f:z\mapsto\phi\) 将简单基分布 \(r(z)\) 推到模型分布 \(q(\phi)\)，其密度由变量替换公式精确计算。训练目标是 \(D_{\mathrm{KL}}(q\Vert p)\)，只需从模型自身采样和计算未归一化作用量。", "直接使用 q 的样本一般仍有模型偏差；把 q 作为 independence proposal，加上 Metropolis–Hastings 接受率，或用重要性权重修正，才能得到渐近精确估计。"),
            sec("模型与方法", "标量理论部分从 checkerboard affine coupling layers 开始：每层冻结一半格点，用其余格点预测 scale 与 shift；多层交替 mask 保证全局耦合且 Jacobian 为三角结构。", r"训练后用 \(A(\phi\!\to\!\phi')=\min[1,p(\phi')q(\phi)/(p(\phi)q(\phi'))]\) 构造 independence chain，并以 reweighting ESS、接受率和 observable autocorrelation 判断 q 是否足够覆盖目标。", "U(1) 部分不直接更新 link angle，而以 plaquette 的 gauge-invariant 信息生成等变 link 更新；mask 必须同时满足可逆性、局域依赖和格点平移覆盖。"),
            sec("核心结果与证据", "教程在二维标量场上逐步展示训练 loss、模型与目标 action、重加权 observable 及自相关诊断；核心证据不是单一数值，而是同一 notebook 能从目标作用量生成无偏 MCMC 流程。", "对 U(1) 理论，Figures 2–5 依次定义 link、plaquette、将 plaquette 更新推回 link 的等变作用以及合法 mask。它们说明规范不变性不是数据增强，而是 coupling layer 的结构约束。", "最重要的物理边界是：flow 的独立样本质量决定接受率与权重方差，但精确性来自后续统计校正。一个视觉上匹配的模型分布不能替代 detailed balance 或 importance identity。"),
            sec("有效性与局限", "这是教学实现，不是大体积 QCD 性能声明；标量与 U(1) 例子的自由度、耦合和网络规模都为课堂可运行性服务。", "反向 KL 倾向 mode seeking，q 若漏掉相空间扇区，会造成低接受率或极端权重；有限训练样本上的漂亮直方图不能证明全局覆盖。", "independence proposal 的接受事件仍可相关，ESS 也依赖 observable；评估必须同时报告接受率、权重尾部和积分自相关时间。", "规范等变层减少无效自由度，但不自动解决拓扑扇区或费米子行列式的代价。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2101.08176；PDF：https://arxiv.org/pdf/2101.08176；论文明确建议配合所附 Jupyter notebook 交互运行。", "全文 PDF 共 40 页，SHA-256：1b0caf63db00d605563de7cf56b5905c2572ee02dbdca7aaaf187231fa1a7822。", "复现应固定格点大小、作用量参数、mask 顺序、随机种子和训练预算；保存 raw chain、log-weight、接受事件与逐 observable 自相关，而不只保存最终均值。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读标量场 notebook 单元，逐项核对变量替换、KL 和 Metropolis 接受率；再用 ESS 与自相关理解“模型质量”和“统计精确性”的区别。", "随后读 U(1) 部分的 Figures 2–5，从 gauge transformation 到 plaquette-conditioned link update 重建等变性。", "最后把教程范围与后续费米子论文分开：这里给出方法骨架，不声称已解决现实 QCD 规模。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "正规化流把简单基分布可逆地映射到格点场配置，并提供精确 Jacobian；结合 independence Metropolis 或重加权后，可作为渐近精确的全局 proposal。教程从二维标量场推进到 U(1) 规范理论，展示怎样把 plaquette 规范不变量和等变 link 更新写进 coupling layer，同时强调生成模型拟合好并不等于采样器已无偏。", "selection_rationale": "原文是代码教程，图多为局部定义和 mask；题目加物理摘要更能概括完整方法链。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Flow density", "latex": r"q(\phi)=r(f^{-1}(\phi))\left|\det\frac{\partial f^{-1}}{\partial\phi}\right|", "role": "evaluate the generated field density exactly", "symbols": {"phi": "lattice field", "z": "base variable", "f": "invertible flow", "r": "base density"}, "evidence": "paper.pdf normalizing-flow introduction", "interpretation": "Exact density evaluation makes importance weights and Metropolis corrections available."},
            {"label": "Independence Metropolis correction", "latex": r"A(\phi\to\phi')=\min\left(1,\frac{p(\phi')q(\phi)}{p(\phi)q(\phi')}\right)", "role": "remove model bias while using the flow as a global proposal", "symbols": {"p": "target Boltzmann density", "q": "flow proposal density", "phi_prime": "proposed field"}, "evidence": "paper.pdf scalar-field sampling section", "interpretation": "The chain remains exact even when q differs from p, provided support and detailed-balance conditions hold."},
        ],
        "evidence_refs": ["paper.pdf scalar tutorial: flow construction, reverse-KL training and exact corrections", "paper.pdf gauge tutorial: lattice U(1), plaquettes, equivariant updates and masks", "source PDF SHA-256 1b0caf63db00d605563de7cf56b5905c2572ee02dbdca7aaaf187231fa1a7822", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2104.09456", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2104.09456",
        "title_en": "Self-supervised Representation Learning With Path Integral Clustering For Speaker Diarization",
        "title_zh": "用于说话人日志的路径积分聚类自监督表征学习",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv", "provenance": provenance("3defde399fb7adf3", "Field Theory"),
        "verified_metadata": meta("2104.09456", "v1", "Self-supervised Representation Learning With Path Integral Clustering For Speaker Diarization", ["Prachi Singh", "Sriram Ganapathy"], ["eess.AS", "cs.SD"], "eess.AS", "2021-04-19T17:13:24Z", "An iterative loop alternates path-integral clustering and triplet-based embedding learning for speaker diarization."),
        "sections": [
            sec("作者信息", "作者：Prachi Singh、Sriram Ganapathy；arXiv:2104.09456v1，语音与音频处理。", "本卡核对 12 页全文。Paper Collection 的 Field Theory 标签来自目录分类；本文的 path integral 是图上随机游走路径和，不是量子或统计场论泛函积分。"),
            sec("研究问题", "传统 diarization 先训练 x-vector，再冻结表示做聚类；表示学习与聚类目标彼此隔离。若 embedding 的局部几何不适合当前录音中的说话人结构，后端 AHC 无法反向修正它。", "作者提出闭环：用图结构的 path-integral clustering 产生伪标签，再用这些标签采样 triplet 微调表示，反复迭代直到达到估计说话人数。"),
            sec("背景", "PIC 把 embedding 相似度归一化为有向图转移概率，并用簇内所有路径概率之和衡量簇稳定性；合并两个强连通簇若提高路径积分，就比只看最近或平均 pairwise affinity 更利用全局结构。", "自监督环路的风险是 confirmation bias：错误聚类会生成错误 triplet，再把错误几何强化。因此论文设置逐轮阈值、temporal weighting 和停止准则。"),
            sec("模型与方法", "Figure 1 是完整反馈回路：固定长度音频片段先得到 x-vectors；PIC 产生第 q 轮簇标签；标签生成 triplet，DNN 用改进 triplet similarity 更新 embedding，再回到下一轮 PIC。", r"图邻接权重为 \(W_{ij}=[1+\exp(-s(i,j))]^{-1}\)，仅保留 K-nearest neighbors；行归一化得到转移矩阵 \(P\)，cluster path integral 由簇内多步转移的 trace/路径和构造。", "说话人数可已知或由阈值估计；实验在 CALLHOME 与 AMI 上对 x-vector+AHC、PIC、SSC 及 VB-HMM refinement 做逐项比较。"),
            sec("核心结果与证据", "Figure 1 比冗长算法文字更清楚地显示 clustering→triplet mining→representation update 的闭环，而不是两个独立阶段。", "论文摘要报告相对 x-vector+AHC 的 diarization error rate 相对改善：CALLHOME 约 13%，AMI 约 59%。改进在 AMI 更大，说明会议录音中全局图结构和表示再训练更有价值。", "Figure 7 的 t-SNE 仅是定性辅助；主要证据来自两数据集 DER 表及已知/未知说话人数设置。VB-HMM 后处理还能进一步改善边界，但这不应归因于 SSC 表征本身。"),
            sec("有效性与局限", "伪标签环路没有真值保证，初始 embedding 或 PIC 图错误可被放大；K、阈值和 temporal weighting 对稳定性关键。", "CALLHOME 与 AMI 的录音条件、分段和说话人数分布有限；跨语言、重叠语音和远场噪声的外推仍需独立测试。", "DER 相对改善依赖基线与后处理配置；应同时报告绝对 DER、oracle speaker count 与 estimated speaker count，不能只引用百分比。", "t-SNE 簇分离不等同于 diarization 成功，时间边界、重叠说话和 speaker confusion 需分项误差。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2104.09456；PDF：https://arxiv.org/pdf/2104.09456。", "全文 PDF 共 12 页，SHA-256：7acc8e17ca9e2fb794f0267350bbdd3c27ed22b70626bd6d9fde1bda5a5e4e38。", "复现需固定分段长度、x-vector extractor、KNN 图、PIC 阈值、triplet margin、每轮训练步数和停止条件；保存每轮簇数、伪标签一致率及 DER 分解。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1，追踪标签怎样从 PIC 回流到 DNN；再读 Sec. III-C 的 path integral 定义和 Sec. III-F 的停止规则。", "随后核对 CALLHOME 与 AMI 的绝对 DER 表，而非只读摘要中的相对百分比。", "最后看 Figure 7 时把它当解释性投影，不把二维可视化当作定量证明。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2104.09456/figure-1-ssc-loop.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "SSC 在路径积分聚类与 triplet 表征学习之间循环的框图。", "caption": "PIC 的簇标签生成下一轮 triplet，更新后的 DNN embedding 又反馈给 PIC。", "selection_rationale": "该机制图直接解释论文贡献，比 t-SNE 或 DER 曲线更适合作为封面。"},
        "figure_refs": [{"label": "Figure 1", "asset_path": "assets/collection-figures/2104.09456/figure-1-ssc-loop.webp", "section": "核心结果与证据", "role": "visualize the iterative clustering-representation loop", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "SSC 自监督循环。", "caption": "聚类伪标签驱动 triplet mining，表示更新后再次聚类。", "interpretation": "The method couples representation geometry to the recording-specific clustering objective."}],
        "equation_refs": [{"label": "KNN graph weight", "latex": r"W_{ij}=\begin{cases}[1+\exp(-s(i,j))]^{-1},&y_j\in\mathcal N_i^K\\0,&\text{otherwise}\end{cases}", "role": "construct the sparse directed similarity graph used by PIC", "symbols": {"s": "pairwise embedding similarity", "N_i_K": "K nearest neighbors", "W": "adjacency matrix"}, "evidence": "paper.pdf p. 3, Eq. (2)", "interpretation": "Only local neighbors define transitions, while path integrals aggregate their global connectivity."}],
        "evidence_refs": ["paper.pdf pp. 2–5: SSC loop, PIC graph and triplet learning", "paper.pdf pp. 6–9: CALLHOME/AMI DER comparisons and embedding visualization", "source PDF SHA-256 7acc8e17ca9e2fb794f0267350bbdd3c27ed22b70626bd6d9fde1bda5a5e4e38", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2106.05934", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2106.05934",
        "title_en": "Flow-based sampling for fermionic lattice field theories",
        "title_zh": "费米格点场论的流模型采样",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv", "provenance": provenance("7bf4c67140c643f3", "Field Theory"),
        "verified_metadata": meta("2106.05934", "v2", "Flow-based sampling for fermionic lattice field theories", ["Michael S. Albergo", "Gurtej Kanwar", "Sébastien Racanière", "Danilo J. Rezende", "Julian M. Urban", "Denis Boyda", "Kyle Cranmer", "Daniel C. Hackett", "Phiala E. Shanahan"], ["hep-lat", "cond-mat.stat-mech", "cs.LG"], "hep-lat", "2021-06-10T17:32:47Z", "Four exact sampling schemes extend normalizing flows to lattice theories with dynamical fermions."),
        "sections": [
            sec("作者信息", "作者：Michael S. Albergo 等九人；arXiv:2106.05934v2，hep-lat 并交叉统计物理与机器学习。", "本卡核对 26 页全文。数值示范是二维无质量 staggered fermion 与标量场 Yukawa 耦合，并以 HMC 为基线。"),
            sec("研究问题", "积分掉 Grassmann 费米场后，玻色场权重包含昂贵且非局域的 fermion determinant。直接训练只对玻色场采样的 flow 会在训练或接受率中反复计算行列式；引入 pseudofermion 又产生条件分布与联合分布的建模选择。", "论文系统比较四种保持渐近精确性的方案：标量边缘、Gibbs 条件更新、自回归分解和完全联合 flow，并问各自把行列式代价、模型误差和 Markov 自相关放在哪里。"),
            sec("背景", r"目标联合密度可写为 \(p(\phi,\varphi)=p(\phi)p(\varphi\mid\phi)\)，其中 pseudofermion \(\varphi=\mathcal A(\phi)\chi\) 可由条件 Gaussian 精确采样。", "flow proposal 本身近似目标；Metropolis correction、Gibbs detailed balance 或重加权赋予 exactness。不同分解的可扩展性不能只由接受率判断，因为某些方案每步仍需 determinant 或线性求解。"),
            sec("模型与方法", "Figure 1 将四种 sampler 并列：φ-marginal、Gibbs、autoregressive 与 joint；蓝色为当前 Markov 状态，黄色为可采样模型，绿色为接受拒绝。", "作者为四种分解设计 coupling-layer flows，并使用 even-odd preconditioning。每种训练后生成 100 条、每条 10,000 步的链，丢弃前 1,000 步热化。", r"统计效率用接受率和 observable-specific integrated autocorrelation \(\tau_X^{\mathrm{int}}=\frac12+\sum_{\tau=1}^{\tau_{\max}}\Gamma_X(\tau)/\Gamma_X(0)\) 评估，窗口由 Madras–Sokal 规则确定。"),
            sec("核心结果与证据", "Figure 1 是方法选择图：它显示哪些变量被 flow 生成、哪些保持为链状态，以及 exact accept/reject 位于何处，替代逐段文字比较。", "四种 flow-based exact samplers 对 magnetization、chiral condensate 及标量/费米二点关联给出与 HMC 相容的结果；一致性是无偏性的首要检查。", "φ-marginal 在该小系统中接受率较高、自相关较低，但显式 determinant 在大体积或轻费米质量下扩展困难；若用 noisy determinant estimator，其方差可压低接受率。", "其余三种方案在 perfect model 极限可达 100% 接受率，但 Gibbs proposal 依赖前一 φ，不能像 independence sampler 那样完全异步生成。论文的结论是权衡地图，不是单一赢家。"),
            sec("有效性与局限", "数值系统为二维 toy Yukawa theory；离四维 QCD、大体积和接近手征极限仍有数量级差距。", "接受率与自相关依赖 action 参数和 observable，不能用一个平均数概括。训练成本、Dirac solve 和 determinant estimator 的墙钟开销需单独核算。", "模型质量在有限格点上可管理，不代表体积增长时 KL 或权重方差温和；接近热力学极限可能出现 overlap catastrophe。", "所有 exactness 论证都依赖接受拒绝、detailed balance 或无偏重加权正确实现，不能直接部署裸 flow 样本。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2106.05934；PDF：https://arxiv.org/pdf/2106.05934。", "全文 PDF 共 26 页，SHA-256：ea75b10a32baf6510c3b1d3696759c6e1c4be346d1e257e5b43282ca64c909ac。", "复现需对四种分解使用相同作用量、格点、链长与误差分析；保存接受事件、每次 Dirac solve/行列式成本、权重、raw observables 和 jackknife blocks。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1 和 Table I，画出每种 sampler 的状态变量、proposal 和 exactness 机制。", "再读 Sec. IV 的四个 flow 架构，注意哪些 conditional 可以精确采样、哪些需近似。", "最后用 Table III 和 Figures 4–5 同时检查正确 observable 与自相关；不要按接受率单独排名。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2106.05934/figure-1-sampling-schemes.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 5, Figure 1", "alt_text": "费米 flow 的四种渐近精确采样方案。", "caption": "边缘、Gibbs、自回归和联合方案把 flow proposal、链状态与接受拒绝放在不同位置。", "selection_rationale": "四方案示意图是论文最重要的比较结构，比单一相关函数曲线更能解释贡献。"},
        "figure_refs": [{"label": "Figure 1", "asset_path": "assets/collection-figures/2106.05934/figure-1-sampling-schemes.webp", "section": "核心结果与证据", "role": "compare four exact sampling factorizations", "evidence": "paper.pdf p. 5, Figure 1", "alt_text": "四种 fermionic flow sampler。", "caption": "蓝色为链状态，黄色为生成密度，绿色为接受拒绝。", "interpretation": "Each factorization moves determinant and conditional-sampling costs to a different stage."}],
        "equation_refs": [
            {"label": "Pseudofermion conditional sample", "latex": r"\varphi=\mathcal A(\phi)\chi,\qquad \chi\sim\mathcal N_{\mathbb C}(0,I)", "role": "draw pseudofermions exactly conditional on the bosonic field", "symbols": {"phi": "bosonic field", "varphi": "pseudofermion", "A": "operator whose product gives the fermion matrix", "chi": "complex Gaussian noise"}, "evidence": "paper.pdf p. 5, Eq. (16)", "interpretation": "Exact conditional sampling enables Gibbs-style schemes without explicitly normalizing the conditional density."},
            {"label": "Integrated autocorrelation time", "latex": r"\tau_X^{\mathrm{int}}=\frac12+\sum_{\tau=1}^{\tau_{\max}}\frac{\Gamma_X(\tau)}{\Gamma_X(0)}", "role": "measure observable-specific Markov-chain efficiency", "symbols": {"X": "observable", "Gamma_X": "autocorrelation function", "tau_max": "window cutoff"}, "evidence": "paper.pdf p. 15, Eq. (52)", "interpretation": "Acceptance rate alone is insufficient because different observables decorrelate on different time scales."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–8: four exact schemes and flow architectures", "paper.pdf pp. 12–16: observable agreement, acceptance and autocorrelation", "paper.pdf Sec. VII: scaling limitations and outlook", "source PDF SHA-256 ea75b10a32baf6510c3b1d3696759c6e1c4be346d1e257e5b43282ca64c909ac", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2106.07582", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2106.07582",
        "title_en": "Non Gaussian Denoising Diffusion Models", "title_zh": "非高斯去噪扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv", "provenance": provenance("124ba7342af02f26", "Generative Models"),
        "verified_metadata": meta("2106.07582", "v1", "Non Gaussian Denoising Diffusion Models", ["Eliya Nachmani", "Robin San Roman", "Lior Wolf"], ["cs.LG", "cs.CV", "cs.SD", "eess.AS"], "cs.LG", "2021-06-14T16:42:43Z", "Gamma and Gaussian-mixture forward noise are tested as alternatives to standard Gaussian diffusion."),
        "sections": [
            sec("作者信息", "作者：Eliya Nachmani、Robin San Roman、Lior Wolf；arXiv:2106.07582v1。", "本卡核对 12 页全文。实验覆盖 CelebA、LSUN Church 与 LJ speech，比较 Gaussian、Gaussian mixture 和 Gamma forward noise。"),
            sec("研究问题", "标准扩散模型选择 Gaussian 噪声，原因是闭合的加噪边缘与简单训练目标，而不是数据残差必然高斯。作者观察预训练 DDPM 的图像差分直方图存在非高斯形状，问额外自由度能否改善少步采样。", "关键约束是替代噪声仍需可高效重参数化，使任意时间步的带噪样本能直接构造，而不是逐步模拟整条 forward chain。"),
            sec("背景", "Gaussian diffusion 的闭包性使多步噪声仍是 Gaussian。Gamma 分布具有可加性；适当中心化和缩放后可维持零均值及预定方差。Gaussian mixture 则用离散成分增加多峰自由度。", "若 forward kernel 改变，reverse model 的训练目标和采样递推也必须一致修改；只在末端换 prior 并不等价。"),
            sec("模型与方法", r"Gamma 方案令每步噪声来自中心化 Gamma，并选择 shape/rate 使累积噪声满足目标方差日程；模型预测标准化噪声 \(\epsilon_t\)，reverse update 使用对应的非高斯样本。", "mixture 方案将多个 Gaussian noise variables 组合，并保持可直接采样的时刻边缘。作者在相同迭代数下比较 DDPM-like 与 DDIM-like 采样。", "图像指标用 FID，语音用 PESQ、STOI 与 MCD；Figure 2 固定同一初始噪声，直观比较三种 noise law 的 100-step 生成结果。"),
            sec("核心结果与证据", "Figure 2 显示同一初始噪声下三行 CelebA 样本：单 Gaussian、Gaussian mixture、Gamma。它让改变量只剩 forward noise family，比随机挑选不同 seed 更可解释。", "CelebA DDIM 10/20/50/100 steps 中 Gamma FID 为 11.64/6.83/4.28/3.17，均优于单 Gaussian 的 17.33/13.73/9.17/6.53；1000-step 时 Gamma 2.92 也优于 3.51。", "LSUN Church 的 Gamma DDPM 在 10/20/50/100 steps 为 28.56/19.68/10.53/7.87，对应 Gaussian 为 51.56/23.37/11.16/8.27。mixture 在高分辨率上因训练成本未完成。", "优势主要出现在少步采样；论文没有给出哪类数据分布对应哪种最优噪声的理论判据。"),
            sec("有效性与局限", "噪声族、参数化与训练预算同时变化，不能把所有收益解释为“真实残差是 Gamma”；Figure 1 的 histogram fit 是动机，不是因果证明。", "只考察 Gamma 与一种 Gaussian mixture，搜索空间远未穷尽；作者在 Limitations 中明确承认缺少适用条件的完整刻画。", "高分辨率 mixture 实验缺失，模型规模和 compute 未完全等价；FID 也不衡量 mode coverage、语义一致性或社会偏差。", "论文年代较早，结论针对其 DDPM/DDIM 配置；不能直接外推到现代 latent diffusion 或不同 parameterization。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2106.07582；PDF：https://arxiv.org/pdf/2106.07582。", "全文 PDF 共 12 页，SHA-256：51b136b3ff13ad0242001ab623f3cec775fc5ba2ad12de95bd940a3ed477d329。", "复现需固定 backbone、variance schedule、训练步数、数据预处理与 FID 实现；每个 noise family 使用相同 seed 集，并同时报告少步/长步采样曲线。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Figure 1，把 empirical residual fit 当作提出假设；再读 Gamma 可加性与 reverse update 推导。", "随后核对 Tables 2–3，区分 DDPM、DDIM、步数和数据集，不要只摘最优单元格。", "最后读 Limitations；这篇文章提出“噪声族是设计变量”，但没有完成噪声选择理论。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2106.07582/figure-2-generated-faces.webp", "label": "Figure 2", "visual_type": "comparison", "evidence": "paper.pdf p. 9, Figure 2", "alt_text": "同一初始噪声下 Gaussian、Gaussian mixture 与 Gamma 扩散生成的人脸。", "caption": "三行分别对应单 Gaussian、Gaussian mixture 与 Gamma noise，均使用 100 个 reverse steps。", "selection_rationale": "这是论文最直观的生成对照；固定初始噪声后能直接比较三种 forward noise family，且比 FID 数据表更适合作为视觉封面。"},
        "figure_refs": [{"label": "Figure 2", "asset_path": "assets/collection-figures/2106.07582/figure-2-generated-faces.webp", "section": "核心结果与证据", "role": "compare samples under three forward-noise families", "evidence": "paper.pdf p. 9, Figure 2", "alt_text": "三种噪声分布的 CelebA 生成比较。", "caption": "固定初始噪声隔离 noise family 对生成轨迹的影响。", "interpretation": "The visual comparison supports a difference in sample quality but does not alone establish coverage or likelihood."}],
        "equation_refs": [{"label": "Centered Gamma noise", "latex": r"\bar g_t=\frac{g_t-k_t\theta_t}{\sqrt{k_t}\theta_t},\qquad g_t\sim\Gamma(k_t,\theta_t)", "role": "construct zero-mean unit-variance non-Gaussian diffusion noise", "symbols": {"g_t": "Gamma random variable", "k_t": "shape", "theta_t": "scale", "bar_g_t": "standardized noise"}, "evidence": "paper.pdf Gamma diffusion section", "interpretation": "Gamma additivity preserves tractable time marginals while changing higher moments."}],
        "evidence_refs": ["paper.pdf pp. 2–6: residual motivation and Gamma/mixture construction", "paper.pdf pp. 7–9: speech and image metrics plus Figure 2", "paper.pdf pp. 9–10: limitations and conclusions", "source PDF SHA-256 51b136b3ff13ad0242001ab623f3cec775fc5ba2ad12de95bd940a3ed477d329", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2111.04470", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2111.04470",
        "title_en": "Self-organized quantization and oscillations on continuous fixed-energy sandpiles",
        "title_zh": "连续固定能量沙堆中的自组织量子化与振荡",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "numerical",
        "style_reference": "physicist_daily_arxiv", "provenance": provenance("3679f3a96b77ee04", "Statistical Physics"),
        "verified_metadata": meta("2111.04470", "v2", "Self-organized quantization and oscillations on continuous fixed-energy sandpiles", ["Jakob Niehues", "Gorm Gruner Jensen", "Jan O. Haerter"], ["cond-mat.stat-mech", "nlin.AO", "nlin.PS", "physics.comp-ph"], "cond-mat.stat-mech", "2021-11-04T12:28:11Z", "A deterministic continuous-energy sandpile develops checkerboard period-two attractors and sharply quantized energy levels."),
        "sections": [
            sec("作者信息", "作者：Jakob Niehues、Gorm Gruner Jensen、Jan O. Haerter；arXiv:2111.04470v2，主分类 cond-mat.stat-mech。", "本卡核对 24 页全文。模型在一维 ring 与二维 periodic square lattice 上同步更新，并扫描平均能量与噪声。"),
            sec("研究问题", "固定能量沙堆通常用离散颗粒和 Abelian toppling 研究吸收态转变。这里每站点能量连续、同步 toppling 且转移量等于该站点当前能量，因此动力学非 Abelian、确定且最终进入 limit cycle。", r"论文问：随守恒平均能量 \(\mu\) 改变，吸收、棋盘 period-two、长周期复杂相与高能扩散态如何组织？连续初值为何会自发收缩成少数尖锐能级？"),
            sec("背景", "每个时间步，能量超过单位阈值的站点把全部能量均分给最近邻；总能量守恒。低 μ 时活动熄灭，高 μ 时所有站点几乎同步 toppling，更新接近离散扩散。", "中间区间的 bipartite lattice 允许两个子格交替活跃，形成空间和时间反相关的 checkerboard。非 Abelian 性意味着吸引子依赖同步更新与初值，而不只依赖总能量。"),
            sec("模型与方法", r"二维协调数 \(k=4\) 时，更新可写成 \(z_i(t+1)=z_i(t)[1-\Theta(z_i-1)]+\sum_{j\in\mathcal N_i}z_j(t)\Theta(z_j-1)/k\)。", r"order parameters 包括活动密度 \(a(t)=N^{-1}\sum_i\Theta(z_i-1)\)、空间方差 \(\sigma\)、极限环周期 \(T\) 与单站点能量 density of states。", "作者对一维 N=1997 与二维多种 L 扫描 μ，从随机连续初值迭代到周期轨道；再加入噪声检验能级尖峰和相边界鲁棒性。"),
            sec("核心结果与证据", "Figure 1 用 6×6 格点直观显示三类吸引子：静止、交替棋盘 period-two 和更复杂 period-three；它比相图先给出序参量背后的真实时空结构。", r"一维与二维相图都显示低能吸收、高能近扩散和中间振荡区。二维大范围由 checkerboard-like \(T=2\) 域占据，但被 frustrated furrows 和长周期窗口穿插。", r"能量连续并未产生平滑 density of states；极限环中出现少数尖锐能级，最高能量常受 \(2\mu\) 附近约束。相边界在 \(\sigma\) 或其对 μ 的导数中表现为不连续跳变。", "Figure 7 表明弱噪声可模糊细节，但 checkerboard 结构和主要能级仍可辨认；这支持吸引子组织的鲁棒性，而非精确微观周期不变。"),
            sec("有效性与局限", "模型是同步、确定、周期边界的理想系统；随机 sequential updates 会改变非 Abelian 动力学，结论不能直接转移。", "“量子化”指稳态能量直方图的离散尖峰，不是量子力学能级；其形成来自阈值、局域守恒和周期吸引子。", "相图由有限格点、有限迭代和周期检测阈值得到；极长 transient 可能被误判，长周期窗口的 thermodynamic limit 尚未解决。", "文中将若干跳变类比一阶或高阶相变，但缺少完整有限尺寸标度和临界指数，因此普适类判断仍开放。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2111.04470；PDF：https://arxiv.org/pdf/2111.04470。", "全文 PDF 共 24 页，SHA-256：3679f3a96b77ee04de0a7c9d4cd08c4d814810dabd8c1009e4801c87443f5e65。", "复现应保存每个 μ、L、seed 的 transient length、周期、能量守恒误差、活动密度、σ 和完整能量直方图；周期检测需用多重 tolerance 并验证轨道闭合。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1，把静止、棋盘和长周期 attractor 与更新规则对应起来。", "再读 Figures 3 与 5 的一维/二维相图，分别检查有限协调数、奇偶格点和 bipartite 结构。", "最后读 Discussion；把自组织能级、噪声鲁棒性与真正的临界有限尺寸标度分成三个命题。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2111.04470/figure-1-periodic-attractors.webp", "label": "Figure 1", "visual_type": "field_map", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "连续沙堆的静止、棋盘 period-two 与 period-three 格点吸引子。", "caption": "黑白棋盘在两个时间片间互换；下排展示更复杂的三周期局域能量图样。", "selection_rationale": "该图是论文最重要的实空间可视化，优先于相图数据曲线作为封面。"},
        "figure_refs": [{"label": "Figure 1", "asset_path": "assets/collection-figures/2111.04470/figure-1-periodic-attractors.webp", "section": "核心结果与证据", "role": "show real-space periodic attractors", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "6×6 格点上的三类周期吸引子。", "caption": "棋盘子格交替是中间能量区最典型的 period-two 组织。", "interpretation": "The order-parameter phases correspond to concrete spatiotemporal attractors rather than static density patterns."}],
        "equation_refs": [
            {"label": "Synchronous toppling map", "latex": r"z_i(t+1)=z_i(t)\bigl[1-\Theta(z_i(t)-1)\bigr]+\frac1k\sum_{j\in\mathcal N_i}z_j(t)\Theta(z_j(t)-1)", "role": "define the deterministic continuous-energy redistribution", "symbols": {"z_i": "site energy", "Theta": "activity threshold", "k": "coordination number", "N_i": "nearest neighbors"}, "evidence": "paper.pdf p. 2, Eq. (2)", "interpretation": "All active sites empty synchronously and distribute their entire current energy, making the dynamics non-Abelian."},
            {"label": "Activity density", "latex": r"a(t)=\frac1N\sum_i\Theta(z_i(t)-1)", "role": "measure the fraction of active sites", "symbols": {"N": "number of lattice sites", "a": "activity density"}, "evidence": "paper.pdf p. 3, Eq. (4)", "interpretation": "Absorbing states have a=0, while checkerboard period-two states typically alternate active sublattices."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: update map, non-Abelian dynamics and attractors", "paper.pdf pp. 6–10: one- and two-dimensional phase diagrams", "paper.pdf pp. 10–12: discussion, energy-level spikes and noise", "source PDF SHA-256 3679f3a96b77ee04de0a7c9d4cd08c4d814810dabd8c1009e4801c87443f5e65", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
