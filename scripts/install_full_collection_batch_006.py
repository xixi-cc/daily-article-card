#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 006."""

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
        "sampled_at": "2026-08-26", "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection", "candidate_count": 452,
    }


def meta(arxiv_id: str, version: str, title: str, authors: list[str], categories: list[str],
         primary: str, published: str, abstract: str) -> dict[str, object]:
    return {"arxiv_id": arxiv_id, "version": version, "title": title, "authors": authors,
            "categories": categories, "primary_category": primary, "published": published,
            "abstract": abstract}


def figure(arxiv_id: str, filename: str, label: str, page: int, role: str,
           alt: str, caption: str, interpretation: str) -> dict[str, object]:
    return {"label": label, "asset_path": f"assets/collection-figures/{arxiv_id}/{filename}",
            "section": "核心结果与证据", "role": role,
            "evidence": f"paper.pdf p. {page}, {label}", "alt_text": alt,
            "caption": caption, "interpretation": interpretation}


CARDS = [
    {
        "arxiv_id": "2111.15141", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2111.15141",
        "title_en": "Path Integral Sampler: a stochastic control approach for sampling",
        "title_zh": "路径积分采样器：随机控制视角下的采样",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("1d621814988a5812", "Field Theory"),
        "verified_metadata": meta("2111.15141", "v2", "Path Integral Sampler: a stochastic control approach for sampling",
            ["Qinsheng Zhang", "Yongxin Chen"], ["cs.LG"], "cs.LG", "2021-11-30T05:50:12Z",
            "A Schrödinger-bridge sampler learned as stochastic optimal control, with path-space importance correction."),
        "sections": [
            sec("作者信息", "作者：Qinsheng Zhang、Yongxin Chen；arXiv:2111.15141v2，ICLR 2022。", "本卡核对 27 页全文。此处 path integral 是受控扩散轨道上的测度与作用量，不应与量子振幅的振荡积分混同。"),
            sec("研究问题", "目标密度只知道到归一化常数时，短链 MCMC 容易困在模态，显式 flow 又受可逆架构约束。论文问能否训练一条有限时间受控 SDE，把简单初态直接输运到目标分布。", "第二个问题是 learned controller 与离散积分必然不完美；作者需要可计算的偏差界与重要性权重，而不只是生成样本的视觉相似。"),
            sec("背景", r"Schrödinger bridge 在给定端点边缘分布时寻找相对参考扩散最可能的路径测度。Girsanov 定理把路径测度的 KL 写成控制能量，从而把采样变成终端代价加运行代价的随机最优控制。", r"数据处理不等式给出 (D_{\mathrm{KL}}(\mu_Q\Vert\mu)\le D_{\mathrm{KL}}(Q\Vert P))：控制的是整条路径，却约束终点样本误差。"),
            sec("模型与方法", r"受控过程为 (dx_t=u_t(x_t)dt+dw_t)。选择终端代价 (Psi(x_T)=\log[\mu^0(x_T)/\mu(x_T)]) 后，最优控制的终点边缘就是目标 (mu)。", "控制场用神经网络参数化；PIS-Grad 额外注入目标 score 以缓解分离模态下的 zero-forcing。训练通过离散 SDE 轨迹反向传播，采样时同时累积路径作用量。", "Figure 1 把无控扩散、终端势与受控路径束并排显示，直观说明控制不是末端重排，而是改变整条轨道测度。"),
            sec("核心结果与证据", r"理论上，若控制误差有界，终点的二阶 Wasserstein 误差满足 (W_2=O(\sqrt{Td(\Delta t+\epsilon)}))；这同时暴露维数、步长与策略误差的依赖。", "路径积分权重可校正次优控制与时间离散偏差，并无偏估计归一化常数；低 ESS 则直接警告校正由少数轨道支配。", "二维分离模态图中 PIS-Grad 比无 score 的 PIS-NN 覆盖更多模态；MG、Funnel 与 LGCP 的 100 次归一化常数实验中，带重权的 PIS-Grad 优于文中 AFT/SMC 配置。但比较预算并不完全等价：退火基线使用约十倍离散步。"),
            sec("有效性与局限", "保证依赖控制场误差的全局上界，实际神经网络训练并不能直接验证该前提；Wasserstein 小也不保证任意稀有事件估计稳定。", "重要性修正恢复期望的无偏性，但权重方差可随维度和时间迅速恶化；必须同时报告 ESS、权重尾部和多模态覆盖。", "数值任务以 toy densities、LGCP、丙氨酸二肽和 VAE latent 为主，尚不能直接推出高维场论采样的可扩展优势。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2111.15141；代码：https://github.com/qsh-zh/pis。", "全文 PDF 共 27 页，SHA-256：e0bb88baf8cf19b54d29195a6765aaf113de42fa7b5aab2d11658fd959175ac8。", "复现应固定 SDE 时域、Euler 步长、控制网络、score 是否注入、目标梯度实现和每个基线的总函数评估数；保存每条轨道的作用量、权重、ESS 与终点样本。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Figure 1 与 Theorem 1，重建终端势为何把随机控制变成目标采样。", "再读 Eqs. (16)–(19)，把近似误差界、重要性校正和归一化常数估计分成三个命题。", "最后核对实验的步数预算与权重版本；不要把未加权样本质量等同于无偏估计。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2111.15141/figure-1-control-bridge.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "无控扩散经终端代价变成命中双峰目标的受控路径束。", "caption": "终端势把参考扩散重新加权为 Schrödinger bridge；最优控制沿有限时域逐步塑造终点分布。", "selection_rationale": "该图直接呈现论文的物理核心：路径测度如何被控制场重整形；它比性能表更适合说明方法的因果结构。"},
        "figure_refs": [figure("2111.15141", "figure-1-control-bridge.webp", "Figure 1", 2, "visualize the controlled path measure", "PIS 的无控与最优受控扩散路径。", "终端代价选择目标密度，最优控制把参考终点分布推到双峰目标。", "Sampling is performed by changing the full trajectory measure, not by a terminal deterministic map.")],
        "equation_refs": [
            {"label": "Controlled diffusion", "latex": r"dx_t=u_t(x_t)\,dt+dw_t", "role": "define the trainable stochastic transport", "symbols": {"x_t": "state", "u_t": "control field", "w_t": "Brownian motion"}, "evidence": "paper.pdf p. 3, Eq. (2)", "interpretation": "The neural policy changes the drift while preserving stochastic exploration."},
            {"label": "Path importance weight", "latex": r"w^u(\tau)=\exp\!\left[-\int_0^T\!\left(\tfrac12\|u_t\|^2dt+u_t^\top dw_t\right)-\Psi(x_T)\right]", "role": "correct controller and discretization bias", "symbols": {"tau": "trajectory", "Psi": "terminal cost", "u_t": "learned control"}, "evidence": "paper.pdf p. 6, Eq. (17)", "interpretation": "Exact expectations remain available only when the path weights have tolerable variance."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: stochastic-control formulation, bounds and importance weights", "paper.pdf pp. 6–9: benchmark, molecular and latent-space experiments", "source PDF SHA-256 e0bb88baf8cf19b54d29195a6765aaf113de42fa7b5aab2d11658fd959175ac8", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2111.15640", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2111.15640",
        "title_en": "Diffusion Autoencoders: Toward a Meaningful and Decodable Representation", "title_zh": "扩散自编码器：走向有意义且可解码的表征",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("42643d6683734bf6", "Field Theory"),
        "verified_metadata": meta("2111.15640", "v3", "Diffusion Autoencoders: Toward a Meaningful and Decodable Representation", ["Konpat Preechakul", "Nattanat Chatthee", "Suttisak Wizadwongsa", "Supasorn Suwajanakorn"], ["cs.CV", "cs.LG"], "cs.CV", "2021-11-30T18:24:04Z", "A semantic encoder and conditional DDIM split image information into editable semantics and stochastic detail."),
        "sections": [
            sec("作者信息", "作者：Konpat Preechakul、Nattanat Chatthee、Suttisak Wizadwongsa、Supasorn Suwajanakorn；arXiv:2111.15640v3，CVPR 2022。", "本卡核对 23 页全文。"),
            sec("研究问题", "扩散模型的噪声轨迹可生成高质量图像，却不是紧凑、线性可操纵的语义坐标；GAN latent 较可编辑，但真实图像反演会丢失身份与细节。", "论文尝试把图像自由度分成低维语义子码与高维随机细节子码，并要求二者合起来近乎精确重构。"),
            sec("背景", "若 decoder 只靠紧凑 bottleneck，像素细节会被均方误差平均掉；若把全部信息放入 DDIM terminal latent，则可重构但难以语义解释。", "方法的物理类比是相关尺度分解：低维 z_sem 承载慢、全局自由度，x_T 承载高频和随机微观细节；这是一种学习到的分工，不是严格正交投影。"),
            sec("模型与方法", r"encoder (E_\phi(x_0)=z_{\mathrm{sem}}) 输出 512 维语义码；conditional noise predictor (epsilon_\theta(x_t,t,z_{\mathrm{sem}})) 构成 DDIM decoder。给定真实图像还可反演得到 (x_T)，所以完整码是 ((z_{\mathrm{sem}},x_T))。", "生成时另训练 latent DDIM 拟合 z_sem 分布，再从 Gaussian x_T 解码；属性编辑只沿 z_sem 中线性分类器法向移动。", "Figure 1 同时展示局部属性编辑与两张真实图像间插值，是“线性语义且可解码”的直接视觉检验。"),
            sec("核心结果与证据", "完整双码在 CelebA-HQ 重构达到 SSIM 0.991、LPIPS 0.011、MSE 6.07e-5；若随机采 x_T，仅 512D z_sem 的 LPIPS 为 0.073，说明语义码保留主体但不保留全部细节。", "T=20 时本方法 SSIM 0.927、LPIPS 0.050，超过 T=100 的 DDIM 的 0.917 与 0.063；条件语义减少了去噪阶段必须反推的信息。", "40 个属性的线性可分性 AUROC 为 0.925，高于文中 StyleGAN-W 反演的 0.891。FFHQ 无条件 FID 在 T=100 为 10.59，对应 DDIM 12.03；优势存在但不是数量级提升。"),
            sec("有效性与局限", "z_sem 与 x_T 的“语义/随机”分工由训练目标和可视化支持，却没有信息论上的唯一性；属性方向也可能纠缠身份、年龄与数据偏差。", "重构对比的 latent dimension 差异很大，训练图像数与公开预训练模型也不完全一致；不能从单表推断压缩率的公平排名。", "人脸编辑主要在 FFHQ/CelebA-HQ 上验证，线性属性轴会继承标签和人群偏差；真实应用需报告分组保持率与编辑外溢。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2111.15640；项目：https://Diff-AE.github.io/。", "全文 PDF 共 23 页，SHA-256：6a8d3ce5412f7ba3dd4610a9b7e719b4d6adcabc338487044de3c957e2c1aa26。", "复现需固定数据裁剪、训练图像数、z_sem 维数、DDIM 步数、反演方案和指标实现；同时保存身份相似度、属性分类器置信度与非目标属性漂移。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figures 1–3，区分 z_sem 改主体与 x_T 改细节。", "再核对 Tables 1–2 的训练预算、latent dimension 和步数，避免跨配置直接比较。", "最后读属性编辑与 limitations，把漂亮插值和可辨识、无偏的表征分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2111.15640/figure-1-editing-interpolation.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "真实人脸的发型、笑容、年龄编辑与连续插值。", "caption": "线性移动语义子码可改变属性；完整双码仍保留可逆重构所需的随机细节。", "selection_rationale": "首图直接展示语义坐标的可操纵性与解码质量；相较指标表，它同时保留真实图像端点、编辑方向与插值连续性。"},
        "figure_refs": [figure("2111.15640", "figure-1-editing-interpolation.webp", "Figure 1", 1, "show semantic edits and interpolation", "真实图像属性编辑与插值。", "z_sem 中的线性移动改变头发、表情或年龄，同时输出保持高保真。", "The visualization tests editability and detail retention, but not disentanglement uniqueness.")],
        "equation_refs": [{"label": "Conditional denoising objective", "latex": r"\mathcal L_{\mathrm{simple}}=\mathbb E_{x_0,\epsilon,t}\!\left[\|\epsilon_\theta(x_t,t,z_{\mathrm{sem}})-\epsilon\|_2^2\right]", "role": "train the diffusion decoder conditioned on semantic content", "symbols": {"z_sem": "semantic code", "x_t": "noisy image", "epsilon": "forward noise"}, "evidence": "paper.pdf p. 3, Eq. (6)", "interpretation": "Conditioning removes high-level ambiguity, allowing fewer denoising steps and a separate stochastic-detail code."}],
        "evidence_refs": ["paper.pdf pp. 2–4: two-part code and conditional DDIM", "paper.pdf pp. 5–8: reconstruction, editing and FID tables", "source PDF SHA-256 6a8d3ce5412f7ba3dd4610a9b7e719b4d6adcabc338487044de3c957e2c1aa26", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2206.13397", "source_version": "v7", "source_pdf": "https://arxiv.org/pdf/2206.13397",
        "title_en": "Generative Modelling With Inverse Heat Dissipation", "title_zh": "用逆热耗散进行生成建模",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("779731ba4665f15c", "Flow Matching"),
        "verified_metadata": meta("2206.13397", "v7", "Generative Modelling With Inverse Heat Dissipation", ["Severi Rissanen", "Markus Heinonen", "Arno Solin"], ["cs.CV", "cs.LG", "stat.ML"], "cs.CV", "2022-06-21T13:40:38Z", "A generative latent-variable model stochastically reverses the heat equation to impose an explicit coarse-to-fine image prior."),
        "sections": [
            sec("作者信息", "作者：Severi Rissanen、Markus Heinonen、Arno Solin；arXiv:2206.13397v7，ICLR 2023。", "本卡核对 55 页全文。"),
            sec("研究问题", "标准扩散在像素各向同性地加噪，没有显式使用自然图像的多尺度结构。作者问：若 forward destruction 改为二维热方程，使高频先衰减，能否把生成过程组织成从平均颜色、轮廓到纹理的逆热流？", "纯逆热方程病态且确定；模型必须加入非零噪声，使不同 forward paths 重叠，从而定义可学习的反向条件分布。"),
            sec("背景", r"热方程 (partial_t u=\Delta u) 在离散余弦基中对每个波数独立衰减：(u_k=V\exp(-\Lambda t_k)V^\top u_0)。高波数具有更大的 Laplacian 本征值，因此更快消失。", r"自然图像近似 (1/f^\alpha) 功率谱也解释了普通扩散的隐式 coarse-to-fine：白噪声先淹没能量较弱的高频；IHDM 则显式按频率衰减。"),
            sec("模型与方法", "forward variational family 在每个热耗散层加入固定训练噪声 σ；reverse network 预测前一层均值，并加入采样噪声 δ。DCT 使热核计算与频率分层高效。", "U-Net 通过逐层 MSE 学习 regularized deblurring。非零 σ 不是装饰：它让反向条件非退化，并正则化病态逆热问题。", "Figure 5 展示五个数据集从平坦场逐步长出结构，并用分叉树强调同一粗态可通向多种细节。"),
            sec("核心结果与证据", "生成序列确实先确定平均颜色和大尺度形状，再出现纹理；固定噪声而改变初态颜色可得到形态相似但色调不同的人脸，说明尺度层级在 latent paths 中可操纵。", "文中 FID：CIFAR-10 18.96、LSUN Churches 128 为 45.06、AFHQ 43.39、FFHQ 64.91；作者明确承认远弱于当时 CIFAR-10 DDPM 3.17，贡献主要是新归纳偏置而非 SOTA。", "采样噪声比 δ/σ 约 1.25–1.3 时最好；δ=0 只锐化已有粗像，不产生足够新细节，而 σ=0 时即使 MNIST 也失败。"),
            sec("有效性与局限", "逆热方程的病态性被噪声正则化但未消失；结果对 σ、δ、离散层数 K 与最大模糊尺度敏感。", "FID 明显落后强 diffusion/GAN 基线，不能把可解释的 coarse-to-fine 视觉过程当成更高概率质量。", "颜色—形状“解缠”来自特定数据与 prior，尚无严格独立性判据；高分辨率成本和似然/FID 的最优超参数也不一致。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2206.13397；代码：https://github.com/AaltoML/generative-inverse-heat-dissipation。", "全文 PDF 共 55 页，SHA-256：ebfe4b0dd02dac03078244ad21cbae4114cc299e95b99bac3b2aa517269a91aa。", "复现应扫描 σ、δ/σ、K 与最大 blur width；保存逐频率功率谱、每层重构误差、同一粗态的分叉样本和固定样本数 FID。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 3 理解为何 σ>0 让 paths 合并，再从热核的 DCT 对角化重建 forward process。", "随后看 Figures 4–5，把频谱论证与实际粗到细样本对应。", "最后读 δ/σ 扫描和定量段落；论文价值在结构性假设，不在 benchmark 冠军。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2206.13397/figure-5-coarse-to-fine.webp", "label": "Figure 5", "visual_type": "comparison", "evidence": "paper.pdf p. 6, Figure 5", "alt_text": "五个数据集的逆热耗散粗到细生成序列与分叉树。", "caption": "生成从近乎平坦的低频场开始，逐步加入轮廓与纹理；同一粗态可随机分叉成不同细节。", "selection_rationale": "该图是论文最关键、最物理直观的多尺度生成可视化；它同时展示尺度顺序和随机分叉，信息量高于单独的 FID 数据表。"},
        "figure_refs": [figure("2206.13397", "figure-5-coarse-to-fine.webp", "Figure 5", 6, "show coarse-to-fine stochastic generation", "逆热耗散生成序列与层级分叉。", "低频结构先确定，高频细节在后续随机反演中出现。", "The learned reverse process follows the scale ordering imposed by the heat operator.")],
        "equation_refs": [{"label": "Heat semigroup", "latex": r"u_k=V\exp(-\Lambda t_k)V^\top u_0", "role": "erase high spatial frequencies at mode-dependent rates", "symbols": {"V": "DCT basis", "Lambda": "discrete Laplacian spectrum", "t_k": "dissipation time"}, "evidence": "paper.pdf heat-equation formulation", "interpretation": "Large Laplacian eigenvalues decay first, explicitly ordering image scales."}],
        "evidence_refs": ["paper.pdf pp. 2–5: probabilistic inverse heat process and spectral bias", "paper.pdf pp. 6–8: generation, FID, noise ratio and latent behavior", "source PDF SHA-256 ebfe4b0dd02dac03078244ad21cbae4114cc299e95b99bac3b2aa517269a91aa", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2208.09392", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2208.09392",
        "title_en": "Cold Diffusion: Inverting Arbitrary Image Transforms Without Noise", "title_zh": "冷扩散：无噪声地反演任意图像变换",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("1123e0812adab953", "Flow Matching"),
        "verified_metadata": meta("2208.09392", "v1", "Cold Diffusion: Inverting Arbitrary Image Transforms Without Noise", ["Arpit Bansal", "Eitan Borgnia", "Hong-Min Chu", "Jie S. Li", "Hamid Kazemi", "Furong Huang", "Micah Goldblum", "Jonas Geiping", "Tom Goldstein"], ["cs.CV", "cs.LG"], "cs.CV", "2022-08-19T15:18:39Z", "Diffusion-like training and sampling are generalized from Gaussian noise to deterministic image degradations."),
        "sections": [
            sec("作者信息", "作者：Arpit Bansal 等九人；arXiv:2208.09392v1。", "本卡核对 23 页全文。"),
            sec("研究问题", "扩散生成通常被解释为反演随机加噪。论文检验更强命题：若 forward operator 是确定的 blur、mask、pixelation、snow 或 animorphosis，类似的逐步 restoration 是否仍能形成生成/重构模型？", "难点是 restoration predictor 不完美时，逐步直接退化其输出会积累误差；稳定 sampler 必须保留并校正当前状态。"),
            sec("背景", r"给定逐级信息损失算子 (D(x,t))，训练 restoration (R(x_t,t)\approx x_0)。朴素更新 (x_{t-1}=D(R(x_t,t),t-1)) 会把每步误差完全写回状态。", "改进算法把预测在相邻退化层的差量加到当前状态；当 R 完美时两算法一致，当相邻步很小时误差的一阶共模部分抵消。"),
            sec("模型与方法", r"训练损失为 (mathbb E\|R(D(x_0,t),t)-x_0\|_1)。Algorithm 2 更新 (x_{t-1}=x_t-D(\hat x_0,t)+D(\hat x_0,t-1))。", "作者在 MNIST、CIFAR-10、CelebA 上测试 deblurring、inpainting、super-resolution、snow removal，并用固定噪声、blur prior 与其他 transform 做生成 proof of concept。", "Figure 1 把 Gaussian hot diffusion 与五种 cold transforms 放在同一 forward/reverse 坐标中，显示“diffusion”框架真正依赖的是退化层级，而非必须注入随机噪声。"),
            sec("核心结果与证据", "deblurring 的 sampled FID 在 MNIST/CIFAR-10/CelebA 为 4.69/80.08/26.14，优于 direct reconstruction 的 5.10/83.69/36.37；但 sampled 的 RMSE、SSIM 可能更差，说明更像总体数据分布不等于更接近原图。", "inpainting 的 sampled FID 为 1.61/8.92/5.73，同样优于 direct 2.24/9.97/7.74。Algorithm 2 的稳定性因此不仅是视觉案例，也体现在 held-out distribution metrics。", "无条件 cold blur 的 CelebA/AFHQ FID 为 49.45/54.68，明显不及 estimated-noise hot diffusion 23.11/20.59；论文建立可行性，而非证明任意退化都优于 Gaussian diffusion。"),
            sec("有效性与局限", "任意 D 并不自动给出易采样 terminal prior；unconditional blur 需要对最终通道均值拟合 GMM，并通过破坏像素对称性改善生成。", "Algorithm 2 对小步误差稳定，但 D 若不平滑、非嵌套或丢失结构突变，局部抵消论证会减弱。", "FID 与逐图像 SSIM/RMSE 衡量不同对象；重构任务和生成任务必须分开评价，不能只挑有利指标。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2208.09392；代码：https://github.com/arpitbansal297/Cold-Diffusion-Models。", "全文 PDF 共 23 页，SHA-256：ec5e6a5ccae672bc6f17649fce078bcb596d58a4547b57e2d66703ae765ce62a。", "复现应固定 D 的完整 schedule、T、R 网络、terminal prior 与 Algorithm 1/2；同时保存 FID、SSIM、RMSE 和逐步误差，避免把分布逼真度当作原图恢复。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1 建立 generalized diffusion 的对象，再逐行比较 Algorithms 1–2。", "随后读 deblurring 段的 difference-of-Gaussians 解释，并核对 Tables 1–4 的指标分歧。", "最后读 cold generation；把条件恢复成功与无条件生成质量严格分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2208.09392/figure-1-cold-transforms.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "噪声、模糊、动物形变、遮罩、像素化和雪化的 forward/reverse 图像序列。", "caption": "同一恢复框架可反演随机加噪，也可反演多种确定退化；不同退化定义不同的生成归纳偏置。", "selection_rationale": "这张总览图最直接表达论文反直觉结论；它把六种退化放在同一 forward/reverse 坐标中，比任一单独指标表更能解释方法边界。"},
        "figure_refs": [figure("2208.09392", "figure-1-cold-transforms.webp", "Figure 1", 1, "compare hot and deterministic cold degradations", "六种 forward 与 reverse 图像变换。", "噪声不是唯一可用的 destruction process；blur、mask 等也能组织逐步 restoration。", "The framework generalizes the degradation path, while sample quality remains operator-dependent.")],
        "equation_refs": [{"label": "Error-correcting cold update", "latex": r"x_{t-1}=x_t-D(\hat x_0,t)+D(\hat x_0,t-1),\qquad \hat x_0=R(x_t,t)", "role": "invert a degradation path without compounding restoration error", "symbols": {"D": "degradation operator", "R": "restoration network", "x_t": "current degraded state"}, "evidence": "paper.pdf p. 4, Algorithm 2", "interpretation": "Only the predicted change between adjacent degradation levels is applied to the current state."}],
        "evidence_refs": ["paper.pdf pp. 3–5: generalized training and stable sampling", "paper.pdf pp. 5–9: restoration metrics and cold generation", "source PDF SHA-256 ec5e6a5ccae672bc6f17649fce078bcb596d58a4547b57e2d66703ae765ce62a", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2209.05557", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2209.05557",
        "title_en": "Blurring Diffusion Models", "title_zh": "模糊扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("3e6cded2f0754313", "Generative Models"),
        "verified_metadata": meta("2209.05557", "v3", "Blurring Diffusion Models", ["Emiel Hoogeboom", "Tim Salimans"], ["cs.LG", "cs.CV", "stat.ML"], "cs.LG", "2022-09-12T19:16:48Z", "Heat dissipation is recast as frequency-dependent Gaussian diffusion and combined with growing noise."),
        "sections": [
            sec("作者信息", "作者：Emiel Hoogeboom、Tim Salimans；arXiv:2209.05557v3，ICLR 2023。", "本卡核对 15 页全文。"),
            sec("研究问题", "IHDM 明确按频率模糊，却在反演协方差和参数化上与成熟 DDPM 脱节。论文问热耗散是否其实是某种非各向同性 Gaussian diffusion，以及能否同时保留 blur 的多尺度偏置和标准 denoising diffusion 的可训练性。", "这要求证明 forward marginals 对应合法 Markov transitions，并在频率空间写出解析 reverse conditional。"),
            sec("背景", r"DCT 将热算子对角化。对频率分量 (u_t=V^\top z_t)，IHDM marginal 是 (q(u_t|u_x)=\mathcal N(d_t\odot u_x,\sigma^2I))：信噪比按频率变化，因此等价于非各向同性 Gaussian diffusion。", "高频 d_t 衰减更快，随后每步有效噪声也更强；低频保留更久，形成显式尺度偏置。"),
            sec("模型与方法", r"作者推广为 (q(u_t|u_x)=\mathcal N(\alpha_t\odot u_x,\operatorname{diag}(\sigma_t^2)))，每个 DCT 模式有自己的 signal/noise schedule。", "合法 Markov transition 与 posterior covariance 可逐频率解析计算；网络仍在像素空间做 epsilon prediction，DCT 只用于构造 forward/reverse 系数。", "Figure 1 对比标准 diffusion、近确定热耗散和 blurring diffusion：后者既模糊又逐步加噪，桥接两个极限。"),
            sec("核心结果与证据", "CIFAR-10 FID：Cold Blur 80.08、IHDM 18.96、Soft Diffusion 4.64、同架构 denoising diffusion 3.58、blurring diffusion 3.17。LSUN Churches 128 上分别为 IHDM 45.1、denoising 4.68、blurring 3.88。", r"最大 blur (sigma_{B,\max}=20) 在 CIFAR-10 最好（FID 3.17），LSUN 则 (sigma_{B,\max}=10) 最好（3.65）；sin² schedule 在强 blur 下优于更激进的 sin schedule。", "结果支持 blur 作为正则化归纳偏置，但收益相对标准 diffusion 只有 0.41–0.80 FID，远小于相对 IHDM 的修复。"),
            sec("有效性与局限", "更强 blur 收敛更慢：CIFAR-10 约 200k 步后、LSUN 约 1M 步后才超过弱 blur；训练预算不足会反转结论。", "只在 CIFAR-10 与 LSUN Churches 两个无条件图像任务验证，且超参数 optimum 不跨数据集保持。", "频率空间对角化依赖线性 blur 与正交 DCT；任意非线性 destruction 不能自动继承解析 Markov/posterior 结构。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2209.05557。", "全文 PDF 共 15 页，SHA-256：2ea8c413fd92dcc21b0c677e210469abae4fcabe996232c70e1a40edb980b909。", "复现需匹配 UNet、训练步数、样本数、DCT 归一化、blur/noise schedule 和 epsilon parameterization；绘制 FID 随训练步与 σ_B,max 的二维曲线，而不只报终点。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1 确认三个 forward process 的区别，再推导 DCT 下的 scalar Gaussian channels。", "随后核对 Markov transition 与 reverse covariance，理解 IHDM 原参数化为何不匹配真实逆过程。", "最后读 Tables 1–4 与 limitations；把理论桥接、相对 IHDM 改善和小幅超过 DDPM 分成三层结论。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2209.05557/figure-1-process-comparison.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "猫图像在标准扩散、热耗散和模糊扩散中的破坏序列。", "caption": "标准扩散各向同性加噪，热耗散优先删除高频，模糊扩散把频率选择性衰减与增长噪声结合。", "selection_rationale": "该图比 FID 表更清楚地展示模型在两个已知极限之间的位置。"},
        "figure_refs": [figure("2209.05557", "figure-1-process-comparison.webp", "Figure 1", 1, "compare three forward processes", "三种 diffusion/destruction process 的猫图像序列。", "blurring diffusion 同时表现出尺度选择性模糊与随机噪声增长。", "The model interpolates structurally between isotropic denoising diffusion and inverse heat dissipation.")],
        "equation_refs": [{"label": "Frequency-dependent diffusion", "latex": r"q(u_t\mid u_x)=\mathcal N\!\left(u_t\mid \alpha_t\odot u_x,\operatorname{diag}(\sigma_t^2)\right)", "role": "define independent diffusion schedules for spatial frequencies", "symbols": {"u_x": "DCT image coefficients", "alpha_t": "mode-wise signal schedule", "sigma_t": "mode-wise noise schedule"}, "evidence": "paper.pdf p. 5, Eq. (19)", "interpretation": "Heat dissipation becomes Gaussian diffusion with frequency-dependent signal-to-noise ratios."}],
        "evidence_refs": ["paper.pdf pp. 2–5: Gaussian reinterpretation of heat dissipation", "paper.pdf pp. 5–9: blurring model, FID and schedule ablations", "source PDF SHA-256 2ea8c413fd92dcc21b0c677e210469abae4fcabe996232c70e1a40edb980b909", "Evidence status: full-text verified; no independent reproduction performed."],
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
