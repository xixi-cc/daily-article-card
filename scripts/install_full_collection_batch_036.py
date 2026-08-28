#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 036."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_032 import card
from install_full_collection_batch_014 import sec


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def title_card(
    pid: str,
    source_version: str,
    source_pdf: str,
    title: str,
    title_zh: str,
    profile: str,
    record: str,
    topic: str,
    metadata: dict[str, object],
    sections: list[dict[str, object]],
    abstract_text: str,
    rationale: str,
    equations: list[dict[str, object]],
    evidence: list[str],
) -> dict[str, object]:
    """Build a card with a truthful title/abstract cover when the paper has no result figure."""
    item = card(
        pid, source_version, source_pdf, title, title_zh, profile, record, topic,
        metadata, sections, "unused.webp", "No source figure", 1, "schematic",
        "", "", "", equations, evidence,
    )
    item["cover"] = {
        "mode": "title_abstract",
        "abstract_text": abstract_text,
        "selection_rationale": rationale,
    }
    item["figure_refs"] = []
    return item


CARDS = [
    card(
        "doi-10.1103-physrevd.107.l051504", "arXiv manuscript", "https://arxiv.org/pdf/2212.08469",
        "Learning trivializing gradient flows for lattice gauge theories", "学习格点规范理论的平凡化梯度流",
        "ai_empirical", "7e87af81efc4a72b", "Renormalization Group",
        {"doi": "10.1103/PhysRevD.107.L051504", "arxiv_id": "2212.08469", "version": "arXiv v2 full text", "title": "Learning trivializing gradient flows for lattice gauge theories", "authors": ["Simone Bacchio", "Pan Kessel", "Stefan Schaefer", "Lorenz Vaitl"], "journal": "Physical Review D", "volume": "107", "issue": "5", "article": "L051504", "published": "2023-03-20", "abstract": "A continuous normalizing flow built from Wilson-loop gradient flows learns perturbatively initialized coefficient functions for two-dimensional SU(3) lattice gauge sampling with 14 or 420 parameters.", "comment": "ArXiv v2 full text cross-checked with the CC BY 4.0 version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Simone Bacchio、Pan Kessel、Stefan Schaefer、Lorenz Vaitl；Physical Review D 107, L051504 (2023)，DOI:10.1103/PhysRevD.107.L051504。全文取 arXiv:2212.08469v2，共11页含补充推导；期刊版本为 CC BY 4.0，Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "格点场论接近连续极限时会出现 critical slowing down；normalizing-flow proposals 可降低自相关，但百万参数模型难训练且体积扩展差。论文问：能否从 Lüscher 的 perturbative trivializing map 出发，只学习少量 Wilson-loop coefficient functions，同时保留 SU(N) 局域/全局对称和可解释初始化？"),
            sec("背景", "可微双射 U=F(V) 把作用量改写为 S_F(V)=S[F(V)]-ln det F*(V)；若该量为常数，uniform latent distribution 就被映射到目标分布。未完全平凡化时，独立 flow proposals 仍可通过 Metropolis 接受率纠偏。", "Lüscher flow 用 SU(N) Lie-algebra-valued force 驱动 links，并把 flow action 写成 Wilson loops 的线性组合。原 perturbative coefficients 在 strong-coupling expansion 中受控，但向 continuum 方向性能快速下降。"),
            sec("模型与方法", "作者把 coefficient functions 参数化为 affine functions 或 cubic splines，使用 adjoint-state method 沿 SU(N) flow 反向求目标梯度；该成本与一次 forward flow 同阶，而不随参数数目线性增加。Model A 含7种 loops×2个参数=14参数；Model B 含42种 loops×10 spline knots=420参数。", "benchmark 是二维 pure SU(3) Yang–Mills，16×16 lattice，β=4、5、6；flow 用20步三阶 Crouch–Grossmann integrator，Adam mini-batch 1024、learning rate 5×10^-4，并以 effective sample size 衡量 proposal quality。"),
            sec("核心结果与证据", "Table I 中，Lüscher next-to-leading coefficients 的 ESS 随 β 从42%降到4%和<1%；14参数 Model A 达91%、65%、26%，420参数 Model B 达98%、88%、70%。作者引用的约10^6参数 gauge-equivariant baseline 为88%、75%、48%。", "Figure 1 显示从 perturbative initialization 开始，Model A 在三种 β 上均提高 ESS；β越大训练越难、最终 ESS 越低。曲线只证明该16²二维 benchmark 的优化轨迹，不足以证明 volume scaling 或 continuum critical exponent 被改善。", "Figure 2 用约1.024×10^6个 samples 比较 HMC 与 flow-NMCMC 的 plaquette/Wilson-loop observables，比例与1一致到绘制误差范围，支持 Metropolis 校正后的无偏性。HMC in trivialized variables、四维应用及 full QCD 都被作者列为未来工作。"),
            sec("有效性与局限", "参数效率比较沿用参考文献报告的约百万参数模型，训练环境、wall-clock、memory、integrator cost 与采样成本并未完全统一；较高 ESS 不自动等价于更低端到端 cost。所有主结果来自二维 pure gauge 16² lattice。", "论文没有测量 topological freezing、continuum extrapolation 或体积扩展，也未实现四维 SU(3)+fermions。对 symmetry-preserving Wilson-loop basis 的强先验是优势，同时限制 expressivity；420参数 Model B 的 loop set 与 knots 仍是人工选择。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2212.08469；期刊：https://doi.org/10.1103/PhysRevD.107.L051504。PDF SHA-256：54cfe9794db066f97bca8cbd9fce2b13046ec417da19833cbb817336c36506ab。实现基于 Lyncs-API、QUDA 和 P100 GPUs；全文未给出专用代码仓库。", "复现需固定 lattice 16²、β、Wilson-loop basis、flow time、20步 Lie-group integrator、spline knots、VarGrad、batch/learning rate、initialization、ESS estimator 与 NMCMC acceptance。Evidence status: full-text verified ML/lattice benchmark manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–3 Eqs. (1)–(19)，理解 trivializing condition、adjoint-state gradient 和对称性；p.4 Table I/Figure 1看参数效率与训练，Figure 2看 observable consistency。最后读 p.5 Conclusion，把四维、HMC 和 full QCD 明确视为未来路线。"),
        ],
        "figure-1-ess-training.webp", "Figure 1", 4, "data_plot",
        "14参数 Model A 从 Lüscher 初始化训练时，β=4、5、6 三组有效样本量随 epoch 的变化。",
        "扰动初始化在三种耦合下都提供非零 ESS 起点，训练继续提高性能，但较大 β 的最终 ESS 明显更低。",
        "Figure 1直接展示少参数模型的学习动力学和随 β 加剧的困难，比单一终值表更能约束结论。",
        [{"label": "Flow-transformed action", "latex": r"S_F(V)=S(F(V))-\ln\det F_*(V)", "role": "define the density induced by a differentiable field redefinition", "symbols": {"F": "trivializing-flow map", "F_*": "Jacobian of the map", "S": "Wilson action"}, "evidence": "paper.pdf p. 2, Eq. (3)", "interpretation": "A constant transformed action would be exactly trivializing; the learned finite model only approximates this condition."}],
        ["paper.pdf pp. 1–3, Eqs. (1)–(19): trivializing flow and adjoint-state method", "paper.pdf p. 4, Table I and Figures 1–2: ESS and observable checks", "paper.pdf p. 5: two-dimensional benchmark scope and future four-dimensional work", "source PDF SHA-256 54cfe9794db066f97bca8cbd9fce2b13046ec417da19833cbb817336c36506ab", "Evidence status: full-text verified ML/lattice benchmark manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physreve.109.034606", "arXiv manuscript", "https://arxiv.org/pdf/2401.09461",
        "Spinodal decomposition and phase separation in polar active matter", "极性主动物质中的旋节分解与相分离",
        "theory_numerics", "d09329bc7821e6c3", "Active Matter",
        {"doi": "10.1103/PhysRevE.109.034606", "arxiv_id": "2401.09461", "version": "arXiv v1 full text", "title": "Spinodal decomposition and phase separation in polar active matter", "authors": ["Maxx Miller", "John Toner"], "journal": "Physical Review E", "volume": "109", "issue": "3", "article": "034606", "published": "2024-03-21", "abstract": "A Toner–Tu–Keller–Segel hydrodynamic theory predicts an anisotropic negative-compressibility instability, moving density bands, slow coarsening and an active uncommon-tangent coexistence construction.", "comment": "ArXiv v1 full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Maxx Miller、John Toner；Physical Review E 109, 034606 (2024)，DOI:10.1103/PhysRevE.109.034606。全文取 arXiv:2401.09461v1，共27页；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "会集体定向运动的 dry flock 若同时释放并追随 chemo-attractant，会怎样失稳和相分离？论文问：Toner–Tu polar order 与 Keller–Segel autochemotaxis 的耦合是否产生类似 equilibrium spinodal decomposition 的 bands/coexistence，以及 plateau densities 应由何种构造决定？"),
            sec("背景", "化学场扩散并以有限寿命衰减；消去快速化学变量后，吸引作用降低 flock 的有效 inverse compressibility B。B<0 时均匀移动态出现有限波矢不稳定，其最大增长方向垂直于平均 flock velocity，因此密度波峰/条带平行于平均运动方向。", "模型更一般地适用于任何把有效 B 推成负值的 attractive microscopic mechanism，并不证明真实蚂蚁、细菌或鸟群都处在该参数区。速度场是 coarse-grained polarization proxy，粒子 current 还含压力与噪声贡献。"),
            sec("模型与方法", "作者从 rotation/translation invariance 写出 density、polarization velocity 和 chemical concentration 的 hydrodynamic equations，在线性化后求各方向 sound modes 与 growth rates。靠近临界点再按小 density/velocity fluctuations 展开 nonlinearity，导出一维 travelling interface equations。", "数值积分无噪声、主要限制为仅依赖横向坐标的一维 profiles 和 periodic domain；长时 coarsening 由 weakly attracting interfaces 控制。近临界 perturbation 给出 spinodal/binodal、plateau values 与 interface tanh/sech² 形状，并与 time-dependent PDE solutions 比较。"),
            sec("核心结果与证据", "Figures 1–4 显示不稳定区域高度各向异性，density bands 平行于平均 flock velocity；条带以不同速度移动并逐步合并。线性分析给最大增长率 Im ωmax∝√|B|，而不是所有方向同时失稳。", "近临界最低阶 theory 可用 common tangent；加入两个 active nonlinear coefficients Λ、Γ 后，Figure 16 显示两 coexistence densities 处 pseudo-free-energy slopes 相同，但切线彼此不同，形成 uncommon tangent construction。只有趋近 critical point 时才恢复 common tangent。", "Figure 17 在 Λ=Γ=0.25、演化3000时间单位时，解析 plateau offset 与数值结果差异小于6%。作者也指出一维无噪声 coarsening 指数很可能不真实；关于二维噪声导致 band wandering/zippering 和代数 coarsening 的说法是 conjecture。"),
            sec("有效性与局限", "解析 coexistence theory 是靠近 critical point 的小振幅与小 Λ、Γ 微扰；在远离临界处的数值吻合是经验观察，不提升为受控渐近证明。数值只解 coarse-grained deterministic equations，没有粒子模拟或实验。", "late-stage phase separation 在一维无噪声下呈指数慢，但作者认为二维噪声会改变该结论；此机制尚未计算。fluctuation-renormalized binodal/spinodal、interface dynamics、finite-size scaling 和真实 autochemotactic 参数映射均留待未来。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2401.09461；期刊：https://doi.org/10.1103/PhysRevE.109.034606。PDF SHA-256：7af903fd62a90f5488bea21d37d0a4f68b9eb4be74b8cf7c2956b6b5c9408bb0。全文未提供公开代码仓库。", "复现需固定 hydrodynamic coefficients、chemical lifetime/diffusivity、negative-B distance、angle、periodic length/grid/time step、initial perturbation、Λ/Γ 与 convergence tolerance。Evidence status: full-text verified theory/PDE simulation manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–4 Figures 1–6看 instability、bands 和 phase diagram；pp.14–18 是各向异性 sound/growth derivation。pp.19–26 建立 coexistence theory，p.25 Figure 16 是 uncommon tangent 核心，p.26 Figure 17 给数值检验；最后保留无噪声一维限制。"),
        ],
        "figure-16-uncommon-tangent.webp", "Figure 16", 25, "schematic",
        "主动相分离的 pseudo-free energy 及两个 coexistence densities 处斜率相同但不重合的两条切线。",
        "active nonlinearities 把 equilibrium common-tangent 条件改成 uncommon tangent；临界点附近才恢复共同切线。",
        "Figure 16凝练了论文区别于平衡相分离的核心构造，并在图注中明确其临界适用边界。",
        [{"label": "Uncommon-tangent shift", "latex": r"\delta_+=\delta_-=\frac{1}{15}(\Lambda+\Gamma)", "role": "give the leading active correction to both coexistence plateau densities", "symbols": {"delta_pm": "plateau-density offsets", "Lambda,Gamma": "small active nonlinear coefficients"}, "evidence": "paper.pdf pp. 25–26, Eq. (V.76)", "interpretation": "The equal leading offsets follow only to first order near the critical point; the authors do not expect them to remain equal at higher order."}],
        ["paper.pdf pp. 1–4, Figures 1–6: anisotropic instability and band formation", "paper.pdf pp. 14–18: directional modes and growth-rate analysis", "paper.pdf pp. 19–26, Figures 13–17: coexistence, interfaces and uncommon tangent", "source PDF SHA-256 7af903fd62a90f5488bea21d37d0a4f68b9eb4be74b8cf7c2956b6b5c9408bb0", "Evidence status: full-text verified theory/PDE simulation manuscript; no independent reproduction performed."],
    ),
    title_card(
        "doi-10.1103-physreve.109.044605", "arXiv manuscript", "https://arxiv.org/pdf/2312.07283",
        "Emergent gauge symmetry in active Brownian matter", "活性布朗物质中的涌现规范对称性",
        "theory", "feebea9aa1ee1749", "Active Matter",
        {"doi": "10.1103/PhysRevE.109.044605", "arxiv_id": "2312.07283", "version": "arXiv v2 full text", "title": "Emergent gauge symmetry in active Brownian matter", "authors": ["Nathan Silvano", "Daniel G. Barci"], "journal": "Physical Review E", "volume": "109", "issue": "4", "article": "044605", "published": "2024-04-24", "abstract": "A hydrodynamic MSRJD field theory maps weak density fluctuations of interacting two-dimensional active Brownian particles to an emergent U(1) gauge theory whose charge is vorticity.", "comment": "ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Nathan Silvano、Daniel G. Barci；Physical Review E 109, 044605 (2024)，DOI:10.1103/PhysRevE.109.044605。全文取 arXiv:2312.07283v2，共15页含附录；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "二维 interacting active Brownian particles 的 density fluctuations 与 orientation field 如何在 hydrodynamic limit 中耦合？论文问：MSRJD functional 在 uniform-density background 附近是否出现一个可识别的 U(1) gauge redundancy，以及这一对偶描述怎样把密度、涡量和 nematic elasticity 组织在一起？"),
            sec("背景", "从粒子 labels 连续化为 material coordinates y 后，area-preserving diffeomorphisms 导致 circulation/vorticity conservation。对 rα(y,t)=yα+ρ0^-1 εαβAβ 展开，重标记变成 A→A+ρ0∇Λ；density fluctuation δρ=∇×A 扮演 emergent magnetic field。", "该 U(1) 只在 δρ/ρ0≪1 的 small-fluctuation expansion 中出现，不是 microscopic ABP equations 的精确基本规范对称。这里的 electric charge/current 是对偶流体变量：charge density 对应 orientation vorticity，而非真实电荷。"),
            sec("模型与方法", "作者从 N 个含 translational/rotational white noise、self-propulsion v0n_i 和 two-body potential U 的 overdamped Langevin equations 构造 MSRJD generating functional，再取 finite-density continuum limit。A0 作为 Lagrange multiplier 实现 Gauss constraint。", "保留 A 的 leading order 后得到 Eq. (4.31)：E²、nonlocal BVB、orientation kinetic term 与 v0-dependent source couplings。对 local interaction U(y)=U0δ²(y) 再积分出 gauge fields，获得 orientation-only 的 retarded/nonlocal action，并研究 stationary limit。"),
            sec("核心结果与证据", "主结果 Eq. (4.31) 是显式 gauge-invariant effective action：B=δρ，electric charge ω=∇×n，current 包括 εij∂tnj 与由 ∇·n、microscopic potential 产生的 identically divergence-free topological term；连续性方程随 gauge invariance 成立。", "local potential stationary state 给出二维 nonlocal Frank free energy。bend 与 splay constants 为 Kb=v0²/(2DRDT)、Ks=Kb/[1+ρ0U0/(2DT)]；以 Pe=v0/√(2DRDT)、kd=ρ0U0/(2DT) 表示时 Kb=Pe²、Ks=Pe²/(1+kd)。", "splay/bend 项通过二维 logarithmic Green function 的 weak identity 相关，stiffness κ=ρ0DR Pe²/(1+kd)。这是一套 model consequence；论文没有数值模拟、实验或相图来验证该 coarse-grained gauge mapping。"),
            sec("有效性与局限", "推导依赖二维、uniform background、小密度涨落、continuum limit、pair potential 与 leading-order expansion；strong MIPS、large density contrasts、defects、boundaries 和远离均匀态时规范结构可能失效。", "local δ-potential 是理想化特例。作者未研究 Eq. (5.18) 支持的 topological defects、phase diagram 或 complex dynamics，也未比较 measured elastic constants；‘可能描述 streaking phenomenology’是物理解释而非已验证预测。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2312.07283；期刊：https://doi.org/10.1103/PhysRevE.109.044605。PDF SHA-256：c00e43b481d77d469286de67d9b1996d3db523776bb83e326b179f55de5d7ffc。全文未提供代码或数据仓库。", "复核需逐步固定 noise convention、MSRJD Jacobian、material-coordinate normalization、ρ0 factors、2D curl signs、Green-function boundary conditions 与 local-potential limit。Evidence status: full-text verified analytical manuscript; no independent reproduction or derivation performed."),
            sec("阅读指南", "先读 pp.1–4 的 particle/MSRJD setup；pp.4–7 Eqs. (4.20)–(4.35) 是 gauge mapping 与主作用量。pp.7–10 看 local potential、nonlocal Frank energy 和 Pe/kd constants；最后把 Discussion 中 defects/phase diagram/streaking 陈述保留为未来工作。"),
        ],
        "全文没有结果图、实验图、数值图或机制示意图；核心证据是 Eq. (4.31) 的 U(1) 有效作用量以及 Eqs. (5.22)–(5.34) 的非局域 Frank 弹性。",
        "不截取标题页或把公式截图冒充论文插图；封面使用经全文核验的题目—摘要模式。",
        [{"label": "Emergent gauge fields", "latex": r"\delta\rho=\nabla\times\mathbf A,\qquad \mathbf E=-\nabla A_0-\partial_t\mathbf A", "role": "map weak density fluctuations to a dual U(1) gauge description", "symbols": {"A0,A": "emergent gauge potentials", "delta rho": "density fluctuation", "E": "emergent electric field"}, "evidence": "paper.pdf p. 5, Eqs. (4.21)–(4.26)", "interpretation": "The mapping is valid only for small fluctuations around constant density."}, {"label": "Nonlocal Frank constants", "latex": r"K_b=\mathrm{Pe}^2,\qquad K_s=\frac{\mathrm{Pe}^2}{1+k_d}", "role": "relate orientational bend and splay stiffness to activity and interaction diffusion", "symbols": {"Pe": "Péclet number", "kd": "dimensionless diffusion-interaction constant"}, "evidence": "paper.pdf p. 9, Eqs. (5.27)–(5.28)", "interpretation": "These constants follow for the local two-body potential in the stationary small-fluctuation theory."}],
        ["paper.pdf pp. 1–4: ABP Langevin equations and MSRJD continuum construction", "paper.pdf pp. 4–7, Eq. (4.31): emergent U(1) action, charge and current", "paper.pdf pp. 7–10, Eqs. (5.21)–(5.34): local interaction and nonlocal Frank energy", "source PDF SHA-256 c00e43b481d77d469286de67d9b1996d3db523776bb83e326b179f55de5d7ffc", "Evidence status: full-text verified analytical manuscript; no independent reproduction or derivation performed."],
    ),
    card(
        "doi-10.1103-physreve.110.015003", "arXiv manuscript", "https://arxiv.org/pdf/2310.08734",
        "Space-time symmetry and nonreciprocal parametric resonance in mechanical systems", "机械系统中的时空对称性与非互易参量共振",
        "theory_numerics", "e74cbbd8d6bec74a", "Nonreciprocal Systems",
        {"doi": "10.1103/PhysRevE.110.015003", "arxiv_id": "2310.08734", "version": "arXiv v2 full text", "title": "Space-time symmetry and nonreciprocal parametric resonance in mechanical systems", "authors": ["Abhijeet Melkani", "Jayson Paulose"], "journal": "Physical Review E", "volume": "110", "issue": "1", "article": "015003", "published": "2024-07-30", "abstract": "Internal pseudo-Hermitian symmetries and a combined space-time Floquet matrix constrain parametric resonances and select one-way amplified modes in periodically modulated oscillator rings.", "comment": "ArXiv full text cross-checked with accepted-manuscript/version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Abhijeet Melkani、Jayson Paulose；Physical Review E 110, 015003 (2024)，DOI:10.1103/PhysRevE.110.015003。全文取 arXiv:2310.08734，共15页；Crossref 提供 accepted manuscript 与期刊记录，未列关联更正或撤稿。"),
            sec("研究问题", "周期调制的耦合振子可发生 exponential parametric amplification，但多模耦合时哪些频率产生共振、哪些 degeneracies 被 symmetry 保护并不直观。论文问：classical mechanics 的 real-valued/symplectic constraints 及外部 space-time translation symmetry 能否给出一般共振条件和单向行波放大选择规则？"),
            sec("背景", "把 n 个线性振子的 coordinates/momenta 写成一阶 Schrödinger-like equation 后，generator 是 purely imaginary 且 pseudo-Hermitian；time-propagation/Floquet eigenvalues 因此成 reciprocal-conjugate multiplets。相反 Krein signature 的 eigenvalues 在 unit circle 上碰撞后可离开圆，产生一增一减的 modes。", "parametric resonance 在这里等价于 Floquet multiplier modulus 偏离1。pseudo-Hermiticity breaking 是线性谱描述；它不需要物理增益元件，但周期参数调制持续向系统输入能量。"),
            sec("模型与方法", "若 modulation 满足 H(t)=S H(t+T/n) S^-1，作者定义 space-time Floquet matrix X_n=S U(T/n)，使 U(T)=X_n^n。X_n 比普通 Floquet matrix 保留更多 translation-time phase 信息，可区分 degeneracy 中的 travelling-wave basis。", "理论先在 δ→0 static limit 由正常模频率和 Krein signatures 求碰撞条件，再用有限 modulation amplitude 数值积分验证 two-oscillator dimer 和 periodic three-oscillator trimer；比较 sawtooth 与 rectangular/cosine modulations。"),
            sec("核心结果与证据", "dimer 中普通 Floquet degeneracy 会多报被 space-time symmetry 禁止的 resonances；X2 的 degeneracies 给出正确 T=2rπ/ω_i 与混合模条件。Figure 4 的有限幅值计算显示 resonance tongues 从这些 δ→0 预测频率长出，而波形改变宽度/强度但不改变极限起点。", "对环上 Bloch wavevector κ，左右行波分别满足 T=n[π(r−1)+κ]/Ω(κ) 与 T=n[πr−κ]/Ω(κ)。除 κ=π/2 外两者不同，因此调 modulation frequency 可选择传播方向。", "Figure 5 的 trimer 证明该选择：T=π/ω2 时只有逆 stiffness-wave 方向的 travelling mode 强共振；T=2π/ω2 时其 chiral partner 以更高阶、较弱方式共振。图是数值线性动力学，不是机械器件实验。"),
            sec("有效性与局限", "主分析假设 linear classical mechanics、periodic coefficients、known symmetry 和稳定 static limit；nonlinearity、saturation、noise、disorder、finite driving/measurement 与实际 amplifier efficiency 均未模拟。放大轨迹可指数增长，线性模型最终必然失效。", "数值示例只有 n=2、3 rings。incommensurate phase shift 会产生 space-time defects；open boundaries 可引入 skin effect，band topology/supercells 也被留作未来。‘适用于所有具有该对称性的系统’指谱约束形式，不保证每种系统都实现可用增益。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2310.08734；期刊：https://doi.org/10.1103/PhysRevE.110.015003。PDF SHA-256：bbb66a11726a941768dac5618fbd15915f6d509d808ff34614047f2dc163106d。全文未提供代码仓库。", "复现 Figure 5 需固定 n=3、k=10、g=3、δ=0.3/0.7、cosine modulation、T=π/ω2 或2π/ω2、cyclic shift convention、time integrator 和 Floquet eigenvector normalization。Evidence status: full-text verified theory/numerical manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–4 的 internal symmetries、Krein collision 与 Floquet spectrum；pp.5–7 定义 X_n 并看 dimer 禁戒条件。pp.7–9 Eqs. (19)–(20) 与 Figure 5 是单向放大主结果；p.10 Discussion 列出线性、边界和未来器件边界。"),
        ],
        "figure-5-one-way-modes.webp", "Figure 5", 9, "comparison",
        "三振子环的正常模、两种选择性放大时间轨迹，以及 space-time Floquet eigenvalue 的 Krein 碰撞。",
        "不同 modulation frequency 分别选中顺时针或逆时针 travelling mode，另一个手性伙伴保持不共振。",
        "Figure 5把对称性选择规则、谱碰撞和时域放大直接对应，是全文最完整的数值证据。",
        [{"label": "Space-time Floquet factorization", "latex": r"X_n=S\,U(T/n),\qquad U(T)=X_n^n", "role": "retain combined translation-time information lost in the ordinary Floquet matrix", "symbols": {"S": "cyclic spatial translation", "U": "time-propagation operator", "T": "modulation period"}, "evidence": "paper.pdf pp. 5–6, Eqs. (16)–(17)", "interpretation": "The factorization requires the stated discrete space-time symmetry and compatible periodic boundary conditions."}],
        ["paper.pdf pp. 1–4: pseudo-Hermiticity, Krein signatures and generic resonance", "paper.pdf pp. 5–8, Figures 3–4: space-time Floquet matrix and dimer tests", "paper.pdf pp. 8–10, Figure 5 and Eqs. (19)–(20): one-way travelling-mode amplification", "source PDF SHA-256 bbb66a11726a941768dac5618fbd15915f6d509d808ff34614047f2dc163106d", "Evidence status: full-text verified theory/numerical manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physreve.74.022101", "arXiv manuscript", "https://arxiv.org/pdf/cond-mat/0601038",
        "Boltzmann and hydrodynamic description for self-propelled particles", "自推进粒子的 Boltzmann 与流体力学描述",
        "theory_numerics", "f4d40a82c00f2e86", "Active Matter",
        {"doi": "10.1103/PhysRevE.74.022101", "arxiv_id": "cond-mat/0601038", "version": "arXiv full text", "title": "Boltzmann and hydrodynamic description for self-propelled particles", "authors": ["Eric Bertin", "Michel Droz", "Guillaume Grégoire"], "journal": "Physical Review E", "volume": "74", "issue": "2", "article": "022101", "published": "2006-08-02", "abstract": "A dilute binary-collision Boltzmann equation is closed near onset to derive density and momentum hydrodynamics for aligning self-propelled particles and predict a finite-wavelength instability of homogeneous order.", "comment": "ArXiv full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Eric Bertin、Michel Droz、Guillaume Grégoire；Physical Review E 74, 022101 (2006)，DOI:10.1103/PhysRevE.74.022101。全文取 arXiv:cond-mat/0601038，共5页；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "Vicsek-like self-propelled particles 会从无序态产生 collective motion，但 phenomenological hydrodynamics 的系数与 microscopic rules 关系不明确。论文问：在稀薄、二元碰撞近似下，能否从 one-particle phase-space distribution 推出 density/momentum equations、相变阈值与 ordered-state instability？"),
            sec("背景", "粒子以单位速度飞行，按 Poisson rate λ 自扩散转角；两粒子距离小于 d0 时，把方向更新为平均方向加噪声。作者先比较 binary-collision 与已有 multi-particle model，说明两者都出现 density stripe 和 discontinuous finite-size transition signatures。", "Figure 2 的两套 microscopic dynamics 并不完全相同：binary simulation 使用 discrete time 与非 Gaussian noise，system sizes 也不同。它支持 qualitative phenomenology，而非同参数逐点验证 Boltzmann 方程。"),
            sec("模型与方法", "Boltzmann equation 包含 free streaming、self-diffusion collision integral 和 binary alignment collision integral。取 angular Fourier modes f_k；f_0=ρ，f_1=w=ρu。靠近 onset 假设 f_k=O(ε^|k|)、f_1=O(ε)，并作长波/慢时间展开到 ε³，消去 f_2。", "所得 continuity equation 与 w equation 含 effective pressure、local Landau relaxation (μ−ξw²)w、viscosity ν∇²w、advection γ(w·∇)w 和 compressibility feedback −κ(∇·w)w；各系数由 density、noise 和 collision rate 显式给出。"),
            sec("核心结果与证据", "Figure 2 显示 binary 与 multi-particle simulations 的 order parameter/Binder cumulant 都在临界附近突变，binary model 的 order-parameter PDF 呈双峰，并形成横向密度 stripe。这支持二元碰撞模型抓住第一阶样有限尺寸现象。", "均匀无序态在 μ=0 处失稳，给出 density–noise transition line；homogeneous ordered solution w0=√(μ/ξ)e 虽对均匀扰动稳定，却有 longitudinal finite-wavelength instability。小 q 下 Re s 的 q²系数为正，因此更复杂 bands/structures 必须介入。", "Eq. (8) 与 Toner–Tu 允许结构相容并给出 microscopic coefficients，但缺少该截断阶次之外的 (w·∇)²w 等项。论文没有数值积分 hydrodynamic PDE 来检验最终非线性结构；后续结构被明确留为待研究。"),
            sec("有效性与局限", "Boltzmann description 原则上限于 low density、molecular chaos、binary collisions；closure 还要求 weak anisotropy、small u 和 length scales≫d0。finite-wavelength instability 可把系统推到 closure 失效的强极化/强梯度区。", "Figure 2 使用有限系统和相近而非完全相同的 microscopic rules；negative Binder dip/双峰支持 discontinuity 但没有 thermodynamic-limit finite-size scaling。论文预测 homogeneous order 不稳定，不能把 μ=0 line 当作最终稳态相界。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/cond-mat/0601038；期刊：https://doi.org/10.1103/PhysRevE.74.022101。PDF SHA-256：54b5c25bfcc8881e0fe68b73d1d7edb517a998544b22425201769187299dab2d。全文未提供代码仓库。", "复现需固定 d0=1/2、λ、p0/p noises、density、L/N、binary update rule、order parameter/Binder estimator、Fourier convention 与 ε power counting。Evidence status: full-text verified theory/microscopic simulation manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 2，区分 binary 与 multi-particle evidence；pp.2–3 Eqs. (1)–(13) 是 Boltzmann-to-hydrodynamics closure。p.3 Figure 3 与 Eqs. (14)–(18) 给 onset/instability；最后读 pp.4–5，保留 low-density、小极化和未解析 nonlinear state 的限制。"),
        ],
        "figure-2-transition-comparison.webp", "Figure 2", 2, "comparison",
        "二元碰撞与多粒子模型的序参量、Binder cumulant、临界 PDF 和密度条带比较。",
        "两类 microscopic rules 都表现出临界突变与密度 stripe，支持使用 binary Boltzmann model 研究近 onset 机制。",
        "Figure 2是微观模拟与解析二元碰撞假设之间唯一直接桥梁，并同时展示双峰 PDF 与空间结构。",
        [{"label": "Hydrodynamic momentum equation", "latex": r"\partial_t\mathbf w+\gamma(\mathbf w\!\cdot\!\nabla)\mathbf w=-\frac12\nabla(\rho-\kappa w^2)+(\mu-\xi w^2)\mathbf w+\nu\nabla^2\mathbf w-\kappa(\nabla\!\cdot\!\mathbf w)\mathbf w", "role": "close the dilute Boltzmann hierarchy near the onset of polar order", "symbols": {"rho": "number density", "w": "momentum/polarization density", "mu,xi": "local ordering coefficients", "nu": "viscosity-like coefficient"}, "evidence": "paper.pdf p. 3, Eq. (8)", "interpretation": "The closure is controlled only for weak anisotropy, long wavelengths and low density near onset."}],
        ["paper.pdf pp. 1–2, Figure 2: binary versus multiparticle simulations", "paper.pdf pp. 2–3, Eqs. (1)–(13): Boltzmann equation and hydrodynamic closure", "paper.pdf pp. 3–4, Figure 3 and Eqs. (14)–(18): onset and finite-wavevector instability", "source PDF SHA-256 54b5c25bfcc8881e0fe68b73d1d7edb517a998544b22425201769187299dab2d", "Evidence status: full-text verified theory/microscopic simulation manuscript; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed = []
    for item in CARDS:
        paper_id = str(item["arxiv_id"])
        (OUT / f"{paper_id}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        installed.append(paper_id)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
