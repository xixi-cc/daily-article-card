#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 037."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card
from install_full_collection_batch_036 import title_card


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-physreve.83.030901", "arXiv v2 manuscript", "https://arxiv.org/pdf/1006.1825",
        "Kinetic theory of flocking: Derivation of hydrodynamic equations", "集群运动的动力学理论：流体力学方程的推导",
        "theory_numerics", "11c38ab40d550f7d", "Active Matter",
        {"doi": "10.1103/PhysRevE.83.030901", "arxiv_id": "1006.1825", "version": "arXiv v2 full text", "title": "Kinetic theory of flocking: Derivation of hydrodynamic equations", "authors": ["Thomas Ihle"], "journal": "Physical Review E", "volume": "83", "issue": "3", "article": "030901", "published": "2011-03-16", "abstract": "An Enskog-type kinetic equation for the discrete-time Vicsek model yields explicit third-order hydrodynamic coefficients, a mean-field transition line, and a longitudinal instability near flocking onset.", "comment": "ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息", "作者 Thomas Ihle；Physical Review E 83, 030901(R) (2011)，DOI:10.1103/PhysRevE.83.030901。全文取 arXiv:1006.1825v2，共4页；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "Vicsek 模型的连续场论常由对称性猜测，因此不能给出输运系数与离散微观规则之间的关系。论文问：能否在保留离散时间、多体对齐和有限作用半径的前提下，从 N 粒子演化显式粗粒化出密度—动量方程，并解释相变的强有限尺寸效应？"),
            sec("背景", "Toner–Tu 理论刻画允许的长波结构，但系数未由原始 Vicsek 更新规则确定；低密度 Boltzmann 模型又省略高密度结构和真正的多体碰撞。作者把 collision circle 内任意 n 个粒子的对齐都写进 Enskog 型碰撞和，从而保留 collisional momentum transfer。", "molecular-chaos 分解只在中高噪声且 mean free path τv0≫R 时受控。论文所说的任意密度有效，是指点粒子 Enskog 碰撞和本身不会因占据排斥截断，并不消除前碰撞相关或短平均自由程问题。"),
            sec("模型与方法", "从 N 粒子 Liouville 方程出发，在分子混沌近似下得到 one-particle kinetic equation Eq. (2)。空间均匀固定点的第一 Fourier mode 在 λ=1 时失稳；随后用 Chapman–Enskog 展开到三阶梯度，在临界点附近闭合 density ρ 与 momentum density w。", "所有变量以时间步 τ 和 mean free path τv0 无量纲化；多体角积分 Jm(n) 决定 p、q、S、Γ，Table I 给出五组张量输运系数。线性化均匀 flock 得到三个增长模；PDE 另用 periodic L×L 网格和 predictor–corrector scheme 做有限尺寸演化。"),
            sec("核心结果与证据", "Figure 1(a) 中理论临界噪声 ηC(M) 与直接 Vicsek 数值在给定数据点上接近，并在低密度给出 ηC∝R√ρ、高密度趋于2π；大 mean-free-path 极限下相界不依赖粒子速度，这与被比较的连续时间 Boltzmann 模型不同。", "均匀有序解的 longitudinal mode 在 ηS<η<ηC 的窄窗内对 0<k<k0 不稳定。Figure 1(b) 展示正增长率区间，并由2π/k*与2π/kmax给出 crossover length L* 的上下界；其随 M 在低、高密度发散、在 M≈2 附近最小，与已有数值趋势一致。", "PDE 积分在 L<2π/k0 时稳定，略大时形成非均匀稳态，更大时扰动无界增长。作者明确指出此时梯度展开被推出有效区，不能用该方程描述微观模拟中的 travelling bands；因此该工作解释 onset instability，而非给出完整带状稳态理论。"),
            sec("有效性与局限", "推导依赖 τv0≫R、中高噪声分子混沌、临界附近小 |λ−1| 和三阶梯度闭合；小速度时必须纳入 pre-collisional correlations。点粒子可无限重叠也与有尺寸实验颗粒不同。", "相变在均匀 mean-field 固定点上连续且指数1/2，但大系统因长波密度模呈现不连续外观；这不是对 thermodynamic-order 的独立有限尺寸标度证明。PDE 无界增长直接标记 closure 失效，不能把它解释成物理发散。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/1006.1825；期刊：https://doi.org/10.1103/PhysRevE.83.030901。PDF SHA-256：c1af8175ce692fec480a073919a3aed5ba86b5758779a0b6c044dce3651736ab。全文未给出代码仓库。", "复核需固定 R、τ、v0、M=ρ0πR²、均匀角噪声定义、Fourier 归一化、Jm(n) 截断、Chapman–Enskog 计数、periodic L、网格与 predictor–corrector 步长。Evidence status: full-text verified kinetic theory/PDE manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Eqs. (1)–(3)，区分离散 Enskog 与低密度 Boltzmann；p.3 Eqs. (5)–(8) 和 Table I 是闭合结构。最后用 p.4 对照 Figure 1(b)、crossover length 与作者关于 travelling bands 超出有效域的警告。"),
        ],
        "figure-1-phase-instability.webp", "Figure 1", 2, "comparison",
        "临界噪声相界、均匀有序态的纵向增长率，以及相变外观改变的 crossover length 估计。",
        "Enskog 理论能跟踪已有数值相界，但临界点下方存在有限波数长波不稳定，且其长度尺度具有强密度依赖。",
        "Figure 1把相界一致性和均匀 flock 的失稳放在同一证据面板中，也直接暴露理论不能只靠均匀 mean-field 判定大系统相变。",
        [{"label": "Vicsek Enskog kinetic equation", "latex": r"f(\theta,\mathbf x+\tau\mathbf v,t+\tau)=\mathcal C[f](\theta,\mathbf x,t)", "role": "retain discrete streaming and genuine n-body alignment collisions", "symbols": {"f": "one-particle angular distribution", "tau": "Vicsek time step", "C": "Enskog-type collision functional"}, "evidence": "paper.pdf p. 2, Eq. (2)", "interpretation": "The molecular-chaos factorization is controlled only for large mean free path and moderate-to-large noise."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(3) and Figure 1(a): discrete-time Enskog equation and transition line", "paper.pdf p. 3, Eqs. (5)–(8) and Table I: third-order hydrodynamic closure", "paper.pdf p. 4 and Figure 1(b): longitudinal instability, crossover scale and breakdown for bands", "source PDF SHA-256 c1af8175ce692fec480a073919a3aed5ba86b5758779a0b6c044dce3651736ab", "Evidence status: full-text verified kinetic theory/PDE manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physreve.87.043014", "APS full text", "https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevE.87.043014/fulltext",
        "Electrohydrodynamic interaction of spherical particles under Quincke rotation", "Quincke 旋转球形粒子的电流体动力学相互作用",
        "theory_numerics", "d42f801bdd49fc14", "Active Matter",
        {"doi": "10.1103/PhysRevE.87.043014", "version": "APS version-of-record full text", "title": "Electrohydrodynamic interaction of spherical particles under Quincke rotation", "authors": ["Debasish Das", "David Saintillan"], "journal": "Physical Review E", "volume": "87", "issue": "4", "article": "043014", "published": "2013-04-29", "abstract": "A method-of-reflections model couples dipole relaxation, rotlet hydrodynamics, and dielectrophoresis for two Quincke-rotating spheres, predicting orientation-dependent onset, synchronization, pairing, and separation.", "comment": "APS full text and Crossref metadata checked; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息", "作者 Debasish Das、David Saintillan；Physical Review E 87, 043014 (2013)，DOI:10.1103/PhysRevE.87.043014。全文取 APS full-text endpoint，共14页；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "孤立介电球的 Quincke rotation 已知，但浓悬浮体系的黏度偏差暗示 pair interactions 不可忽略。论文问：两个相同球的 electric dipole–dipole 与 hydrodynamic rotlet interactions 如何改变旋转阈值、稳态角速度，以及自由粒子的配对/分离动力学？"),
            sec("背景", "Taylor–Melcher leaky-dielectric model 中，粒子比液体充电更慢时诱导偶极可反平行外场；超过临界场后电矩与黏性矩平衡，出现 supercritical pitchfork rotation。已有成对理论重视电相互作用，却忽略旋转产生的 hydrodynamic flow。", "作者用 method of reflections 展开两个相距 R 的球：dipolar electric field、rotlet velocity/vorticity 和 dielectrophoretic translation 被耦合进同一组常微分方程。远场项截到给定阶次，因此 near contact 不是精确两球解。"),
            sec("模型与方法", "dipole relaxation 方程 Eqs. (52)–(53) 与 torque balance Eqs. (54)–(55) 控制 P1,P2,Ω1,Ω2；自由球再由 Eqs. (56)–(57) 得平移速度。长度以半径 a、时间以 Maxwell–Wagner relaxation time、场以 E0 无量纲化，Mason number 衡量黏性与极化力。", "固定 R 时对无旋转 base state 的6×6 Jacobian 做线性稳定性分析；非线性 ODE 用四阶 Runge–Kutta。数值采用 ε21=−0.1097、σ21=−0.5，并给 dipoles 加约10^-3随机微扰；自由运动另加短程排斥防止重叠。"),
            sec("核心结果与证据", "Figure 5 显示 Ec/Ec0 取决于球心连线与外场夹角 Θ：近乎沿场排列时阈值升高，垂直排列时降低；偏移随大 R 为 O(R^-3)。关掉 electric interaction 后曲线与完整模型重合，而仅保留 electric interaction 时偏移较弱，说明阈值修正主要由 hydrodynamic modes 控制。", "固定球模拟中，角速度分量可经历瞬态振荡，但两球 |Ω| 总在长时同步；旋转轴不必相同。平均稳态 |Ω|² 与 Appendix A 的 corotating far-field estimate 在大 R 下吻合，且旋转 onset 与线性稳定阈值一致。", "自由球出现四类轨迹：无扰动时螺旋接触并绕接触点旋转；沿场配对后 counterrotate 并横向平移；垂直场配对后 corotate；或边旋转边缓慢分离。Figure 12 的 pairing probability 随初始 R0、Θ0 和场强变化，但相同构型对微小初扰高度敏感。"),
            sec("有效性与局限", "method of reflections 适用于 widely separated particles；靠近接触时 lubrication、完整 multipoles 和边界条件会改变轨迹，因此配对后的接触动力学只能定性解读。短程排斥是数值规避重叠，不是实验接触模型。", "研究只有两个相同球、无界静止流体和特定材料参数；多体结构、浓悬浮流变、外加剪切、噪声及实验验证均未解决。初始微扰敏感性意味着单条轨迹不是稳健预测，概率图也只对应指定扰动采样。"),
            sec("复现与资源", "全文：https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevE.87.043014/fulltext；期刊：https://doi.org/10.1103/PhysRevE.87.043014。PDF SHA-256：d42f801bdd49fc140ed7e570cec375909f295d1ae335605927598e5a5ff8a43e。全文未提供代码仓库。", "复现需固定 ε21、σ21、E0/Ec0、R0、Θ0、10^-3微扰分布、reflection truncation、RK4步长、excluded-volume force 与 pairing 判据。Evidence status: full-text verified analytical/ODE study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–7 建立单球与 pair equations；p.8 Figure 5 是阈值机制的最直接拆分。pp.9–12 看同步与四类自由轨迹，最后读 p.12 的 concluding remarks 和 p.13 Appendix A，保留远场/近接触边界。"),
        ],
        "figure-5-critical-field.webp", "Figure 5", 8, "comparison",
        "两球相对外场的取向与间距如何改变 Quincke rotation 临界场，并分解 electric 与 hydrodynamic interaction 的贡献。",
        "沿场取向倾向稳定、垂直取向倾向失稳；只保留 hydrodynamic interaction 几乎复现完整阈值曲线。",
        "Figure 5直接支撑论文最重要的因果判断：阈值的 leading interaction correction 主要是 hydrodynamic，而非仅由 dipole–dipole electric coupling 决定。",
        [{"label": "Electric Mason number", "latex": r"\mathrm{Ma}=\frac{2\eta}{\tau_{MW}\epsilon_1 E_0^2}=(\epsilon_{21}-\sigma_{21})\left(\frac{E_c^0}{E_0}\right)^2", "role": "compare viscous and polarization torques and parameterize the onset field", "symbols": {"eta": "fluid viscosity", "tau_MW": "Maxwell-Wagner relaxation time", "E_c^0": "isolated-sphere critical field"}, "evidence": "paper.pdf p. 7, Eqs. (50)–(51)", "interpretation": "Pair interactions enter the dipole and torque equations and shift the isolated-sphere threshold."}],
        ["paper.pdf pp. 2–7, Eqs. (12), (33), and (52)–(57): leaky-dielectric pair model", "paper.pdf p. 8, Figure 5: orientation, distance and interaction decomposition of critical field", "paper.pdf pp. 9–12, Figures 6–13: synchronization, pairing and separation trajectories", "source PDF SHA-256 d42f801bdd49fc140ed7e570cec375909f295d1ae335605927598e5a5ff8a43e", "Evidence status: full-text verified analytical/ODE study; no independent reproduction performed."],
    ),
    title_card(
        "doi-10.1103-physrevfluids.8.054101", "arXiv v2 manuscript", "https://arxiv.org/pdf/2210.14412",
        "Stokesian dynamics with odd viscosity", "含奇黏度的 Stokesian Dynamics",
        "theory", "f2942f284ab442af", "Fluid Dynamics",
        {"doi": "10.1103/PhysRevFluids.8.054101", "arxiv_id": "2210.14412", "version": "arXiv v2 full text", "title": "Stokesian dynamics with odd viscosity", "authors": ["Hang Yuan", "Monica Olvera de la Cruz"], "journal": "Physical Review Fluids", "volume": "8", "issue": "5", "article": "054101", "published": "2023-05-02", "abstract": "The Stokesian Dynamics mobility formalism is extended perturbatively to a uniaxial active fluid with weak odd viscosity by deriving odd Oseen, Faxén, and near- and far-field mobility tensors.", "comment": "ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息", "作者 Hang Yuan、Monica Olvera de la Cruz；Physical Review Fluids 8, 054101 (2023)，DOI:10.1103/PhysRevFluids.8.054101。全文取 arXiv:2210.14412v2，共36页含大量附录张量表；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "传统 Stokesian Dynamics 假设被动、time-reversal-symmetric 黏性介质；主动流体可具有 nondissipative odd viscosity。论文问：能否从 odd Stokes equation 的 Green function 系统地产生自迁移、成对近场/远场 mobility tensors，并把它们接入多球 Stokesian Dynamics？"),
            sec("背景", "黏度张量在交换应力与应变率指标对时，even 部分满足 Onsager 对称，odd 部分反对称。作者限制到局域角动量沿 z 的 quasi-2D/uniaxial 情形，只需一个标量 μo；χ=μo/μs 衡量 odd 对常规 shear viscosity 的相对大小。", "odd viscosity 不耗散但会把面内速度响应旋转到 transverse component，令 Green tensor 出现 antisymmetric part。这里仍是3D Stokes flow 中带选定轴的本构，而非所有二维 odd-fluid 几何的通用公式。"),
            sec("模型与方法", "由 incompressibility 与本构 Eq. (7) 得 odd Stokes equations Eqs. (8)–(9)，在 Fourier space 反演得到 pressure/velocity Green functions。因 exact inverse transform 有额外 k-dependence，论文取 χ≪1，只保留 odd Oseen tensor 的一阶项。", "借 generalized Lorentz reciprocal theorem 推出 odd Faxén laws；再以 Rotne–Prager–Yamakawa surface integrals 计算 r≤2a 的 regularized near-field tensors，以 differential Faxén laws 计算 r>2a 的 far-field tensors。Appendix D 列出 force/torque/stresslet 到 translation/rotation/strain 的显式分量与对称关系。"),
            sec("核心结果与证据", "Eq. (19) 把 Green tensor 写为 conventional Oseen response 加 O(χ) antisymmetric odd response；Eq. (31) 给出 isolated sphere 的六类 self-mobility，其中 translation–force、rotation–torque 和 strain–stresslet 获得横向 odd terms。", "Eqs. (30) 与 (35) 分别给出 near-/far-field pair mobility construction；两者按构造在 particle surface 连续。generalized reciprocal theorem 改变若干符号关系，但 grand odd mobility 的一半仍可由另一半恢复，降低实现冗余。", "最终 Eq. (37) 是 M=Me+Mo，可在已有 Stokesian Dynamics 中加入 leading odd-viscosity interactions。论文只完成解析框架和实现所需张量，没有实际多粒子 simulation、benchmark timing、实验拟合或 emergent collective-state 结果。"),
            sec("有效性与局限", "结果只到 χ 的一阶，要求 μo≪μs；本构还限定 quasi-2D/uniaxial angular momentum，不能覆盖一般3D odd-viscosity 多系数张量。far-field 是稀悬浮近似，多体反射修正未显式求和。", "所谓 near-field tensors 是 RPY regularization，不是精确 odd lubrication solution；作者明确要求 dense suspension 避免使用它。墙面修正、Brownian fluctuation–dissipation relation、正定性/热噪声采样和高性能实现都留作未来工作。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2210.14412；期刊：https://doi.org/10.1103/PhysRevFluids.8.054101。PDF SHA-256：20f721a2d1b63a2601c4e0b91b33feba49260bbe9c2bbe49936d0ec1d564a805。全文未提供代码或数值数据仓库。", "复核需固定 Levi–Civita/traction 约定、χ expansion、surface normal、Faxén 符号、r=2a 拼接和 grand-matrix block ordering；可先用 Appendix D 的 self limits 与 reciprocity identities 做符号单元测试。Evidence status: full-text verified analytical framework; no independent symbolic verification or simulation performed."),
            sec("阅读指南", "先读 pp.3–8 Eqs. (3)–(19)，把本构假设与 χ 展开锁定；pp.9–16 是 Faxén、near/far mobility 和 M=Me+Mo 主线。p.16–17 先读限制，再按实现需要查 Appendices B–D，而无需线性通读所有分量。"),
        ],
        "全文没有实验图、数值图或结果示意图；可审计贡献是 Eqs. (19)、(30)、(31)、(35) 与 Appendix D 的 mobility tensors。",
        "不截取长张量公式或标题页冒充论文插图；封面使用经全文核验的题目—摘要模式。",
        [{"label": "Odd Stokesian grand mobility", "latex": r"\mathbf M=\mathbf M^{e}+\mathbf M^{o}", "role": "add leading odd-viscosity hydrodynamic responses to conventional Stokesian Dynamics", "symbols": {"M": "full grand mobility", "M_e": "even-viscosity mobility", "M_o": "near- and far-field odd mobility to first order in chi"}, "evidence": "paper.pdf p. 16, Eq. (37)", "interpretation": "The construction is perturbative and lacks exact odd-viscosity lubrication corrections for dense suspensions."}, {"label": "Odd-viscosity expansion parameter", "latex": r"\chi=\mu_o/\mu_s\ll 1", "role": "control the leading antisymmetric correction to the Oseen tensor", "symbols": {"mu_o": "odd viscosity", "mu_s": "even shear viscosity"}, "evidence": "paper.pdf pp. 6–8, Eqs. (16)–(19)", "interpretation": "Higher-order odd-viscosity responses are omitted."}],
        ["paper.pdf pp. 3–8, Eqs. (3)–(19): uniaxial odd constitutive law, Stokes equation and Green tensor", "paper.pdf pp. 9–16, Eqs. (30)–(37): Faxén construction and mobility blocks", "paper.pdf pp. 16–17: missing lubrication, walls, Brownian relation and implementation limits", "paper.pdf pp. 27–34, Appendix D: explicit mobility tensors and symmetry checks", "source PDF SHA-256 20f721a2d1b63a2601c4e0b91b33feba49260bbe9c2bbe49936d0ec1d564a805", "Evidence status: full-text verified analytical framework; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevfluids.8.110501", "APS version of record", "https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevFluids.8.110501/fulltext",
        "Traveling Faraday waves", "行进 Faraday 波",
        "experiment", "2d98de46772a1157", "Fluid Dynamics",
        {"doi": "10.1103/PhysRevFluids.8.110501", "version": "APS CC BY version-of-record full text", "title": "Traveling Faraday waves", "authors": ["Jian H. Guan", "Connor W. Magoon", "Matthew Durey", "Roberto Camassa", "Pedro J. Sáenz"], "journal": "Physical Review Fluids", "volume": "8", "issue": "11", "article": "110501", "published": "2023-11-16", "abstract": "Vertically vibrated annular channels in a capillary-dominated deep-fluid regime exhibit persistent clockwise or counterclockwise traveling Faraday patterns at about 10 mm/s and can drive biased pumping and object transport.", "comment": "APS CC BY 4.0 version of record and Crossref metadata checked; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息", "作者 Jian H. Guan、Connor W. Magoon、Matthew Durey、Roberto Camassa、Pedro J. Sáenz；Physical Review Fluids 8, 110501 (2023)，DOI:10.1103/PhysRevFluids.8.110501。APS CC BY 4.0 全文5页；关联视频获2022 APS DFD Milton van Dyke Award；Crossref 未列更正或撤稿。"),
            sec("研究问题", "Faraday waves 在大容器中由 standing pattern 经二次不稳定走向缺陷湍动，在窄重力主导环道中只报告过低于0.01 mm/s的 slow drift。论文问：当 wavelength λ、channel width W 和 capillary length lc 可比且流体足够深时，侧壁/接触线效应能否产生快得多的相干 traveling state，并被用于输运？"),
            sec("背景", "液层垂直正弦振动超过 Faraday threshold 后产生驱动频率一半的单色 standing waves；继续加速会越过 order–disorder threshold。surface pattern 与 bulk streaming 相耦合，底边界或侧壁振荡边界层可以整流出 dc flow。", "本文属于 Gallery of Fluid Motion 短文，证据核心是影像、装置演示和定性数值支持，而不是完整参数扫描论文。没有给出阈值曲线、误差条、重复次数或 governing simulation details。"),
            sec("模型与方法", "作者垂直振动3D打印环形/变曲率/网络通道，填充水或 silicone oils，用斜视或俯视彩色高速相机记录。选择 H≫λ 的 deep-fluid limit，排除以底边界为主的经典 drift mechanism，使 lateral walls、wettability 与 contact-line dynamics 成为主要 streaming 来源。", "当 forcing 增大，环中 pattern 自发选定 clockwise 或 counterclockwise 方向并持续传播；通过在垂直壁加入 ratchets 显式打破对称性，可预设方向。另把两个 ratcheted rings 接到直通道观察 dye transport，并在自由表面放置3D打印物体验证载运。"),
            sec("核心结果与证据", "Figure 1 直接比较 standing、chaotic 和 annular traveling states。新状态在 λ≈W≈lc 时出现，传播速度约10 mm/s，比文献中的 gravity-dominated narrow-channel drift 最高可快三个数量级；自发选择的转向随机，但选定后持续。", "Figure 2 显示现象不局限于圆环：variable-curvature channels 与含直/曲段网络仍保持同量级波速，只要 W 不变；ratchet walls 固定传播方向并在相连通道形成单向泵送。Figure 3 中漂浮物速度与 wave speed 成正比。", "作者将增强归因于 capillary effects 对 wave-generated streaming 的放大，并称 experiments 与 simulations 共同支持。但短文没有展示 velocity field、contact-line model 或定量 simulation–experiment overlay，因此机制证据弱于现象与功能演示。"),
            sec("有效性与局限", "约10 mm/s与‘快三个数量级’来自文中量级陈述，未给 sample count、uncertainty 或全几何标度；不能据此断言所有λ≈W≈lc通道都有相同增益。方向持久性也没有报告 observation-time distribution。", "材料只覆盖水/硅油与3D打印边界；ratchet pump 和浮物输运是 proof-of-concept，没有流量—压头、载荷、效率、长期稳定性或微尺度缩放。机制部分需要完整实验/模拟论文才能分离 wettability、contact-line 与侧壁 streaming 的贡献。"),
            sec("复现与资源", "全文：https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevFluids.8.110501/fulltext；期刊/视频：https://doi.org/10.1103/PhysRevFluids.8.110501、https://doi.org/10.1103/APS.DFD.2022.GFM.V0040。PDF SHA-256：296c3e5354e5a121a1516d36d5f6a1597d7d35c845029a45a33f0c19a3331be5。", "定量复现仍需补齐 bath radius/width/depth、fluid density/viscosity/surface tension、contact angle、drive frequency/acceleration、threshold definition、camera calibration、wave tracking、ratchet dimensions 和 simulation equations。Evidence status: full-text verified experimental Gallery article; no independent video/experiment reproduction performed."),
            sec("阅读指南", "先看 p.2 Figure 1 建立 standing—chaotic—traveling 的视觉区别，再读 pp.2–3 的 λ、W、lc、H 与约10 mm/s条件。p.3 Figure 2 和 Figure 3 是功能演示；读完应把高可信现象与尚未定量拆解的 capillary-streaming 机制分开。"),
        ],
        "figure-1-traveling-waves.webp", "Figure 1", 2, "comparison",
        "standing、chaotic 与环道中顺/逆时针 traveling Faraday waves 的直接影像比较。",
        "当 W、λ、lc 同量级时，环形约束中的 pattern 自发破缺左右对称并选择一个持久传播方向。",
        "Figure 1是该 Gallery 论文对新现象最直接的原始视觉证据，同时展示随机二选一的传播手性。",
        [{"label": "Faraday subharmonic response", "latex": r"f_{wave}=\frac{1}{2}f_{drive}", "role": "identify the standard subharmonic Faraday state preceding the traveling instability", "symbols": {"f_wave": "surface-wave oscillation frequency", "f_drive": "vertical forcing frequency"}, "evidence": "paper.pdf p. 1, opening paragraph", "interpretation": "The paper states the standard subharmonic relation but does not provide a new dispersion measurement."}],
        ["paper.pdf pp. 1–2 and Figure 1: standing, chaotic and traveling states", "paper.pdf pp. 2–3: deep-fluid/capillary regime and approximately 10 mm/s speed", "paper.pdf pp. 3–4, Figures 2–3: complex channels, ratchet pumping and floating-object transport", "source PDF SHA-256 296c3e5354e5a121a1516d36d5f6a1597d7d35c845029a45a33f0c19a3331be5", "Evidence status: full-text verified experimental Gallery article; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.122.194503", "arXiv v1 manuscript with supplement", "https://arxiv.org/pdf/1904.10855",
        "Active Particles Powered by Quincke Rotation in a Bulk Fluid", "由体相流体中 Quincke 旋转驱动的活性粒子",
        "theory_numerics", "347524d9e43b5507", "Active Matter",
        {"doi": "10.1103/PhysRevLett.122.194503", "arxiv_id": "1904.10855", "version": "arXiv v1 full text with supplementary material", "title": "Active Particles Powered by Quincke Rotation in a Bulk Fluid", "authors": ["Debasish Das", "Eric Lauga"], "journal": "Physical Review Letters", "volume": "122", "issue": "19", "article": "194503", "published": "2019-05-16", "abstract": "Boundary-element simulations and slender-helix resistance theory show that geometric chirality converts Quincke rotation into wall-free translation perpendicular to a DC field in a bulk weakly conducting fluid.", "comment": "ArXiv v1 manuscript and appended supplement cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息", "作者 Debasish Das、Eric Lauga；Physical Review Letters 122, 194503 (2019)，DOI:10.1103/PhysRevLett.122.194503。全文取 arXiv:1904.10855v1，主文5页并附数值方法/验证/实验量级补充，共9页；Crossref 未列更正或撤稿。"),
            sec("研究问题", "球形 Quincke particle 在无限流体只旋转不平移，已知 Quincke rollers 必须借助壁面把旋转转成滚动。论文问：仅依靠粒子几何不对称，能否在无壁体相流体中把 DC-field-induced rotation 转换为横向自推进，并由可计算的形状参数预测 onset 与速度？"),
            sec("背景", "在 Melcher–Taylor leaky-dielectric picture 中，粒子充电时间大于液体且 E0>Ec 时，反平行诱导偶极发生不稳定并产生持续转动。对具有 translation–rotation resistance coupling 的手性物体，力自由条件允许 Ω 通过非对角阻力 R14 产生 U。", "作者选 helix 作为原型；同长圆柱是对称 control。该系统仍由外部 DC 场持续供能，‘bulk active particle’指不依赖附近壁面，并不意味着无外场自主能源。"),
            sec("模型与方法", "电势满足内外 Laplace equation，surface charge 由 Ohmic current 与 surface advection 演化；流体满足 Stokes equations，particle force/torque balances 为零。boundary-element method 同时求 Maxwell traction、hydrodynamic traction、U 与 Ω，补充材料用球/无限圆柱解析 Quincke solution 检验网格误差。", "解析模型把小 pitch-amplitude helix 的 electric response 近似为等 contour-length cylinder，用 resistive-force theory 写6×6 hydrodynamic resistance。force-free 得 U1=−Ω1R14/R11；torque balance 与 dipole relaxation 给 shape factor G、Ec,hl=Ec,cl√(1+G) 和稳态 Ω。"),
            sec("核心结果与证据", "Figures 2–3 中相同 aspect ratio 的 cylinder 只旋转，而三圈 helix 同时旋转并在垂直外场的平面内平移；初始倾斜使其轨迹离开初始 x–z plane。这是几何手性把旋转耦合为体相推进的直接数值对照。", "Figure 4(a) 显示 pitch angle 与 cross-sectional radius 改变临界场；(b) 中 U 在 straight rod α=0 与 torus α=π/2 两端为零，在中间角最大：E*=2.5 时 simulation optimum约0.2π、theory约0.215π，E*=5.5 时两者约0.25π。", "Figure 4(c) 随 a/L 出现 supercritical pitchfork-like swimming onset；过细 filament 电矩相对黏性矩不足。解析曲线能抓住阈值与中间角最优，但大 a/L 偏离增大，符合 slender-body 假设失效。补充材料估计 PMMA helix 在典型介电液中可达 tens of microns/s，尚非实验测量。"),
            sec("有效性与局限", "主证据是 boundary-element simulation 加 slender-helix theory，没有制造颗粒或实验轨迹。解析 electric approximation 要求 small pitch amplitude，resistive-force theory 要求 a/L→0；粗 helix、复杂非手性不对称体需要完整阻力/电极化计算。", "模型假设无限、弱导电、惯性可忽略、neutrally buoyant 的单粒子；电极边界、重力、Brownian rotation、charge injection、材料非均匀和多粒子 electrohydrodynamics 均未纳入。collective 3D motion 是展望，不是本文结果。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/1904.10855；作者公开稿：https://www.damtp.cam.ac.uk/user/lauga/papers/162.pdf；期刊：https://doi.org/10.1103/PhysRevLett.122.194503。PDF SHA-256：4306a54c2df48342eca4ce2909f29229b0e650fab46c80b3b093771f0940fdfb。", "复现需固定 R=σ+/σ−、Q=ε−/ε+、E*=E0/Ec,cl、N、α、a/L、λ/L、initial tilt、BEM mesh/time integrator、charge advection 和 force/torque tolerance；先重现 supplement Figure 5 sphere/cylinder convergence。Evidence status: full-text verified theory/BEM manuscript; no independent numerical reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Eqs. (1)–(5) 和 Figure 2，理解场—电荷—流体闭环；pp.3–4 Figures 3–4 与 Eqs. (6)–(12) 是几何耦合主证据。最后查 pp.6–9 supplement 的 BEM validation 与 dimensional estimates，并把后者标成预测。"),
        ],
        "figure-4-helix-swimming.webp", "Figure 4", 4, "comparison",
        "helix 的 pitch angle、截面半径与外场如何共同控制 Quincke onset 和无壁游动速度，符号为 BEM、曲线为 slender-helix theory。",
        "推进在直杆和环形极限消失，在中间 pitch angle 最大；截面过细时存在无游动阈值，解析与数值在细长极限附近一致。",
        "Figure 4同时检验临界场、最优几何与 pitchfork-like onset，是从机制到可设计参数最完整的定量证据。",
        [{"label": "Rotation-translation conversion", "latex": r"U_1=-\Omega_1\frac{R_{14}}{R_{11}}", "role": "convert Quincke rotation into force-free translation through chiral resistance coupling", "symbols": {"R14": "translation-rotation coupling resistance", "R11": "translational resistance", "Omega1": "rotation about the helix axis"}, "evidence": "paper.pdf p. 4, Eq. (9)", "interpretation": "Translation vanishes when geometry makes the off-diagonal resistance R14 zero."}, {"label": "Helix rotation state", "latex": r"\Omega_1=\sqrt{\frac{E^{*2}}{1+G}-1}", "role": "predict the supercritical steady Quincke rotation above the geometry-shifted threshold", "symbols": {"E*": "field normalized by cylinder threshold", "G": "helical shape factor"}, "evidence": "paper.pdf p. 4, Eq. (12)", "interpretation": "The formula uses the cylinder-like electric approximation and slender-helix hydrodynamics."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(5) and Figure 2: leaky-dielectric BEM setup and cylinder control", "paper.pdf pp. 3–4, Figures 3–4 and Eqs. (6)–(12): translation and geometry-dependent theory", "paper.pdf pp. 6–9, Supplemental Figures 5 and Table I: BEM validation and dimensional estimates", "source PDF SHA-256 4306a54c2df48342eca4ce2909f29229b0e650fab46c80b3b093771f0940fdfb", "Evidence status: full-text verified theory/BEM manuscript; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
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
