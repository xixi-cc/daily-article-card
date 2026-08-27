#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 019."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2506.14330", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2506.14330",
        "title_en": "Random organization criticality with long-range hydrodynamic interactions",
        "title_zh": "长程流体动力学相互作用下的随机组织临界性",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["30685821a868d8a3"], ["Fluid Dynamics"]),
        "verified_metadata": meta(
            "2506.14330", "v1",
            "Random organization criticality with long-range hydrodynamic interactions",
            ["Tristan Jocteur", "Cesare Nardini", "Eric Bertin", "Romain Mari"],
            ["cond-mat.soft", "cond-mat.stat-mech"], "cond-mat.soft",
            "2025-06-17T09:15:36Z",
            "A mediated random-organization model shows continuously varying critical exponents, convex absorbing transitions and loss of hyperuniformity under sufficiently long-ranged hydrodynamic interactions.",
        ),
        "sections": [
            sec("作者信息", r"作者：Tristan Jocteur、Cesare Nardini、Eric Bertin、Romain Mari；arXiv:2506.14330v1。全文 22 页。论文研究周期剪切悬浮液的可逆—不可逆吸收相变，建立带长程机械噪声的 random organization model，并在 \(d=2,3\) 数值测量临界指数。"),
            sec("研究问题", r"原始 Random Organization Model（ROM）把未接触粒子视为完全静止，通常给出 Conserved Directed Percolation（CDP）临界性；真实悬浮液中，一个接触产生的 Stokes 流却能远程移动被动粒子并制造新接触。论文问：相互作用按 \(1/r^\alpha\) 衰减时，吸收相变的阶参量指数、涨落与超均匀性如何随 \(\alpha\) 改变？"),
            sec("背景", r"周期剪切后以 stroboscopic 时间观察：若一周期内没有接触，构型回到原位并进入 absorbing state；若接触持续产生，粒子发生不可逆扩散。常规 CDP 区域的活动密度满足 \(\langle A\rangle\sim(\phi-\phi_c)^\beta\)，且临界构型在长波极限抑制数密度涨落。", r"Figure 1 将新物理机制画出：红色 active particles 接受局部随机 kick，灰色 passive particles 也因远处接触产生位置依赖 kick；粗粒化 activity field \(A(\mathbf r)\) 决定长程噪声的局部方差。"),
            sec("模型与方法", r"作者在 \(d\)-维周期盒中保留 ROM 的接触判据与 active kicks，并将空间划成 boxes。每个 box 的活动密度 \(A_b\) 经长程 kernel \(G(r)\) 卷积，给被动粒子一个零均值 Gaussian displacement，其标准差为 \(\Delta_{p,i}=[\sum_{b'}G(r_{b'b})A_{b'}]^{1/2}\)。", r"若 hydrodynamic mobility 按 \(1/r^\alpha\) 衰减，位移方差核取 \(G(r)\sim r^{-2\alpha}\)。作者扫描 \(\phi-\phi_c\)、\(\alpha\)、系统尺寸与 \(d=2,3\)，拟合 \(\beta,\nu_\perp,\gamma\) 等指数，并用 structure factor \(S(q)\) 与 box-counting variance 检查 hyperuniformity。另以局域 mean-field activation channels \(A+P\to2A\) 与 \(2P\to2A\) 解释 convex transition。"),
            sec("核心结果与证据", r"Figure 1 显示长程相互作用并不直接搬运“活动标签”，而是由活动接触产生机械噪声、让原本被动的粒子相碰；这一区别决定为何简单加入 long-range activity transport 的 CDP 场论不能复现数值相图。", r"当 \(\alpha\gtrsim d\) 时临界性接近通常 CDP；减小 \(\alpha\) 后临界指数连续漂移，阶参量曲线从 concave（\(\beta<1\)）变为 convex（\(\beta>1\)）。质的交叉位于 bulk hydrodynamics 的 \(\alpha=d-1\) 与 confined mobility 的 \(\alpha=d\) 之间。", r"在 \(d=2\) 中，\(S(q)\sim q^{0.45}\) 的 hyperuniform sector 随 \(\alpha\) 减小逐步缩短，并在约 \(\alpha\lesssim1.5\) 出现小-\(q\) plateau/上翘、与 convexity change 同期消失。论文据此预测三维 bulk 悬浮液（\(\alpha=2=d-1\)）为非 CDP、convex 且非超均匀，而受限系统（\(\alpha=d\)）更接近 CDP 与 hyperuniform。"),
            sec("有效性与局限", r"mediated ROM 是 stroboscopic minimal model：它忽略周期内接触网络的时间演化、近场 lubrication、张量流体 mobility、相关 kick directions 与真实边界。kernel 只保留远场幂律，因而不能定量替代 Stokesian dynamics 或实验。", r"指数拟合受有限尺寸、临界点估计与 crossover window 影响；作者也指出 mean-field 对部分指数只定性成立。关于 bulk/ confined 实验的预测与既有报道有张力，可能源于实验可达波数不足。hyperuniformity 的消失尺度、continuum theory 的非解析项及 universality classification 仍未解决。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.14330。全文 22 页，PDF SHA-256：30685821a868d8a32884bb5d70035f34bdda97df52392619c1ed5e2b18864625。", r"复现需固定 \(d,N,L,D,\Delta_a\)、box size、periodic distance、kernel regularization/cutoff、\(\alpha\) grid、absorbing stopping rule、\(\phi_c\) estimator、finite-size windows、structure-factor binning 与 box-counting protocol。应保存每个 seed 的 absorption time 和 exponent fit covariance。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，区分长程机械噪声与长程 activity transport；再读数值相图、\(\beta(\alpha)\) 与 structure-factor figures。随后检查 mean-field 的两条 activation channels，最后读 conclusion 中 bulk/ confined predictions，并把模型内 universality statement 与真实悬浮液实验判定分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.14330/figure-1-mediated-rom.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "active particles 的局部 kick、被动粒子的长程位置依赖 kick，以及粗粒化 activity field。", "caption": "接触产生的长程机械噪声把被动粒子激活；它改变 activity creation，而非简单远程搬运活动。", "selection_rationale": "Figure 1 是全文最重要的物理机制图，优先于单一临界指数曲线。"},
        "figure_refs": [figure("2506.14330", "figure-1-mediated-rom.webp", "Figure 1", 3, "explain the long-range activation mechanism", "Mediated random-organization rules and the coarse-grained activity field.", "Remote contacts generate position-dependent passive-particle noise, opening a new activity-creation channel.", "The schematic omits tensor hydrodynamics, near-field lubrication and within-cycle contact evolution.")],
        "equation_refs": [
            {"label": "Mediated passive-particle kick", "latex": r"\Delta_{p,i}=\left[\sum_{b'}G(r_{b'b})A_{b'}\right]^{1/2},\qquad G(r)\sim r^{-2\alpha}", "role": "encode long-range hydrodynamic mechanical noise", "symbols": {"A_b": "coarse-grained activity density", "alpha": "mobility decay exponent", "Delta_p": "passive kick standard deviation"}, "evidence": "paper.pdf p. 3, Eqs. (2)–(4)", "interpretation": "Variance contributions from distant active boxes add, so slowly decaying mobility creates activity nonlocally."},
            {"label": "Absorbing-transition order parameter", "latex": r"\langle A\rangle\sim(\phi-\phi_c)^\beta", "role": "classify concave and convex critical onset", "symbols": {"phi": "particle volume fraction", "phi_c": "critical volume fraction", "beta": "order-parameter exponent"}, "evidence": "paper.pdf pp. 4–7", "interpretation": "Longer-ranged interactions drive beta through one and away from the short-range CDP value."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: ROM and mediated long-range kernel", "paper.pdf pp. 4–15: exponent drift, hyperuniformity and theoretical interpretation", "source PDF SHA-256 30685821a868d8a32884bb5d70035f34bdda97df52392619c1ed5e2b18864625", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.15742", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2506.15742",
        "title_en": "FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space",
        "title_zh": "FLUX.1 Kontext：潜空间中的上下文图像生成与编辑流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["b4d7d95594eedfb6"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2506.15742", "v2",
            "FLUX.1 Kontext: Flow Matching for In-Context Image Generation and Editing in Latent Space",
            ["Black Forest Labs", "Stephen Batifol", "Andreas Blattmann", "Frederic Boesel", "Saksham Consul", "Cyril Diagne", "Tim Dockhorn", "Jack English", "Zion English", "Patrick Esser", "Sumith Kulal", "Kyle Lacey", "Yam Levi", "Cheng Li", "Dominik Lorenz", "Jonas Müller", "Dustin Podell", "Robin Rombach", "Harry Saini", "Axel Sauer", "Luke Smith"],
            ["cs.GR"], "cs.GR", "2025-06-17T20:18:23Z",
            "A rectified-flow transformer concatenates context and target image tokens to unify text-to-image generation, instruction editing and iterative visual workflows.",
        ),
        "sections": [
            sec("作者信息", r"作者单位为 Black Forest Labs；arXiv:2506.15742v2，共 21 位署名作者。全文 20 页。论文公开 FLUX.1 Kontext 的模型设计、KontextBench 与应用/失败案例，但训练图文对、完整数据配方和 [pro]/[max] 权重并未全部开放。"),
            sec("研究问题", r"现有图像编辑器常需任务专用 fine-tuning，或在连续多轮编辑中发生 identity/style drift；多模态自回归系统又可能延迟高。论文问：能否让一个 latent flow model 同时处理纯文本生成与以参考图、自然语言指令为条件的 in-context editing，并在多轮操作中维持对象一致性？"),
            sec("背景", r"目标条件分布写为 \(p(x\mid y,c)\)：\(x\) 是输出图，\(y\) 是可选 context image，\(c\) 是指令。与通道拼接不同，Kontext 把 context latent tokens 直接追加到 target tokens，在 Transformer attention 中建立图—图关系；纯文本任务令 \(y=\varnothing\)。", r"Figure 2 以连续四步编辑说明关键能力：去除遮挡、迁移到 Freiburg、再改变天气，同时尽量保留人物、衣着与摄影风格。这张图展示“可迭代条件映射”，但只是作者选取的成功轨迹，不能替代随机任务统计。"),
            sec("模型与方法", r"基座是 latent-space rectified-flow Transformer，混合 double-stream 与 38 个 single-stream blocks；3D RoPE 为 token 编码虚拟时间和空间位置。target tokens 使用 \(u_x=(0,h,w)\)，第 \(i\) 张 context image 使用 \(u_{y_i}=(i,h,w)\)，从而以 time offset 区分多图而保留内部二维结构。", r"训练从 FLUX.1 text-to-image checkpoint 出发，在数百万 relational pairs \((x\mid y,c)\) 上做 velocity matching；linearly interpolated latent 为 \(z_t=(1-t)x+t\epsilon\)。[pro] 随后使用 latent adversarial diffusion distillation，[dev] 使用 guidance distillation，并针对 editing 继续优化。"),
            sec("核心结果与证据", r"Figure 2 中三次指令改变遮挡、地点和天气，而人物身份与服装仍可辨认；这是把多轮编辑中的 invariant 与 controlled variables 直接可视化，比文字列举更有效。", r"KontextBench 含 1,026 个 crowd-sourced image–prompt pairs，覆盖 text/local/global editing、character/style reference 等类别。human evaluation 中 [pro]/[max] 在 local editing、text editing 与一般 character reference 排名前列；global edit 与 style reference 并非所有比较都第一。", r"作者报告 1024×1024 的 text-to-image 和 image-to-image latency 约 3–5 s，并称相对部分系统快至一个数量级；该数字依赖未完全统一的 API、硬件与服务条件。Flux-VAE 在 4,096 张 ImageNet 图上的 reconstruction 为 PDist 0.332、SSIM 0.896、PSNR 31.1，明显优于表中 SD3/SDXL VAEs。"),
            sec("有效性与局限", r"Figure 2 与后续应用图是筛选样例；benchmarks 同时混合 proprietary APIs、不同 sampling budgets 与 human preferences，不能唯一把差异归因于 flow matching。内部 T2I benchmark 的 1,000 prompts 与训练数据细节不完全公开，限制独立复核。", r"作者明确指出过多轮编辑会积累 artifacts、偶尔忽略指令，distillation 也会损伤 fidelity；目前重点是单 context image，multi-image 与 video editing 仍属未来工作。[dev] 的 I2I-only optimization 也意味着不同 variant 的能力边界不可互换。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.15742；模型页：https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev。全文 20 页，PDF SHA-256：86c8acc1ca714fa463f02315d849a81b5d746c4da4ecb50743b9d672311f916b。", r"复现需固定 autoencoder、relational-pair generation/curation、context token order、RoPE offsets、\(p(t)\) logit-normal shift、T2I/I2I mixing、LADD/guidance distillation、sampling steps、API latency environment 与 human-evaluation randomization。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 2 与 4，理解成功编辑链和 token concatenation；再读 Eq. (3) 的 rectified-flow objective 与 distillation recipe。随后核对 KontextBench 六类结果、latency 条件和 Figure 12/15 的 drift failures，避免把少量演示当作无界的多轮一致性。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.15742/figure-2-iterative-editing.webp", "label": "Figure 2", "visual_type": "comparison", "evidence": "paper.pdf p. 3, Figure 2", "alt_text": "同一人物经过去遮挡、迁移城市与雪景变换的连续四步编辑。", "caption": "每一步改变受控因素，同时尝试保持人物、衣着与摄影风格；这是成功样例，不代表所有多轮轨迹。", "selection_rationale": "Figure 2 是论文最直观的核心能力图，优先于架构框图和 benchmark 柱状图。"},
        "figure_refs": [figure("2506.15742", "figure-2-iterative-editing.webp", "Figure 2", 3, "visualize iterative instruction-conditioned editing", "A reference portrait followed by occlusion removal, relocation and weather editing.", "The sequence separates edited variables from identity and style invariants.", "It is a selected success case; aggregate drift and instruction failures require benchmark and failure-case review.")],
        "equation_refs": [
            {"label": "Conditional image distribution", "latex": r"p_\theta(x\mid y,c),\qquad y\in\mathcal X\cup\{\varnothing\}", "role": "unify editing and text-to-image generation", "symbols": {"x": "target image", "y": "optional context image", "c": "natural-language instruction"}, "evidence": "paper.pdf pp. 4–5, Eq. (1)", "interpretation": "Removing context tokens recovers text-to-image generation; retaining them defines an image-conditioned map."},
            {"label": "Rectified-flow loss", "latex": r"\mathcal L_\theta=\mathbb E\left\|v_\theta(z_t,t,y,c)-(\epsilon-x)\right\|_2^2,\qquad z_t=(1-t)x+t\epsilon", "role": "train one velocity field for T2I and I2I tasks", "symbols": {"epsilon": "Gaussian latent noise", "t": "flow time", "v_theta": "conditional velocity network"}, "evidence": "paper.pdf p. 5, Eq. (3)", "interpretation": "Context and instruction enter the velocity field while the target follows the same linear latent interpolation."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: context-token construction and flow objective", "paper.pdf pp. 7–12: KontextBench, latency, applications and limitations", "source PDF SHA-256 86c8acc1ca714fa463f02315d849a81b5d746c4da4ecb50743b9d672311f916b", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.19774", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2506.19774",
        "title_en": "Kling-Foley: Multimodal Diffusion Transformer for High-Quality Video-to-Audio Generation",
        "title_zh": "Kling-Foley：用于高质量视频到音频生成的多模态扩散 Transformer",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["1f9c1585090b9ff6"], ["Transformer Theory"]),
        "verified_metadata": meta(
            "2506.19774", "v1",
            "Kling-Foley: Multimodal Diffusion Transformer for High-Quality Video-to-Audio Generation",
            ["Jun Wang", "Xijuan Zeng", "Chunyu Qiang", "Ruilong Chen", "Shiyao Wang", "Le Wang", "Wangjing Zhou", "Pengfei Cai", "Jiahui Zhao", "Nan Li", "Zihan Li", "Yuzhe Liang", "Xiaopeng Wang", "Haorui Zheng", "Ming Wen", "Kang Yin", "Yiran Wang", "Nan Li", "Feng Deng", "Liang Dong", "Chen Zhang", "Di Zhang", "Kun Gai"],
            ["eess.AS", "cs.AI", "cs.CL", "cs.SD"], "eess.AS",
            "2025-06-24T16:39:39Z",
            "A multimodal flow-matching transformer aligns video, text and audio tokens to synthesize variable-duration, temporally synchronized soundtracks.",
        ),
        "sections": [
            sec("作者信息", r"作者：Jun Wang、Xijuan Zeng、Chunyu Qiang 等 23 位作者，来自 Kuaishou Technology；arXiv:2506.19774v1。全文 24 页。工作包含生成模型、latent audio codec、20,935 条人工标注的 Kling-Audio-Eval，以及产品安全讨论。"),
            sec("研究问题", r"video-to-audio 不只要求声学自然，还要同时满足事件语义、帧级时间同步、可变时长和多声源空间感。论文问：如何在同一 latent flow 中联合 text/video/audio conditions，并避免不同帧率 token 的位置编码失配，使声音事件与视觉动作同步？"),
            sec("背景", r"输入视频可含可选 text prompt；目标是输出与画面语义一致、时间对齐的声效/背景音乐。Figure 1 用锻铁视频示意输入—生成过程和随视频延伸的 waveform，是系统任务定义而非单纯架构图。", r"模型在 Mel-VAE latent 中生成，再由 mel decoder、Mono2Stereo 与 vocoder 重建 waveform。视频、文本、抽帧对齐特征分别编码；缺失模态由 learnable placeholders 支持 flexible pairwise training。"),
            sec("模型与方法", r"MM-DiT 将 text、vision、audio 的 queries/keys/values 拼到共享 scaled dot-product attention，再按模态拆分；audio-only blocks 增深声学建模。aligned RoPE 按 audio/video 的实际 temporal rates 缩放频率，局部 1D convolutions/MLPs 与 synchronization module 进一步约束短时同步。", r"conditional flow matching 在 \(x_t=tx_1+(1-t)x_0\) 上拟合目标 velocity；推断以 Euler solver 从 Gaussian audio latent 积分到生成 latent。duration embeddings 编码 clip start 与 total duration，并通过 adaptive LayerNorm 调制各层，实现可变时长。数据 pipeline 还包括单事件过滤、时间增强合成多事件与多模型 captions。"),
            sec("核心结果与证据", r"Figure 1 直接说明输出不是一个 class label，而是与输入视频等长的多声道声轨；caption 还强调可生成任意时长序列，但正文的 limitations 将稳定同步范围限制在较短 clips。", r"在 VGGSound 15,220-sample test 上，Kling-Foley 的 IB-score 为 30.75、DeSync 为 0.43、SDR 为 -2.41、MCD 为 2.60；MMAudio 对应 29.26、0.45、-3.09、2.84。分布指标并非全胜：FDPANNs 7.60 与 KLPANNs 1.86 均落后于 MMAudio 的 6.29 与 1.77，说明语义/同步优势不等于每项分布距离最好。", r"latent codec 在 2,000 个 out-of-domain samples 上覆盖 sound effect、music、speech、singing；例如 speech PESQ 3.27 对 MMAudio 3.10，singing MCD 0.70 对 1.08。Kling-Audio-Eval 含 20,935 条、九种声音场景，但 benchmark 构建与部分数据仍为工业内部资源。"),
            sec("有效性与局限", r"论文明确指出复杂物理过程和多物体链式碰撞/多人叠声容易产生 acoustic logic errors；超过约 20 s 的视频可能发生 audio-video synchronization drift，稀有文化/医疗场景因训练样本不足而波动。", r"多数客观指标依赖 PANNs、ImageBind、Synchformer 等代理模型，未等同于听觉盲评；VGGSound 与训练来源可能重叠分布。Figure 1 不能展示真实音质，必须结合音频试听。数据、模型权重、训练 compute 与商业系统细节未完全开放，exact reproduction 受限。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.19774；项目页：https://klingfoley.github.io/Kling-Foley/。全文 24 页，PDF SHA-256：86fb0ba7ff99989a028150f2499a186f5c47bd31250457463cc3ffb1dbe64e46。", r"复现需固定 video/audio sampling rates、Mel-VAE/vocoder、RoPE rate scaling、frame extractor、duration embedding、pairwise modality dropout、flow time grid/Euler step、mono-to-stereo rendering、VGGSound split 与各 metric checkpoint。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 了解任务输出，再看 Figure 2 的 multimodal joint conditioning；随后读 flow objective、aligned RoPE 与 sync module。评估时同时查看 Table 2 的六个指标，注意 distribution matching 的反例；最后读 20 s drift 与 complex-scene limitations，并通过项目页试听。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.19774/figure-1-kling-foley-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "视频和可选文本输入 Kling-Foley，输出与视频等长的多声道音频波形。", "caption": "系统把视觉事件与可选文本映射为同步声轨；流程图定义任务，但音质仍需实际试听与指标验证。", "selection_rationale": "Figure 1 最直观地呈现视频到音频的输入输出，优先于无声的指标表。"},
        "figure_refs": [figure("2506.19774", "figure-1-kling-foley-overview.webp", "Figure 1", 1, "show the video-to-audio task and variable-duration output", "Input video and text are mapped to aligned stereo audio waveforms.", "The model generates an audio sequence whose duration follows the video.", "A static figure cannot establish perceptual audio quality or long-duration synchronization.")],
        "equation_refs": [
            {"label": "Conditional flow-matching loss", "latex": r"\mathcal L_{\rm CFM}=\mathbb E\left\|v_\theta(t,C,tx_1+(1-t)x_0)-u(t,tx_1+(1-t)x_0)\right\|_2^2", "role": "learn audio-latent transport conditioned on video and text", "symbols": {"x0": "Gaussian audio latent", "x1": "target audio latent", "C": "multimodal condition"}, "evidence": "paper.pdf p. 5, Eq. (1)", "interpretation": "The ODE transports noise to audio while joint attention supplies visual and textual constraints."},
            {"label": "Joint multimodal attention", "latex": r"\operatorname{Attn}(Q,K,V)=\operatorname{softmax}\!\left(\frac{[Q_a;Q_v;Q_t][K_a;K_v;K_t]^\top}{\sqrt d}\right)[V_a;V_v;V_t]", "role": "exchange information across audio, video and text tokens", "symbols": {"a,v,t": "audio, video and text modalities", "d": "attention width"}, "evidence": "paper.pdf pp. 6–7, joint-attention section", "interpretation": "Shared attention supplies semantic coupling; aligned RoPE and the synchronization module carry explicit temporal structure."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–10: multimodal flow, aligned RoPE, codec and data pipeline", "paper.pdf pp. 14–18: VGGSound metrics, codec results and limitations", "source PDF SHA-256 86fb0ba7ff99989a028150f2499a186f5c47bd31250457463cc3ffb1dbe64e46", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.23205", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2506.23205",
        "title_en": "BridgeShape: Latent Diffusion Schrödinger Bridge for 3D Shape Completion",
        "title_zh": "BridgeShape：用于三维形状补全的潜空间扩散 Schrödinger 桥",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["ac099926b4ddd8a6"], ["Field Theory"]),
        "verified_metadata": meta(
            "2506.23205", "v2",
            "BridgeShape: Latent Diffusion Schrödinger Bridge for 3D Shape Completion",
            ["Dequan Kong", "Honghua Chen", "Zhe Zhu", "Mingqiang Wei"],
            ["cs.CV"], "cs.CV", "2025-06-29T12:21:21Z",
            "A latent diffusion Schrödinger bridge transports incomplete-shape latents toward complete-shape latents using a depth-enhanced VQ-VAE.",
        ),
        "sections": [
            sec("作者信息", r"作者：Dequan Kong、Honghua Chen、Zhe Zhu、Mingqiang Wei；arXiv:2506.23205v2。全文 18 页。论文将 paired-data Schrödinger bridge 与 depth-enhanced VQ-VAE 用于 voxel/TSDF 形式的 3D shape completion。"),
            sec("研究问题", r"传统 diffusion completion 从无结构 Gaussian noise 出发，再靠额外分支反复注入 incomplete-shape features；这既浪费计算，也没有显式建模 partial→complete distribution transport。论文问：能否把 incomplete latent 直接作为 bridge endpoint，学习一条受 paired shapes 约束的随机最优输运路径？"),
            sec("背景", r"partial scan 表示为 TSDF，complete shape 为 TUDF。Stage I 用完整形状训练 VQ-VAE，并把多个渲染 depth views 的 DINOv2 features 平均后以 cross-attention 融入 encoder；Stage II 用单独 encoder 将 partial shape 映射到同一 latent space，再构造 Schrödinger bridge。", r"Figure 3 对比 Input、ShapeFormer、DiffComplete、BridgeShape 与 GT。它直观显示 BridgeShape 对柜体孔洞、桌腿、灯罩与沙发轮廓的补全更接近 GT，但仍是选取样例，不能替代全测试集误差。"),
            sec("模型与方法", r"给定 complete latent \(z_0\sim p_A\) 与 incomplete latent \(z_T\sim p_B\)，目标是在参考 path measure 下最小化 path-space KL 且满足两端 marginals。paired training 允许直接采样 Gaussian bridge posterior \(q(z_t\mid z_0,z_T)\)，其均值按累计方差在两个 endpoints 间插值。", r"极稀疏 partial shapes 会使 transport path 不稳，因此作者先向 incomplete latent 注入 Gaussian stochasticity。denoising U-Net 预测 bridge noise，reverse DDPM 从 \(z_T\) 迭代到 \(\hat z_0\)，再由 VQ-VAE decoder 还原完整体素形状。"),
            sec("核心结果与证据", r"Figure 3 中 BridgeShape 相比 ShapeFormer 与 DiffComplete 更好恢复细杆、封闭平面和对称结构；图像也暴露 partial input 的多解性，不能仅凭视觉决定几何正确。", r"3D-EPN 八类平均 voxel \(l_1\) error 为 0.039；DiffComplete 为 0.053，论文计算约下降 26%。对 unseen synthetic categories，平均 CD×100 为 4.06、IoU×100 为 70.1；real-world ScanNet unseen categories 为 CD 6.99、IoU 53.5，说明 domain shift 下仍有明显精度下降。", r"depth features 把 ablation 的 reconstruction error 从 0.0022 降到 0.0021，并将 completion IoU 从 92.36% 提到 94.41%。附录报告每步约 33.6 GFLOPs、总约 100.8 GFLOPs；相较 100-step diffusion 的约 15,950 GFLOPs，效率优势来自 latent bridge 与少步推断的组合。"),
            sec("有效性与局限", r"Schrödinger bridge 的“optimal transport”依赖选定 reference diffusion、paired endpoints 与 latent geometry；VQ-VAE distortion 会改变物理空间的距离含义。CD/IoU 与 voxel \(l_1\) 不保证拓扑正确、可制造性或薄结构连通。", r"论文 failure cases 指出极端稀疏观测下细节补全不足，latent codebook/representation 也限制高频结构。real-world IoU 明显低于 synthetic；DINOv2 depth views、Scan2CAD labels 与训练类别可能引入先验。与 baselines 的 resolution、steps 和 compute 需逐项对齐。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.23205；代码：https://github.com/kongdq/BridgeShape。全文 18 页，PDF SHA-256：ca46114d61a42ba9f5d31c71c57fe04404ddf0a8db7254fe36deb31fcac8ca67。", r"复现需固定 TSDF/TUDF resolution、VQ codebook、render views、DINOv2 checkpoint、cross-attention stage、partial encoder、bridge variance schedule/stochasticity、reverse steps、surface sampling、CD/IoU threshold 与 five-run aggregation。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2，理解从 Gaussian denoising 改为 partial→complete bridge；再读 Eqs. (6)–(15) 的 endpoints、posterior 和 reverse kernel。随后用 Figure 3/Table 1 建立直觉，再检查 unseen synthetic/real tables、depth/stochasticity ablations 与 failure cases。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.23205/figure-3-shape-completion.webp", "label": "Figure 3", "visual_type": "comparison", "evidence": "paper.pdf p. 5, Figure 3", "alt_text": "八类不完整三维物体经 ShapeFormer、DiffComplete、BridgeShape 补全并与 ground truth 比较。", "caption": "BridgeShape 在选取样例中更好恢复整体几何与细结构；总体优劣仍需结合 voxel、CD 与 IoU。", "selection_rationale": "Figure 3 是最具可视性的结果图，可直接替代对不同补全方法的冗长文字描述。"},
        "figure_refs": [figure("2506.23205", "figure-3-shape-completion.webp", "Figure 3", 5, "compare qualitative 3D completion geometry", "Rows show partial input, two baselines, BridgeShape and ground truth across object classes.", "The latent bridge recovers more coherent global shapes and several thin structures in these examples.", "Selected renderings do not establish topology, uncertainty calibration or real-world robustness.")],
        "equation_refs": [
            {"label": "Paired bridge posterior", "latex": r"q(z_t\mid z_0,z_T)=\mathcal N\!\left(z_t;\frac{\sigma_{b,t}^2z_0+\sigma_t^2z_T}{\sigma_{b,t}^2+\sigma_t^2},\frac{\sigma_t^2\sigma_{b,t}^2}{\sigma_t^2+\sigma_{b,t}^2}I\right)", "role": "sample intermediate latents between complete and incomplete endpoints", "symbols": {"z0": "complete-shape latent", "zT": "incomplete-shape latent", "sigma": "accumulated bridge variances"}, "evidence": "paper.pdf p. 4, Eqs. (11)–(13)", "interpretation": "Paired endpoints make the intermediate bridge Gaussian and tractable in the chosen latent coordinates."},
            {"label": "Bridge noise-prediction loss", "latex": r"\mathcal L=\left\|\epsilon_\theta(z_t,t)-\frac{z_t-z_0}{\sigma_t}\right\|_2^2", "role": "learn reverse transport toward the complete latent", "symbols": {"epsilon_theta": "denoising network", "zt": "intermediate bridge state"}, "evidence": "paper.pdf p. 5, Eq. (14)", "interpretation": "The incomplete endpoint supplies the starting structure, so the network predicts a conditional correction rather than denoising from an unrelated prior."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: depth-enhanced VQ-VAE and latent Schrödinger bridge", "paper.pdf pp. 5–12: known/unseen completion results, efficiency and failures", "source PDF SHA-256 ca46114d61a42ba9f5d31c71c57fe04404ddf0a8db7254fe36deb31fcac8ca67", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2506.23589", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2506.23589",
        "title_en": "Transition Matching: Scalable and Flexible Generative Modeling",
        "title_zh": "Transition Matching：可扩展且灵活的生成建模",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["579444607faedf8b"], ["Generative Models"]),
        "verified_metadata": meta(
            "2506.23589", "v1",
            "Transition Matching: Scalable and Flexible Generative Modeling",
            ["Neta Shaul", "Uriel Singer", "Itai Gat", "Yaron Lipman"],
            ["cs.LG", "cs.AI"], "cs.LG", "2025-06-30T07:51:58Z",
            "Transition Matching learns finite stochastic Markov kernels and connects diffusion, flow matching and continuous autoregressive generation.",
        ),
        "sections": [
            sec("作者信息", r"作者：Neta Shaul、Uriel Singer、Itai Gat、Yaron Lipman；arXiv:2506.23589v1。全文 41 页。论文提出 Transition Matching（TM）总框架，并在统一 1.7B DiT、350M licensed image-caption pairs 下比较 DTM、ARTM、FHTM、flow matching 与 autoregressive baselines。"),
            sec("研究问题", r"diffusion/flow 通常以连续时间局部速度描述生成，自回归模型则顺序预测 tokens。论文问：能否直接学习离散时间 Markov transition kernel \(p_\theta(x_{t+1}\mid x_t)\)，允许随机、非连续 supervision，并通过 kernel factorization 在并行 flow 与 causal AR 之间选择？"),
            sec("背景", r"给定 supervising process \(q(x_{0:T})\)，TM 不必重建其微分生成元，而是匹配相邻状态的 conditional transition。一个 auxiliary variable \(Y\) 参数化 \(q(x_{t+1}\mid x_t,Y)\)，网络学习 posterior \(p_\theta(Y\mid x_t)\)；这把设计自由度分成 process、parameterization 与 probabilistic model。", r"Figure 7 在同一类 DiT 训练设置下并列 FM、MAR、FHTM 与 DTM 的文本图像样本。DTM/FHTM 在复杂属性和文字上常更符合 prompt，但这些仍是筛选样例，必须结合 Tables 1–3。"),
            sec("模型与方法", r"DTM 采用线性 path \(X_t=(1-t/T)X_0+(t/T)X_T\)，令 \(Y=X_T-X_0\)，每一步由 \(X_{t+1}=X_t+Y/T\) 更新。大 backbone 每个 transition 计算一次 features，小 flow head（约 backbone 参数的 2%）并行生成各 patch 的 stochastic difference。", r"ARTM/FHTM 使用 independent linear process，每个 \(t\) 重新采样 base noise，并以 causal factorization 逐 token 生成 \(X_{t+1}\)。FHTM 的 attention 完全 causal，可放进标准 LLM；代价是每个 transition 的 backbone forwards 随 image token 数增长。理论上 \(\mathbb E[Y\mid X_t=x]\) 等于 flow-matching marginal velocity，且 \(T\to\infty\) 时 DTM 收敛到 Euler FM。"),
            sec("核心结果与证据", r"Figure 7 显示 DTM/FHTM 在獾、机器人标牌、自由女神像、飞机与文字牌等 prompts 上能同时处理对象、风格和文字；但图中失败/随机 seed 未完整展示。", r"PartiPrompts 上 DTM 用 32 backbone NFEs 报告 CLIPScore 26.8、PickScore 21.2、ImageReward 0.53、UnifiedReward 5.12；FM 用 256 NFEs 对应 26.0、21.0、0.23、4.78。GenEval overall 为 DTM 0.54、MAR 0.52、FM 0.47。DTM 并非 CLIPScore 唯一最佳，MAR/三步 causal variants 可到 27.0。", r"优化 sampling 时，DTM 以 16 backbone forwards 的 kernel time 1.6 s 达到 CLIPScore 26.8、PickScore 21.1；FM 128 forwards 为 10.8 s、26.0、21.0，约 7× speedup。ARTM/FHTM 没有该速度优势，三 transition 的 NFE 约为 \(3\times256\)，论文明确把 causal integration 与高 sampling cost 作为 tradeoff。"),
            sec("有效性与局限", r"比较虽固定数据、backbone 与 optimizer，但所有 baselines 是作者重实现；350M licensed dataset 不公开，无法外部 exact reproduce。自动 preference metrics 与 GenEval 不等于人类盲评或 memorization audit；Figure 7 是 cherry-picked samples。", r"DTM 的小 head 在每步独立生成 patches，限制 kernel expressiveness；加大 patch kernel 主要帮助极少 transition steps。ARTM/FHTM 成本高且尚未在真正多模态 LLM 中展示 reasoning。\(T\to\infty\) 收敛只说明连续极限，不能保证有限 \(T\)、有限网络的误差单调。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2506.23589。全文 41 页，PDF SHA-256：313020feeb16473e8aaef1b2aec285e1b3e47cb5c8a202caeae667b4f6159e1d。", r"复现需固定 350M data snapshot、SDXL-VAE/Chameleon tokenizer、1.7B DiT、40M head、Flan-UL2 encoder、500k iterations、batch 2048、transition count、head ODE steps、activation caching、metric checkpoints 与 inference hardware。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section 2.1，把 TM 写成 supervising process、\(Y\) parameterization 与 \(B\mid A\) model 三元组；再看 DTM Eqs. (10)–(14) 和连续极限定理。随后比较 Figure 7 与 Tables 1–3，最后读 kernel expressiveness、independent process 和 causal-cost ablations。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2506.23589/figure-7-transition-samples.webp", "label": "Figure 7", "visual_type": "comparison", "evidence": "paper.pdf p. 8, Figure 7", "alt_text": "FM、MAR、FHTM、DTM 在多组文本提示下的生成图像并列比较。", "caption": "有限随机 transition kernels 在若干复杂提示上改善属性与文字匹配；图像样例需结合统一设置下的指标。", "selection_rationale": "Figure 7 是最具可视性的主结果，优先于抽象架构图和数据表。"},
        "figure_refs": [figure("2506.23589", "figure-7-transition-samples.webp", "Figure 7", 8, "compare finite-transition and baseline samples", "Four columns compare FM, MAR, FHTM and DTM across object, style and text prompts.", "Expressive stochastic transitions can improve finite-step text adherence and image quality.", "The examples are selected; aggregate metrics and compute costs provide the quantitative evidence.")],
        "equation_refs": [
            {"label": "Difference transition", "latex": r"X_t=\left(1-\frac{t}{T}\right)X_0+\frac{t}{T}X_T,\qquad Y=X_T-X_0,\qquad X_{t+1}=X_t+\frac{Y}{T}", "role": "define DTM's finite stochastic step", "symbols": {"T": "number of transitions", "Y": "endpoint difference latent"}, "evidence": "paper.pdf p. 5, Eqs. (10)–(12)", "interpretation": "The network samples a conditional endpoint difference rather than evaluating only its mean velocity."},
            {"label": "Flow-matching limit", "latex": r"\mathbb E[Y\mid X_t=x]=\mathbb E[X_T-X_0\mid X_t=x]=u_t(x)", "role": "connect DTM to the marginal flow velocity", "symbols": {"u_t": "flow-matching velocity", "Y": "DTM difference latent"}, "evidence": "paper.pdf p. 6, Eq. (14)", "interpretation": "As transitions become infinitesimal, stochastic DTM steps concentrate around the Euler flow-matching update."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: TM framework, DTM/ARTM/FHTM and FM limit", "paper.pdf pp. 8–10: controlled text-to-image results, efficiency and limitations", "source PDF SHA-256 313020feeb16473e8aaef1b2aec285e1b3e47cb5c8a202caeae667b4f6159e1d", "Evidence status: full-text verified; no independent reproduction performed."],
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
