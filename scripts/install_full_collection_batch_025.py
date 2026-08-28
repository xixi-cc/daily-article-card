#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 025."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2608.02844", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.02844",
        "title_en": "Particle-based Generalised Stochastic Optimisation",
        "title_zh": "基于粒子的广义随机优化",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["0a0b564bed928702"], ["Machine Learning"]),
        "verified_metadata": meta("2608.02844", "v1", "Particle-based Generalised Stochastic Optimisation", ["Jiechen Jackie Zhang", "O. Deniz Akyildiz"], ["stat.ML", "cs.LG", "stat.CO"], "stat.ML", "2026-08-03T19:59:47Z", "A mean-field optimiser coupled to parameter-dependent sampler particles yields momentum and higher-order Langevin variants with contraction and finite-particle bounds."),
        "sections": [
            sec("作者信息", r"作者：Jiechen Jackie Zhang、O. Deniz Akyildiz；arXiv:2608.02844v1。全文 39 页。论文把若干 persistent-particle stochastic optimisers纳入同一 mean-field framework，并给出理论、去模糊和 energy-based model 实验。"),
            sec("研究问题", r"目标梯度常写成依赖参数的期望 \(\nabla\ell(\theta)=\int F(\theta,x)\pi_\theta(dx)\)，而 \(\pi_\theta\) 只能由 MCMC 采样。论文问：能否让 optimiser 与 sampler 同时连续演化，以 persistent particles 替代每步重启内层链，并仍得到收敛和有限粒子误差？"),
            sec("背景", r"普通 stochastic gradient 假设可直接抽样无偏梯度；latent-variable likelihood、EBM 和部分 generative training 则需从当前 \(\pi_\theta\) 采样。若粒子未混合，gradient bias 与 optimisation dynamics 相互反馈。", r"Figure 2 以图像去模糊展示 particle cloud 的可解释输出：原图、blurred observation、MYPGD 与 higher-order Langevin MYPGD 的单粒子重建并排比较。"),
            sec("模型与方法", r"一般系统包含 optimiser state \(\vartheta_t\) 与 sampler state \(Z_t=(X_t,V_t)\)：optimiser drift 由粒子 law \(\nu_t\) 下的期望 \(G_{\nu_t}(\vartheta_t)\) 驱动，sampler 则由 \(\Psi_t(\vartheta_t,Z_t)\) 与 Brownian noise 演化。用 \(N\) 个独立噪声、共同 optimiser 的 interacting system 近似 \(\nu_t\)。", r"框架覆盖 PGD、proximal MYPGD、implicit diffusion，并构造 momentum MFPO 与 higher-order Langevin variants。离散实现使用 splitting/OBABO 类 scheme。"),
            sec("核心结果与证据", r"Theorem 2 在 well-posedness 与 twisted joint contractivity A3 下给出 mean-field law 到 stationary pair 的 exponential Wasserstein contraction。A3 是 optimiser–sampler 联合强单调条件，单独的 objective convexity 或 sampler dissipativity 并不足够。", r"Theorems 3–4 给出 continuous-time interacting system 的非渐近 parameter error：transient 以 \(e^{-\rho t}\) 衰减，particle interaction 项按 \(N^{-1/2}\) 缩放；time discretisation error 需另加，不能由该定理消失。", r"去模糊实验中 higher-order Langevin 方案报告更优 MSE/SSIM 和更清晰重建。EBM rings/beads/lattice 使用 \(N=10{,}000\) particles、25 independent runs，momentum method 更快达到较低 Fisher divergence；这些是特定调参下的数值结果。"),
            sec("有效性与局限", r"统一 mean-field 描述和显式 finite-particle bound 是主要理论贡献，多个采样器/优化器实例增加可迁移性。实验同时检查 image quality 与 distribution-level Fisher divergence，而非只报 objective。", r"理论依赖 global joint contractivity、uniform moment/variance bounds 与 stationary pair，深网和多峰 EBM 中可能不成立。实验规模有限，higher-order 方法有额外状态、friction 与 step-size 调参；图像更锐利不证明普遍更快或更省计算。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.02844。全文 39 页，PDF SHA-256：0a0b564bed92870219d8c0d6e26adddd88d4a9292c4b866147e44720e0b31b47。", r"复现需固定 particle count、initial law、Brownian seeds、energy/gradient estimator、friction、mass/higher-order coefficients、splitting scheme、step size、deblurring operator/noise、Fisher-divergence estimator 和 25-run aggregation。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Eqs. (3)–(4) 和 Figure 0 的 general system，再看 Theorems 2–4 的 A3–A5。随后用 Figure 2 理解粒子输出，再看 Figures 1、3–4 的 MSE/SSIM 与 EBM diagnostics；最后检查 Appendix 的 counterexample 和 discretisation assumptions。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.02844/figure-2-deblurring.webp", "label": "Figure 2", "visual_type": "comparison", "evidence": "paper.pdf p. 11, Figure 2", "alt_text": "原图、模糊图、MYPGD 与 HOL-MYPGD 重建的并排比较。", "caption": "persistent particle optimisers 的输出可直接作为重建样本比较。", "selection_rationale": "Figure 2 是最直观的可视化结果，优先于 MSE/SSIM 曲线。"},
        "figure_refs": [figure("2608.02844", "figure-2-deblurring.webp", "Figure 2", 11, "visual reconstruction comparison", "原图、模糊观测和两种 particle reconstruction。", "去模糊重建对照。", "The higher-order particle scheme produces a visibly sharper single-particle reconstruction in this setup.")],
        "equation_refs": [
            {"label": "Coupled mean-field optimiser", "latex": r"d\vartheta_t=-G_{\nu_t}(\vartheta_t)\,dt,\qquad dZ_t=\Psi_t(\vartheta_t,Z_t)\,dt+\Sigma\,dB_t", "role": "joint optimiser-sampler dynamics", "symbols": {"nu_t": "law of sampler state", "vartheta": "general optimiser state"}, "evidence": "paper.pdf pp. 4–5, Eqs. (3)–(4)", "interpretation": "The parameter and persistent sampler evolve on one coupled timescale."},
            {"label": "Finite-particle parameter bound", "latex": r"\mathbb E\Vert\vartheta_t^N-\vartheta^\star\Vert\lesssim e^{-\rho t}\,\mathcal W_2(\mu_0,\mu^\star)+C N^{-1/2}", "role": "transient plus interaction error", "symbols": {"rho": "joint contraction rate", "N": "particle count"}, "evidence": "paper.pdf pp. 8–9, Theorem 4", "interpretation": "Continuous-time error separates exponentially decaying initialization bias from Monte Carlo interaction error."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–9: mean-field system and Theorems 1–4", "paper.pdf pp. 10–13: deblurring and EBM experiments", "paper.pdf p. 11, Figure 2 and p. 12, Figure 3", "source PDF SHA-256 0a0b564bed92870219d8c0d6e26adddd88d4a9292c4b866147e44720e0b31b47", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2608.03117", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.03117",
        "title_en": "Simulation-free and finite-time diffusion model",
        "title_zh": "免模拟训练且有限时间生成的扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["befae0a92a07baa6"], ["Generative Models"]),
        "verified_metadata": meta("2608.03117", "v1", "Simulation-free and finite-time diffusion model", ["Kentaro Kaba", "Masayuki Ohzeki", "Yuki Sughiyama"], ["cs.LG"], "cs.LG", "2026-08-04T04:39:14Z", "Prescribing tractable time-dependent conditional marginals and constructing their reference process yields simulation-free training and finite-time generation."),
        "sections": [
            sec("作者信息", r"作者：Kentaro Kaba、Masayuki Ohzeki、Yuki Sughiyama；arXiv:2608.03117v1。全文 14 页。论文给出 reference diffusion 的构造框架，并在四个二维 toy distributions 上检验 Gaussian 与 Johnson’s \(S_U\) priors。"),
            sec("研究问题", r"标准 score-based model 用可解析 OU marginals 获得 simulation-free training，却只在长时间渐近到 prior；finite-time bridge 往往需要模拟参考过程。论文问：能否同时获得可直接采样的训练 pair 和严格有限时间的 data-to-prior connection？"),
            sec("背景", r"reference process 决定训练和生成，而不只是噪声 schedule。通常先写 SDE 再求 marginals；作者反过来先规定 \(\rho_t(z\mid x)\)，让 \(p_t(z)=\int\rho_t(z\mid x)\mu(dx)\) 在 \(t=0,1\) 连接 data 与 prior，再反构 realizing SDE。", r"Figure 1 把训练数据与三种生成设置并排：Gaussian prior、Johnson’s \(S_U\) prior 和 VP-SBM baseline，覆盖 Gaussian mixture、spiral、checkerboard 与 moon。"),
            sec("模型与方法", r"条件边缘必须可采样、端点正确并满足 continuity equation。给定 conditional velocity \(\bar\alpha(t,z,x)\) 和正 diffusion tensor \(\Gamma(t,z)\)，作者积分掉 \(x\) 得 marginal drift，再构造 forward reference SDE；time reversal 产生生成方向 drift。", r"simulation-free loss 用 \((X,Z_t)\) 的直接样本回归 conditional drift/score，无需轨迹模拟。Gaussian 条件用线性 mean 与 variance schedule；non-Gaussian prior 通过一族 bijections/pushforwards 构造。"),
            sec("核心结果与证据", r"框架在 \([0,1]\) 上精确匹配端点，因此 generation horizon 有限；训练 pair 来自显式 conditional marginals，因此 objective 不需模拟 reference SDE。score matching 在这里不是原始公理，而是把 data-to-prior reference process 反转后出现的回归量。", r"将 diffusion level 缩放为 \(\epsilon\Gamma\) 并取 \(\epsilon\to0\)，SDE 退化为 conditional continuity equation，objective 收敛到 conditional flow matching；这给出 stochastic diffusion 到 deterministic flow 的结构极限。", r"Figure 1 的 7,500 training points 与 7,500 generated samples 显示四类 toy distributions 在 Gaussian 和 Johnson priors 下均被重建；VP-SBM 用 \(T=10\)、100 Euler–Maruyama steps。结果是定性结构比较，没有高维数据或 likelihood/FID。"),
            sec("有效性与局限", r"优点是把 finite horizon 与 simulation-free property 归结为 conditional-family design，并允许 non-Gaussian prior。推导清楚区分 reference process、reverse process 与 learned drift。", r"数值只覆盖二维 toy data；图中质量依赖 interpolation schedule，作者也指出不良 schedule 会降低生成质量。构造要求 tractable conditional distributions/bijections 和可逆 covariance；高维图像/文本中的数值稳定性、网络规模和 compute 尚未验证。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.03117。全文 14 页，PDF SHA-256：befae0a92a07baa6f0d0b7f094fdfb94b40a652d7783e728432a202a0967f8b1。", r"复现需固定 conditional family、mean/variance schedules、prior parameters、network (3 residual blocks, width 256, SiLU)、optimizer、batch、iterations、time reversal convention、Euler–Maruyama steps、7,500-point evaluation 与 random seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section III 的 prescribed conditional construction 和 Eq. (23) loss；再看 Gaussian/non-Gaussian realizations。随后读 score reversal 与 \(\epsilon\to0\) flow limit，最后用 Figure 1 和 Appendix E 的 schedule study 检查经验边界。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.03117/figure-1-toy-samples.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 8, Figure 1", "alt_text": "四个二维训练分布与三种生成设置的样本矩阵。", "caption": "有限时间 reference process 在 Gaussian 与 non-Gaussian priors 下重建四类 toy geometry。", "selection_rationale": "Figure 1 是唯一且最重要的生成结果可视化，直接比较数据与不同 priors。"},
        "figure_refs": [figure("2608.03117", "figure-1-toy-samples.webp", "Figure 1", 8, "generated-sample geometry", "四类训练数据和三种生成样本。", "Gaussian、Johnson 与 VP-SBM 生成结果。", "The finite-time construction preserves the qualitative topology of four two-dimensional datasets under two priors.")],
        "equation_refs": [
            {"label": "Prescribed marginal family", "latex": r"p_t(z)=\int \rho_t(z\mid x)\,\mu(dx),\qquad p_0=\mu,\quad p_1=\pi", "role": "design finite-time probability path", "symbols": {"rho_t": "tractable conditional distribution", "pi": "chosen prior"}, "evidence": "paper.pdf pp. 4–5, Eq. (17)", "interpretation": "A tractable conditional family fixes the full marginal path and exact endpoints."},
            {"label": "Small-noise flow limit", "latex": r"\partial_t\rho_t(z\mid x)=-\nabla_z\!\cdot\left[\bar\alpha(t,z,x)\rho_t(z\mid x)\right]", "role": "conditional flow matching limit", "symbols": {"bar_alpha": "conditional velocity", "rho_t": "conditional path"}, "evidence": "paper.pdf p. 6, Eq. (40)", "interpretation": "When diffusion vanishes, the stochastic construction reduces to deterministic conditional transport."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–7: conditional marginals, reference SDE and reversal", "paper.pdf pp. 6–8: score/flow connections and experiments", "paper.pdf p. 8, Figure 1", "source PDF SHA-256 befae0a92a07baa6f0d0b7f094fdfb94b40a652d7783e728432a202a0967f8b1", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2608.04882", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.04882",
        "title_en": "Variational Bounds for Perceptron Learning from Structured Data",
        "title_zh": "结构化数据感知机学习的变分界",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["952ac3355f7d9e17"], ["Machine Learning"]),
        "verified_metadata": meta("2608.04882", "v1", "Variational Bounds for Perceptron Learning from Structured Data", ["Francesco Camilli", "Pierluigi Contucci", "Federica Gerace", "Emanuele Mingione"], ["cs.LG", "cond-mat.dis-nn", "math-ph", "stat.ML"], "cs.LG", "2026-08-05T14:08:08Z", "Interpolation and log-concavity yield lower and upper minimax bounds for a finite-temperature continuous-spin perceptron trained on a Gaussian mixture."),
        "sections": [
            sec("作者信息", r"作者：Francesco Camilli、Pierluigi Contucci、Federica Gerace、Emanuele Mingione；arXiv:2608.04882v1。全文 52 页。研究对象是 Gaussian-mixture structured data 上的 finite-temperature continuous-spin perceptron，覆盖 concave utilities 与 log-concave separable priors。"),
            sec("研究问题", r"结构化数据使 perceptron 的 quenched free energy 同时包含 teacher-alignment 和 sample-overlap order parameters。论文问：能否不依赖 replica 假设，给出 thermodynamic pressure 的 rigorous lower/upper variational bounds，并从同一 potential 计算 training、generalization 与 ground state？"),
            sec("背景", r"训练可写成 Gibbs measure：utility 决定样本损失，prior/regularizer 约束连续权重。高维极限 \(M/N\to\alpha\) 后，pressure 集中但 disorder average 非平凡。adaptive interpolation 可把原模型连接到 scalar channels。", r"Figure 1 画出 reduced variational potential \(\Phi_u^\star(\rho,r)\) 的六个曲面；鞍点几何直接对应 \(\sup_\rho\inf_r\) 是否能交换。"),
            sec("模型与方法", r"数据由 Gaussian mixture 生成，order parameters 包括权重 overlap、teacher alignment 和 conjugate fields。作者结合 Guerra-style interpolation、Brascamp–Lieb/log-concavity 与 concentration，构造同一 scalar potential 的嵌套 extrema。", r"Theorem 1 的 lower 与 upper bounds 只交换两个剩余参数 \(\rho,r\) 的优化顺序；其余 \(\delta,h,q,m\) extrema 由 concave–convex structure 控制。stationarity 给 fixed-point equations，pressure derivatives 给 observables。"),
            sec("核心结果与证据", r"一般情形得到 \(\sup_\rho\inf_r\Phi_u^\star\le p\le\inf_r\sup_\rho\Phi_u^\star\)。若 minimax order 可交换，两界相合，识别 limiting quenched pressure；这不是无条件 replica-symmetric exact formula。", r"同一 potential 的导数产生 training loss 与 generalization error，\(\beta\to\infty\) 给 ground-state energy。这样 thermodynamics 和 learning observables 不需另建不同 saddle systems。", r"Figure 1 对 logistic loss/L2、\(\alpha=1,3\)、\(\beta=1,100\)、\(\kappa=1,0.01\) 的 50×50 surfaces 显示 saddle geometry；Figure 2 在 smooth L1 regularization 下也观察到。数值支持这些参数区 bounds coincide，但不证明全参数唯一性。"),
            sec("有效性与局限", r"证明不依赖非严格 replica continuation，并明确指出 exactness 的 minimax-commutation 条件。log-concavity 使 overlap concentration 和 scalar reduction 可控。", r"适用范围要求 concave utility、log-concave separable prior 和 Gaussian-mixture structure；非凸深网、多层特征学习与非高斯重尾数据不在定理内。Figure 1–2 是 variational landscape numerics，不是 finite-N training benchmark；鞍点外观也不能替代唯一性证明。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.04882。全文 52 页，PDF SHA-256：952ac3355f7d9e173d380d85acf5756ce9582c955f33566ce1b317a568360531。", r"复核需固定 utility、prior/regularizer、\(\alpha,\beta,\lambda,\kappa\)、Gaussian centroid law、order-parameter domains、nested solver order、L-BFGS-B tolerances、50×50 grid 与 boundary handling。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section 2 的 model/pressure，再读 Theorem 1 并标出两个不交换的 extrema；随后核对 fixed-point 和 observable derivatives。最后看 Figures 1–2，把数值 saddle evidence 与严格 minimax equality 条件区分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.04882/figure-1-variational-surfaces.webp", "label": "Figure 1", "visual_type": "field_map", "evidence": "paper.pdf p. 26, Figure 1", "alt_text": "六组参数下 reduced variational potential 的三维曲面。", "caption": r"曲面在 \(\rho,r\) 上呈鞍点结构，对应 lower/upper minimax order 的交换。", "selection_rationale": "Figure 1 是唯一直接可视化 theorem exactness 条件的图，优先于纯公式页。"},
        "figure_refs": [figure("2608.04882", "figure-1-variational-surfaces.webp", "Figure 1", 26, "variational saddle geometry", r"不同参数下 \(\Phi_u^\star(\rho,r)\) 的六个曲面。", "reduced potential 的 saddle surfaces。", "The visible saddle structure numerically supports exchanging the two remaining extrema in the plotted regimes.")],
        "equation_refs": [
            {"label": "Minimax variational bounds", "latex": r"\sup_{\rho}\inf_r\Phi_u^\star(\rho,r)\le p\le\inf_r\sup_{\rho}\Phi_u^\star(\rho,r)", "role": "bound limiting quenched pressure", "symbols": {"p": "limiting quenched pressure", "rho,r": "remaining variational parameters"}, "evidence": "paper.pdf pp. 5–6, Theorem 1", "interpretation": "Only the order of two extrema separates the rigorous lower and upper bounds."},
            {"label": "Exactness condition", "latex": r"\sup_{\rho}\inf_r\Phi_u^\star=\inf_r\sup_{\rho}\Phi_u^\star\quad\Longrightarrow\quad p=\operatorname{extr}\Phi_u^\star", "role": "identify exact thermodynamic solution", "symbols": {"Phi_u": "reduced variational potential"}, "evidence": "paper.pdf pp. 5–7 and 25–27", "interpretation": "When minimax commutation holds, both bounds collapse to the same pressure."},
        ],
        "evidence_refs": ["paper.pdf pp. 5–9: Theorem 1 and fixed-point conditions", "paper.pdf pp. 22–27: zero-temperature/observables and Figures 1–2", "paper.pdf p. 26, Figure 1", "source PDF SHA-256 952ac3355f7d9e173d380d85acf5756ce9582c955f33566ce1b317a568360531", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2608.05027", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.05027",
        "title_en": "Scaling behavior in non-reciprocal and odd conserved dynamics near criticality",
        "title_zh": "临界附近非互易与奇守恒动力学的标度行为",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["9eddce578e9dcf52"], ["Nonreciprocal Systems"]),
        "verified_metadata": meta("2608.05027", "v1", "Scaling behavior in non-reciprocal and odd conserved dynamics near criticality", ["Martin Kjøllesdal Johnsrud", "Giulia Pisegna", "Ramin Golestanian"], ["cond-mat.soft", "cond-mat.stat-mech", "physics.bio-ph"], "cond-mat.soft", "2026-08-05T16:31:44Z", "Dynamical RG of the non-reciprocal Cahn-Hilliard model reveals distinct structural and dynamical correlation lengths and several active scaling regimes."),
        "sections": [
            sec("作者信息", r"作者：Martin Kjøllesdal Johnsrud、Giulia Pisegna、Ramin Golestanian；arXiv:2608.05027v1。全文 30 页。论文用 perturbative dynamical RG 分析 two-field conserved NRCH model 的临界标度。"),
            sec("研究问题", r"非互易 Cahn–Hilliard dynamics 同时受 temperature-like \(r\) 与 nonreciprocal coupling \(\alpha_0\) 调控。论文问：接近相分离临界点时，equal-time structure 与 response dynamics 是否仍由同一 correlation length 控制，还是 activity 产生新的 scaling exponent/regimes？"),
            sec("背景", r"平衡临界动力学中 fluctuation–dissipation relation 把结构与响应锁在同一尺度。非互易耦合破坏 parity/time reversal，可产生 traveling patterns。Figure 1 从 enzyme/active-colloid micro scale 到 density-field meso scale，再到 macro domains，标出 \(r,\alpha_0\) 如何调节 crossover length。"),
            sec("模型与方法", r"NRCH 是两个 conserved fields 的 Model-B-like Langevin equation，mobility 中含 antisymmetric/odd part，free-energy-like reciprocal sector 与 linear/nonlinear nonreciprocal couplings 并存。作者定义 equal-time correlation 的 \(\xi_s\) 和 response/dynamic correlation 的复长度 \(\xi_d\)。", r"通过 momentum-shell 与 Callan–Symanzik 两种 RG 计算 beta functions、fixed points 和 crossover scaling；\(4-d=\epsilon\) 展开给 Wilson–Fisher/OCH 与 manifestly NR fixed points。"),
            sec("核心结果与证据", r"结构长度始终按 temperature 控制：\(\xi_s\sim r^{-\nu}\)，\(\nu=1/2+\epsilon/10+O(\epsilon^2)\)。动态长度在 effective-equilibrium regime 跟随 \(\xi_s\)，但在 NR regimes 可按 \(r^{-\nu_n}\) 或 \(|\alpha_0|^{-\nu_n}\) 发散，\(\nu_n=1/2+O(\epsilon^2)\)。", r"临界点本身流向具有 odd mobility 的 conserved equilibrium-like OCH fixed point；在有限但很大的 \(\xi_d\) 尺度上，NR± fixed points 控制 broken-FDT behavior。Figure 2/3 划分 EE、\(\alpha\)NR、rNR 与 suppressed-NR regimes。", r"结果意味着 structural snapshot 可能看似 Wilson–Fisher，而 relaxation/correlation time 却由 nonreciprocity 单独调节。论文提出代谢/催化 rate 可作为 living mixtures 的 dynamical tuning parameter，但未做实验或数值格点验证。"),
            sec("有效性与局限", r"两个独立 RG formulations 的一致性和 fixed-point/crossover map 是理论优势；显式区分 \(\xi_s\) 与 \(\xi_d\) 也给实验 observable 清晰分工。", r"结论来自 \(\epsilon\)-expansion 和 perturbative two-loop analysis，作者指出 OCH fixed-point 的稳定性/更高阶修正仍需数值与 higher-loop verification。真实活性体系可能有额外 hydrodynamics、noise color、composition tuning 和 finite-size crossover。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.05027。全文 30 页，PDF SHA-256：9eddce578e9dcf5207164faa72124143561ba9734060934104b318fda90a1efb。", r"复核需固定 field normalization、noise/mobility convention、reciprocal/nonreciprocal couplings、\(d=4-\epsilon\)、renormalization scheme、beta-function truncation、fixed-point branch、matching conditions 与 complex \(\xi_d\) definition。", r"Evidence status: full-text verified RG theory; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 与 Eqs. (1)、(25)–(27) 理解两个长度；再读 Table I/Figure 2 的 scaling regimes。随后检查 OCH 与 NR± beta functions、Figure 3 RG flow，最后读 conclusion 中对 two-loop stability 和实验解释的保留。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.05027/figure-1-hierarchical-scales.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "从微观活性粒子到介观密度场和宏观相区的层级示意。", "caption": "温度与非互易耦合在不同尺度上调节结构和动力相关长度。", "selection_rationale": "Figure 1 是全文最重要的跨尺度机制图，优先于 RG regime 相图。"},
        "figure_refs": [figure("2608.05027", "figure-1-hierarchical-scales.webp", "Figure 1", 2, "multiscale physical mechanism", "微观、介观、宏观层级及调控参数。", "NRCH 的层级尺度示意。", "The diagram links microscopic nonreciprocity to separate structural and dynamical crossover scales.")],
        "equation_refs": [
            {"label": "Two correlation lengths", "latex": r"C_{ET}(x)\sim x^{-(d-1)/2}e^{-x/\xi_s},\qquad \chi_T(x)\sim x^{-(d-1)/2}e^{-x/\xi_d}", "role": "separate structure and response", "symbols": {"xi_s": "structural correlation length", "xi_d": "dynamical response length"}, "evidence": "paper.pdf pp. 4–5, Eqs. (25)–(26)", "interpretation": "Broken time reversal permits equal-time structure and dynamics to decay on different lengths."},
            {"label": "Active scaling regimes", "latex": r"\xi_s\sim r^{-\nu},\qquad \xi_d\sim\begin{cases}r^{-\nu},&\mathrm{EE}\\r^{-\nu_n}\ \mathrm{or}\ |\alpha_0|^{-\nu_n},&\mathrm{NR}\end{cases}", "role": "critical crossover scaling", "symbols": {"nu": "Wilson-Fisher exponent", "nu_n": "nonreciprocal dynamical exponent"}, "evidence": "paper.pdf pp. 2–4, Table I and Figure 2", "interpretation": "Activity changes dynamical scaling without changing the leading structural exponent."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: Figure 1, Table I and correlation-length definitions", "paper.pdf pp. 5–14: RG flows and fixed points", "paper.pdf Figures 2–4: scaling regimes and RG geometry", "source PDF SHA-256 9eddce578e9dcf5207164faa72124143561ba9734060934104b318fda90a1efb", "Evidence status: full-text verified RG theory; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2608.05251", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.05251",
        "title_en": "Nucleation beyond Equilibrium: Fronts Control Invasion in Bistable Ecosystems",
        "title_zh": "超越平衡的成核：传播前沿控制双稳生态系统入侵",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8e61789d08568052"], ["Complex Systems"]),
        "verified_metadata": meta("2608.05251", "v1", "Nucleation beyond Equilibrium: Fronts Control Invasion in Bistable Ecosystems", ["Victor Lequin", "Giulio Biroli", "Camille Scalliet"], ["cond-mat.stat-mech", "physics.bio-ph"], "cond-mat.stat-mech", "2026-08-05T16:01:35Z", "A weak-noise nucleation theory for vector reaction-diffusion systems replaces equilibrium free-energy difference and surface tension by front speed and diffusivity."),
        "sections": [
            sec("作者信息", r"作者：Victor Lequin、Giulio Biroli、Camille Scalliet；arXiv:2608.05251v1。全文 35 页。论文为 non-conserved vector reaction–diffusion systems 推导 weak-noise nucleation theory，并用 two-species Lotka–Volterra 数值 quasipotential 验证。"),
            sec("研究问题", r"经典成核理论依赖 detailed balance 和 scalar energy landscape；生态 metacommunity 通常是多组分、不可逆且无自由能。论文问：能否只用 deterministic invasion front 的 speed、curvature response 和 noise geometry，预测 critical nucleus 与 exponentially small invasion probability？"),
            sec("背景", r"bistability 给出 metastable/stable fixed points；空间耦合后，超过 critical radius 的 droplet 会扩张。Figure 1 把平衡 Ising/CNT 与非平衡 metacommunity 并排：能量差 \(\Delta\phi\) 与 surface tension \(\gamma\) 被 front speed \(c\) 与 effective diffusivity \(D\) 替代。"),
            sec("模型与方法", r"一般 stochastic reaction–diffusion equation 为 \(\partial_t\mathbf u=D\nabla^2\mathbf u+\mathbf f_{\mathbf p}(\mathbf u)+\sqrt{2T}\,\mathbf G(\mathbf u)\boldsymbol\eta\)。Freidlin–Wentzell action 定义 quasipotential \(U\) 与 minimum-action path。", r"binodal 附近 critical nucleus 是弱曲率 traveling front；curvature expansion 给 radius dynamics。spinodal 附近沿 soft eigenmode 做 universal rescaling。作者用 string/shrinking-dimer 与 geometric minimum action method 数值求 Lotka–Volterra critical nuclei/quasipotentials。"),
            sec("核心结果与证据", r"曲面 front 的总速度近似 \(c_{tot}=c-(d-1)D/R+\sqrt{2T}\,g\xi\)，因此 \(R_c=(d-1)D/c\)。这与 CNT 的 \((d-1)\gamma/\Delta\phi\) 同构，但 \(c,D\) 是非平衡动力学性质。", r"weak-noise nucleation 仍服从 \(p\asymp\exp[-U_c/T]\)。binodal 与 spinodal 两端的 asymptotic theory 均被 numerical quasipotential computations 支持；Figure 16 展示跨 bistability 区间的比较。", r"Lotka–Volterra fronts 在强 interspecific competition 下出现总丰度显著 depletion。即使 competitive advantage 固定，depletion 降低 front susceptibility/speed，使 barrier 指数增大；scalar species-frequency order parameter 看不到这一 vector structure。"),
            sec("有效性与局限", r"Figure 1 的 mapping、binodal front expansion、spinodal soft mode 与 full quasipotential numerics 构成跨极限证据。理论同时处理 state-dependent noise 与 vector order parameter。", r"核心渐近依赖 weak noise、稳定且 gapped 的 front、critical radius 大于 front width；靠近 spinodal 时 barrier 消失使 weak-noise expansion 最脆弱。prefactor、front fluctuations/renormalization、finite domain confinement 与 conserved/hydrodynamic fields 需另行处理。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.05251。全文 35 页，PDF SHA-256：8e61789d08568052cf0ad02b04e9e42b96123682f8d27e5394aa20d0cd3cf8dc。", r"复现需固定 reaction parameters \(a,b\)、diffusivity/noise matrix、domain/boundary、front solver、curvature convention、string/shrinking-dimer/GMAM images、time/space discretization、weak-noise extrapolation 与 binodal/spinodal distance. ", r"Evidence status: full-text verified theory and numerics; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 Eqs. (1)、(20)，再读 front properties 与 Eqs. (40)–(47) 的 \(R_c,U_c\)。随后读 spinodal asymptotics，再看 Lotka–Volterra Figures 9–16 的 depletion、critical nuclei 与 numerical quasipotential。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.05251/figure-1-nucleation-framework.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "平衡 Ising/CNT 与非平衡生态前沿/准势成核的并排框架。", "caption": "非平衡系统中 front speed 与 diffusivity 接替 bulk free-energy difference 与 surface tension。", "selection_rationale": "Figure 1 是全文最重要的统一机制图，优先于单个 quasipotential 曲线。"},
        "figure_refs": [figure("2608.05251", "figure-1-nucleation-framework.webp", "Figure 1", 3, "equilibrium-nonequilibrium mapping", "Ising/CNT 与生态反应扩散成核的对照框架。", "平衡与非平衡成核的量对应。", "The diagram shows that the mathematical CNT structure survives after replacing energetic inputs by front dynamics.")],
        "equation_refs": [
            {"label": "Curved-front radius dynamics", "latex": r"c_{\rm tot}(R)=c-\frac{(d-1)D}{R},\qquad R_c=\frac{(d-1)D}{c}", "role": "deterministic growth-decay threshold", "symbols": {"c": "flat-front speed", "D": "curvature diffusivity"}, "evidence": "paper.pdf pp. 12–13, Eqs. (40)–(42)", "interpretation": "Droplets smaller than the curvature-controlled radius shrink; larger droplets invade."},
            {"label": "Weak-noise nucleation law", "latex": r"p(R_0)\asymp\exp\!\left[-\frac{U_c-U(R_0)}{T}\right]", "role": "quasipotential activation probability", "symbols": {"U_c": "critical-nucleus quasipotential", "T": "noise strength"}, "evidence": "paper.pdf pp. 8, 13, Eqs. (20), (46)", "interpretation": "Quasipotential replaces equilibrium energy in the Arrhenius exponent."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–13: Figure 1, Freidlin-Wentzell theory and binodal front theory", "paper.pdf pp. 14–18: spinodal asymptotics and quasipotential", "paper.pdf pp. 20–31: Lotka-Volterra fronts, depletion and numerical tests", "source PDF SHA-256 8e61789d08568052cf0ad02b04e9e42b96123682f8d27e5394aa20d0cd3cf8dc", "Evidence status: full-text verified theory and numerics; no independent reproduction performed."],
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
