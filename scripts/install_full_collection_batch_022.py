#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 022."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2512.18184", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2512.18184",
        "title_en": "Is There a Better Source Distribution than Gaussian? Exploring Source Distributions for Image Flow Matching",
        "title_zh": "图像流匹配中是否存在优于高斯的源分布？",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["dd2c72d8e038972e"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2512.18184", "v1",
            "Is There a Better Source Distribution than Gaussian? Exploring Source Distributions for Image Flow Matching",
            ["Junho Lee", "Kwanseok Kim", "Joonseok Lee"], ["cs.CV"], "cs.CV",
            "2025-12-20T02:44:54Z",
            "A high-dimensional geometric analysis explains why Gaussian sources remain robust and motivates norm-aligned training with directionally pruned inference.",
        ),
        "sections": [
            sec("作者信息", r"作者：Junho Lee、Kwanseok Kim、Joonseok Lee；arXiv:2512.18184v1。全文 29 页，发表于 TMLR（2025-12）。论文把 source-distribution design 拆成密度、方向和模长三个几何问题，并在 CIFAR-10 与 ImageNet-64 上验证。"),
            sec("研究问题", r"流匹配允许自由选择 source distribution，但标准各向同性 Gaussian 是否只是方便，还是高维几何下的稳健选择？论文问：让源分布逼近 target density、方向或模长，分别会怎样改变路径纠缠、mode coverage、有限 NFE 误差与生成质量？"),
            sec("背景", r"连续流以 ODE \(\dot x_t=v_t(x_t)\) 把 \(p_0\) 推到 \(p_1\)。高维 Gaussian 的半径集中在 \(\sqrt d\) 附近而方向近似均匀；因此“二维平面上的 Gaussian 云”不能同时表现径向集中和球面方向覆盖。", r"Figure 1(c) 把高维样本压到“方向角—模长”二维表示：黑点是 source，蓝点是 data，细线是 source–target transport。相较 Figure 1(a,b) 的普通二维玩具，它把方向覆盖、模长错配和 sparse angular sectors 可视化。"),
            sec("模型与方法", r"作者先证明 Gaussian 可等价写成独立的 \(\chi_d\) 半径与球面均匀方向，即 \(x_0=r u\)，\(r\sim\chi_d\)、\(u\sim\mathrm{Unif}(\mathbb S^{d-1})\)。随后分别构造 target-density approximation、vMF directional alignment、norm alignment 与 angular pruning，在 I-CFM/OT-CFM 下做消融。", r"最终策略训练时保留完整 Gaussian 的 omnidirectional supervision，并把 target 平均模长缩放到 source shell；推理时才删除数据稀疏或 mode-equidistant 的方向。pruned sampling 因而可直接用于既有 Gaussian-trained model，不需要重训。"),
            sec("核心结果与证据", r"Figure 1 的关键不是三幅漂亮轨迹，而是第三幅所暴露的高维约束：Gaussian shell 从所有方向提供监督；若方向分布过窄，多个 target modes 的路径在同一 angular sector 纠缠，局部 vector field 反而更难学。", r"逼近 target density 并不单调改善结果：CIFAR-10 上 Gaussian baseline FID 为 4.40，DCT-Weak 为 4.20，但 GMM-1/GMM-2/GMM-10 分别恶化到 11.75/12.49/12.11，CNF source 为 17.18。更“像数据”的 source 会因 mode discrepancy 与 sparse coverage 失去稳定监督。", r"hybrid Gaussian-train→Pruned-inference 在不同 NFE 上稳定优于完整或全程 pruned；ImageNet-64 的 FID 从 NFE 5/10/20/100 的 53.95/18.84/10.62/9.10 改善为 49.56/16.70/9.54/8.78。收益来自避开 poorly trained initial regions，而非证明 Gaussian 在所有任务上全局最优。"),
            sec("有效性与局限", r"核心机制来自作者设计的二维投影和有限数据集实验；它把高维方向与模长分离得很清楚，却不保留真实图像流形的全部 topology。FID 对特征空间和样本数敏感，不能单独判断 mode fidelity、likelihood 或语义覆盖。", r"pruning 依赖训练数据方向/聚类估计，可能删除 rare modes；norm alignment 使用全局平均半径，会掩盖 class-conditional 或 heavy-tailed radial structure。结论支持 Gaussian 的 robust baseline 地位，不构成不存在更优 task-specific source 的定理。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2512.18184；代码：https://github.com/kwanseokk/SourceFM。全文 29 页，PDF SHA-256：ab773183888f02162d4f4371209fb3038b24664171335dda56b8d4f802685804。", r"复现需固定 CIFAR-10/ImageNet-64 preprocessing、I-CFM/OT-CFM pairing、source estimator、vMF concentration \(\kappa\)、cluster count、angular pruning threshold、norm rescaling、ODE solver、NFE、FID implementation 与 seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把普通二维 toy 与 direction–norm projection 区分；再按 Figures 2–5 依次检查 density approximation、directional entanglement、Gaussian coverage 和 sparse-region failure。最后看 Tables 2–6，特别区分 training source 与 inference source。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2512.18184/figure-1-2d-simulations.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "三种二维流匹配模拟，第三幅把高维方向和模长几何投影到二维。", "caption": "高维 Gaussian 的价值在于球面方向的全面监督；只让源分布更接近数据并不保证更容易学习。", "selection_rationale": "Figure 1 是全文的几何直觉入口，比单个 FID 表更直接解释主要机制。"},
        "figure_refs": [figure("2512.18184", "figure-1-2d-simulations.webp", "Figure 1", 2, "visualize the high-dimensional direction–norm surrogate", "三幅 source–target transport 图比较普通二维玩具与高维几何代理。", "第三幅把 omnidirectional coverage、radial shell 和 path failures 放进同一图。", "This is a diagnostic surrogate, not an isometric embedding of an image manifold.")],
        "equation_refs": [
            {"label": "Gaussian radial-direction factorization", "latex": r"x_0=r u,\qquad r\sim\chi_d,\quad u\sim\operatorname{Unif}(\mathbb S^{d-1}),\quad r\perp u", "role": "separate norm and direction in the source", "symbols": {"d": "latent dimension", "r": "source norm", "u": "source direction"}, "evidence": "paper.pdf pp. 4–5, Section 3.1", "interpretation": "High-dimensional Gaussian mass occupies a thin radial shell while retaining nearly uniform angular coverage."},
            {"label": "Norm alignment", "latex": r"x_1'=x_1\,\frac{\mathbb E\lVert x_0\rVert}{\mathbb E\lVert x_1\rVert}", "role": "match average target and source radii during training", "symbols": {"x_0": "Gaussian source", "x_1": "data sample"}, "evidence": "paper.pdf p. 15, Section 5.4", "interpretation": "Removing a global radial mismatch shortens transport without sacrificing angular supervision."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–10: high-dimensional surrogate and five geometric findings", "paper.pdf pp. 11–16: CIFAR-10/ImageNet-64 source and pruning experiments", "source PDF SHA-256 ab773183888f02162d4f4371209fb3038b24664171335dda56b8d4f802685804", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2512.21075", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2512.21075",
        "title_en": "Feature Learning Dynamics in Infinite-Depth Neural Networks",
        "title_zh": "无限深神经网络中的特征学习动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["d65f26b6af5cd650"], ["Scaling Laws"]),
        "verified_metadata": meta(
            "2512.21075", "v3", "Feature Learning Dynamics in Infinite-Depth Neural Networks",
            ["Zihan Yao", "Ruoyu Wu", "Tianxiang Gao"], ["cs.LG", "cs.AI", "math.PR", "stat.ML"], "cs.LG",
            "2025-12-24T09:39:04Z",
            "A depth-muP limit suppresses reused-weight forward-backward coupling and yields a decoupled Neural Feature Dynamics SDE with nonlinear feature learning.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zihan Yao、Ruoyu Wu、Tianxiang Gao；arXiv:2512.21075v3。全文 43 页。论文研究 one-layer ResNet 在 depth-\(\mu\)P 参数化下的 width/depth 双极限，并用 CIFAR-10 SGD 实验检查理论速率。"),
            sec("研究问题", r"反向传播复用 forward matrix \(W_\ell\) 的转置 \(W_\ell^\top\)，因此 feature 与 gradient 并非独立 Gaussian。论文问：这类 forward–backward coupling 在 \(n\to\infty\)、\(L\to\infty\) 时是否消失；若消失，怎样仍保留训练产生的 feature–gradient alignment，而不退化成 lazy/kernel dynamics？"),
            sec("背景", r"depth-\(\mu\)P ResNet 把 layer time 写成 \(t_\ell=\ell/L\)，单层 residual increment 具有 \(1/\sqrt L\) 尺度，深度极限成为 SDE。困难在于同一随机矩阵同时进入前向与伴随反向方程，破坏 naive independence closure。", r"Figure 2 用实线/虚线分别比较 standard reused weights 与 independent backward initialization。只有 depth-\(\mu\)P 的第三列随着深度增加让两条训练和测试轨迹重合；这就是 gradient-independence ansatz（GIA）被深度恢复的直接证据。"),
            sec("模型与方法", r"作者在取任何极限前用 conditional Gaussian representation，把 reused-weight coupling 与 decoupled Gaussian fluctuation 显式分开。初始化时 coupling 为有限宽修正，uniformly over depth 按 \(O(n^{-1})\) 消失；训练后 SGD 会产生在 width limit 中仍存活的相关项。", r"关键是 depth-\(\mu\)P 将该训练相关项推到更高 depth order：逐层累积为 \(O(L^{-2})\)，而普通 SDE discretization error 是 \(O(L^{-1})\)。由此定义 Neural Feature Dynamics（NFD）：backward noise 与 forward noise 解耦，但 covariance 通过 feature–gradient statistics 自洽演化。"),
            sec("核心结果与证据", r"Figure 2 显示 vanilla DNN 随深度出现 vanishing gradients，普通 \(\mu\)P ResNet 的 standard/decoupled 轨迹仍错位且深层可过拟合；depth-\(\mu\)P 则随 \(L=2,4,8,16\) 改善，实虚线在中等深度已近乎不可分。图像因此直接验证“不是所有无限深参数化都恢复 GIA”。", r"初始化时 finite-network propagation 到 forward–backward SDE 的误差为 \(O(n^{-1}+L^{-1})\)，width 与 depth limits 可交换。训练中在 nondegeneracy assumptions 下，finite dynamics 到 NFD 为 \(O(L^{-1})\)，遗漏的 reused-weight coupling 更快按 \(O(L^{-2})\) 衰减。", r"NFD 不是 frozen kernel：它保留训练生成的 feature–gradient covariance，允许 nonlinear feature evolution。Figure 1 的数值误差随 width/depth 与理论阶数一致，Figure 3 的最小 covariance eigenvalue 在 5 seeds、width 512–4096 下支持所需非退化条件。"),
            sec("有效性与局限", r"严格结果针对 one-layer ResNets、特定 smoothness/nondegeneracy assumptions 与 depth-\(\mu\)P scaling；它不自动覆盖 Transformer、normalization、finite batch correlations 或任意 optimizer。Figure 3 只是对假设的数值支持，不是一般正定性的证明。", r"CIFAR-10 实验宽度和深度有限，主要检验 asymptotic error/alignment 而非 state-of-the-art accuracy。所谓 decoupled backward weights 是理论控制构造，不是通常训练算法；NFD 的预测力仍需在更深、不同架构和真实 feature observables 上验证。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2512.21075。全文 43 页，PDF SHA-256：55abca63b0577051d613856c1447f833a9ef75f9786732fe3a1392a6e69af944。", r"复现 Figure 2 需固定 CIFAR-10 split、width 128、\(L=2,4,8,16\)、depth-\(\mu\)P/\(\mu\)P scaling、SGD schedule、standard/decoupled initialization 与 seeds；Figure 1 还需保存 finite-to-NFD errors 并分别拟合 \(1/n\)、\(1/L\)。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2，直观区分 width independence 与 depth-restored GIA；再读 Section 4 的 initialization coupling，随后读 Section 5 的 one-update conditional Gaussian decomposition 和 NFD theorem。最后核对 Figure 1/3，区分已证明速率、数值支持的假设与架构外推。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2512.21075/figure-2-gia-restoration.webp", "label": "Figure 2", "visual_type": "data_plot", "evidence": "paper.pdf p. 6, Figure 2", "alt_text": "三种深网参数化中 standard 与 decoupled forward-backward 训练和测试轨迹的比较。", "caption": "只有 depth-μP 随深度恢复 standard/decoupled 轨迹对齐，支持耦合项是更高阶深度修正。", "selection_rationale": "论文没有概念示意图；Figure 2 是最直接呈现核心机制的关键图。"},
        "figure_refs": [figure("2512.21075", "figure-2-gia-restoration.webp", "Figure 2", 6, "test restoration of gradient independence with depth", "三列分别为 vanilla DNN、μP ResNet 与 depth-μP ResNet 的 training/test loss。", "depth-μP 下 standard 与 decoupled trajectories 随深度重合。", "The experiment supports the scaling mechanism on CIFAR-10; it does not prove GIA for arbitrary architectures.")],
        "equation_refs": [
            {"label": "Depth-muP residual update", "latex": r"h_\ell=h_{\ell-1}+\frac{1}{\sqrt L}\,\Phi_\ell(h_{\ell-1})", "role": "set the continuous-depth fluctuation scale", "symbols": {"L": "network depth", "h_l": "layer feature"}, "evidence": "paper.pdf pp. 2–3, model setup", "interpretation": "Layer increments remain stochastic in continuous depth while their accumulated correlation can be power counted in L."},
            {"label": "Training-limit error hierarchy", "latex": r"\lVert\text{finite dynamics}-\text{NFD}\rVert=O(L^{-1}),\qquad \lVert\text{reused-weight coupling}\rVert=O(L^{-2})", "role": "separate discretization and coupling errors", "symbols": {"NFD": "Neural Feature Dynamics limit"}, "evidence": "paper.pdf pp. 8–9, Theorem 5.5", "interpretation": "The omitted coupling is asymptotically subleading to ordinary depth discretization error."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: model, initialization limit and GIA experiment", "paper.pdf pp. 6–9: training coupling, NFD and convergence theorem", "source PDF SHA-256 55abca63b0577051d613856c1447f833a9ef75f9786732fe3a1392a6e69af944", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2601.09881", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2601.09881",
        "title_en": "Transition Matching Distillation for Fast Video Generation",
        "title_zh": "用于快速视频生成的转移匹配蒸馏",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["4d124aa87b3150b9"], ["Video Generation"]),
        "verified_metadata": meta(
            "2601.09881", "v2", "Transition Matching Distillation for Fast Video Generation",
            ["Weili Nie", "Julius Berner", "Nanye Ma", "Chao Liu", "Saining Xie", "Arash Vahdat"],
            ["cs.CV", "cs.AI", "cs.LG"], "cs.CV", "2026-01-14T21:30:03Z",
            "Transition Matching Distillation reuses semantic backbone features and performs lightweight inner flow updates to obtain fractional-NFE video generators.",
        ),
        "sections": [
            sec("作者信息", r"作者：Weili Nie、Julius Berner、Nanye Ma、Chao Liu、Saining Xie、Arash Vahdat；arXiv:2601.09881v2。全文 27 页。作者把 Wan2.1 1.3B/14B text-to-video flow models 蒸馏为少步生成器，并报告 VBench、2AFC user study 与 wall-clock/compute proxy。"),
            sec("研究问题", r"视频 diffusion/flow teacher 需要几十步全网络求值；直接一步 distribution matching 容易丢失时序细节，多步 student 又重复昂贵语义计算。论文问：能否把一次外层 transition 内的语义表示固定下来，只用小型 flow head 做多次内层修正，从而连续调节质量—计算成本？"),
            sec("背景", r"Transition matching 不要求 student 逐点复制 teacher trajectory，而是让少数 probabilistic transitions 复现多步 denoising 的分布演化。TMD 将 30/40-block DiT 的前部视为 main backbone，最后 \(H\) 个 blocks 作为 flow head；每个 outer step 只运行一次 main backbone。", r"Figure 1 展示同一 prompt 在 5 s、480p 视频的四个时刻：有效 NFE 2.75 和 1.38 都保持主体与场景连续。它是视觉证据而非 metric，说明极低外层求值下仍能产生可辨运动序列。"),
            sec("模型与方法", r"第一阶段 TM-MF pretraining 把 flow head 变为条件 flow map，并用 time-conditioned gate 融合 backbone feature、text condition 与 noisy head target；finite-difference JVP 避免依赖特定 attention/FSDP implementation。", r"第二阶段以改进的 DMD2-v 做 distribution matching，并在每个 transition 中 unroll inner flow。DMD2-v 使用 Conv3D discriminator、按步数选择 KD warm-up 和 timestep shifting；unrolled gradients 穿过所有 head steps，以减少 train–inference mismatch。"),
            sec("核心结果与证据", r"Figure 1 的两组序列表明 TMD 的计算并非简单“少取帧”：NFE 1.38/2.75 是按使用的 DiT blocks 折算的全网络求值，四个展示帧仍跨越完整 5 s。图中视觉一致性需与盲测和 VBench 一起读，不能由精选样例单独成立。", r"Wan2.1 1.3B 蒸馏中，TMD-N2H5 在 effective NFE 2.33 得 VBench overall 84.68，超过 4-NFE rCM 的 84.43；NFE 1.17 时 overall 83.80，超过 1-NFE DMD2-v 的 83.24。Wan2.1 14B 上 NFE 1.38 的 TMD 为 84.24，对应 DMD2-v 为 83.69。", r"计算定义为 \(M[1+(N-1)H/L]\)，因此可出现 fractional NFE。5 个 head blocks、2 个 inner steps 对 30-block teacher 的额外 student-update compute 低于 17%。14B 的 2.75-NFE TMD 并未超过所有 2-step baselines，作者明确保留这一负结果。"),
            sec("有效性与局限", r"Figure 1/3 是作者筛选的 qualitative examples；视频真实性、物理一致性和 rare prompt failure 不能从中推断。VBench 与 2AFC 覆盖有限 prompt distribution，且训练数据含 Wan2.1 14B 生成的 500k text–video pairs，可能继承 teacher bias 与 artifacts。", r"effective NFE 是按 block 数线性折算的 proxy，不等于真实 latency、memory traffic 或 energy；flow-head rollout 的 kernel efficiency 依硬件而变。主要证据围绕 Wan2.1 及 480p latent resolution，跨架构、长视频和高分辨率泛化尚未确立。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2601.09881；项目页：https://research.nvidia.com/labs/genair/tmd。全文 27 页，PDF SHA-256：226e7cba2ddb49b8b39aae62730cd4976cf1704c97027f6c1aed41756a874599。", r"复现需固定 Wan2.1 checkpoint、500k prompt/video corpus、latent shape \([21,60,104]\)、81-frame decoder、outer steps \(M\)、inner steps \(N\)、head blocks \(H\)、TM-MF finite difference、DMD2-v discriminator/KD/timestep shift、VBench revision 与 2AFC protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2 的 main-backbone/flow-head 拆分，再看 Figure 1/3 的时间序列；随后读 Eqs. (13)–(16)，确认 inner rollout 与 effective NFE 的定义。最后对照 Tables 1–2 和 user study，并把 block-count proxy、实际 latency 与视觉质量分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2601.09881/figure-1-generated-videos.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "两个文本提示生成的 5 秒视频在四个时刻的帧序列，分别采用两种有效 NFE。", "caption": "TMD 在约 1.38–2.75 次等效全网络求值下生成连贯的 5 秒视频序列。", "selection_rationale": "按 v2.3 封面规则优先使用最重要的可视化生成结果，而不是 VBench 数据表。"},
        "figure_refs": [figure("2601.09881", "figure-1-generated-videos.webp", "Figure 1", 1, "show temporal samples at very low effective NFE", "兔子行走与人物饮咖啡两组视频各展示四个时间点。", "少量外层 backbone evaluations 配合内层 head refinement 可维持可辨运动与场景。", "These are selected generations and must be interpreted together with aggregate and blinded evaluations.")],
        "equation_refs": [
            {"label": "Conditional inner flow map", "latex": r"f_\theta(y_s,s,r;m)=y_s+(s-r)u_\theta(y_s,s,r;m)", "role": "refine a transition using reused semantic features", "symbols": {"m": "main-backbone feature", "u_theta": "average inner velocity"}, "evidence": "paper.pdf p. 4, Eq. (13)", "interpretation": "Several cheap head updates share one expensive semantic representation."},
            {"label": "Effective network evaluations", "latex": r"\operatorname{NFE}_{\rm eff}=M\!\left[1+\frac{(N-1)H}{L}\right]", "role": "compare fractional compute against full-backbone steps", "symbols": {"M": "outer transitions", "N": "inner flow steps", "H": "flow-head blocks", "L": "teacher blocks"}, "evidence": "paper.pdf p. 5, Eq. (16)", "interpretation": "The proxy counts head blocks as fractions of a full DiT pass; it is not a direct latency measurement."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: transition formulation, two-stage training and effective NFE", "paper.pdf pp. 5–8: Wan2.1 evaluations, visual comparisons and user study", "source PDF SHA-256 226e7cba2ddb49b8b39aae62730cd4976cf1704c97027f6c1aed41756a874599", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2601.22033", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2601.22033",
        "title_en": "Holographic generative flows with AdS/CFT",
        "title_zh": "基于 AdS/CFT 的全息生成流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["f238cf2cfef0f82c"], ["Field Theory"]),
        "verified_metadata": meta(
            "2601.22033", "v1", "Holographic generative flows with AdS/CFT",
            ["Ehsan Mirafzali", "Sanjit Shashi", "Sanya Murdeshwar", "Edgar Shaghoulian", "Daniele Venturi", "Razvan Marinescu"],
            ["cs.LG", "gr-qc", "hep-th"], "cs.LG", "2026-01-29T17:39:40Z",
            "A scalar-field bulk-to-boundary map in anti-de Sitter geometry is used as an inductive bias for flow matching on checkerboard and MNIST data.",
        ),
        "sections": [
            sec("作者信息", r"作者：Ehsan Mirafzali、Sanjit Shashi、Sanya Murdeshwar、Edgar Shaghoulian、Daniele Venturi、Razvan Marinescu；arXiv:2601.22033v1。全文 14 页。工作把 AdS scalar bulk-to-boundary propagation 嵌入 flow matching，并在 checkerboard 与 MNIST 上做 proof-of-concept。"),
            sec("研究问题", r"普通 flow matching 完全从数据学习 velocity field，未利用可能的几何约束。论文问：能否把 data distribution 视作 conformal boundary 上的 field，把 flow time 视作 AdS radial coordinate，用 bulk equations/propagator 提供结构化 inductive bias，并在相同规模网络下加快收敛？"),
            sec("背景", r"在 Poincaré patch 中，\((d+1)\)-维 AdS 的边界位于 \(z=0\)，radial direction 对应 coarse-graining scale；scalar field 的 bulk solution 由 boundary source 通过 bulk-to-boundary kernel 传播。作者把这个字典类比为 base→data 的生成 transport。", r"Figure 1 的 Escher Poincaré disk 用欧氏图像直观展示负曲率：图案靠近边界看似缩小，但 hyperbolic proper size 保持不变。红色等半径圆因此同时扮演 RG slices 与 generative-flow time slices 的概念封面。"),
            sec("模型与方法", r"GenAdS 把数据点编码为 boundary scalar sources，通过参数化 kernel/field 得到 bulk representation，再由网络预测沿 radial coordinate 的 flow。训练比较 linear 与 Hermite interpolation paths，以及 full velocity loss 与将已知 AdS contribution 分离后的 residual loss。", r"checkerboard 使用 point-source style encoding 与 FCN baseline；MNIST 使用像素 holographic encoding，并与同参数量 CNN baseline 比较。附录还将 metric 换为 hyperscaling-violating geometry，以检查优势是否只来自 AdS 特例。"),
            sec("核心结果与证据", r"Figure 1 本身不是性能证据，而是模型的几何字典：boundary data 经 red radial slices 延拓到 bulk，生成时间由 radial coordinate 提供。对物理读者，关键是这里借用的是可计算的 scalar propagation 与负曲率 inductive bias，并未构造或验证一个真实量子引力 dual pair。", r"checkerboard 上 GenAdS 在样本质量阈值与 convergence curves 中通常比 matched physics-free FCN 更早到达目标；linear path + full velocity loss 是最快组合。MNIST 的 100/250/500/1500 epoch 样例与 BPM/FID 显示部分 ablated GenAdS 可与 CNN baseline 竞争。", r"负结果同样关键：加入最多物理结构的 residual-loss + Hermite-path 模型在 MNIST 反而更差；作者据此判断有效成分主要是 holographic encoding/AdS geometry，而不是越多 equations-of-motion constraint 越好。hyperscaling-violating ablation 也显示 AdS 的灵活性，而非唯一性。"),
            sec("有效性与局限", r"“AdS/CFT”在此是 architecture prior 与 transport analogy；boundary 数据并非已知 CFT observables，bulk 网络也未满足完整 gravitational path integral。不能把 benchmark 提升解释为发现了数据的物理 holographic dual。", r"实验只有二维 checkerboard 和 MNIST，baseline/encoding 选择可能贡献大部分差异；BPM/FID 与收敛 epoch 不足以证明高维自然图像或大模型收益。pixel-to-boundary encoding 很简单，作者也承认需要更精细的 spatial source/decoder。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2601.22033。全文 14 页，PDF SHA-256：122bd782a3e33f34deee4217ba5016e9937b8bd9ff55cd6d12906a150a92cc34。", r"复现需固定 AdS dimension/metric、scalar mass or conformal dimension \(\Delta\)、bulk-to-boundary kernel regularization、boundary encoding、linear/Hermite paths、full/residual losses、matched FCN/CNN parameter counts、BPM/FID estimators、threshold definition 与 seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 并把 radial coordinate、RG slice 与 generative time 三者对应；再读 Sections II–IV 的 scalar kernel 和 GenAdS loss。随后看 checkerboard/MNIST ablations，尤其是 fully physics-informed 方案的失败，最后读 discussion，避免把有用的几何先验写成已建立的 AdS/CFT 对偶。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2601.22033/figure-1-poincare-disk.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "Escher 的 Poincaré disk 与红色等半径切片，展示双曲空间靠近边界的尺度结构。", "caption": "红色 radial slices 把 AdS 的尺度方向可视化，并被论文映射为生成流的时间坐标。", "selection_rationale": "Figure 1 是文中最具物理直觉和可视化价值的图片，优先于 checkerboard/MNIST 数据表。"},
        "figure_refs": [figure("2601.22033", "figure-1-poincare-disk.webp", "Figure 1", 1, "visualize the negatively curved radial geometry", "Poincaré disk 中图案向边界欧氏缩小，红圈标出 radial slices。", "The radial foliation motivates a scale-indexed generative transport from bulk to boundary.", "The image illustrates AdS geometry; it does not demonstrate that the dataset has a physical holographic dual.")],
        "equation_refs": [
            {"label": "Poincare AdS metric", "latex": r"ds^2=\frac{dz^2+d\vec x^{,2}}{z^2},\qquad z>0", "role": "define the negatively curved bulk geometry", "symbols": {"z": "AdS radial coordinate", "x": "boundary coordinates"}, "evidence": "paper.pdf pp. 2–3, Section II", "interpretation": "The conformal boundary lies at z approaching zero, while radial motion supplies a scale coordinate."},
            {"label": "Scalar bulk-to-boundary map", "latex": r"\phi(z,x)=\int d^d x'\,K_\Delta(z,x;x')\,\phi_0(x')", "role": "encode boundary data into a bulk field", "symbols": {"K_Delta": "bulk-to-boundary propagator", "phi_0": "boundary source"}, "evidence": "paper.pdf pp. 3–5, scalar-field construction", "interpretation": "GenAdS turns a fixed geometric propagation rule into an inductive bias for the learned transport."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–5: AdS/CFT dictionary, scalar fields and holographic encoding", "paper.pdf pp. 8–12: checkerboard, MNIST and geometry/loss ablations", "source PDF SHA-256 122bd782a3e33f34deee4217ba5016e9937b8bd9ff55cd6d12906a150a92cc34", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2602.00869", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2602.00869",
        "title_en": "Improving Flow Matching by Aligning Flow Divergence",
        "title_zh": "通过对齐流散度改进流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["718967ebb315d9b4"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2602.00869", "v1", "Improving Flow Matching by Aligning Flow Divergence",
            ["Yuhao Huang", "Taos Transue", "Shih-Hsin Wang", "William Feldman", "Hong Zhang", "Bao Wang"],
            ["cs.LG", "cs.AI", "math.NA"], "cs.LG", "2026-01-31T19:07:54Z",
            "A PDE error identity bounds probability-path total variation by vector-field and divergence mismatch, motivating Flow and Divergence Matching.",
        ),
        "sections": [
            sec("作者信息", r"作者：Yuhao Huang、Taos Transue、Shih-Hsin Wang、William Feldman、Hong Zhang、Bao Wang；arXiv:2602.00869v1。全文 23 页，发表于 ICML 2025（PMLR 267）。论文从 continuity equation 的误差传播推导 FDM，并覆盖 density、DNA、dynamical systems 与 video benchmarks。"),
            sec("研究问题", r"CFM 让 learned velocity \(v_t\) 在平方误差意义下逼近 conditional target，却不直接控制 induced density \(\hat p_t\)。论文问：两个速度场很接近时，为什么 probability paths 仍可偏离；需要控制什么局部量，才能给 \(\mathrm{TV}(p_t,\hat p_t)\) 一个可训练的上界？"),
            sec("背景", r"exact 与 learned density 分别满足 continuity equations。令 \(\epsilon_t=p_t-\hat p_t\)，相减后得到带 forcing term 的线性输运 PDE；forcing 不只含 \(u_t-v_t\)，还含 divergence gap \(\nabla\!\cdot u_t-\nabla\!\cdot v_t\)。", r"Figure 2 在 \(t=0.6,0.85,1\) 比较四峰 Gaussian mixture：普通 FM 的蓝色路径逐步偏离红色 data，FDM 的黑色路径到终点仍对齐。图直接把“低 velocity loss 不等于正确 density”变成可视化。"),
            sec("模型与方法", r"Theorem 3.3 先以 \(\mathcal L_{DM}\) 控制 TV gap；由于 marginal target divergence 不可直接得到，作者构造 conditional divergence matching loss \(\mathcal L_{CDM}\) 作为上界，并训练 \(\mathcal L_{FDM}=\lambda_1\mathcal L_{CFM}+\lambda_2\mathcal L_{CDM}\)。", r"高维 divergence 用 Hutchinson trace estimator；efficient squared CDM 采用 stop-gradient，只比 baseline 多一次 backward pass。不同任务仍使用 OT、VE/VP 或 Dirichlet probability paths，FDM 改的是训练约束而非 ODE sampler。"),
            sec("核心结果与证据", r"Figure 2 显示误差传播的时间结构：FM 在中间时刻已错配弱峰，终点放大为明显 density bias；FDM 同时约束 compression/expansion rate 后，四个峰的质量与位置都更接近 target。Figure 3 的整条 probability surface 给出同一结论。", r"理论上 \(\mathrm{TV}(p_t,\hat p_t)\le\tfrac12\mathcal L_{DM}\le\tfrac12\mathcal L_{CDM}\)。CIFAR-10 OT path 上 NLL 从 2.99 降到 2.85、FID 从 6.35 降到 5.62；checkerboard、DNA 的 likelihood/TV 也一致改善。", r"KTH 以前 10 帧预测后 30 帧时，latent FM 的 FVD/PSNR 为 180/30.4，latent FDM 为 \(155.5\pm5\)/31.2；代价从每 iter 0.18 s 增至 0.27 s。结果说明 divergence regularization 有实质收益，同时也明确存在约 50% 的训练迭代开销。"),
            sec("有效性与局限", r"TV bound 依赖文中 mild regularity/integrability assumptions，且上界可能松；控制 TV 不自动控制 KL、tails 或 rare events。conditional upper bound 与 Hutchinson estimator 会引入方差，\(\lambda_2\) 仍需 task-specific search。", r"实验横跨多域但每域规模有限；CIFAR-10 和 KTH/BAIR 不能代表现代大规模生成。FDM 增加 backward compute，论文所说“不牺牲 generation efficiency”仅指 inference ODE 未变，不是 training cost 不变。代码可用仍不等于结果已被独立复现。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2602.00869；代码：https://github.com/Utah-Math-Data-Science/Flow_Div_Matching。全文 23 页，PDF SHA-256：e54a1d133672fbe9d1b27f9ca01c33442657b825db44c30a8fd7a657329b89b9。", r"复现需固定 probability path、\(\lambda_1,\lambda_2\)、Hutchinson probe count/distribution、stop-gradient estimator、network/optimizer、ODE solver、dataset splits、NLL/FID/FVD checkpoint、event-guidance protocol 与 seeds，并同时报告 training time。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2，直观看 density path 而非只看 velocity loss；再读 Proposition 3.1 与 Theorems 3.3/4.1 的 PDE 和 TV bound。随后看 efficient CDM estimator，最后按 Table 2、DNA、dynamical systems、KTH/BAIR 顺序检查收益与额外训练成本。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2602.00869/figure-2-probability-paths.webp", "label": "Figure 2", "visual_type": "distribution", "evidence": "paper.pdf p. 5, Figure 2", "alt_text": "FM 与 FDM 在三个时刻拟合四峰 Gaussian mixture probability path 的比较。", "caption": "速度误差小仍可能累积为密度偏差；加入散度匹配后，四峰概率路径在终点保持对齐。", "selection_rationale": "Figure 2 直接可视化论文的 PDE 机制，比单项 benchmark 数据更适合作为封面。"},
        "figure_refs": [figure("2602.00869", "figure-2-probability-paths.webp", "Figure 2", 5, "show probability-path error accumulation", "上排 FM、下排 FDM 在三个时间点与四峰目标密度比较。", "Divergence matching suppresses the density error that remains invisible to a small conditional velocity loss.", "The visualization is one controlled one-dimensional mixture, not a universal estimate of high-dimensional error.")],
        "equation_refs": [
            {"label": "Probability-path TV bound", "latex": r"\operatorname{TV}(p_t,\hat p_t)\le\frac12\mathcal L_{DM}(\theta)\le\frac12\mathcal L_{CDM}(\theta)", "role": "connect local flow/divergence mismatch to density error", "symbols": {"p_t": "exact path", "p_hat_t": "learned path", "L_CDM": "conditional divergence matching loss"}, "evidence": "paper.pdf pp. 4–5, Theorems 3.3 and 4.1", "interpretation": "Matching divergence supplies a trainable control on the total-variation gap that CFM alone does not provide."},
            {"label": "Flow and divergence matching objective", "latex": r"\mathcal L_{FDM}=\lambda_1\mathcal L_{CFM}+\lambda_2\mathcal L_{CDM},\qquad \lambda_1,\lambda_2>0", "role": "train velocity and local volume change jointly", "symbols": {"lambda_1": "flow weight", "lambda_2": "divergence weight"}, "evidence": "paper.pdf p. 5, Eq. (17)", "interpretation": "The second term regularizes compression and expansion of probability mass without changing the inference solver."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: error PDE, TV bounds and FDM objective", "paper.pdf pp. 5–9: density, DNA, dynamical-system and video experiments", "source PDF SHA-256 e54a1d133672fbe9d1b27f9ca01c33442657b825db44c30a8fd7a657329b89b9", "Evidence status: full-text verified; no independent reproduction performed."],
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
