#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 018."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2505.13447", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2505.13447",
        "title_en": "Mean Flows for One-step Generative Modeling",
        "title_zh": "MeanFlow：用平均速度场实现一步生成",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["e1b182ad373c34ce"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2505.13447", "v1", "Mean Flows for One-step Generative Modeling",
            ["Zhengyang Geng", "Mingyang Deng", "Xingjian Bai", "J. Zico Kolter", "Kaiming He"],
            ["cs.LG", "cs.CV"], "cs.LG", "2025-05-19T17:59:59Z",
            "MeanFlow learns an average velocity field whose finite-time displacement directly maps noise to data in one or a few evaluations.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zhengyang Geng、Mingyang Deng、Xingjian Bai、J. Zico Kolter、Kaiming He；arXiv:2505.13447v1。全文 16 页。论文研究无需教师蒸馏的一步生成，其核心对象不是瞬时 probability-flow velocity，而是跨有限时间区间的平均速度。"),
            sec("研究问题", r"Flow matching 学到瞬时速度场后通常仍要数值积分许多步；把采样压到一次网络调用时，Euler 近似误差会成为主导。论文问：能否直接学习从时刻 \(t\) 到 \(r\) 的有限位移，使一步映射本身成为训练目标，同时仍与原始连续流严格相容？"),
            sec("背景", r"对连续轨迹 \(z_t\)，瞬时速度 \(v(z_t,t)=\mathrm d z_t/\mathrm dt\) 只描述局部切向量；一步生成需要的是端点差 \(z_r-z_t\)。MeanFlow 定义双时间平均速度 \(u(z_t,r,t)\)，满足 \(z_r=z_t+(r-t)u\)。这类似从微分方程的局部生成元转向有限时间 propagator。", r"Figure 5 展示 ImageNet-256 的 class-conditional curated samples。它直观说明一次函数求值可以产生结构清晰的图像，但该图经过挑选，只能作为感知质量示例；FID 与消融表才是总体分布的量化证据。"),
            sec("模型与方法", r"作者从平均速度的定义出发，对终止时间求导，得到连接 \(u\)、瞬时速度 \(v\) 与 Jacobian-vector product 的 MeanFlow identity。训练时网络预测 \(u_\theta(z,r,t)\)，target 由已知插值速度和对网络输出的方向导数组成；JVP 可用自动微分在一次联合计算中获得。", r"采样时若取 \(t=1,r=0\)，单次更新 \(z_0=z_1-u_\theta(z_1,0,1)\) 即完成 1-NFE 生成。多步采样则把时间区间分段，每段仍用平均速度更新。论文在 ImageNet-256 上使用 class conditioning、classifier-free guidance，并系统检查 time sampling、loss weighting、network size 与 NFE。"),
            sec("核心结果与证据", r"Figure 5 的可视化覆盖多种 ImageNet 类别；局部纹理和物体轮廓说明 1-NFE 输出没有出现普遍坍缩。必须同时读其 caption：这些是 curated examples，不能代替随机样本统计。", r"MeanFlow-XL/2 在 ImageNet 256×256、1 NFE 下报告 FID 3.43；对照的一步 Shortcut Models 为 10.60，iMM 为 7.77。使用两次函数求值的 MeanFlow-XL/2+ 报告 FID 2.20，与多步 DiT/SiT 结果处于相近量级。CIFAR-10 的 1-NFE FID 为 2.92。", r"JVP 并非免费：TPU v4-8 上训练迭代从普通 flow matching 的 0.045 s 增至 0.052 s，约 16% wall-clock overhead。论文的贡献因此是把采样积分成本转移为较小的训练微分成本，而不是消除计算。"),
            sec("有效性与局限", r"结果集中在 class-conditional ImageNet-256 与 CIFAR-10，并依赖特定 backbone、CFG、240-epoch training 和评估协议；不能直接外推到高分辨率、文本条件或科学场生成。FID 对 feature extractor 与 sample count 敏感，也不保证每类忠实度或 rare-mode coverage。", r"MeanFlow identity 在精确场上成立，但有限网络、有限数据和 JVP 估计会引入误差；一步端点拟合可能隐藏中间轨迹的不正确。Figure 5 是人工筛选图，不证明 1-NFE 在所有 prompts/classes 上优于多步 solver。本文未给出独立复现，训练成本、超参数与 accelerator 仍需对齐。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2505.13447；项目页：https://meanflows.com。全文 16 页，PDF SHA-256：322ba9244ad2c72382038e421fe0ffa92510c51d4f9c740bd7282b36bfc25206。", r"复现需固定 interpolation path、\((r,t)\) sampling、loss weighting、JVP implementation、network/EMA、CFG scale、training epochs、NFE grid、50k-sample FID protocol 与随机种子。应分别报告训练吞吐、1-NFE latency、FID 和随机未筛选样本。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Figure 2 的几何定义和 MeanFlow identity，再看算法框中的 JVP target；随后核对 ImageNet Table 1、ablation 与训练开销。最后查看 Figure 5，但把 curated visualization 与 FID 的总体统计证据分开，并检查一步映射是否保留所关心的中间动力学。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2505.13447/figure-5-meanflow-samples.webp", "label": "Figure 5", "visual_type": "comparison", "evidence": "paper.pdf p. 16, Figure 5", "alt_text": "MeanFlow-XL/2 一步生成的多类别 ImageNet-256 curated samples。", "caption": "一次网络求值可产生结构清晰的 ImageNet 样本；这是作者筛选的可视化，定量结论应结合 FID。", "selection_rationale": "Figure 5 是全文最重要且最直观的生成结果，优先于纯数据表；caption 明确保留 curated 边界。"},
        "figure_refs": [figure("2505.13447", "figure-5-meanflow-samples.webp", "Figure 5", 16, "show representative one-step generations", "MeanFlow-XL/2 在 ImageNet-256 上的一步生成样本。", "The samples show that a finite-time average-velocity map can generate coherent images in one evaluation.", "The examples are curated and do not establish distribution-wide quality without FID and random-sample audits.")],
        "equation_refs": [
            {"label": "Finite-time average velocity", "latex": r"u(z_t,r,t)=\frac{z_r-z_t}{r-t},\qquad z_r=z_t+(r-t)u(z_t,r,t)", "role": "replace numerical integration by a finite-time displacement", "symbols": {"z_t": "state at source time", "r,t": "endpoint and source times", "u": "average velocity"}, "evidence": "paper.pdf pp. 3–4", "interpretation": "At r=0 and t=1, a learned average velocity directly maps a noise sample to the data endpoint."},
            {"label": "MeanFlow identity", "latex": r"u=v-(t-r)\frac{\mathrm d u}{\mathrm d t},\qquad \frac{\mathrm d u}{\mathrm d t}=\partial_tu+v\cdot\nabla_zu", "role": "construct a self-consistent training target", "symbols": {"v": "instantaneous flow velocity", "du/dt": "total derivative along the flow"}, "evidence": "paper.pdf pp. 4–5", "interpretation": "The JVP term connects the finite-time field to the local flow without teacher distillation."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: average-velocity definition, identity and training algorithm", "paper.pdf pp. 8–16: ImageNet/CIFAR results, ablations and curated samples", "source PDF SHA-256 322ba9244ad2c72382038e421fe0ffa92510c51d4f9c740bd7282b36bfc25206", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2505.18647", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2505.18647",
        "title_en": "STFlow: Data-Coupled Flow Matching for Geometric Trajectory Simulation",
        "title_zh": "STFlow：面向几何轨迹模拟的数据耦合流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["1fc69cf0b30d65c8"], ["Flow Matching"]),
        "verified_metadata": meta("2505.18647", "v3", "STFlow: Data-Coupled Flow Matching for Geometric Trajectory Simulation", ["Kiet Bennema ten Brinke", "Koen Minartz", "Vlado Menkovski"], ["cs.LG", "cs.AI"], "cs.LG", "2025-05-24T09:46:55Z", "A data-coupled flow-matching model combines a conditional prior with spatial message passing and temporal convolutions for geometric trajectory forecasting."),
        "sections": [
            sec("作者信息", r"作者：Kiet Bennema ten Brinke、Koen Minartz、Vlado Menkovski；arXiv:2505.18647v3。全文 23 页。STFlow 面向带粒子置换与欧氏几何结构的时空轨迹，实验覆盖 N-body、MD17 分子动力学和 NBA 球员轨迹。"),
            sec("研究问题", r"标准 conditional flow matching 常从与观测轨迹无关的 Gaussian prior 出发，生成器必须同时学习全局位移、几何约束和时间关联。论文问：若把条件初态直接耦合进 prior，并在网络中分开建模空间相互作用与时间传播，能否用很少的 NFE 生成更准确的未来轨迹？"),
            sec("背景", r"轨迹张量可视为 \(T\times N\times d\) 的时空场：时间轴承载动力学关联，粒子轴需要 permutation equivariance，坐标轴还受平移/旋转结构约束。Figure 1 将三部分放在一起：由 observed prefix 构造 data-coupled noise、沿 flow 插值、再用 spatial message passing 与 temporal convolution 预测速度。"),
            sec("模型与方法", r"先从条件轨迹 \(x_{0:c}\) 计算均值延拓 \(m(x_{0:c})\)，构造 \(x_0=m(x_{0:c})+\zeta\) 的条件 prior；因此 flow 不必从空间原点附近搬运整条 future。训练使用 conditional flow matching，在随机时间拟合连接 prior sample 与真实未来 \(x_1\) 的 vector field。", r"网络在每个时刻用几何 message passing 处理粒子相互作用，再用 temporal convolutions 交换相邻帧信息。设计保持粒子重标号下的 equivariance，并支持不同 conditioning horizon。推断用固定步 ODE solver；N-body 主要结果仅用 5 NFEs。"),
            sec("核心结果与证据", r"Figure 1 解释了增益来源：conditioned prior 已包含观测末态的平移与粗趋势，flow 主要修正交互诱导的弯曲和多模态残差；时空网络则把对称性约束施加在正确轴上。", r"在 N-body benchmark 上，论文相对此前最佳平均降低 48.1% ADE 与 56.9% FDE；同时相对 LaM-SLidE 使用约一半 NFE，相对 GeoTDM 少约 200 倍 NFE。MD17 使用 8 种分子、30 帧轨迹和 10 帧 conditioning，并报告多分子上的竞争性位移误差。", r"NBA 结果并非全面占优：在一种 protocol 下 STFlow 的 mean20 指标有优势，但 min20 指标和另一设置中存在被 baseline 超过的项目。这个混合结果说明 data coupling 更直接改善平均预测，不自动保证多样本 oracle-best trajectory。"),
            sec("有效性与局限", r"ADE/FDE 是坐标误差，不检查能量守恒、symplectic structure、碰撞稳定性或正确的长期不变测度。N-body 与短 MD17 windows 距离真实长时分子动力学仍很远；NBA 的观测噪声、战术多模态与数据切分也会改变结果。", r"data-coupled prior 使用观测状态，提升来自更好的 conditional initialization、架构与训练目标的组合，当前消融不能对所有数据集唯一分离三者。5-NFE 效率依赖 solver、batch 与硬件；混合 NBA 结果限制了“普遍优于”的表述。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2505.18647。全文 23 页，PDF SHA-256：9b75706f09235a08e0e8b489d58db20fa540a6f2a89b23d91925b6d8a7578539。", r"复现需固定 trajectory split、conditioning/prediction lengths、coordinate normalization、prior mean construction、noise scale、message-passing graph、temporal kernel、ODE solver/NFE、五样本或二十样本聚合规则以及 ADE/FDE 单位。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，逐块确认 data coupling、spatial equivariance 与 temporal mixing；再读 conditional prior 和 vector-field parameterization。随后按 N-body、MD17、NBA 三组表分别检查 horizon、NFE 和 mean/min 指标，最后把短时几何预测与物理守恒的长期模拟分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2505.18647/figure-1-stflow-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "STFlow 从观测轨迹构造耦合 prior，再以空间消息传递和时间卷积生成未来轨迹。", "caption": "把 observed prefix 写入 prior 后，flow 主要学习相互作用引起的条件残差，而非从无结构噪声重建整条轨迹。", "selection_rationale": "Figure 1 同时展示 prior、flow 与时空网络，是全文最重要的机制图。"},
        "figure_refs": [figure("2505.18647", "figure-1-stflow-overview.webp", "Figure 1", 3, "explain the data-coupled spatiotemporal generator", "Observed trajectory, coupled prior, flow path and spatiotemporal network blocks.", "Conditioning is injected both through the prior and through the equivariant vector field.", "The schematic does not by itself demonstrate physical conservation or long-horizon stability.")],
        "equation_refs": [
            {"label": "Data-coupled prior", "latex": r"x_0=m(x_{0:c})+\zeta,\qquad \zeta\sim\mathcal N(0,\sigma^2I)", "role": "center the generative source on the observed trajectory", "symbols": {"m": "conditional trajectory extrapolator", "c": "conditioning endpoint", "zeta": "residual noise"}, "evidence": "paper.pdf pp. 4–5", "interpretation": "The flow transports a conditional residual rather than an unconditional Gaussian trajectory."},
            {"label": "Average displacement error", "latex": r"\operatorname{ADE}=\frac{1}{N(T-c)}\sum_{t=c+1}^{T}\sum_{i=1}^{N}\|\hat x_i^t-x_i^t\|_2", "role": "measure mean future-coordinate error", "symbols": {"N": "particles or agents", "T-c": "prediction horizon"}, "evidence": "paper.pdf p. 7", "interpretation": "ADE averages geometric error but does not test conservation laws or calibrated trajectory probabilities."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: coupled prior, spatiotemporal architecture and metrics", "paper.pdf pp. 7–14: N-body, MD17 and NBA comparisons", "source PDF SHA-256 9b75706f09235a08e0e8b489d58db20fa540a6f2a89b23d91925b6d8a7578539", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2505.18825", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2505.18825",
        "title_en": "How to build a consistency model: Learning flow maps via self-distillation",
        "title_zh": "如何构建一致性模型：用自蒸馏学习流映射",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["ae6b8a193d3649c7"], ["Flow Matching"]),
        "verified_metadata": meta("2505.18825", "v2", "How to build a consistency model: Learning flow maps via self-distillation", ["Nicholas M. Boffi", "Michael S. Albergo", "Eric Vanden-Eijnden"], ["cs.LG", "cs.CV"], "cs.LG", "2025-05-24T16:56:10Z", "A two-time flow-map framework derives and compares Eulerian, Lagrangian and progressive self-distillation methods for consistency models."),
        "sections": [
            sec("作者信息", r"作者：Nicholas M. Boffi、Michael S. Albergo、Eric Vanden-Eijnden；arXiv:2505.18825v2。全文 31 页。论文把多种 consistency/self-distillation 方法统一为学习双时间 flow map 的数值问题，并给出低维与 64×64 图像实验。"),
            sec("研究问题", r"Flow/score model 学的是瞬时速度，采样仍需积分；consistency model 试图直接学习有限时间映射，却有多套看似不同的 teacher、EMA 与 bootstrapping 规则。论文问：这些算法能否从 flow map 的半群性质和 tangent condition 统一推导，并明确不同离散化的稳定性—偏差权衡？"),
            sec("背景", r"确定性 ODE 的两时间 flow map \(X_{s,t}(x)\) 把时刻 \(t\) 的状态送到 \(s\)。它满足 identity、composition 和切向条件。Figure 1 先画两时间曲面及 tangent constraint，再用 Gaussian handshake 展示如何把不同 self-distillation families 放进同一实验坐标系。"),
            sec("模型与方法", r"作者从 flow-map evolution equations 构造四类离散训练：Eulerian self-distillation 在固定空间点比较相邻时间映射；Lagrangian self-distillation 沿估计轨迹搬运输入；progressive self-distillation 则逐级压缩 solver steps，并区分 uniform 与 midpoint variants。", r"teacher 由 velocity model 或当前 flow-map network 的停止梯度/EMA 副本给出。训练不只要求端点一致，还要求 map composition 与局部 tangent 相容。统一 notation 暴露了误差来源：teacher solver truncation、student regression、off-manifold evaluation 和递归 bootstrapping。"),
            sec("核心结果与证据", r"Figure 1 的价值是把 consistency model 还原为数值流映射：同一 \(X_{s,t}\) 可沿 Eulerian 或 Lagrangian 路径约束；Gaussian handshake 提供匹配 training budgets 的比较协议，而非把算法名字当作机制。", r"在 CelebA-64 上，Lagrangian self-distillation 在所有测试步数中取得表内最佳 FID，1-step FID 为 12.22；在 AFHQ-64 上 LSD 从 1-step FID 11.19 改善到 16-step 的 5.61。checkerboard toy problem 中 LSD 除 16-step 外也给出最低 KL。", r"这些结果支持 Lagrangian evaluation 减少 distribution mismatch，但论文明确不以 SOTA 为目标。数据规模、网络与训练预算有限，因此更可靠的结论是设计空间与优化行为，而不是某个缩写对所有生成任务普遍最优。"),
            sec("有效性与局限", r"自蒸馏 target 依赖 teacher trajectory；若初始 velocity/flow map 有系统误差，composition 可把误差固化。有限步 solver、EMA lag、stop-gradient 和 time-pair sampling 都影响稳定性，理论 identity 本身不保证 neural optimization 收敛。", r"实验主要是 checkerboard、CelebA-64 与 AFHQ-64，分辨率和规模不足以确定现代高分辨率生成的排序。FID 随 step count 改善说明模型仍非完美一致；one-step quality、multi-step correctability 与真实 ODE fidelity 是不同指标。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2505.18825。全文 31 页，PDF SHA-256：523ae498a8c5db38db2975091ae474d4b8f858a0ffcd194d9b57e46393899d92。", r"复现需固定 base velocity model、\((s,t)\) sampling、teacher solver 与步长、EMA、stop-gradient location、self-distillation family、training evaluations、FID sample count 和 checkerboard KL estimator。应保存每个 NFE 的 checkpoint，而非只报最佳点。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 flow-map 三条代数性质；再按 Eulerian、Lagrangian、progressive 三组算法逐行比较 target 的 evaluation point。随后读 Table 1 的同预算结果与优化曲线，最后检查 appendix 的实现细节，区分解析恒等式、离散算法和经验排序。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2505.18825/figure-1-flowmap-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "双时间 flow map、tangent condition 与 Gaussian handshake 的统一示意图。", "caption": "Consistency training 可视为直接逼近满足切向与复合关系的有限时间 flow map。", "selection_rationale": "Figure 1 是全文统一理论与比较协议的核心机制图，优先于单一 FID 表。"},
        "figure_refs": [figure("2505.18825", "figure-1-flowmap-overview.webp", "Figure 1", 2, "unify consistency models as flow-map learning", "Two-time flow-map surface, tangent relation and Gaussian comparison handshake.", "Eulerian, Lagrangian and progressive targets discretize constraints on the same flow map.", "Exact flow-map identities do not guarantee stable finite-network self-distillation.")],
        "equation_refs": [
            {"label": "Flow-map composition", "latex": r"X_{s,t}=X_{s,r}\circ X_{r,t},\qquad X_{t,t}=\operatorname{Id}", "role": "state the semigroup consistency constraint", "symbols": {"X_s,t": "map from time t to time s", "r": "intermediate time"}, "evidence": "paper.pdf pp. 2–3", "interpretation": "A learned finite-time map should agree whether transport is performed directly or through an intermediate time."},
            {"label": "Tangent condition", "latex": r"\left.\partial_sX_{s,t}(x)\right|_{s=t}=v_t(x)", "role": "connect the finite flow map to the instantaneous velocity", "symbols": {"v_t": "probability-flow vector field", "x": "state at time t"}, "evidence": "paper.pdf p. 3, Lemma 2.1", "interpretation": "Local agreement with the vector field anchors self-distillation to the underlying continuous dynamics."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–9: flow-map identities and self-distillation families", "paper.pdf pp. 12–20: checkerboard, CelebA and AFHQ comparisons", "source PDF SHA-256 523ae498a8c5db38db2975091ae474d4b8f858a0ffcd194d9b57e46393899d92", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.01337", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2506.01337",
        "title_en": "NoiseAR: AutoRegressing Initial Noise Prior for Diffusion Models",
        "title_zh": "NoiseAR：为扩散模型自回归生成初始噪声先验",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["a619bd5c2964e92c"], ["Generative Models"]),
        "verified_metadata": meta("2506.01337", "v1", "NoiseAR: AutoRegressing Initial Noise Prior for Diffusion Models", ["Zeming Li", "Xiangyue Liu", "Xiangyu Zhang", "Ping Tan", "Heung-Yeung Shum"], ["cs.LG", "cs.AI"], "cs.LG", "2025-06-02T06:58:46Z", "NoiseAR replaces the fixed Gaussian start of a text-to-image diffusion model with a prompt-conditioned autoregressive distribution over latent-noise patches."),
        "sections": [
            sec("作者信息", r"作者：Zeming Li、Xiangyue Liu、Xiangyu Zhang、Ping Tan、Heung-Yeung Shum；arXiv:2506.01337v1。全文 21 页。NoiseAR 是可插接既有 text-to-image diffusion models 的条件 prior learner，并用 DPO 做小规模 preference fine-tuning。"),
            sec("研究问题", r"扩散模型通常从与 prompt 无关的各向同性 Gaussian \(z_T\) 出发，条件信息只在 denoising 途中注入。论文问：若直接学习 \(p(z_T\mid c)\)，让初始噪声已经携带与文本有关的空间结构，是否能在不改 downstream diffusion model 的情况下提高 alignment 与感知质量？"),
            sec("背景", r"反演真实图像可得到与该图/文本匹配的“golden noise”，说明固定 Gaussian 中不同点并非同等适合某一 prompt。但直接回归单个 noise 会丢失多样性。NoiseAR 将 latent noise 切成 patches，并把条件 prior 写成自回归联合分布，从而同时保留概率采样和 prompt dependence。", r"Figure 2 将同一 prompt 下的 Origin Noise、Golden Noise、NoiseAR 与 NoiseAR+DPO 结果并列。它能展示构图/语义差异，但仍是少量可视化；跨数据集的多指标表才支持平均改善。"),
            sec("模型与方法", r"先用预训练 diffusion model 对图文对执行 inversion，收集 \((z_T,c)\) cold-start pairs。Transformer 按空间 patch 顺序建模 \(p_\theta(z_T\mid c)=\prod_jp_\theta(z_{T,j}\mid z_{T,<j},c)\)，每个位置输出连续 noise patch 的条件分布；推断时逐 patch 采样，再交给冻结的 SDXL、DreamShaper 或 Hunyuan-DiT 去噪。", r"因为 prior 显式给出 log probability，作者把 patch sequence 看作 policy trajectory，用 2,000 个 Pick-a-Pic prompts、每 prompt 20 rollouts 构造 preferred/rejected pairs，并做 DPO。该阶段优化的是自动指标合成的 preference，而非直接人类 pairwise labels。"),
            sec("核心结果与证据", r"Figure 2 中 NoiseAR 相比原始 Gaussian 往往给出更完整的主体与更匹配的布局；DPO 后若干例子进一步改善语义对齐。图像只是代表性案例，不能单独证明总体优势。", r"Table 1 在 DrawBench、Pick-a-Pic 与 GenEval 上比较三种 downstream models。以 DrawBench+SDXL 为例，NoiseAR 的 HPSv2 27.86、PickScore 58.06、ImageReward 75.99、CLIPScore 84.27，高于标准 Gaussian 对应的 26.78、46.31、52.74、83.34，也总体超过 Golden Noise。其他模型/数据集多数指标同样提高，但幅度随 metric 改变。", r"DPO 是 proof of concept：它把 SDXL+DrawBench 的 ImageReward 从约 76.00 进一步推高，但训练偏好来自 HPS/PickScore/ImageReward/MPS 的组合。改进因此是对这些 proxy 的优化，是否等价于人类长期偏好仍需独立评测。"),
            sec("有效性与局限", r"初始 noise pairs 来自特定 inversion 和 downstream diffusion models，可能把生成器偏差写进 prior。patch factorization 引入顺序与分辨率选择；更强 prior 也可能降低 diversity 或复制训练图结构，文中指标不足以完整审计 memorization 和 mode coverage。", r"作者明确未研究 model/data scaling law，DPO 仅初步验证，也未系统组合 advanced samplers 或后期 noise search。实验局限于 text-to-image，没有覆盖 audio、video 或 3D。Figure 2 的成功样例不能代替随机 prompt、失败样例与人类盲评。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.01337。全文 21 页，PDF SHA-256：13b1bcbb9df4afb2dcd018ccb73467c41b1836fdb4f52b3308e7510c5995aa74。", r"复现需固定 inversion method、cold-start dataset、latent VAE、patch size/order、distribution parameterization、Transformer depth、sampling temperature、downstream checkpoint、seed、prompt sets 与指标版本。DPO 还需保存 2,000 prompts、20 rollouts、proxy merge rule 和 pair selection。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 的数据构造与 AR prior，再看 Figure 2 形成直觉；随后逐列核对 Table 1，避免只挑一个 metric。最后读 patch/depth ablations、DPO 数据生成和 limitations，把“更好的初始条件”“更强的最终生成器”与“对 proxy reward 的适配”分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.01337/figure-2-noisear-comparison.webp", "label": "Figure 2", "visual_type": "comparison", "evidence": "paper.pdf p. 9, Figure 2", "alt_text": "标准噪声、Golden Noise、NoiseAR 和 NoiseAR+DPO 在相同文本提示下的生成图比较。", "caption": "Prompt-conditioned initial noise 能在去噪前重排空间结构；可视化趋势需与跨 prompt 指标和多样性审计一起解读。", "selection_rationale": "Figure 2 是最直观的原文结果图，能用图像替代冗长的样例描述。"},
        "figure_refs": [figure("2506.01337", "figure-2-noisear-comparison.webp", "Figure 2", 9, "compare initial-noise strategies visually", "Rows compare Origin Noise, Golden Noise, NoiseAR and NoiseAR with DPO.", "A learned prompt-conditioned prior changes composition before the frozen diffusion denoiser acts.", "Selected examples do not quantify diversity, memorization or average human preference.")],
        "equation_refs": [
            {"label": "Autoregressive noise prior", "latex": r"p_\theta(z_T\mid c)=\prod_{j=1}^{J}p_\theta(z_{T,j}\mid z_{T,<j},c)", "role": "model prompt-conditioned initial noise patch by patch", "symbols": {"z_T,j": "latent-noise patch j", "c": "text condition", "J": "number of patches"}, "evidence": "paper.pdf pp. 4–5", "interpretation": "The Gaussian starting measure is replaced by a structured conditional distribution while retaining stochastic sampling."},
            {"label": "DPO prior objective", "latex": r"\mathcal L_{\rm DPO}=-\mathbb E\log\sigma\!\left(\beta\log\frac{\pi_\theta(z^+\mid c)}{\pi_{\rm ref}(z^+\mid c)}-\beta\log\frac{\pi_\theta(z^-\mid c)}{\pi_{\rm ref}(z^-\mid c)}\right)", "role": "prefer initial noises that yield higher-scoring images", "symbols": {"z+": "preferred noise rollout", "z-": "rejected rollout", "beta": "preference strength"}, "evidence": "paper.pdf pp. 7–8", "interpretation": "Optimization acts on the prior likelihood ratio; its semantics are inherited from the proxy used to form preference pairs."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: inversion pairs and autoregressive prior", "paper.pdf pp. 7–10: multi-model evaluation, DPO and visual comparison", "source PDF SHA-256 13b1bcbb9df4afb2dcd018ccb73467c41b1836fdb4f52b3308e7510c5995aa74", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.09985", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2506.09985",
        "title_en": "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning",
        "title_zh": "V-JEPA 2：自监督视频模型连接理解、预测与规划",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["002e259088de9677"], ["World Models"]),
        "verified_metadata": meta("2506.09985", "v1", "V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning", ["Mahmoud Assran", "Adrien Bardes", "David Fan", "Quentin Garrido", "Russell Howes", "Mojtaba Komeili", "Matthew Muckley", "Ammar Rizvi", "Claire Roberts", "Koustuv Sinha", "Artem Zholus", "Sergio Arnaud", "Abha Gejji", "Ada Martin", "Francois Robert Hogan", "Daniel Dugas", "Piotr Bojanowski", "Vasil Khalidov", "Patrick Labatut", "Francisco Massa", "Marc Szafraniec", "Kapil Krishnakumar", "Yong Li", "Xiaodong Ma", "Sarath Chandar", "Franziska Meier", "Yann LeCun", "Michael Rabbat", "Nicolas Ballas"], ["cs.AI", "cs.CV", "cs.LG", "cs.RO"], "cs.AI", "2025-06-11T17:59:56Z", "Internet-scale joint-embedding video pretraining supports video understanding and an action-conditioned latent predictor for model-predictive robot control."),
        "sections": [
            sec("作者信息", r"作者：Mahmoud Assran、Adrien Bardes、David Fan 等 29 位作者；arXiv:2506.09985v1，FAIR at Meta 与 Mila/Polytechnique Montréal。全文 49 页。工作包含 action-free video pretraining、LLM alignment、action-conditioned post-training 和 Franka 机器人部署。"),
            sec("研究问题", r"世界模型若完全依赖机器人交互数据，规模受真实采集限制；像素级视频生成又把容量消耗在不可预测细节。论文问：能否先从海量无动作标签视频学到 latent predictive representation，再用少量 state-action videos 训练 action-conditioned predictor，并在新实验室中以目标图像规划？"),
            sec("背景", r"JEPA 不重建像素，而在 embedding space 预测被 mask 的未来/缺失区域，倾向保留可预测的物体与运动结构。Figure 1 把整个层级画出：1M 小时网络视频和 1M 图像产生 V-JEPA 2；language alignment/attentive probes 服务理解任务；少量 robot data 只训练 action-conditioned predictor，用于闭环规划。"),
            sec("模型与方法", r"第一阶段冻结式 target encoder 与 context encoder/predictor 进行 masked feature prediction，得到 action-free V-JEPA 2。理解任务用 attentive probe 或与 8B LLM 对齐，不重新定义底层视觉目标。", r"机器人阶段冻结 video encoder，在少于 62 h、约 23k 条 DROID trajectories 上训练自回归 V-JEPA 2-AC：给定当前 latent state、proprioception 与 candidate actions，预测未来 latent observations。控制时用 cross-entropy method 搜索 action sequence，使预测终态 embedding 接近人工提供的 goal image；执行首段动作后重新观测，构成 receding-horizon MPC。"),
            sec("核心结果与证据", r"Figure 1 显示 action-free observation learning 与 action-conditioned control 的明确分工：大规模 web data 提供视觉动力学表示，机器人数据只把 action 接到 frozen latent space 上。它是架构/数据流证据，不是所有能力由同一目标自动涌现的证明。", r"V-JEPA 2 在 Something-Something v2 报告 77.3 top-1，在 Epic-Kitchens-100 action anticipation 报告 39.7 recall-at-5；与 8B LLM 对齐后，PerceptionTest 为 84.0、TempCompass 为 76.9。各数字来自不同 probe/对齐协议，不能直接当作单一零样本能力。", r"V-JEPA 2-AC 在两个训练数据未覆盖的实验室、Franka arms 与低分辨率单目 RGB 上执行 reach、pick-and-place。reaching 的三项任务最终误差进入 4 cm 内且随 MPC rollout 下降；操作表按每项 10 trials 报告成功率。对照 Octo 使用超过 1M trajectories，Cosmos 使用约 20M 小时视频，而 V-JEPA 2-AC 的交互 post-training 约 23k trajectories，但预训练视频规模仍达 1M 小时。"),
            sec("有效性与局限", r"“zero-shot”指目标实验室未收集训练数据，并非没有机器人数据：模型仍用 DROID 的 Franka trajectories 做 action-conditioned post-training，且部署是同一机器人类型。pick-and-place 依赖人工给定中间 goal images，任务集合和每项 10 次 trials 都较小。", r"latent 距离是规划能量，不保证与物理可达性、安全、接触稳定或任务 reward 单调一致。CEM/MPC 计算成本、相机视角、遮挡和失败恢复限制实时性。benchmark 提升同时含数据规模、架构和训练 recipe，未由 matched ablation 唯一归因；这些结果也不足以证明通用物理世界模型。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.09985；代码：https://github.com/facebookresearch/vjepa2。全文 49 页，PDF SHA-256：9cfcfde5fb0d9730637da5b9e7317825c3f3d09e91f3553e22eeba42c74d2226。", r"复现需记录 video/image corpus、clip sampling、mask schedule、encoder size、probe/LLM alignment protocol、DROID subset、camera/proprio normalization、action horizon、predictor rollout、CEM population/elites/iterations、goal-image construction 与成功判据。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把 representation pretraining、language/probe evaluation 与 robot post-training 分开；再读 JEPA objective 和 V-JEPA 2-AC predictor。随后核对视频 benchmarks 的协议，再看 robot Tables 2–3、Figure 7 的误差轨迹和 appendix deployment details，重点审计 zero-shot 的精确定义与 10-trial uncertainty。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.09985/figure-1-vjepa2-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "互联网视频和图像预训练 V-JEPA 2，再经语言对齐、probe 或机器人 action-conditioned post-training 分流到理解、预测与规划。", "caption": "大规模 action-free 表征与小规模 action-conditioned post-training 被清楚分层；机器人规划不是单靠网络视频直接获得。", "selection_rationale": "Figure 1 是全文最重要且可视化最清晰的数据流/能力图，优先于单项 benchmark 曲线。"},
        "figure_refs": [figure("2506.09985", "figure-1-vjepa2-overview.webp", "Figure 1", 2, "show the staged data and capability pipeline", "Internet video pretraining branches into understanding tasks and robot action-conditioned post-training.", "Large-scale observation learning supplies a frozen latent space; robot trajectories attach actions for MPC planning.", "The diagram does not imply that action semantics or manipulation emerge without robot interaction data.")],
        "equation_refs": [
            {"label": "Latent action prediction", "latex": r"\hat z_{k+1:k+T}=P_\theta(a_{1:T};s_k,z_k)", "role": "predict future visual representations under candidate actions", "symbols": {"z_k": "current visual embedding", "s_k": "robot state", "a_1:T": "candidate action sequence"}, "evidence": "paper.pdf Section 4", "interpretation": "The predictor rolls dynamics forward in representation space rather than generating future RGB frames."},
            {"label": "Goal-conditioned planning energy", "latex": r"E(a_{1:T};z_k,s_k,z_g)=\|P_\theta(a_{1:T};s_k,z_k)-z_g\|_1", "role": "rank action sequences for model-predictive control", "symbols": {"z_g": "goal-image embedding", "E": "terminal latent distance"}, "evidence": "paper.pdf Section 4.2", "interpretation": "CEM searches for actions whose predicted terminal representation approaches the supplied visual goal."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–12: architecture, pretraining and video understanding", "paper.pdf pp. 20–31: action-conditioned predictor, MPC and robot experiments", "source PDF SHA-256 9cfcfde5fb0d9730637da5b9e7317825c3f3d09e91f3553e22eeba42c74d2226", "Evidence status: full-text verified; no independent reproduction performed."],
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
