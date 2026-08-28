#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 034."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_032 import card
from install_full_collection_batch_014 import sec


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1038-s42256-024-00937-0", "arXiv manuscript", "https://arxiv.org/pdf/2409.07590",
        "Deep learning for predicting rate-induced tipping", "用深度学习预测速率诱导突变",
        "ai_empirical", "98342fda698828fb", "Climate Dynamics",
        {"doi": "10.1038/s42256-024-00937-0", "arxiv_id": "2409.07590", "version": "arXiv v1 full text", "title": "Deep learning for predicting rate-induced tipping", "authors": ["Yu Huang", "Sebastian Bathiany", "Peter Ashwin", "Niklas Boers"], "journal": "Nature Machine Intelligence", "volume": "6", "pages": "1556–1565", "published": "2024-11-28", "abstract": "A one-dimensional CNN predicts trajectory-level rate-induced tipping probabilities in three noisy prototype systems where classical critical-slowing-down indicators do not separate tipping and non-tipping ensembles.", "comment": "arXiv full text cross-checked with open-access version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Yu Huang、Sebastian Bathiany、Peter Ashwin、Niklas Boers；Nature Machine Intelligence 6, 1556–1565 (2024)，DOI:10.1038/s42256-024-00937-0；全文取 arXiv:2409.07590，共35页含补充图。核验 Crossref 开放许可与状态，未发现关联更正或撤稿。"),
            sec("研究问题", "当外部 forcing 改变得太快，系统可能在静态平衡仍局部稳定时越过 basin boundary，发生 rate-induced tipping（R-tipping）；噪声又使相同 forcing 下部分轨迹突变、部分不突变。论文问：单条轨迹在突变前是否含有超越 variance 与 lag-1 autocorrelation 的可预测信息，以及深度网络能否输出提前量相关的突变概率？"),
            sec("背景", "critical slowing down（CSD）依赖系统接近缓慢移动的 equilibrium 与局部线性化；R-tipping 正是破坏这一假设。Figure 2 对 saddle-node、Bautin 和 Compost-bomb 三个原型施加相同时间 forcing、不同白噪声，显示突变时刻分布很宽且突变/非突变轨迹在视觉上高度重叠。", "这些都是已知随机微分方程的 ensemble simulations，不是气候观测。文章借 climate tipping 说明动机，但没有直接预测 AMOC、冰盖或真实生态系统的突变概率。"),
            sec("模型与方法", "三个原型分别包含移动固定点、移动周期吸引子和 soil-carbon/temperature feedback；用 Euler–Maruyama 积分并按是否越出 non-tipping envelope 标注。对每个 lead time，训练由两层一维 CNN、average pooling 和全连接层组成的二分类器；输入是截断到突变前的时间序列。", "作者将 tipping 与 non-tipping 样本配平，再用 Kolmogorov–Smirnov test 比较输出分布；Layer-wise Relevance Propagation（LRP）定位时间点贡献。不同 lead time 使用不同模型，因此实验已知距突变时间，尚不是无需时间对齐的在线报警器。"),
            sec("核心结果与证据", "saddle-node 模型的30万条 ensemble 中约37%突变；进一步各取60,000条形成 A/B 组。Figure 3 显示 variance 与 autocorrelation 的99%区间大幅重叠，而 DL 概率在突变前分离；KS 检验给出的可分提前量约为 saddle-node 290、Bautin 130、Compost-bomb 1000 time steps。", "在 saddle-node 的突变前100到10步，简单 envelope 方法成功率低于20%，CNN 从约60%升至95%。这是相对于作者构造的平衡分类任务与模拟分布；50%基线、时间步长和各模型的物理时间不同，不能直接横向解释为现实预警年数。", "LRP 的高 relevance 通常靠近输入末端，并在部分提前量上出现更早窗口；作者将其解释为 R-tipping fingerprint。LRP 是模型归因而非机制证明，且 forcing rate、噪声幅度变化会改变输出分布。"),
            sec("有效性与局限", "训练与测试来自同一三类低维方程和参数协议，标签依赖作者定义的 non-tipping envelope。模型能区分模拟轨迹不等于识别未知 governing equations、结构误差、非平稳观测噪声或多变量气候数据中的真实突变。", "实际应用通常不知道当前距突变还有多少时间，而本文逐 lead-time 训练；作者也把 continuous updating 作为未来工作。校准、class prevalence、false alarms、OOD forcing 与跨系统 transfer 尚未充分验证；CSD 失败只针对这些 R/N-tipping 设定。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2409.07590；期刊：https://doi.org/10.1038/s42256-024-00937-0；代码：https://github.com/yhuangDLClimate/predict-rate-induced-tipping。PDF SHA-256：d34199bac5003e5ca7785067984220079c51f697623243f35baa7d621f2ffd47。", "复现需固定三组 SDE 参数、dt、noise seeds、tipping envelope、group balancing、lead-time slicing、CNN filters/kernel、train split、KS/LRP 实现与概率校准。Evidence status: full-text verified simulation manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–4 与 p.19 Figure 1，确认 R-tipping 与 CSD 的适用边界；p.20 Figure 2看 ensemble 构造，pp.4–8看 CNN、KS 与 LRP 结果。最后读 pp.9–13 Discussion/Methods，特别保留‘已知 lead time、三类原型系统、模拟数据’三个限定。"),
        ],
        "figure-2-tipping-ensembles.webp", "Figure 2", 20, "comparison",
        "三个原型系统在相同 forcing、不同噪声下的突变/非突变轨迹、forcing 曲线与突变时刻分布。",
        "噪声使相同 forcing 下的轨迹产生宽分布突变时刻，为概率预测而非确定阈值判断提供了测试场景。",
        "Figure 2直接定义三组模拟 ensemble 与分类困难，是后续深度学习结果的证据入口。",
        [{"label": "Noisy moving saddle-node", "latex": r"dX_t=[(X_t+\lambda(t))^2-1]dt+\sqrt{2D_1}\,dW_t", "role": "generate mixed rate- and noise-induced tipping trajectories", "symbols": {"lambda": "time-varying forcing", "D1": "noise intensity", "W": "Wiener process"}, "evidence": "paper.pdf p. 11, prototype systems", "interpretation": "At epsilon=1.25 below the deterministic threshold 4/3, noise makes tipping probabilistic in this prototype."}],
        ["paper.pdf pp. 2–6: R-tipping ensembles, CSD comparison and CNN prediction", "paper.pdf pp. 7–10: LRP fingerprints, forcing/noise sensitivity and limitations", "paper.pdf p. 20, Figure 2: three prototype ensemble protocols", "source PDF SHA-256 d34199bac5003e5ca7785067984220079c51f697623243f35baa7d621f2ffd47", "Evidence status: full-text verified simulation manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1038-s42256-026-01233-9", "version of record", "https://www.nature.com/articles/s42256-026-01233-9.pdf",
        "Deep neural operator for free boundary problems", "用于自由边界问题的深度神经算子",
        "ai_empirical", "4e5d867d540801bc", "AI for Science",
        {"doi": "10.1038/s42256-026-01233-9", "version": "version of record", "title": "Deep neural operator for free boundary problems", "authors": ["Zongjia Long", "Qi Zhou", "Aiqing Zhu", "Dong Dai", "Yiqun Liu"], "journal": "Nature Machine Intelligence", "volume": "8", "pages": "806–817", "published": "2026-05-21", "abstract": "FBNO learns a conjugate flow on a fixed reference domain together with a diffeomorphic map to evolving physical domains, enabling operator learning for free-boundary PDE families.", "comment": "Open-access version of record; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Zongjia Long、Qi Zhou、Aiqing Zhu、Dong Dai、Yiqun Liu；Nature Machine Intelligence 8, 806–817 (2026)，DOI:10.1038/s42256-026-01233-9。核验15页开放期刊版、Methods、Supplementary/Source Data 声明与 Crossref；未发现关联更正或撤稿。"),
            sec("研究问题", "经典 neural operator 通常在预先给定 domain 上学习 function-to-function map，但 free boundary problem 的输出场和定义域同时未知且互相耦合。论文问：能否把随时间变化的未知几何映射到固定 reference domain，在同一算子中预测内部物理场与移动边界，并保留 operator universal approximation 的理论基础？"),
            sec("背景", "FBNO 将原 FBP 看成 infinite-dimensional dynamical system：未知-domain flow map F_t 与固定-domain conjugate flow G_t 通过 homeomorphism H 相连。Figure 1 展示 H^{-1} 把初态映入 reference domain、G_t 演化，再由 H 返回物理域；网络同时学习场值和 diffeomorphism χ。", "严格正的空间 Jacobian determinant 用作局部可逆约束，以避免网格折叠。该构造假设演化域与 reference domain 在所考虑时间内可微同胚；发生拓扑变化或 singularity 时不一定适用。"),
            sec("模型与方法", "框架支持 physics-informed 与 supervised data-driven 两种训练。前者联合 initial、fixed/free-boundary、PDE residual 与 diffeomorphism losses；后者直接用 u(x,t) 数据，无需显式构造每个参考点到物理点的配对。实现以 MIONet 类多输入算子作为基础网络。", "数值验证包括一维 Stefan melting、二维 thermal–structural coupling 和 tumour-growth free boundary。Stefan 例用有限元生成训练/测试数据；肿瘤例共运行3,660个高保真模拟，并通过经验证的 interpolation 增广，划分3,000训练、600测试、60验证。"),
            sec("核心结果与证据", "Figure 2 中 Stefan problem 的场 u 平均 relative L2 error 为0.0125，自由边界 Γ_f 为0.0072；300个测试样本的误差分布和 Riemannian metric 分析支持对不同 forcing/domain 的稳定预测。误差是对作者有限元 reference 的 surrogate 精度，不是解析真解误差。", "thermal–structural 例同时预测 density、temperature、velocity 和 geometry，Figure 3 报告各量约0.1%到2.8%的平均 relative L2 error；加入 physics-informed constraints 在作者设置下改善多物理量误差。", "肿瘤例在训练分布覆盖的参数和初始几何上预测 size/nutrient fields；推理相对传统数值方法报告最高约10^4 speed-up，但训练、数据生成和硬件成本未计入单次推理比较。临床个体化治疗是潜在应用，不是临床验证。"),
            sec("有效性与局限", "近似定理保证在连续性、紧性和 diffeomorphic conjugacy 等假设下存在逼近，不保证有限网络、有限优化能找到全局最优。shock、pinch-off、merger 等 singularity/topology change 会破坏当前映射；多相问题还需显式耦合多个子域。", "训练数据稀缺、interpolation bias 和 local minima 限制 OOD generalization。inference speed-up 不能替代 end-to-end cost；肿瘤模型是合成 PDE 数据，未输入真实患者 longitudinal scans，也未验证 treatment outcome。"),
            sec("复现与资源", "期刊：https://doi.org/10.1038/s42256-026-01233-9；开放 Supplementary 与 Source Data 位于期刊页面。PDF SHA-256：6d14e39b9a6e2a8a743028a2ca28105fc664fe3fc443b15871855f8e603ec2e2。", "复现需固定 FBP equations、reference-domain parameterization、MIONet width/depth、sensor sampling、loss weights、Jacobian lower bound、FEM mesh/time step、data split、interpolation 和硬件计时口径。Evidence status: full-text verified version of record; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–4 Figure 1 与 Eqs. (3)–(7)，确认 conjugacy/χ 的角色；p.5 Figure 2看 Stefan 精度，pp.6–8 Figures 3–4看多物理和肿瘤结果。最后读 pp.8–10 Discussion/Methods，重点检查 singularity、diffeomorphism、训练成本与临床外推边界。"),
        ],
        "figure-2-stefan-validation.webp", "Figure 2", 5, "comparison",
        "Stefan 问题中参考场、FBNO 预测、绝对误差、自由边界误差和测试集统计。",
        "FBNO在所测 Stefan forcing family 上同时重建温度场与移动边界，平均相对误差约为百分之一量级。",
        "Figure 2把定性场图、边界误差和300个测试样本统计放在一起，是最完整的基准证据。",
        [{"label": "Conjugate operator", "latex": r"\mathcal F_t=\mathcal H\circ\mathcal G_t\circ\mathcal H^{-1}", "role": "move free-boundary evolution to a fixed reference domain", "symbols": {"F": "original free-boundary flow", "G": "conjugate flow on the reference domain", "H": "homeomorphism between domains"}, "evidence": "paper.pdf pp. 3–4, methodology", "interpretation": "The factorization is useful only while a suitable invertible smooth correspondence exists."}, {"label": "Diffeomorphic constraint", "latex": r"\det(\partial\chi/\partial\xi)>\delta>0", "role": "prevent local folding of the learned domain map", "symbols": {"chi": "reference-to-physical coordinate map", "xi": "reference coordinate", "delta": "positive safety margin"}, "evidence": "paper.pdf p. 9, Eq. (13)", "interpretation": "Positive local Jacobian supports invertibility but does not cover topology-changing boundaries."}],
        ["paper.pdf pp. 2–4, Figure 1 and Eqs. (3)–(7): conjugate-system construction", "paper.pdf p. 5, Figure 2: Stefan validation", "paper.pdf pp. 6–8, Figures 3–4: thermal-structural and tumour tests", "paper.pdf pp. 8–10: limitations and training methods", "source PDF SHA-256 6d14e39b9a6e2a8a743028a2ca28105fc664fe3fc443b15871855f8e603ec2e2", "Evidence status: full-text verified version of record; no independent reproduction performed."],
    ),
    card(
        "doi-10.1038-s44387-025-00057-z", "version of record", "https://www.nature.com/articles/s44387-025-00057-z.pdf",
        "A self-correcting multi-agent LLM framework for language-based physics simulation and explanation", "面向自然语言物理仿真与解释的自纠错多智能体大模型框架",
        "ai_empirical", "513dc1157f56f368", "LLM Agents",
        {"doi": "10.1038/s44387-025-00057-z", "version": "version of record", "title": "A self-correcting multi-agent LLM framework for language-based physics simulation and explanation", "authors": ["Donggeun Park", "Hyeonbin Moon", "Seunghwa Ryu"], "journal": "npj Artificial Intelligence", "volume": "2", "article": "10", "published": "2026-01-20", "abstract": "MCP-SIM coordinates six GPT-4o-based agents, persistent memory and a FEniCS execution loop to turn underspecified prompts into simulations and multilingual explanations on a curated twelve-task benchmark.", "comment": "Open-access version of record; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Donggeun Park、Hyeonbin Moon、Seunghwa Ryu；npj Artificial Intelligence 2, 10 (2026)，DOI:10.1038/s44387-025-00057-z。核验10页开放期刊版、Supplementary、Zenodo/GitHub 声明与 Crossref；未发现关联更正或撤稿。"),
            sec("研究问题", "自然语言提出有限元任务时常缺 geometry、材料、PDE 或 boundary conditions；一次性 LLM 生成的代码又可能语法错误、solver divergence 或物理不一致。论文问：把 clarification、code generation、execution、diagnosis、prompt revision 和 explanation 分给专门 agents，并共享历史记忆，能否减少人工介入并提高小型跨域基准的成功率？"),
            sec("背景", "MCP-SIM 由 Memory-Centric Orchestrator 协调六个 agents：Input Clarifier、Code Builder、Simulation Executor、Error Diagnosis、Input Rewriter、Mechanical Insight。Figure 1 的 Plan–Act–Reflect–Revise loop 会保存规范化问题、代码版本、错误日志和 error→fix 映射。", "仿真后端是 FEniCS，agents 使用 GPT-4o 与人工设计的 physics-aware prompt templates。所谓 persistent memory 是该流程内的状态记录，不等于模型权重更新，也不自动证明生成解释科学正确。"),
            sec("模型与方法", "12个任务从完整的 elasticity/heat problems 递增到缺设定的 fluid、thermomechanical、piezoelectric 与 phase-field fracture。成功需代码可执行、归一化 governing-equation residual 低于10^-4且 field distribution 被作者判为 physically plausible。", "三条 baseline 是 one-shot GPT、GPT+自动澄清、GPT+澄清+human diagnosis；它们分别保留不同程度人工操作。测试数量只有12，任务源于教程/作者设计且未报告多次随机重复、置信区间或 blind external graders。"),
            sec("核心结果与证据", "Figure 2 报告 B1、B2、B3 分别完成6/12、8/12、9/12，而 MCP-SIM 完成12/12；正文另一处写 B3 为10/12，图文存在需保留的内部不一致。不能把12/12写成一般物理仿真100%可靠。", "多数 MCP-SIM 任务在不超过5个修订周期完成，但最难的 phase-field crack growth 需要10轮。Figure 3展示12个最终 field plots；这些图证明 pipeline 产生可运行输出，未与解析解或独立高精度 solver 对每项做统一误差基准。", "作者以 fracture 例说明自动补全材料/边界、修复 variational form 和 mesh resolution。相对于人为设限的 baselines，完整 loop 的优势同时包含更多自动化步骤、记忆和诊断，因此不能从消融唯一归因于‘多智能体’或某一 agent。"),
            sec("有效性与局限", "基准规模小且 curated，任务/判据/agent prompts 均由作者掌控；缺少未见专业领域、对抗提示、错误物理先验、unsafe boundary conditions 和真实工程认证。physically plausible 仍需 human/external verification，residual 小只说明离散方程求解收敛，不保证方程选择正确。", "GPT-4o 服务、prompt stochasticity、成本/延迟与依赖版本影响复现。系统会在含糊输入时自行补假设，这提高可执行性却可能偏离用户意图；高风险仿真不能取消专家审批。图文 B3 计数不一致也说明需直接核查 artifacts。"),
            sec("复现与资源", "期刊：https://doi.org/10.1038/s44387-025-00057-z；代码/数据：https://doi.org/10.5281/zenodo.15645333 与 https://github.com/KAIST-M4/MCP-SIM。PDF SHA-256：3055a70df955d5d540ef27ccfaaac88dc5a0a375764512dcee3880179afd6c3a。", "复现需固定 GPT-4o snapshot、temperature、agent templates、memory schema、FEniCS/container、12 prompts、success judge、retry budget 与人工 baseline protocol。Evidence status: full-text verified version of record; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1建立 agent/记忆边界，再看 pp.3–4 Figure 2和 Table 1逐项核对任务、成功率与迭代数；pp.4–6看 fracture 与解释输出。最后读 Discussion/Methods，并特别记录 B3 图文计数差异和12-task外推限制。"),
        ],
        "figure-2-mcp-sim-benchmark.webp", "Figure 2", 4, "comparison",
        "12个物理仿真任务、四种 agent setup 的成功计数，以及各任务达到成功所需修订轮数。",
        "完整 MCP-SIM loop 在作者的12任务基准上全部达到既定 residual 与 plausibility 判据。",
        "Figure 2是全文唯一把任务难度、成功计数、迭代数和自动化范围并列的核心比较。",
        [{"label": "Numerical convergence criterion", "latex": r"r_k/r_0<10^{-4}", "role": "declare a generated finite-element solve numerically converged", "symbols": {"r_k": "total governing-equation imbalance at iteration k", "r_0": "initial imbalance"}, "evidence": "paper.pdf p. 3, benchmark metrics", "interpretation": "A small normalized residual does not validate whether the inferred PDE and boundary conditions match the user's intended physics."}],
        ["paper.pdf pp. 1–3, Figure 1: agent roles, memory and correction loop", "paper.pdf pp. 3–5, Figure 2 and Table 1: twelve-task benchmark", "paper.pdf pp. 5–7: fracture case, explanations and limitations", "source PDF SHA-256 3055a70df955d5d540ef27ccfaaac88dc5a0a375764512dcee3880179afd6c3a", "Evidence status: full-text verified version of record; no independent reproduction performed."],
    ),
    card(
        "doi-10.1073-pnas.2206994120", "arXiv manuscript", "https://arxiv.org/pdf/2101.06568",
        "Learning hydrodynamic equations for active matter from particle simulations and experiments", "从粒子模拟与实验学习主动物质流体力学方程",
        "theory_numerics", "ca267e769b304795", "Active Matter",
        {"doi": "10.1073/pnas.2206994120", "arxiv_id": "2101.06568", "version": "arXiv full text", "title": "Learning hydrodynamic equations for active matter from particle simulations and experiments", "authors": ["Rohit Supekar", "Boya Song", "Alasdair Hastewell", "Gary P. T. Choi", "Alexander Mietke", "Jörn Dunkel"], "journal": "Proceedings of the National Academy of Sciences", "volume": "120", "article": "e2206994120", "published": "2023-02-10", "abstract": "Kernel coarse-graining, spectral differentiation and symmetry-constrained sparse regression recover interpretable continuum PDEs from chiral-particle simulations and Quincke-roller videos.", "comment": "arXiv full text cross-checked with open-access version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Rohit Supekar、Boya Song、Alasdair Hastewell、Gary P. T. Choi、Alexander Mietke、Jörn Dunkel；PNAS 120, e2206994120 (2023)，DOI:10.1073/pnas.2206994120；全文取 arXiv:2101.06568，共34页含 Supplementary。核验 PNAS/PMC 状态，未发现关联更正或撤稿。"),
            sec("研究问题", "实验和 particle simulations 能追踪大量 active units，但 coarse-grained PDE 的项与系数通常依赖难以闭合的 kinetic hierarchy。论文问：能否从二维粒子轨迹直接构造平滑 hydrodynamic fields，用 conservation laws 与 broken symmetries 限定候选库，再以 sparse regression 同时发现方程结构和可解释系数？"),
            sec("背景", "Figure 1给出四步链：粒子位置/方向 → kernel coarse-graining 的 density/polarization → Fourier/Chebyshev 谱表示与微分 → physics-informed library 上稀疏回归并回代模拟。空间 kernel scale 必须大于 mean free path/interaction range、又小于 collective structures。", "谱压缩滤去快速噪声并提供稳定 derivatives；时间谱指数衰减被用作 deterministic PDE 可行性的线索。它不是从数据证明系统严格确定性，未解析变量或 colored noise 仍可能被吸收到有效项中。"),
            sec("模型与方法", "第一测试是12,000个具有 speed/rotation heterogeneity 的 chiral active Brownian particles，形成长寿命 vortices。作者构造 density 与 polarization 的旋转/手性允许项，用 sequentially thresholded least squares（STLSQ）和 stability selection 在数据子样本上筛选。", "第二部分处理约2,200个 Quincke rollers 的视频，非周期边界用适配基函数；学习 density/velocity PDE 后在 channel 和 square geometry 中回代。Supplementary 还处理约1,024条 sunbleak fish 轨迹，属于可迁移示例而非独立大样本验证。"),
            sec("核心结果与证据", "对模拟粒子，最稀疏 density 方程为 mass conservation：∂tρ=a1∇·p，a1=-0.99，接近 nondimensional microscopic expectation -1。Figure 2显示 spectral cutoff、derivative consistency、candidate library 和 coefficient path；线性系数与 analytic coarse-graining 较一致。", "polarization 方程需更丰富的线性、非线性和 gradient terms 才能回代形成正确 vortex scale/lifetime；部分高阶 learned coefficients 与常用 closure 明显不同，说明简单 analytic truncation 在 heterogeneous particles 下失效。", "Quincke 视频学习出的 continuum model 在训练几何外的封闭方形域仍产生实验中观察到的 inward density shocks/vortices，并预测典型速度和尺度。它是同一实验数据族的外推检验；模型选择、smoothing、boundary 和小数值 diffusivity 都影响结果。"),
            sec("有效性与局限", "稀疏识别以真实 PDE 位于候选 library、fields 可观测且尺度分离为前提；遗漏 hidden fields、过强 filtering 或高度共线 terms 会给出错误但可拟合模型。stability selection 降低抽样不稳，不能消除结构误设。", "coarse-graining width、spectral cutoff、threshold path 与边界基函数是实质超参数。实验验证集中于二维 active systems；三维扩展在形式上直接但数据、库规模和计算量更困难。原文代码/数据声明为向通讯作者合理请求，不是完全一键复现包。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2101.06568；期刊：https://doi.org/10.1073/pnas.2206994120；补充代码仓库：https://github.com/rohitsupekar/learning-active-matter-equations。PDF SHA-256：4b2c9aff0cc6f91ea5b8279c4bc1626398ddd7524960eca9386221d937f0f669。", "复现需固定 tracking、kernel σ、basis/cutoff、derivative normalization、symmetry library、STLSQ thresholds、subsampling/stability cutoff、boundary conditions、PDE solver 与 uncertainty bootstrap。Evidence status: full-text verified simulation/experiment manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1掌握数据到 PDE 的链条；pp.2–6 Figures 2–3核对 simulated-particle 方程发现与回代。pp.7–10 Figures 4–5是 Quincke 实验验证；最后读 Supplementary A–E，检查 filtering、stability selection、closure 对比和数值 diffusivity。"),
        ],
        "figure-1-learning-workflow.webp", "Figure 1", 2, "schematic",
        "从粒子轨迹、粗粒化场、谱表示与微分到稀疏 PDE 学习和 continuum simulation 的四步流程。",
        "物理守恒与对称性先约束候选项，谱处理再使微观轨迹能够支持可解释 PDE 回归。",
        "Figure 1完整展示跨尺度推断链和每一步输入输出，最适合作为全文证据地图。",
        [{"label": "Kernel coarse-graining", "latex": r"\rho(t,x)=\sum_i K[x-x_i(t)],\qquad p(t,x)=\sum_iK[x-x_i(t)]p_i(t)", "role": "convert discrete trajectories into hydrodynamic density fields", "symbols": {"K": "normalized spatial kernel", "rho": "number density", "p": "polarization density"}, "evidence": "paper.pdf p. 3, Eqs. (2a)–(2b)", "interpretation": "The kernel scale defines which microscopic fluctuations are discarded before equation learning."}, {"label": "Sparse hydrodynamic library", "latex": r"\partial_t\rho=\sum_l a_l C_l(\rho,p),\qquad\partial_t p=\sum_l b_l\mathbf C_l(\rho,p)", "role": "select symmetry-allowed continuum terms from data", "symbols": {"C_l": "scalar candidate terms", "bold C_l": "vector candidate terms", "a_l,b_l": "phenomenological coefficients"}, "evidence": "paper.pdf pp. 4–6, sparse-regression formulation", "interpretation": "Sparsity is conditional on the chosen library, filtering and stability threshold."}],
        ["paper.pdf pp. 1–3, Figure 1: coarse-graining and spectral workflow", "paper.pdf pp. 4–6, Figures 2–3: particle-simulation equation learning", "paper.pdf pp. 7–10, Figures 4–5: Quincke-roller inference and validation", "paper.pdf Supplementary A–E: filtering, stability selection and coefficient uncertainty", "source PDF SHA-256 4b2c9aff0cc6f91ea5b8279c4bc1626398ddd7524960eca9386221d937f0f669", "Evidence status: full-text verified simulation/experiment manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1088-0256-307x-40-12-126401", "arXiv manuscript", "https://arxiv.org/pdf/2304.08895",
        "Tunable Memory and Activity of Quincke Particles in Micellar Fluid", "胶束流体中可调记忆与活性的 Quincke 粒子",
        "experiment", "c8eb9e3348da90aa", "Active Matter",
        {"doi": "10.1088/0256-307X/40/12/126401", "arxiv_id": "2304.08895", "version": "arXiv full text", "title": "Tunable Memory and Activity of Quincke Particles in Micellar Fluid", "authors": ["Yang Yang", "Meng Fei Zhang", "Lailai Zhu", "Tian Hui Zhang"], "journal": "Chinese Physics Letters", "volume": "40", "article": "126401", "published": "2023-11-01", "abstract": "Square-wave electric driving separates velocity and polarization relaxation in Quincke rollers, producing frequency-tunable directional memory, reduced activity and enhanced memory in dense clusters.", "comment": "arXiv full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Yang Yang、Meng Fei Zhang、Lailai Zhu、Tian Hui Zhang；Chinese Physics Letters 40, 126401 (2023)，DOI:10.1088/0256-307X/40/12/126401；全文取 arXiv:2304.08895，共7页含补充。核验 Crossref/期刊状态，未发现关联更正或撤稿。"),
            sec("研究问题", "Quincke rollers 常被视为 overdamped active colloids，但在高浓度 AOT/hexadecane 胶束液中，viscoelastic stress 与 charge polarization 都有有限 relaxation time。论文问：square-wave electric field（SWE）的频率能否分别调节速度记忆、推进方向记忆与平均活性，以及粒子聚集后局域电相互作用是否进一步改变记忆？"),
            sec("背景", "10 μm polystyrene particles 位于 ITO cell 底部，峰值场 Ep>Ec 激活 Quincke rotation，谷值 Eg<Ec 周期性停止/减弱推进。Figure 1测得 acceleration time 约13 ms、deceleration time 约4 ms；Re≈9×10^-4，故‘inertia-like’来自 micellar viscoelastic memory，不是颗粒真实质量惯性。", "推进由 induced dipole 与 field torque 决定，polarization relaxation 与 velocity relaxation 可分离。作者用相邻周期速度夹角的 persistence index <cosΔθ> 区分无记忆、速度记忆与速度+推进记忆。"),
            sec("模型与方法", "轨迹以1000 fps、约1 μm/pixel记录，位置精度约0.1 pixel；主要扫描 Ep=2.1Ec、Eg=0 与 SWE frequency。每周期 Ep/Eg 各占一半，统计 speed、MSD 和 persistence；再改变 Eg、field amplitude 与 cluster density。", "阈值 <cosΔθ>=0.85 是作者定义的 persistent directional motion 判据。高频下每周期帧数有限，局部 rheology、humidity 对 AOT conductivity 以及粒子密度会影响 relaxation estimates。"),
            sec("核心结果与证据", "Figure 2 显示低频 persistence 小；约125 Hz 以上速度无法在 off-half-cycle 完全松弛，出现 velocity memory；实验达到 persistence threshold 需约250 Hz，说明 polarization/propulsion 还需约2 ms relaxation，300 Hz以上 plateau 约0.90。", "提高频率缩短 acceleration 时间，使最大/平均速度下降；因此可以在保留方向记忆的同时降低 activity。正的 Eg 延缓 charge relaxation，把 persistent threshold 从 Eg=0 的约250 Hz 降至 Eg=0.5Ec 的125 Hz和 Eg=0.8Ec 的72 Hz，而 deceleration time 基本不变。", "160 Hz 时形成液态动态 clusters；cluster 内 dipolar repulsion 提供额外推进并延缓 polarization relaxation，persistent threshold 约185 Hz，低于孤立粒子。该解释由轨迹、速度与 persistence 支持，但没有独立测量完整 micellar stress 或局域 electric field。"),
            sec("有效性与局限", "机制分解基于 relaxation times、frequency response 与已知 Quincke physics 的一致性，不是对 memory kernel、viscoelastic modulus 和 charge field 的联合参数反演。AOT 吸湿性会改变 conductivity；threshold 与时间常数可能随样品制备、field waveform 和 humidity 漂移。", "单一粒径、cell、液体配方和二维近壁几何限制普适性。cluster memory 同时伴随 density、EHD attraction 和 dipolar forces，不能仅从 correlation 确认单一因果通道；论文也未建立完整 collective phase diagram 或 thermodynamic-limit scaling。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2304.08895；期刊：https://doi.org/10.1088/0256-307X/40/12/126401。PDF SHA-256：10b60b88e2bd0b55b445e4fc970726d09a756b05f3a2ab6479909810fc32c04d。", "复现需固定 AOT/water content、viscosity/conductivity、particle/cell geometry、Ec calibration、Ep/Eg、duty cycle、camera rate、tracking filter、cycle averaging、persistence threshold 和 cluster definition。Evidence status: full-text verified experimental manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1确认装置、13/4 ms relaxation 与 inertia-like 的含义；p.3 Figure 2是三段记忆机制，p.4 Figure 3看 activity/Eg 调控，pp.4–5 Figure 4看 cluster memory。最后将直接轨迹证据与 viscoelastic/electric 机制解释分开。"),
        ],
        "figure-2-memory-regimes.webp", "Figure 2", 3, "phase_diagram",
        "persistence index 随 SWE 频率的跃升，以及无记忆、速度记忆、速度与推进共同记忆三段示意。",
        "速度约在125 Hz开始保留，而完整推进方向记忆约在250 Hz建立，揭示两个不同 relaxation channels。",
        "Figure 2把直接测量的 persistence curve 与作者提出的三阶段机制一一对应。",
        [{"label": "Cycle-to-cycle persistence", "latex": r"P=\langle\cos(\Delta\theta)\rangle", "role": "quantify directional memory between consecutive driving cycles", "symbols": {"Delta theta": "angle between velocities in adjacent cycles", "P": "persistence index"}, "evidence": "paper.pdf p. 3, Figure 2 and surrounding text", "interpretation": "The paper defines P=0.85 as a practical threshold; it is not a universal phase-transition criterion."}, {"label": "Maxwell–Wagner time", "latex": r"\tau_{MW}=(\epsilon_p+2\epsilon_l)/(\sigma_p+2\sigma_l)", "role": "estimate polarization relaxation", "symbols": {"epsilon": "permittivity", "sigma": "conductivity", "p,l": "particle and liquid"}, "evidence": "paper.pdf p. 3, charge-relaxation discussion", "interpretation": "The inferred roughly 2 ms scale is sample-sensitive because AOT conductivity depends strongly on water content."}],
        ["paper.pdf pp. 1–2, Figure 1: apparatus and velocity relaxation", "paper.pdf p. 3, Figure 2: frequency-dependent persistence regimes", "paper.pdf pp. 4–5, Figures 3–4: activity control and cluster memory", "source PDF SHA-256 10b60b88e2bd0b55b445e4fc970726d09a756b05f3a2ab6479909810fc32c04d", "Evidence status: full-text verified experimental manuscript; no independent reproduction performed."],
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
