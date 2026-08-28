#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 026."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2608.05666", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2608.05666",
        "title_en": "Potential Matching Optimal Transport: Continuous Normalizing Flows for Exact $p$-Wasserstein Dynamics",
        "title_zh": "势匹配最优传输：实现精确 p-Wasserstein 动力学的连续归一化流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["f8a93a5f3481da6d"], ["Fluid Dynamics"]),
        "verified_metadata": meta("2608.05666", "v1", "Potential Matching Optimal Transport: Continuous Normalizing Flows for Exact $p$-Wasserstein Dynamics", ["Lishuo Zhang", "Ruizhi Huang", "Yang Yu", "Lei Li"], ["cs.LG", "math.NA"], "cs.LG", "2026-08-06T07:04:30Z", "PMOT trains a scalar-potential CNF with self-induced straight bridges and proves ideal zero-loss recovery of the p-optimal transport dynamics under explicit regularity and uniqueness assumptions."),
        "sections": [
            sec("作者信息", r"作者：Lishuo Zhang、Ruizhi Huang、Yang Yu、Lei Li；arXiv:2608.05666v1。全文 22 页。工作把 generalized Benamou–Brenier potential velocity 用于任意 (p>1) 的连续归一化流。"),
            sec("研究问题", r"标准 flow matching 可生成正确终点分布，却不保证轨迹实现给定 (c_p(x,y)=\lVert x-y\rVert^p) 下的最优传输。论文问：能否不用预先计算 OT coupling 或内层 OT solver，直接训练一个 (p)-特异的 potential flow，并在理想条件下恢复最优 map 与整条动力学？"),
            sec("背景", r"广义 Benamou–Brenier 表述把速度写为 (v_\Phi=-\lVert\nabla\Phi\rVert^{q-2}\nabla\Phi)，其中 (q=p/(p-1))。不同 (p) 会选择不同 coupling；仅匹配 terminal distribution 不能区分这些路径。", r"Figure 2 用 two moons 同时显示 PMOT 诱导 coupling、仅作事后评价的 Sinkhorn coupling 和连续 trajectories，直观区分训练对象与评价参考。"),
            sec("模型与方法", r"PMOT 从源样本 (x) 经当前流得到 endpoint (F_\Phi(x))，再沿二者的直线桥采样。损失将桥上的 (\nabla\Phi) 匹配到 (-\lVert F_\Phi(x)-x\rVert^{p-2}[F_\Phi(x)-x])，并另加灵活的 terminal discrepancy。桥和 target 都由当前模型自身产生。", r"这种构造不需要外部 coupling；Sinkhorn 只在训练后用来比较。likelihood 任务可用 CNF density objective，sample-only color transfer 则用 MMD terminal loss。"),
            sec("核心结果与证据", r"Theorem 3.2 说明：在 absolute continuity、BB minimizer 可由给定 potential class 表示、interior (C^2) regularity、所有中间分布 full support、terminal exact matching 和唯一性成立时，任何 zero-loss solution 满足 generalized BB optimality system，并恢复相应 (p)-optimal map。有限网络训练的非零经验损失不自动获得这一结论。", r"8-Gaussians 与 Pinwheel 上，学习到的 transport cost 分别在 matched OT reference 的约 2.4% 与 3.4% 内。Figure 1 的重复 evaluation resampling 给出 off-diagonal/diagonal endpoint-MSE ratio (1.410\pm0.048)；它衡量评价样本波动，不是独立重训误差。", r"tabular density experiments 中 PMOT 在 MiniBooNE、POWER、HEPMASS 报告较低 NLL，但 OT-Flow baseline 对 regularization weight 敏感且各数据集使用不同设置；这些结果支持竞争力，不证明普遍优势。"),
            sec("有效性与局限", r"理论贡献是把 (p)-specific geometry、terminal matching 与 potential PDE 连接起来，并明确列出 exactness 条件。多种 (p)、density 与 sample-only experiments 检查了不同使用方式。", r"zero-loss、realizability、full support 与 uniqueness 都很强；有限采样、网络容量、ODE integration 和优化误差不在 exact theorem 中消失。deterministic CNF 仍受 Monge-map 可表达性限制，且没有独立复现或大规模图像基准。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2608.05666。全文 22 页，PDF SHA-256：f8a93a5f3481da6d22f9bd11591296a4d278cb3f288d5e97b3cc00771faddf5d。", r"复现需固定 (p,q)、potential network、ODE solver/tolerances、bridge-time sampling、terminal discrepancy、optimization schedule、evaluation Sinkhorn regularization、seeds 与重复抽样协议。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 p.4 的 generalized velocity 与 PM objective，再核对 pp.4–5 Theorem 3.2 的全部假设。随后看 p.7 Figure 2 和 p.6 Table 1，最后读 appendix 的 resampling study，并把 post-hoc OT reference 与训练信号分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2608.05666/figure-2-transport.webp", "label": "Figure 2", "visual_type": "comparison", "evidence": "paper.pdf p. 7, Figure 2", "alt_text": "two-moons 数据上的 PMOT coupling、Sinkhorn reference 与连续轨迹。", "caption": "PMOT 直接诱导 coupling 与 trajectories；Sinkhorn 仅在训练后用于比较。", "selection_rationale": "Figure 2 最直接展示方法如何同时产生 map 和连续动力学。"},
        "figure_refs": [figure("2608.05666", "figure-2-transport.webp", "Figure 2", 7, "show learned coupling and trajectories", "PMOT coupling、事后 Sinkhorn reference 和 transport trajectories。", "two-moons 上的 (p=2) transport geometry。", "The learned map is evaluated against Sinkhorn only after training; the figure does not show an external coupling used as supervision.")],
        "equation_refs": [
            {"label": "Generalized potential velocity", "latex": r"v_\Phi(x,t)=-\lVert\nabla\Phi(x,t)\rVert^{q-2}\nabla\Phi(x,t),\qquad q=\frac{p}{p-1}", "role": "parameterize p-Wasserstein CNF dynamics", "symbols": {"p": "transport-cost exponent", "q": "Hölder conjugate"}, "evidence": "paper.pdf p. 4, Eq. (1)", "interpretation": "Changing p changes how the scalar-potential gradient is converted into velocity."},
            {"label": "Potential-matching target", "latex": r"\nabla\Phi(x_t,t)\approx-\lVert F_\Phi(x)-x\rVert^{p-2}\bigl(F_\Phi(x)-x\bigr)", "role": "self-induced straight-bridge matching", "symbols": {"F_Phi": "current flow endpoint", "x_t": "point on the endpoint bridge"}, "evidence": "paper.pdf p. 4, PM objective", "interpretation": "The current model supplies its own endpoints and hence its own bridge target."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–5: objective and zero-loss exactness theorem", "paper.pdf pp. 6–9: synthetic, density and color-transfer experiments", "paper.pdf p. 7, Figure 2", "paper.pdf p. 20: repeated evaluation resampling", "source PDF SHA-256 f8a93a5f3481da6d22f9bd11591296a4d278cb3f288d5e97b3cc00771faddf5d", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "cond-mat-0107443", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/cond-mat/0107443",
        "title_en": "Phase Separation and Coarsening in Electrostatically Driven Granular Media",
        "title_zh": "静电驱动颗粒介质中的相分离与粗化",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["604b2b22ade536e7"], ["Soft Matter"]),
        "verified_metadata": meta("cond-mat/0107443", "v2", "Phase Separation and Coarsening in Electrostatically Driven Granular Media", ["I. S. Aranson", "B. Meerson", "P. V. Sasorov", "V. M. Vinokur"], ["cond-mat.soft", "cond-mat.stat-mech"], "cond-mat.soft", "2001-07-20T20:54:09Z", "A globally constrained bistable Ginzburg–Landau model and its sharp-interface limit explain phase separation and curvature-driven coarsening in an electrostatically driven granular submonolayer."),
        "sections": [
            sec("作者信息", r"作者：I. S. Aranson、B. Meerson、P. V. Sasorov、V. M. Vinokur；arXiv:cond-mat/0107443v2。全文 5 页。论文针对上下电极间受静电驱动的导电颗粒亚单层建立连续模型。"),
            sec("研究问题", r"实验中颗粒在稀薄 gas 与致密 precipitate 之间相分离，随后岛状结构持续粗化。论文问：如何用最小场论同时表达局部吸附/脱附、总颗粒数守恒和界面曲率，并预测晚期 growth law？"),
            sec("背景", r"电场对单颗粒的向上力会被附近 precipitate 屏蔽；振动碰撞又把颗粒从底板抬起。局部 bistability 因而与空间均匀的 gas density (n_g(t)) 耦合，而不是普通局域 Allen–Cahn 模型。", r"Figure 2 展示数值 precipitate 从连通纹理断裂成圆形岛并继续并合/长大，给出 sharp-interface regime 的直观图像。"),
            sec("模型与方法", r"作者写出 globally constrained Ginzburg–Landau 方程 (\partial_t n=\phi(n,n_g,n_*)+\nabla^2n)，并以 (L^{-2}\int n\,dxdy+n_g=\varepsilon) 实施总数守恒。piecewise source term 在 (n=0) 与 (n=1) 之间产生 bistability。", r"在界面宽度远小于 cluster radius 时做 matched asymptotics，得到 gas supersaturation 驱动与 curvature (K) 竞争的 normal velocity。数值在周期 500×500 系统、(n_*=0.2) 下积分连续模型。"),
            sec("核心结果与证据", r"area rule 给平衡 gas density (n_g^{eq}=n_*^3/[C(1-n_*)^3])。sharp-interface law 为 (v_n=\nu C(1-n_*)^3n_*^{-3/2}(n_g-n_g^{eq})-K)：全局 supersaturation 推动所有界面，而局部曲率使小岛优先消失。", r"晚期尺度由 curvature 给 (R(t)\sim t^{1/2})，固定沉积面积下 cluster number (N(t)\sim t^{-1})。论文还指出有限系统中稳定 cluster 数的下界随 (L^{2/3}) 缩放。", r"Figure 2 的 (t=100,160,300,600,4000,6000) 序列复现实验 up-quench 的形态演化；这是机制级定性一致，不是逐像素拟合。"),
            sec("有效性与局限", r"模型用一个全局守恒变量把非局域竞争纳入局部 bistable PDE，并从同一模型导出 sharp-interface dynamics 与 scaling prediction。", r"source term 与系数是 phenomenological；低频、准均匀 gas 和良好分离的界面尺度是关键假设。高频下作者预期由 attachment-limited (1/2) 向 diffusion-limited (1/3) crossover；当 (n_*) 很小或界面宽度接近 cluster radius 时 sharp-interface 失效。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/cond-mat/0107443。全文 5 页，PDF SHA-256：604b2b22ade536e7516b3c21f731d183ae6974090813bc8fec2d3551d1b391b2。", r"复现需固定 (C,n_*,\varepsilon)、domain/grid、periodic boundary、time integrator、initial perturbation、cluster segmentation 与 late-time fit window。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.1–2 的 screening force、Eqs. (4)–(6) 与总数约束，再看 p.3 area rule 和 Eq. (11) sharp-interface law。最后用 p.4 Figure 2 核对 morphology，并区分低频 (1/2) prediction 与作者讨论的高频 crossover。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/cond-mat-0107443/figure-2-coarsening.webp", "label": "Figure 2", "visual_type": "simulation_snapshot", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "六个时刻的数值 precipitate 图像，从连通结构演化为较大的圆形 clusters。", "caption": "globally constrained bistable PDE 产生 curvature-driven coarsening。", "selection_rationale": "Figure 2 是模型主要动力学结果，并以六个有时间标记的快照直接展示晚期粗化过程。"},
        "figure_refs": [figure("cond-mat-0107443", "figure-2-coarsening.webp", "Figure 2", 4, "show simulated coarsening morphology", "六个时刻的 precipitate density snapshots。", "数值相分离与粗化序列。", "The sequence qualitatively reproduces the observed morphology and is consistent with curvature-driven growth.")],
        "equation_refs": [
            {"label": "Globally constrained field model", "latex": r"\partial_t n=\phi(n,n_g,n_*)+\nabla^2n,\qquad L^{-2}\!\int n\,dxdy+n_g=\varepsilon", "role": "couple local phase conversion to particle conservation", "symbols": {"n": "precipitate density", "n_g": "uniform gas density"}, "evidence": "paper.pdf p. 2, Eqs. (4)–(6)", "interpretation": "All clusters compete through one conserved gas reservoir."},
            {"label": "Sharp-interface velocity", "latex": r"v_n=\nu C\frac{(1-n_*)^3}{n_*^{3/2}}(n_g-n_g^{eq})-K", "role": "combine supersaturation and curvature", "symbols": {"K": "interface curvature", "n_g_eq": "area-rule gas density"}, "evidence": "paper.pdf p. 3, Eq. (11)", "interpretation": "Global supersaturation promotes growth while curvature removes small clusters."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2: electrostatic mechanism and constrained PDE", "paper.pdf p. 3: area rule and sharp-interface equations", "paper.pdf p. 4, Figure 2 and growth-law discussion", "source PDF SHA-256 604b2b22ade536e7516b3c21f731d183ae6974090813bc8fec2d3551d1b391b2", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "cond-mat-0411522", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/cond-mat/0411522",
        "title_en": "Far-from-equilibrium Ostwald ripening in electrostatically driven granular powders",
        "title_zh": "静电驱动颗粒粉末中的远离平衡 Ostwald 熟化",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["2a7134ede31921d1"], ["Soft Matter"]),
        "verified_metadata": meta("cond-mat/0411522", "v1", "Far-from-equilibrium Ostwald ripening in electrostatically driven granular powders", ["M. V. Sapozhnikov", "A. Peleg", "B. Meerson", "I. S. Aranson", "K. L. Kohlstedt"], ["cond-mat.soft"], "cond-mat.soft", "2004-11-19T18:42:54Z", "Experiments on an electrostatically driven granular submonolayer show dynamic scaling and attachment–detachment-controlled coarsening, with the scaled size distribution strongly modified by cluster mergers."),
        "sections": [
            sec("作者信息", r"作者：M. V. Sapozhnikov、A. Peleg、B. Meerson、I. S. Aranson、K. L. Kohlstedt；arXiv:cond-mat/0411522v1。全文 6 页。实验使用约 (10^7) 个直径 40 μm 的铜颗粒，置于 27×27 cm、间距 1.5 mm 的电极之间并充干燥氮气。"),
            sec("研究问题", r"电场共存区中的 granular gas 与 immobile clusters 持续交换颗粒。论文问：这种强驱动、耗散体系是否仍有 Ostwald-ripening 式 dynamic scaling；若有，其 cluster-size distribution 是否等于零体积分数极限的经典 Wagner distribution？"),
            sec("背景", r"在阈值 (E_1<E<E_2) 内，孤立颗粒可被抬起，而 cluster 内屏蔽降低 electrostatic force。gas 颗粒快速运动并在 cluster 边界附着/脱离，使晚期动力学更接近 interface-controlled ripening。", r"Figure 2 在 (t=0,10^4,2\times10^4,5\times10^4\) s 显示 clusters 变粗且发生 merger，是后续 size-distribution 分析的直接实验基础。"),
            sec("模型与方法", r"作者追踪 cluster area、number 和 equivalent radius，从四次独立实验的 340 个时间截面构建 scaled PDF。dynamic-scaling ansatz 为 (f(R,t)=R_*^{-3}F(R/R_*))，其中 (R_*) 由平均尺度给定。", r"attachment–detachment-controlled 单 cluster law 写成 \(\dot R=D(1/R_c-1/R)\)。比较对象包括忽略 cluster fraction/merger 的 Wagner theory，以及 Conti 等人显式加入 binary coalescence、输入实测面积分数的理论。"),
            sec("核心结果与证据", r"Figure 3 给 mean cluster area 近线性增长，拟合指数 (1.00\pm0.014)；inverse cluster number 的指数为 (1.042\pm0.014)。因此 (R_*\sim t^{1/2})、(N\sim t^{-1})，符合 interface-controlled coarsening。", r"晚期总 cluster area fraction 约保持不变。340 组 PDF collapse 到共同 scaled curve，支持 dynamic scaling。", r"经典 Wagner distribution 对峰和 cutoff 明显不符；Conti coalescence theory 仅用实测面积分数 (\varepsilon=0.092) 即更好描述主体与大尺寸尾部。小半径处仍有系统偏差，作者归因于 fast-gas-transport 近似或 intercluster correlations。"),
            sec("有效性与局限", r"同一实验同时检查 growth exponent、number decay、area conservation 和完整 scaled distribution，证据比单一幂律更完整；coalescence theory 的比较没有逐曲线自由拟合形状。", r"场视野、cluster segmentation 和有限时间窗会影响 PDF 与指数；快速均匀 gas、圆形 equivalent radius 与二体 merger 模型都是近似。结果来自一个颗粒/气体/几何设置，不能直接推广到所有 driven granular media。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/cond-mat/0411522。全文 6 页，PDF SHA-256：2a7134ede31921d1aac0bc71928109c3f4f1ee44be5e20efc6f46ab435f0f5fa。", r"复现需固定粒径与数量、plate spacing/area、电场 2.33 kV/cm、氮气条件、imaging cadence、cluster threshold、edge handling、equivalent-radius definition、scaling normalization 和 fit interval。", r"Evidence status: full-text verified experimental report; no independent reproduction performed."),
            sec("阅读指南", r"先看 p.2 Figure 2–3 的图像与两个增长量，再读 p.3 Eqs. (3)–(7) 和 Figure 5 的 PDF collapse。比较 Wagner 与 merger theory 时重点检查实测 (\varepsilon=0.092) 和小半径偏差。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/cond-mat-0411522/figure-2-experiment.webp", "label": "Figure 2", "visual_type": "real_space", "evidence": "paper.pdf p. 2, Figure 2", "alt_text": "四个时刻的实验颗粒 cluster 图像，显示岛变大、数目减少并发生合并。", "caption": "实验序列直接显示远离平衡 granular clusters 的熟化与 merger。", "selection_rationale": "Figure 2 是实验现象本身，以四个有时间标记的真实空间图像直接展示粗化与 cluster merger。"},
        "figure_refs": [figure("cond-mat-0411522", "figure-2-experiment.webp", "Figure 2", 2, "show experimental coarsening and mergers", "四个时刻的 granular-cluster snapshots。", "静电驱动颗粒层的实验熟化。", "The images establish coarsening and visible mergers before the statistical scaling analysis.")],
        "equation_refs": [
            {"label": "Dynamic scaling ansatz", "latex": r"f(R,t)=R_*^{-3}(t)F\!\left(\frac{R}{R_*(t)}\right)", "role": "collapse cluster-size distributions", "symbols": {"R_star": "characteristic cluster radius", "F": "scaled distribution"}, "evidence": "paper.pdf p. 3, Eq. (3)", "interpretation": "After rescaling by one growing length, late-time PDFs should share one shape."},
            {"label": "Interface-controlled growth", "latex": r"\dot R=D\left(\frac{1}{R_c(t)}-\frac{1}{R}\right)", "role": "model attachment-detachment-limited ripening", "symbols": {"R_c": "critical radius", "D": "effective kinetic coefficient"}, "evidence": "paper.pdf pp. 3–4, Eq. (7)", "interpretation": "Clusters below the critical radius shrink while larger clusters grow."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2: apparatus and snapshot/growth data", "paper.pdf pp. 3–4: dynamic scaling and growth law", "paper.pdf p. 3, Figures 4–5: area fraction and scaled PDF", "source PDF SHA-256 2a7134ede31921d1aac0bc71928109c3f4f1ee44be5e20efc6f46ab435f0f5fa", "Evidence status: full-text verified experimental report; no independent reproduction performed."],
    },
    {
        "arxiv_id": "cond-mat-0702169", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/cond-mat/0702169",
        "title_en": "Non-equilibrium Phase Transitions with Long-Range Interactions",
        "title_zh": "具有长程相互作用的非平衡相变",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["3df45acf3acc918f"], ["Statistical Physics"]),
        "verified_metadata": meta("cond-mat/0702169", "v2", "Non-equilibrium Phase Transitions with Long-Range Interactions", ["Haye Hinrichsen"], ["cond-mat.stat-mech"], "cond-mat.stat-mech", "2007-02-07T11:05:33Z", "A review of absorbing-state transitions with spatial or temporal Lévy flights and of restricted long-range processes whose continuum equations contain fractional density powers rather than fractional derivatives."),
        "sections": [
            sec("作者信息", r"作者：Haye Hinrichsen；arXiv:cond-mat/0702169v2。全文 40 页。这是一篇 2007 年综述，主题是 absorbing-state transitions 中两类长程机制及其场论描述。"),
            sec("研究问题", r"长程传播会让 directed-percolation universality 如何改变？论文区分两个并不等价的问题：无限制 Lévy flights 是否用 fractional spatial/temporal derivatives 描述；传播距离被最近粒子截断时，continuum limit 又会产生什么非解析项？"),
            sec("背景", r"空间跳跃尾部 (P(r)\sim r^{-d-\sigma})，时间等待尾部 (P(\Delta t)\sim\Delta t^{-1-\kappa})。自由过程的朴素边界是 (\sigma=2,\kappa=1)，但 interacting absorbing transition 的 crossover 可因 anomalous dimensions 移动。", r"Figure 2 把 (\sigma\)–(\kappa) 平面分成 superdiffusive、diffusive、subdiffusive 与混合区，并标注相应 dynamic-exponent relations，是全文概念地图。"),
            sec("模型与方法", r"无限制 Lévy flights 在 Fourier space 由 (\widetilde\nabla^\sigma e^{ikr}=-|k|^\sigma e^{ikr}) 表示，重尾 waiting times 对应 temporal fractional derivative ((i\omega)^\kappa)。把这些项加入 Reggeon/DP field theory 后做 scaling 与 renormalization-group 分析。", r"综述随后讨论 restricted ‘sigma process’ 与 ‘alpha process’：传播率或最大跳距依赖最近活跃粒子距离。其 coarse-grained 方程仍用短程 differential operators，但 reaction/diffusion coefficients 出现 density 的 fractional powers。"),
            sec("核心结果与证据", r"在一定区间内，spatial 或 temporal Lévy term 不被重整化，从而给出连接 critical exponents 的 exact scaling relations；critical exponents 随 (\sigma\) 或 (\kappa) 连续变化。mean-field、long-range nontrivial 和 short-range DP 三个 regime 由两条 crossover boundaries 分隔。", r"相互作用使 crossover 一般移到 (\sigma_*>2) 或 (\kappa_*>1)，因此不能用自由随机游走的阈值直接判断 short-range universality。综述汇总的一圈 RG 与 simulations 支持这一结构，但各 exponent estimate 有近似与有限尺寸误差。", r"restricted sigma process 在 (\sigma<1) 可出现 discontinuous compact transition；alpha process 的 fractional density terms 产生另一组连续变化 exponents。它们不是把 Laplacian 简单换成 fractional Laplacian 的同一模型。"),
            sec("有效性与局限", r"综述的主要价值是把传播核、fractional operators、RG non-renormalization 和 restricted interactions 放在同一分类中，并明确哪些 exact relations 来自 operator structure。", r"这是截至 2007 年的文献综合，不是新的统一数值数据集；部分结论来自 one-loop expansion 或当时有限规模 simulations。fractional continuum description 依赖真正的无截断幂律尾部，而 restricted processes 需要不同 coarse graining。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/cond-mat/0702169。全文 40 页，PDF SHA-256：3df45acf3acc918f6d903c1760884f6fae9860eac675b59a1eb688e098789689。", r"复核具体 exponent 需回到综述所引原论文，固定 Lévy sampling convention、boundary/finite-size cutoff、absorbing criterion、RG order、simulation size/time 和 exponent-fit window。", r"Evidence status: full-text verified review; no independent reproduction performed."),
            sec("阅读指南", r"先看 pp.3–10 的 distributions、fractional derivatives 与 Figure 2，再读 long-range DP 的 action、scaling relations 和 crossover。最后读 pp.27–31 的 sigma/alpha processes，特别注意 ‘fractional derivative’ 与 ‘fractional density power’ 的差别。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/cond-mat-0702169/figure-2-phase-diagram.webp", "label": "Figure 2", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 10, Figure 2", "alt_text": "sigma–kappa 平面中的 superdiffusive、diffusive 与 subdiffusive 区域。", "caption": "空间与时间 Lévy 指数共同决定 anomalous diffusion regime 和 dynamic scaling。", "selection_rationale": "Figure 2 是长程空间与时间传播分类的中心相图，并在卡片尺寸下仍能清楚表达四种 anomalous-diffusion 区域。"},
        "figure_refs": [figure("cond-mat-0702169", "figure-2-phase-diagram.webp", "Figure 2", 10, "map spatial and temporal anomalous diffusion", "以 sigma 与 kappa 为轴的四区 phase diagram。", "空间/时间 Lévy operators 的动力学区域。", "The diagram classifies the free anomalous-diffusion sectors; interacting critical crossovers are shifted by fluctuations.")],
        "equation_refs": [
            {"label": "Spatial Lévy operator", "latex": r"\widetilde\nabla^\sigma e^{ikr}=-|k|^\sigma e^{ikr}", "role": "define the fractional spatial derivative", "symbols": {"sigma": "spatial tail exponent", "k": "wave number"}, "evidence": "paper.pdf p. 6, Eq. (8)", "interpretation": "A power-law jump kernel becomes a nonanalytic |k|^sigma propagator."},
            {"label": "Long-range DP action sector", "latex": r"\bar\psi\bigl[\partial_t-D\nabla^2-\widetilde D\widetilde\nabla^\sigma-\tau\bigr]\psi", "role": "embed spatial Lévy flights in absorbing-state field theory", "symbols": {"D_tilde": "long-range diffusion amplitude", "tau": "distance from criticality"}, "evidence": "paper.pdf p. 33, Eq. (A1)", "interpretation": "Short- and long-range propagation compete in the same response functional."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–10: Lévy kernels, fractional operators and Figure 2", "paper.pdf pp. 11–25: long-range absorbing transitions and crossover", "paper.pdf pp. 27–31: restricted sigma and alpha processes", "paper.pdf p. 33, Appendix action", "source PDF SHA-256 3df45acf3acc918f6d903c1760884f6fae9860eac675b59a1eb688e098789689", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
    {
        "arxiv_id": "cond-mat-9501089", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/cond-mat/9501089",
        "title_en": "Theory of Phase Ordering Kinetics",
        "title_zh": "相序动力学理论",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["d18c975ff77d8885"], ["Statistical Physics"]),
        "verified_metadata": meta("cond-mat/9501089", "v1", "Theory of Phase Ordering Kinetics", ["A. J. Bray"], ["cond-mat"], "cond-mat", "1995-01-19T19:30:15Z", "A comprehensive review of domain coarsening after a quench, organizing growth laws, scaling functions and structure-factor tails through conservation laws and topological defects."),
        "sections": [
            sec("作者信息", r"作者：A. J. Bray；arXiv:cond-mat/9501089v1。PDF 共 85 页。这是 phase-ordering kinetics 的经典长篇综述，覆盖 scalar、vector、tensor order parameters，非守恒/守恒动力学、缺陷、流体与无序体系。"),
            sec("研究问题", r"系统从均匀相淬火到 broken-symmetry phase 后，domain 为什么通常只剩一个增长尺度 (L(t))？如何由 conservation law、curvature、transport mechanism 与 defect dimensionality 推出 growth law，并预测 correlation/structure-factor scaling functions？"),
            sec("背景", r"粗粒化自由能为 (F[\phi]=\int[\tfrac12(\nabla\phi)^2+V(\phi)]d^dx)。Model A 让 order parameter 局部弛豫，Model B 强制总 order parameter 守恒；相同静态自由能因此可产生不同动态指数。", r"综述以 domain walls、vortices、strings、monopoles 等 topological defects 统一不同 (O(n)) 模型；defect core 的短尺度结构决定高波数散射尾。"),
            sec("模型与方法", r"dynamic-scaling hypothesis 写成 (C(r,t)=f(r/L))、(S(k,t)=L^dg(kL))。作者结合界面运动、energy-dissipation scaling、exactly soluble limits、Gaussian auxiliary-field approximations 与 simulations/experiments，逐类建立 growth laws。", r"非守恒 scalar 界面满足 Allen–Cahn (v=-K)，给 (L\sim t^{1/2})。守恒 scalar 由 Gibbs–Thomson chemical potential 和 bulk diffusion 控制，给 (L\sim t^{1/3})。"),
            sec("核心结果与证据", r"curvature-driven Model A domain 的 collapse time 随 (R^2) 缩放，因此 (L(t)\sim t^{1/2})；守恒 Model B spherical domain 有 \(\dot R\sim-R^{-2}\)，因此 (L(t)\sim t^{1/3})。这两个指数来自不同 transport constraints，而非不同 equilibrium phases。", r"generalized Porod law 对 scalar interfaces 给 (S(k,t)\sim[Lk^{d+1}]^{-1})；对 (O(n)) defects 给 (S(k,t)\sim[L^nk^{d+n}]^{-1})。tail exponent 直接记录 defect codimension。", r"非守恒 vector systems 通常 (L\sim t^{1/2})，二维 XY 情形有 logarithmic correction (L\sim(t/\ln t)^{1/2})。流体输运、非零 volume fraction、quenched disorder 或长程相互作用可引入 crossover 或改变增长律。"),
            sec("有效性与局限", r"综述把 growth law、scaling function 和 defect scattering 连接起来，并持续用 exact result、approximation、simulation 与 experiment 交叉检查，而不把单一 closure 当成普适证明。", r"dynamic scaling 本身除简单模型外通常未被严格证明。OJK、Mazenko 等 Gaussian closures 可分别拟合某些 correlators，却可能无法同时给出 (C) 与四点函数的绝对幅度；守恒场的朴素近似甚至会错误地产生 (t^{1/4})，除非正确纳入 bulk diffusion。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/cond-mat/9501089。PDF 共 85 页，SHA-256：d18c975ff77d8885c3c2db85a4a6a022d411c62e20236a8b6d908fea4b3527ec。", r"复核具体模型需固定 order-parameter dimension、conservation law、temperature/noise、domain/boundary、initial spectrum、length estimator、defect identification、finite-size window 和 logarithmic-correction convention。", r"Evidence status: full-text verified review; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.4–11 的 Models A/B、dynamic scaling 与 scalar growth laws，再看 pp.19–21 的 vector growth 和 generalized Porod law。之后按自己的体系选择 conserved fields、hydrodynamics 或 disorder 章节；所有近似 scaling functions 都要对照其 assumptions。"),
        ],
        "cover": {"mode": "title_abstract", "label": "Review overview", "visual_type": "title_abstract", "evidence": "paper.pdf pp. 1–3 and full-text review structure", "alt_text": "相序动力学综述的标题与核心主题摘要。", "caption": "从守恒律、曲率与拓扑缺陷统一理解 domain-growth laws。", "abstract_text": "这篇经典综述以 dynamic scaling 为主线，比较非守恒与守恒动力学的增长律，并用 domain walls、vortices、strings 与 monopoles 等拓扑缺陷统一解释结构因子的 Porod 尾。", "selection_rationale": "该 85 页多主题综述没有一幅在卡片尺寸下仍能代表全篇且可清晰抽取的单一中心图；使用 title/abstract cover 避免让局部旧式矢量图误代表整篇。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Model A and Model B", "latex": r"\partial_t\phi=-\frac{\delta F}{\delta\phi},\qquad \partial_t\phi=\nabla^2\frac{\delta F}{\delta\phi}", "role": "distinguish nonconserved and conserved ordering", "symbols": {"F": "coarse-grained free energy", "phi": "order parameter"}, "evidence": "paper.pdf pp. 4–5, Eqs. (2)–(3)", "interpretation": "The extra Laplacian enforces conservation and changes the coarsening transport mechanism."},
            {"label": "Generalized Porod tail", "latex": r"S(k,t)\sim\frac{1}{L^n k^{d+n}}", "role": "relate large-k scattering to O(n) defects", "symbols": {"n": "order-parameter/defect codimension", "d": "space dimension"}, "evidence": "paper.pdf pp. 20–21, Eqs. (69)–(70)", "interpretation": "Defect cores determine the universal high-wave-number power law."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–11: models, scaling hypothesis and scalar growth laws", "paper.pdf pp. 19–21: vector growth and generalized Porod law", "paper.pdf later review chapters: conserved fields, hydrodynamics and disorder", "source PDF SHA-256 d18c975ff77d8885c3c2db85a4a6a022d411c62e20236a8b6d908fea4b3527ec", "Evidence status: full-text verified review; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{str(card['arxiv_id']).replace('/', '-')}.json"
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
