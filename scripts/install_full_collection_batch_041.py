#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 041."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-physrevx.11.021028", "arXiv v2 manuscript", "https://arxiv.org/pdf/2012.02358",
        "Local Number Fluctuations in Hyperuniform and Nonhyperuniform Systems: Higher-Order Moments and Distribution Functions",
        "超均匀与非超均匀体系的局域粒子数涨落：高阶矩与分布函数", "theory_numerics",
        "22dc44d551c207e7", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.11.021028","arxiv_id":"2012.02358","version":"arXiv v2 full text","title":"Local Number Fluctuations in Hyperuniform and Nonhyperuniform Systems: Higher-Order Moments and Distribution Functions","authors":["Salvatore Torquato","Jaeuk Kim","Michael A. Klatt"],"journal":"Physical Review X","volume":"11","issue":"2","article":"021028","published":"2021-05-05","abstract":"Higher-order local-number cumulants and full counting distributions distinguish hyperuniform, ordinary nonhyperuniform, and antihyperuniform point processes and determine their approach to Gaussian statistics.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Salvatore Torquato、Jaeuk Kim、Michael A. Klatt；Physical Review X 11, 021028 (2021)，DOI:10.1103/PhysRevX.11.021028。核验 arXiv:2012.02358v2 全文23页及期刊元数据；未发现关联更正或撤稿。"),
            sec("研究问题", "点过程通常用观测窗内粒子数 N(R) 的方差判断 hyperuniformity，但相同大尺度方差标度并不能完全描述局域统计。论文问：skewness、excess kurtosis 和完整分布 P[N(R)] 如何依赖二、三、四体相关；hyperuniform、ordinary nonhyperuniform 与 antihyperuniform 体系趋向中心极限定理的速度是否存在系统差别？"),
            sec("背景", "半径 R 球形观测窗中的 local number variance σ²(R) 只含 pair correlation；第三、第四 cumulants 则分别含至三体、四体信息。hyperuniform 体系在大 R 下方差增长慢于体积，ordinary nonhyperuniform 与体积同阶，antihyperuniform 则更快。", "作者比较一至三维 lattice、stealthy/URL disordered hyperuniform processes、RSA/equilibrium hard particles、Poisson、Poisson cluster 和 hyperplane-intersection process。模型集合横跨有序、无序和长程聚集，但不是所有可能点过程的穷举。"),
            sec("模型与方法", "作者从 n-point correlation functions 推导 N(R) 前四阶矩的精确积分表达式，并定义标准化 skewness γ1、excess kurtosis γ2 及分布到同均值同方差 Gaussian 的离散 L2 距离 l2(R)。不同 R 的 counting distribution 通过点配置采样，快速振荡体系再用 running averages 估计渐近标度。", "当体系满足 CLT 时，以匹配均值和方差的 gamma distribution 近似 P[N(R)]；该近似同时给出 γ1、γ2 和 l2 的标度。晶格和一维 class-I hyperuniformity 的非 CLT 结论则来自 bounded variance/周期结构的解析论证，而非只看拟合曲线。"),
            sec("核心结果与证据", "对满足 CLT 的 disordered hyperuniform models，作者得到并数值观察 γ1 与 l2 约按 R^{-(d+1)/2}、γ2 约按 R^{-(d+1)} 衰减；ordinary nonhyperuniform systems 通常更慢，antihyperuniform HIP 最慢。Figure 5 把1D、2D、3D多种模型的 l2(R) 放在同一坐标中，展示维度与长波密度涨落共同控制 Gaussian convergence。", "完整 P[N(R)] 在有限 R 可高度偏斜或呈晶格振荡，即使其二阶方差具有相似标度。Figures 3–4 对比点配置与标准化分布；gamma approximation 对 obeying-CLT models 捕捉主要形状和渐近标度，但不是所有 R 的精确分布。", "论文证明一维 class-I hyperuniform systems 以及任意维晶格不能服从通常的 local-number CLT：方差有界或强烈随窗位置/尺度振荡，标准化计数不会收敛到连续 Gaussian。这个否定结果依赖文中观测窗与极限定义，不能直接推广到加入随机位移或改变窗平均方式后的体系。"),
            sec("有效性与局限", "精确 cumulant 公式适用于统计齐次点过程，但具体数值标度来自有限配置、有限 R 和选定模型；高阶矩对尾部与采样量尤其敏感。2D/3D stealthy 与 URL 数据的振荡使 exponent 难以精确拟合，作者也明确用 running average 缓解而非消除该问题。", "Gaussian distance 与 gamma approximation 是描述性工具，不意味着微观相关可由低阶统计唯一反演。晶格的非 CLT 结论也不否认加入 disorder 后可能恢复 CLT；本文没有实验数据，也没有把计数统计用于具体材料分类器。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2012.02358；期刊：https://doi.org/10.1103/PhysRevX.11.021028。核验 PDF SHA-256：ad753b3166301dadf7b2955ce349d4ed5b26a2cc6ba073117198963d4fe5b2a6。正文未给统一代码仓库。", "复现需固定每类 point process 的生成算法、system size、number density、window-center sampling、R grid、periodic boundaries、histogram normalization 与 running-average rule，并同时报告 σ²、γ1、γ2、l2 和有限样本误差。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–6 的 local-number moments 与 correlation-function 表达式，再看 pp.8–13 各模型的 skewness/kurtosis。pp.15–18 Figures 3–5 最直观地区分分布形状与 Gaussian convergence；最后读 pp.19–21 的 gamma approximation 和非 CLT 证明，保留有限尺寸与窗平均限定。"),
        ],
        "figure-5-gaussian-distance.webp", "Figure 5", 18, "data_plot",
        "一至三维多种点过程的局域粒子数分布到 Gaussian 的距离随观测窗半径变化。",
        "超均匀、普通非超均匀与反超均匀模型的 Gaussian convergence 速度随维度和长波涨落性质显著不同。",
        "Figure 5 是跨模型、跨维度比较中心极限定理趋近速度的直接证据。",
        [{"label":"Gaussian distance","latex":r"l_2(R)=\left[\sum_N\left(P[N(R)]-G[N;\langle N(R)\rangle,\sigma^2(R)]\right)^2\right]^{1/2}","role":"quantify convergence of the local-number distribution to a matched Gaussian","symbols":{"P":"local-number probability mass function","G":"matched Gaussian discretization","R":"window radius"},"evidence":"paper.pdf pp. 14–18 and Figure 5","interpretation":"A decreasing distance diagnoses distributional convergence but does not identify the microscopic source of correlations by itself."}],
        ["paper.pdf pp. 2–6: exact local-number moments and correlation integrals","paper.pdf pp. 8–13, Figures 2–4: model-by-model cumulants and distributions","paper.pdf p. 18, Figure 5: Gaussian-distance comparison across dimensions","paper.pdf pp. 19–21: gamma approximation and non-CLT results","source PDF SHA-256 ad753b3166301dadf7b2955ce349d4ed5b26a2cc6ba073117198963d4fe5b2a6","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.11.031059", "arXiv v2 manuscript", "https://arxiv.org/pdf/2012.04030",
        "Statistical Mechanics of Deep Linear Neural Networks: The Backpropagating Kernel Renormalization",
        "深线性神经网络的统计力学：反向传播核重整化", "theory_numerics",
        "e0fe07aa55fae77b", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.11.031059","arxiv_id":"2012.04030","version":"arXiv v2 full text","title":"Statistical Mechanics of Deep Linear Neural Networks: The Backpropagating Kernel Renormalization","authors":["Qianyi Li","Haim Sompolinsky"],"journal":"Physical Review X","volume":"11","issue":"3","article":"031059","published":"2021-09-16","abstract":"Backpropagating kernel renormalization gives an exact proportional-limit equilibrium theory for deep linear networks, predicting generalization and layerwise representations beyond the infinite-width Gaussian-process limit.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Qianyi Li、Haim Sompolinsky；Physical Review X 11, 031059 (2021)，DOI:10.1103/PhysRevX.11.031059。核验 arXiv:2012.04030v2 全文31页含补充推导；未发现关联更正或撤稿。"),
            sec("研究问题", "无限宽 neural-network Gaussian process 令 training-set size P 相对 hidden width N 可忽略，因此隐藏层基本不因数据而重整化。论文问：在 P,N→∞ 且 α=P/N 固定的 proportional limit 中，深线性网络的有限宽 feature adaptation、generalization error 和 layerwise representation 能否被精确求解？"),
            sec("背景", "网络输出对每层权重分别是非线性的，但对深线性网络的端到端 map 仍为线性。Bayesian/Gibbs measure 把 squared training error、weight decay 和 temperature 组成能量；直接同时积分所有层会产生强耦合。", "作者提出 Back-Propagating Kernel Renormalization（BPKR）：从 output layer 向 input layer 逐层积分权重，每一步用 scalar/order-parameter 修正下一层 kernel。它是统计力学积分方法，不是标准训练中的 gradient backpropagation。"),
            sec("模型与方法", "主体模型是 fully connected deep linear network，P 个输入的维度 N0，各 hidden widths Nl 与 P 同阶，输出是 noisy linear teacher labels。replica calculation 在 thermodynamic limit 求 free energy、order parameter u_l、predictive mean/variance 和 test error。", "理论区分 wide regime α<1 与 narrow regime α>1；后者在 hidden representation 中需要非平凡权重变化才能插值。作者用有限 N 的 Langevin/Monte Carlo 或直接数值训练比较理论曲线，并构造 cluster/template data 分离 bias 与 variance。对 ReLU 的推广使用 Gaussian-equivalence heuristic，不属于线性网络精确解。"),
            sec("核心结果与证据", "逐层积分得到从顶层反向传播的 renormalized kernels；有限 α 下 order parameters 偏离 Gaussian-process limit，并把 depth、width、training size、temperature、regularization 与 input-output covariance 统一到预测公式中。wide 与 narrow 两侧的 generalization 可随 depth 改善或恶化，并非‘越深越好’。", "Figure 4 将 generalization error、variance、bias 与 order parameter 对深度 L 的依赖并列。三组噪声/样本参数中，蓝点的有限网络模拟跟随黑色理论曲线，而虚线 GP limit 可能定性错误；bias 近似不变时，深度效应主要通过 variance 和 kernel renormalization 进入。", "Figures 3、5、6 分别改变 width、phase parameters 与 training size，支持 BPKR 在 modest depth、not-too-small width 的预测。ReLU Figures 11–15 也呈相似趋势，但作者明确把它作为 heuristic extension；agreement 不能把非线性网络公式升级为精确定理。"),
            sec("有效性与局限", "精确性依赖 linear activations、Gaussian/Bayesian equilibrium、quadratic loss、replica-symmetric saddle 与比例极限；真实 SGD 的路径、early stopping、classification loss 和 feature hierarchy不在证明内。输入或教师模型的随机假设也限制外推。", "有限规模实验支持 saddle-point predictions，但没有系统覆盖极窄网络、很深网络或 replica-symmetry instability。ReLU 近似只在本文数据与参数范围内比较；不能据此声称 BPKR 已精确解决一般深度学习。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2012.04030；期刊：https://doi.org/10.1103/PhysRevX.11.031059。核验 PDF SHA-256：f573a7ff1c8e6e812e3b00b79147ff9e9f48195bbff8c2c0136d6501749c096c。正文未给专用代码仓库。", "复现需固定 P、N0、各层 Nl、teacher/noise covariance、β、weight priors、training sampler 与测试集，并数值解 BPKR saddle equations；ReLU 部分还应单独标注 approximation。Evidence status: full-text verified theory/finite-network study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–5 的模型和 BPKR recursion，明确它与梯度反向传播的区别；pp.7–10 Figures 3–5 展示 width/depth/phase 预测。再读 pp.11–14 的 training-size 与 representation 结果，最后查补充材料的 replica 推导和 ReLU Figures 11–15。"),
        ],
        "figure-4-depth-generalization.webp", "Figure 4", 9, "comparison",
        "深线性网络的泛化误差、方差、偏差和阶参量随深度变化的理论曲线与有限网络模拟。",
        "有限宽核重整化可使深度降低或提高泛化误差，而无限宽 GP 极限会遗漏这种参数依赖。",
        "Figure 4 直接检验 BPKR 对深度效应的核心定量预测。",
        [{"label":"Layerwise kernel renormalization","latex":r"K_l=u_l K_{l-1},\qquad u_l=\mathcal F_l(\alpha_l,\beta,\sigma_l^2,K_{l-1})","role":"propagate finite-width data dependence backward through network layers","symbols":{"K_l":"effective kernel at layer l","u_l":"BPKR order parameter","alpha_l":"sample-to-width ratio"},"evidence":"paper.pdf pp. 3–6, BPKR equations","interpretation":"The scalar form is exact for the analyzed deep linear ensemble, not for arbitrary nonlinear architectures."}],
        ["paper.pdf pp. 2–6: Gibbs formulation and BPKR derivation","paper.pdf pp. 7–9, Figures 3–4: width and depth dependence","paper.pdf pp. 9–13, Figures 5–6: phase summary and training-size effects","paper.pdf pp. 23–30, Figures 11–15: heuristic ReLU comparisons","source PDF SHA-256 f573a7ff1c8e6e812e3b00b79147ff9e9f48195bbff8c2c0136d6501749c096c","Evidence status: full-text verified theory/finite-network study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.13.011013", "arXiv v4 manuscript", "https://arxiv.org/pdf/2206.02684",
        "Thermodynamic Unification of Optimal Transport: Thermodynamic Uncertainty Relation, Minimum Dissipation, and Thermodynamic Speed Limits",
        "最优输运的热力学统一：不确定性关系、最小耗散与速度极限", "theory",
        "9298a05c35deab16", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.13.011013","arxiv_id":"2206.02684","version":"arXiv v4 full text","title":"Thermodynamic Unification of Optimal Transport: Thermodynamic Uncertainty Relation, Minimum Dissipation, and Thermodynamic Speed Limits","authors":["Tan Van Vu","Keiji Saito"],"journal":"Physical Review X","volume":"13","issue":"1","article":"011013","published":"2023-02-03","abstract":"A mobility-weighted thermodynamic formulation of discrete optimal transport yields improved uncertainty relations, exact minimum-dissipation variational principles, speed limits, and finite-time Landauer bounds for classical and quantum Markov dynamics.","comment":"ArXiv v4 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Tan Van Vu、Keiji Saito；Physical Review X 13, 011013 (2023)，DOI:10.1103/PhysRevX.13.011013。核验 arXiv:2206.02684v4 全文42页含附录；未发现关联更正或撤稿。"),
            sec("研究问题", "最优输运用最小代价连接两个概率分布，随机热力学则用 entropy production、activity/mobility 与 current 描述有限时间过程。论文问：能否选择适当的 dynamical state mobility，使 thermodynamic uncertainty relation、minimum dissipation、speed limit 和 Landauer principle 都成为同一个离散 Wasserstein 几何的推论？"),
            sec("背景", "Markov jump process 可表示为图 G(V,E)：允许跃迁是边，节点间最短路径 d_xy 构成 transport cost。端点分布 p^A、p^B 的离散 W1 是 coupling π_xy 的最小平均距离。Figure 3 用五节点图把拓扑、最短路径矩阵与 Wasserstein cost 连接起来。", "传统 TUR 常用总 activity，可能在远离平衡时较松。作者引入 state mobility m_t，将 probability current 与 thermodynamic force 的关系写成对数均值结构，并把时间积分 mobility Mτ 与 irreversible entropy production Στ 配对。"),
            sec("模型与方法", "作者先对一般离散 Markov master equation 推导 improved TUR，再对所有满足端点和图拓扑约束的 transition-rate matrices 做变分。最优 dynamics 可由 optimal transport coupling 构造，使 W1 等于最小的 ∫√(σ_t m_t)dt，并给出 Στ Mτ 乘积的精确下界。", "随后将框架应用于 classical speed limits、finite-time information erasure 和 quantum master/Lindblad dynamics。量子部分在选定基底/跃迁表示中定义 population currents 与 quantum state mobility；它扩展了结构，但不是任意 coherent control 的统一几何。"),
            sec("核心结果与证据", "核心变分式表明 W1(p^A,p^B)=min∫0^τ√(σ_t m_t)dt，并进一步得到 W1²≤Στ Mτ。与基于 activity 的标准 TUR 相比，mobility bound 在文中模型和数值例子中更紧；等号可由满足 detailed-balance-like optimal construction 的可控跃迁率达到。", "Figure 3 说明 transport geometry 取决于允许跃迁图：同一端点概率在不同 topology 下具有不同最短路径代价。Figure 4 再把 W1、minimum dissipation 与 mobility 的关系画成统一结构，Figures 5–6 分别展示 classical erasure/speed-limit 和 quantum applications。", "有限时间 Landauer bound 在 quasistatic kBT ln2 之外增加由 transport distance、mobility 和 duration 决定的项；speed limit 则把达到给定 distributional change 所需时间下界化。所谓 exact minimum 是在作者允许优化 transition rates、固定 topology 与 mobility convention 的 admissible class 内成立。"),
            sec("有效性与局限", "结果依赖离散状态、Markovian dynamics、well-defined currents 与选定 mobility；连续扩散使用不同 Wasserstein order/metric convention，不能直接把离散公式逐项替换。若实验只能控制部分 rates、rates 有上限或需保持固定 steady state，文中可达等号的 protocol 可能不可实施。", "量子推广主要控制 populations 与 Lindblad transitions；coherence、non-Markovian baths、strong coupling 和 measurement backaction 需要额外处理。几何下界给必要代价而非具体装置的完整工程成本。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2206.02684；期刊：https://doi.org/10.1103/PhysRevX.13.011013。核验 PDF SHA-256：9edb1d3e2b923c3e77e8a522193a489e59de0fa49640d006687eb4a02641eab5。本文以解析证明和可构造 toy protocols 为主，未给专用代码仓库。", "复现需明确 graph topology、endpoint distributions、transport cost、rate constraints、entropy-production 与 mobility definitions；数值求 optimal coupling 后应验证 master equation、端点、Στ、Mτ 和 equality gap。Evidence status: full-text verified analytical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.3–6 的 current、entropy production、mobility 与 improved TUR；pp.10–13 Figure 3 和 Theorem 1 建立离散 Wasserstein 变分式。再看 pp.17–23 的 minimum dissipation、speed limits 和 Landauer bound，量子推广查 pp.24–29；始终核对 admissible dynamics。"),
        ],
        "figure-3-discrete-wasserstein.webp", "Figure 3", 12, "schematic",
        "五节点允许跃迁图及由其拓扑计算的最短路径距离矩阵。",
        "离散 Wasserstein 代价由可达图的最短路径决定，因此热力学下界也依赖允许的跃迁结构。",
        "Figure 3 最清楚地展示抽象最优输运距离如何嵌入 Markov jump thermodynamics。",
        [{"label":"Mobility-weighted transport identity","latex":r"\mathcal W_1(p^A,p^B)=\min_{\{W_t\}}\int_0^\tau\sqrt{\sigma_t m_t}\,dt=\min_{\{W_t\}}\sqrt{\Sigma_\tau\mathcal M_\tau}","role":"relate discrete transport distance to minimum thermodynamic cost","symbols":{"sigma_t":"instantaneous entropy-production rate","m_t":"state mobility","Sigma_tau":"integrated irreversible entropy production","M_tau":"integrated mobility"},"evidence":"paper.pdf p. 12, Eqs. (73)–(74), and subsequent theorem","interpretation":"The minima range over admissible controllable Markov rates on the fixed graph."}],
        ["paper.pdf pp. 3–8: improved TUR and dynamical mobility","paper.pdf pp. 10–13, Figure 3 and Theorem 1: discrete Wasserstein construction","paper.pdf pp. 17–23, Figures 4–5: minimum dissipation, speed limits and Landauer bound","paper.pdf pp. 24–29, Figure 6: quantum extension","source PDF SHA-256 9edb1d3e2b923c3e77e8a522193a489e59de0fa49640d006687eb4a02641eab5","Evidence status: full-text verified analytical study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.13.041032", "arXiv v1 manuscript", "https://arxiv.org/pdf/2201.00098",
        "Optimal Control of Nonequilibrium Systems through Automatic Differentiation",
        "通过自动微分实现非平衡系统最优控制", "theory_numerics",
        "89a2dae3d48659b5", "Control & Reinforcement Learning",
        {"doi":"10.1103/PhysRevX.13.041032","arxiv_id":"2201.00098","version":"arXiv v1 full text","title":"Optimal Control of Nonequilibrium Systems through Automatic Differentiation","authors":["Megan C. Engel","Jamie A. Smith","Michael P. Brenner"],"journal":"Physical Review X","volume":"13","issue":"4","article":"041032","published":"2023-11-16","abstract":"Automatic differentiation through stochastic simulations optimizes nonequilibrium protocols, reproducing analytical near-equilibrium solutions and finding lower-work controls for Ising and barrier-crossing systems far from equilibrium.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Megan C. Engel、Jamie A. Smith、Michael P. Brenner；Physical Review X 13, 041032 (2023)，DOI:10.1103/PhysRevX.13.041032。核验 arXiv:2201.00098v1 全文26页；未发现关联更正或撤稿。"),
            sec("研究问题", "有限时间驱动常远离 equilibrium，linear-response thermodynamic geometry 只在慢驱动附近可靠；直接搜索 protocol 又要对 stochastic simulator 求梯度。论文问：能否让 automatic differentiation 穿过 Monte Carlo 或 Langevin trajectory，直接最小化平均 dissipated work/entropy production，并在 far-from-equilibrium 区域发现理论近似遗漏的控制结构？"),
            sec("背景", "控制 protocol λ(t) 决定能量函数并驱动概率分布。near equilibrium 时最优速度与 thermodynamic metric/friction tensor 有关，但高 barrier、phase transition 和短 duration 会产生强迟滞。AD 可对可微程序做 reverse-mode differentiation；随机采样需重参数化或连续松弛以保留 gradient path。", "作者不是训练 reinforcement-learning policy，而是优化预先参数化、低维、open-loop time schedule。目标由一批模拟 trajectory 的平均 work 或 entropy production 估计。"),
            sec("模型与方法", "三类验证依次增加复杂性：二维 32×32 Ising model 同时控制 magnetic field B(t) 与 temperature T(t)；Brownian particle in a moving harmonic trap 具有已知精确 optimum；double-well barrier crossing 由 harmonic trap center 驱动。实现基于 JAX，对整段 dynamics unroll 后反向传播。", "Ising Monte Carlo 的离散 spin flips 以 differentiable approximation 处理；连续 Langevin noise 用固定 random draws/reparameterization。每轮用多条 trajectories 估计 stochastic gradient，更新离散 time-control points，并用独立/更多 trajectories 评估 protocol。"),
            sec("核心结果与证据", "在 harmonic trap 的可解问题中，AD protocol 收敛到理论 optimum，表明 simulator gradient 和 optimizer 能恢复已知答案。Ising reversal 中联合调节 B、T 可在 phase-transition 附近降低 entropy production；Figure 1 的有限样本曲线支持该具体 32×32、固定 duration protocol。", "Figure 3 对 2.5 kBT barrier 的 near-equilibrium case，AD、theory 的 path 与 work distribution 基本重合；在 10 kBT barrier 下，AD path 变得不对称，并在开始/结束出现离散 jumps。其平均 dissipated work 约3.260±0.007 kBT，低于 near-equilibrium theory 的5.37±0.02 kBT 和 linear protocol 的5.172±0.009 kBT。", "高 barrier optimum 先加速接近 barrier、后缓慢离开，使粒子更早获得越障机会；这解释曲线而非单纯黑箱胜出。数值优化找到的是给定参数化和初始化下的低损失解，论文没有证明全局最优。"),
            sec("有效性与局限", "AD 需要可微或可松弛的 simulator；离散事件、chaotic long trajectories 和 rare transitions 会导致 biased/high-variance gradients。计算和内存随 trajectory length 与 ensemble size 增长，实验硬件还需可微 surrogate 或 system identification。", "示例的控制维度低、duration 固定、模型动力学已知且没有未知 delay/constraints。优化可能依赖 initialization 和 local minima；‘far from equilibrium outperforms theory’仅指文中 near-equilibrium approximation 与 baseline，不是对所有控制算法的比较。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2201.00098；期刊：https://doi.org/10.1103/PhysRevX.13.041032。核验 PDF SHA-256：b2cdb300dba35359037ec415c8c696a5f8716f7dad018aee4244c0cd052fcf29。正文说明使用 JAX；代码可用性应以论文当前 Data/Code statement 为准。", "复现需固定 dynamics discretization、random seeds、trajectory count、control knots、optimizer/learning rate、gradient estimator、initial protocol、evaluation ensemble 与 confidence intervals；Ising 松弛还需与真实 discrete dynamics 复核。Evidence status: full-text verified simulation/control study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–4 的 differentiable simulation workflow，再看 pp.5–6 Figure 1 的 Ising control。p.7 harmonic trap 是 correctness check，p.8 Figure 3 是 far-from-equilibrium 核心证据；最后读 Methods/Appendix 核对 stochastic gradients、松弛和样本数。"),
        ],
        "figure-3-optimal-protocols.webp", "Figure 3", 8, "comparison",
        "低与高势垒下线性、近稳态理论和自动微分控制协议及其耗散功分布。",
        "低势垒时 AD 复现近稳态理论；高势垒时出现非对称路径和边界跳跃，并降低平均耗散功。",
        "Figure 3 同时提供已知极限校验与远离平衡时改进的定量证据。",
        [{"label":"Protocol objective","latex":r"\lambda^*=\arg\min_\lambda\;\langle W_{\rm diss}[x_{0:T};\lambda]\rangle,\qquad \nabla_\lambda\langle W_{\rm diss}\rangle\approx\frac1M\sum_{m=1}^M\nabla_\lambda W_{\rm diss}^{(m)}","role":"optimize an open-loop protocol by differentiating through stochastic trajectories","symbols":{"lambda":"time-discretized control","W_diss":"dissipated work","M":"trajectory batch size"},"evidence":"paper.pdf pp. 2–4, optimization framework","interpretation":"The gradient is estimator- and simulator-dependent and does not guarantee a global optimum."}],
        ["paper.pdf pp. 2–4: automatic-differentiation control framework","paper.pdf pp. 5–6, Figure 1: Ising magnetization reversal","paper.pdf p. 7, Figure 2: harmonic-trap analytical check","paper.pdf p. 8, Figure 3: low- and high-barrier protocols and work distributions","source PDF SHA-256 b2cdb300dba35359037ec415c8c696a5f8716f7dad018aee4244c0cd052fcf29","Evidence status: full-text verified simulation/control study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.13.041044", "arXiv v3 manuscript", "https://arxiv.org/pdf/2202.06936",
        "Minimum-Action Method for Nonequilibrium Phase Transitions", "非平衡相变的最小作用量方法",
        "theory_numerics", "a645297207d3ac53", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.13.041044","arxiv_id":"2202.06936","version":"arXiv v3 full text","title":"Minimum-Action Method for Nonequilibrium Phase Transitions","authors":["Ruben Zakine","Eric Vanden-Eijnden"],"journal":"Physical Review X","volume":"13","issue":"4","article":"041044","published":"2023-12-07","abstract":"Minimum-action algorithms for general nonequilibrium Hamiltonians compute directional quasipotentials, coexistence lines, nucleation barriers, and asymmetric transition paths in field and reaction-diffusion models.","comment":"ArXiv v3 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Ruben Zakine、Eric Vanden-Eijnden；Physical Review X 13, 041044 (2023)，DOI:10.1103/PhysRevX.13.041044。核验 arXiv:2202.06936v3 全文27页；未发现关联更正或撤稿。"),
            sec("研究问题", "equilibrium first-order transition 可由 free-energy minima 和 equal-depth condition 判断；nonequilibrium systems 通常没有自由能，forward/backward rare transitions 也不沿同一路径。论文问：能否从 stochastic dynamics 的 path large deviations 直接计算 directional quasipotentials、coexistence line、critical nucleus 与 nucleation barrier，并适用于非 Gaussian noise？"),
            sec("背景", "弱噪声 ε 下，一条 trajectory 的概率按 exp[-S/ε] 缩放；从稳定态到分界面的最小 action 给 quasipotential barrier，transition rate 呈 Arrhenius-like exp[-V/ε]。非平衡时 V(A→B) 与 V(B→A) 不必相等，stationary weights 由两个方向的 escape rates 共同决定。", "minimum action method 将罕见 transition 转成 Hamiltonian boundary-value optimization。与 equilibrium nudged-elastic-band 不同，Hamiltonian 可由 Markov jump/reaction noise 产生且不必二次，路径还含 conjugate momentum。"),
            sec("模型与方法", "作者发展适用于一般 convex Hamiltonian 的 minimizer 与 geometric string algorithms：在离散 path 上交替优化 momentum/coordinate，并用 arclength reparametrization 避免无限 transition time。phase coexistence 通过两个方向 quasipotential 相等确定，而不是假设某个 free energy。", "数值例一是含 non-gradient term κ 的一维 Ginzburg–Landau field；例二是空间离散 Schlögl reaction-diffusion network，具有 Poissonian reaction noise。作者扫描参数得到 phase diagram，并比较 forward/backward minimizers、heteroclinic descent 与 nucleation-size scaling。"),
            sec("核心结果与证据", "在 modified Ginzburg–Landau model 中，κ 破坏 detailed balance 后 coexistence line 偏离 equilibrium Maxwell-like condition。Figure 5 给 phase diagram；Figure 6 显示从 ρ−→ρ+ 与反向的 minimum-action paths 在不同位置越过 separatrix，具有不同 critical nuclei 和 action accumulation。", "Figure 6 的上排是 density path，第二排是 conjugate momentum，第三排是 action density；forward minimizer 与 string 结果接近，而 backward path 明显不同。越过 critical nucleus 后 momentum 与 Lagrangian 归零，系统沿 noiseless relaxation 下坡，这把 rare fluctuation 与 deterministic descent 分开。", "Schlögl network 的 Figures 7–8 复现同类方向不对称，并处理非 Gaussian jump noise。Figure 10 显示大系统下 nucleation barrier/critical droplet 的尺度行为。结果支持方法可跨 diffusion field 与 reaction network，但仍是已知 coarse-grained models 的数值计算。"),
            sec("有效性与局限", "quasipotential/rate interpretation是 ε→0 large-deviation 渐近；中等噪声、多重竞争路径和有限 observation time 可能改变 prefactor 或主导机制。数值 path discretization、domain size、mesh 和初始 string 会导致局部极小与分支遗漏。", "方法要求已知 Markov generator 或 Hamiltonian，不能从原始实验轨迹自动识别动力学。文章主要计算 exponential action，不系统给 Kramers prefactor；phase boundary 的有限噪声修正、真实材料参数和实验验证超出范围。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2202.06936；期刊：https://doi.org/10.1103/PhysRevX.13.041044。核验 PDF SHA-256：f08979841fd9af2d50ef7a833ca40deb050a9e50757e0473c755f79f8f0d2c13。正文未给专用代码仓库。", "复现需固定 spatial grid、boundary conditions、κ/h/D 或 reaction rates、path images、arclength rule、optimizer tolerance 与 initial strings；应从多初始化搜索并同时报告 forward/backward action、critical nucleus 和 discretization convergence。Evidence status: full-text verified theory/numerical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–5 的 path action、Hamiltonian 与 quasipotential；pp.6–9 看 numerical minimizer/string method。pp.12–15 Figures 5–6 是 GL 主结果，pp.16–19 Figures 7–8 是 Schlögl extension；最后看 nucleation scaling 和 discretization limitations。"),
        ],
        "figure-6-minimum-action-paths.webp", "Figure 6", 14, "trajectory",
        "非平衡 Ginzburg–Landau 模型的正向、反向最小作用量路径、共轭动量与沿路径作用量。",
        "正反相变穿越不同临界核；噪声负责越障，越过分界后则沿确定性动力学松弛。",
        "Figure 6 直接呈现非平衡相变方向不对称及最小作用量算法的一致性检查。",
        [{"label":"Quasipotential barrier","latex":r"V(a,b)=\inf_{T>0}\inf_{\phi(0)=a,\,\phi(T)=b}S_T[\phi],\qquad \mathbb P[\phi]\asymp e^{-S_T[\phi]/\epsilon}","role":"identify the most probable weak-noise transition path and exponential barrier","symbols":{"S_T":"path action","epsilon":"noise strength","phi":"state-space trajectory"},"evidence":"paper.pdf pp. 2–4, large-deviation formulation","interpretation":"This controls the leading weak-noise exponential; rate prefactors and finite-noise corrections are separate."}],
        ["paper.pdf pp. 2–5: large-deviation action and quasipotentials","paper.pdf pp. 6–9: minimizer and geometric string algorithms","paper.pdf pp. 12–15, Figures 5–6: Ginzburg–Landau phase diagram and directional paths","paper.pdf pp. 16–20, Figures 7–10: Schlögl network and nucleation scaling","source PDF SHA-256 f08979841fd9af2d50ef7a833ca40deb050a9e50757e0473c755f79f8f0d2c13","Evidence status: full-text verified theory/numerical study; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ids: list[str] = []
    for item in CARDS:
        pid = str(item["arxiv_id"])
        (OUT / f"{pid}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        ids.append(pid)
    print(json.dumps({"installed": ids}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
