#!/usr/bin/env python3
"""Install theory cards for full Collection backfill batch 003."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_id: str, topic: str) -> dict[str, object]:
    return {
        "program": "Collection",
        "catalog": "Paper Collection",
        "catalog_record_id": record_id,
        "catalog_record_ids": [record_id],
        "catalog_topic": topic,
        "collection_date": "2026-08-23",
        "sampled_at": "2026-08-26",
        "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection",
        "candidate_count": 452,
    }


CARDS = [
    {
        "arxiv_id": "1612.03122",
        "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/1612.03122",
        "title_en": "Non-Perturbative Renormalization Group for the Diffusive Epidemic Process",
        "title_zh": "扩散流行病过程的非微扰重整化群",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("1697b1ea5a2604c9", "Renormalization Group"),
        "verified_metadata": {
            "arxiv_id": "1612.03122",
            "version": "v2",
            "title": "Non-Perturbative Renormalization Group for the Diffusive Epidemic Process",
            "authors": ["Malo Tarpin", "Federico Benitez", "Léonie Canet", "Nicolás Wschebor"],
            "categories": ["cond-mat.stat-mech"],
            "primary_category": "cond-mat.stat-mech",
            "published": "2016-12-09T18:43:01Z",
            "abstract": "The paper revisits the relation between the diffusive epidemic process and directed percolation with a conserved quantity using symmetries and a derivative-expansion non-perturbative RG calculation.",
        },
        "sections": [
            sec("作者信息", "作者：Malo Tarpin、Federico Benitez、Léonie Canet、Nicolás Wschebor；论文为 arXiv:1612.03122v2，主分类 cond-mat.stat-mech。", "本卡核对 13 页全文。工作将 Doi–Peliti 场论、Ward 恒等式与非微扰重整化群的 LPA′ 截断结合起来。"),
            sec("研究问题", "扩散流行病过程（DEP）含健康粒子与感染粒子，总粒子数守恒，并在活跃流行态和无感染者的吸收态之间转变。微扰场论常把它归入带守恒量的 directed percolation（DP-C），但 DP-C 对临界指数的精确约束与一、二维晶格模拟并不一致。", r"论文问的是：这些 DP-C 对称性是否真能从完整 DEP 微观作用量在红外涌现？若能，固定点应强制 \(\nu=2/d\) 等关系；若不能，低维 DEP 可能属于对称性更少的独立普适类。"),
            sec("背景", r"微观反应为 \(A+B\xrightarrow{k}B+B\) 与 \(B\xrightarrow{1/\tau}A\)，两种粒子以不同扩散常数运动。总密度守恒使问题不同于普通 DP。", "DP-C 是在上临界维数附近丢弃 DEP 中微扰无关项得到的截断场论。它拥有纯位移、对偶和时间规范位移等对称性；这些对称性可保护某些传播子并锁定临界指数。完整 DEP 保留更多顶角，其中一些会破坏 DP-C 的偶然对称性。"),
            sec("模型与方法", r"作者为 DEP 与 DP-C 分别推导场变量变换及对应 Ward 恒等式，再引入尺度依赖有效作用量 \(\Gamma_k\) 与 Litim regulator，使 \(k\) 从微观尺度流向零。", r"LPA′ ansatz 保留全局有效势 \(U_k(\Phi+\bar\Phi,\Psi,\bar\Psi)\)、场归一化 \(Z_k\) 与动力学尺度 \(\lambda_k\)，并把势在运行极小值 \(\chi_k\) 周围按场多项式展开到四至六阶。", "固定点通过无量纲 beta functions 数值求解；改变空间维数与多项式截断阶数，检查固定点是否存在、相关方向数是否正确以及反常维数是否收敛。"),
            sec("核心结果与证据", r"DP-C 的 Ward 恒等式给出 \(g\,\partial_\sigma U_k=\partial_\Phi U_k\)。在解析势展开下，只有极小值 \(\chi_k\) 承担调谐方向，从而得到精确关系 \(\nu=2/d\)。这解释了为什么该指数是 DP-C 固定点的结构性预言。", r"NPRG 在 \(d_c=4\) 附近恢复一圈 \(\epsilon=4-d\) 展开与相应 DP-C 固定点；但随 \(d\) 降低，四至六阶截断中的物理解在 \(d\simeq3\) 附近消失或转成不物理解。", "因此一、二维模拟与 DP-C 指数不一致有两种尚未区分的解释：有限阶 LPA′ 丢失了真实固定点，或者低维 DEP 确由一个不满足 DP-C 精确恒等式的新固定点控制。论文明确没有把固定点消失直接宣布为相变机制的最终结论。"),
            sec("有效性与局限", "固定点消失对截断敏感：反常维数随多项式阶数仍有明显漂移，LPA′ 又不能重整化某些传播子，因此不足以判定低维固定点是否真的不存在。", "DEP 与 DP-C 的对称性比较是解析且稳健的，但从微观 DEP 流到 DP-C 子空间的动力学仍未完整求解；更宽 theory space 和更高阶导数展开是必要复核。", "论文没有重新模拟晶格 DEP，也没有直接拟合临界指数；它解释既有数值矛盾的可能来源，而非用新数据裁决。", r"精确式 \(\nu=2/d\) 只在具有相应 DP-C Ward 恒等式、且该固定点确实控制红外时成立，不能无条件套到完整 DEP。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1612.03122；PDF：https://arxiv.org/pdf/1612.03122。", "全文 PDF 共 13 页，SHA-256：32de7e2d4ad61af5ffc19aa582fd8aa45c4aeb166e4971f31aeba275f22f72df。", "复核应先符号推导 Appendix A 的 Ward 恒等式，再从 Appendix B 的频率留数与 beta functions 重建四、五、六阶多项式流；扫描维数时保存所有固定点分支与稳定矩阵本征值，避免只追踪单一 Newton 根。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 1–5 的 DEP/DP-C 场变量与对称性，特别区分微观 DEP 对称性和 DP-C 截断后的额外对称性。", r"再读 pp. 6–8 的 LPA′ 流和维数扫描；把“\(d\simeq3\) 以下未找到固定点”理解为当前截断内的结果。", r"最后用 Appendix A 检查 \(\nu=2/d\) 的逻辑链，并用 Appendix B 确认哪些传播子在当前 ansatz 中被允许重整化。"),
        ],
        "cover": {
            "mode": "title_abstract",
            "abstract_text": "扩散流行病过程通常被归入带守恒量的 directed percolation，但该场论的 Ward 恒等式会锁定临界指数，与低维晶格模拟存在张力。作者用非微扰 RG 在上临界维数附近恢复 DP-C 固定点，却发现它在 LPA′ 多项式截断中于约三维以下消失。结果把低维矛盾定位为两种可能：截断失败，或完整 DEP 流向对称性更少的新固定点。",
            "selection_rationale": "论文的证据核心是对称性、Ward 恒等式与固定点分支；原文图主要是截断阶数下的指数曲线，题目与物理摘要更能避免把数值截断图误当作最终相图。",
        },
        "figure_refs": [],
        "equation_refs": [
            {"label": "Diffusive epidemic reactions", "latex": r"A+B\xrightarrow{k}B+B,\qquad B\xrightarrow{1/\tau}A", "role": "define infection and spontaneous recovery while conserving total particle number", "symbols": {"A": "healthy particles", "B": "infected particles", "k": "infection rate", "tau": "recovery time"}, "evidence": "paper.pdf p. 1, Eq. (1)", "interpretation": "The absorbing state contains no B particles, while conservation of A+B couples the order parameter to a diffusive mode."},
            {"label": "DP-C exponent identity", "latex": r"\nu=\frac{2}{d}", "role": "express the Ward-identity constraint at a DP-C fixed point", "symbols": {"nu": "spatial correlation-length exponent", "d": "space dimension"}, "evidence": "paper.pdf Appendix A, Eq. (A10)", "interpretation": "This is exact only if the DP-C shift/duality structure survives and its fixed point controls the transition."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–5: DEP/DP-C actions, simulations tension and symmetry inventory", "paper.pdf pp. 6–8: NPRG ansatz, truncation-order comparison and fixed-point loss near d=3", "paper.pdf Appendix A–B: Ward identities, exact exponent relation and explicit LPA′ flow", "source PDF SHA-256 32de7e2d4ad61af5ffc19aa582fd8aa45c4aeb166e4971f31aeba275f22f72df", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "1804.06561",
        "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/1804.06561",
        "title_en": "A Mean Field View of the Landscape of Two-Layers Neural Networks",
        "title_zh": "双层神经网络损失景观的平均场视角",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("bddffd6b3fd137d7", "Training Dynamics"),
        "verified_metadata": {"arxiv_id": "1804.06561", "version": "v2", "title": "A Mean Field View of the Landscape of Two-Layers Neural Networks", "authors": ["Song Mei", "Andrea Montanari", "Phan-Minh Nguyen"], "categories": ["stat.ML", "cond-mat.stat-mech", "cs.LG", "math.ST"], "primary_category": "stat.ML", "published": "2018-04-18T05:31:45Z", "abstract": "In a large-width and small-step limit, SGD for two-layer networks converges to a nonlinear distributional PDE that is a Wasserstein gradient flow of the population risk."},
        "sections": [
            sec("作者信息", "作者：Song Mei、Andrea Montanari、Phan-Minh Nguyen；论文为 arXiv:1804.06561v2，主分类 stat.ML，并交叉 cond-mat.stat-mech、cs.LG 与 math.ST。", "本卡核对含补充证明与数值实验的 104 页全文。"),
            sec("研究问题", "有限宽双层网络的 population risk 是高维非凸函数。作者不试图证明所有局部极小值都消失，而是问：当隐藏单元数很大、SGD 步长很小时，参数粒子的经验分布是否收敛到一个可分析的连续场动力学？", "若该平均场动力学趋近全局最优，是否足以解释 SGD 在有限但过参数化网络中的表现，而无需对每个有限宽驻点逐一分类？"),
            sec("背景", r"把第 \(i\) 个神经元参数 \(\theta_i\) 看成 \(D\) 维粒子，网络宽度 \(N\) 对应粒子数。其经验测度 \(\hat\rho^{(N)}=N^{-1}\sum_i\delta_{\theta_i}\) 在 \(N\to\infty\) 时成为连续密度。", "风险泛函在测度变量上由单体势 V 与二体核 U 构成，并因 U 半正定而在测度空间中凸；但局部质量守恒意味着动力学仍不能任意瞬移到所有测度方向。"),
            sec("模型与方法", r"作者取 SGD 步长 \(s_k=\varepsilon\xi(k\varepsilon)\)，证明在 \(N\to\infty\)、\(\varepsilon\to0\) 且适当正则条件下，经验测度弱收敛到 distributional dynamics。有限时间的非渐近误差要求典型地 \(\varepsilon\ll1/D\)、\(N\gg D\)。", r"极限 PDE 是风险 \(R(\rho)\) 在概率测度空间 \((\mathcal P(\mathbb R^D),W_2)\) 上的 Wasserstein 梯度流。对 noisy SGD，扩散项把能量改成带熵的自由能 \(F_{\beta,\lambda}\)。", "作者利用数据分布的旋转对称性把若干 Gaussian 分类例化为一维径向 PDE，并将 PDE 数值解与有限 N SGD 比较；随后给出全局或近全局收敛定理。"),
            sec("核心结果与证据", r"无噪声平均场方程为 \(\partial_t\rho_t=2\xi(t)\nabla_\theta\!\cdot[\rho_t\nabla_\theta\Psi(\theta;\rho_t)]\)，其中 \(\Psi=V+\int U(\theta,\theta')\rho(d\theta')\)。它把神经元相互作用压缩为自洽势。", r"noisy SGD 增加 \(2\xi(t)\beta^{-1}\Delta_\theta\rho_t\)，成为熵正则自由能的梯度流；论文证明在其假设下可泛化地趋向正则风险的近全局最小值，收敛时间不显含宽度 \(N\)。", "在中心各向同性/各向异性 Gaussian 与变量选择例子中，PDE 预测参数分布和风险轨迹，并能预告非单调激活下的失败。Figure 1 的径向密度和 Figure 3 的长平台都说明平均场不是静态 landscape 计数，而是完整输运动力学。"),
            sec("有效性与局限", "定理针对双层网络、population square loss 与受控正则条件；例子的数据分布和激活函数被刻意简化，以便解析降维，不能直接代表现代深层网络。", r"平均场近似需要 \(N\gg D\) 和小步长；有限宽、有限时间误差常数及维数依赖会决定实际可用性。论文没有证明有限 \(N\) 风险只有一个局部极小值，也没有证明所有初始化都进入同一个测度最优解。", "无噪声梯度流受局部质量守恒和初始支撑限制；测度泛函凸不自动保证任意 Wasserstein 流都避开所有驻点。", "经验图用于验证 PDE 与特定合成任务，不是自然数据上的泛化基准；noisy SGD 的全局陈述还包含正则化与有限温度假设。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1804.06561；PDF：https://arxiv.org/pdf/1804.06561。", "全文 PDF 共 104 页，SHA-256：9728a2be8430c21f7b6efd661d507f0ad4b630fecc3755ebc9c908e870b7d435。", "最小复现可实现各向同性 Gaussian 例：固定 d、N、步长与初始径向分布，同时求解一维 PDE 和有限粒子 SGD，比较随时间的 Wasserstein 距离、径向直方图与 population risk。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 3–6 的粒子—密度映射、风险泛函和 Wasserstein 梯度流；这是全文的物理图像。", "再读 pp. 6–14 的三个合成例子，特别比较 PDE 成功与非单调激活失败的条件。", r"最后读 Theorem 3 与 Discussion；把 \(N\to\infty\) 的传播混沌、PDE 自身的长时收敛和有限样本泛化分成三个不同命题。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "宽双层网络可视为大量参数粒子组成的相互作用气体。作者证明，在大宽度和小步长极限下，SGD 的经验参数分布收敛到一个自洽非线性 PDE；该 PDE 是 population risk 在 Wasserstein 测度空间中的梯度流。框架解释了为什么宽度继续增加后动力学可趋于稳定，并在简化 Gaussian 任务中证明近全局收敛，但它不等价于有限宽损失景观不存在坏局部极小值。", "selection_rationale": "论文图像均为径向分布或风险曲线，主要贡献是粒子极限与 Wasserstein 动力学；题目加物理摘要比单一数据图更忠实。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Distributional dynamics", "latex": r"\partial_t\rho_t=2\xi(t)\nabla_\theta\cdot\left[\rho_t\nabla_\theta\Psi(\theta;\rho_t)\right]", "role": "describe the mean-field transport of neuron parameters under SGD", "symbols": {"rho_t": "parameter probability measure", "xi(t)": "learning-rate schedule", "theta": "single-neuron parameter", "Psi": "self-consistent potential"}, "evidence": "paper.pdf p. 5, Eq. (7)", "interpretation": "SGD becomes a locally mass-conserving Wasserstein gradient flow rather than arbitrary descent in density space."},
            {"label": "Finite-temperature distributional dynamics", "latex": r"\partial_t\rho_t=2\xi(t)\nabla_\theta\cdot[\rho_t\nabla_\theta\Psi_\lambda]+2\xi(t)\beta^{-1}\Delta_\theta\rho_t", "role": "represent noisy SGD as free-energy gradient flow", "symbols": {"beta": "inverse noise temperature", "lambda": "L2 regularization", "Delta_theta": "parameter-space Laplacian"}, "evidence": "paper.pdf p. 6, Eq. (12)", "interpretation": "Injected noise adds entropy-producing diffusion and changes the optimized object from risk to regularized free energy."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: risk as a measure functional and DD/Wasserstein equations", "paper.pdf pp. 6–14: Gaussian and variable-selection examples, success and failure predictions", "paper.pdf pp. 15–16 and Theorem 3: scope, finite-width convergence and limitations", "paper.pdf Supplement Sections 6–11: proofs and empirical validation", "source PDF SHA-256 9728a2be8430c21f7b6efd661d507f0ad4b630fecc3755ebc9c908e870b7d435", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "1807.01083",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/1807.01083",
        "title_en": "A Mean-Field Optimal Control Formulation of Deep Learning",
        "title_zh": "深度学习的平均场最优控制表述",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("227f376aa23c3384", "Control & Reinforcement Learning"),
        "verified_metadata": {"arxiv_id": "1807.01083", "version": "v1", "title": "A Mean-Field Optimal Control Formulation of Deep Learning", "authors": ["Weinan E", "Jiequn Han", "Qianxiao Li"], "categories": ["math.OC", "cs.LG"], "primary_category": "math.OC", "published": "2018-07-03T11:05:13Z", "abstract": "Population-risk minimization for continuous-depth residual networks is formulated as mean-field optimal control and characterized by Wasserstein-space HJB and Pontryagin conditions."},
        "sections": [
            sec("作者信息", "作者：Weinan E、Jiequn Han、Qianxiao Li；论文为 arXiv:1807.01083v1，主分类 math.OC，交叉 cs.LG。", "本卡核对 45 页全文。工作建立连续深度残差网络的控制论基础，不报告新的神经网络基准实验。"),
            sec("研究问题", "把 ResNet 层看成时间步后，训练可写成最优控制。但 population risk 的同一控制参数同时作用于整个输入—标签分布，状态不再是单条轨迹。论文问：能否在概率测度空间中建立与经典控制同样完整的动态规划和最大值原理？", "进一步，population 控制问题的稳定解是否在有限训练样本形成的 empirical 控制问题中有邻近解，从而给出一种不直接按参数数目增长的泛化联系？"),
            sec("背景", r"离散 ResNet \(x_{t+1}=x_t+f(x_t,\theta_t)\) 在连续极限变成受控 ODE \(\dot x_t=f(x_t,\theta_t)\)。输入与标签 \((x_0,y_0)\sim\mu_0\) 是随机初值，而时间函数 \(\theta_t\) 是所有样本共享的控制。", "经典 HJB 给出全局 value function 与反馈控制，Pontryagin maximum principle（PMP）给出状态—伴随变量的局部必要条件。这里两者必须提升到输入—标签分布或等价的随机变量 Hilbert 空间。"),
            sec("模型与方法", r"population 问题最小化 \(J(\boldsymbol\theta)=\mathbb E_{\mu_0}[\Phi(x_T,y_0)+\int_0^T L(x_t,\theta_t)dt]\)，受 \(\dot x_t=f(x_t,\theta_t)\) 约束；empirical 问题把期望替换为 N 个样本平均。", r"作者在 \(\mathcal P_2(\mathbb R^{d+l})\) 上定义 value function，用 Lions derivative 与 lifting 到 \(L^2\) 随机变量空间，证明其为无限维 HJB 的唯一 viscosity solution。", "另一条路线对共享控制做 needle variation，推导 mean-field PMP；再用稳定逆映射与一致大数界证明稳定 population PMP 解附近存在 sampled PMP 解。"),
            sec("核心结果与证据", r"HJB Hamiltonian 为 \(H(\xi,P)=\inf_{\theta\in\Theta}\mathbb E[P\cdot\bar f(\xi,\theta)+\bar L(\xi,\theta)]\)。value function 的 lifting 满足 \(\partial_tV+H(\xi,DV)=0\)，从而同时刻画最优损失和反馈控制。", r"mean-field PMP 给出前向状态、后向伴随与平均 Hamiltonian 最大化：\(\mathbb E H(x_t^*,p_t^*,\theta_t^*)\ge\mathbb E H(x_t^*,p_t^*,\theta)\)。共享权重必须对整个数据分布平均最优，而非逐样本最优。", "在强凹 Hamiltonian 等充分条件下 PMP 解唯一；更一般地，只要 population PMP 解稳定并满足一致收敛假设，有限样本 PMP 以高概率存在邻近解，参数路径和目标值误差随经验平均收敛。"),
            sec("有效性与局限", "分析针对连续深度理想化；作者认为可延伸到离散层，但本文未给出离散化误差与有限深度网络的完整定理。", "HJB 的全局刻画在无限维测度空间中通常不可直接数值求解；PMP 只是必要条件，除非额外凹性或稳定性成立，解仍可能非唯一或非全局。", "主要假设包括有界/Lipschitz 动力学与损失、输入分布二阶矩或有界支撑，以及 sampled 算子的统一集中；现代非光滑激活和无界参数需要额外处理。", "论文给出的泛化联系是稳定控制解之间的存在与误差估计，不是训练算法必然找到该解，也不是现成的测试误差界。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1807.01083；PDF：https://arxiv.org/pdf/1807.01083。", "全文 PDF 共 45 页，SHA-256：3aa23633cd0ee6322385ff02dce05518bb60833e8ea8dcd754b32aa190904474。", "复核路线是先从连续 ResNet 控制泛函推导动态规划恒等式，再 lifting 到 L2 验证 HJB；独立地做 needle variation 得到 PMP，并在一个线性—二次模型中比较 population 与 sampled 边值问题。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Sec. 3 的 population 与 sampled 控制问题，确认“mean-field”来自共享控制对数据分布的依赖，而不是状态 ODE 显含分布。", "再读 Secs. 4–5 的 measure derivative、HJB 和 viscosity solution；如果关注训练算法，可跳到 Sec. 6 的 PMP。", "最后读 Secs. 7–9，将 PMP 唯一性、稳定 population 解附近的 sampled 解存在性和实际优化收敛严格区分。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "连续深度残差网络把层传播变成受控 ODE，而同一权重轨迹同时作用于整个输入—标签分布。论文把 population-risk 训练提升为概率测度空间中的平均场最优控制：无限维 HJB 给出全局 value function，mean-field Pontryagin 原理给出前向状态、后向伴随和平均 Hamiltonian 最大化条件。稳定 population 解还可与有限样本 PMP 解建立高概率邻近关系，但这不是实际训练算法的无条件全局收敛定理。", "selection_rationale": "全文是控制论结构与定理推导，没有承担结论的原始可视化；题目与物理摘要能准确区分 HJB 全局刻画、PMP 必要条件和有限样本稳定性。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Population optimal-control objective", "latex": r"\inf_{\boldsymbol\theta}\;\mathbb E_{\mu_0}\!\left[\Phi(x_T,y_0)+\int_0^T L(x_t,\theta_t)\,dt\right],\quad \dot x_t=f(x_t,\theta_t)", "role": "represent continuous-depth population-risk minimization", "symbols": {"mu_0": "input-target distribution", "theta_t": "shared control or layer weights", "Phi": "terminal loss", "L": "running regularizer", "f": "network dynamics"}, "evidence": "paper.pdf p. 5, Eq. (3)", "interpretation": "Randomness enters through the data distribution, while a single control path acts on every realization."},
            {"label": "Mean-field PMP maximum condition", "latex": r"\mathbb E_{\mu_0}H(x_t^*,p_t^*,\theta_t^*)\ge \mathbb E_{\mu_0}H(x_t^*,p_t^*,\theta),\qquad \forall\theta\in\Theta", "role": "state the shared-control optimality condition", "symbols": {"x_t": "forward state", "p_t": "adjoint state", "H": "Pontryagin Hamiltonian", "Theta": "admissible control set"}, "evidence": "paper.pdf p. 23, Eq. (45)", "interpretation": "Optimality is imposed after averaging the Hamiltonian over the population, not independently for each sample."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–7: continuous ResNet and population/sample control objectives", "paper.pdf pp. 7–22: Wasserstein value function, HJB and viscosity solution", "paper.pdf pp. 22–31: mean-field PMP, uniqueness conditions and HJB–PMP relation", "paper.pdf pp. 31–41: stable sampled solutions, generalization interpretation and scope", "source PDF SHA-256 3aa23633cd0ee6322385ff02dce05518bb60833e8ea8dcd754b32aa190904474", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
