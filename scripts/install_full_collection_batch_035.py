#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 035."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_032 import card
from install_full_collection_batch_014 import sec


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1088-1751-8121-adbfe6-meta", "arXiv manuscript", "https://arxiv.org/pdf/2409.14166",
        "Why gauge invariance applies to statistical mechanics", "为什么规范不变性适用于统计力学",
        "theory_numerics", "f4279cf69df26364", "Statistical Mechanics",
        {"doi": "10.1088/1751-8121/adbfe6", "arxiv_id": "2409.14166", "version": "arXiv v3 full text", "title": "Why gauge invariance applies to statistical mechanics", "authors": ["Johanna Müller", "Florian Sammüller", "Matthias Schmidt"], "journal": "Journal of Physics A: Mathematical and Theoretical", "volume": "58", "issue": "12", "article": "125003", "published": "2025-03-21", "abstract": "Local canonical shifts of particle coordinates and momenta preserve the Gibbs measure, form a noncommutative group and generate exact hyperforce identities in classical equilibrium statistical mechanics.", "comment": "ArXiv v3 full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Johanna Müller、Florian Sammüller、Matthias Schmidt；Journal of Physics A 58, 125003 (2025)，DOI:10.1088/1751-8121/adbfe6。全文取 arXiv:2409.14166v3，共19页；Crossref 未给出关联更正或撤稿。Collection ID 末尾的 meta 是原始清单标识，不是 DOI 的组成部分。"),
            sec("研究问题", "平衡经典统计力学中的系综平均依赖相空间积分，看似会随粒子坐标的局域重参数化而变化。论文问：怎样同时移动位置与动量，使微分相空间体积和 Gibbs 测度严格保持，并由有限变换、无穷小生成元和 Noether 结构系统地产生精确相关函数恒等式？"),
            sec("背景", "对每个粒子作 r_i→r_i+ε(r_i)，动量必须乘以位置 Jacobian 的逆矩阵，才能补偿坐标体积变化。要求 r+ε(r) 是光滑双射；该变换是 canonical transformation，逐粒子保持 dr_i dp_i，因而任何规范变换后的 observable 与同步变换的 Hamiltonian 具有相同热平均。", "这里的 gauge 是相空间坐标重参数化，不是电磁规范场，也没有引入新的物理相互作用。论文借电动力学说明群与 Noether 思路，但统计力学构造的对象、生成元和守恒量不同。"),
            sec("模型与方法", "两次有限位移按 ε21(r)=ε1(r)+ε2[r+ε1(r)] 复合，因此一般不交换；逆变换由隐式方程确定。作者进一步构造 configurational 与 full-phase-space shifting operators，证明其 commutators 闭合为非交换 Lie algebra，并将局域生成元作用于 Boltzmann weight 和任意 observable。", "由分部积分和归一化 Gibbs 测度得到 one-body hyperforce sum rule，把 observable 的局域位移响应与其和微观力密度的相关联系起来。推导是平衡、经典、可积分边界条件下的精确恒等式；量子、非平衡或奇异非双射映射不在该证明范围内。"),
            sec("核心结果与证据", "Figure 6 用一维硬杆 Monte Carlo 直接检验有限变换：ε0/a=0.5 时位移场满足可逆性，原系统和变换系统的密度 ρ(x) 与单体相空间分布在数值误差内重合；ε0/a=1.5 超过可逆阈值后，密度和分布出现伪影。", "数值例证区分了两件事：测度不变性由 canonical/diffeomorphic 结构严格推出，Monte Carlo 只展示算法实现是否忠实；无效位移的失败不是理论反例，而是违反变换定义域。", "无穷小算符的交换子保留 Dirac-localized 粒子分辨率，Jacobi identity 成立；对 Hamiltonian 和 Boltzmann weight 的作用给出力密度，从而得到适用于一般 observables/order parameters 的 exact hyperforce identities。"),
            sec("有效性与局限", "核心结论依赖平衡 Gibbs ensemble、经典粒子相空间、光滑可逆映射和适当边界项消失。hard-core 相互作用可由构型空间边界处理，但带拓扑改变、不可逆映射或不规范采样的算法不能直接套用。", "Figure 6 仅是受限一维硬杆的小型验证，不能证明所有 Monte Carlo proposal 都提高效率；作者把 smart sampling 作为前景。hyperforce sum rules 的数值方差、有限样本优势和复杂多体体系中的实现仍需逐例评估。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2409.14166；期刊：https://doi.org/10.1088/1751-8121/adbfe6。PDF SHA-256：ba7ce9d942248312755717ff16d51b53cbde2b8fb1bbce081ba814364bf93ac5。", "复现 Figure 6 需固定硬杆数与尺寸、L=10a、壁势、温度、ε(x)=ε0 sin(4πx/L)、Jacobian/动量映射、proposal 与 acceptance rule、热化和采样长度。Evidence status: full-text verified theory/simulation manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 的定义边界，再读 pp.4–7 的有限变换、群复合与逆元；pp.8–14 看局域生成元、交换代数和 hyperforce identities。最后以 p.12 Figure 6 检查可逆性条件，并把 p.14 的采样讨论视为算法展望。"),
        ],
        "figure-6-gauge-invariance.webp", "Figure 6", 12, "comparison",
        "一维硬杆在未位移、可逆有限位移和超过可逆阈值三种情况下的密度与相空间分布。",
        "满足双射条件的 canonical shift 保持测量分布，而不可逆位移产生明显数值伪影。",
        "Figure 6把严格的可逆性条件与可观察的 Monte Carlo 后果直接并列。",
        [{"label": "Canonical phase-space shift", "latex": r"\mathbf r_i'=\mathbf r_i+\boldsymbol\epsilon(\mathbf r_i),\quad \mathbf p_i'=[\mathbf 1+\nabla_i\boldsymbol\epsilon(\mathbf r_i)]^{-1}\mathbf p_i", "role": "preserve the particle-resolved phase-space volume under a local coordinate shift", "symbols": {"epsilon": "smooth displacement field", "r_i,p_i": "particle position and momentum"}, "evidence": "paper.pdf pp. 4–5, Eqs. (10)–(11)", "interpretation": "The invariance requires the coordinate map to remain a diffeomorphism."}],
        ["paper.pdf pp. 4–7, Eqs. (10)–(23): canonical map, group composition and inverse", "paper.pdf pp. 8–14: local generators, commutators and hyperforce sum rules", "paper.pdf p. 12, Figure 6: finite-shift Monte Carlo validation", "source PDF SHA-256 ba7ce9d942248312755717ff16d51b53cbde2b8fb1bbce081ba814364bf93ac5", "Evidence status: full-text verified theory/simulation manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-4t7t-v19l", "arXiv manuscript", "https://arxiv.org/pdf/2408.10205",
        "Kolmogorov-Arnold Networks Meet Science", "Kolmogorov–Arnold 网络遇见科学",
        "ai_empirical", "dad692c69e5156b4", "AI for Science",
        {"doi": "10.1103/4t7t-v19l", "arxiv_id": "2408.10205", "version": "arXiv v1 full text", "title": "Kolmogorov-Arnold Networks Meet Science", "authors": ["Ziming Liu", "Max Tegmark", "Pingchuan Ma", "Wojciech Matusik", "Yixuan Wang"], "journal": "Physical Review X", "volume": "15", "issue": "4", "article": "041051", "published": "2025-12-17", "abstract": "KAN 2.0 adds multiplication nodes, symbolic compilation, modular structure discovery and hypothesis testing, then demonstrates these tools on known conservation laws, Lagrangians, symmetries and constitutive relations.", "comment": "ArXiv v1 full text linked by Crossref as the preprint of the open-access version of record; no update relation found"},
        [
            sec("作者信息", "作者 Ziming Liu、Max Tegmark、Pingchuan Ma、Wojciech Matusik、Yixuan Wang；Physical Review X 15, 041051 (2025)，DOI:10.1103/4t7t-v19l。全文取 arXiv:2408.10205v1，共27页；Crossref 将其列为期刊论文 preprint，未发现更正或撤稿。"),
            sec("研究问题", "第一代 KAN 将可学习的一元 spline 放在边上，便于把网络转换为符号公式，但纯加法节点难以紧凑表达乘法结构，也缺少从已知公式初始化、从大模型抽取模块和比较物理假设的工作流。论文问：怎样把 KAN 变成可交互的科学建模工具，而不只是回归器？"),
            sec("背景", "MultKAN 在普通求和节点外加入 multiplication nodes，使 xy 等乘性结构可由单节点表达；kanpiler 把用户给定的符号表达式编译成 KAN，再允许 spline fine-tuning。作者还提出 attribute/feature、module 和 symbolic-formula 三层可解释性。", "所谓 science discovery 主要是对已知方程的合成数据回收、先验引导的结构选择与假设检验。它证明工具链能表示和优化这些结构，不等于系统自动发现了新的自然定律。"),
            sec("模型与方法", "整体网络是多层 Ψ_l 的复合，乘法层把若干 addition-node outputs 相乘。workflow 包括稀疏初始化、pruning、symbolic fitting、checkpoint rewind、branching hypothesis tests，以及先用宽 KAN 识别 separability、再构造更小模块网络。", "应用覆盖二维谐振子守恒量、单摆和相对论粒子 Lagrangian、Schwarzschild 隐对称、Neo-Hookean constitutive law。多数训练点由已知解析方程均匀采样；先验、候选函数库、随机种子和人工交互均参与最终结构选择。"),
            sec("核心结果与证据", "Figure 10 中三个 [4,[0,2],1] KAN 以不同随机种子分别回收到二维谐振子的 x 向能量、y 向能量和角动量，训练条件来自必要充分条件 f(z)·∇H(z)=0。图展示的是已知系统上的独立守恒量回收，不是从实验噪声中发现未知守恒律。", "kanpiler 对 Feynman 数据集的120个公式进行 exact symbolic encoding，spline approximation 的理论/数值误差随网格密度呈高阶下降。这里的 exact 指已知表达式被编译，不能与 blind symbolic regression 的成功率混为一谈。", "Schwarzschild 例暴露失败模式：KAN 常落入带 domain wall 的分段解，约三分之一随机种子得到全局平滑解；先用 MLP 教师初始化、再细化 spline 网格才把 loss 降至约10^-15。相对论动能的候选拟合也表明噪声和先验会改变符号判断。"),
            sec("有效性与局限", "样例多为低维、合成、已知答案的方程；输入 feature、module、线性本构先验或候选函数库会把预期结构写入搜索空间。网络拟合和 symbolic simplification 对局部极小、正则化、grid、seed、threshold 与数据噪声敏感。", "可解释性随网络规模增加而下降，复杂科学问题仍需人工提出假设并核验。Figure 14 的 accuracy–interpretability tradeoff 是概念总结而非统一 benchmark；文中没有证明 KAN 普遍优于 MLP、neural operator 或其他符号回归方法。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2408.10205；期刊：https://doi.org/10.1103/4t7t-v19l；代码：https://github.com/KindXiaoming/pykan。PDF SHA-256：f7c1070cd3be933f8690e9b7a903441ed10f7d7e35fb2d574b645ae66059dace。", "复现需锁定 pykan 0.2.x、网络宽度/乘法 arity、grid、spline order、sample domain、loss normalization、regularization、pruning/symbolic thresholds、候选库和全部 seeds。Evidence status: full-text verified AI/theory benchmark manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–5 的 MultKAN 与 kanpiler，再读 pp.6–13 的 modularity、symbolic fitting 和 hypothesis testing。p.14 Figure 10 是最清晰的物理回收案例；随后读 pp.15–19 的 Lagrangian、symmetry、constitutive examples，并重点保留 domain wall、候选误判与 prior dependence。"),
        ],
        "figure-10-conserved-quantities.webp", "Figure 10", 14, "comparison",
        "三个 KAN 结构分别表示二维谐振子的两个分方向能量和角动量守恒量。",
        "在已知动力系统和正交约束损失下，不同随机种子回收到三个独立守恒量。",
        "Figure 10直接展示可解释网络图与物理公式的一一对应，同时清楚限定为已知合成系统。",
        [{"label": "Conservation constraint", "latex": r"\mathbf f(\mathbf z)\cdot\nabla H(\mathbf z)=0", "role": "train a scalar KAN to remain constant along a known dynamical flow", "symbols": {"z": "phase-space state", "f": "known vector field", "H": "candidate conserved quantity"}, "evidence": "paper.pdf pp. 14–15, Section 5.1", "interpretation": "The learned invariant is conditional on the supplied dynamics and sampling domain."}],
        ["paper.pdf pp. 2–5: MultKAN and symbolic compiler", "paper.pdf pp. 6–13: modularity, symbolic fitting and hypothesis tests", "paper.pdf pp. 14–19, Figures 10–13: physics applications and failure modes", "source PDF SHA-256 f7c1070cd3be933f8690e9b7a903441ed10f7d7e35fb2d574b645ae66059dace", "Evidence status: full-text verified AI/theory benchmark manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-k6f7-gtr7", "arXiv manuscript", "https://arxiv.org/pdf/2508.20472",
        "Photonic Restricted Boltzmann Machine for Content Generation Tasks", "用于内容生成任务的光子限制玻尔兹曼机",
        "theory_experiment", "5ac46a28f8fc55bb", "Photonic Computing",
        {"doi": "10.1103/k6f7-gtr7", "arxiv_id": "2508.20472", "version": "arXiv v1 full text", "title": "Photonic Restricted Boltzmann Machine for Content Generation Tasks", "authors": ["Li Luo", "Yisheng Fang", "Wanyi Zhang", "Zhichao Ruan"], "journal": "Physical Review X", "volume": "16", "issue": "1", "article": "011071", "published": "2026-03-31", "abstract": "A wavelength-multiplexed spatial-light-modulator architecture evaluates RBM Gibbs updates optically and is tested on Ising sampling, small image generation/restoration and piano-roll sequences.", "comment": "ArXiv v1 full text linked by Crossref as the preprint of the open-access version of record; no update relation found"},
        [
            sec("作者信息", "作者 Li Luo、Yisheng Fang、Wanyi Zhang、Zhichao Ruan；Physical Review X 16, 011071 (2026)，DOI:10.1103/k6f7-gtr7。全文取 arXiv:2508.20472v1，共21页含补充材料；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "RBM 生成需要在 visible/hidden layers 之间反复 Gibbs sampling，电子实现受矩阵乘加、存储和数据搬运限制。论文问：能否把每个条件概率所需的局域能量差编码到多波长光场，在一次光学传播中并行求和，同时避免一般 spatial photonic Ising machine 所需的矩阵分解？"),
            sec("背景", "PRBM 用不同波长对应不同待更新 spin，SLM 三个区域分别编码目标 spin、与其连接的另一层 spins×weights 和 bias。checkerboard phase 的 gauge transform 把任意有界 interaction/bias 映射成相位，camera intensity difference 给出翻转能量差，再由数字反馈抽样。", "作者把每次光学求和的传播深度视为 O(1)，而电子直接求和为 O(N)。这一复杂度口径不包含 SLM 写入、camera readout、随机数、反馈循环、波长资源和串行更新全部系统成本。"),
            sec("模型与方法", "先把10×10 二维 nearest-neighbor Ising lattice 二分为 visible/hidden layers，在14个温度用光子 Gibbs sampling 测量 susceptibility 与 heat capacity。随后用14×14二值 Fashion-MNIST/MNIST 图像训练独立 RBMs，并对未进入训练集的20×20遮挡/加噪图像做15步恢复。", "时间内容测试将88个钢琴键映为 visible spins、96个 hidden spins，使用 Nottingham 数据训练 RNN-RBM；每个 time step 做20次 Gibbs iteration，生成150个八分音符时长的 piano roll。评价主要是图像/音乐可视化与物理校准，未给统一 FID、likelihood 或听觉盲评。"),
            sec("核心结果与证据", "Figure 2 的光学样本随温度由无序转为有序，susceptibility/heat-capacity peak 给出 Tc=2.3J，与无限二维 Ising 精确值约2.27J接近。这是核心硬件正确性校准，但10×10有限尺寸、测量误差和采样相关会影响峰位置。", "Figures 3–4 展示 Boot、Pants、数字0的15步生成，以及训练集外遮挡/噪声图的恢复；Figure 5 展示150步音乐序列。结果说明设备能执行这些小型 RBM workloads，不等于达到现代生成模型的质量或规模。", "论文估计更快 SLM 可达纳秒 step、10^10 pixels 和200 TFLOPS，并据计算量模型预测大规模训练优势。这些是器件/面积/并行假设下的外推，不是本文装置实测；与 H100/GPT-3 的比较也没有端到端能耗和 wall-clock benchmark。"),
            sec("有效性与局限", "实验速度受液晶 SLM 调制限制，反馈、探测和随机抽样仍包含电子环节。波长通道数、像素串扰、shot noise、校准漂移、interaction dynamic range 和光功率会限制规模；O(1) 指理想并行算术深度，不表示总体资源与 N 无关。", "内容任务规模小、类别少，且定性展示多于标准生成指标。图像恢复不是排除所有 overfitting 的充分检验，音乐相似性也未由人类或统计指标独立评估；语言模型、10亿参数及两数量级训练加速均属未来推算。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2508.20472；期刊：https://doi.org/10.1103/k6f7-gtr7。PDF SHA-256：e90bed6aa563b775ac1b2fe78f25f0d7cb4a70a9892ecf94fdd0d8ec51bc7e47。", "复现需固定 laser spectrum、grating/lens/SLM/camera、phase calibration、macro-pixel、weight normalization L、feedback latency、temperature、Gibbs update order、training split、iterations 和 seeds。Evidence status: full-text verified photonic experiment manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–4 Figure 1、Eqs. (1)–(2) 理解编码与能量差；p.4 Figure 2核对 Ising 校准。pp.4–6 看图像、恢复和音乐结果，随后把 p.6 的 O(1)、TFLOPS、H100 与十亿参数陈述分成实测结果和条件外推两类。"),
        ],
        "figure-2-ising-validation.webp", "Figure 2", 4, "comparison",
        "10×10 Ising lattice 的光子 Gibbs 样本以及 susceptibility、heat capacity 随温度的峰。",
        "装置测得的有限尺寸相变温度约2.3J，与二维 Ising 理论值约2.27J接近。",
        "Figure 2是比生成图像更可量化的硬件校准，直接测试条件概率采样是否实现正确物理统计。",
        [{"label": "Photonic Gibbs update", "latex": r"P(h_k=1\mid\mathbf v)=\left[1+\exp(\Delta H_k/T)\right]^{-1}", "role": "convert the optically measured flip-energy difference into a hidden-spin sample", "symbols": {"Delta H_k": "intensity-derived energy difference", "T": "sampling temperature"}, "evidence": "paper.pdf p. 3, Eq. (2) and feedback rule", "interpretation": "Optical summation accelerates the energy calculation, while stochastic feedback and repeated Gibbs iterations remain necessary."}],
        ["paper.pdf pp. 2–3, Figure 1 and Eqs. (1)–(2): optical encoding and Gibbs update", "paper.pdf p. 4, Figure 2: Ising phase-transition validation", "paper.pdf pp. 4–6, Figures 3–5: image and temporal generation", "source PDF SHA-256 e90bed6aa563b775ac1b2fe78f25f0d7cb4a70a9892ecf94fdd0d8ec51bc7e47", "Evidence status: full-text verified photonic experiment manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-kwyy-1xln", "arXiv manuscript", "https://arxiv.org/pdf/2506.15121",
        "Generative Thermodynamic Computing", "生成式热力学计算",
        "theory_numerics", "41206da31a1be155", "Thermodynamic Computing",
        {"doi": "10.1103/kwyy-1xln", "arxiv_id": "2506.15121", "version": "arXiv v3 full text", "title": "Generative Thermodynamic Computing", "authors": ["Stephen Whitelam"], "journal": "Physical Review Letters", "volume": "136", "issue": "3", "article": "037101", "published": "2026-01-20", "abstract": "A continuous-spin Langevin computer is trained from forward noising trajectories so that its autonomous physical dynamics approximately reverses them and generates small MNIST-like samples.", "comment": "ArXiv v3 manuscript cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Stephen Whitelam；Physical Review Letters 136, 037101 (2026)，DOI:10.1103/kwyy-1xln。全文取 arXiv:2506.15121v3，共5页；Crossref 未列关联更正或撤稿。卡片使用作者手稿而非受限许可的 APS 排版版。"),
            sec("研究问题", "数字扩散模型用神经网络和伪随机噪声逐步去噪。论文问：能否让处于热浴中的非线性模拟器件自身提供噪声，并把训练得到的生成信息写入其势能 landscape，使系统从随机初态出发仅靠自然 Langevin dynamics 生成结构？"),
            sec("背景", "N 个连续自由度遵从 overdamped Langevin equation，势能含单元二次/四次项、bias 和 pairwise couplings。训练时先在 coupling-free 系统上把 MNIST 输入逐渐噪声化，再最大化带参数系统生成 reverse steps 的路径概率；生成时固定训练后的 couplings，不再由外部神经网络逐步控制。", "这是数字模拟的 thermodynamic computer proof of principle。文中提及机械、电路或 Josephson oscillators 只是可能硬件载体，未制造、测量或校准真实模拟器件。"),
            sec("模型与方法", "作者用离散 Euler–Maruyama step 写出 forward 与 reverse transition likelihood，并沿每条 noising trajectory 对 Jij、bi 做 gradient ascent。通过 fluctuation relation，最大化 reverse likelihood 等价于降低生成反向轨迹的预期 heat/entropy production。", "示例含28² visible units、512 hidden units，训练参数包括 NvNh 可见–隐藏耦合、隐藏层互耦和 biases；训练集只含三个数字。生成轨迹长度 tf=2.5，从 coupling-free equilibrium noise 出发，论文报告的是1000条数字模拟的统计与示例。"),
            sec("核心结果与证据", "Figure 2a 的三条独立轨迹从噪声逐渐形成训练过的数字结构；Figure 2b 展示25个终态，样式具有多样性但也出现倒相数字和 mode mixing。作者明确称其为 rudimentary proof of principle，而不是高质量 MNIST benchmark。", "Figure 2c 的16个隐藏单元 coupling maps 呈局域笔画样 receptive fields，说明训练把部分视觉结构编码到能量 landscape。该可视化是机制线索，未证明隐变量唯一可解释或覆盖完整数据分布。", "数字估算中，模拟 thermodynamic trajectory 的平均 heat emission 为2.9×10^3 kBT；与假设每 MAC 约1 pJ、784→128→128→784 denoiser、10 steps 的数字预算相比得到>10^11能耗比。比较没有实际硬件、控制/读出/训练/制冷成本，不能当作实测节能。"),
            sec("有效性与局限", "全部生成结果来自数值积分，训练仅三种数字且没有 FID、likelihood、coverage 或与数字 diffusion baseline 的同协议比较。连续变量、全连接耦合的精确物理实现、parameter precision、device disorder 和读出都会改变可行性。", "thermodynamic optimal 的含义限定为给定 reference process 与模型族内，训练降低 reverse-path heat；不保证全局最优，也不等于 Landauer 极限或整个计算系统的最小能耗。条件生成和 time-dependent couplings 被留作未来扩展。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2506.15121；期刊：https://doi.org/10.1103/kwyy-1xln。PDF SHA-256：a66f12fad69b91e609372e3f4e817c24a6db7749b0d5851b04b18790d3bd73fa。", "复现需固定 J2=J4=10kBT、Nv=784、Nh=512、训练三数字、tf=2.5、dt、mobility、trajectory count、learning rate、initial biases、seeds 与 heat/MAC accounting assumptions。Evidence status: full-text verified theory/digital simulation manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 的 Langevin dynamics、potential 和 reverse-step likelihood；p.3 Figure 2 看实际生成质量与 mode mixing。pp.3–5 的 fluctuation relation 给出热解释；阅读能耗部分时把模拟 heat、假设硬件能标和端到端系统能耗严格分开。"),
        ],
        "figure-2-thermodynamic-generation.webp", "Figure 2", 3, "comparison",
        "三条噪声到数字的 Langevin 轨迹、25个生成终态和代表性隐藏单元耦合图。",
        "训练后的势能 landscape 能在数字模拟中把热噪声初态导向多样的数字样结构，同时仍出现 mode mixing。",
        "Figure 2同时给出成功样本、失败模式与内部耦合，是评估 proof-of-principle 最完整的证据。",
        [{"label": "Langevin computer dynamics", "latex": r"\dot x_i=-\mu\,\partial_i V_\theta(\mathbf x)+\sqrt{2\mu k_BT}\,\eta_i(t)", "role": "generate samples through autonomous noisy physical dynamics", "symbols": {"mu": "mobility", "V_theta": "trainable potential energy", "eta": "Gaussian white noise"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "The paper simulates this stochastic dynamics; no physical hardware implementation is demonstrated."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(12): Langevin model and reverse-path training", "paper.pdf p. 3, Figure 2: generated trajectories, samples and couplings", "paper.pdf pp. 3–5, Eqs. (13)–(14): heat interpretation and hardware extrapolation", "source PDF SHA-256 a66f12fad69b91e609372e3f4e817c24a6db7749b0d5851b04b18790d3bd73fa", "Evidence status: full-text verified theory/digital simulation manuscript; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevd.106.065013", "arXiv manuscript", "https://arxiv.org/pdf/2108.10085",
        "Numerical fluid dynamics for FRG flow equations: Zero-dimensional QFTs as numerical test cases. II. Entropy production and irreversibility of RG flows", "FRG 流方程的数值流体动力学：零维 QFT 数值测试（二）熵产生与 RG 流不可逆性",
        "theory_numerics", "ad63b9c0632bb9dc", "Renormalization Group",
        {"doi": "10.1103/PhysRevD.106.065013", "arxiv_id": "2108.10085", "version": "arXiv v2 full text", "title": "Numerical fluid dynamics for FRG flow equations: Zero-dimensional QFTs as numerical test cases. II. Entropy production and irreversibility of RG flows", "authors": ["Adrian Koenigstein", "Martin J. Steil", "Nicolas Wink", "Eduardo Grossi", "Jens Braun"], "journal": "Physical Review D", "volume": "106", "issue": "6", "article": "065013", "published": "2022-09-13", "abstract": "In a zero-dimensional Z2-symmetric functional-RG benchmark, nonlinear diffusion makes a total-variation-related numerical entropy grow monotonically and exposes irreversibility at the flow-equation level.", "comment": "ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref update relation found"},
        [
            sec("作者信息", "作者 Adrian Koenigstein、Martin J. Steil、Nicolas Wink、Eduardo Grossi、Jens Braun；Physical Review D 106, 065013 (2022)，DOI:10.1103/PhysRevD.106.065013。全文取 arXiv:2108.10085v2，共23页；Crossref 未列关联更正或撤稿。"),
            sec("研究问题", "FRG 把 ultraviolet action 沿 scale 演化到 infrared effective action，粗粒化直觉暗示信息损失，但 flow equation 本身如何量化不可逆性并不显然。论文问：当局域势近似的 FRG 方程写成非线性 advection/diffusion PDE 时，能否借 numerical entropy 与 total-variation non-increasing 性质构造单调量？"),
            sec("背景", "作者将 RG time 定义为 t=-ln(k/Λ)，把 field coordinate 视为空间变量；零维 O(1) 模型的 local potential approximation 给出纯非线性 diffusion equation。扩散抹平尖点和大梯度，类似热传导丢失初态细节，从而在 flow-equation 层面呈现 semigroup 而非可逆群。", "文中的 entropy 首先是 PDE/numerical-fluid-dynamics 意义下的单调泛函，不是直接从微观态计数得到的热力学熵。它与 C-/A-theorem 的联系被作者明确描述为可能关系，而非已证明的一般等价。"),
            sec("模型与方法", "对 u(t,x)=∂xU(t,x)，作者以负的梯度平方积分定义 S，并减去 t=0 值得到有限归一化 C。有限体积网格用前向差分重建 ∂xu；其离散形式与 total variation 的符号约定相反，因此 diffusion 下 TV 非增而 C 非减。", "数值采用前一系列论文给出的 Kurganov–Tadmor central scheme，比较五类零维 Z2 初始势：含不连续斜率的分段势、正/负质量 φ4、含 arctan 与 cusp 的条件。Table I 用高精度一维积分检查二点函数，相对误差约6×10^-6至5.8×10^-6/10^-5量级。"),
            sec("核心结果与证据", "Figure 2 对非解析初始势显示 C 在扩散最强的 RG 时间窗快速上升，随后在 IR 达到 plateau；这对应初始跳变被平滑、细节丢失和稳态建立。绝对 plateau 数值因 t=0 的非光滑导数及离散化而病态，作者只赋予单调趋势定性意义。", "φ4 正负质量及其他测试的 Figures 5、6、8、10 也显示数值熵单调上升，UV/IR plateaus 与 RG consistency/steady regimes 对应。更剧烈的初态不连续导致更大的 discrete total-variation change，但不同图的绝对值不应当作普适物理熵比较。", "文章进一步讨论 dimensionless rescaled flow 中的 advection 与 source terms：它们可增加 arc length，使当前 C 不再显然单调。作者没有为一般高维 O(N)、含 fermions 或完整 theory space 构造 C-function，因此结果是一个受控 benchmark 和方法线索。"),
            sec("有效性与局限", "严格数值展示集中于零维 O(1) 和特定 LPA PDE；零维模型没有真实时空传播，也不存在通常意义的相变。将 IR steady flow 类比 thermodynamic equilibrium、将 RG time 类比时间箭头是结构解释，不应扩张为所有 RG 方案的热力学定理。", "C 的定义使用 dimensionful fields/couplings；canonical rescaling 引入 source/advection 后会破坏简单单调性。非光滑初态的绝对熵强依赖 grid，有限体积 scheme 自身也有 numerical diffusion；作者验证了结果/精确积分误差，但没有消除所有 scheme dependence。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2108.10085；期刊：https://doi.org/10.1103/PhysRevD.106.065013。PDF SHA-256：aab52b617c0291308e4e99ee75f4e791910e98c91be275ddec80c20fad3063e0。原文称数值和图由 Mathematica 生成。", "复现需固定 regulator、Λ、xmax、volume cells、ghost-cell boundary、KT flux/time stepping、五类 UV potentials、t range 和 high-precision partition-function benchmark。Evidence status: full-text verified theory/numerical manuscript; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–3 的 RG–PDE 对应，再读 pp.6–8 Eqs. (20)–(26) 区分 C、S 与 TV。p.10 Figure 2 是最清楚的单调增长证据；pp.9–15 检查各测试，pp.16–18 重点看 dimensionless rescaling 和作者未解决的一般化障碍。"),
        ],
        "figure-2-rg-entropy.webp", "Figure 2", 10, "data_plot",
        "零维 O(1) 非解析初始条件下，归一化数值熵 C 随 RG time 单调上升并进入 IR plateau。",
        "非线性扩散抹平初态跳变的同一时间窗中，数值熵增长并在 IR 稳态停止变化。",
        "Figure 2最直接显示论文所定义单调量；图下注释也提醒其绝对值不具有定量普适意义。",
        [{"label": "Normalized numerical entropy", "latex": r"C[\partial_xu(t,x)]=S[\partial_xu(t,x)]-S[\partial_xu(0,x)]", "role": "quantify diffusion-driven loss of field-space structure along RG time", "symbols": {"u": "field derivative of the effective potential", "S": "negative gradient-square entropy functional", "t": "RG time"}, "evidence": "paper.pdf pp. 7–8, Eqs. (20)–(24)", "interpretation": "Monotonicity is established for the studied diffusion equation; the construction is not yet a general dimensionless C-function."}],
        ["paper.pdf pp. 1–3: FRG, RG time and fluid-dynamic interpretation", "paper.pdf pp. 6–8, Eqs. (20)–(26): numerical entropy and total variation", "paper.pdf pp. 9–15, Figures 2–10: zero-dimensional test cases", "paper.pdf pp. 16–18: rescaled-flow obstacles and C/A-theorem discussion", "source PDF SHA-256 aab52b617c0291308e4e99ee75f4e791910e98c91be275ddec80c20fad3063e0", "Evidence status: full-text verified theory/numerical manuscript; no independent reproduction performed."],
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
