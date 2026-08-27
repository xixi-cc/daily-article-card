#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 016."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2410.20587", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2410.20587",
        "title_en": "Generator Matching: Generative modeling with arbitrary Markov processes",
        "title_zh": "生成器匹配：用任意马尔可夫过程进行生成建模",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["5e379f3baa4eff3f"], ["Generative Models"]),
        "verified_metadata": meta("2410.20587", "v3", "Generator Matching: Generative modeling with arbitrary Markov processes", ["Peter Holderrieth", "Marton Havasi", "Jason Yim", "Neta Shaul", "Itai Gat", "Tommi Jaakkola", "Brian Karrer", "Ricky T. Q. Chen", "Yaron Lipman"], ["cs.LG", "cs.AI"], "cs.LG", "2024-10-27T20:47:29Z", "A modality-agnostic framework learns infinitesimal generators of arbitrary Markov processes and supports jump, superposed, and multimodal generative models."),
        "sections": [
            sec("作者信息", r"作者：Peter Holderrieth、Marton Havasi、Jason Yim、Neta Shaul、Itai Gat、Tommi Jaakkola、Brian Karrer、Ricky T. Q. Chen、Yaron Lipman；arXiv:2410.20587v3，ICLR 2025。全文 68 页。"),
            sec("研究问题", r"diffusion、flow matching 与 discrete diffusion 看似使用不同状态空间和动力学。论文问：能否把它们统一为“学习概率路径的无穷小生成器”，并在同一框架中构造 jump process、不同过程的叠加以及连续–离散多模态生成？"),
            sec("背景", r"马尔可夫过程由转移核决定；在短时间步 (h) 下，其一阶变化由 generator (L_t) 描述。给定从简单分布到数据分布的 conditional probability path，作者先构造生成单个数据点的 conditional generator，再用 posterior averaging 得到生成总体边缘分布的 marginal generator。", r"Figure 1 将状态空间、概率路径、generator matching objective 与 sampling algorithm 串成闭环，并明确框架不要求状态具有欧氏密度。"),
            sec("模型与方法", r"训练的核心恒等式是 marginal generator 对 conditional generators 的后验平均：(L_t f(x)=\mathbb E[L_t^Z f(x)\mid X_t=x])。因此可用 regression、Bregman divergence 或 cross-entropy 拟合 generator 参数，而无需求数据密度。", r"连续 flow、diffusion、jump process 与 finite-state CTMC 只对应不同的 (L_t)。若 (L_t=L_t^{(1)}+L_t^{(2)})，则可把两种合法动力学 superpose；乘积状态空间上的分量 generators 则给出严格的多模态构造。"),
            sec("核心结果与证据", r"Figure 1 是全文的操作图：从 conditional path 出发，构造 conditional generator，回归 marginal generator，再逐步采样；它解释了“统一”发生在无穷小动力学层，而不是把所有数据强行连续化。", r"CIFAR-10/ImageNet32 上，单独 jump model 的 FID 为 4.23/7.66；Euler flow 为 2.94/4.58；jump+flow superposition 改善到 2.49/3.47，mixed second-order-flow + Euler-jump 为 2.36/3.33。作者还在 joint protein sequence–structure generation 上展示多模态 generator composition。", r"这些数字支持 superposition 可互补，但 jump 单模型仍落后成熟 diffusion/flow；当前优势是设计空间与组合规律，而不是新过程已经全面胜出。"),
            sec("有效性与局限", r"generator matching 的边缘一致性依赖 conditional path、posterior parameterization 与正则条件；有限步数值积分仍带来离散误差。不同 generators 共享相同 marginal path 不表示其 sample paths、计算成本或归纳偏置相同。", r"图像实验只到 CIFAR-10/ImageNet32，且 jump sampler 目前主要用 Euler、缺少成熟的 classifier-free guidance 和高阶 solver。蛋白质评估是有限 benchmark，不能证明结构可折叠性或实验功能。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2410.20587；项目：https://generatormatching.github.io/。全文 68 页，PDF SHA-256：58211310b930bedfe81d8ccaf1ee53f815d88e535de550857881bfd3fcc3b086。", r"复现需固定 probability path、generator class、posterior network、Bregman objective、jump bins/intensity、superposition weights、ODE/jump integrator、steps、image preprocessing 与 protein benchmark protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 与 Eqs. (1)–(6)，建立 path–generator–kernel 三层关系；再读 marginalization theorem 和 Table 1，逐一把 flow、diffusion、jump、CTMC 代回。最后检查 Table 2 和蛋白实验，把统一性定理与有限规模经验优势分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2410.20587/figure-1-generator-matching.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "Generator Matching 从数据与概率路径到 conditional generator、训练目标、marginal generator 和采样器的流程图。", "caption": "Generator Matching 在 generator 层统一连续、离散与多模态马尔可夫生成过程。", "selection_rationale": "Figure 1 是全文最重要的方法机制图，优先于单一数据集的 FID 表。"},
        "figure_refs": [figure("2410.20587", "figure-1-generator-matching.webp", "Figure 1", 2, "explain the complete generator-matching construction", "Probability-path, generator-learning and sampling pipeline.", "The shared object is the infinitesimal generator, while state space and sample paths may differ.", "The diagram states a construction; numerical accuracy still depends on model and solver.")],
        "equation_refs": [
            {"label": "Generator action", "latex": r"L_t f(x)=\lim_{h\downarrow0}\frac{\mathbb E[f(X_{t+h})\mid X_t=x]-f(x)}{h}", "role": "encode infinitesimal Markov dynamics", "symbols": {"f": "test function", "L_t": "time-dependent generator"}, "evidence": "paper.pdf pp. 3–4", "interpretation": "Flows, diffusions and jumps differ through the operator acting on test functions."},
            {"label": "Marginal generator", "latex": r"L_t f(x)=\mathbb E\!\left[L_t^{Z}f(x)\mid X_t=x\right]", "role": "turn point-conditioned dynamics into data-marginal dynamics", "symbols": {"Z": "data endpoint", "X_t": "state on the probability path"}, "evidence": "paper.pdf pp. 5–6", "interpretation": "Posterior averaging is the generator analogue of the conditional-to-marginal identity used in flow matching."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–10: probability paths, generators, objectives and experiments", "paper.pdf appendices: generator characterizations and multimodal construction", "source PDF SHA-256 58211310b930bedfe81d8ccaf1ee53f815d88e535de550857881bfd3fcc3b086", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2411.17470", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2411.17470",
        "title_en": "Towards Precise Scaling Laws for Video Diffusion Transformers", "title_zh": "迈向视频扩散 Transformer 的精确缩放律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["5d02ca111b30d307"], ["Video Generation"]),
        "verified_metadata": meta("2411.17470", "v2", "Towards Precise Scaling Laws for Video Diffusion Transformers", ["Yuanyang Yin", "Yaqi Zhao", "Mingwu Zheng", "Ke Lin", "Jiarong Ou", "Rui Chen", "Victor Shea-Jay Huang", "Jiahao Wang", "Xin Tao", "Pengfei Wan", "Di Zhang", "Baoqun Yin", "Wentao Zhang", "Kun Gai"], ["cs.CV", "cs.AI", "cs.LG"], "cs.CV", "2024-11-25T18:59:04Z", "Scaling laws for video DiTs jointly predict model size, batch size, learning rate and validation loss under finite compute."),
        "sections": [
            sec("作者信息", r"作者：Yuanyang Yin、Yaqi Zhao、Mingwu Zheng、Ke Lin 等 14 人；arXiv:2411.17470v2。全文 17 页，拟合模型规模约 0.017B–0.26B，并外推/验证到 0.72B 与 1.07B。"),
            sec("研究问题", r"传统 compute-optimal scaling law 多把 optimizer hyperparameters 当作固定 nuisance variables；视频 DiT 却对 learning rate 与 batch size 非常敏感。论文问：在给定训练 tokens (T)、参数量 (N) 与 compute (C) 时，能否同时预测最优 (B,\eta,N) 和非最优模型的 loss？"),
            sec("背景", r"若不同规模模型都用固定 batch size/learning rate，测得的 validation-loss envelope 会混入 optimization error，从而错误偏向更大模型。Figure 1 的灰点是次优超参数，红点是每个规模的最优点；同一 (N) 下两者差距随训练继续显著扩大。"),
            sec("模型与方法", r"作者先在四个小模型与不同 token budgets 上网格搜索 (B,\eta)，拟合 (B_{\rm opt}=\alpha_B T^{\beta_B}N^{\gamma_B}) 和对应的 learning-rate power law；再将优化后的 loss 拟合为 (L(T,N))，并以 FLOPs constraint 求 compute-optimal (N)。", r"为处理实际 inference 约束，论文进一步拟合任意 (N,T) 的 generalized loss surface，而不只给最优 envelope。训练采用 constant learning rate；理论动机来自 mini-batch SGD 的 curvature–gradient-noise trade-off。"),
            sec("核心结果与证据", r"Figure 1 是关键诊断：0.02B、0.06B、0.13B、0.26B 四组曲线中，固定次优超参数的灰点系统性高于最佳红点，说明不优化 (B,\eta) 会污染 scaling fit。", r"在 (10^{10}) TFlops budget 下，作者用约 0.64B 模型而非 conventional law 给出的更大模型，报告相近生成性能并减少 40.1% inference cost；另一表述是约节省 39.9% parameters。0.72B/1.07B validation experiments 用于检查外推。", r"generalized law 对非最优模型也给出 loss prediction，适合部署时显式交换训练预算和推理尺寸；但它仍是同一模型族、数据与训练 recipe 内的经验标度。"),
            sec("有效性与局限", r"论文使用 constant learning rate，作者明确指出加入 decay schedule 可能改变缩放关系。规模跨度与一次 1.07B 外推有限，不能直接外推到十亿级以上不同架构、不同 VAE/tokenizer、数据质量或更长视频。", r"40.1% 是作者定义的 inference-cost proxy 下、给定 compute budget 的模型尺寸差异，不等于端到端延迟/显存必然同比下降。validation loss 与感知质量、人类偏好、运动物理一致性之间也非一一对应。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2411.17470。全文 17 页，PDF SHA-256：b412e87304d7ab17a9aa4cec816fbf2d8ac4c220fc728c73590282a7c2f8a1fd。", r"复现需固定 video tokenizer/VAE、DiT family、token definition、FLOPs accounting、constant-LR schedule、batch/LR grid、near-optimal tolerance、fit weighting、0.72B/1.07B validation runs 与 generation evaluator。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，确认 optimization confound；再读 Eqs. (10)–(14) 的 (B_{opt},\eta_{opt},N_{opt}) 拟合。随后检查 0.72B/1.07B validation 和 40.1% cost claim，最后读 limitations，尤其是 constant learning rate 与 model-family boundary。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2411.17470/figure-1-video-scaling.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "四个视频 DiT 参数规模的 validation loss 对 training tokens 曲线，灰色为固定次优超参数，红色为最优点。", "caption": "不先优化 batch size 与 learning rate，视频 DiT 的 scaling curve 会被系统性抬高。", "selection_rationale": "论文没有机制示意图；Figure 1 最直接揭示新缩放律要解决的优化混杂。"},
        "figure_refs": [figure("2411.17470", "figure-1-video-scaling.webp", "Figure 1", 2, "show hyperparameter-induced bias in scaling curves", "Validation-loss curves for four DiT sizes with optimal and suboptimal settings.", "Optimization error can masquerade as a model-size scaling effect.", "The plot covers one architecture and training recipe; it is not a universal video law.")],
        "equation_refs": [
            {"label": "Optimal batch-size law", "latex": r"B_{\rm opt}=\alpha_B T^{\beta_B}N^{\gamma_B}", "role": "predict batch size from tokens and model size", "symbols": {"T": "training tokens", "N": "parameters"}, "evidence": "paper.pdf p. 4, Eq. (10)", "interpretation": "Batch size is promoted from a fixed implementation choice to a fitted scaling variable."},
            {"label": "Compute-optimal size", "latex": r"N_{\rm opt}=1.5787\,C^{0.4146}", "role": "select model size under compute budget", "symbols": {"C": "training compute under the paper's convention"}, "evidence": "paper.pdf p. 5, Eq. (14)", "interpretation": "The coefficient and exponent are empirical for this video-DiT family and FLOPs definition."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: scaling setup, hyperparameter laws and generalized loss", "paper.pdf pp. 6–7 and appendices: extrapolation checks and limitations", "source PDF SHA-256 b412e87304d7ab17a9aa4cec816fbf2d8ac4c220fc728c73590282a7c2f8a1fd", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2411.18579", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2411.18579",
        "title_en": "Surveying the space of descriptions of a composite system with machine learning", "title_zh": "用机器学习测绘复合系统的描述空间",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["74e3573c7f5e3bec"], ["Machine Learning"]),
        "verified_metadata": meta("2411.18579", "v2", "Surveying the space of descriptions of a composite system with machine learning", ["Kieran A. Murphy", "Yujing Zhang", "Dani S. Bassett"], ["cs.IT", "cs.LG", "physics.data-an"], "cs.IT", "2024-11-27T18:24:13Z", "Neural lossy channels optimize total correlation and O-information to map continuous description spaces of composite systems."),
        "sections": [
            sec("作者信息", r"作者：Kieran A. Murphy、Yujing Zhang、Dani S. Bassett；arXiv:2411.18579v2。全文 14 页，案例包括五自旋 Ising 系统、4×4 Sudoku 与英文四字母序列。"),
            sec("研究问题", r"把复合系统分析限制在离散 subsystem，相当于每个 component 只能“全保留或全丢弃”。论文问：若允许每个 component 经过任意有损信道 (p(u_i\mid x_i))，连续的 description space 具有怎样的边界，哪些极值描述能暴露 redundancy、synergy 与组织结构？"),
            sec("背景", r"description (U=(U_1,\ldots,U_N)) 是对各分量 (X_i) 的局部随机压缩，且满足 (U_i\perp X_{j\ne i}\mid X_i)。总输入信息 (I_{in}=\sum_i I(X_i;U_i)) 固定时，可比较同一压缩预算下的 total correlation 与 O-information。", r"Figure 1 将自旋耦合图、description channel、离散 subsystem 点、随机压缩云与优化边界放在同一相图中，是全文最接近统计物理“状态空间测绘”的图。"),
            sec("模型与方法", r"每个 (p(u_i\mid x_i)) 由 neural encoder 参数化；单分量 mutual information 用 likelihood-ratio lower bound，跨分量项用 InfoNCE。损失含预算约束 (\gamma|I_{in}-\hat I_{in}|) 与待极值的信息量；需要最小化 mutual information 时使用 adversarial estimator。", r"total correlation (TC(U)) 衡量联合后熵的减少；O-information (\Omega(U)>0) 表示 redundancy 主导，(<0) 表示 synergy 主导。作者沿不同 (\hat I_{in}) 重复优化以描出边界。"),
            sec("核心结果与证据", r"Figure 1 显示五自旋系统的连续描述不只包含黑色 subsystem 点，还填充其间区域；低温时 description space 更宽，升温后整体收窄并降低 total correlation。最大 redundancy 锁定 ferromagnetic chain，最大 synergy 对应 frustrated triangle。", r"4×4 Sudoku 的约束把 (4^{16}\) 个填法压到 288 个合法 board；约 16 bits 后所有描述转为强 redundancy，而低预算 extremal descriptions 暴露 row/column/quadrant constraint。四字母序列则从自然语言统计中找到不同位置组合的 redundant/synergistic modes。", r"方法展示的是可优化的信息几何，而非唯一 coarse graining；不同目标函数会选出不同“重要结构”。"),
            sec("有效性与局限", r"InfoNCE 是 batch-dependent lower bound，adversarial minimization 还引入 min–max optimization error；神经网络找到的边界不保证全局极值。作者能对小自旋系统用密集随机描述校验，但 Sudoku 和语言空间没有同等完整的 ground truth。", r"O-information 只给 redundancy–synergy 的净平衡，不能替代完整 partial information decomposition。4-gram 与 4×4 Sudoku 是受控案例；对高维连续实验数据的样本复杂度、estimator bias 与可解释性仍待验证。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2411.18579；代码：https://github.com/kadmurphy/Descriptions。全文 14 页，PDF SHA-256：74e3573c7f5e3bec176b819afe634ff12e214d24703947a0e27a0f15e77b1b29。", r"复现需固定 system sampler、temperature/couplings、description latent dimension、(\hat I_{in}) grid、InfoNCE batch/critic、adversarial alternation、Monte Carlo evaluation 与 multi-start seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把黑点、灰云与蓝色 extremal boundary 对应到 subsystem、随机 channel 与优化 channel；再读 Eqs. (1)–(3) 的 TC、O-information、InfoNCE。最后比较 spin/Sudoku/language 三例，并始终区分 estimator bound、numerical extremum 与真实信息结构。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2411.18579/figure-1-description-space.webp", "label": "Figure 1", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "五自旋系统、局部描述信道，以及 total correlation 和 O-information 的描述空间边界。", "caption": "连续有损描述把离散 subsystem 扩展为可测绘的信息空间；极值边界挑出铁磁链与受挫三角形。", "selection_rationale": "Figure 1 同时给出概念、物理系统和主要结果，优先于单个 Sudoku 或语言案例。"},
        "figure_refs": [figure("2411.18579", "figure-1-description-space.webp", "Figure 1", 2, "visualize the continuous description space", "Spin system, local compression channels and information-theoretic phase plots.", "Extremal lossy descriptions identify interaction motifs at fixed information budget.", "Neural boundaries are numerical estimates and need not be globally optimal.")],
        "equation_refs": [
            {"label": "Total correlation of a description", "latex": r"TC(U)=\sum_{i=1}^{N}I(X_i;U_i)-I(X;U)", "role": "measure dependence retained after local compression", "symbols": {"U_i": "description of component i", "X": "full system state"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "At fixed transmitted information, higher total correlation means more shared structure survives the description."},
            {"label": "O-information", "latex": r"\Omega(U)=(N-2)I(U;X)+\sum_i\left[I(U_i;X_i)-I(U_{/i};X_{/i})\right]", "role": "separate redundancy- and synergy-dominated descriptions", "symbols": {"U_/i": "all descriptions except i", "X_/i": "all components except i"}, "evidence": "paper.pdf p. 2, Eq. (2)", "interpretation": "The sign summarizes the net balance, not a full decomposition of every informational atom."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–4: description formalism, estimators and spin/Sudoku results", "paper.pdf pp. 5–7 and supplement: language case and optimization details", "source PDF SHA-256 74e3573c7f5e3bec176b819afe634ff12e214d24703947a0e27a0f15e77b1b29", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2412.03603", "source_version": "v6", "source_pdf": "https://arxiv.org/pdf/2412.03603",
        "title_en": "HunyuanVideo: A Systematic Framework For Large Video Generative Models", "title_zh": "HunyuanVideo：大型视频生成模型的系统化框架",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["d907caff0751c3dd"], ["Video Generation"]),
        "verified_metadata": meta("2412.03603", "v6", "HunyuanVideo: A Systematic Framework For Large Video Generative Models", ["Weijie Kong", "Qi Tian", "Zijian Zhang", "Rox Min", "Zuozhuo Dai", "Jin Zhou", "Jiangfeng Xiong", "Xin Li", "Bo Wu", "Jianwei Zhang", "Kathrina Wu", "Qin Lin", "Junkun Yuan", "Yanxin Long", "Aladdin Wang", "Andong Wang", "Changlin Li", "Duojun Huang", "Fang Yang", "Hao Tan", "Hongmei Wang", "Jacob Song", "Jiawang Bai", "Jianbing Wu", "Jinbao Xue", "Joey Wang", "Kai Wang", "Mengyang Liu", "Pengyu Li", "Shuai Li", "Weiyan Wang", "Wenqing Yu", "Xinchi Deng", "Yang Li", "Yi Chen", "Yutao Cui", "Yuanbo Peng", "Zhentao Yu", "Zhiyu He", "Zhiyong Xu", "Zixiang Zhou", "Zunnan Xu", "Yangyu Tao", "Qinglin Lu", "Songtao Liu", "Dax Zhou", "Hongfa Wang", "Yong Yang", "Di Wang", "Yuhong Liu", "Jie Jiang", "Caesar Zhong"], ["cs.CV"], "cs.CV", "2024-12-03T23:52:37Z", "A 13B open video foundation model combines curated data, a 3D causal VAE, dual/single-stream DiT, progressive scaling and distributed training."),
        "sections": [
            sec("作者信息", r"HunyuanVideo Team（Weijie Kong 等 52 人）；arXiv:2412.03603v6。全文 36 页；foundation model 超过 13B parameters，公开代码与权重。"),
            sec("研究问题", r"开放视频生成与闭源系统之间的差距不仅来自 backbone，还来自数据清洗/描述、video compression、progressive scaling、并行训练与 post-training 的联合工程。论文问：能否给出一套从数据到 720p×129-frame 输出、可公开复用的大模型系统？"),
            sec("背景", r"视频 latent 同时承受高空间分辨率与长时间维。HunyuanVideo 用 3D causal VAE 压缩时空 token，再以 text-conditioned diffusion Transformer 生成；训练从低分辨率短视频逐步过渡到高分辨率长视频。", r"Figure 1 是原文未精选的多比例生成样例。它优先作为封面，因为直接展示人物、复杂场景、运动和宽高比，而不是只给训练系统框图。"),
            sec("模型与方法", r"3D causal VAE 采用 temporal causal convolution/attention 和 tiling；DiT 先用 dual-stream blocks 分别处理 text/video，再用 single-stream blocks 做联合建模，并结合 3D RoPE。文本条件由 MLLM encoder 提供，比传统 CLIP/T5 更长、更具指令语义。", r"模型通过 256px image、multi-resolution image、低分辨率短/长视频、高分辨率长视频和 SFT 逐级训练；数据 pipeline 包括去重、质量/美学/运动/文本过滤和结构化 caption。最大训练样本到 (720\times1280\times129) frames。"),
            sec("核心结果与证据", r"Figure 1 的 non-curated samples 展示竖屏/横屏构图、写实人物与高运动水体，提供比 aggregate score 更直观的能力边界；它是视觉证据，不替代 benchmark。", r"60 名专业评估者在 1,533 prompts 上比较多个系统；论文 Table 3 报告 HunyuanVideo overall satisfaction 最高，且 motion quality 优势最明显。作者还用内部 scaling experiments 在固定数据/256px 条件下选择 13B，而非无条件继续放大。", r"“开源”具体指 foundation model code/checkpoints 可获取；训练数据与完整大规模训练资源并未随之开放，exact reproduction 仍远超普通实验室资源。"),
            sec("有效性与局限", r"专业人评来自作者设计的 prompt、匿名展示和评分流程，闭源基线版本会漂移；satisfaction rate 不是物理一致性或长时因果正确性的直接测量。Figure 1 仍是有限样例，即使标为 non-curated。", r"系统依赖大规模私有数据清洗和训练基础设施；数据许可、人物/风格模仿和视频误用风险不能由开源权重消除。论文也把从低到高分辨率的 scaling property 留作 future work，13B choice 不是普适最优律。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2412.03603；代码/权重：https://github.com/Tencent-Hunyuan/HunyuanVideo。全文 36 页，PDF SHA-256：422e33cf9e96f692abadf2113ce253ba20a070f7ca883b39f0c1c79e3d157faf。", r"复现需固定 checkpoint、VAE/tile settings、MLLM text encoder、prompt template、resolution/frame count、sampler/steps/guidance、seed、SFT version、human-eval prompts 与 baseline snapshots。完整 pretraining 还需要未公开等价数据和大规模集群。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 建立输出直觉，再按 Figures 2–5 追踪 data–VAE–DiT–training system；随后读 scaling 与 progressive training sections。最后审查 Table 3 的人评协议，并把模型开放、训练可复现和社会使用边界分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2412.03603/figure-1-hunyuan-samples.webp", "label": "Figure 1", "visual_type": "simulation_snapshot", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "HunyuanVideo 生成的多比例样例，包括城市人物、数字艺术、长颈鹿与巨浪场景。", "caption": "原文 non-curated samples 直接展示 13B 模型在多宽高比、人物和高运动场景上的输出。", "selection_rationale": "按 v2.3 标准优先选最重要的可视化输出，而非数据表或系统框图。"},
        "figure_refs": [figure("2412.03603", "figure-1-hunyuan-samples.webp", "Figure 1", 1, "show representative visual capabilities", "Multi-aspect-ratio generated video frames.", "The samples expose composition, identity and motion-rich scene generation more directly than a scalar score.", "They are illustrative outputs and do not establish benchmark superiority by themselves.")],
        "equation_refs": [
            {"label": "Diffusion velocity objective", "latex": r"\mathcal L=\mathbb E_{x_0,\epsilon,t}\left\|v_\theta(x_t,t,c)-v_t\right\|_2^2", "role": "train the text-conditioned video latent denoiser", "symbols": {"x_t": "noised video latent", "c": "MLLM text condition"}, "evidence": "paper.pdf pp. 8–10", "interpretation": "The 13B Transformer learns a conditional velocity in the compressed spatiotemporal latent space."},
            {"label": "Latent token count", "latex": r"L=k_T T_t\,k_H H_h\,k_W W_w", "role": "count patchified spatiotemporal tokens", "symbols": {"k_T,k_H,k_W": "patch-grid factors", "T_t,H_h,W_w": "latent dimensions"}, "evidence": "paper.pdf p. 8", "interpretation": "Video cost grows multiplicatively across time and space, motivating VAE compression and progressive resolution training."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–12: samples, data pipeline, VAE, DiT and scaling", "paper.pdf pp. 17–21: human evaluation and inference system", "source PDF SHA-256 422e33cf9e96f692abadf2113ce253ba20a070f7ca883b39f0c1c79e3d157faf", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2412.19437", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2412.19437",
        "title_en": "DeepSeek-V3 Technical Report", "title_zh": "DeepSeek-V3 技术报告",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8355e49ff30a5fbe"], ["Scaling Laws"]),
        "verified_metadata": meta("2412.19437", "v2", "DeepSeek-V3 Technical Report", ["DeepSeek-AI"], ["cs.CL", "cs.AI"], "cs.CL", "2024-12-27T04:03:16Z", "A 671B-total, 37B-active MoE model uses MLA, DeepSeekMoE, auxiliary-loss-free balancing, MTP and FP8 training on 14.8T tokens."),
        "sections": [
            sec("作者信息", r"DeepSeek-AI；arXiv:2412.19437v2。全文 54 页。模型含 671B total parameters，每 token 激活 37B；预训练 14.8T tokens，随后 SFT 与 RL。作者列表以团队署名为主，完整成员见原文。"),
            sec("研究问题", r"稀疏 MoE 可增加总容量而不同比增加 token compute，但会遇到 KV-cache、expert imbalance、跨节点通信与低精度训练稳定性。论文问：如何在 671B 总规模上把 active compute 控制到 37B/token，并以可承受的 H800 训练预算维持性能？"),
            sec("背景", r"DeepSeek-V3 延续 MLA 与 DeepSeekMoE：前者把 attention 的 key/value 压到共享 latent，后者组合 shared experts 与 routed experts。Figure 2 把这两个结构放在同一 Transformer block 中，优先于 benchmark 雷达图，因为它解释效率来自哪里。"),
            sec("模型与方法", r"MLA 对 KV 做 low-rank joint compression，推理缓存压缩 latent 而非完整 multi-head keys/values。DeepSeekMoE 用细粒度 routed experts 与 shared experts；router 的动态 bias 做 auxiliary-loss-free load balancing，避免较大的 balance loss 干扰主目标。", r"Multi-Token Prediction 在主 next-token head 之外预测后续 token，训练后可丢弃或用于 speculative decoding。系统侧采用 FP8 mixed precision、DualPipe pipeline parallelism、跨节点受限 routing 与通信/计算重叠。"),
            sec("核心结果与证据", r"Figure 2 展示单个 block 的两个压缩：MLA 把 attention state 投到 latent KV，DeepSeekMoE 每 token 只路由少数 experts；671B/37B 的稀疏比正由此实现。", r"作者报告 pretraining 2.664M H800 GPU-hours、context extension 119K、post-training 5K，总计 2.788M；按每 GPU-hour 2 美元估算 5.576M 美元，但明确不含前期研究、消融、数据和基础设施成本。", r"报告的 chat 模型分数包括 MMLU 88.5、MMLU-Pro 75.9、GPQA 59.1；这些是指定 prompts/evaluation harness 下的自报结果。MTP 与 load-balancing strategy 另有较小模型消融，不能把完整模型所有收益单独归因于某一模块。"),
            sec("有效性与局限", r"训练成本口径只含官方最终 run，不能作为从零复现实验的总预算。大量 benchmark 可能受数据污染、prompt/scoring 选择和 post-training 影响；“comparable to closed-source” 会随服务版本变化。", r"MoE 的总参数、激活参数、内存占用、通信量和实际推理吞吐是不同尺度；37B active 不等于 37B dense 的相同延迟。技术报告公开 checkpoints，但训练数据只做类别性描述，无法 exact data-level reproduction。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2412.19437；代码/模型：https://github.com/deepseek-ai/DeepSeek-V3。全文 54 页，PDF SHA-256：812a3fd645c80725354de9d831a6785503007a60681461407f64e97305fa9330。", r"复现/评估需固定 checkpoint variant、tokenizer、precision、expert parallel topology、MLA cache convention、router bias update、MTP depth、prompt templates、sampling parameters 与 benchmark commits。完整 pretraining 数据不可获得。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2，分清 MLA 与 DeepSeekMoE；再读 Sections 2.1–2.2 的 routing、load balance 与 MTP。随后读 training infrastructure/FP8 和 Table 1 成本口径，最后审查 benchmark 表与 limitations，避免把 active parameters、总参数和实际服务成本混为一谈。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2412.19437/figure-2-deepseek-architecture.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 7, Figure 2", "alt_text": "DeepSeek-V3 Transformer block 中的 Multi-Head Latent Attention 与 DeepSeekMoE routed/shared expert 结构。", "caption": "MLA 压缩 KV state，DeepSeekMoE 稀疏激活 experts；二者共同决定 671B 总参数、37B 每 token 激活的效率结构。", "selection_rationale": "Figure 2 是最重要的架构机制图，优先于 benchmark 数据图。"},
        "figure_refs": [figure("2412.19437", "figure-2-deepseek-architecture.webp", "Figure 2", 7, "explain the model's sparse and latent-attention architecture", "MLA and DeepSeekMoE blocks in DeepSeek-V3.", "Inference efficiency comes from compressed KV state and sparse expert activation rather than total parameter count alone.", "The schematic omits communication topology and end-to-end serving overhead.")],
        "equation_refs": [
            {"label": "MoE routed output", "latex": r"h'_t=u_t+\sum_{i=1}^{N_s}\operatorname{FFN}^{(s)}_i(u_t)+\sum_{i=1}^{N_r}g_{i,t}\operatorname{FFN}^{(r)}_i(u_t)", "role": "combine shared and sparsely routed experts", "symbols": {"N_s": "shared experts", "N_r": "routed experts", "g_i,t": "routing weight"}, "evidence": "paper.pdf p. 8", "interpretation": "Only selected routed experts execute for a token while shared experts provide common capacity."},
            {"label": "Auxiliary-loss-free routing bias", "latex": r"g_{i,t}=s_{i,t}\,\mathbf 1\!\left(i\in\operatorname{TopK}\{s_{j,t}+b_j\}\right)", "role": "balance expert load without adding a large training loss", "symbols": {"s_i,t": "affinity score", "b_j": "dynamically updated routing bias"}, "evidence": "paper.pdf pp. 8–9", "interpretation": "Bias affects expert selection while the unshifted affinity controls the expert weight, reducing interference with the language objective."},
        ],
        "evidence_refs": ["paper.pdf pp. 7–16: MLA, DeepSeekMoE, MTP, parallelism and FP8", "paper.pdf pp. 24–35: benchmark protocol, ablations and limitations", "source PDF SHA-256 812a3fd645c80725354de9d831a6785503007a60681461407f64e97305fa9330", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        (OUT / f"{card['arxiv_id']}.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"installed": [card["arxiv_id"] for card in CARDS]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
