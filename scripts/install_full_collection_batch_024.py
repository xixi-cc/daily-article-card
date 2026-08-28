#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 024."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2603.18992", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2603.18992",
        "title_en": "Foundations of Schrödinger Bridges for Generative Modeling",
        "title_zh": "生成建模的薛定谔桥基础",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["0f11a8b5baa4378b"], ["Generative Models"]),
        "verified_metadata": meta("2603.18992", "v1", "Foundations of Schrödinger Bridges for Generative Modeling", ["Sophia Tang"], ["cs.LG", "cs.AI"], "cs.LG", "2026-03-19T14:59:56Z", "A self-contained guide develops Schrödinger bridges from optimal transport, stochastic control and path-space entropy, then connects them to score and flow matching."),
        "sections": [
            sec("作者信息", r"作者：Sophia Tang；arXiv:2603.18992v1。全文 221 页，是一部从测度论、随机过程和最优输运出发的系统教程；它整理并证明既有结果，再连接现代生成模型，不是新 benchmark 论文。"),
            sec("研究问题", r"给定端点分布 \(\pi_0,\pi_T\) 和参考随机过程 \(Q\)，怎样在路径空间中找一个既满足端点约束、又对 \(Q\) 改动最小的过程？进一步，score-based diffusion、flow matching 与 simulation-free bridge training 如何从同一变分问题中出现？"),
            sec("背景", r"经典最优输运最小化端点搬运成本；Schrödinger bridge 则以相对熵约束整个随机路径测度。噪声不只是数值扰动，而是参考动力学的一部分；控制漂移负责在保持绝对连续性的同时实现目标边缘分布。", r"Figure 8 把 IPF 与 IMF 画成几何投影：IPF 交替满足两个端点边缘但中间迭代不保持耦合；IMF 在 Markovian 与 reciprocal 类之间投影，每一步保持两端约束并向最优桥测度收敛。"),
            sec("模型与方法", r"动态桥定义为在连续路径测度上最小化 \(\mathrm{KL}(P\Vert Q)\)，约束 \(p_0=\pi_0,p_T=\pi_T\)。对受控扩散，Girsanov 变换把路径 KL 化为期望控制能 \(\frac12\mathbb E\int_0^T\Vert u_t\Vert^2dt\)，并与 controlled Fokker–Planck PDE 耦合。", r"教程依次给出 Schrödinger potentials、HJB–FP 系统、Doob transform、time reversal、forward/backward SDE、IPF、IMF、score/flow matching，以及 Gaussian、generalized、multi-marginal 和 unbalanced bridges。"),
            sec("核心结果与证据", r"最重要的统一关系是：同一最优路径测度既可写成 entropy projection，也可写成随机最优控制；Hopf–Cole 变换把非线性 HJB–FP 耦合化为一对线性 Schrödinger potential 方程。", r"Figure 8 对应 Lemma 4.15、Proposition 4.16 和 Theorem 4.17：IMF 的 KL Pythagorean identity 给出单调改进，并在文中假设下收敛到唯一桥测度。该图是算法结构证据，不是数值性能曲线。", r"第 6 章说明 score matching 学习时间边缘的 score，flow matching 学习 probability-flow velocity；bridge matching 则额外编码双端条件。它们共享 transport-through-time 结构，但训练目标、参考过程与端点耦合不能互换。"),
            sec("有效性与局限", r"教程的价值是推导覆盖广、符号体系统一；但“统一框架”并不意味着各种算法计算成本或统计效率等价。存在性、唯一性和 Girsanov 表示依赖绝对连续性、有限 KL、正则系数和边缘条件。", r"全文没有新数据集、消融或独立实验；221 页中的广义桥、生成建模应用与算法实现深度不均。读者不能把理论等价直接解释为有限网络、离散求解器或有限样本下的经验等价。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2603.18992。全文 221 页，PDF SHA-256：5e707a69bd7ba57d90625e84bb3b3ffb54da5df485f6dd3a6503d7225f08ffd1。", r"复核应固定参考过程、扩散系数、端点边缘、KL convention、time orientation、Fokker–Planck sign、control scaling、IPF/IMF projection class 与 discretization。", r"Evidence status: full-text verified tutorial; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section 2.7 的 dynamic SB definition，再读 Girsanov/control-energy 等价与 HJB–FP 系统；随后看 Figure 8 和 Section 4 的 IPF/IMF。最后读 Section 6，把 score、flow 和 bridge matching 分别映射到它们学习的场与条件。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2603.18992/figure-8-imf-ipf.webp", "label": "Figure 8", "visual_type": "schematic", "evidence": "paper.pdf p. 106, Figure 8", "alt_text": "IPF 与 IMF 在边缘约束、Markovian 类和 reciprocal 类之间的投影路径。", "caption": "IMF 交替做 Markovian 与 reciprocal projection，并在每一步保持两端边缘。", "selection_rationale": "Figure 8 是全文最重要的算法几何图，优先于单一公式页。"},
        "figure_refs": [figure("2603.18992", "figure-8-imf-ipf.webp", "Figure 8", 106, "algorithmic projection geometry", "IMF 与 IPF 的投影轨迹和约束集合。", "IPF/IMF 的路径空间几何比较。", "The picture distinguishes endpoint-preserving IMF iterations from alternating marginal projections in IPF.")],
        "equation_refs": [
            {"label": "Dynamic Schrödinger bridge", "latex": r"P^\star=\arg\min_{P:\,P_0=\pi_0,\,P_T=\pi_T}\mathrm{KL}(P\Vert Q)", "role": "path-space entropy projection", "symbols": {"P": "candidate path measure", "Q": "reference path measure"}, "evidence": "paper.pdf pp. 31–32, Definition 2.2", "interpretation": "Choose the endpoint-compatible process that changes the reference dynamics least in relative entropy."},
            {"label": "Controlled diffusion cost", "latex": r"\mathrm{KL}(P^u\Vert Q)=\frac12\,\mathbb E_{P^u}\!\int_0^T\Vert u(X_t,t)\Vert^2dt", "role": "stochastic-control representation", "symbols": {"u": "scaled control drift", "T": "bridge horizon"}, "evidence": "paper.pdf pp. 49–53, dynamic SB control form", "interpretation": "Under the stated absolute-continuity assumptions, path entropy becomes quadratic control energy."},
        ],
        "evidence_refs": ["paper.pdf pp. 31–53: dynamic SB, Girsanov and controlled Fokker-Planck", "paper.pdf pp. 104–108: IMF/IPF geometry and convergence", "paper.pdf Sections 6–8: score, flow and bridge matching connections", "source PDF SHA-256 5e707a69bd7ba57d90625e84bb3b3ffb54da5df485f6dd3a6503d7225f08ffd1", "Evidence status: full-text verified tutorial; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2603.27880", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2603.27880",
        "title_en": "Kernel Dynamics under Path Entropy Maximization",
        "title_zh": "路径熵最大化下的核动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["3f027a13f14d1e56"], ["Training Dynamics"]),
        "verified_metadata": meta("2603.27880", "v1", "Kernel Dynamics under Path Entropy Maximization", ["Jnaneshwar Das"], ["cs.LG", "cs.AI", "cs.RO", "math.DS"], "cs.LG", "2026-03-29T21:34:08Z", "A Maximum Caliber proposal treats the representation kernel itself as a dynamical variable, with thermodynamic, fidelity and consistency constraints."),
        "sections": [
            sec("作者信息", r"作者：Jnaneshwar Das；arXiv:2603.27880v1。全文 8 页。论文明确区分 formal construction、structured correspondence 与 conjecture；RG、NTK、biology、scientific paradigms 和 craft mastery 主要是候选实例，不是已证实等价。"),
            sec("研究问题", r"通常 kernel \(k(x,x')\) 被当作固定相似度；但若 agent 的可分辨结构会随训练、能量预算和环境改变，优化所处的 information geometry 也在改变。论文问：能否在 kernel trajectories 上做 Maximum Caliber，并定义自洽 fixed points 与可检验的转变？"),
            sec("背景", r"每个正定核定义 RKHS，也诱导概率空间上的度量 \(g_k\)。因此路径 \(\gamma:t\mapsto k_t\) 不是只更新参数，而是在一族有效几何之间移动。MaxCal 以最少附加假设选择满足路径约束的分布。", r"Figure 2 用湖泊藻华采样解释这件事：移动的 bloom front 改变“哪些差异值得测量”，adaptive waypoints 随 kernel 变化，同时必须保留返航能量边界。"),
            sec("模型与方法", r"作者在 kernel path measure \(P[\gamma]\) 上最大化相对路径熵，并加入三类约束：核变化的 thermodynamic work、与环境相关变量的 mutual-information fidelity，以及 agent model 与环境分布的 KL consistency。解属于相对参考测度 \(Q[\gamma]\) 的 exponential family。", r"两核 toy model 给出切换阈值；self-consistency 要求 kernel 等于 MaxCal 动力学推回的 kernel。随后把 Wilson RG、finite-width NTK evolution 和 adaptive lake sampling 写成结构对应，并给出六个开放问题。"),
            sec("核心结果与证据", r"正式结果是 MaxCal 分布 \(P[\gamma]\propto Q[\gamma]\exp[-\lambda_W W[\gamma]+\lambda_I I[\gamma]-\lambda_D D_{KL}[\gamma]]\)：约束决定最可能 kernel path，而不是先验指定单一路径。", r"在明确的信息热力学假设下，新增 mutual information 满足 Landauer-type 下界 \(\delta W_k\ge k_BT\,\delta I_k\)。这是一条条件性下界，不证明实际深网或生物系统可逆地达到它。", r"Figure 2 把可证伪预测具体化：相同能量和样本数下，adaptive-kernel planning 应在高 advection 时优于 fixed kernel；论文未运行该实验。"),
            sec("有效性与局限", r"框架的优点是把 representation change、information gain 与 work budget 放进同一 path ensemble；但 kernel space 的参考测度、约束泛函和 multiplier 都需要外部指定。不同 kernel 的度量可比性及 fixed-point stability 仍未给出一般定理。", r"RG universality、NTK evolution、paradigm shifts 与 craft mastery 被作者标为 conjectural bridges；无数值模拟、消融或实测能耗。Landauer 下界需要信息以 nats 计量及物理实现假设，不能直接当成训练 GPU 能耗公式。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2603.27880。全文 8 页，PDF SHA-256：a1dea9868568a4ab6396d5b9a18904723ddef0f5e98d17141c9c85ed4c08fa36。", r"复核需明确 kernel family、reference path measure、time discretization、work/information/consistency estimators、multipliers、fixed-point map、environment process 与 falsification threshold。", r"Evidence status: full-text verified position paper; no independent reproduction performed."),
            sec("阅读指南", r"先读 Sections II–IV，核对 assumptions A1–A6 与 MaxCal distribution；再看 Figure 2 的湖泊协议，确认哪些量实际可测。最后读 RG/NTK correspondences 与 open questions，逐项区分 theorem、correspondence、conjecture 和 proposed experiment。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2603.27880/figure-2-lake-sampling.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 5, Figure 2", "alt_text": "动态藻华边界、adaptive waypoints、基地返航路线与能量储备边界。", "caption": "Kernel adaptation 改变采样航点，但仍受返航能量和会合约束。", "selection_rationale": "Figure 2 是最具可视化和可检验性的应用图，优先于抽象核轨迹小图。"},
        "figure_refs": [figure("2603.27880", "figure-2-lake-sampling.webp", "Figure 2", 5, "falsifiable adaptive-sampling protocol", "移动藻华、采样航点与返航约束。", "动态藻华的自适应采样示意。", "The figure turns kernel dynamics into a budgeted sensing-and-return problem rather than a metaphor.")],
        "equation_refs": [
            {"label": "MaxCal kernel path distribution", "latex": r"P[\gamma]\propto Q[\gamma]\exp\!\left[-\lambda_W W[\gamma]+\lambda_I I[\gamma]-\lambda_D D_{KL}[\gamma]\right]", "role": "least-assuming constrained path ensemble", "symbols": {"gamma": "kernel trajectory", "Q": "reference path measure"}, "evidence": "paper.pdf p. 3, Eq. (12)", "interpretation": "Thermodynamic cost, information fidelity and model consistency reweight the reference ensemble."},
            {"label": "Landauer-type kernel-change bound", "latex": r"\delta W_k\ge k_B T\,\delta I_k", "role": "conditional work lower bound", "symbols": {"delta_I_k": "new mutual information unlocked by kernel change", "T": "temperature"}, "evidence": "paper.pdf p. 3, Eq. (13)", "interpretation": "Under the stated physical assumptions, gaining representational mutual information cannot be free."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–3: assumptions, kernel path entropy and MaxCal distribution", "paper.pdf p. 5, Figure 2: adaptive lake-sampling protocol", "paper.pdf pp. 4–8: RG/NTK correspondences, conjectures and open questions", "source PDF SHA-256 a1dea9868568a4ab6396d5b9a18904723ddef0f5e98d17141c9c85ed4c08fa36", "Evidence status: full-text verified position paper; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2604.08121", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2604.08121",
        "title_en": "Uni-ViGU: Towards Unified Video Generation and Understanding via A Diffusion-Based Video Generator",
        "title_zh": "Uni‑ViGU：以扩散视频生成器统一视频生成与理解",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["91c76234d9010370"], ["Video Generation"]),
        "verified_metadata": meta("2604.08121", "v1", "Uni-ViGU: Towards Unified Video Generation and Understanding via A Diffusion-Based Video Generator", ["Luozheng Qin", "Jia Gong", "Qian Qiao", "Tianjiao Li", "Li Xu", "Haoyu Pan", "Chao Qu", "Zhiyu Tan", "Hao Li"], ["cs.CV", "cs.AI"], "cs.CV", "2026-04-09T11:41:58Z", "A generation-centric model performs continuous video flow and discrete text flow in one Transformer and reuses text-to-video priors for video understanding."),
        "sections": [
            sec("作者信息", r"作者：Luozheng Qin、Jia Gong、Qian Qiao、Tianjiao Li、Li Xu、Haoyu Pan、Chao Qu、Zhiyu Tan、Hao Li；arXiv:2604.08121v1。全文 14 页，基于 Wan2.1 的统一视频生成/理解原型。"),
            sec("研究问题", r"统一多模态模型通常从 understanding-centric MLLM 加生成模块，但视频扩散的 token 与算力规模远高于理解。论文反问：能否以预训练 video generator 为底座，把 text generation 写成同一 flow，并把 text-to-video correspondence 反向用于理解？"),
            sec("背景", r"视频生成在连续 VAE latent 上做 denoising/flow；文本输出是离散 token。若保持自回归文本头，两个时间方向和训练目标割裂。Uni‑ViGU 把 token embedding 连续化后做 discrete flow matching，使两种模态共享 \(\tau\in[0,1]\) 的去噪语言。", r"Figure 2 是最重要架构图：noisy video 与 noisy text 进入共享 self/cross-attention；video/text FFN 分支保持模态特异性，两个 head 分别输出 clean video manifold 与 token probability。"),
            sec("模型与方法", r"视频 latent 采用线性 interpolant \(z_{v,\tau}=(1-\tau)z_{v,0}+\tau z_{v,1}\) 并学习 velocity；文本 token 经 embedding 后采用相同形式，但最终由 text head 产生类别概率。设置 \((\tau_v,\tau_t)=(1,0)\) 做理解，\((0,1)\) 做生成。", r"modality-driven MoE 共享 attention、分离 video/text FFN。训练分两阶段：Knowledge Recall 用 10K video-prompt pairs 重构 prompt；Capability Refinement 再用 10K video-prompt-detailed-caption triples，迫使模型从视频恢复更丰富语义。"),
            sec("核心结果与证据", r"Figure 2 表明统一点不是把两个模型拼接，而是共享 attention 中的双向条件交换：video latent 约 30K tokens，text 仅 256 tokens，因此损失权重取 \(\lambda_t=|z_v|/|z_t|\) 平衡梯度。", r"训练从 Wan2.1 初始化，Stage 1 为 40K steps、learning rate \(2\times10^{-4}\)；Stage 2 为 60K steps、\(5\times10^{-5}\)，Adam \((\beta_1,\beta_2)=(0.90,0.95)\)，总成本为 16 张 H800、一周以内。", r"论文呈现 Figure 3 的 joint video-text qualitative examples，并声称 generation 与 understanding 均具竞争力；但正文没有给出标准 benchmark 表或可复核的数值比较。因此证据支持“可运行原型与定性联合生成”，不支持量化 SOTA 结论。"),
            sec("有效性与局限", r"两阶段数据由 state-of-the-art video generators 合成，再由 LLM 生成 detailed captions；这能控制 prompt/caption 长度，却可能继承生成器和 LLM 偏差。10K+10K 数据规模小，模型是否泛化到真实长视频、开放问答和细粒度时序推理未被量化。", r"Figure 3 文本存在明显不流畅片段；缺少 benchmark table、baseline、seed、variance 和消融，使“competitive”无法独立核验。生成与理解共享 flow 的机制合理，但训练成本和推理 latency 也未与双塔系统做公平比较。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2604.08121；项目页与代码：https://fr0zencrane.github.io/uni-vigu-page/。全文 14 页，PDF SHA-256：ca69b148b9f383c1a0e0f2af9bddb5424bf04718c95143c46a4ec551738ad606。", r"复现需固定 Wan2.1 checkpoint、VAE/UMT5、video resolution/frames、token lengths、10K+10K construction pipeline、condition dropout、MoE initialization、loss weighting、ODE solver、CFG、seeds 与 evaluation protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2，追踪 video/text 两条 flow 在 shared attention 的交换；再读 Sections 3.1–3.3 的 continuous/discrete flow、MoE 与两阶段训练。最后看 Section 4 和 Figure 3，并把 architecture feasibility、qualitative samples 与 benchmark-level evidence 分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2604.08121/figure-2-univigu-framework.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "连续视频 flow 与离散文本 flow 在共享 Transformer 中联合去噪。", "caption": "共享 attention 联结两种模态，分离 FFN 保留视频和文本的生成专长。", "selection_rationale": "Figure 2 同时展示输入输出、共享 attention 与模态分支，是全文最重要的机制图，优先于定性样例。"},
        "figure_refs": [figure("2604.08121", "figure-2-univigu-framework.webp", "Figure 2", 4, "unified architecture", "视频与文本联合 flow matching 架构。", "Uni‑ViGU 的共享 attention 与双 head。", "Continuous video transport and token-space text transport share attention but retain modality-specific feed-forward experts.")],
        "equation_refs": [
            {"label": "Continuous video flow", "latex": r"z_{v,\tau}=(1-\tau)z_{v,0}+\tau z_{v,1},\qquad u_v=z_{v,1}-z_{v,0}", "role": "video latent transport", "symbols": {"z_v0": "Gaussian video latent", "z_v1": "clean encoded video"}, "evidence": "paper.pdf p. 4, Eq. (6)", "interpretation": "An ODE integrates the learned velocity from noise to the video latent manifold."},
            {"label": "Token-count loss balance", "latex": r"\mathcal L=\lambda_v\mathcal L_v+\lambda_t\mathcal L_t,\qquad \lambda_v=1,\quad \lambda_t=|z_v|/|z_t|", "role": "balance video and text gradients", "symbols": {"z_v": "video token sequence", "z_t": "text token sequence"}, "evidence": "paper.pdf pp. 6–7, training setup", "interpretation": "The much shorter text sequence receives a compensating weight."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–7: Figure 2, uni-flow, MoE and two-stage training", "paper.pdf pp. 7–8: data, compute and qualitative joint generation", "paper.pdf p. 8, Figure 3: qualitative outputs", "source PDF SHA-256 ca69b148b9f383c1a0e0f2af9bddb5424bf04718c95143c46a4ec551738ad606", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2605.14675", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2605.14675",
        "title_en": "Agentic AI in Industry: Adoption Level and Deployment Barriers",
        "title_zh": "工业界 Agentic AI：采用成熟度与部署障碍",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["3454844f3a50a629"], ["AI Agents"]),
        "verified_metadata": meta("2605.14675", "v1", "Agentic AI in Industry: Adoption Level and Deployment Barriers", ["Spyridon Alvanakis Apostolou", "Jan Bosch", "Helena Holmström Olsson"], ["cs.SE"], "cs.SE", "2026-05-14T10:34:59Z", "Interviews with sixteen practitioners across twelve companies identify low production maturity and a capability-deployment verification gap shaped by context, proprietary knowledge, nondeterminism and confidentiality."),
        "sections": [
            sec("作者信息", r"作者：Spyridon Alvanakis Apostolou、Jan Bosch、Helena Holmström Olsson；arXiv:2605.14675v1。全文 17 页。研究是 \(N_p=16\) 位从业者、\(N_c=12\) 家公司的半结构化访谈，不是随机抽样调查。"),
            sec("研究问题", r"Agentic AI 的 demo capability 与工业 production deployment 之间差多少？作者问：12 家公司的成熟度分布怎样；哪些障碍阻止 agents 从个人助手升级为负责完整任务或多 agent orchestration 的生产系统？"),
            sec("背景", r"论文采用六级 AI-driven organization maturity framework。这里的 level 是组织流程集成程度，不是模型智力评分：Level 1 提供 assistants，Level 2 让 agents 承担局部任务，Level 3 出现 multi-agent orchestration；更高等级要求更深组织闭环。", r"原文只有表格，没有机制示意或可视化 Figure；按 v2.3 用题目和经全文核验的摘要作封面，不把成熟度表包装成视觉机制图。"),
            sec("模型与方法", r"访谈分四部分并采用 adaptive routing；16 份 transcript 被逐份结构化总结，barriers 经多轮归类直到稳定。作者用本地模型辅助摘要，但要求回查原始 transcript；公司、行业、规模、监管状态和 maturity level 组成 cross-case matrix。", r"样本覆盖 12 家不同规模/领域公司，其中若干受 safety/security regulation。分析聚焦受访者报告的实际 workflow、实验 capability、生产集成和 verification practices，而非厂商自报 benchmark。"),
            sec("核心结果与证据", r"成熟度计数为 \((N_{L1},N_{L2},N_{L3})=(7,4,1)\)，Levels 0、4、5 均为零。四家公司虽实验了更高一级 capability，却未进入 production，形成作者所称 capability–deployment verification gap。", r"Table 4 显示 context management 被 11/12 公司报告；所有使用 proprietary languages/protocols 的 C5、C6、C7、C8、C12 都报告模型欠拟合。所有 Level 2 公司认为至少 verification 环节必须 human-in-the-loop。", r"四类障碍是：跨 code/docs/regulation 的 context fragmentation；proprietary content underperformance；non-determinism 与 qualification 不兼容；data confidentiality。作者将前三者归纳为 information asymmetry 与 qualification absence 两个相互依赖维度。"),
            sec("有效性与局限", r"优点是跨公司访谈把“模型能力”和“可部署性”拆开，并报告具体缓解手段：RAG/graph retrieval、local/cloud separation、static analysis、tests 和 sandboxing。结果对 safety-critical software workflow 有直接启发。", r"但 12 家公司是小型目的样本，行业、地区和角色分布限制外推；访谈存在 recall/social-desirability bias，成熟度分级与 barrier coding 也依赖研究者判断。计数不能估计整个工业界采用率，相关性也不证明监管导致或阻止成熟度。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2605.14675。全文 17 页，PDF SHA-256：8a6a665cef66598a998e3b2d57dafce4340c28e5ea40aa82973676bdde19ec0f。出于匿名性，原始 transcripts 仅研究团队可访问。", r"复核需获得 interview guide、adaptive routing、company inclusion criteria、maturity coding rules、barrier codebook、双人复核/分歧处理、模型辅助摘要 prompts 与匿名化 cross-case matrix。", r"Evidence status: full-text verified qualitative study; no independent reproduction performed."),
            sec("阅读指南", r"先读 Table 1 的 maturity definitions，再读 Table 3 的 7/4/1 分布；随后看 Table 4 与 Sections 4.3–5 的 verification gap。最后读 validity threats，严格区分 interview evidence、作者归纳、总体采用率和因果主张。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "A qualitative interview study with sixteen practitioners across twelve companies finds that production use clusters at assistant and task-ownership levels. The central capability-deployment verification gap combines fragmented information access with absent qualification mechanisms, while proprietary content, nondeterminism and confidentiality further constrain deployment.", "selection_rationale": "论文没有 Figure，只有成熟度和 barrier 表格；按 v2.3 使用题目与经全文核验的摘要封面。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Study sample", "latex": r"N_{\rm practitioners}=16,\qquad N_{\rm companies}=12", "role": "qualitative evidence scope", "symbols": {"N_practitioners": "interview participants", "N_companies": "distinct companies"}, "evidence": "paper.pdf pp. 1, 5–6", "interpretation": "These counts define the case-study scope, not a population-representative survey."},
            {"label": "Observed maturity distribution", "latex": r"(N_{L1},N_{L2},N_{L3})=(7,4,1)", "role": "cross-case maturity count", "symbols": {"L1": "AI Assistants", "L2": "AI Compensators", "L3": "AI Superchargers"}, "evidence": "paper.pdf p. 7, Table 3", "interpretation": "Most sampled companies remain at assistant-level production integration."},
        ],
        "evidence_refs": ["paper.pdf pp. 5–7: interview design, sample and maturity coding", "paper.pdf pp. 10–14: verification gap and cross-case barriers", "paper.pdf p. 7, Table 3 and p. 11, Table 4", "source PDF SHA-256 8a6a665cef66598a998e3b2d57dafce4340c28e5ea40aa82973676bdde19ec0f", "Evidence status: full-text verified qualitative study; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2605.17781", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2605.17781",
        "title_en": "Universal interface fluctuations in absorbing-state phase transitions",
        "title_zh": "吸收态相变中的普适界面涨落",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "numerical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["32a8409016cbce3e"], ["Statistical Physics"]),
        "verified_metadata": meta("2605.17781", "v1", "Universal interface fluctuations in absorbing-state phase transitions", ["Yohsuke T. Fukai", "Keiichi Tamai", "Tetsuya Hiraiwa"], ["cond-mat.stat-mech", "nlin.CG", "q-bio.PE"], "cond-mat.stat-mech", "2026-05-18T02:59:54Z", "Numerics reveal a universal crossover from absorbing-transition interface fluctuations to long-time KPZ growth after rescaling by bulk correlation length and time."),
        "sections": [
            sec("作者信息", r"作者：Yohsuke T. Fukai、Keiichi Tamai、Tetsuya Hiraiwa；arXiv:2605.17781v1。主文 5 页并含 End Matter/Supplement，总 PDF 30 页。研究比较 DP 与 CDP 类的离散模型和 continuum sFKPP 方程。"),
            sec("研究问题", r"吸收态相变（APT）的 bulk critical fluctuations 与远离临界点的 KPZ moving-interface fluctuations 常在同一模型不同参数区出现。论文问：靠近临界点时，能否用 APT 的 \(\xi_\perp,\xi_\parallel\) 把二者连成一个普适 crossover scaling function？"),
            sec("背景", r"有 active boundary 时，active cluster 向 inactive region 侵入，最远 active site 定义界面高度 \(h(x,t)\)。临界点的时空尺度按 DP/CDP 指数发散；远离临界点，噪声 traveling front 预期进入 \((1+1)\)-dimensional KPZ 类。", r"Figure 1 同时给出 height definition、bond-percolation/biased-voter snapshots、mean density 与 height distributions，直观展示从稀疏临界 cluster 到 compact moving front 的演化。"),
            sec("模型与方法", r"continuum 模型为 stochastic FKPP：\(\partial_t\rho=D\nabla^2\rho+A\rho-B\rho^2+\sigma\sqrt{f(\rho)}\eta\)。DP 取 \(B=1,f=\rho\)；CDP 取 \(A=B=\epsilon,f=\rho(1-\rho)\)。离散对照是 bond percolation 与 biased voter/Domany–Kinzel model。", r"作者测量 \(\xi_\parallel\sim|\epsilon|^{-\nu_\parallel}\)、\(\xi_\perp\sim|\epsilon|^{-\nu_\perp}\)，再用 \(t_\xi=t/\xi_\parallel,x_\xi=x/\xi_\perp,h_\xi=h/\xi_\perp\) 重标，比较 mean、variance、skewness、kurtosis 和 height distributions。"),
            sec("核心结果与证据", r"Figure 1 显示界面 morphology 与密度/高度分布在 \(t\sim\xi_\parallel\) 附近改变；Figure 2 进一步表明不同 \(\epsilon\) 和离散/连续模型的 cumulants collapse 到同一 crossover curves。", r"短时 \(t_\xi\ll1\) 按 APT 动力学指数增长：\(\langle h_\xi^k\rangle_c\sim t_\xi^{k/z_{\rm APT}}\)；长时 \(t_\xi\gg1\) 的均值线性增长，higher cumulants 按 KPZ \(t_\xi^{k\beta_{\rm KPZ}}\) 且 \(\beta_{\rm KPZ}=1/3\)。skewness/kurtosis 趋向 flat-KPZ 的 GOE Tracy–Widom 值。", r"DP discrete/continuum 高度分布和 KPZ parameters 在误差内一致。CDP sFKPP 还保留 dimensionless \(D/\sigma^2\) 依赖；小 \(D/\sigma^2\) 极限恢复 biased voter model，说明该比值在二维是 marginal control parameter。"),
            sec("有效性与局限", r"跨离散与 continuum 实现的 collapse、短/长时极限和 distribution-shape 检查构成较强数值 universality evidence；但仍是有限尺寸/时间模拟，临界参数、threshold \(\rho_{th}\) 和 fitting windows 来自数值估计。", r"几何是 active-wall flat interface，尚未覆盖 curved geometry、其他 APT classes 或实验噪声。长时 KPZ regime 在 \(\epsilon\to0\) 时被发散 crossover time 推远；Supplement 的 convergence 与 parameter tables 必须一起检查。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2605.17781。PDF 30 页，SHA-256：32a8409016cbce3e95c118a19bb2657b42855b6dd1f91ec6228a29917dc6c9ee。", r"复现需固定 lattice geometry/size、active boundary、critical parameters、\(\Delta x=3\)、\(\Delta t=0.25\)、nonnegative sFKPP integrator、\(D,\sigma,\rho_b,\rho_{th}\)、epsilon grid、samples、fit windows 与 cumulant conventions。", r"Evidence status: full-text verified numerical study; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 建立界面定义；再读 Eqs. (1)–(3) 和 Figure 2 的 collapse。随后检查 Figure 3、Eq. (4) 的 KPZ parameterization 与 End Matter 的 Tables AI–AIII。最后用 Supplement 的 finite-size、threshold 和 fit-window tests 评估 universality claim。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2605.17781/figure-1-interface-growth.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "active boundary 界面、两类离散模型的演化快照及密度和高度分布。", "caption": "APT correlation scales 控制界面从临界 cluster 到移动 KPZ front 的 crossover。", "selection_rationale": "Figure 1 包含界面定义和真实演化快照，优先于纯 cumulant 数据图。"},
        "figure_refs": [figure("2605.17781", "figure-1-interface-growth.webp", "Figure 1", 3, "interface mechanism and snapshots", "active boundary、界面快照和高度分布。", "DP/CDP 界面生长的定义与定性 crossover。", "The snapshots show how the same rescaled interface changes from critical clusters to a compact moving front around the APT correlation time.")],
        "equation_refs": [
            {"label": "Stochastic FKPP field equation", "latex": r"\partial_t\rho=D\nabla^2\rho+A\rho-B\rho^2+\sigma\sqrt{f(\rho)}\,\eta", "role": "continuum absorbing-state model", "symbols": {"rho": "active density", "eta": "spatiotemporal white noise"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "DP and CDP are realized by different reaction and multiplicative-noise functions within one front equation."},
            {"label": "APT-to-KPZ cumulant crossover", "latex": r"\langle h_\xi^k\rangle_c\sim\begin{cases}t_\xi^{k/z_{\rm APT}},&t_\xi\ll1\\ t_\xi,&t_\xi\gg1,\ k=1\\ t_\xi^{k\beta_{\rm KPZ}},&t_\xi\gg1,\ k>1\end{cases}", "role": "universal crossover scaling", "symbols": {"t_xi": "time divided by APT correlation time", "beta_KPZ": "KPZ growth exponent, 1/3"}, "evidence": "paper.pdf p. 3, Eq. (3)", "interpretation": "Bulk critical dynamics controls short times, while long times recover KPZ interface growth."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: models, Figure 1, rescaling and cumulant collapse", "paper.pdf p. 4, Figures 2–3 and Eqs. (4)–(5)", "paper.pdf End Matter/Supplement: critical parameters, fit windows and robustness tests", "source PDF SHA-256 32a8409016cbce3e95c118a19bb2657b42855b6dd1f91ec6228a29917dc6c9ee", "Evidence status: full-text verified numerical study; no independent reproduction performed."],
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
