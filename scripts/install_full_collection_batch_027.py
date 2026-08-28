#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 027."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "hep-ph/0005122", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/hep-ph/0005122",
        "title_en": "Non-Perturbative Renormalization Flow in Quantum Field Theory and Statistical Physics",
        "title_zh": "量子场论与统计物理中的非微扰重整化流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["4051502ebe7750f5"], ["Renormalization Group"]),
        "verified_metadata": meta("hep-ph/0005122", "v1", "Non-Perturbative Renormalization Flow in Quantum Field Theory and Statistical Physics", ["J. Berges", "N. Tetradis", "C. Wetterich"], ["hep-ph", "cond-mat"], "hep-ph", "2000-05-12T14:23:47Z", "A broad review of the effective-average-action flow equation, its controlled approximations, and applications to critical phenomena, first-order transitions, thermal field theory and chiral physics."),
        "sections": [
            sec("作者信息", r"作者：J. Berges、N. Tetradis、C. Wetterich；arXiv:hep-ph/0005122v1。PDF 共 180 页。这是一篇 effective average action / functional RG 长综述，覆盖 (O(N)) scalar models、Kosterlitz–Thouless transition、polymer limit、first-order nucleation、thermal field theory 与 chiral models。"),
            sec("研究问题", r"微观作用量已知时，如何连续积掉动量尺度 (q\gtrsim k) 的涨落，同时保留低能非微扰结构？综述的核心问题是：exact flow equation 本身不近似，但实际 truncation 如何连接 bare action、fixed points、universal observables 与宏观相变？"),
            sec("背景", r"effective average action (\Gamma_k) 在 (k=\Lambda) 近似 microscopic action，在 (k\to0) 变成完整 effective action。红外 regulator (R_k) 抑制低动量涨落，使每个中间尺度的 propagator 有效有隙，并把一次性 path integral 改写为连续 initial-value problem。", r"Figure 1 展示双阱 average potential 随 (k) 降低逐步在 inner region 变平；这把 exact effective potential 的 convexity recovery 直接画成 coarse-graining flow。"),
            sec("模型与方法", r"核心方程为 (\partial_k\Gamma_k=\tfrac12\mathrm{Tr}[(\Gamma_k^{(2)}+R_k)^{-1}\partial_kR_k])。形式上它是一圈 trace，但使用 full field-dependent inverse propagator，因此包含所有 loop orders。", r"求解必须选择 ansatz，例如 derivative expansion (\Gamma_k=\int[U_k(\rho)+\tfrac12Z_k(\rho)(\partial\phi)^2+\cdots])、vertex expansion 或 large-(N) expansion。regulator/ansatz 不改变 exact equation 的目标，但 finite truncation 的结果会保留 scheme dependence，可用扩大 truncation 与比较 regulator 来估计。"),
            sec("核心结果与证据", r"三维 (O(N)) 模型中，near-critical trajectories 在 dimensionless fixed-point potential 附近形成 plateau；离开 fixed point 的 relevant direction 决定 correlation length，而落入 fixed point 的 irrelevant directions抹去 microscopic details。Figures 2–3 直接显示 potential 与 (\kappa,\lambda,\eta) 的 fixed-point plateaus。", r"Table 1 比较 derivative-expansion truncations，文中报告部分结果的截断变化低于 1%；Table 2 的 critical exponents 与高阶 perturbative/其他方法通常在约 1–5% 范围相符。这个数值范围是所列模型和 truncation 的经验表现，不是 FRG 的统一误差界。", r"应用章节进一步计算 universal equation of state、CO₂ liquid–vapor isotherms、weak first-order nucleation 与 chiral transitions。Figure 25 表明 nucleation action 与 prefactor 各自显著依赖 coarse-graining scale，只有在适用区间内组合 rate 才应近似稳定。"),
            sec("有效性与局限", r"exactness 属于 functional equation，而不是任意有限 ansatz 的答案。主要误差来自省略 operators、derivative expansion 的 momentum validity、regulator dependence、数值离散和对 bare action 的模型化。扩大 truncation 后的稳定性是误差诊断，不等于严格 remainder bound。", r"综述中的 QCD/thermal 结果多依赖 quark–meson 或 four-fermion effective models，并非从完整 QCD 无近似推出。均匀成核还要求 bubble scale 与 coarse-graining scale 分离；强 first-order 或多场情形会使 saddle-point treatment 变差。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/hep-ph/0005122。PDF 共 180 页，SHA-256：8a78c87b08670377c43655395c7f00413cffa7b4cbd1a2e018b908e9513e8354。", r"复核具体结果需固定 regulator (R_k)、dimensionless conventions、truncation order、field grid/expansion point、initial action、flow integrator、stopping criterion、critical tuning 与 observable extraction。", r"Evidence status: full-text verified review; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.14–28 的 average action、exact flow 与 truncations，再看 pp.50–69 的 (O(N)) fixed point、Figures 2–7 与 Tables 1–4。若关注一阶相变，直接转到 pp.111–126；若关注热场论和 QCD，再读后部 fermion/chiral sections，并始终区分 exact flow 与 model/truncation output。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/hep-ph-0005122/figure-1-potential-flow.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 29, Figure 1", "alt_text": "不同 RG 尺度下的一组双阱平均势曲线，内区逐渐变平。", "caption": "随着红外尺度降低，average potential 的内区趋于凸，而外区逐渐冻结。", "selection_rationale": "Figure 1 用一个可读的多曲线图直接展示 effective-average-action coarse graining 与 convexity recovery，是整篇方法最具代表性的物理图像。"},
        "figure_refs": [figure("hep-ph-0005122", "figure-1-potential-flow.webp", "Figure 1", 29, "show convexification under the RG flow", "不同 (k) 下的 average potential 曲线。", "effective potential 随 coarse graining 恢复凸性。", "The plot visualizes one scalar truncation; it does not by itself validate every later application.")],
        "equation_refs": [
            {"label": "Effective-average-action flow", "latex": r"\partial_k\Gamma_k[\phi]=\frac12\operatorname{Tr}\!\left[(\Gamma_k^{(2)}[\phi]+R_k)^{-1}\partial_kR_k\right]", "role": "evolve the coarse-grained effective action", "symbols": {"Gamma_k": "effective average action", "R_k": "infrared regulator"}, "evidence": "paper.pdf p. 21, Eq. (2.28)", "interpretation": "The full inverse propagator makes the one-trace form nonperturbative; approximation enters when Gamma_k is truncated."},
            {"label": "Leading derivative expansion", "latex": r"\Gamma_k[\phi]=\int d^dx\left\{U_k(\rho)+\frac12 Z_k(\rho)\partial_\mu\phi_a\partial_\mu\phi_a+\cdots\right\}", "role": "organize practical nonperturbative approximations", "symbols": {"rho": "O(N)-invariant field amplitude", "Z_k": "running wave-function factor"}, "evidence": "paper.pdf pp. 24–26, truncation discussion", "interpretation": "Keeping more derivative and field structures systematically enlarges the ansatz, though convergence must be checked case by case."},
        ],
        "evidence_refs": ["paper.pdf pp. 14–28: effective average action, exact flow and truncations", "paper.pdf pp. 50–69: O(N) scaling solution, exponents and equations of state", "paper.pdf p. 29, Figure 1; pp. 55–59, Figures 2–3 and Tables 1–2", "paper.pdf pp. 111–126: coarse graining and nucleation", "source PDF SHA-256 8a78c87b08670377c43655395c7f00413cffa7b4cbd1a2e018b908e9513e8354", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
    {
        "arxiv_id": "hep-th/0002034", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/hep-th/0002034",
        "title_en": "Exact Renormalization Group Equations. An Introductory Review",
        "title_zh": "精确重整化群方程：入门综述",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["615f6599bf75c065"], ["Renormalization Group"]),
        "verified_metadata": meta("hep-th/0002034", "v2", "Exact Renormalization Group Equations. An Introductory Review", ["C. Bagnuls", "C. Bervillier"], ["hep-th", "cond-mat.stat-mech"], "hep-th", "2000-02-04T11:53:17Z", "An introductory critical review of sharp- and smooth-cutoff exact RG equations for scalar fields, with emphasis on local-potential and derivative expansions, fixed points and continuum limits."),
        "sections": [
            sec("作者信息", r"作者：C. Bagnuls、C. Bervillier；arXiv:hep-th/0002034v2。PDF 共 78 页。综述限制在 scalar field，但系统比较 Wegner–Houghton、Wilson/Polchinski 与 Legendre-transformed ERGE，并集中讨论 derivative expansion。"),
            sec("研究问题", r"不同 cutoff 实现给出形式不同的 exact RG equations；它们如何编码同一 long-distance physics？更关键的是，当 functional equation 必须截断时，local potential approximation 与 higher derivative orders 能否稳定定位 fixed points、critical surfaces 和 continuum limits？"),
            sec("背景", r"一次 RG step 包含 high-mode elimination、rescaling 与 field renormalization。不同 ERGE 将这三步组织成不同 functional differential equations；exact level 的 universal physics 应一致，但有限阶 approximation 会暴露 scheme 与 normalization dependence。", r"Figure 2 用 shooting method 调节 bare mass (u_2(0))：只有临界值 (u_2^c\simeq-0.299586913) 的轨迹到达 Wilson–Fisher fixed point，偏离两侧的轨迹流向不同 phases。"),
            sec("模型与方法", r"Local potential approximation (LPA) 只保留 (S=\int[V(\phi,t)+\tfrac12(\partial\phi)^2])。对 Wilson/Polchinski form，dimensionless potential 满足 (\dot V=V''-(V')^2+(1-d/2)\phi V'+dV)；这是仍保留 nonlinear fixed-point structure 的最低阶 PDE。", r"derivative expansion 再加入 field-dependent (Z(\phi,t)(\partial\phi)^2) 及更高导数 operators。作者讨论 shooting、large-field boundary conditions、linearized eigenvalues、reparametrization invariance 与 cutoff parameters如何影响有限阶的 anomalous dimension。"),
            sec("核心结果与证据", r"LPA 已能产生 Gaussian、Wilson–Fisher 和 multicritical fixed points，以及 relevant/irrelevant eigendirections。Figure 2 的临界 shooting 和 Figures 3–5 的 RG trajectories 把 critical surface、renormalized trajectory 与 phase separation画成 coupling-space geometry。", r"不同 exact equations 在 LPA 可给相同或变换相关的结果，但加入 derivative terms 后，reparametrization invariance 可能被 truncation 破坏，导致 anomalous dimension 与 cutoff normalization 相关。选择保持该 invariance 的特定 cutoff 可减少歧义，但不是所有 scheme 都可做到。", r"综述对 derivative expansion 的收敛保持保留态度：某些 quantities/flows 显示良好稳定性，另一些出现慢收敛或 regulator sensitivity。因此 finite-order agreement 是 case-specific evidence，不应转写成普遍收敛定理。"),
            sec("有效性与局限", r"文章的强项是把 exact equation、approximation 与 continuum-limit geometry 分开，并明确批评仅凭 perturbative renormalizability 或形式 equivalence 推断非微扰控制。", r"内容限于 scalar theory，且主要反映 2000 年前后的结果。LPA 固定 kinetic term，不能可靠给出一般 anomalous dimension 或 momentum-dependent observables；higher derivative expansion 又要求 regulator smoothness、large-field boundary 和 normalization consistency。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/hep-th/0002034。PDF 共 78 页，SHA-256：59bb2fb714228ea16c74e4086ddece2949d56838834f38e8cdcbe58b7aeee6ce。", r"复核需固定 ERGE version、cutoff kernel、RG-time sign、dimensionless field convention、LPA/derivative order、large-field boundary、shooting tolerance、coupling projection 与 eigenvalue normalization。", r"Evidence status: full-text verified review; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.4–24 的 RG steps 和各类 ERGE，再读 pp.25–39 的 LPA、fixed points 与 continuum limit；Figure 2–5 位于文末图页。最后读 pp.40–49 的 derivative expansion 与 convergence discussion，把 exact scheme equivalence 和 truncated numerical behavior严格区分。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/hep-th-0002034/figure-2-critical-shooting.webp", "label": "Figure 2", "visual_type": "trajectory", "evidence": "paper.pdf p. 68, Figure 2", "alt_text": "u2–u4 平面中的临界 shooting 轨迹，只有调到 u2c 的虚线到达固定点。", "caption": "临界 bare mass 把 RG trajectory 调到 Wilson–Fisher fixed point；两侧偏差流向不同 phases。", "selection_rationale": "Figure 2 将 fixed point、critical surface、relevant tuning 与 shooting procedure 放在一张图中，是入门综述最清晰的 RG 几何示例。"},
        "figure_refs": [figure("hep-th-0002034", "figure-2-critical-shooting.webp", "Figure 2", 68, "show critical tuning in coupling space", "临界面附近的多条 shooting trajectories。", "只有临界初值到达 Wilson–Fisher fixed point。", "The diagram illustrates the LPA flow in a projected coupling plane, not the full infinite-dimensional theory space.")],
        "equation_refs": [
            {"label": "Polchinski local-potential flow", "latex": r"\dot V=V''-(V')^2+\left(1-\frac d2\right)\phi V'+dV", "role": "lowest-order functional RG approximation", "symbols": {"V": "dimensionless local potential", "t": "RG time"}, "evidence": "paper.pdf p. 26, Eq. (59)", "interpretation": "Even after dropping derivative operators, the nonlinear PDE retains non-Gaussian fixed points and critical trajectories."},
            {"label": "Derivative expansion", "latex": r"S[\phi]=\int d^dx\left[V(\phi,t)+\frac12Z(\phi,t)(\partial_\mu\phi)^2+O(\partial^4)\right]", "role": "extend LPA with momentum dependence", "symbols": {"Z": "field-dependent kinetic coefficient", "O(partial4)": "higher derivative operators"}, "evidence": "paper.pdf p. 40, derivative-expansion section", "interpretation": "Higher orders can estimate anomalous scaling but also expose regulator and reparametrization dependence."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–24: RG definitions and exact-equation variants", "paper.pdf pp. 25–39: LPA fixed points, trajectories and continuum limits", "paper.pdf pp. 40–49: derivative expansion, reparametrization and convergence", "paper.pdf p. 68, Figure 2", "source PDF SHA-256 59bb2fb714228ea16c74e4086ddece2949d56838834f38e8cdcbe58b7aeee6ce", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
    {
        "arxiv_id": "physics/0004057", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/physics/0004057",
        "title_en": "The information bottleneck method", "title_zh": "信息瓶颈方法",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["5480901a1a13d3fc"], ["Information Theory"]),
        "verified_metadata": meta("physics/0004057", "v1", "The information bottleneck method", ["Naftali Tishby", "Fernando C. Pereira", "William Bialek"], ["physics.data-an", "cond-mat.dis-nn", "cs.LG", "nlin.AO"], "physics.data-an", "2000-04-24T15:22:30Z", "The information bottleneck defines a compressed representation of X that preserves information about Y, derives self-consistent equations, and gives a convergent alternating re-estimation algorithm."),
        "sections": [
            sec("作者信息", r"作者：Naftali Tishby、Fernando C. Pereira、William Bialek；arXiv:physics/0004057v1。PDF 共 17 页。这篇方法论文提出 Information Bottleneck (IB) 变分原则；它主要是理论构造和算法推导，不是现代神经网络 benchmark。"),
            sec("研究问题", r"普通 rate–distortion theory 必须先指定 distortion function，但“哪些特征有意义”往往正是未知量。论文问：给定联合分布 (p(x,y))，能否在压缩 (X) 的同时保留关于 relevance variable (Y) 的信息，并让 distortion 从统计关系本身导出？"),
            sec("背景", r"representation (\widetilde X) 由 stochastic encoder (p(\tilde x|x)) 生成，满足 Markov chain (Y\leftarrow X\rightarrow\widetilde X)。压缩成本为 (I(X;\widetilde X))，保留的 relevance 为 (I(\widetilde X;Y)\le I(X;Y))。", r"参数 (\beta) 沿 information plane 扫描 tradeoff：(\beta=0) 将所有样本压到一个 codeword，增大 (\beta) 则允许更详细的表示。它控制分辨率，不等于监督学习中的 inverse temperature 的普遍物理含义。"),
            sec("模型与方法", r"IB 最小化 (\mathcal L=I(X;\widetilde X)-\beta I(\widetilde X;Y))。变分给 encoder 的 Gibbs form：(p(\tilde x|x)\propto p(\tilde x)e^{-\beta D_{KL}[p(y|x)\Vert p(y|\tilde x)]})。因此 KL divergence 作为 relevance-aware distortion 从目标导出，而非预先指定。", r"encoder、codeword marginal (p(\tilde x)) 与 decoder (p(y|\tilde x)) 三组 self-consistent equations 交替更新，形式上推广 Blahut–Arimoto。"),
            sec("核心结果与证据", r"Theorem 4 给出 stationary optimal-assignment equations；其关键是同时优化 soft partition 与 representatives，而不是先固定 distortion matrix。Eq. (28) 明确显示，两个 (x) 是否可合并由它们对 (Y) 的 conditional distributions 是否接近决定。", r"Theorem 5 证明每个 alternating step 都最小化同一有下界 functional，因此 iteration 收敛。functional 对三组 distributions 分别 convex，但在 product space 并非 jointly convex；所以证明不保证解唯一，也不保证从任意初始化到同一 global optimum。", r"随 (\beta) 增大，information-plane curves 可发生 bifurcation，形成逐级细分的 relevant quantizations。原文把 semantic clustering、document classification、neural coding 等列为当时正在发展的应用，但本文本身没有提供完整数据实验。"),
            sec("有效性与局限", r"理论假设联合分布 (p(x,y)) 已知或能充分估计；有限样本估计误差、连续高维变量、cardinality selection 和 large-alphabet bias 不由本篇收敛证明解决。", r"algorithmic convergence 只针对给定 finite distribution problem 的 alternating functional。非联合凸意味着 initialization dependence 和 local minima 仍可能存在；“relevant” 也完全相对于用户选择的 (Y)，不是从 (X) 单独发现客观语义。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/physics/0004057。PDF 共 17 页，SHA-256：afdbc45366b590086e34faef76ad0570885884489ed32233c8571912ef92ef47。", r"复现需给出离散/估计的 (p(x,y))、codebook cardinality、(\beta) schedule、initial encoder、zero-probability handling、KL convention、stopping tolerance 与多初始化比较。", r"Evidence status: full-text verified theory; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.8–9 的 relevance variable 与 Eq. (15)，再逐行看 pp.10–12 Theorem 4 和 Eq. (28)。然后读 pp.13–14 Theorem 5，特别注意“converges”与“不保证 uniqueness”同时成立；最后再看 information-plane bifurcation。"),
        ],
        "cover": {"mode": "title_abstract", "label": "Information bottleneck principle", "visual_type": "title_abstract", "evidence": "paper.pdf pp. 8–14, variational principle and self-consistent equations", "alt_text": "信息瓶颈方法的标题和压缩—相关信息权衡摘要。", "caption": "用最少的 I(X; X̃) 保留尽可能多的 I(X̃; Y)。", "abstract_text": "Information Bottleneck 把 relevance 定义为表示对目标变量 (Y) 保留的 mutual information，并从同一变分原则导出 KL distortion、self-consistent encoder/decoder 和交替重估算法。", "selection_rationale": "原文没有中心图或数据图；核心贡献是变分原则与 self-consistent equations，因此标题摘要比装饰性示意或公式页裁剪更忠实。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Information-bottleneck objective", "latex": r"\mathcal L[p(\tilde x|x)]=I(X;\widetilde X)-\beta I(\widetilde X;Y)", "role": "trade compression against retained relevance", "symbols": {"beta": "relevance Lagrange multiplier", "X_tilde": "compressed representation"}, "evidence": "paper.pdf p. 9, Eq. (15)", "interpretation": "A single parameter traces the Pareto tradeoff between compactness and predictive/relevant information."},
            {"label": "Self-consistent encoder", "latex": r"p(\tilde x|x)=\frac{p(\tilde x)}{Z(x,\beta)}\exp\{-\beta D_{KL}[p(y|x)\Vert p(y|\tilde x)]\}", "role": "derive relevance-aware soft assignments", "symbols": {"Z": "normalization", "D_KL": "emergent distortion"}, "evidence": "paper.pdf p. 12, Eq. (28)", "interpretation": "Inputs are grouped when they induce similar conditional distributions over the chosen relevance variable."},
        ],
        "evidence_refs": ["paper.pdf pp. 8–9: relevance variable and IB objective", "paper.pdf pp. 10–12: variational derivation and KL distortion", "paper.pdf pp. 13–14: alternating algorithm, convergence and non-uniqueness boundary", "source PDF SHA-256 afdbc45366b590086e34faef76ad0570885884489ed32233c8571912ef92ef47", "Evidence status: full-text verified theory; no independent reproduction performed."],
    },
    {
        "arxiv_id": "physics/0007070", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/physics/0007070",
        "title_en": "Predictability, complexity and learning", "title_zh": "可预测性、复杂性与学习",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["2262ca7bc224406b"], ["World Models"]),
        "verified_metadata": meta("physics/0007070", "v3", "Predictability, complexity and learning", ["William Bialek", "Ilya Nemenman", "Naftali Tishby"], ["physics.data-an", "cond-mat.dis-nn", "cond-mat.other", "cs.LG", "nlin.AO", "q-bio.OT"], "physics.data-an", "2000-07-20T00:45:11Z", "Predictive information—the mutual information between past and future—is related to the subextensive entropy and separates finite-memory, finite-parameter and nonparametric learning regimes."),
        "sections": [
            sec("作者信息", r"作者：William Bialek、Ilya Nemenman、Naftali Tishby；arXiv:physics/0007070v3。PDF 共 54 页。文章把 time-series predictability、Bayesian learning、coding 与 statistical-mechanical complexity 放入同一信息论框架。"),
            sec("研究问题", r"entropy 主要随观测长度 (T) extensive 增长，却把随机噪声也算作信息。论文问：能否定义只测量过去对未来有用信息的复杂度，并从其大 (T) divergence 区分有限记忆、有限参数学习与非参数学习？"),
            sec("背景", r"predictive information 定义为 past block 与 future block 的 mutual information。对 stationary process，把总 block entropy 写为 (S(T)=S_0T+S_1(T)) 后，extensive noise 部分在 mutual information 中抵消，留下 subextensive entropy (S_1)。", r"Figure 3 用 spin chains 展示三种行为：fixed coupling 的 (S_1) 饱和；学习一个可变 coupling 时约为 \(\tfrac12\log N\)；具有长程变化的 couplings 时出现约 (N^{1/2}) 增长。"),
            sec("模型与方法", r"作者把无限 future limit 的 (I_{pred}(T)) 与 entropy 的 subextensive part 联系起来，再对 Bayesian model classes 计算 marginal likelihood 的大样本 asymptotics。有限 (K) 个 regular parameters 用 saddle-point/Fisher-information expansion；非参数类用靠近 target model 的 density-of-models 和 smoothness prior。", r"该框架关注 data-generating distribution 的可学习结构，不指定某个 predictor 的 loss。由 data processing inequality，任何特定 representation/prediction algorithm 可提取的信息都不超过 (I_{pred})。"),
            sec("核心结果与证据", r"有限相关长度或有限阶 Markov-like 情形的 predictive information 可饱和。对 regular 的 (K)-parameter model，主 divergence 为 (I_{pred}(N)\sim(K/2)\log_2N)，系数在 parameter reparameterization 下不变并计数局部模型维数。", r"若 small-KL model density 有 essential singularity (\rho(D)\sim\exp(-B/D^\mu))，saddle point 给 (I_{pred}(N)\sim N^{\mu/(\mu+1)})。这为 smooth nonparametric learning 提供 power-law class；它依赖 prior/regularity 和 asymptotic assumptions，不是所有无限维模型的普遍指数。", r"作者进一步论证 divergent (I_{pred}) 满足若干 complexity desiderata，并联系 MDL、VC dimension、dynamical systems 与自然语言。所谓“unique complexity measure”是基于所列公理和 asymptotic divergent part 的论证，不是脱离这些条件的普适定理。"),
            sec("有效性与局限", r"主要结果假设 stationary/ergodic structure、可定义的 infinite-future limit 与有效 Bayesian averaging。finite-(N) saddle points、singular/nonidentifiable models、multiple modes、prior boundaries 和 nonstationarity 可改变 prefactor 或 scaling。", r"Figure 3 是长 spin-chain toy model；语言的 (N^{1/2}) 证据来自对早期实验/文本统计的讨论，作者也建议重新设计实验。predictive information 衡量可预测结构量，不保证存在计算可行的提取算法，也不等于因果复杂度。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/physics/0007070。PDF 共 54 页，SHA-256：f12cf158dcbe051eea5fc7beaa6238e3446f99ab99d5e725ab5a278fee0496a4。", r"复核需固定 stationarity window、block definition、log base、finite-future extrapolation、model prior、parameter regularity、KL-density estimate、entropy estimator、finite-size correction 与 fit range。", r"Evidence status: full-text verified theory and toy numerics; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.7–13 的 entropy decomposition 与 (I_{pred})，用 p.8 Figure 3 建立三类直觉。随后读 pp.14–30 的 finite-parameter derivation和 pp.29–35 的 power-law class；最后再看 complexity claims，并逐项检查其 stationarity、prior 与 asymptotic assumptions。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/physics-0007070/figure-3-subextensive-entropy.webp", "label": "Figure 3", "visual_type": "data_plot", "evidence": "paper.pdf p. 8, Figure 3", "alt_text": "subextensive entropy 随 word length 的常数、对数和平方根增长曲线。", "caption": "三种 (S_1(N)) scaling 对应有限记忆、有限参数学习和更丰富的长程/非参数结构。", "selection_rationale": "Figure 3 在一张图中展示全文最核心的常数、对数与 power-law universality classes，优先于纯定义或单一模型推导。"},
        "figure_refs": [figure("physics-0007070", "figure-3-subextensive-entropy.webp", "Figure 3", 8, "compare predictive-information scaling classes", "三类 spin-chain interaction 的 subextensive entropy curves。", "常数、半对数和平方根增长的对照。", "The plot is a toy-model illustration; the later nonparametric classification relies on additional asymptotic analysis.")],
        "equation_refs": [
            {"label": "Predictive information", "latex": r"I_{pred}(T,T')=I(X_{past};X_{future})=\left\langle\log_2\frac{P(X_{future}|X_{past})}{P(X_{future})}\right\rangle", "role": "measure information shared by past and future", "symbols": {"T": "past observation duration", "T_prime": "future duration"}, "evidence": "paper.pdf p. 8, Eq. (4)", "interpretation": "Random extensive entropy cancels, leaving only the structure useful for prediction."},
            {"label": "Finite-parameter scaling", "latex": r"I_{pred}(N)\sim S_1(N)\sim\frac K2\log_2N", "role": "count regular learnable parameters asymptotically", "symbols": {"K": "local parameter dimension", "N": "sample or block length"}, "evidence": "paper.pdf p. 17, Eq. (41)", "interpretation": "Each regular parameter contributes one-half log N bits to the leading predictive-information divergence."},
        ],
        "evidence_refs": ["paper.pdf pp. 7–13: predictive information and subextensive entropy", "paper.pdf p. 8, Figure 3", "paper.pdf pp. 14–30: finite-parameter learning asymptotics", "paper.pdf pp. 29–35: nonparametric power-law class", "source PDF SHA-256 f12cf158dcbe051eea5fc7beaa6238e3446f99ab99d5e725ab5a278fee0496a4", "Evidence status: full-text verified theory and toy numerics; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1007-jhep01-2020-172", "source_version": "version_of_record",
        "source_pdf": "https://repo.scoap3.org/records/52373/",
        "title_en": "Stochastic renormalization group and gradient flow", "title_zh": "随机重整化群与梯度流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["f1774dbbf19ceda8"], ["Renormalization Group"]),
        "verified_metadata": {"doi": "10.1007/JHEP01(2020)172", "arxiv_id": "1904.13057", "version": "v2 / version of record", "title": "Stochastic renormalization group and gradient flow", "authors": ["Andrea Carosso"], "categories": ["hep-th"], "primary_category": "hep-th", "published": "2020-01-28", "abstract": "A stochastic Markov process on field space defines a continuous functional RG transformation, relates effective-theory observables to stochastic and gradient-flowed correlators, and yields ratio formulae for anomalous dimensions.", "comment": "JHEP 01 (2020) 172; open-access version of record"},
        "sections": [
            sec("作者信息", r"作者：Andrea Carosso；JHEP 01 (2020) 172，DOI:10.1007/JHEP01(2020)172；对应 arXiv:1904.13057v2。核验的 SCOAP³ 期刊版 PDF 共 21 页，发表于 2020-01-28。"),
            sec("研究问题", r"gradient flow 会平滑高动量模，看起来像 RG blocking，但纯 deterministic flow 并不会自动定义非平凡 effective action。论文问：能否把 functional RG 写成 field space 上的 stochastic Markov process，从而获得合法 coarse graining、Monte Carlo RG equivalence 和可测的 gradient-flow ratio laws？"),
            sec("背景", r"functional RG 的 Boltzmann weight equation 可视为 Fokker–Planck equation。若其 transition probability 由 Langevin dynamics 生成，normalization、initial delta distribution 与 Chapman–Kolmogorov composition law 自动成立。", r"文章没有中心图；证据主要由 exact probability identities、(\phi^4_3) 的一圈 fixed-point check 和 large-separation correlator limits组成。"),
            sec("模型与方法", r"作者采用线性 field-space Langevin equation (\partial_t\phi_t(p)=-\omega(p)\phi_t(p)+\eta_t(p))，其中 noise cutoff 与 bare theory cutoff 匹配。transition kernel (P_t(\phi,\varphi)) 生成 effective Boltzmann distribution (e^{-S_t(\phi)}=\int D\varphi P_t(\phi,\varphi)e^{-S_0(\varphi)})。", r"Markov semigroup 给 successive RG steps；对 stochastic observables 的 noise 和 bare-field double average 等于 effective-theory expectation。随后把 (\omega=p^2) 的 deterministic part 识别为 gradient flow，并在大 operator separation 下控制 additive noise kernel。"),
            sec("核心结果与证据", r"Eq. (2.34) 建立 MCRG identity：任意 effective observable 可在 bare ensemble 上再平均 stochastic flow 得到，不需要先显式求 (S_t)。对三维 (\phi^4)，适当 rescaling 后作者在一圈近似中检查到 non-Gaussian IR fixed point；这只是 perturbative consistency check，不是非微扰数值验证。", r"effective two-point function 等于 gradient-flowed correlator 加 (A_t(x-y))。当 separation 远大于 flow radius 且 correlation length 足够大时，(A_t) Gaussian decay，故二者渐近相等；composite operators 有类似但更多 (A_t) corrections。", r"Markov scaling 与 operator insertions 给 Eq. (4.14) 的 flowed-correlator ratio，其 exponent 为 anomalous-dimension combination (\gamma_O-m\gamma_\phi)。这提出 lattice measurement route，但本文没有实际 lattice 数据。"),
            sec("有效性与局限", r"large-distance 条件是核心：短距离 additive (A_t) 项不可忽略，此时仅测 deterministic gradient flow 不足，必须模拟完整 stochastic transformation。ratio formula 还忽略受 appendix 控制的 small-step corrections，并要求接近 scaling regime。", r"线性 Langevin choice 适合文中 scalar setting；compact fields 或 local gauge symmetries通常需要保持 symmetry 的 nonlinear flow。non-Gaussian fixed point 检查只到一圈，不能证明一般 interacting theory 的 numerical efficiency 或 regulator independence。"),
            sec("复现与资源", r"期刊页：https://doi.org/10.1007/JHEP01(2020)172；开放全文：https://repo.scoap3.org/records/52373/；arXiv：https://arxiv.org/abs/1904.13057。核验期刊版 PDF SHA-256：7921b4f521f84e1b0216a21c34652dce15d0ad1a5958d25cdbd2a5476748a82e。", r"复核需固定 bare cutoff、noise covariance、drift (\omega)、RG/flow-time convention、field rescaling、operator basis、separation-to-flow-radius ratio、small-step (\epsilon) 和 perturbative order。", r"Evidence status: full-text verified version of record; no independent reproduction performed."),
            sec("阅读指南", r"先读期刊版 pp.4–9 的 Langevin/FP construction 与 Eq. (2.34)，再看 pp.10–15 的 effective action、fixed-point check 和 Eq. (3.36)。最后读 pp.16–18 的 ratio formula 与 conclusion，重点保留 large-separation、small-step 和 scalar/symmetry范围。"),
        ],
        "cover": {"mode": "title_abstract", "label": "Stochastic RG construction", "visual_type": "title_abstract", "evidence": "version-of-record PDF pp. 4–18, stochastic construction and correlator identities", "alt_text": "随机重整化群和梯度流论文的标题与方法摘要。", "caption": "Markov field-space dynamics 把 functional RG、Monte Carlo blocking 与 large-distance gradient-flow observables连接起来。", "abstract_text": "论文以 field-space Langevin process 生成 functional RG transition kernel，证明 effective observables 的 stochastic MCRG identity，并在大距离下把它们约化为更易测量的 gradient-flowed correlators。", "selection_rationale": "期刊版没有中心图或数据图，核心证据是贯穿全文的 probability identities 与 scaling equations；标题摘要比截取单个公式页更准确。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Stochastic MCRG identity", "latex": r"\langle O(\phi)\rangle_{S_t}=\left\langle\mathbb E_{\eta}[O(\phi_t[\varphi;\eta])]\right\rangle_{S_0}", "role": "compute effective observables from bare fields and RG noise", "symbols": {"S_t": "effective action", "phi_t": "Langevin-flowed field"}, "evidence": "version-of-record PDF p. 9, Eq. (2.34)", "interpretation": "The effective action need not be reconstructed before measuring its observables."},
            {"label": "Large-distance gradient-flow equivalence", "latex": r"\langle\phi(x)\phi(y)\rangle_{S_t}\longrightarrow\langle(f_t\varphi)(x)(f_t\varphi)(y)\rangle_{S_0}", "role": "replace stochastic effective correlators asymptotically", "symbols": {"f_t": "deterministic gradient-flow kernel", "A_t": "discarded short-range correction"}, "evidence": "version-of-record PDF p. 15, Eq. (3.36)", "interpretation": "The replacement is valid only when the additive noise kernel has decayed at large separation."},
        ],
        "evidence_refs": ["version-of-record PDF pp. 4–9: Langevin process, Fokker–Planck equation and MCRG identity", "version-of-record PDF pp. 10–15: effective theory, fixed-point check and gradient-flow correlators", "version-of-record PDF pp. 16–18: ratio formulae, anomalous dimensions and limitations", "SCOAP3 version-of-record PDF SHA-256 7921b4f521f84e1b0216a21c34652dce15d0ad1a5958d25cdbd2a5476748a82e", "Evidence status: full-text verified version of record; no independent reproduction performed."],
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
