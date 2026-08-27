#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 010."""

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
        "arxiv_id": "2310.17391", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2310.17391",
        "title_en": "Theory of Hyperuniformity at the Absorbing State Transition", "title_zh": "吸收态相变处超均匀性的理论",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("34ccd3ff52287b90", "Statistical Physics"),
        "verified_metadata": meta("2310.17391", "v1", "Theory of Hyperuniformity at the Absorbing State Transition", ["Xiao Ma", "Johannes Pausch", "Michael E. Cates"], ["cond-mat.stat-mech"], "cond-mat.stat-mech", "2023-10-26T13:39:48Z", "Doi-Peliti field theory and one-loop RG explain C-DP hyperuniformity through cancellation of active and passive density fluctuations."),
        "sections": [
            sec("作者信息", r"作者：Xiao Ma、Johannes Pausch、Michael E. Cates；arXiv:2310.17391v1。全文 20 页，研究对象是 conserved directed percolation（C-DP）吸收态临界点。"),
            sec("研究问题", r"多吸收态系统在临界点不是出现普通临界密度发散，而是低波数涨落被压低：\(S(q)\sim q^{\varsigma}\)。C-DP 的 \(\beta,\nu_\perp,z\) 可由 quenched Edwards–Wilkinson 映射与 FRG 得到，但超均匀指数 \(\varsigma\) 在该映射中不可见。论文问：能否直接从反应—扩散场论算出它，并说明一个稀少的 active population 怎样抵消大量 passive particles 的涨落？"),
            sec("背景", r"模型包含扩散的 active 粒子 \(A\) 与静止的 passive 粒子 \(P\)：\(A+P\to2A\) 以速率 \(\kappa\) 激活粒子，\(A\to P\) 以速率 \(\mu\) 衰减。总密度守恒，而 active density 是在临界点消失的非守恒序参量。", r"高斯层面，\(S_{AA}\) 与 \(S_{PP}\) 各自有限，交叉关联却几乎精确抵消它们，使总密度结构因子在 \(q\to0\) 时消失。低于上临界维 \(d_c=4\)，单独组分的涨落甚至发散，超均匀性仍来自更强的非高斯反关联。"),
            sec("模型与方法", r"作者从 master equation 构造 Doi–Peliti action，先在均匀 active/passive 背景上计算树级静态 correlators，再以 \(\epsilon=4-d\) 做 one-loop perturbative RG。三个独立耦合固定点为 \(u^*=v^*=-2\epsilon/9\)、\(w^*=2\epsilon/3\)。", r"场的 anomalous dimensions 原本存在分配歧义；要求总密度涨落必须超均匀而非发散，唯一选出 \(\eta_{\check a}=\eta_{\check p}=\eta_{\tilde p}=-\epsilon/18\)、\(\eta_{\tilde a}=5\epsilon/18\)。随后从未被抵消的 leading term 读出 \(\varsigma\)。"),
            sec("核心结果与证据", r"Figure 1 直接画出 cancellation mechanism：蓝色 passive 与红色 active structure factors 在 \(q\to0\) 各自不消失，但黑色总密度曲线趋于零；右图的 active/passive 空间涨落幅度很大，黑色总密度却显著平滑。", r"高于四维的高斯理论给出 singular hyperuniformity \(\varsigma=0^+\)；在 \(d=4-\epsilon\) 中，one-loop 结果为 \(\varsigma=2\epsilon/9+O(\epsilon^2)\)。同一 RG 还恢复 \(\beta=1-\epsilon/9\)、\(\nu_\perp=1/2+\epsilon/12\)、\(z=2-2\epsilon/9\)。", r"该结果否定 Hexner–Levine 猜想 \(\varsigma=d-2\beta/\nu_\perp=\epsilon/9+O(\epsilon^2)\)。代入 \(d=(3,2,1)\) 时本文一阶预测为 \((0.22,0.44,0.66)\)，与已报道数值 \((0.24,0.45,0.43)\) 在三维和二维接近，但一维偏差明显。"),
            sec("有效性与局限", r"结果在 \(d=4-\epsilon\) 的一阶展开中受控；把它直接外推到一维并不定量可靠。Figure 1 的 Gaussian density fields 可取负值，仅用于揭示 cancellation，不是低维 microscopic configuration。", r"RG 只固定幂律而不固定各 correlator 的 amplitude ratios，因此临界抵消由 scaling consistency 与已知超均匀物理条件选定，而非逐项显式计算。保守扩散噪声不能随意丢弃；忽略它会错误地预测整个 active phase 都有 \(\varsigma=2\)。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2310.17391。全文 20 页，PDF SHA-256：d69c21ab708ee198fe4b70e448d97bba119f0aba28c69915c8a60b499ed70761。", r"复现解析部分需固定 Doi–Peliti shift、propagator/vertex conventions、transmutation vertices 的可约图分类、dimensional regularization 与 \(\epsilon=4-d\) 记号；数值比较需报告 \(q\) 区间、有限尺寸与临界点误差。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把“两个大涨落之和很小”作为全文物理图像；再读 Eqs. (1)–(5) 的 Gaussian correlators。随后看 Eq. (6) 的六项结构与 anomalous-dimension 选择，最后读 Eq. (7) 及 Discussion，区分受控 \(\epsilon\)-expansion 与低维外推。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2310.17391/figure-1-structure-factors.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "active、passive 与总密度结构因子以及对应的一维密度涨落。", "caption": r"active 与 passive 涨落各自很强，却通过负交叉关联使总密度的 \(q\to0\) 模式被压低。", "selection_rationale": "论文没有独立示意图；该图把超均匀性的核心 cancellation mechanism 同时画在波数与实空间中。"},
        "figure_refs": [figure("2310.17391", "figure-1-structure-factors.webp", "Figure 1", 2, "show hyperuniformity by cancellation of component fluctuations", "三条结构因子曲线与 active/passive/total density profiles。", "单组分并不超均匀，总密度的低波数抑制来自 active-passive 反关联。", "The plot is a Gaussian-level mechanism illustration rather than a low-dimensional positive-density simulation.")],
        "equation_refs": [
            {"label": "Gaussian total structure factor", "latex": r"S(q)=a_0+p_0\frac{q^2\xi^2}{1+q^2\xi^2}", "role": "expose the low-wave-number cancellation mechanism", "symbols": {"a_0": "mean active density", "p_0": "mean passive density", "xi": "Gaussian correlation length"}, "evidence": "paper.pdf p. 2, Eqs. (2)–(3)", "interpretation": "Taking q to zero before the critical limit suppresses the conserved total-density fluctuation."},
            {"label": "C-DP hyperuniformity exponent", "latex": r"\varsigma=\frac{2\epsilon}{9}+O(\epsilon^2),\qquad \epsilon=4-d", "role": "state the one-loop critical prediction below the upper critical dimension", "symbols": {"varsigma": "hyperuniformity exponent", "epsilon": "distance below d=4"}, "evidence": "paper.pdf pp. 1 and 4", "interpretation": "The result differs by a factor of two from the Hexner-Levine scaling conjecture at first order."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2: Gaussian cancellation and conservative noise", "paper.pdf pp. 3–5: one-loop fixed point, anomalous dimensions and exponent comparison", "source PDF SHA-256 d69c21ab708ee198fe4b70e448d97bba119f0aba28c69915c8a60b499ed70761", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2311.15127", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2311.15127",
        "title_en": "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets", "title_zh": "Stable Video Diffusion：将潜视频扩散模型扩展到大型数据集",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("914b139b3661cddc", "Video Generation"),
        "verified_metadata": meta("2311.15127", "v1", "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets", ["Andreas Blattmann", "Tim Dockhorn", "Sumith Kulal", "Daniel Mendelevitch", "Maciej Kilian", "Dominik Lorenz", "Yam Levi", "Zion English", "Vikram Voleti", "Adam Letts", "Varun Jampani", "Robin Rombach"], ["cs.CV"], "cs.CV", "2023-11-25T22:28:38Z", "A three-stage latent video diffusion pipeline studies large-scale video curation and transfers the learned motion prior to image-to-video and multi-view generation."),
        "sections": [
            sec("作者信息", r"作者：Andreas Blattmann 等十二人（Stability AI）；arXiv:2311.15127v1。全文 31 页，公开代码与模型位于 Stability AI generative-models 仓库。"),
            sec("研究问题", r"把 2D latent diffusion 加入 temporal layers 可以生成视频，但训练协议与数据清洗差异很大。论文问：image pretraining、large-scale video pretraining 和 high-quality finetuning 三阶段各自贡献什么；哪些 motion、caption、cut 与 aesthetics filters 真正改善模型；学到的 motion prior 能否迁移到 image-to-video、camera control 与 multi-view synthesis？"),
            sec("背景", r"SVD 沿用 Stable Diffusion 2.1 的空间 U-Net，在每个 spatial convolution/attention 后加入 temporal convolution/attention，并 finetune 全模型。训练在 latent space 中进行，以降低多帧高分辨率生成的成本。", r"原始 web video 含大量镜头切换、渐变、静止片段、文字覆盖与弱 caption。对于生成模型，这些不是无害噪声：它们会直接成为模型学习的运动统计。论文因此把 dataset construction 当作动力学建模的一部分。"),
            sec("模型与方法", r"训练分三阶段：Stage I 从 SD2.1 初始化 image representation；Stage II 在处理后的 LVD-F 上预训练 14 帧、\(256\times384\) base model；Stage III 在约 1M 个高质量样本上以 \(576\times1024\) finetune 50k steps。", r"LVD 从约 577M clips 出发，经三级 cut detector、2 fps optical flow、OCR、CLIP/aesthetic scores 与 CoCa/VideoBLIP/LLM captions 构成过滤信号；human-preference ablation 选择阈值，得到 152M clips 的 LVD-F。高分辨率训练采用 EDM preconditioning 并把 noise schedule 向更高噪声移动。"),
            sec("核心结果与证据", r"Figure 1 用连续帧展示三种能力：text-to-video 的动作一致性、image-to-video 的时序延展，以及把 video prior finetune 成多视角环绕。它比单帧指标更直接地显示模型到底学习了什么运动结构。", r"同规模实验中，image-pretrained spatial weights 在 quality 与 prompt alignment 上均优于随机初始化；LVD-10M 过滤成约四分之一大小的 LVD-10M-F 后，human preference 反而提升。完整 LVD 为 577M clips/212.09 years，LVD-F 为 152M/50.64 years。", r"UCF-101 zero-shot FVD 为 242.02，优于表中公开 baselines。SVD-MV 在 GSO 上得到 LPIPS 0.14、PSNR 16.83、CLIP-S 0.89；image-prior SD2.1-MV 为 0.18/15.06/0.83。该 multi-view finetuning 只训练 12k steps（约 16 小时、8×80GB A100）。"),
            sec("有效性与局限", r"作者明确指出模型擅长短视频而非 long-form generation：一次生成多 keyframes 仍昂贵，输出有时运动不足；diffusion sampling 慢且 VRAM 需求高。真实部署还需独立评估偏差、滥用、合成内容标识与数据来源。", r"核心质量证据大量依赖 human preference、FVD/LPIPS/CLIP-S 与特定数据流程；私有原始 LVD 和过滤标注使完全复现困难。Figure 1 是精选样例，不代表 failure-rate distribution；与 closed-source Gen-2/Pika 的比较也无法控制训练数据与推理预算。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2311.15127；代码与权重：https://github.com/Stability-AI/generative-models。全文 31 页，PDF SHA-256：654ef597e183c0544cd753494cb442125bc42b17dd2477481b6799114482a92e。", r"复现需固定 cut-detector cascade、optical-flow/OCR/aesthetic thresholds、caption source、frame rate、resolution、noise distribution、temporal-layer initialization、CFG across frames、training clips 与 human-evaluation protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 确认三类 downstream motion prior；再读 Section 3 与 Figure 2–4，把数据量、过滤和 initialization 的贡献拆开。随后读 Section 4 的 I2V/MV experiments，最后读 Appendix A 的 limitations；不要用精选视频帧替代总体失败率。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2311.15127/figure-1-video-samples.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "机器人 DJ、爆炸奶酪屋、紫袍兔子与多视角玩具的连续生成帧。", "caption": "同一 latent video prior 支撑 text-to-video、image-to-video 与 multi-view synthesis；连续帧可直接检查运动和视角一致性。", "selection_rationale": "这是论文最重要的可视化原图，优先于数据表，能同时概括三种模型用途。"},
        "figure_refs": [figure("2311.15127", "figure-1-video-samples.webp", "Figure 1", 1, "show temporal consistency and transfer of the learned motion prior", "四组连续视频帧，覆盖文本生成、图像条件生成和多视角生成。", "连续帧使运动一致性与跨任务迁移可见，但仍是作者精选样例。", "Qualitative samples must be read together with aggregate human and benchmark evaluations.")],
        "equation_refs": [
            {"label": "Probability-flow dynamics", "latex": r"d x=-\dot\sigma(t)\sigma(t)\nabla_x\log p(x;\sigma(t))\,dt", "role": "describe iterative latent denoising across noise scales", "symbols": {"sigma(t)": "noise schedule", "nabla log p": "score field"}, "evidence": "paper.pdf p. 18, Eq. (1)", "interpretation": "High-resolution finetuning changes the noise schedule because the relevant signal-to-noise regime shifts with resolution."},
            {"label": "Denoising score-matching loss", "latex": r"\mathbb E\!\left[\lambda_\sigma\left\|D_\theta(x_0+n;\sigma,c)-x_0\right\|_2^2\right],\qquad n\sim\mathcal N(0,\sigma^2I)", "role": "train the conditional latent denoiser", "symbols": {"D_theta": "conditional denoiser", "c": "text, image or other condition", "lambda_sigma": "noise-dependent weight"}, "evidence": "paper.pdf p. 18, Eq. (2)", "interpretation": "The same denoising backbone can be adapted by changing conditioning and temporal layers."},
        ],
        "evidence_refs": ["paper.pdf pp. 1 and 3–6: architecture, three-stage training and curation ablations", "paper.pdf pp. 7–8: image-to-video and multi-view transfer", "paper.pdf p. 15: broader impact and limitations", "source PDF SHA-256 654ef597e183c0544cd753494cb442125bc42b17dd2477481b6799114482a92e", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2312.11181", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2312.11181",
        "title_en": "Anomalous relaxation and hyperuniform fluctuations in center-of-mass conserving systems with broken time-reversal symmetry", "title_zh": "质心守恒且破坏时间反演系统中的异常弛豫与超均匀涨落",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("87f3f264dbd7ac9d", "Statistical Physics"),
        "verified_metadata": meta("2312.11181", "v2", "Anomalous relaxation and hyperuniform fluctuations in center-of-mass conserving systems with broken time-reversal symmetry", ["Anirban Mukherjee", "Dhiraj Tapader", "Animesh Hazra", "Punyabrata Pradhan"], ["cond-mat.stat-mech"], "cond-mat.stat-mech", "2023-12-18T13:24:04Z", "Microscopic theory and simulations of the one-dimensional Oslo model connect center-of-mass conservation to anomalous relaxation, vanishing mobility and hyperuniform current fluctuations."),
        "sections": [
            sec("作者信息", r"作者：Anirban Mukherjee、Dhiraj Tapader、Animesh Hazra、Punyabrata Pradhan；arXiv:2312.11181v2。全文 28 页，研究一维环上的 fixed-energy Oslo model。"),
            sec("研究问题", r"dipole/center-of-mass 守恒常被认为导致 subdiffusive hydrodynamics，但这个判断通常还隐含 time-reversal symmetry。论文问：若同时守恒质量与质心、却破坏 detailed balance，密度弛豫、current fluctuations、mobility 与 hyperuniformity 会怎样；这些动态指数能否由吸收相变的静态指数锁定？"),
            sec("背景", r"Oslo model 是带随机阈值、确定性 toppling 的 sandpile。总质量与 center of mass 守恒，临界密度约 \(\rho_c\simeq1.732\)；在 \(\rho>\rho_c\) 的 active phase，activity \(a(\rho)\) 是序参量。", r"与只有质量守恒的 Manna sandpile 不同，CoM 守恒使跨 bond 的长时间净输运受到严格约束。作者同时研究 density relaxation、integrated current、subsystem mass、power spectrum 与 tagged-particle diffusion，以分清 bulk diffusion、self diffusion 和 mobility。"),
            sec("模型与方法", r"远离临界点，microscopic closure 给出 nonlinear diffusion equation \(\partial_t\rho=\partial_x[D(\rho)\partial_x\rho]\)，其中 \(D(\rho)=a'(\rho)\)。近临界时 \(D\sim\Delta^{-(1-\beta)}\)，故弛豫时间 \(\tau_r\sim L^z\)，\(z=2-(1-\beta)/\nu_\perp<2\)。", r"对累计 bond current \(Q_i(T)\) 与长度 \(l\) 子系统质量 \(M_l\)，质量守恒给出 asymptotic equality \(\Sigma_Q^2=\Sigma_M^2\)。作者用 unequal-time correlations 与 Monte Carlo 检验 current growth、power spectra、structure factor 与 tagged-particle MSD。"),
            sec("核心结果与证据", r"Figure 1 展示远离临界的 step-profile relaxation：不同时间的原始 fronts 按 \(x/t^{1/2}\) 缩放后坍缩到同一曲线，且 nonlinear hydrodynamic solution 与模拟吻合；常数扩散系数的虚线则有可见偏差。", r"远离临界时 integrated current fluctuation 从下方饱和：\(\langle Q_i^2(T)\rangle\simeq\Sigma_Q^2-\mathrm{const}\,T^{-1/2}\)。近临界时先以 \(T^\alpha\) 次扩散增长再饱和，\(\delta=2(1-1/\nu_\perp)/\nu_\perp\)、\(\alpha=\delta/(z\nu_\perp)\)。取 \(\nu_\perp\simeq4/3,z\simeq10/7\) 得 \(\delta\simeq3/8\)、\(\alpha\simeq0.197\)。", r"particle mobility 对所有 \(\rho>\rho_c\) 精确为零，尽管 bulk density 仍可扩散。tagged-particle self-diffusion 则满足 \(D_s(\rho)=a(\rho)/\rho\)，在临界点随 activity 一起消失。远离临界的 \(S(q)\sim q^2\) 是 class-I hyperuniformity，近临界转为更弱的 class-III。"),
            sec("有效性与局限", r"结论来自一维 Oslo model、\(\rho>\rho_c\) 与特定 closure；作者论证结构应适用于更广的 mass+CoM conserving class，但并未逐模型验证。time-reversal breaking 的具体 microscopic rule 可能改变 hydrodynamics，不能把本结果直接套到所有 fracton fluids。", r"Figure 1 验证的是远离临界的 density relaxation；近临界 exponent relations 依赖已有 \(\beta,\nu_\perp,z\) 数值与有限尺寸 scaling。mobility 的零值还依赖极限顺序：先 \(T\to\infty\)，再 \(L\to\infty\)。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2312.11181。全文 28 页，PDF SHA-256：3167ffd3c3faaf432457a75ec8d47511064047852635e7a8686b12243021f8a0。", r"复现需固定 ring size、random thresholds、parallel/sequential toppling convention、\(\rho_c\)、step/wedge initial profile、Monte Carlo time units、current sign、极限顺序与拟合窗口；current、mass、structure-factor 和 MSD observables 应同一轨迹同步保存。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 理解“CoM 守恒并不必然 subdiffusive”；再读 Introduction 的五点 summary 与 Eq. (1) 的 mass-current relation。随后按 Figure 6–9 跟踪 \(\Sigma_Q^2\) 与 \(T^\alpha\)，最后看 Table I，把 Oslo 与单守恒 Manna 的 mobility、power spectra 和 diffusion coefficients 分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2312.11181/figure-1-density-relaxation.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 6, Figure 1", "alt_text": "step-like density front 在多个时刻的演化，以及按 x/t 的平方根重标度后的曲线坍缩。", "caption": r"原始 density front 随时间展宽；按 \(x/t^{1/2}\) 缩放后坍缩，证明远离临界仍是 diffusion，而非由 CoM 守恒强制的 subdiffusion。", "selection_rationale": "论文没有更合适的机制示意图；该图最直接展示其反直觉主结论与 theory-simulation agreement。"},
        "figure_refs": [figure("2312.11181", "figure-1-density-relaxation.webp", "Figure 1", 6, "demonstrate diffusive density relaxation despite center-of-mass conservation", "多个时刻的 step density profiles 与 x over square-root-t scaling collapse。", "nonlinear diffusion theory matches simulation more closely than a constant-D approximation。", "The collapse applies away from criticality; the near-critical regime has a different superdiffusive exponent.")],
        "equation_refs": [
            {"label": "Current-mass conservation relation", "latex": r"\Sigma_Q^2(\rho)=\Sigma_M^2(\rho)", "role": "connect asymptotic dynamic current fluctuations to static subsystem-mass fluctuations", "symbols": {"Sigma_Q": "long-time bond-current fluctuation", "Sigma_M": "large-subsystem mass fluctuation"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "Center-of-mass conservation makes transport fluctuations boundary-controlled and forces the mobility to vanish."},
            {"label": "Critical current exponents", "latex": r"\delta=\frac{2(1-1/\nu_\perp)}{\nu_\perp},\qquad \alpha=\frac{\delta}{z\nu_\perp}", "role": "determine current-fluctuation divergence and temporal growth from critical exponents", "symbols": {"delta": "divergence exponent of Sigma_Q squared", "alpha": "pre-saturation current-growth exponent", "z": "dynamic exponent"}, "evidence": "paper.pdf pp. 1–3 and p. 17", "interpretation": "The dynamic current law is not an independent exponent once mass conservation and hyperuniform scaling are imposed."},
            {"label": "Tagged-particle self diffusion", "latex": r"D_s(\bar\rho)=\frac{a(\bar\rho)}{\bar\rho}", "role": "relate single-particle diffusion to the steady-state activity", "symbols": {"D_s": "self-diffusion coefficient", "a": "active-site fraction", "rho_bar": "global density"}, "evidence": "paper.pdf p. 22, Eq. (122)", "interpretation": "Self diffusion vanishes at the absorbing transition even while the bulk diffusion coefficient diverges."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: model, conservation principle and exponent summary", "paper.pdf pp. 6–9: diffusive and superdiffusive density relaxation", "paper.pdf pp. 15–23: current fluctuations, hyperuniformity and tagged diffusion", "source PDF SHA-256 3167ffd3c3faaf432457a75ec8d47511064047852635e7a8686b12243021f8a0", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2312.16038", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2312.16038",
        "title_en": "Physics-informed neural networks for solving functional renormalization group on a lattice", "title_zh": "用物理信息神经网络求解格点泛函重整化群",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("5d54e653c95484ec", "Renormalization Group"),
        "verified_metadata": meta("2312.16038", "v3", "Physics-informed neural networks for solving functional renormalization group on a lattice", ["Takeru Yokota"], ["cond-mat.dis-nn", "cond-mat.stat-mech", "cond-mat.str-el", "hep-lat", "hep-th"], "cond-mat.dis-nn", "2023-12-26T12:55:36Z", "A PINN represents the interaction-induced effective action and solves the high-dimensional lattice Wetterich equation up to a 101-dimensional zero-dimensional O(N) benchmark."),
        "sections": [
            sec("作者信息", r"作者：Takeru Yokota（RIKEN iTHEMS）；arXiv:2312.16038v3。全文 12 页，提出 PINN-LFRG，并在 zero-dimensional \(O(N)\) model 上验证到 \(N=100\)。"),
            sec("研究问题", r"有限格点上的 Wetterich equation 是 \((N_{\mathrm{DOF}}+1)\)-维 PDE；给每个 field component 建网格会产生指数级维数灾难，vertex/derivative expansions 又只在特定场配置附近有效。论文问：能否用 differentiable neural network 直接表示一整片 field configuration space 上的 effective action，并以 FRG 方程残差训练？"),
            sec("背景", r"effective average action \(\Gamma_k(\phi)\) 在 UV 端接近 bare action，在 IR 端给出完整 effective action。Wetterich 方程含 \((\Gamma_k^{(2)}+R_k)^{-1}\) 的 trace，因此既要求对场做二阶导数，也要求高维 matrix inverse。", r"PINN 不离散输入空间，而用自动微分计算 PDE residual。潜在收益不是“用黑箱拟合几个 observables”，而是一次获得 \(\gamma(l,\phi)\) 与 self-energy 在多种、包括非均匀 field configurations 上的函数。"),
            sec("模型与方法", r"作者分解 \(\Gamma_k(\phi)=S(\phi)+\Gamma_{RG}(l,\phi)\)，再让共享参数的两个网络实现 \(\gamma(l,\phi)\simeq NN_\theta(l,\phi)-NN_\theta(0,\phi)\)，从结构上满足 \(l=0\) boundary condition。网络有 3 hidden layers、每层 256 units、Softplus activation。", r"loss 是在 collocation points 上的 Wetterich residual；为改善非微扰区收敛，先用 one-point/vertex-like approximation pretrain，再训练完整 PDE。实验遍历 \(N=1,10,100\) 与 \(\tilde g=0.1,1,10\)，并与 exact path integral、leading perturbation、large-\(N\) expansion 比较。"),
            sec("核心结果与证据", r"Figure 1 清楚显示 \(l\)、\(N\)-component field 与 \(l=0\) reference 同时进入共享网络，输出相减后自动满足初值；这比只看 loss curve 更能解释 PINN-LFRG 的 boundary-condition engineering。", r"所有 \(N,\tilde g\) 组合中，\(\gamma(l_{end},0)\) 相对误差在 3% 内，\(\sigma(l_{end},0)\) 在 1% 内；在小 \(N\)、强耦合 \(\tilde g=10\) 时，PINN 仍可超过失效的 perturbative 与 large-\(N\) approximations。", r"对 \(N=100\)，不同 field directions 的输出几乎重合，训练过程自行恢复 \(O(N)\) symmetry。A100 40GB 上 pretraining 为 4–6 分钟，完整 Wetterich training 从 \(N=1\) 的 6 小时增至 \(N=100\) 的 11 小时；训练使用 \(10^5\) 与 \(10^6\) iterations。"),
            sec("有效性与局限", r"最强数值证据来自 zero-dimensional \(O(N)\) toy model，它有 exact benchmark，却没有真实格点的空间结构；论文尚未展示 inhomogeneous phase、critical lattice scaling 或大体积 many-body observable。", r"trace/matrix inverse 仍为 \(O(N_{\mathrm{DOF}}^3)\) 的实现瓶颈；作者只讨论可用 Hutchinson estimator 降到约二次，未实测端到端误差与方差。fermionic Grassmann variables 没有直接 NN 表示；pretraining ansatz 也引入 problem-specific prior。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2312.16038；代码：https://github.com/TakeruYokota/PINN-LFRG。全文 12 页，PDF SHA-256：d194ec1e4048a53953e6701af3dd124513c765f07f0c1f20a18e0d77579954d1。", r"复现需固定 regulator、\(m^2,\tilde g,N\)、field/RG-time sampling distributions、collocation count、pretraining target、network depth/width、matrix inverse precision、optimizer schedule 与 exact quadrature。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，理解为什么相减结构自动施加 \(l=0\) boundary condition；再读 Eqs. (5)、(8)–(12) 对齐 Wetterich residual 与 pretraining。随后看 Figure 2–4 的 exact comparisons，最后读 Appendix A 的 complexity，避免把 101-dimensional toy PDE 等同于已解决真实格点 FRG。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2312.16038/figure-1-pinn-lfrg-architecture.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "RG scale、N 分量场与 l=0 参考场进入共享神经网络并相减输出有效作用量。", "caption": r"共享网络分别评估 \((l,\phi)\) 与 \((0,\phi)\)；相减结构把 FRG 初值条件直接编码进 \(\gamma(l,\phi)\)。", "selection_rationale": "这是论文最重要的机制示意图，优先于误差数据图，能直观解释 PINN-LFRG 的输入与边界条件。"},
        "figure_refs": [figure("2312.16038", "figure-1-pinn-lfrg-architecture.webp", "Figure 1", 3, "show the boundary-condition-preserving neural representation of the effective action", "RG scale 与 field vector 两次进入共享参数网络并作差。", "网络结构而非 penalty weight 强制相互作用有效作用量在 l=0 为零。", "The architecture removes one boundary-loss tuning problem but does not remove the matrix-inverse cost.")],
        "equation_refs": [
            {"label": "Lattice Wetterich equation", "latex": r"\partial_k\Gamma_k(\phi)=\frac12\operatorname{tr}\!\left[\partial_kR_k\left(\frac{\partial^2\Gamma_k}{\partial\phi\,\partial\phi}+R_k\right)^{-1}\right]", "role": "define the high-dimensional FRG PDE solved by the PINN", "symbols": {"Gamma_k": "effective average action", "R_k": "infrared regulator", "phi": "lattice field vector"}, "evidence": "paper.pdf p. 2, Eq. (5)", "interpretation": "Automatic differentiation supplies field derivatives, while the Hessian inverse remains the main computational bottleneck."},
            {"label": "Boundary-conditioned neural ansatz", "latex": r"\gamma(l,\phi;\theta)=NN_\theta(l,\phi)-NN_\theta(0,\phi)", "role": "enforce the interaction-induced initial condition exactly", "symbols": {"gamma": "RG-induced interaction part", "l": "logarithmic RG scale", "theta": "shared network parameters"}, "evidence": "paper.pdf p. 3, Eq. (9)", "interpretation": "The ansatz gives gamma(0,phi)=0 without a separate boundary-condition penalty."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: lattice FRG and PINN ansatz", "paper.pdf pp. 4–5: O(N) benchmarks, errors and symmetry recovery", "paper.pdf pp. 6–9: complexity, runtime and training details", "source PDF SHA-256 d194ec1e4048a53953e6701af3dd124513c765f07f0c1f20a18e0d77579954d1", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2401.08740", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2401.08740",
        "title_en": "SiT: Exploring Flow and Diffusion-based Generative Models with Scalable Interpolant Transformers", "title_zh": "SiT：用可扩展插值 Transformer 探索流与扩散生成模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("d3593ea6cb44205b", "Transformer Theory"),
        "verified_metadata": meta("2401.08740", "v2", "SiT: Exploring Flow and Diffusion-based Generative Models with Scalable Interpolant Transformers", ["Nanye Ma", "Mark Goldstein", "Michael S. Albergo", "Nicholas M. Boffi", "Eric Vanden-Eijnden", "Saining Xie"], ["cs.CV", "cs.LG"], "cs.CV", "2024-01-16T18:55:25Z", "Scalable Interpolant Transformers separate path, prediction target and sampler design while holding the DiT backbone fixed, improving class-conditional ImageNet FID."),
        "sections": [
            sec("作者信息", r"作者：Nanye Ma、Mark Goldstein、Michael S. Albergo、Nicholas M. Boffi、Eric Vanden-Eijnden、Saining Xie；arXiv:2401.08740v2。全文 36 页。"),
            sec("研究问题", r"DiT 的表现混合了 architecture、forward noise path、prediction target、time discretization 与 sampler。论文问：在参数量、GFLOPs 和 transformer backbone 完全不变时，哪些 dynamical-transport design choices 真正带来增益；flow ODE 与 reverse SDE 能否在同一 stochastic-interpolant 框架下模块化比较？"),
            sec("背景", r"取数据 \(x_*\sim p\) 与 Gaussian noise \(\epsilon\)，用 \(x_t=\alpha_tx_*+\sigma_t\epsilon\) 连接两端。给定同一 marginal path，既可用 probability-flow ODE 的 velocity \(v\) 生成，也可在任意 \(w_t\ge0\) 下用含 score \(s=\nabla\log p_t\) 的 reverse SDE 生成。", r"标准 score diffusion 通常把 \(\alpha_t,\sigma_t,w_t\) 绑定到 forward SDE。stochastic interpolant 则把 path、learned field 与 inference diffusion coefficient 分开；后者甚至可在训练后调节。"),
            sec("模型与方法", r"SiT 严格复用 DiT-{S,B,L,XL} latent transformer、VAE、patch size 2 与 AdaLN-Zero，只依次改变：discrete→continuous time、score/noise→velocity target、VP→Linear/GVP interpolant、ODE→SDE sampler 与 \(w_t\) choice。transition ablation 使用 ImageNet \(256^2\)、SiT-B、400k steps、250 NFE。", r"Linear path 取 \(\alpha_t=1-t,\sigma_t=t\)，GVP 取 \(\cos(\pi t/2),\sin(\pi t/2)\)。训练通常拟合 velocity；score 可由 velocity 解析恢复。SDE diffusion coefficient 比较 \(\sigma_t\)、\(\sin^2\pi t\)、KL-optimal \(w_t^{KL}\) 与 cost-regularized \(w_t^{KL,\eta}\)。"),
            sec("核心结果与证据", r"Figure 1 是论文最重要的视觉证据：\(512^2\) 与 \(256^2\) SiT-XL 的 class-conditional samples 显示跨类别细节与多尺度一致性；它应与后面的 FID curves 一起读，而不能单独当作总体质量证明。", r"逐项 ablation 中，continuous-time 只把 FID 44.2 改到 43.6；velocity/weighted score 约 39，Linear/GVP path 进一步到 34.8/34.6。相同 trained model 下 SDE 又优于 ODE：GVP 为 32.9 vs 34.6，Linear 为 33.6 vs 34.8。最优 \(w_t\) 依赖 path 与 parameterization，并非单一 schedule。", r"最终 SiT-XL 在 ImageNet \(256^2\) 取得 FID-50K 2.06（DiT-XL 2.27），在 \(512^2\) 取得 2.62（DiT-XL 3.04），架构、参数量和训练超参数保持一致。SDE 在大 NFE 时可达更低 FID，但 ODE 在低 NFE 区更快收敛。"),
            sec("有效性与局限", r"实验集中于 class-conditional ImageNet 与 DiT latent backbone；结论尚未覆盖 text-to-image、视频、likelihood、mode coverage 或真实 human preference。FID 的小幅差异不能自动解释为所有感知维度都更好。", r"sampler 优劣与 NFE budget 强相关；论文固定 Heun ODE 与 Euler–Maruyama SDE，不能把差异完全归因于 stochasticity。最佳 diffusion coefficient 是 model/path dependent，\(w_t^{KL}\) 在 Linear/GVP 端点会发散，需要 cost regularization。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2401.08740；代码：https://github.com/willisma/SiT。全文 36 页，PDF SHA-256：9207ad5e0793761417ea4bb02bee888a5ac565bd7877c4652ed8dc93784a5c46。", r"复现需固定 DiT checkpoint convention、VAE、ImageNet preprocessing、\(\alpha_t,\sigma_t\)、prediction loss weighting、ODE/SDE integrator、NFE、\(w_t\)、CFG、训练 steps、FID evaluator 与 50k sample seed。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1/2 建立 sample 与 scaling impression；再读 Eqs. (1)–(9)，确认同一路径为何既有 ODE 又有 SDE。随后按 Tables 2–6 逐步追踪每个 design choice，最后读 Table 7；不要把 2.06 归因于 transformer 结构变化，因为架构被刻意固定。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2401.08740/figure-1-sit-samples.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "狮子、面包圈、金毛犬及多个 ImageNet 类别的 SiT 生成样例网格。", "caption": "SiT-XL 在固定 DiT backbone 下通过改变 interpolant、prediction target 与 sampler 获得这些 class-conditional samples。", "selection_rationale": "该图是文章最重要的可视化原图，比 FID 表更适合作为封面，同时仍在正文中明确样例选择偏差。"},
        "figure_refs": [figure("2401.08740", "figure-1-sit-samples.webp", "Figure 1", 3, "show representative outputs of the final scalable interpolant transformer", "多个 ImageNet 类别的 512 与 256 分辨率生成样例。", "样例展示最终生成能力，但设计归因必须依赖 controlled ablations。", "Qualitative samples do not replace FID curves, recall or independent perceptual evaluation.")],
        "equation_refs": [
            {"label": "Stochastic interpolant path", "latex": r"x_t=\alpha_t x_*+\sigma_t\epsilon", "role": "separate the probability path from model architecture and sampler", "symbols": {"x_*": "data sample", "epsilon": "standard Gaussian noise", "alpha_t,sigma_t": "interpolant schedules"}, "evidence": "paper.pdf p. 4, Eq. (1)", "interpretation": "Changing the path alters transport geometry without changing the transformer backbone."},
            {"label": "Reverse stochastic sampler", "latex": r"dX_t=\left[v(X_t,t)-\frac12w_t s(X_t,t)\right]dt+\sqrt{w_t}\,d\bar W_t", "role": "sample the same marginal path with a tunable diffusion coefficient", "symbols": {"v": "probability-flow velocity", "s": "score", "w_t": "inference-time diffusion coefficient"}, "evidence": "paper.pdf p. 5, Eq. (4)", "interpretation": "w_t may be selected after training, but its best value depends on the path and learned parameterization."},
            {"label": "Linear and GVP paths", "latex": r"\text{Linear}:\ (\alpha_t,\sigma_t)=(1-t,t),\qquad \text{GVP}:\ (\alpha_t,\sigma_t)=\left(\cos\frac{\pi t}{2},\sin\frac{\pi t}{2}\right)", "role": "define exact finite-time data-to-noise connections", "symbols": {"t": "interpolation time"}, "evidence": "paper.pdf p. 7, Eq. (12)", "interpretation": "These paths reduce numerical singularities and transport curvature relative to the VP baseline in the reported experiments."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–8: interpolant, velocity-score relation and tunable SDE", "paper.pdf pp. 9–13: controlled design ablations and ImageNet benchmarks", "source PDF SHA-256 9207ad5e0793761417ea4bb02bee888a5ac565bd7877c4652ed8dc93784a5c46", "Evidence status: full-text verified; no independent reproduction performed."],
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
