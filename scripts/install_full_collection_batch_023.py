#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 023."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2602.05435", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2602.05435",
        "title_en": "Stable Velocity: A Variance Perspective on Flow Matching",
        "title_zh": "稳定速度：流匹配的方差视角",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["7cc62f0d37b6d5c2"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2602.05435", "v2", "Stable Velocity: A Variance Perspective on Flow Matching",
            ["Donglin Yang", "Yongxing Zhang", "Xin Yu", "Liang Hou", "Xin Tao", "Pengfei Wan", "Xiaojuan Qi", "Renjie Liao"],
            ["cs.CV"], "cs.CV", "2026-02-05T08:25:05Z",
            "A variance decomposition of conditional flow matching motivates unbiased multi-reference targets, regime-aware representation alignment and a finetuning-free low-variance sampler.",
        ),
        "sections": [
            sec("作者信息", r"作者：Donglin Yang、Yongxing Zhang、Xin Yu、Liang Hou、Xin Tao、Pengfei Wan、Xiaojuan Qi、Renjie Liao；arXiv:2602.05435v2。全文 37 页。论文统一分析 CFM training-target variance，并在 ImageNet-256、SD3.5、Flux、Qwen-Image 与 Wan2.2 上验证训练和采样方案。"),
            sec("研究问题", r"CFM 用单个 conditional velocity \(v_t(x_t\mid x_0)\) 作为 marginal velocity \(v_t(x_t)\) 的 Monte Carlo target；均值正确并不意味着方差小。论文问：方差沿 flow time 如何分区；怎样在不改变 global minimizer 的前提下降方差；低方差区能否支持更强语义监督和解析采样捷径？"),
            sec("背景", r"给定 \(x_t\) 时，CFM target 的随机性来自 posterior \(p_t(x_0\mid x_t)\)。靠近 data endpoint 时 posterior 通常尖锐，单个 reference 已几乎确定 velocity；靠近 pure-noise endpoint 时 posterior 多峰，不同 reference 给出相互冲突的 conditional velocities。", r"Figure 2 把这一点画成两幅局部速度场：左侧 \(t\le\xi\) 时蓝色 conditional arrow 与黑色 marginal arrow 重合；右侧 \(t>\xi\) 时多条 colored arrows 分散。图直接替代了对 posterior mixing 的冗长描述。"),
            sec("模型与方法", r"StableVM 从 data distribution 取 \(n\) 个 references，构造 mixture conditional path，并以 posterior weights 对 conditional velocities 做 self-normalized aggregation。Theorem 3.1 证明 target 无偏且与 CFM 有同一最优 velocity；Theorem 3.2 在 affine conditional field 下给出严格方差下降。", r"VA-REPA 只在低方差区激活 representation alignment，并按有效样本归一化；conditional generation 用 class-specific FIFO memory bank 缓解同类 references 稀疏。StableVS 则利用低方差区由单一 data mode 主导，把 ODE/SDE 更新化为闭式近似，无需 finetuning。"),
            sec("核心结果与证据", r"Figure 2 的物理含义是一个 time-dependent conditioning transition：低方差区仍携带关于 \(x_0\) 的语义信息，alignment 是 well posed；高方差区接近噪声，试图从 \(x_t\) 恢复唯一语义会把 irreducible posterior ambiguity 当成监督。", r"Figure 3 的 ImageNet-256 消融中，100k iterations 的 SiT-XL baseline FID 为 18.58；全时段 REPA 为 17.88；仅低方差 \([0,0.7]\) 对齐最好，而仅高方差区为 38.89，直接支持 regime-aware weighting。StableVM 的 large-\(n\) variance 主项约缩小为 \(\mathcal V_{CFM}/(n-1)\)。", r"StableVS 在 SD3.5、Flux、Qwen-Image 与 Wan2.2 的低方差区实现超过 \(2\times\) step reduction，并在相同 seed 下维持或改善 aggregate quality；它只替换 \([0,\xi]\) 内的 solver，高方差区仍沿用 base method。"),
            sec("有效性与局限", r"方差定理的严格不等式依赖 affine conditional velocity、连续性和 reference sampling assumptions；有限 \(n\) 的 self-normalized estimator 与 memory bank 会带来相关性和额外计算/显存。split \(\xi\) 随维度、VAE、path 和数据分布变化，并非普适常数。", r"采样加速集中在作者定义的低方差区，“超过 2×”不是完整 end-to-end latency 必然减半。大型 pretrained-model 结果主要是 benchmark 与精选视觉比较，不能排除 rare prompt、motion consistency 或 long-tail mode 的损失。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.05435；代码：https://github.com/linYDTHU/StableVelocity。全文 37 页，PDF SHA-256：4d40e1a56ebff4f55e9ebe8e9402de470d064469c58a39528b0697a46e502bf7。", r"复现需固定 interpolant convention、time direction、reference count \(n\)、memory-bank capacity、split \(\xi\)、VA-REPA weighting、CFG、base solver/steps、VAE、FID/GenEval/T2V-CompBench revisions、seeds 与 end-to-end latency。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2，建立 variance curve 与 posterior picture；再读 Theorems 3.1–3.2，区分 unbiasedness 和 variance reduction。随后看 Figure 3 的 alignment failure，再读 StableVS 闭式更新与 Tables 4–6，最后核对附录的 estimator assumptions。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2602.05435/figure-2-cfm-variance.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "低方差与高方差流匹配区间中 posterior concentration 和 conditional velocities 的示意。", "caption": "靠近数据时 posterior 尖锐、conditional velocity 稳定；靠近噪声时多 references 产生冲突速度。", "selection_rationale": "Figure 2 是全文最重要的机制图，优先于单一 FID 表或生成样例。"},
        "figure_refs": [figure("2602.05435", "figure-2-cfm-variance.webp", "Figure 2", 4, "explain the two variance regimes", "左图 posterior 集中且速度一致，右图 posterior 覆盖多个 references 且速度分散。", "The training target changes from informative to intrinsically ambiguous along flow time.", "The split point is distribution- and representation-dependent rather than universal.")],
        "equation_refs": [
            {"label": "StableVM target", "latex": r"\widehat v_{\rm StableVM}(x_t)=\frac{\sum_{k=1}^{n}p_t(x_t\mid x_0^k)v_t(x_t\mid x_0^k)}{\sum_{j=1}^{n}p_t(x_t\mid x_0^j)}", "role": "average conditional velocities with posterior-like weights", "symbols": {"n": "number of references", "x_0_k": "reference data samples"}, "evidence": "paper.pdf p. 3, Eq. (7)", "interpretation": "Multiple references reduce Monte Carlo fluctuations while preserving the marginal velocity in expectation."},
            {"label": "Asymptotic variance reduction", "latex": r"\mathcal V_{\rm StableVM}(t)=\frac{1}{n-1}\mathcal V_{\rm CFM}(t)+O(n^{-1})\ \text{corrections}", "role": "quantify the leading variance gain", "symbols": {"V": "trace-of-covariance target variance"}, "evidence": "paper.pdf p. 4, Eq. (10)", "interpretation": "The dominant single-reference noise is suppressed approximately inversely with reference count."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: variance regimes, StableVM and VA-REPA", "paper.pdf pp. 5–8: StableVS and large-model evaluations", "source PDF SHA-256 4d40e1a56ebff4f55e9ebe8e9402de470d064469c58a39528b0697a46e502bf7", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2602.14011", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2602.14011",
        "title_en": "KoopGen: Koopman Generator Networks for Representing and Predicting Dynamical Systems with Continuous Spectra",
        "title_zh": "KoopGen：连续谱动力系统的 Koopman 生成元网络",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["0bee563c36d224a2"], ["Machine Learning"]),
        "verified_metadata": meta(
            "2602.14011", "v1", "KoopGen: Koopman Generator Networks for Representing and Predicting Dynamical Systems with Continuous Spectra",
            ["Liangyu Su", "Jun Shu", "Rui Liu", "Deyu Meng", "Zongben Xu"], ["cs.LG"], "cs.LG", "2026-02-15T06:32:23Z",
            "A state-dependent Koopman generator with exact skew-adjoint and self-adjoint blocks separates conservative transport from dissipation in continuous-spectrum systems.",
        ),
        "sections": [
            sec("作者信息", r"作者：Liangyu Su、Jun Shu、Rui Liu、Deyu Meng、Zongben Xu；arXiv:2602.14011v1。全文 26 页。论文针对 broadband/continuous-spectrum dynamics 提出 KoopGen，并在 pendulum、Lorenz-63、Lorenz-96 与 Kuramoto–Sivashinsky systems 上测试。"),
            sec("研究问题", r"经典 finite-dimensional Koopman model 以固定矩阵 \(K\) 在线性 latent space 中推进状态，适合离散谱近似；对湍流、混沌和连续谱，固定 eigenmodes/eigenvalues 难以维持长期稳定。论文问：能否学习随 latent state 连续变化的 generator，同时严格编码 conservative 与 dissipative operator structure？"),
            sec("背景", r"Koopman semigroup 在线性 observable space 作用，generator 是其 infinitesimal derivative。任意闭算子形式上可作 Cartesian decomposition \(G=(G-G^*)/2+(G+G^*)/2\)：skew-adjoint 部分产生 unitary/oscillatory transport，self-adjoint 部分产生 contraction or amplification。", r"Figure 1 把这一物理分解嵌入网络：lifting map 得到 \(z=\Phi(x)\)，gate network 根据当前 \(z\) 混合一组 skew/self-adjoint generators；指数映射生成 state-dependent \(K(z)\)，再同时做 prediction 与 reconstruction。"),
            sec("模型与方法", r"KoopGen block 写成 \(G(z)=\widetilde G(z)+\overline G(z)\)。前者由若干 exact skew-adjoint real blocks 线性组合，编码 reversible oscillation；后者由 self-adjoint blocks 组合，编码 irreversible dissipation。gate weights 随 \(z\) 变化，因而 spectrum 沿 trajectory 连续变化。", r"结构约束通过 real block parameterization 精确满足，而不是 soft penalty。一步 latent evolution 用 matrix exponential \(K(z)=\exp G(z)\)，训练结合 multi-step prediction、reconstruction 与 regularization，并与 DeepKoopman、LRAN 等固定谱 baselines 比较。"),
            sec("核心结果与证据", r"Figure 1 的关键是把“连续谱”转译成 state-dependent operator family：固定 \(K\) 的红框不能让 spectrum 随轨迹变化；KoopGen 的绿框以 gate-dependent \(K(z(t))\) 允许局部 generator 在 phase space 中连续重排。", r"在 Lorenz-63 与 pendulum 中，learned skew/self-adjoint fields 分别追踪旋转 transport 与 contraction；Lorenz-96 和 KS 的时空图显示 KoopGen 在更长 rollout 上保持更接近真值的 coherent structures，而 fixed-spectrum baselines 更早出现 phase drift 或过度平滑。", r"作者报告四个系统上 prediction RMSE 与 reconstruction error 整体优于或接近 baselines，并强调结构约束改善长期稳定性。结果最有说服力的是 qualitative field evolution 与 operator interpretation 的一致，而不是宣称有限 generator bank 完整解析了数学意义上的连续谱。"),
            sec("有效性与局限", r"state-dependent \(K(z)\) 不再是单一 global linear Koopman operator；它是局部/非自治 operator model，解释性与经典 Koopman spectral theorem 不能直接等同。有限 generator bank 和 learned lifting 仍可能把复杂 dynamics 隐藏在 encoder/gates 中。", r"实验集中于合成或标准 PDE/ODE systems，noise、irregular sampling、parameter shift 与真实实验数据有限。长期稳定与 energy behavior 依赖训练窗口、time step、matrix exponential 数值和 self-adjoint eigenvalue constraints；没有独立 reproduction。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.14011。全文 26 页，PDF SHA-256：804f9459589a0a076c06cf4437c0e33f73a18ca96c613e4d68ec5fa595831d2f。", r"复现需固定 ODE/PDE integrator、sampling \(\Delta t\)、train/test trajectories、lifting dimension、skew/self generator counts、gate architecture、block parameterization、matrix-exponential backend、rollout horizon、normalization 与 seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，理解 lifting、gate 和 Cartesian blocks；再读 Section 2.3 的 generator decomposition 与 exact parameterization。随后用 Figure 4 检查 Lorenz local fields，再看 Figures 5–6 的 long rollout，最后回到 conclusion 区分 operator-inspired model 与严格谱识别。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2602.14011/figure-1-koopgen-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "KoopGen 从 nonlinear system 经 lifting、state-dependent generator blocks 到 latent prediction 的整体框架。", "caption": "状态依赖的 skew/self-adjoint generator 混合把可逆输运和不可逆耗散分离，并允许谱沿轨迹变化。", "selection_rationale": "Figure 1 同时呈现连续谱动机、模型结构和物理算子分解，是最重要的机制图。"},
        "figure_refs": [figure("2602.14011", "figure-1-koopgen-overview.webp", "Figure 1", 3, "summarize the state-dependent generator architecture", "上部对比固定与状态依赖 Koopman model，下部展示 gate、generator sets 与 structure-preserving blocks。", "A Cartesian decomposition is enforced exactly while the gate makes the local spectrum trajectory dependent.", "State dependence moves the model beyond a single global finite-dimensional Koopman operator.")],
        "equation_refs": [
            {"label": "Cartesian generator decomposition", "latex": r"G(z)=\widetilde G(z)+\overline G(z),\qquad \widetilde G^*=-\widetilde G,\quad \overline G^*=\overline G", "role": "separate conservative and dissipative dynamics", "symbols": {"G_tilde": "skew-adjoint generator", "G_bar": "self-adjoint generator"}, "evidence": "paper.pdf pp. 7–9, Section 2.3", "interpretation": "The two operator sectors encode oscillatory transport and contraction/amplification with exact algebraic constraints."},
            {"label": "State-dependent Koopman step", "latex": r"z(t+1)=K(z(t))z(t),\qquad K(z)=\exp(G(z))", "role": "advance latent dynamics with a local generator", "symbols": {"z": "lifted state", "K": "state-dependent propagator"}, "evidence": "paper.pdf pp. 3–5, Eqs. (2)–(4)", "interpretation": "The propagator spectrum can vary continuously along the trajectory instead of remaining globally fixed."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–9: architecture, generator decomposition and structure-preserving blocks", "paper.pdf pp. 10–15: ODE/PDE prediction and interpretability experiments", "source PDF SHA-256 804f9459589a0a076c06cf4437c0e33f73a18ca96c613e4d68ec5fa595831d2f", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2602.16763", "source_version": "v4",
        "source_pdf": "https://arxiv.org/pdf/2602.16763",
        "title_en": "When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation",
        "title_zh": "当 AI 基准进入平台期：基准饱和的系统研究",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["5631a15ca6e32d75"], ["Scaling Laws"]),
        "verified_metadata": meta(
            "2602.16763", "v4", "When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation",
            ["Mubashara Akhtar", "Anka Reuel", "Prajna Soni", "Sanchit Ahuja", "Pawan Sasanka Ammanamanchi", "Ruchit Rawal", "Vilém Zouhar", "Srishti Yadav", "Chenxi Whitehouse", "Dayeon Ki", "Jennifer Mickel", "Leshem Choshen", "Marek Šuppa", "Jan Batzner", "Jenny Chim", "Jeba Sania", "Yanan Long", "Hossein A. Rahmani", "Christina Knight", "Yiyang Nan", "Jyoutir Raj", "Yu Fan", "Shubham Singh", "Subramanyam Sahoo", "Eliya Habba", "Usman Gohar", "Siddhesh Pawar", "Robert Scholz", "Arjun Subramonian", "Jingwei Ni", "Mykel Kochenderfer", "Sanmi Koyejo", "Mrinmaya Sachan", "Stella Biderman", "Zeerak Talat", "Avijit Ghosh", "Irene Solaiman"],
            ["cs.AI"], "cs.AI", "2026-02-18T16:51:37Z",
            "Across 60 language-model benchmarks, top-model score compression is common; age and measurement scale matter more consistently than public test access.",
        ),
        "sections": [
            sec("作者信息", r"作者团队共 37 人；arXiv:2602.16763v4。全文 29 页。研究从 61 份公开 model reports 中筛出 60 个 text-based LLM benchmarks，人工标注 14 类属性，并对 top-performing model scores 的压缩程度建立 saturation index。"),
            sec("研究问题", r"benchmark score 接近上限时，数值仍上涨却难以区分 frontier models，类似测量仪器进入动态范围边缘。论文问：如何把 score ceiling 与 top-model compression 合成可比较的 saturation measure；饱和是否由 public exposure、语言、人工策划、response format、年龄或 templating 驱动？"),
            sec("背景", r"作者把 benchmark saturation 区分为 ceiling proximity 与 discrimination loss：平均分高不一定饱和，关键还在 top \(k\) 模型之间的 spread 是否相对可用分数范围塌缩。saturation index 将两者组合并在 \([0,1]\) 上分档。", r"Figure 1 按 index 排列 60 个 benchmarks：左侧红色点形成高饱和平台，右侧蓝色点接近零。图像直观显示评价生态不是统一“都饱和”，而是跨越完整动态范围。"),
            sec("模型与方法", r"样本含 56 public 与 4 private benchmarks、44 English-only 与 16 multilingual、28 closed-ended 与 31 open-ended、14 templated 与 46 non-templated。作者收集各 benchmark 的 top scores、release age、test size、citations、access 和 curation attributes。", r"分析包括 Mann–Whitney/age-balanced group comparisons、Spearman correlations 与 joint regressions。由于 age 与 adoption 同时影响 exposure，作者把 H1/H5/H6 的 age-balanced comparisons 与 H2–H4 的 age-confounded descriptive comparisons 分开。"),
            sec("核心结果与证据", r"Figure 1 显示 60 个 benchmarks 中 29 个为 high/very-high saturation（\(S_{index}\ge0.7\)），其中 14 个超过 0.9。大 test set 通常对应更低 saturation，支持 measurement resolution 影响 top-model discrimination。", r"年龄趋势方向上存在但不强：近 24 个月发布的 benchmarks 中 42.9% 饱和，超过 60 个月为 54.5%；相应 mean index 为 0.51、0.52、0.60，传统显著性阈值下不稳健。citation/adoption 与 saturation 也相关，但与 age 共线。", r"age-balanced 分析中，expert/curated benchmarks 更抗饱和；public vs private test access 没有可靠差异。English-only、closed-ended 等表面差异多被 maturity 混杂，不能简单推断“公开测试导致饱和”。"),
            sec("有效性与局限", r"只有 4 个 private benchmarks，H1 的统计功效很低；模型报告偏向常用 benchmark，选择机制本身与 saturation/adoption 相关。top scores 来自不同 model families、prompting、few-shot 和时间点，未必完全可比。", r"index 的 \(k\)、ceiling 和权重 \(\alpha\) 虽做 sensitivity analysis，仍是 operational definition；score compression 也可能代表任务真正解决，而不全是 contamination。观察性相关不能把 age、citation、public access 或 curation 解释成因果效应。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.16763；项目页：https://evalevalai.com/。全文 29 页，PDF SHA-256：49047bd3bb498699d0b4374684dddc5d291c967e605e4e07772acfaa8c6d1caf。", r"复现需冻结 61 reports、60-benchmark inclusion list、top-score extraction、score normalization/ceiling、\(k,\alpha\)、release/citation snapshot、annotation rubric、age bins、multiple-testing policy 与 regression specification。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，建立 saturation distribution；再读 Section 2 的 index，检查 \(k\) 与 \(\alpha\) sensitivity。随后看 Figure 2 的 age-balanced 分组和 Figures 3–4 的 age/citation trends，最后读 limitations，避免把无显著差异说成“证明 public access 无影响”。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2602.16763/figure-1-saturation-index.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 5, Figure 1", "alt_text": "60 个语言模型 benchmarks 按 saturation index 从高到低排列的彩色散点图。", "caption": "60 个基准横跨完整饱和区间；29 个已进入高或极高 top-model score compression。", "selection_rationale": "论文没有机制示意图；Figure 1 是最重要的总体数据图，直接展示研究对象的分布。"},
        "figure_refs": [figure("2602.16763", "figure-1-saturation-index.webp", "Figure 1", 5, "show the empirical distribution of benchmark saturation", "Benchmarks are ranked from near-total top-score compression to low saturation.", "Nearly half of the sampled benchmarks lie in the high or very-high bins.", "The ranking is conditional on the operational index and heterogeneous score records.")],
        "equation_refs": [
            {"label": "Saturation index", "latex": r"S_{\rm index}=\alpha S_{\rm ceiling}+(1-\alpha)S_{\rm compression}", "role": "combine proximity to the score ceiling with frontier-model compression", "symbols": {"alpha": "component weight", "S_compression": "normalized lack of spread among top models"}, "evidence": "paper.pdf pp. 3–4, Section 2", "interpretation": "A benchmark is called saturated when high scores are also unable to resolve differences among leading systems."},
            {"label": "Top-model spread", "latex": r"\Delta_k=\max_{i\le k}s_i-\min_{i\le k}s_i", "role": "measure discrimination among the top k models", "symbols": {"s_i": "normalized model score", "k": "frontier subset size"}, "evidence": "paper.pdf pp. 3–4, saturation metric", "interpretation": "Small spread indicates that score resolution at the frontier has collapsed, subject to score comparability."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: saturation index, sensitivity and benchmark sample", "paper.pdf pp. 5–8: prevalence, age-balanced comparisons and regressions", "source PDF SHA-256 49047bd3bb498699d0b4374684dddc5d291c967e605e4e07772acfaa8c6d1caf", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2602.19461", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2602.19461",
        "title_en": "Laplacian Multi-scale Flow Matching for Generative Modeling",
        "title_zh": "用于生成建模的拉普拉斯多尺度流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["e081dffe139abbb4"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2602.19461", "v1", "Laplacian Multi-scale Flow Matching for Generative Modeling",
            ["Zelin Zhao", "Petr Molodyk", "Haotian Xue", "Yongxin Chen"], ["cs.CV", "cs.LG"], "cs.CV", "2026-02-23T03:09:56Z",
            "LapFlow generates Laplacian-pyramid residuals with a causally coupled mixture-of-transformers, allocating flow time from coarse to fine scales.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zelin Zhao、Petr Molodyk、Haotian Xue、Yongxin Chen；arXiv:2602.19461v1。全文 21 页。论文提出 LapFlow，在 CelebA-HQ 256–1024 与 ImageNet-256 上比较 single-scale 和 cascaded multi-scale flow models。"),
            sec("研究问题", r"高分辨率 flow matching 在完整 latent grid 上从头到尾更新所有频率，attention cost 随 token 数快速增长；cascaded pyramids 又需要每尺度独立模型和 re-noising bridge。论文问：能否在一个共享模型里并行表示多尺度 Laplacian residuals，但沿 flow time 维持 coarse-to-fine 因果依赖？"),
            sec("背景", r"Laplacian pyramid 将图像写成最粗 low-pass component 与逐层 band-pass residuals；重建是上采样粗尺度再加 residual。自然图像的 global geometry 主要在低频，纹理和边缘在高频，因此 flow time 可按尺度贡献分段。", r"Figure 1 从 \(t=0\) 到 1 展示三尺度 schedule：先只去噪最粗层，到 \(T_2\) 后加入中尺度，到 \(T_1\) 后加入最细 residual，最后层级重建。图直接表达了模型的 causal information flow。"),
            sec("模型与方法", r"LapFlow 用 multi-scale Mixture-of-Transformers：各尺度有独立 Q/K/V projections 与 scale expert，global attention weights 共享；causal mask 只允许 fine scale 读取已稳定的 coarse states。多个 residual fields 由同一 \(V_\theta\) 并行预测。", r"training/sampling 将 \([0,1]\) 分成 scale-specific segments，并对各尺度使用 modified noise schedule；较细尺度在其 activation time 前保持 noise。与 cascades 不同，尺度间不做显式 re-noising 或独立 bridge model。"),
            sec("核心结果与证据", r"Figure 1 的核心是 time–scale light cone：粗尺度先形成全局结构，之后的细尺度只能在已完成 coarse image 条件下补 residual；这避免高频路径反向扰动尚未稳定的低频 geometry。", r"CelebA-HQ 256 上 LapFlow FID 为 3.53，而文中 LFM baseline 为 5.26；模型扩展到 1024。附录 scale ablation 显示 256 分辨率用 2/3/4 scales 的 FID 分别为 3.53/3.59/5.12，说明更多尺度并非单调更好。", r"在 1024 的三尺度 temporal split 中，平衡的 \(T_1=0.67,T_2=0.33\) 最佳；过晚加入 fine scale 留下不足优化时间，过早加入则破坏 global consistency。ImageNet-256 结果也在较低 GFLOPs 下优于多项 single/multi-scale baselines，但依赖 matched implementation。"),
            sec("有效性与局限", r"Laplacian decomposition 是手工频带先验，边界、aliasing 与 VAE latent statistics 可能使 residuals 不正交；coarse-to-fine 对纹理主导或非图像数据未必最优。MoT、causal mask、noise schedule 和 training allocation 同时变化，归因需要依赖消融。", r"主要数据是 CelebA-HQ 与 ImageNet，FID 不能覆盖语义 fidelity、diversity 或 memorization。GFLOPs 与 measured inference time 受 kernel/hardware 影响；1024 结果样本/训练预算有限，尚无独立 reproduction。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.19461；代码链接见论文：https://github.com/sjtuytc/gen。全文 21 页，PDF SHA-256：2238514b8ac4722fbc832e9a91a401e06db2bc143ce48c18916c7519eea18332。", r"复现需固定 VAE、Laplacian filters/downsampling、scale count、MoT experts、shared attention、causal mask、\(T_i\)、noise schedule、CFG、ODE steps、GFLOPs convention、FID-50K implementation、resolution-specific training budget 与 seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 的时间—尺度顺序，再看 Figure 2 的 MoT 与 causal mask；随后读 Eqs. (8)–(10) 的 multi-scale path。最后对照 Tables 1–3 和附录 scale/split ablations，注意 2 scales 优于更多 scales 的负结果。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2602.19461/figure-1-multiscale-generation.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "三尺度 Laplacian pyramid 从粗到细分段去噪并层级重建图像的流程。", "caption": "LapFlow 把 flow time 分配给不同频带：先确定全局低频结构，再因果地加入中高频 residual。", "selection_rationale": "Figure 1 是全文最重要的生成机制图，优先于 FID 表和精选人脸样例。"},
        "figure_refs": [figure("2602.19461", "figure-1-multiscale-generation.webp", "Figure 1", 2, "show the coarse-to-fine temporal schedule", "Three Laplacian scales activate sequentially and reconstruct into a full-resolution sample.", "The schedule imposes a causal hierarchy from global structure to fine residuals.", "The ordering is an architectural prior whose benefit is established only on the tested image domains.")],
        "equation_refs": [
            {"label": "Laplacian reconstruction", "latex": r"x^{(s)}=\operatorname{Up}(x^{(s+1)})+r^{(s)}", "role": "reconstruct a finer scale from coarse image and residual", "symbols": {"r_s": "Laplacian band residual", "Up": "upsampling operator"}, "evidence": "paper.pdf pp. 3–4, Laplacian decomposition", "interpretation": "Each scale adds a band-limited correction to an already formed coarse image."},
            {"label": "Scale-activated flow", "latex": r"\dot x_t^{(s)}=\mathbf 1_{t\ge T_s}\,v_\theta^{(s)}(x_t^{(\ge s)},t)", "role": "encode the coarse-to-fine temporal activation", "symbols": {"T_s": "activation time for scale s", "v_theta_s": "scale-specific velocity"}, "evidence": "paper.pdf pp. 4–6, methodology", "interpretation": "Fine-scale dynamics begin only after the required coarse context has entered the causal model."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: Laplacian schedule, MoT architecture and multi-scale path", "paper.pdf pp. 7–10 and appendix: CelebA-HQ/ImageNet results and scale/split ablations", "source PDF SHA-256 2238514b8ac4722fbc832e9a91a401e06db2bc143ce48c18916c7519eea18332", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2602.24100", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2602.24100",
        "title_en": "Artificial Agency Program: Curiosity, compression, and communication in agents",
        "title_zh": "人工能动性计划：智能体中的好奇心、压缩与通信",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["f069379fcbb20834"], ["World Models"]),
        "verified_metadata": meta(
            "2602.24100", "v1", "Artificial Agency Program: Curiosity, compression, and communication in agents",
            ["Richard Csaky"], ["cs.AI", "cs.LG"], "cs.AI", "2026-02-27T15:40:31Z",
            "A position paper proposes resource-bounded embedded agents driven by learning progress, interface expansion and adaptive observation-action-deliberation budgets.",
        ),
        "sections": [
            sec("作者信息", r"作者：Richard Csaky；arXiv:2602.24100v1。全文 17 页，作者明确标为 working draft / position and research agenda。文章提出 Artificial Agency Program（AAP），主要贡献是可证伪假设、资源预算形式化和分阶段实验路线，不是已完成的 benchmark study。"),
            sec("研究问题", r"如果 AI 是嵌入现实、与人和工具耦合的 resource-bounded agent，仅最大化静态 task score 会忽略 sensing、actuation、deliberation 与 communication 的代价。AAP 问：curiosity-as-learning-progress 能否驱动 agent 扩展真正受限的接口，并在固定预算下提升 prediction、control 与 human–tool agency？"),
            sec("背景", r"AAP 把 curiosity 定义为预测压缩的进步而非 raw novelty：随机噪声不可压缩、已完全掌握的模式也无进步，只有当前能力边界附近的结构产生 intrinsic reward。agent 与环境、传感器、动作和私有通信 channel 共同构成 extended system。", r"论文无关键 Figure；Table 1 是 hypotheses/falsifiers 而非可视化图。因此按 v2.3 使用题目与经全文核验的摘要作封面，避免把装饰性合成图误当作论文证据。"),
            sec("模型与方法", r"formal setup 给 observation/action/compute interfaces 显式 capacities 与 costs，允许 agent 花预算扩展接口。intrinsic reward 比较两个时间窗口的 predictive loss，奖励 learning progress，并扣除 observation、action、deliberation 和 interface modification costs。", r"作者提出五类 hypotheses：prediction–control pragmatic alignment、boundary/interface expansion、constraint-induced predictive control、adaptive compute allocation、private self-communication。每一项在 Table 1 都配 positive evidence 与 disconfirmation path。"),
            sec("核心结果与证据", r"该文没有经验“核心结果”。它的可检验内容是：同预算下动态 observe/act/deliberate meta-controller 应优于 tuned fixed schedule；接口投资应只在 long-horizon return 增益超过成本时发生；learning-progress gains 应在相当任务区间伴随 control/empowerment gains。", r"Table 1 同时列出否证条件，例如 predictive gain 不带来 control、agent 不顾成本永久扩接口、private tokens 退化为冗长文本、meta-control 无法超过静态 schedule。把反例写进纲领是优点，但尚不能算实验支持。", r"实验路线分三阶段：可观测 ground truth 的 synthetic POMDPs；ARC-AGI-style interactive inference；以 frozen multimodal/VLA backbone 加 lightweight meta-controller 的现实测试。proof-of-concept 只描述 token budget/architecture proposal，未给出完成的 quantitative comparison。"),
            sec("有效性与局限", r"AAP 综合 intrinsic motivation、MDL、empowerment、bounded rationality 和 thermodynamics，但这些概念并不天然量纲一致；learning progress 依赖 predictor class 与 update schedule，empowerment estimation 在高维也昂贵。extended-agency gain 可能与 human autonomy、安全或可控性冲突。", r"文章是单作者 working draft，假设覆盖面很广，尚无 preregistered protocol、data、code 或统计结果。private deliberation 的可解释性、接口扩展的安全边界和能量成本测量仍开放；不能把研究纲领写成已证实的通用 agency theory。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.24100。全文 17 页，PDF SHA-256：418578f9c0d9e6ca7a577ea1dc3c45e24e4fa0d61fdb903ef3c6001c7ff45b0c。", r"真正复现需先把纲领变成 protocol：固定 POMDP latent dynamics、interface costs、prediction horizon、empowerment estimator、total token/energy budget、static/meta-control baselines、update proxy、human-interface metric、seeds 与 disconfirmation thresholds。", r"Evidence status: full-text verified position paper; proposed experiments have not been independently executed."),
            sec("阅读指南", r"先读 abstract/Section 1，确认这是 research program；再读 Eq. (12) 的 learning-progress-minus-cost objective 与 Section 2 的 metrics。随后直接看 Table 1 的 falsifiers，再读三阶段 testbed。最后检查 limitations，把类比、假设、实验设计和现有证据严格分开。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "The Artificial Agency Program treats AI as a reality-embedded, resource-bounded component of an extended human–tool system. It links curiosity to learning progress in predictive compression, makes observation, action, deliberation and interface changes explicitly costly, and proposes falsifiable hypotheses plus staged experiments from synthetic POMDPs to multimodal VLA meta-control.", "selection_rationale": "论文没有可作为封面的关键 Figure，唯一表格是 hypotheses/falsifiers；因此按 v2.3 使用论文题目和经全文核验的摘要生成文字封面，不伪造证据图。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Learning-progress intrinsic reward", "latex": r"r_t^{\rm LP}=L_{\rm pred}(\theta_{t-H};\tau_{t-H:t})-L_{\rm pred}(\theta_t;\tau_{t-H:t})", "role": "reward improvement in predictive compression", "symbols": {"H": "comparison horizon", "L_pred": "future-observation predictive loss"}, "evidence": "paper.pdf pp. 4–5, learning-progress definition", "interpretation": "The agent is rewarded for reducing error on a shared interaction segment, not for surprise or novelty alone."},
            {"label": "Resource-bounded objective", "latex": r"J(\pi)=\mathbb E_\pi\!\left[\sum_t r_t^{\rm LP}-\lambda_O c_t^O-\lambda_A c_t^A-\lambda_C c_t^C-\lambda_I c_t^I\right]", "role": "trade learning progress against sensing, action, compute and interface costs", "symbols": {"c_O": "observation cost", "c_A": "action cost", "c_C": "compute cost", "c_I": "interface-change cost"}, "evidence": "paper.pdf pp. 4–5, Eq. (12)", "interpretation": "Agency is operationalized as budget allocation rather than unconstrained capability maximization."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–7: embedded-agent thesis, formal costs and five hypotheses", "paper.pdf pp. 8–12: falsifiers, language bottleneck and staged testbed", "source PDF SHA-256 418578f9c0d9e6ca7a577ea1dc3c45e24e4fa0d61fdb903ef3c6001c7ff45b0c", "Evidence status: full-text verified position paper; no independent reproduction performed and proposed experiments not executed."],
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
