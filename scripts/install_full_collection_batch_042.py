#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 042."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-physrevx.14.021052", "arXiv v2 manuscript", "https://arxiv.org/pdf/2304.09207",
        "Universal Phenomenology at Critical Exceptional Points of Nonequilibrium O(N) Models",
        "非平衡 O(N) 模型临界异常点的普适现象", "theory", "9f94f1f923dc0de3", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.14.021052","arxiv_id":"2304.09207","version":"arXiv v2 full text","title":"Universal Phenomenology at Critical Exceptional Points of Nonequilibrium O(N) Models","authors":["Carl Philipp Zelle","Romain Daviet","Achim Rosch","Sebastian Diehl"],"journal":"Physical Review X","volume":"14","issue":"2","article":"021052","published":"2024-06-26","abstract":"Nonequilibrium O(N) field theories at critical exceptional points exhibit rotating order and enhanced Goldstone modes, while fluctuations below four dimensions either restore symmetry or drive a first-order transition.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Carl Philipp Zelle、Romain Daviet、Achim Rosch、Sebastian Diehl；Physical Review X 14, 021052 (2024)，DOI:10.1103/PhysRevX.14.021052。核验 arXiv:2304.09207v2 全文44页；未发现关联更正或撤稿。"),
            sec("研究问题", "平衡临界动力学中 friction 与 thermal noise 受 fluctuation–dissipation relation 约束；非平衡 antidamping 可令摩擦消失而噪声仍有限。论文问：当 exceptional point 与连续相变重合时，非线性涨落会产生怎样的普适宏观行为，mean-field 的静态—旋转有序连续边界能否在 d<4 保持？"),
            sec("背景", "作者研究非守恒 O(N) stochastic field theory：对称无序相、O(N)→O(N−1) 静态有序相和 O(N)→O(N−2) rotating/limit-cycle phase 相邻。在线性响应的 CEP，两支衰减 mode 合并，damping 趋零而 noise 不消失，产生 q^{-4} 级增强的 phase fluctuations。", "exceptional point 在这里是 full retarded response 的 pole/eigenvector coalescence，不只是非 Hermitian single-particle spectrum。limit cycle 多出 time-translation 与内部 rotation 锁定结构；mean field 计数给 rotating phase 2N−3 个 Goldstone modes。"),
            sec("模型与方法", "从 mesoscopic Langevin dynamics 构建 Martin–Siggia–Rose–Janssen–De Dominicis action，再通过 effective action 将涨落重整化到 response、noise 与 nonlinear vertices。N=2 情形用 Dyson–Schwinger equations 自洽重求和 loop corrections；任意 N 则在 long-wavelength nonlinear sigma model 中推广。", "作者比较 Gaussian scale、Ginzburg scale、symmetry-restoration scale 与 fluctuation-induced first-order scale，并构造 weakly driven easy-plane ferrimagnet 及 Lindblad O(N) realizations。后两者是可实现机制与有效模型映射，不是实验观测。"),
            sec("核心结果与证据", "mean field 的 phase diagram 包含沿静态—旋转边界的 critical exceptional line，所有边界在 multicritical exceptional point 汇合。Figure 1(a) 展示该结构；Figure 1(b) 给出 d<4 时涨落后的两种结局：增强涨落先恢复对称，或连续 CEP 线被 first-order transition 替代。", "Gaussian CEP 的 equal-time phase correlation 约按 q^{-4} 发散，使 upper/lower critical dimensional structure 相对普通 O(N) criticality 改变。自洽方程没有流向稳定二阶 fixed point；quartic time-derivative coupling 可变负并形成有限 rotation frequency 的新 minimum，从而支持 weakly first-order jump。", "两种结局由裸 order amplitude 与 nonlinear coupling 的组合控制；远离最终窄尺度区仍可能观察近似 Gaussian CEP scaling。论文因此没有宣称 d<4 存在一个新的精确连续 universality class，而是说明 fluctuations 会阻止直接到达它。"),
            sec("有效性与局限", "结论建立在 Markovian local O(N) field theory、无额外 conserved hydrodynamic modes、long-wavelength expansion 和自洽 resummation 上。Dyson–Schwinger 截断不是严格 all-orders theorem，first-order 与 symmetry-restoration 的分界含非普适裸参数。", "weakly driven ferrimagnet 和 Lindblad 模型说明对称性上可实现，但材料参数、heating、finite-size/time 与实验读出未验证。对 N、d 和 coupling 的外推应保留文章给出的适用区，不能把所有 many-body exceptional points 都归入同一机制。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2304.09207；期刊：https://doi.org/10.1103/PhysRevX.14.021052。核验 PDF SHA-256：c6b716a45304cffea7433319861ae13de004eeb0ec7f02de8cc741e96fee548f。本文为解析场论研究，正文未给专用代码仓库。", "复现需固定 effective action convention、noise normalization、UV cutoff、dimension、N 与 bare couplings；逐步验证 pole coalescence、Goldstone counting、loop integrals和自洽方程的多分支稳定性。Evidence status: full-text verified analytical field-theory study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–4 Figure 1 和 Figure 2 确认 phase/CEP 定义；pp.8–13 看 effective action、response poles 与 Goldstone counting。pp.18–25 是 fluctuation/resummation 核心，Figure 13–14 总结两种结局；最后读 driven-magnet realization，区分普适论证与平台建议。"),
        ],
        "figure-1-critical-exceptional-phase-diagram.webp", "Figure 1", 3, "phase_diagram",
        "非守恒 O(N) 模型的平均场和涨落修正相图，含静态、旋转与对称相。",
        "平均场 CEP 连续线在 d<4 被强涨落改造成对称区间或一级静态—旋转转变。",
        "Figure 1 集中展示文章的 phase structure 与最关键的 fluctuation-induced revision。",
        [{"label":"Critical exceptional correlation","latex":r"G^K_{\theta,ii}(q,t=0)\xrightarrow{\delta\to0}\frac{C}{q^4}","role":"diagnose enhanced phase fluctuations when damping vanishes at finite noise","symbols":{"theta":"Goldstone phase field","delta":"renormalized damping distance from the CEP","q":"wave number"},"evidence":"paper.pdf pp. 18–19, Eq. (75)","interpretation":"The q^{-4} divergence is the Gaussian CEP signal whose nonlinear fate is analyzed by resummation."}],
        ["paper.pdf pp. 2–4, Figures 1–3: phase structure and realization concept","paper.pdf pp. 8–13, Figures 4–8: response poles and Goldstone modes","paper.pdf pp. 18–25, Figures 9–14: fluctuation enhancement and self-consistent resummation","paper.pdf pp. 27–34: driven ferrimagnet and Lindblad realizations","source PDF SHA-256 c6b716a45304cffea7433319861ae13de004eeb0ec7f02de8cc741e96fee548f","Evidence status: full-text verified analytical field-theory study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.15.021050", "arXiv v1 manuscript", "https://arxiv.org/pdf/2401.02252",
        "Thermodynamics of Active Matter: Tracking Dissipation across Scales", "主动物质热力学：跨尺度追踪耗散",
        "theory_numerics", "55a5119256ca0bc8", "Active Matter",
        {"doi":"10.1103/PhysRevX.15.021050","arxiv_id":"2401.02252","version":"arXiv v1 full text","title":"Thermodynamics of Active Matter: Tracking Dissipation across Scales","authors":["Robin Bebon","Joshua F. Robinson","Thomas Speck"],"journal":"Physical Review X","volume":"15","issue":"2","article":"021050","published":"2025-05-12","abstract":"A bottom-up stochastic-thermodynamic derivation follows chemical dissipation from explicit catalytic particles through active Brownian particles to hydrodynamic and scalar field theories.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Robin Bebon、Joshua F. Robinson、Thomas Speck；Physical Review X 15, 021050 (2025)，DOI:10.1103/PhysRevX.15.021050。核验 arXiv:2401.02252v1 全文24页；未发现关联更正或撤稿。"),
            sec("研究问题", "active Brownian particle 方程只保留位置和取向，却隐藏持续消耗 fuel 的化学自由能；从可见轨迹做 time-reversal inference 因而可能漏掉主要耗散。论文问：能否从显式 catalytic solute conversion 出发，逐级 coarse-grain 到 ABP、density–polarization hydrodynamics 和 scalar field theory，同时保留正确的 entropy production 与 local dissipation？"),
            sec("背景", "完整 stochastic thermodynamics 要包含所有向环境传递 entropy 的 degrees of freedom。仅对 position/orientation 路径计算的 informatic entropy production 可小于真实 thermodynamic dissipation，尤其当隐藏 chemical events 与机械位移在粗粒化后不再可逆辨认。", "Figure 1 给出四层尺度链：explicit fuel/solute model→ABPs→hydrodynamic fields→density-only scalar theory。作者的主张不是 coarse-graining 无损，而是追踪哪些 thermodynamic currents 被积分掉以及它们如何进入剩余场的 dissipation formula。"),
            sec("模型与方法", "微观层研究 catalytic Janus particle 周围两类溶质的扩散与表面转换，计算 steady concentration、solute flux、propulsive force 和 chemical entropy production。再将多次反应事件近似为 along-orientation biased random walk，导出 ABP speed、translational noise 与 effective chemical attempt rate。", "多粒子层从 N-body Fokker–Planck/Dean-like hierarchy 得到 density ρ 与 polarization p 的 hydrodynamics，并由 microscopic free-energy consumption 推导 global/local heat rate。作者用解析 wall profile 与 ABP MIPS simulations 比较 source、sink 与 boundary flux，最后在 polarization 快变量极限消去 p 得到 scalar field description。"),
            sec("核心结果与证据", "底层推导显示相同 ABP equation 可对应不同 reaction attempt rate 和 chemical affinity，因此仅由 effective speed/noise 不能唯一推断真实 heat dissipation。文章给出与 microscopic reaction flux 一致的平均 entropy production，并指出 naive Onsager-current substitution 会遗漏或错配局部项。", "Figure 5 的平墙例子显示 particle accumulation 形成强 density-dependent source，边界附近也可有相对较小的 dissipation sink；全局仍由 fuel turnover 支配。Figure 6 的 MIPS simulation 将 dense/dilute domains 的 density、polarization 与 coarse-grained dissipation 对照，界面和局域极化重排改变空间分布。", "消去 polarization 后，scalar field 的 visible irreversibility 可快速衰减，而底层 chemical dissipation 仍为 extensive leading term。Figure 1 因此是方法学主线：若 coarse-graining 时没有保留 reservoir bookkeeping，路径不可逆性不能自动等同于热。"),
            sec("有效性与局限", "显式模型采用理想化 solute diffusion、reaction boundary conditions、overdamped dynamics 与近似 scale separation；真实 phoretic mobility、hydrodynamic interactions、finite reservoirs 和 nonlinear chemistry 会改变参数。field closure 与快速 polarization elimination 只在长波慢时标适用。", "数值示例是 ABP wall/MIPS 而非热量直接实验；local dissipation 的细节对 effective reaction rate 和 coarse-graining convention 很敏感。研究也不意味着观测不可逆性无用，而是要求把它标为 lower-dimensional/informatic quantity。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2401.02252；期刊：https://doi.org/10.1103/PhysRevX.15.021050。核验 PDF SHA-256：e5099ef0c0acd5b6f24533f0cb4a5dc1456e5a28d05ff6a4da1719df0b053cf2。正文致谢相关 simulation code/data，但未在核验文本中给统一公开仓库链接。", "复现需固定 reaction rates、chemical potential difference、solute diffusivity、phoretic coupling、ABP mapping、interaction potential、box/wall、MIPS density、grid 与 time averaging；分别核对 microscopic、ABP 和 field-level heat balance。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1 把握尺度链；pp.3–6 看 catalytic particle 与 entropy production，pp.7–9 看 ABP mapping。pp.10–14 推导 field heat balance，Figures 5–6 是 wall/MIPS 应用；最后读 scalar-field section，比较 thermodynamic 与 informatic dissipation。"),
        ],
        "figure-1-dissipation-across-scales.webp", "Figure 1", 2, "schematic",
        "从显式催化粒子、主动布朗粒子到流体场和密度标量场的逐级粗粒化示意。",
        "每次粗粒化都减少可见自由度，因此必须单独追踪被隐藏的化学耗散。",
        "Figure 1 定义全文跨尺度热力学账本，优先于单一壁面或 MIPS 数值图。",
        [{"label":"Chemical entropy production","latex":r"\dot S_{\rm tot}=\sum_\alpha J_\alpha\,\Delta\mu_\alpha/T\ge0","role":"account for reservoir free-energy consumption before coarse graining","symbols":{"J_alpha":"net chemical event current","Delta_mu_alpha":"chemical affinity","T":"bath temperature"},"evidence":"paper.pdf pp. 3–7, explicit catalytic-particle thermodynamics","interpretation":"The effective ABP trajectory alone generally does not determine the hidden event current."}],
        ["paper.pdf pp. 1–2, Figure 1: hierarchy of coarse-grained descriptions","paper.pdf pp. 3–7, Figures 2–3: catalytic particle and ABP mapping","paper.pdf pp. 9–13, Figure 4: hydrodynamic heat balance and boundary flux","paper.pdf pp. 14–17, Figures 5–6: wall aggregation and MIPS dissipation","source PDF SHA-256 e5099ef0c0acd5b6f24533f0cb4a5dc1456e5a28d05ff6a4da1719df0b053cf2","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.15.021051", "arXiv v6 manuscript", "https://arxiv.org/pdf/2306.10404",
        "RL Perceptron: Generalization Dynamics of Policy Learning in High Dimensions",
        "RL 感知机：高维策略学习的泛化动力学", "theory_numerics", "2ceed9b03362ddf0", "Control & Reinforcement Learning",
        {"doi":"10.1103/PhysRevX.15.021051","arxiv_id":"2306.10404","version":"arXiv v6 full text","title":"RL Perceptron: Generalization Dynamics of Policy Learning in High Dimensions","authors":["Nishil Patel","Sebastian Lee","Stefano Sarao Mannelli","Sebastian Goldt","Andrew Saxe"],"journal":"Physical Review X","volume":"15","issue":"2","article":"021051","published":"2025-05-13","abstract":"An analytically solvable teacher-student reinforcement-learning perceptron reduces high-dimensional policy learning to order-parameter ODEs and exposes curricula, fixed points, and speed-accuracy tradeoffs.","comment":"ArXiv v6 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Nishil Patel、Sebastian Lee、Stefano Sarao Mannelli、Sebastian Goldt、Andrew Saxe；Physical Review X 15, 021051 (2025)，DOI:10.1103/PhysRevX.15.021051。核验 arXiv:2306.10404v6 全文21页；未发现关联更正或撤稿。"),
            sec("研究问题", "policy-gradient RL 的 learning curves、fixed points 与 generalization 常只靠实验观察，深网络又难解析。论文问：在高维 teacher–student sequential-decision task 中，能否精确闭合策略权重的宏观动力学，并用它解释 reward timing、negative reward、episode length 与 learning-rate schedules 如何影响速度和最终准确率？"),
            sec("背景", "teacher perceptron 对每个 Gaussian state 给正确二元 action；student perceptron 以整段 episode return 更新权重。泛化由 student–teacher normalized overlap ρ 决定，error εg=arccos(ρ)/π。D→∞ 时 microscopic weights 可由 norm Q 与 overlap R 两个 self-averaging order parameters 描述。", "这是可解的 online policy-learning toy model：state distribution、teacher rule 与 episodic update 已知。它保留 delayed/sparse reward 和 sequential success condition，却没有 environment dynamics、value function、exploration state distribution shift 或深网络 representation learning。"),
            sec("模型与方法", "作者对每次 policy-gradient-like update 的 Gaussian averages 求期望，在 rescaled sample time α 上导出 Q、R 的 deterministic ODEs；不同 reward protocols 只改变相应 averages。有限 D=900 simulations 检查 ODE curves，并解析 fixed points、critical learning rates 与 convergence times。", "随后优化随训练变化的 episode length T 和 learning rates η1、η2，研究 all-decisions-correct、partial reward、penalty 等规则。外部案例在简化 Bossfight 与 Pong pixel environments 中训练 linear policies，检验理论提出的 speed–accuracy tension 是否定性出现。"),
            sec("核心结果与证据", "Figure 2 将四类 reward/episode protocols 的 ODE prediction（虚/实理论线）与有限维 simulation 曲线叠加，normalized overlap 的转折时间和终值一致。该结果验证 high-dimensional reduction，而不是证明所有 RL learning dynamics 都由两变量决定。", "negative reward 或 credit assignment 条件可产生 good/bad stable fixed points，靠近边界出现 critical slowing down；较强早期奖励会加速离开 plateau，却可能把 student 推入较差 asymptotic overlap。动态增加 T、anneal η 可兼顾早期速度和后期精度，Figure 3–6 给 phase maps 与 convergence scaling。", "Bossfight/Pong 的线性 policy 实验观察到 lives/reward stringency 增加时学习更慢而最终泛化改善，并出现可解释 weight maps。它们是定性 transfer evidence；图像环境、网络与训练预算均远小于标准 deep-RL benchmark。"),
            sec("有效性与局限", "精确 ODE 依赖 i.i.d. isotropic Gaussian inputs、single teacher perceptron、large D、online updates 与给定 return functional。有限维噪声、correlated states、多类 actions、nonstationary visitation 和 nonlinear policies 会增加 order parameters 或破坏闭合。", "最优 schedule 是相对于模型目标与 admissible controls，未计 wall-clock、variance reduction 和 exploration cost。Bossfight/Pong 只支持趋势，且算力限制影响 longest-run comparison；不能把 toy-model phase boundary 当成实际 PPO 等算法的通用超参数规则。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2306.10404；期刊：https://doi.org/10.1103/PhysRevX.15.021051。核验 PDF SHA-256：0d8eb8cbe3e9a17d7c08b00419b3c67a151284f21056aa5ac280628e6f36a101。论文正文给出 code/instructions 链接声明；复现时应记录实际仓库 commit。", "复现需固定 D、teacher/student initialization、episode length、reward rule、η1/η2、discount、number of agents/seeds 和 α normalization；分别积分 ODE、跑 finite-D simulation，再独立评估 Bossfight/Pong generalization。Evidence status: full-text verified theory/finite-model study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–5 Figure 1、Eqs. (6)–(9) 理解 overlap 与 error；p.5 Figure 2 是 ODE correctness 核心。pp.7–11 Figures 3–6 看 schedules、fixed points 和 slowing down；pp.12–14 Figures 7–8 是环境外推，最后用 appendices 核对 Gaussian averages。"),
        ],
        "figure-2-learning-dynamics.webp", "Figure 2", 5, "comparison",
        "四种奖励与 episode 协议下 student–teacher overlap 的 ODE 曲线和有限维模拟。",
        "两个 order parameters 的闭合动力学准确复现该 RL 感知机在多种协议下的学习转折与终值。",
        "Figure 2 在四种不同奖励与 episode 协议下逐一叠加理论和有限维模拟，是解析降维正确性及适用范围的最直接跨协议检验。",
        [{"label":"Perceptron generalization error","latex":r"\epsilon_g=\frac{1}{\pi}\arccos\!\left(\frac{R}{\sqrt{Q}}\right),\qquad R=\frac{\mathbf w\cdot\mathbf w^*}{D},\;Q=\frac{\mathbf w\cdot\mathbf w}{D}","role":"map high-dimensional student weights to a scalar policy-generalization metric","symbols":{"R":"student-teacher overlap","Q":"student weight norm","D":"input dimension"},"evidence":"paper.pdf p. 5, Eqs. (8)–(9)","interpretation":"The formula uses isotropic Gaussian states and binary teacher/student perceptrons."}],
        ["paper.pdf pp. 2–4, Figure 1: RL-perceptron task and update rule","paper.pdf p. 5, Figure 2 and Eqs. (6)–(9): ODE/simulation agreement","paper.pdf pp. 7–11, Figures 3–6: schedules, fixed points and slowing down","paper.pdf pp. 12–14, Figures 7–8: Bossfight and Pong evidence","source PDF SHA-256 0d8eb8cbe3e9a17d7c08b00419b3c67a151284f21056aa5ac280628e6f36a101","Evidence status: full-text verified theory/finite-model study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.9.011031", "arXiv v3 manuscript", "https://arxiv.org/pdf/1708.04993",
        "Quantifying Hidden Order out of Equilibrium", "量化非平衡体系中的隐序", "theory_numerics",
        "6c32ba54fb47359f", "Statistical Physics",
        {"doi":"10.1103/PhysRevX.9.011031","arxiv_id":"1708.04993","version":"arXiv v3 full text","title":"Quantifying Hidden Order out of Equilibrium","authors":["Stefano Martiniani","Paul M. Chaikin","Dov Levine"],"journal":"Physical Review X","volume":"9","issue":"1","article":"011031","published":"2019-02-14","abstract":"Lossless-compression length defines a computable information density that detects ordering and critical behavior in absorbing-state and active-particle systems without specifying an order parameter.","comment":"ArXiv v3 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Stefano Martiniani、Paul M. Chaikin、Dov Levine；Physical Review X 9, 011031 (2019)，DOI:10.1103/PhysRevX.9.011031。核验 arXiv:1708.04993v3 全文17页含补充材料；未发现关联更正或撤稿。"),
            sec("研究问题", "非平衡 steady/absorbing states 通常没有已知 ensemble probability，也可能事先不知道 order parameter。论文问：能否直接把单个离散化微观配置无损压缩，用 compressed length 构造 computable information density（CID），从而发现相变、relaxation time 和隐藏空间组织？"),
            sec("背景", "Shannon entropy 需要 source distribution；Kolmogorov complexity 对单个 sequence 定义最短程序却不可计算。LZ77 等 universal code 在大样本 ergodic source 下逼近 entropy rate，因此作者用 compressed binary length L(x) 除以原始 length L 作为可计算 proxy。", "CID 依赖 serialization、quantization、compressor header 与 finite-size extrapolation；它不是严格 Kolmogorov complexity，也不是 thermodynamic entropy 的普遍替代。优势是无需先指定哪个 correlation 或 density mode 应作为 order parameter。"),
            sec("模型与方法", "对 lattice configurations 直接编码 occupancy；off-lattice Random Organization 和 active Brownian particles 先把坐标量化为 binary grids。作者测 CID 随 density、time 与 system size 的变化，并与 active fraction、pair correlation、structure factor 和 relaxation time 对照。", "案例包括 2D Manna absorbing-state model、off-lattice Random Organization 与发生 MIPS 的 active Brownian particles。critical exponent 由 CID relaxation 与传统 active-fraction relaxation 的共同 power-law fit 得到；近热力学极限使用文中 LZ77 finite-length correction。"),
            sec("核心结果与证据", "Figure 3 的 Manna model 中 CID 随演化下降，并在 ρc≈0.683 附近形成 cusp-like minimum。CID relaxation time 与 active fraction 给出相同临界发散，拟合 ν∥≈1.3±0.2；它在没有输入 active-site order parameter 的情况下定位 absorbing transition。", "同图比较随机初态、动力学到达的 absorbing states 与均匀抽样 absorbing states：临界附近动力学选择的终态 CID 更低，揭示普通 density/active fraction 未直接表达的 hidden organization。Random Organization 的 Figure 4 给相似临界标度。", "ABP Figure 5 中均匀气体的瞬时配置持续变化但 CID 近稳；进入 MIPS 后 phase separation 产生更可压缩的大尺度结构。这个指标检测的是编码可利用的多尺度重复/相关，不会自动说明其物理机制或区分所有具有相似 compressibility 的状态。"),
            sec("有效性与局限", "有限文件压缩率受 alphabet、site ordering、grid resolution、compressor implementation 与 system size 影响；不同设置下 CID 的绝对值不可直接比较。universal-code 收敛可能慢，critical systems 的长程相关会加剧 finite-size corrections。", "量化连续坐标会丢失亚网格信息；旋转/平移或重新排序可能改变 serialized pattern，除非预处理固定。案例均为模拟系统，虽然相变位置与已知 observables 一致，但‘未知序’解释仍需后续 correlation/physics analysis。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/1708.04993；期刊：https://doi.org/10.1103/PhysRevX.9.011031。核验 PDF SHA-256：996cf2882c45dcfc62ae7a3d3733b49e906568749520ce6c488fd5347010699a。作者使用 LZ77；代码可用性应按当前期刊/补充声明核对。", "复现需固定 lattice/site traversal、binary alphabet、LZ77 variant、header treatment、grid bin size、system size、density、initial ensemble、cycles 与 bootstrap fits，并与至少一个独立 observable 对照。Evidence status: full-text verified numerical/compression study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Eqs. (1)–(2) 区分 Shannon、Kolmogorov 与 CID；pp.3–5 Figures 2–3 看 Manna hidden order。pp.6–8 Figures 4–5 是 off-lattice/ABP 扩展；最后读补充材料的 LZ77、finite-size extrapolation 和 serialization details。"),
        ],
        "figure-3-manna-cid.webp", "Figure 3", 5, "comparison",
        "二维 Manna 模型的微观更新、CID 演化、临界松弛时间和不同吸收态集合比较。",
        "CID 无需预设 active fraction 即定位吸收相变，并显示动力学选择的临界吸收态具有额外可压缩结构。",
        "Figure 3 将定义、临界标度与 hidden-order 证据放在同一组图中。",
        [{"label":"Computable information density","latex":r"\mathrm{CID}(x)=\frac{L_{\rm comp}(x)}{L(x)}","role":"estimate configuration information content with a fixed lossless compressor","symbols":{"L_comp":"binary length after lossless compression","L":"uncompressed sequence length","x":"serialized configuration"},"evidence":"paper.pdf p. 1, Eq. (2)","interpretation":"CID is compressor- and encoding-dependent at finite size and approaches an entropy-rate proxy only under stated asymptotic conditions."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(2): information measures and CID definition","paper.pdf pp. 3–5, Figures 2–3: correlations and Manna criticality","paper.pdf pp. 6–8, Figures 4–5: Random Organization and ABP applications","paper.pdf pp. 10–17: LZ77 and finite-size supplementary analysis","source PDF SHA-256 996cf2882c45dcfc62ae7a3d3733b49e906568749520ce6c488fd5347010699a","Evidence status: full-text verified numerical/compression study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.9.031043", "arXiv v1 manuscript", "https://arxiv.org/pdf/1903.01134",
        "Freezing a Flock: Motility-Induced Phase Separation in Polar Active Liquids",
        "冻结鸟群：极性主动液体中的运动诱导相分离", "theory_experiment", "315e6790dccd2ff5", "Active Matter",
        {"doi":"10.1103/PhysRevX.9.031043","arxiv_id":"1903.01134","version":"arXiv v1 full text","title":"Freezing a Flock: Motility-Induced Phase Separation in Polar Active Liquids","authors":["Delphine Geyer","David Martin","Julien Tailleur","Denis Bartolo"],"journal":"Physical Review X","volume":"9","issue":"3","article":"031043","published":"2019-09-09","abstract":"Quincke-roller experiments and nonlinear polar hydrodynamics show that dense flocks can arrest into propagating active solids through a first-order motility-induced phase separation.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Delphine Geyer、David Martin、Julien Tailleur、Denis Bartolo；Physical Review X 9, 031043 (2019)，DOI:10.1103/PhysRevX.9.031043。核验 arXiv:1903.01134v1 全文10页；未发现关联更正或撤稿。"),
            sec("研究问题", "传统 flocking 理论常把 motile units 视作恒速点粒子，难以描述高密度接触导致的减速和 arrest。论文问：极性主动液体随密度增加是否会形成真正的 active solid；若会，其 nucleation、coexistence、coarsening 与 hysteresis 是否满足一级相分离特征，能否由 motility-induced phase separation 解释？"),
            sec("背景", "实验以直径约5 μm 的 Quincke rollers 在长9.8 cm、宽2 mm 的 microfluidic racetrack 中运动；孤立速度约1040 μm/s。低密度先从 isotropic gas 经 flocking transition 进入 homogeneous polar liquid，再在更高 packing fraction 出现大部分粒子静止的 jammed domains。", "active solid 不是静态平衡晶体：局部结构可重排，边界持续 melting/freezing，整个 jam 还能逆着 polar-liquid flow 稳定传播。作者用‘solid’强调动力 arrest 与更高短程结构，而非长程晶格有序。"),
            sec("模型与方法", "视频追踪给 density ρ(r,t)、longitudinal current W(r,t)、orientation 与 velocity distributions；改变平均 packing fraction 和 electric-field amplitude，记录 nucleation、domain length、bulk coexistence densities、coarsening 与 cycling hysteresis。", "理论在一维 Toner–Tu-like density/current equations 中加入随 density 急降的 motility/alignment coefficients ε1(ρ)、ε2(ρ) 以及 density diffusion。线性 stability 与数值 PDE 解给 gas、polar bands、uniform liquid、traveling jam coexistence 和 uniform arrested phase。"),
            sec("核心结果与证据", "Figure 3(a–c) 显示 jam fraction 在 onset 处不连续跳变并出现两种可能状态；进入 coexistence 后 polar-liquid 与 active-solid bulk densities 近似保持，增加总密度主要改变 solid length，符合 lever rule。", "Figure 3(d) 中两个 jams 在总 solid fraction 近恒定时一个增长、另一个缩小，支持 slow coarsening；Figure 3(e–f) 随 electric field 上下扫描得到不同 solid fraction，形成 hysteresis。nucleation、bistability、lever rule、coarsening 与 hysteresis 联合支持 first-order dynamical phase separation。", "测得 roller speed 在 local density 超过约0.35后骤降。非线性 hydrodynamics 因 effective pressure/current 随密度降低而发生 spinodal instability，复现实验的五个 phase regimes 与 traveling fronts；机制属于 complete MIPS，但 polar order 令 dense jam 可在 dilute flock 中传播。"),
            sec("有效性与局限", "实验平台是特定电驱 Quincke colloids、准一维 racetrack 与有限 observation time；near-field lubrication/electrohydrodynamic interaction 的 microscopic slowing mechanism未被唯一确认。面积分数、场强和边界不能直接映射到动物群或机器人群。", "hydrodynamic model 是一维 mean-field closure，忽略横向 fluctuations 并以经验 density-dependent coefficients 表示微观作用。它解释 phase topology 和 fronts，但不是对每个粒子 interaction 的参数无关预测；‘generic flock freezing’仍要求其他系统验证。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/1903.01134；期刊：https://doi.org/10.1103/PhysRevX.9.031043。核验 PDF SHA-256：9db05703aff22f2c67a7a83c6c481921204502385aa9afc10d055393c88668e9。论文含 supplementary movies；正文未给统一代码仓库。", "复现需固定 bead/electrolyte、cell geometry、AC/DC field、camera/tracking、density calibration、velocity threshold、ramp rate 与 hysteresis protocol；PDE 部分需固定 ε1/ε2、Dp、Dw、λ、grid 和 initial perturbations。Evidence status: full-text verified experiment/theory study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1 看 gas→flock→active solid；pp.2–4 Figure 2 检查 jam structure/dynamics。p.4 Figure 3 是一级相分离的核心证据；pp.4–6 Figures 4–5 给 hydrodynamic mechanism，最后读 appendices 核对实验与 PDE 参数。"),
        ],
        "figure-3-active-solidification.webp", "Figure 3", 4, "comparison",
        "Quincke roller 赛道中的固态堵塞、固相比例、共存密度、粗化和电场循环滞回。",
        "不连续跳变、定密度共存、杠杆律、粗化与滞回共同支持一级主动固化。",
        "Figure 3 汇集区分普通拥堵与 first-order phase separation 的主要实验判据。",
        [{"label":"Polar active hydrodynamics","latex":r"\partial_t\rho+\partial_x W=D_\rho\partial_{xx}\rho,\qquad \partial_tW+\lambda W\partial_xW=D_W\partial_{xx}W-\partial_x[\epsilon_1(\rho)\rho]+[\rho\epsilon_2(\rho)-\phi]W-a_4W^3","role":"model density-dependent loss of motility and polar order","symbols":{"rho":"roller density","W":"longitudinal current","epsilon_1":"effective pressure/motility coefficient","epsilon_2":"alignment coefficient"},"evidence":"paper.pdf p. 4, Eqs. (1)–(2)","interpretation":"The density-dependent coefficients are phenomenological closures calibrated to the roller system."}],
        ["paper.pdf pp. 1–2, Figure 1: experimental phases of Quincke rollers","paper.pdf pp. 2–3, Figure 2: active-jam structure and motion","paper.pdf p. 4, Figure 3: first-order coexistence, coarsening and hysteresis","paper.pdf pp. 4–6, Figures 4–5: nonlinear hydrodynamic mechanism","source PDF SHA-256 9db05703aff22f2c67a7a83c6c481921204502385aa9afc10d055393c88668e9","Evidence status: full-text verified experiment/theory study; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ids: list[str] = []
    for item in CARDS:
        pid = str(item["arxiv_id"])
        (OUT / f"{pid}.json").write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ids.append(pid)
    print(json.dumps({"installed": ids}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
