#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 039."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-physrevlett.131.047101", "arXiv v3 manuscript", "https://arxiv.org/pdf/2302.11514",
        "Two-Dimensional Crystals far from Equilibrium", "远离平衡的二维晶体", "numerical",
        "e848907cc5cce3a4", "Condensed Matter",
        {"doi":"10.1103/PhysRevLett.131.047101","arxiv_id":"2302.11514","version":"arXiv v3 full text","title":"Two-Dimensional Crystals far from Equilibrium","authors":["Leonardo Galliano","Michael E. Cates","Ludovic Berthier"],"journal":"Physical Review Letters","volume":"131","issue":"4","article":"047101","published":"2023-07-25","abstract":"Center-of-mass-conserving random-organization dynamics produces a two-dimensional active crystal with genuine long-range translational order, suppressed phonons, and hyperuniform density fluctuations.","comment":"ArXiv v3 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Leonardo Galliano、Michael E. Cates、Ludovic Berthier；PRL 131, 047101 (2023)。全文 arXiv:2302.11514v3 共6页；Crossref 未列更正或撤稿。"),
            sec("研究问题","Mermin–Wagner 机制使二维平衡晶体的长波声子涨落发散，只允许准长程平移序。论文问：若微观更新破坏详细平衡和能量均分，但仍保持各向同性与质心守恒，二维粒子能否形成真正的长程平移序？"),
            sec("背景","模型源于周期驱动悬浮液的 random organization：低密度最终没有重叠并进入 absorbing state，高密度保持有限 activity。作者把临界点推到高 packing fraction，使 absorbing–active criticality 与六角晶体有序在同一区域发生。","这里的“违反 Mermin–Wagner”不是否定定理，而是越出其平衡、能量均分假设；模型也没有热力学温度或 Hamiltonian。"),
            sec("模型与方法","N 个直径 σ 的圆盘置于周期方盒；每一离散步把每对重叠粒子沿连心线反向移动同一随机距离 [0,ε]，从而保持质心。控制参数为 packing fraction φ 和 ε，activity f 是当步移动粒子比例。","作者从随机或完美有序初态模拟至 steady state，最大 N 约10^5；用 Ψ6、g6(r)、pair correlation g(r)、MSD、位移结构因子 Su(q) 与静态 S(q) 区分 polycrystal、长程晶体和 hyperuniformity，并做有限尺寸 critical scaling。"),
            sec("核心结果与证据","ε=0.1 时临界 packing fraction 为 φc=0.8226。activity 衰减 α=0.42、稳态 β=0.64、susceptibility γ=0.49、relaxation ν∥=1.3 以及空间长度 ν⊥=0.8 均与 conserved directed percolation 数值相容；作者同时提醒 CDP 与 DP 指数很接近，数值上难严格区分。","φ<φc 的吸收构型是有限晶粒 polycrystal；越过 φc 后 Ψ6 跳到接近1，g 与 g6 的相关长度共同发散。Figure 4 显示 active crystal 的 MSD plateau 不随 L 增长，Su(q→0) 有限而非平衡声子的 q^−2 发散，故长波 displacement modes 被压低。","静态 S(q) 具有幅度随 N 增长的 Bragg peaks，同时 diffuse background 在低 q 满足 S(q)∼q²。这把稳定长程平移序与 hyperuniform density fluctuations 连接起来，而不是只凭视觉上的单晶构型。"),
            sec("有效性与局限","结果来自二维、单分散、无惯性、特定重叠更新与有限 ε 的理想数值模型；它没有直接模拟剪切实验、Brownian colloids 或真实 granular dissipation。临界指数一致性支持但不能唯一确认 CDP universality class。","高密度有限盒需要极长 coarsening 才形成单晶；有限运行时间可能把慢态当作稳态。作者证明的是该规则下无能量均分导致 phonon suppression，不代表任意 nonequilibrium drive 都稳定二维晶体。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2302.11514；期刊：https://doi.org/10.1103/PhysRevLett.131.047101。PDF SHA-256：5385c4c3ed51befe69ae4101350badd3ff4bd2e0bb91e9c5939496596d5916d0。全文未给代码仓库。","复现需固定 ε、φ、N/L、overlap pair 更新顺序、随机位移抽样、初态和稳态容差；分别复算 f、χ、τr、Ψ6、g/g6、MSD、Su(q) 与 S(q)，并报告低 q 和尺寸拟合区间。Evidence status: full-text verified simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Figure 1 和更新规则，再看 p.2 Figure 2 的临界指数。p.3 Figure 3 建立结构长度与临界性的耦合；p.4 Figure 4 是长程序、phonon suppression 和 hyperuniformity 的关键证据，结论页用于核对适用边界。"),
        ],
        "figure-4-crystal-hyperuniformity.webp", "Figure 4", 4, "data_plot",
        "active crystal 的 MSD、位移结构因子与静态结构因子随尺度和波数的变化。",
        "MSD plateau 不随系统尺寸增长，Su(q) 不出现 q^−2 发散，而 S(q) 在低 q 约按 q² 消失。",
        "Figure 4 同时检验晶格稳定、长波声子抑制和超均匀性，是越出平衡二维晶体限制的直接数值证据。",
        [{"label":"Finite displacement criterion","latex":r"\Delta^2(\infty)\sim\int_{2\pi/L}^{\Lambda}S_u(q)q^{d-1}\,dq","role":"test whether long-wavelength displacement modes destroy translational order","symbols":{"S_u(q)":"displacement structure factor","L":"linear system size","Lambda":"ultraviolet cutoff"},"evidence":"paper.pdf p. 4, Eq. (9) and Figure 4","interpretation":"A finite low-q Su makes the two-dimensional integral converge, unlike equilibrium equipartition Su proportional to q^-2."}],
        ["paper.pdf pp. 1–2, Figures 1–2 and Eqs. (1)–(3): dynamics and absorbing transition","paper.pdf p. 3, Figure 3 and Eqs. (4)–(7): orientational/translational ordering length","paper.pdf p. 4, Figure 4 and Eqs. (8)–(9): MSD, phonon suppression and hyperuniformity","source PDF SHA-256 5385c4c3ed51befe69ae4101350badd3ff4bd2e0bb91e9c5939496596d5916d0","Evidence status: full-text verified simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.131.238302", "arXiv v3 manuscript", "https://arxiv.org/pdf/2208.06831",
        "Pulsating Active Matter", "脉动主动物质", "theory_numerics", "56d6bf41f3b7f24e", "Active Matter",
        {"doi":"10.1103/PhysRevLett.131.238302","arxiv_id":"2208.06831","version":"arXiv v3 full text","title":"Pulsating Active Matter","authors":["Yiwei Zhang","Étienne Fodor"],"journal":"Physical Review Letters","volume":"131","issue":"23","article":"238302","published":"2023-12-08","abstract":"A minimal model of repulsive particles with periodically varying sizes shows that competition between mechanical pulsation and local synchronization generates planar, spiral, circular, and turbulent deformation waves.","comment":"ArXiv v3 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Yiwei Zhang、Étienne Fodor；PRL 131, 238302 (2023)。全文 arXiv:2208.06831v3 共6页；Crossref 未列更正或撤稿。"),
            sec("研究问题","许多组织即使几乎不平移，细胞仍会持续收缩、膨胀并传播 deformation waves。论文问：不引入化学反应或自推进，仅让密集排斥粒子的尺寸周期脉动并局域同步，是否足以自发产生平面、螺旋、环形波和缺陷湍流？"),
            sec("背景","传统 active matter 常以 self-propulsion 注能；本文把 activity 放在 particle size σ(θ) 的周期变化上。密集体系在固定总面积中必须协调膨胀和收缩，因此 repulsion 与 phase synchronization 可能把局部脉动转化为空间传播。","与 reaction–diffusion systems 的相似是 pattern/hydrodynamic level 的类比；微观模型没有化学反应，不能直接当作具体组织的生化模型。"),
            sec("模型与方法","二维 N 粒子位置服从 overdamped Langevin dynamics，排斥势只在归一距离 a<1 时作用；粒径 σ(θ)=σ0(1+λ sinθ)/(1+λ)。phase θ 以频率 ω 驱动，受局域 Kuramoto-like ε sin(θi−θj)、repulsion-induced phase force 和噪声 Dθ 共同演化。","扫描平均密度 ρ0 与同步强度 ε，用全局同步序参量 r、packing fraction φ 和 phase current ν 分类 cycling、arrested、wave/defect states；再对局域复序参量 A(r,t) coarse-grain，得到带 repulsion-induced gauge-symmetry-breaking term 的 complex Ginzburg–Landau-like 方程。"),
            sec("核心结果与证据","Figure 2 给出两个彼此分离的有序区：ρ0<约1.5 时粒子可同步 cycling，ρ0>约1.8 时密堆积造成 arrested order；大 ε、中等密度之间均匀 phase profile 失稳，出现平面、螺旋、圆形波或不断重组的 defect turbulence。","在一条边界上 P(r) 变成 bimodal 且有明显 hysteresis，指示 discontinuous transition；另一边界 P(r) 保持 unimodal、hysteresis 弱，转变连续。Figure 3 还显示 φ 与 current ν 相差约四分之一周期，pattern state 的 oscillation amplitude 比全局同步态小。","coarse-grained Eq. (7) 重现 disorder、clockwise/counter-clockwise cycling 与 arrest 的 homogeneous phase boundaries；加入噪声后在 cycling 与 arrest 之间产生移动缺陷。但该场论没出现微观模拟中的 nonmotile-defect waves，作者据此指出被忽略的 density fluctuations 对稳定这些结构可能重要。"),
            sec("有效性与局限","这是 minimal soft-particle model，不含细胞形状、division、extrusion、substrate friction 或 mechanochemical feedback。U、局域同步、λ 和噪声选择会移动 phase boundaries；结果支持一个通用机制而不是对特定组织的定量预测。","hydrodynamics 为简化而设置位置 mobility coupling μ=0，并作局域与低阶梯度 closure；它只定性连接 reaction–diffusion phenomenology。有限系统、长寿命 metastability 和 phase classification 也会影响 discontinuous/continuous 判断。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2208.06831；期刊：https://doi.org/10.1103/PhysRevLett.131.238302。PDF SHA-256：58b1d7f7c703a3a0fca6721c8a9e46b19681a078deba0d03a46feff3db6ea07d。全文未给代码仓库。","复现需固定 N/L、ρ0、σ0、λ、ω、U0、μ/D、μθ/Dθ、ε、积分步长、初态和 averaging time；输出 r、P(r)、φ、ν、defect trajectories 与波型，并独立检查 coarse-grained stability。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Eqs. (1)–(5) 与 Figures 1–2 了解机制和相图；pp.3–4 Figure 3 与 Eq. (7) 连接 microscopic currents 和 hydrodynamics。最后读 p.5 discussion，保留 field closure 没能稳定 nonmotile defects 的限制。"),
        ],
        "figure-2-pam-phase-diagram.webp", "Figure 2", 2, "phase_diagram",
        "密度—同步强度相图，以及跨越两条有序—无序边界时同步序参量分布和 hysteresis。",
        "低密度 cycling 与高密度 arrest 构成两个有序区，中间区域由 repulsion–synchronization competition 产生 deformation waves。",
        "Figure 2 同时给出全局 phase inventory 和两类不同转变的分布证据。",
        [{"label":"Pulsating particle size","latex":r"\sigma(\theta_i)=\sigma_0\frac{1+\lambda\sin\theta_i}{1+\lambda}","role":"encode individual mechanical pulsation","symbols":{"theta_i":"particle phase","lambda":"pulsation amplitude","sigma_0":"largest diameter"},"evidence":"paper.pdf p. 2, Eq. (2)","interpretation":"Collective waves arise only after coupling this size cycle to repulsion and local synchronization."}],
        ["paper.pdf pp. 1–2, Figures 1–2 and Eqs. (1)–(5): pulsating-particle model and phase diagram","paper.pdf pp. 3–4, Figure 3 and Eqs. (6)–(7): current statistics and hydrodynamic closure","paper.pdf pp. 4–5, Figure 4 and Discussion: field phases and missing density-fluctuation mechanism","source PDF SHA-256 58b1d7f7c703a3a0fca6721c8a9e46b19681a078deba0d03a46feff3db6ea07d","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.132.118301", "published open-access manuscript", "https://ins.sjtu.edu.cn/people/hpzhang/papers/PhysRevLett.132.118301.pdf",
        "Emergent Chirality and Hyperuniformity in an Active Mixture with Nonreciprocal Interactions", "非互易相互作用活性混合物中的涌现手性与超均匀性", "theory_experiment", "b3ef2f3ab49a8c05", "Nonreciprocal Systems",
        {"doi":"10.1103/PhysRevLett.132.118301","version":"published open-access full text","title":"Emergent Chirality and Hyperuniformity in an Active Mixture with Nonreciprocal Interactions","authors":["Jianchao Chen","Xiaokang Lei","Yalun Xiang","Mengyuan Duan","Xingguang Peng","H. P. Zhang"],"journal":"Physical Review Letters","volume":"132","issue":"11","article":"118301","published":"2024-03-14","abstract":"Experiments with 48 programmable robots and larger simulations show that an angular-speed threshold stabilizes collective chiral motion under nonreciprocal alignment, while repulsion drives an absorbing-active transition with disordered hyperuniformity at criticality.","comment":"Institutional copy of the published full text cross-checked with Crossref metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Jianchao Chen、Xiaokang Lei、Yalun Xiang、Mengyuan Duan、Xingguang Peng、H. P. Zhang；PRL 132, 118301 (2024)。开放获取期刊全文共6页；Crossref 未列更正或撤稿。"),
            sec("研究问题","二物种中 A 对 B 对齐而 B 对 A 反对齐时，非互易作用可诱发 time-dependent chirality，但早期机器人实验只见短暂手性态。论文问：有限角速度阈值能否稳定 collective chiral motion，以及局域排斥如何在手性相内产生 absorbing–active transition 与 hyperuniform structure？"),
            sec("背景","非互易相互作用打破 action–reaction symmetry，在主动胶体、细胞和反馈机器人中常见。二物种 Vicsek-like orientation model 以 JAB≠JBA 表示互易性破缺；J+=(JAB+JBA)/2 和 J−=(JAB−JBA)/2 分离 reciprocal 与 nonreciprocal parts。","实验平台使相互作用可编程，但 robot boundary collisions 和有限转向能力是真实干扰。作者只把未被这些碰撞破坏前的 steady states 纳入主实验相图。"),
            sec("模型与方法","48 台机器人在 5.4 m×5 m 场地以定速运动，16-camera motion capture 以300 Hz追踪，中央服务器计算角速度并以5 Hz广播。同物种 JAA=JBB>0；异物种 JAB、JBA 可独立设置，近距离 R 内加入避碰转向。","命令角速度经 θdot=sgn(ω)min(|ω|,Ω) 截断。作者用 two-robot fixed points 推导进入 chiral state 的概率和 phase boundary，再以 48-robot experiments 与 periodic simulations 检验；更大 N=2048/8192 模拟扫描 density φ、repulsion range R，并测 MSD、diffusion D、S(q) 和 number variance。"),
            sec("核心结果与证据","当 |J+| 大时得到 flocking 或 antiflocking；nonreciprocal part 占优时，所有机器人以阈值 Ω 共同画圆并形成稳定 chiral state。没有阈值时，两机器人只有完全非互易 J+=0 才可持续手性；阈值产生新的稳定 fixed points，Eq. (4) 的边界与 48-robot simulation phase diagram 及实验符号相符。","Figure 3 显示 chiral region 内两物种各自 polar ordered，平均 heading difference 约0.55π；mixed boundary 附近可随机切换。该稳定性是有限观测窗内结论，长期 robot–boundary interactions 仍会改变 flocking/antiflocking dynamics。","Figure 4 中增大 φ 或 R 把 chiral system 从 MSD plateau 的 absorbing state 推至 diffusive active state。临界附近 S(q)∼q^0.45，而大窗口 number variance 约 L^−2.45，显示 disordered hyperuniform state；这来自大规模 simulations，不是48台机器人直接测得的低 q 极限。"),
            sec("有效性与局限","实验机器人数量仅48、边界有限且控制更新5 Hz；hyperuniform exponent 来自 periodic large-N simulation。角速度 threshold 是硬截断的工程机制，不能自动外推到连续 torque response 的细胞或胶体。","相界 Eq. (4) 来自简化 few-robot reasoning；noise、repulsion、N 和 Ω 会影响边界附近状态。临界指数拟合范围有限，文中没有建立 absorbing transition 的完整 universality-class exponent set。"),
            sec("复现与资源","全文：https://ins.sjtu.edu.cn/people/hpzhang/papers/PhysRevLett.132.118301.pdf；期刊：https://doi.org/10.1103/PhysRevLett.132.118301。PDF SHA-256：72bd8624ce7d85b211320f320b657c4d5e370ead8599cfe15a7662d01832826a。","复现需固定 JAA/JBB/JAB/JBA、Ω、v0、R、边界规则、tracking/broadcast rates、initial headings 和 observation window；模拟还需固定 N/W、noise、repulsion law、稳态判据以及 S(q)/number-variance fit ranges。Evidence status: full-text verified experiment/simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Figure 1 和 Eqs. (1)–(3) 理解机器人闭环；p.3 Figure 2 看 threshold-stabilized fixed points，p.4 Figure 3 对照实验与相图。pp.4–5 Figure 4 是 absorbing–active 与 hyperuniformity 的数值证据，注意和48-robot实验分开。"),
        ],
        "figures-3-4-chiral-hyperuniform.webp", "Figures 3–4", 4, "comparison",
        "48机器人集体态相图与大规模模拟中的 absorbing–active 边界、结构因子和密度涨落。",
        "角速度阈值稳定手性区；增加密度或排斥范围触发 active diffusion，临界密度涨落呈超均匀标度。",
        "并置 Figures 3–4 可清楚区分实验验证的集体手性与仅在大规模模拟检验的超均匀临界结构。",
        [{"label":"Angular-speed threshold","latex":r"\dot\theta_m=\operatorname{sgn}(\omega_m)\min(|\omega_m|,\Omega)","role":"stabilize collective chiral fixed points","symbols":{"omega_m":"unthresholded interaction command","Omega":"maximum angular speed"},"evidence":"paper.pdf p. 2, Eq. (3)","interpretation":"The hard saturation is a programmable robot constraint and the mechanism responsible for the widened chiral region."}],
        ["paper.pdf pp. 1–2, Figure 1 and Eqs. (1)–(3): robot apparatus and programmed interactions","paper.pdf pp. 3–4, Figures 2–3 and Eq. (4): threshold mechanism and collective-state phase diagram","paper.pdf pp. 4–5, Figure 4: absorbing-active transition and hyperuniform scaling","source PDF SHA-256 72bd8624ce7d85b211320f320b657c4d5e370ead8599cfe15a7662d01832826a","Evidence status: full-text verified experiment/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.132.268301", "arXiv v1 manuscript", "https://arxiv.org/pdf/2404.10608",
        "Swirling Due to Misaligned Perception-Dependent Motility", "由感知依赖运动方向错位引起的旋涡", "theory_numerics", "dab016a78fd58743", "Active Matter",
        {"doi":"10.1103/PhysRevLett.132.268301","arxiv_id":"2404.10608","version":"arXiv v1 full text","title":"Swirling Due to Misaligned Perception-Dependent Motility","authors":["Rodrigo Saavedra","Gerhard Gompper","Marisol Ripoll"],"journal":"Physical Review Letters","volume":"132","issue":"26","article":"268301","published":"2024-06-25","abstract":"Two-dimensional Langevin simulations and conservation-law estimates show that offsetting a particle's perception cone from its propulsion direction creates cohesive clusters with controlled persistent rotation and tunable fluid-like or solid-like interiors.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Rodrigo Saavedra、Gerhard Gompper、Marisol Ripoll；PRL 132, 268301 (2024)。全文 arXiv:2404.10608v1 共6页；Crossref 未列更正或撤稿。"),
            sec("研究问题","许多群体旋转模型依赖 intrinsic chirality、显式 alignment、attraction 或 external torque。论文问：若粒子只感知邻居位置，并让 perception cone 轴与 propulsion direction 固定错开 γ，配合 thresholded on/off motility，是否即可形成有指定旋向的 cohesive swirl？"),
            sec("背景","vision-type perception 本身产生 asymmetric、nonreciprocal interactions，因为 i 看见 j 不保证 j 看见 i。已有 feedback-controlled colloids 能按视觉规则开关推进；本文进一步把感知轴相对运动方向偏转，让 inward-selection 同时产生切向偏置。","模型目标是展示可实现的 self-organization strategy，不是拟合某一动物群或已完成实验。"),
            sec("模型与方法","N=1000 个二维 Brownian particles 以 overdamped Langevin dynamics 演化，WCA 排斥；视锥半角 α、范围 rc，感知量 Pi 为视锥内 1/rij 的和。归一化 qi 超过 threshold q* 时以 v0 推进，否则静止；感知轴相对推进 ei 偏转 γ。","从圆形均匀初态用 Euler Δt=10^−5 模拟，默认 Péclet=4.8。作者测总/active density、tangential polarization 和 angular-velocity radial profiles，并用 soft-interface tanh fit 提取 cluster radius Rc、bulk density ρb、bulk angular speed ωb；基于粒子守恒和边界通量推导解析估计。"),
            sec("核心结果与证据","γ=0 时得到 compact non-swirling cluster；γ>0 固定旋向。低 q* 时中心广泛 active、内部较 fluid-like；较高 q* 只选择向内感知的表层粒子，steric coupling 把 passive core 拖动成近 solid-body rotation。γ 接近 π/2 时径向 cohesion 消失，cluster 溶解。","Figure 3 的 radial profiles 显示 density 在核心近常数而界面软衰减；active distribution、tangential polarization 和 angular velocity 随 q* 改变，区分中心活跃和外层驱动两类 swirl。","Figure 4 中 Rc 在广泛 γ 区间近恒定，极大错位时急增并解体；ωb 小 γ 近线性增加，随后达到最大再下降。解析 Rc 只用 effective diffusion 作拟合参数，在 compact regime 与模拟定量吻合；dilute regime 因 boundary polarization approximation 仅定性。"),
            sec("有效性与局限","核心证据是 idealized simulations 与近似守恒理论，没有机器人或胶体实验验证。on/off threshold、固定视锥、二维圆形初态、WCA、Pe 和 N 会改变 cluster morphology；定向错位在现实系统中的 sensing/actuation delay 未建模。","解析式假定圆形稳定 cluster、边界加入和扩散离开平衡，并把复杂 activity 平均进 Deff；接近 dissolution 或稀疏 cluster 时近似变差。论文展示 persistent swirling，但没有系统评估噪声扰动下的长期控制鲁棒性。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2404.10608；期刊：https://doi.org/10.1103/PhysRevLett.132.268301。PDF SHA-256：d28730047ecc5661f9ce8552b88236c44e7529f4077ad0db3573a5a2cb9dc8c9。全文未给代码仓库。","复现需固定 N、α、rc、γ、q* normalization、v0、Dt/Dr、Pe、WCA、Δt=10^−5、initial radius 和 independent seeds；复算 activity maps、radial binning、tanh fits 与 Deff calibration。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Figure 1 和 Eqs. (1)–(2) 建立感知几何；p.3 Figure 2 看四类 cluster，p.4 Figures 3–4 检查 radial profiles 和解析拟合。结论段明确实验实现只是建议，不能写成已实现 microrobot demonstration。"),
        ],
        "figures-3-4-cluster-profiles.webp", "Figures 3–4", 4, "comparison",
        "不同错位角与感知阈值下的密度、活跃粒子、切向取向、角速度径向剖面及解析—模拟比较。",
        "感知错位建立切向偏置；cluster 可由外层 active particles 驱动近刚体旋转，过大错位则失去凝聚。",
        "Figures 3–4 把视觉构型从定性 snapshot 推进为可拟合的半径和角速度机制检验。",
        [{"label":"Cluster radius estimate","latex":r"R_c(q^*,\gamma)=\frac{D_{\rm eff}(q^*)}{A(q^*)}\left(\frac{1}{\cos\gamma}-1\right)+R_{\gamma0}(q^*)","role":"balance diffusive loss against active influx at the cluster boundary","symbols":{"D_eff":"activity-enhanced diffusion","A":"threshold-dependent influx factor","gamma":"perception-propulsion misalignment"},"evidence":"paper.pdf p. 4, Eq. (4) and Figure 4","interpretation":"Agreement is quantitative for compact clusters and only qualitative for dilute cases."}],
        ["paper.pdf pp. 1–2, Figure 1 and Eqs. (1)–(2): misaligned perception rule and Langevin dynamics","paper.pdf p. 3, Figure 2: stationary cluster morphologies and activity maps","paper.pdf p. 4, Figures 3–4 and Eqs. (3)–(4): radial fits and conservation-law predictions","source PDF SHA-256 d28730047ecc5661f9ce8552b88236c44e7529f4077ad0db3573a5a2cb9dc8c9","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.133.078301", "arXiv v2 manuscript", "https://arxiv.org/pdf/2306.03513",
        "Defect Solutions of the Nonreciprocal Cahn-Hilliard Model: Spirals and Targets", "非互易 Cahn–Hilliard 模型的缺陷解：螺旋与靶纹", "theory_numerics", "4e61e4db8c2718bf", "Nonreciprocal Systems",
        {"doi":"10.1103/PhysRevLett.133.078301","arxiv_id":"2306.03513","version":"arXiv v2 full text","title":"Defect Solutions of the Nonreciprocal Cahn-Hilliard Model: Spirals and Targets","authors":["Navdeep Rana","Ramin Golestanian"],"journal":"Physical Review Letters","volume":"133","issue":"7","article":"078301","published":"2024-08-15","abstract":"Analytical defect ansatzes and large-scale simulations of the nonreciprocal Cahn-Hilliard model reveal stable charged spirals and neutral targets, followed by a disorder-order transition to globally polar traveling waves near alpha=0.28.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Navdeep Rana、Ramin Golestanian；PRL 133, 078301 (2024)。全文 arXiv:2306.03513v2 共15页含补充材料；Crossref 未列更正或撤稿。"),
            sec("研究问题","nonreciprocal Cahn–Hilliard (NRCH) 已知能产生 traveling phases，但 conserved scalar fields 中的局域 topological defects 尚未系统刻画。论文问：模型允许哪些稳定 spiral/target solutions，它们如何选择远场波数，并在增强 nonreciprocity 时怎样组织成 defect networks 或 traveling waves？"),
            sec("背景","把两个守恒标量组合成 complex field φ=φ1+iφ2 后，线性 nonreciprocity α 使一组分“追逐”另一组并破坏 parity/time reversal。均匀 plane wave 的 amplitude 满足 R²=1−q²，并受 Eckhaus stability 限制。","拓扑 charge m 描述绕 core 的 phase winding；target m=0 为中性，spiral m=±1 有手性。这里的“polar order”是复场梯度构造的 current-like order，不是粒子朝向。"),
            sec("模型与方法","无量纲 NRCH 写作 ∂tφ=∇²[(-1+iα)φ+|φ|²φ−∇²φ]。作者采用 φ(r,t)=R(r)exp{i[mθ+Z(r)−ωt]} 的 defect ansatz，求 radial amplitude R 与 local wavenumber k=Z′，并分析远场 plane-wave stability。","大型 pseudo-spectral simulations 从随机场 quench，扫描 α 与 L=1600、3200、6400；识别 spiral/target cores、defect density、target fraction 和全局 polar order Jbar，并以不同 L 的 ensemble 测进入 traveling-wave state 的比例。"),
            sec("核心结果与证据","稳定孤立解包括 neutral target m=0 和 unit-charge spiral m=±1；|m|>1 会裂成 spiral pairs。远场选择 k∞=C√α，C 约0.76 (spiral) 或0.7 (target)，R∞²=1−k∞²；这给出 defect solution 消失的理论 crossover α×，加上 Eckhaus 条件后约0.58。","实际随机初态在更小 αc 转变。Figure 3 对 L=6400 展示 α=0.1–0.25 的 quasi-stationary defect networks 和 α=0.3–0.8 的 noisy traveling bands；Jbar 在阈值处陡升，多尺寸 ensemble 给 αc=0.28±0.01。","低 α 以孤立/束缚同号 spirals 为主；接近 αc 时 neutral targets 比例上升且间距更大，defect density 随 α 降低并在 traveling phase 消失。αc<α× 说明 random-network collective transition 不能仅由孤立 defect existence limit 预测。"),
            sec("有效性与局限","作者明确称 defect networks 为 quasi-stationary 且对初态敏感；临界附近 fluctuations 可持续很久，有限 L 会在 α略低于 αc 时误触发 traveling waves。αc 是给定方程、quench 和数值判据的估计。","主模型只保留 linear、purely nonreciprocal coupling 并恢复 φ-space rotational symmetry；补充材料才讨论 reciprocal term。非线性 nonreciprocity、守恒噪声以及 isolated defects 对小扰动的完整 stability 留待未来。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2306.03513；期刊：https://doi.org/10.1103/PhysRevLett.133.078301。PDF SHA-256：3eee550e156dabf25bad7fbd50371a59bb5cd86ca850304f085a2ce4f57a4724。全文未给代码仓库。","复现需固定 spectral grid、L/N、time step、dealiasing、random-field spectrum/seeds、run time、core classifier、Jbar averaging 和 traveling-state threshold；分别验证 radial shooting、k∞ fit、Eckhaus bound 与 finite-size transition fractions。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Eqs. (1)–(3) 和 Figure 2 的孤立缺陷；p.3 Figure 3 是 αc 的核心证据，p.4 Figure 4 区分 spiral/target composition。再查 pp.6–15 的数值、渐近解、reciprocal coupling 与 noise 细节。"),
        ],
        "figure-3-defect-wave-transition.webp", "Figure 3", 3, "phase_diagram",
        "随非互易强度增加，螺旋/靶纹缺陷网络转为全局有序 traveling waves，并给出多尺寸转变态比例。",
        "低 α 保持准稳态 defect networks；α≥约0.28 时大多数模拟进入 traveling waves，polar order 陡升。",
        "Figure 3 直接连接实空间模式、序参量与 finite-size transition probability，是 αc=0.28±0.01 的完整证据。",
        [{"label":"Defect ansatz","latex":r"\phi(r,t)=R(r)e^{i[m\theta+Z(r)-\omega t]},\qquad k_\infty=C\sqrt{\alpha}","role":"classify spiral and target defects and their selected far-field wave number","symbols":{"m":"topological charge","R":"radial amplitude","Z":"radial phase","alpha":"nonreciprocity strength"},"evidence":"paper.pdf p. 2, Eq. (3) and Figure 2","interpretation":"m=0 targets and m=±1 spirals are stable in the studied model; the isolated-defect crossover exceeds the collective transition alpha_c."}],
        ["paper.pdf pp. 1–2, Figures 1–2 and Eqs. (1)–(3): NRCH and isolated defect solutions","paper.pdf pp. 3–4, Figures 3–4: finite-size disorder-order transition and defect composition","paper.pdf pp. 6–15: numerics, asymptotics, reciprocal coupling and noise checks","source PDF SHA-256 3eee550e156dabf25bad7fbd50371a59bb5cd86ca850304f085a2ce4f57a4724","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed = []
    for item in CARDS:
        pid = str(item["arxiv_id"])
        (OUT / f"{pid}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        installed.append(pid)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
