#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 009."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_id: str, topic: str) -> dict[str, object]:
    return {
        "program": "Collection", "catalog": "Paper Collection",
        "catalog_record_id": record_id, "catalog_record_ids": [record_id],
        "catalog_topic": topic, "collection_date": "2026-08-23",
        "sampled_at": "2026-08-28", "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection", "candidate_count": 452,
    }


def meta(arxiv_id: str, version: str, title: str, authors: list[str], categories: list[str],
         primary: str, published: str, abstract: str) -> dict[str, object]:
    return {"arxiv_id": arxiv_id, "version": version, "title": title, "authors": authors,
            "categories": categories, "primary_category": primary, "published": published,
            "abstract": abstract, "comment": ""}


def figure(arxiv_id: str, filename: str, label: str, page: int, role: str,
           alt: str, caption: str, interpretation: str) -> dict[str, object]:
    return {"label": label, "asset_path": f"assets/collection-figures/{arxiv_id}/{filename}",
            "section": "核心结果与证据", "role": role,
            "evidence": f"paper.pdf p. {page}, {label}", "alt_text": alt,
            "caption": caption, "interpretation": interpretation}


CARDS = [
    {
        "arxiv_id": "2307.02284", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2307.02284",
        "title_en": "Universal Scaling Laws of Absorbing Phase Transitions in Artificial Deep Neural Networks", "title_zh": "人工深度神经网络中吸收相变的普适缩放律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("7419ddc22aa2fd0a", "Scaling Laws"),
        "verified_metadata": meta("2307.02284", "v3", "Universal Scaling Laws of Absorbing Phase Transitions in Artificial Deep Neural Networks", ["Keiichi Tamai", "Tsuyoshi Okubo", "Truong Vinh Truong Duy", "Naotake Natori", "Synge Todo"], ["stat.ML", "cond-mat.dis-nn", "cond-mat.stat-mech", "cs.LG"], "stat.ML", "2023-07-05T13:39:02Z", "Deterministic signal collapse near the edge of chaos is analyzed as an absorbing transition, with mean-field and directed-percolation scaling in MLPs and CNNs."),
        "sections": [
            sec("作者信息", r"作者：Keiichi Tamai、Tsuyoshi Okubo、Truong Vinh Truong Duy、Naotake Natori、Synge Todo；arXiv:2307.02284v3。全文 16 页。"),
            sec("研究问题", r"深网在 edge of chaos 附近出现发散的相关深度，但“临界初始化有利”并没有说明有限宽度、网络深度与泛化怎样共同缩放。论文问：两个输入信号在逐层传播时合并成同一状态，能否严格类比非平衡统计物理中的吸收相变，并由 universality class 给出超越具体激活函数的定量规律？"),
            sec("背景", r"网络初始化后前向动力学是确定的：若两个 preactivations 在某层完全相同，之后永远不能分离，因此 \(\rho=0\) 是吸收态。权重方差 \(\sigma_w\) 和偏置方差 \(\sigma_b\) 控制 ordered 与 chaotic 两相；最大 Lyapunov 指数的变号给出稳定性边界。", r"把层号 \(l\) 当作时间，输入或通道的空间坐标当作真实空间，order parameter \(\rho\) 描述两信号的去相关程度。全连接网络是 mean-field 极限；卷积局域性和有限通道涨落则允许 directed-percolation 型传播。"),
            sec("模型与方法", r"对无限宽 MLP，作者用 covariance mean-field recursion 推导 fixed point 与 correlation depth。取 \(\rho^{(l)}=1-c^{(l)}\)，在临界点附近得到吸收相变缩放：\(\beta=1\)、\(\nu_\parallel=1\)，而激活函数差异进入非普适 metric factors \(\kappa,\gamma\)。", r"有限宽时 leading non-Gaussian correction 为 \(O(n^{-1})\)，作者提出 \(\rho(l;n)\simeq n^{-1}f(l/n)\)。CNN 中局部耦合加入扩散项与 multiplicative noise，数值检验一维和二维 directed percolation 的已知临界指数。"),
            sec("核心结果与证据", r"Figure 1 把四层证据放在一张图：\((\sigma_w,\sigma_b)\) 相图、有限宽最大 Lyapunov 指数、order parameter 随深度衰减，以及 tanh/erf/sin 经 metric factors 重标度后的 data collapse。以 \(\sigma_b=0.3\) 为例，tanh 临界点约 \(\sigma_{w,c}=1.39558\)。", r"MLP 的临界衰减为 \(\rho(l)\sim(\kappa l)^{-1}\)。有限宽拟合表明要接近无限宽流，需要 \(n\gtrsim\mu L\)；增大 \(\kappa\) 可用较浅网络获得临界记忆，却通常伴随更大的宽度成本 \(\mu\)。", r"有限通道 CNN 的 collapse 与 directed percolation 相符：一维使用 \(\beta\approx0.27649,\nu_\parallel\approx1.73385\)，二维使用 \(\beta\approx0.58,\nu_\parallel\approx1.29\)。这支持 universality 的结构解释，但仍是特定随机网络上的数值证据。"),
            sec("有效性与局限", r"临界边界只是必要而非充分条件。作者的 NTK 分析表明 \(\kappa L\) 太小会使 kernel 近 rank-1，太大则使 test kernel 近似与输入无关；两者都损害训练或泛化。合适窗口还依赖数据的 cosine-distance 分布，不能由一个普适常数确定。", r"理论以随机初始化、特定参数化和简化 MLP/CNN 为主；finite-width correction 的 metric factor \(\mu\) 由拟合得到，尚无闭式推导。训练后的 feature learning、残差连接、normalization 与现代大模型可能改变或破坏吸收态结构。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2307.02284。全文 16 页，PDF SHA-256：7419ddc22aa2fd0a4c710d64274d5d0a84f9abf49a0e89a474a0ea9c7ed7c223。", r"复现应固定激活函数、\(\sigma_w,\sigma_b\)、宽度/通道、深度、卷积维数与 kernel、输入 cosine distance、独立初始化次数和临界点拟合区间；data collapse 必须同时报告未重标度曲线。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把 phase boundary、Lyapunov 稳定性和 order-parameter collapse 对齐；再读 Eqs. (17)、(20)–(23) 分清普适指数与非普适 metric factor。最后看 Figure 3/4 的有限宽和 CNN 检验，再读 NTK 的 \(\kappa L\) 两端极限，避免把 edge of chaos 简化成单点调参处方。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2307.02284/figure-1-absorbing-transition.webp", "label": "Figure 1", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "有序—混沌相图、Lyapunov 指数、序参量演化和缩放坍缩的四联图。", "caption": r"信号传播的有序—混沌边界被重写为吸收相变；临界指数普适，而 \(\kappa\) 等 metric factors 决定具体网络的深度记忆。", "selection_rationale": "该图同时显示相图、稳定性和 data collapse，是论文核心论证的完整视觉摘要。"},
        "figure_refs": [figure("2307.02284", "figure-1-absorbing-transition.webp", "Figure 1", 2, "connect edge-of-chaos dynamics to absorbing-transition scaling", "相边界、Lyapunov 指数、序参量与重标度结果。", "不同激活函数经非普适尺度因子重标度后落到同一临界曲线。", "The collapse supports a universality class, while the metric factors remain architecture-specific.")],
        "equation_refs": [
            {"label": "Absorbing-state order parameter", "latex": r"\rho^{(l)}=1-c^{(l)}", "role": "measure separation of two propagated signals", "symbols": {"rho": "order parameter", "c": "mean-field correlation coefficient", "l": "hidden-layer index"}, "evidence": "paper.pdf p. 4, Eq. (20)", "interpretation": "Once rho reaches zero, deterministic forward propagation cannot regenerate signal differences."},
            {"label": "Mean-field critical exponents", "latex": r"\rho^*\propto\tau^\beta,\qquad \xi_\parallel\propto|\tau|^{-\nu_\parallel},\qquad \beta=\nu_\parallel=1", "role": "state the absorbing-transition scaling near the MLP critical point", "symbols": {"tau": "distance from criticality", "xi_parallel": "correlation depth", "beta": "order-parameter exponent"}, "evidence": "paper.pdf p. 4, Eqs. (17)–(21)", "interpretation": "Activation choices change metric factors but not these mean-field exponents."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: phase diagram and universal MLP scaling", "paper.pdf pp. 6–9: NTK, finite-width and directed-percolation tests", "source PDF SHA-256 7419ddc22aa2fd0a4c710d64274d5d0a84f9abf49a0e89a474a0ea9c7ed7c223", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2308.05695", "source_version": "v4", "source_pdf": "https://arxiv.org/pdf/2308.05695",
        "title_en": "Masked Diffusion as Self-supervised Representation Learner", "title_zh": "Masked Diffusion：作为自监督表征学习器的掩码扩散",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("5b9a89dd6954b815", "Field Theory"),
        "verified_metadata": meta("2308.05695", "v4", "Masked Diffusion as Self-supervised Representation Learner", ["Zixuan Pan", "Jianxu Chen", "Yiyu Shi"], ["cs.CV"], "cs.CV", "2023-08-10T16:57:14Z", "A time-dependent patch-masking process replaces Gaussian noising in diffusion-style pretraining and is evaluated for few-shot semantic segmentation."),
        "sections": [
            sec("作者信息", r"作者：Zixuan Pan、Jianxu Chen、Yiyu Shi；arXiv:2308.05695v4。全文 19 页。Paper Collection 将其归入 Field Theory 主题，但论文本身属于计算机视觉与自监督分割。"),
            sec("研究问题", r"DDPM 的 U-Net 中间特征可用于像素级语义任务，但生成能力、Gaussian denoising 与表征质量纠缠在一起。论文问：若保留“连续腐蚀强度 + time-aware reconstruction”结构，却把加性噪声替换成 patch masking，能否获得更适合少标签分割的表示？"),
            sec("背景", r"扩散预训练对一系列 noise levels 做去噪，可被视为许多腐蚀强度共享参数的 denoising autoencoder。MAE 则遮住 patches 并重构像素，但通常只在单一 masking regime 下训练。MDM 将两者的有效自由度拆开：腐蚀类型取 masking，扩散时间 \(t\) 仍控制强度。", r"作者用 SSIM 而非纯 MSE，使重构损失偏向局部结构与对比度；这更接近 dense segmentation 需要的几何信息，但也使结论与 loss choice 不可分离。"),
            sec("模型与方法", r"给定 \(H\times W\times C\) 图像，划分为 \(N=HW/P^2\) 个 patches；均匀采样 \(t\in[1,T]\)，令 masking ratio \(R_m=t/(T+1)\)，随机置零 \(\lfloor R_mN\rfloor\) 个 patches。time-aware U-Net 接收 \(x_t,t\) 并重构完整 \(x_0\)。", r"预训练后冻结 U-Net，从多个尺度和 timesteps 抽取特征，拼接并训练轻量 segmentation network。Figure 2 明确分离 reconstruction pretraining 与 label-limited downstream training。"),
            sec("核心结果与证据", r"Figure 2 显示同一 encoder–decoder 先从不同遮挡率恢复图像，再把多尺度 representations 交给 segmentation net；它说明 MDM 的“diffusion”主要是腐蚀强度轴，而非学习反向 Gaussian SDE。", r"GlaS 仅 8 个标注样本时，MDM Dice/IoU 为 \(91.60\pm0.69/84.51\pm1.15\)，DDPM 为 \(90.30\pm0.47/82.32\pm0.77\)。MoNuSeg 仅 3 个标注样本时，MDM Dice/AJI 为 \(79.71\pm0.75/66.43\pm1.02\)，DDPM 为 \(74.37\pm3.08/60.03\pm3.48\)。", r"FFHQ-34/CelebA-19 mIoU 为 \(60.34\pm0.15/59.57\pm0.13\)，略高于 DDPM 的 \(59.36\pm0.17/58.86\pm0.12\)。消融中 fixed-\(t\) MDM 退化为 86.82 Dice，而多 \(t\)+SSIM 达到 91.60，支持多级腐蚀和结构损失共同起作用。"),
            sec("有效性与局限", r"作者明确限制：实现只测试 U-Net、两个医学和两个人脸分割数据集；没有大规模通用 segmentation、分类、检测或跨架构迁移。MDM 与比较方法的预训练迭代、checkpoint 来源和结构不同，不能把表中差异完全归因于 masking。", r"MDM 并非标准概率扩散模型，也没有 likelihood 或无条件生成检验；“denoising 不是必需”只针对表征学习。SSIM 的收益依赖下游结构偏置，MAE 上反而变差，因此不是普适 reconstruction objective。医学数据的样本数与独立划分也较小。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2308.05695；代码：https://github.com/zx-pan/mdm/。全文 19 页，PDF SHA-256：e1f8afc04383576873de25cc51ddce929b36622bcb411c254ce55d57012fa37a。", r"复现需固定 patch size、\(T\)、timestep sampling、SSIM 常数、U-Net 层级、抽取 timesteps、feature interpolation、标注子集、pretraining iterations 和多次划分随机种子。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2，确认生成训练与分割训练的参数冻结关系；再读 masking ratio 和 Eq. (4) 的 SSIM objective。最后按 Table 1–4 分开看 full-label、few-shot、fixed-\(t\) 与 loss ablation，避免用单一 SOTA 结论掩盖训练协议差异。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2308.05695/figure-2-mdm-overview.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "Masked diffusion 重构预训练与下游分割训练的两阶段框图。", "caption": r"时间 \(t\) 控制 patch 遮挡率；冻结的 U-Net 表示被多尺度抽取后用于少标签分割。", "selection_rationale": "该图完整显示论文的两阶段方法与表征流向，比单独分割样例或数据表更能解释机制。"},
        "figure_refs": [figure("2308.05695", "figure-2-mdm-overview.webp", "Figure 2", 4, "show the corruption-reconstruction and downstream representation pipeline", "原图、遮挡、U-Net 重构和分割网络的两阶段流程。", "MDM 保留 time conditioning，却用结构遮挡替代 Gaussian noise。", "The diagram separates representation learning from generative diffusion claims.")],
        "equation_refs": [
            {"label": "Time-dependent masking ratio", "latex": r"R_m(t)=\frac{t}{T+1},\qquad N_{\mathrm{mask}}=\left\lfloor R_m(t)N\right\rfloor", "role": "turn diffusion time into a hierarchy of patch-corruption strengths", "symbols": {"t": "sampled timestep", "T": "number of corruption levels", "N": "number of image patches"}, "evidence": "paper.pdf p. 5, masking procedure", "interpretation": "A single U-Net learns reconstruction across a continuum of missing-information fractions."},
            {"label": "MDM reconstruction objective", "latex": r"\mathcal L_{\mathrm{MDM}}=\mathbb E_{t,x_0}\!\left[\frac{1-\operatorname{SSIM}\!\left(x_0,U_\theta(x_t,t)\right)}{2}\right]", "role": "align masked reconstruction with structural information needed for segmentation", "symbols": {"U_theta": "time-aware U-Net", "x_t": "masked image", "x_0": "clean target"}, "evidence": "paper.pdf p. 5, Eq. (4)", "interpretation": "The downstream gain reflects both multilevel masking and a structure-sensitive loss."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–6: masking process, SSIM loss and feature extraction", "paper.pdf pp. 7–10: segmentation comparisons, ablations and limitations", "source PDF SHA-256 e1f8afc04383576873de25cc51ddce929b36622bcb411c254ce55d57012fa37a", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2308.12355", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2308.12355",
        "title_en": "Renormalizing Diffusion Models", "title_zh": "重整化扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("e224d89f844755a5", "Renormalization Group"),
        "verified_metadata": meta("2308.12355", "v2", "Renormalizing Diffusion Models", ["Jordan Cotler", "Semon Rezchikov"], ["hep-th", "cs.LG", "hep-lat"], "hep-th", "2023-08-23T18:02:31Z", "Exact renormalization-group diffusion processes define physically interpretable score models and adaptive bridge samplers for lattice field theories."),
        "sections": [
            sec("作者信息", r"作者：Jordan Cotler、Semon Rezchikov；arXiv:2308.12355v2。全文 85 页，是一篇连接 exact RG、diffusion、lattice sampling 和量子变分方法的长篇理论工作。"),
            sec("研究问题", r"普通 normalizing flow 或 diffusion sampler 可拟合 lattice field distribution，却没有可解释的中间尺度；终点样本正确也不保证 learned path 是物理 RG flow。论文问：能否把正向 noising 明确选成一个 exact renormalization-group scheme，使反向 score model 学到受控的 inverse RG，并以沿程物理 observable 诊断采样器？"),
            sec("背景", r"RG 把 UV microscopic theory 连续粗粒化为 IR effective theory；diffusion 把复杂数据分布推向简单 prior。两者的数学核心都是概率测度的 Markov semigroup。若正向 SDE 就是 Carosso 或 Polchinski ERG，反向 SDE 的 score 便是 effective action 对场的梯度。", r"这还给出 adaptive bridge/parallel tempering：IR 分布易采样，learned inverse maps 提议 UV 配置，Metropolis 或 auxiliary MCMC 可校正。中间尺度不再是任意 latent，而对应 cutoff 与 renormalized couplings。"),
            sec("模型与方法", r"Carosso lattice flow 为 stochastic heat equation：\(\partial_t\phi_t=\Delta\phi_t+\eta_t\)。高动量模按 \(e^{-|\hat p|^2t}\) 衰减并注入 Gaussian noise，长时先验可解析采样。反向过程加入 \(\sigma^2s_t[\phi]\)，score network 逼近 \(\nabla_\phi\log p_t\)。", r"作者提出 path-aware objective：端点用 \(\mathrm{KL}(p_{\theta0}\|p_0)\)，沿 RG 时间用 forward KL \(\int\lambda(t)\mathrm{KL}(p_t\|p_{\theta t})dt\)。另给 score-matching 版本，避免重复求解 neural ODE。实验在二维 lattice \(\phi^4\)、\(N=20\) 上比较该目标与只拟合 UV 的 reverse KL。"),
            sec("核心结果与证据", r"Figure 3 把任务画成两条相反箭头：正向 RG 从 microscopic field 逐步滤去短波；learned inverse 从可采样的 very coarse distribution 恢复细尺度。它说明模型要匹配的是整条尺度轨迹，而不只是两端分布。", r"Carosso 与 Polchinski schemes 的 field snapshots 视觉上很不同，但 renormalized mass 与 quartic coupling 的流速只差小因子；Polchinski 过快切掉高频而更难训练。RG scheme 因此类似 diffusion noise schedule：物理等价不代表数值等价。", r"相同 1000 gradient steps 下，Figure 7/8 显示 Eq. (5.22) learned flows 对 \(m_R,Z,\lambda_R\) 等 observables 一贯比 reverse-KL flow 更接近 true Carosso flow。作者强调只看 field images 无法发现差异，必须测量物理估计量；负质量案例的 quartic coupling 对所有模型都难估。"),
            sec("有效性与局限", r"数值示范限于小型二维 scalar \(\phi^4\) lattice；尚未证明在大体积、临界 slowing、gauge fields、fermions 或拓扑扇区上优于 HMC、multigrid、cluster 或 worm algorithms。沿程 forward-KL 需要 true RG samples，训练成本依赖昂贵 UV sampler。", r"Carosso 长时固定为 Gaussian 的表象需配合 field renormalization 才描述非平凡 fixed point。observable agreement 是比视觉更强的诊断，但仍不等同于全分布、autocorrelation time 或独立 effective-sample-rate 改进。文章提出多个算法方向，只有其中一部分做了数值测试。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2308.12355。全文 85 页，PDF SHA-256：c89d33445df2dd4b866b54bb46663dd8afaf92ef04b22decd0c5f8dcdb3b7a29。", r"复现需固定 lattice convention、\(L,N,m^2,\lambda\)、Carosso/Polchinski kernel、field rescaling、RG-time grid、NUTS warmup、observable estimators、prior 与 1000-step optimizer budget。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 3 建立正/逆 RG 的尺度方向；再读 Eqs. (4.32)、(5.22)–(5.25)，把 exact RG SDE、path objective 与 reverse score 对齐。最后看 Figure 6–8，重点比较 renormalized observables 而非样本外观，并区分“学到 RG flow”与“最终采样效率更高”。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2308.12355/figure-3-rg-inverse.webp", "label": "Figure 3", "visual_type": "schematic", "evidence": "paper.pdf p. 9, Figure 3", "alt_text": "微观场正向粗粒化和从粗粒化先验反向生成微观场的双向流程。", "caption": "正向 exact RG 逐尺度滤去 UV 模式；反向 diffusion 学习 physically interpretable inverse flow，而非任意 latent interpolation。", "selection_rationale": "该图是 85 页文章最清晰的概念总览，直接连接 RG、扩散和多尺度采样。"},
        "figure_refs": [figure("2308.12355", "figure-3-rg-inverse.webp", "Figure 3", 9, "visualize forward coarse-graining and learned inverse RG", "场配置沿正向粗粒化变平滑，并沿学习到的反向动力学恢复细尺度。", "模型的中间状态对应明确 cutoff，而非无物理标签的噪声层级。", "A physically meaningful path enables diagnostics with renormalized observables.")],
        "equation_refs": [
            {"label": "Carosso RG diffusion", "latex": r"\partial_t\phi_t(n)=\Delta\phi_t(n)+\eta_t(n),\qquad \phi_0(n)=\phi(n)", "role": "instantiate exact coarse-graining as a stochastic diffusion", "symbols": {"phi_t": "lattice field at RG time t", "Delta": "discrete Laplacian", "eta": "Gaussian noise"}, "evidence": "paper.pdf p. 33, Eq. (4.32)", "interpretation": "High-frequency field modes are smoothed while stochastic noise preserves a nontrivial probability flow."},
            {"label": "RG-path variational objective", "latex": r"\mathcal J(\theta)=\mathrm{KL}(p_{\theta0}\|p_0)+\int_0^T\lambda(t)\,\mathrm{KL}(p_t\|p_{\theta t})\,dt", "role": "fit the entire physical RG trajectory instead of only the UV endpoint", "symbols": {"p_t": "true RG-flowed law", "p_theta_t": "learned intermediate law", "lambda(t)": "scale weighting"}, "evidence": "paper.pdf p. 42, Eq. (5.22)", "interpretation": "Intermediate-scale observables constrain the learned sampler beyond endpoint likelihood."},
            {"label": "Reverse RG SDE", "latex": r"d\phi_t=\left[-\Delta\phi_t+\sigma^2s_t(\phi_t)\right]dt+\sigma\,dB_t", "role": "generate fine fields by reversing the chosen RG diffusion", "symbols": {"s_t": "field score", "B_t": "Brownian field", "sigma": "noise strength"}, "evidence": "paper.pdf p. 44, Eq. (5.25)", "interpretation": "The learned score is the force that restores UV structure along a physically specified scale flow."},
        ],
        "evidence_refs": ["paper.pdf pp. 31–44: exact RG diffusion and learning objectives", "paper.pdf pp. 63–68: scheme comparison and lattice phi-four experiments", "source PDF SHA-256 c89d33445df2dd4b866b54bb46663dd8afaf92ef04b22decd0c5f8dcdb3b7a29", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2309.10668", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2309.10668",
        "title_en": "Language Modeling Is Compression", "title_zh": "语言建模就是压缩",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("4d38daadaeb5b4d6", "Transformer Theory"),
        "verified_metadata": meta("2309.10668", "v2", "Language Modeling Is Compression", ["Grégoire Delétang", "Anian Ruoss", "Paul-Ambroise Duquenne", "Elliot Catt", "Tim Genewein", "Christopher Mattern", "Jordi Grau-Moya", "Li Kevin Wenliang", "Matthew Aitchison", "Laurent Orseau", "Marcus Hutter", "Joel Veness"], ["cs.LG", "cs.AI", "cs.CL", "cs.IT"], "cs.LG", "2023-09-19T14:50:38Z", "Arithmetic coding turns predictive models into lossless compressors, enabling cross-modal evaluation and a model-size-adjusted view of scaling."),
        "sections": [
            sec("作者信息", r"作者：Grégoire Delétang 等十二人；arXiv:2309.10668v2，ICLR 2024。全文 18 页。"),
            sec("研究问题", r"语言模型以 cross-entropy 训练，而 lossless compressor 以 bit length 评价；两者由 Shannon coding theorem 等价。论文问：把 foundation model 真正接到 arithmetic coder 后，能否用压缩率作为跨文本、图像、音频的统一预测指标，并在把模型参数本身计入 code length 后重新解释 scaling law？"),
            sec("背景", r"一个 predictor 给出条件概率 \(\hat\rho(x_i\mid x_{<i})\)。Arithmetic coding 按这些概率递归细分 \([0,1)\)，序列占据的区间宽度决定 bit 数，理想长度接近 \(-\log_2\hat\rho(x_{1:n})\)。反向地，compressor 的长度差可构造下一符号概率。", r"因此 log loss 不是压缩的比喻，而是忽略有限精度常数后的实际 expected codelength。真正的 description length 还应包含模型程序/参数；这使“更大模型总更好”的结论依赖被压数据量。"),
            sec("模型与方法", r"Figure 1 用字符串 AIXI 展示 arithmetic encoder：每读一个字符，模型概率把区间再次切分；最终从 4 bytes 得到 7-bit code。实验将 Transformer、Llama 2 与 Chinchilla 的 token probabilities 转成 bytes 上的算术码，与 gzip、LZMA2、PNG、FLAC 比较。", r"数据为各 1GB 的 enwik9、ImageNet patches、LibriSpeech 和随机 bytes。作者同时报告 raw compression rate 与 adjusted rate；后者把 float16 参数按每参数 2 bytes 加入 compressed size。"),
            sec("核心结果与证据", r"Figure 1 把概率预测和可逆编码一一对应：高概率字符选中较宽子区间，需要较少新增 bits；解码器用相同 \(\hat\rho\) 从最终区间恢复原序列。", r"忽略模型大小时，Chinchilla 70B 将 ImageNet patches 压到原始大小的 43.4%，优于 PNG 58.5%；LibriSpeech 压到 16.4%，优于 FLAC 30.3%。但 1GB 数据上计入参数后，70B 的 adjusted rate 约 14000%，远差于经典 compressor。", r"小 Transformer 的 adjusted curves 都有最优模型尺寸：测试集越大，最优参数量越大；越过该点，新增参数 bytes 超过 prediction gain。ASCII tokenization 在 38M 模型上 raw rate 6.4%，优于 BPE-20K 的 9.0%，说明短序列与大 alphabet 的代价需共同计算。"),
            sec("有效性与局限", r"跨模态 raw rate 的惊艳数字不含数十到数百 GB 参数，不能直接表示可部署 compressor。作者估计 foundation model 需 TB 级数据才能摊薄模型；编码还需逐 token 运行巨大网络，速度与能耗没有和 PNG/FLAC 公平比较。", r"压缩率给出平均 log probability，不保证 autoregressive sample 的感知质量；Figure 3 中 gzip 与 Chinchilla 的图像续写都不连贯，误差会累积。ImageNet 被逐行独立编码，输入转换和 tokenizer 也改变序列结构；训练语料中仍不能绝对排除编码后的图像/音频泄漏。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2309.10668；代码：https://github.com/google-deepmind/language_modeling_is_compression。全文 18 页，PDF SHA-256：78c4e944f08a21d111b2818abce424a2355972b48c07e0b2d67008893ee71bf0。", r"复现需固定 byte conversion、tokenizer、context length、arithmetic-coder precision、model checkpoint、参数存储位宽、数据切片和 raw/adjusted 分母，并同时报告吞吐与内存。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 并手算区间宽度，确认 log loss 如何变成 bits；再读 Eq. (2) 的 cross-entropy 恒等式。随后对照 Table 1 的 raw 与 adjusted 两半，再看 Figure 2 的 U-shaped size tradeoff；不要只引用 43.4%/16.4% 而忽略 70B 参数成本。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2309.10668/figure-1-arithmetic-coding.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "AIXI 四个字符在算术编码中逐次细分概率区间并输出二进制码。", "caption": "语言模型的条件概率直接决定 arithmetic code 的区间宽度；cross-entropy 因而就是期望 bit length。", "selection_rationale": "该图可视化了全文的核心等价关系，比压缩率表更能解释为什么语言建模就是压缩。"},
        "figure_refs": [figure("2309.10668", "figure-1-arithmetic-coding.webp", "Figure 1", 2, "visualize probability-to-bitstream conversion", "A、I、X、I 的条件概率递归切分单位区间。", "更准确的 predictor 为真实符号分配更宽区间，从而输出更短 code。", "The mapping is lossless only when encoder and decoder share the same predictive distribution.")],
        "equation_refs": [
            {"label": "Expected predictive codelength", "latex": r"H(\rho,\hat\rho)=\mathbb E_{x\sim\rho}\!\left[-\sum_{i=1}^{n}\log_2\hat\rho(x_i\mid x_{<i})\right]", "role": "identify cross-entropy with expected lossless code length", "symbols": {"rho": "data source", "rho_hat": "predictive model", "x_i": "next symbol"}, "evidence": "paper.pdf p. 4, Eq. (2)", "interpretation": "Maximum likelihood minimizes the number of arithmetic-coded bits up to coding overhead."},
            {"label": "Prediction from a compressor", "latex": r"\hat\rho(b\mid x_{<i})=2^{\ell_c(x_{<i})-\ell_c(x_{<i}b)}", "role": "turn code-length increments into next-symbol probabilities", "symbols": {"ell_c": "compressed length under compressor c", "b": "candidate next symbol"}, "evidence": "paper.pdf p. 4, compression-based sequence prediction", "interpretation": "A compressor defines an energy over continuations, although finite code lengths may require normalization and can be biased."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: arithmetic coding and prediction-compression equivalence", "paper.pdf pp. 5–9: cross-modal rates, adjusted scaling and limitations", "source PDF SHA-256 78c4e944f08a21d111b2818abce424a2355972b48c07e0b2d67008893ee71bf0", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2310.02244", "source_version": "v5", "source_pdf": "https://arxiv.org/pdf/2310.02244",
        "title_en": "Tensor Programs VI: Feature Learning in Infinite-Depth Neural Networks", "title_zh": "Tensor Programs VI：无限深神经网络中的特征学习",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("e09961a5caff848f", "Training Dynamics"),
        "verified_metadata": meta("2310.02244", "v5", "Tensor Programs VI: Feature Learning in Infinite-Depth Neural Networks", ["Greg Yang", "Dingli Yu", "Chen Zhu", "Soufiane Hayou"], ["cs.NE", "cond-mat.dis-nn", "math.PR"], "cs.NE", "2023-10-03T17:50:40Z", "Depth-muP classifies residual-network depth scalings, identifies a feature-learning/diversity optimum for one-layer blocks, and proves limits for deeper blocks."),
        "sections": [
            sec("作者信息", r"作者：Greg Yang、Dingli Yu、Chen Zhu、Soufiane Hayou；arXiv:2310.02244v5。全文 57 页。"),
            sec("研究问题", r"\(\mu\)P 允许从窄网络把最优超参数迁移到宽网络。论文问：对 residual depth \(L\)，branch multiplier 与 learning rate 应怎样共同缩放，才能在 \(L\to\infty\) 时既保持 \(O(1)\) feature change，又避免相邻层变成冗余的 neural ODE，并由浅网预测深网超参数？"),
            sec("背景", r"初始化稳定只要求独立 residual increments 的方差不爆炸；训练时各层 updates 高度相关，累积律不同。因此 branch scaling 与 optimizer-specific learning-rate scaling 必须一起分类。", r"作者把最优性分成 feature learning 和 feature diversity：前者要求训练引起有限非零表示变化，后者要求深度方向仍保留独立结构，而不是所有相邻层输出平滑同质化。"),
            sec("模型与方法", r"对 block depth 1，Depth-\(\mu\)P 取 \(x^l=x^{l-1}+aL^{-1/2}g^l(x^{l-1};W^l)\)。SGD 的参数更新本身已有 \(L^{-1/2}\) 梯度因子，因此 base learning rate 保持 \(O(1)\)；Adam 对梯度尺度不敏感，learning rate 取 \(\eta L^{-1/2}\)。", r"作者分类 branch exponent \(\alpha\) 与 update exponent \(\gamma\)：\(\alpha+\gamma<1\) 更新爆炸，\(>1\) feature learning 消失；\(\alpha+\gamma=1\) 且 \(\alpha>1/2\) 形成冗余 smooth limit，唯一同时 maximal learning/diversity 的点是 \(\alpha=\gamma=1/2\)。"),
            sec("核心结果与证据", r"Figure 3 比较 homogeneous nonlinearities：在同一 CIFAR-10/Adam 设置下，absolute value 的最小 log loss 随深度下降得比 ReLU 更快；作者解释 \(\phi'(h)=\operatorname{sign}(h)\) 最大化跨层 decorrelation，从而提高 feature diversity。", r"Depth-\(\mu\)P 在单层 residual blocks 上实现 depthwise hyperparameter transfer，并可训练上千 blocks；但 pre-nonlinearity ResNet 虽然 transfer，8 层后几乎无性能增益，说明 transfer 不是架构质量的充分条件。", r"block depth \(\ge2\) 出现不可能性：为保 diversity，block 内多层 weights 在极限中被迫加性而非乘性耦合，最优超参数随深度漂移。Megatron/Common Crawl 中更深模型早期更差、中期最优 learning rate 近 \(O(1)\)、训练末期才近 \(L^{-1/2}\)，没有单一全程 transfer law。"),
            sec("有效性与局限", r"正面定理针对 infinite width 后 infinite depth、residual block depth 1 和特定 homogeneous nonlinearities；finite width/depth、normalization、attention 与训练时长可改变最优 scaling。absolute value 在本文设置中改善 loss，不代表对所有数据与架构优于 ReLU，也可能改变表达偏置。", r"作者对现代 Transformer 给出的是限制性结论而非现成 recipe：\(L^{-1/2}\) 可能迁移 maximum viable learning rate，却不能同时对齐训练全过程的 optimum。理论的“唯一最优”依赖选定的参数化空间和 feature-diversity 定义。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2310.02244。全文 57 页，PDF SHA-256：e1777ad3d3a77e870a3c3ef8daa7bd05ad186a94cd3bf0f68e552c11b7e746e8。", r"复现需固定 widthwise \(\mu\)P、block depth、pre/post-nonlinearity、normalization、optimizer、\(a,\eta\)、训练 steps/epochs 与数据；迁移图应展示完整二维超参数 surface，而非只报最佳点。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Table 1 与 Eq. (1)，分别跟踪初始化 increments 和训练 updates 的 \(L\) 标度；再看 \((\alpha,\gamma)\) 分类和 feature-diversity 定义。随后用 Figure 3 检验 nonlinearity 机制，最后读 block-depth-2 与 Megatron 反例，明确 Depth-\(\mu\)P 的适用边界。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2310.02244/figure-3-feature-diversity.webp", "label": "Figure 3", "visual_type": "data_plot", "evidence": "paper.pdf p. 18, Figure 3", "alt_text": "absolute-value 与 ReLU 残差网络在不同深度和学习率下的训练损失比较。", "caption": "absolute-value nonlinearity 提高跨层 feature diversity；在该 CIFAR-10 设置中，深度增加带来更低的最优训练损失。", "selection_rationale": "论文缺少更合适的可视化示意图；该图直接展示其最重要且反直觉的经验机制，优先于纯公式页。"},
        "figure_refs": [figure("2310.02244", "figure-3-feature-diversity.webp", "Figure 3", 18, "compare nonlinearities through depthwise feature diversity", "不同深度的 loss surface 以及 abs 与 ReLU 的最优损失曲线。", "absolute value 的 derivative 更强地 decorrelate 层间 updates，并在此实验中改善深度收益。", "The plot is empirical support within one setup, not a universal activation ranking.")],
        "equation_refs": [
            {"label": "Depth-muP residual scaling", "latex": r"x^l=x^{l-1}+\frac{a}{\sqrt L}\,g^l(x^{l-1};W^l)", "role": "balance independent initialization increments and correlated training updates", "symbols": {"L": "number of residual blocks", "a": "depth-transferable branch constant", "g_l": "one-layer residual block"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "Each initialized branch is order L^{-1/2}, while correlated update contributions accumulate to order one."},
            {"label": "Optimal depth exponents", "latex": r"\alpha+\gamma=1,\qquad \alpha=\gamma=\frac12", "role": "identify the unique block-depth-one limit with maximal feature learning and diversity", "symbols": {"alpha": "branch-multiplier exponent", "gamma": "effective-update exponent"}, "evidence": "paper.pdf p. 3, optimality classification", "interpretation": "Other stable feature-learning limits become layerwise redundant or unfaithful under the paper's classification."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: Depth-muP recipe and scaling intuition", "paper.pdf pp. 18–23: feature diversity, activation and block-depth experiments", "paper.pdf pp. 45–51: classification and impossibility results", "source PDF SHA-256 e1777ad3d3a77e870a3c3ef8daa7bd05ad186a94cd3bf0f68e552c11b7e746e8", "Evidence status: full-text verified; no independent reproduction performed."],
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
