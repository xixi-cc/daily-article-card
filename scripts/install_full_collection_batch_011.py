#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 011."""

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


def meta(arxiv_id: str, version: str, title: str, authors: list[str],
         categories: list[str], primary: str, published: str,
         abstract: str) -> dict[str, object]:
    return {
        "arxiv_id": arxiv_id, "version": version, "title": title,
        "authors": authors, "categories": categories,
        "primary_category": primary, "published": published,
        "abstract": abstract, "comment": "",
    }


def figure(arxiv_id: str, filename: str, label: str, page: int, role: str,
           alt: str, caption: str, interpretation: str) -> dict[str, object]:
    return {
        "label": label,
        "asset_path": f"assets/collection-figures/{arxiv_id}/{filename}",
        "section": "核心结果与证据", "role": role,
        "evidence": f"paper.pdf p. {page}, {label}", "alt_text": alt,
        "caption": caption, "interpretation": interpretation,
    }


CARDS = [
    {
        "arxiv_id": "2402.00861", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2402.00861",
        "title_en": "Evaluating Large Language Models for Generalization and Robustness via Data Compression",
        "title_zh": "用数据压缩评估大语言模型的泛化与稳健性",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("3a1c7815e90418b3", "Transformer Theory"),
        "verified_metadata": meta(
            "2402.00861", "v2",
            "Evaluating Large Language Models for Generalization and Robustness via Data Compression",
            ["Yucheng Li", "Yunhao Guo", "Frank Guerin", "Chenghua Lin"],
            ["cs.CL", "cs.AI"], "cs.CL", "2024-02-01T18:56:18Z",
            "Lossless compression on a dated 2017–2023 corpus is used to probe post-cutoff generalization and temporal robustness of fourteen language models across text and byte-stream domains.",
        ),
        "sections": [
            sec("作者信息", r"作者：Yucheng Li、Yunhao Guo、Frank Guerin、Chenghua Lin；arXiv:2402.00861v2。全文 13 页，比较 14 个开放权重语言模型以及 Gzip、PNG、FLAC 等传统压缩器。"),
            sec("研究问题", r"常用 benchmark 可能落在模型训练语料内，又会随 prompt 变化。论文把模型视为概率编码器，问两个更接近统计物理外推的问题：给定训练截止时间以前的数据，模型对截止时间以后的同分布演化能否保持低码长；其压缩率随时间漂移的斜率能否量化 robustness，而不是只报告单点 accuracy？"),
            sec("背景", r"Shannon source coding 把预测与压缩联系起来：若模型给序列 \(X=(x_1,\ldots,x_n)\) 的概率为 \(P(X)\)，理想无损码长约为 \(-\log_2 P(X)\)。因此低 negative log-likelihood 对应高压缩效率；按月份组织的数据又把 train/test split 从人工题库改成可审计的时间边界。", r"数据覆盖 2017 年 1 月到 2023 年 11 月，共 83 个月，包括 Wikipedia、BBC news、GitHub code、arXiv、图片字节流和音频字节流。作者把 2017–2022 作为近似训练期，把 2023 作为测试期，并明确区分 performance \(R_{23}\) 与 temporal gap \(R_{23}-R_{17\text{--}22}\)。"),
            sec("模型与方法", r"文本先按模型 context window 切成 token chunks，逐 token 计算条件概率，再用 arithmetic coding 形成无损 bitstream；图片和音频则把每个 byte 映射到保留的 byte token。主指标是压缩率 \(R=\text{compressed size}/\text{raw size}\)，越低越好。", r"比较对象覆盖 6B–70B 参数、2K–32K 原生上下文的 LLaMA、Llama-2、CodeLlama、Mistral、Qwen、Yi、Baichuan2、InternLM 与 ChatGLM3。额外 ablation 比较 2K/4K/8K chunks、2K sliding window 以及 BPT/BPC，避免把 tokenizer 或 context 实现差异误判为模型知识。"),
            sec("核心结果与证据", r"Figure 2a 显示 Wikipedia 压缩率随月份普遍上升；Figure 2b 将 2023 压缩率与 train-test gap 分开后，模型不再沿单一“越大越好”轴排列。作者报告 7B 以内 Mistral-7B 的 performance–robustness balance 最好，较大模型中 Llama-2-70B 最好；这只是该数据与该二维定义下的结果。", r"截止时间效应可见：LLaMA-65B 在 2023 Wikipedia 上相对 2017–2022 的压缩率恶化约 20%。CodeLlama 在 code 上压缩更好，却比基础 Llama-2 显示更大的时间漂移。2023 news、Wikipedia 与 code 普遍更难，arXiv 压缩率却常保持或改善，作者将其归因于学术写作风格较稳定。", r"增大静态 context 从 2K 到 4K、8K 通常继续改善压缩，但收益递减；2K sliding window 在所有列出的模型上又优于较大的非重叠 chunks，代价约为 4 倍计算。所有语言模型在原始 image/audio byte streams 上都远差于专用压缩器，说明文本 tokenizer 的 byte fallback 不是多模态建模。"),
            sec("有效性与局限", r"时间切分减少了显式 benchmark contamination，却不能证明 2023 数据完全未被训练：模型真实语料与 cutoff 往往不公开，release date 只提供上界。Wikipedia 条目具有自相关，arXiv 的写作模板稳定也可能让压缩率改善而不代表新知识理解。", r"压缩率混合了模型概率质量、tokenizer、context policy、arithmetic-coder overhead 与算力预算；它不是 reasoning、factuality 或 safety 的充分统计量。Figure 2 的二维象限还依赖作者选定的 2017–2022/2023 分割，不能把图上的相对位置泛化为模型的全局能力排序。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2402.00861。全文 13 页，PDF SHA-256：29ceff618138b065480e471172016bf757818bae3506d6b76c0cd90300395ae6。", r"复现需保存每月原始文件哈希、模型与 tokenizer revision、byte-token mapping、chunk size/stride、算术编码精度、compressed/raw byte counts、cutoff assumption 与 GPU 时间。应同时报告 \(R_{23}\)、\(R_{17\text{--}22}\) 与逐月曲线，而不是只保留二维排名。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section 2.2 与 Eqs. (1)–(3)，确认“预测即压缩”的精确定义；再看 Figure 1 的 cutoff divergence 与 Figure 2 的 performance–robustness plane。随后查 Tables 3、5、6 分别隔离 domain、context 与 tokenizer 效应，最后用 limitations 检查真实训练语料未知这一识别边界。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/2402.00861/figure-2-performance-robustness.webp",
            "label": "Figure 2", "visual_type": "data_plot",
            "evidence": "paper.pdf p. 7, Figure 2",
            "alt_text": "Wikipedia 月度压缩率曲线以及 2023 表现与训练测试差距的二维散点图。",
            "caption": r"左图显示压缩率随时间漂移；右图把 2023 performance 与 \(R_{23}-R_{17\text{--}22}\) robustness gap 分成两条轴。",
            "selection_rationale": "文章没有机制示意图；Figure 2 是最直接承载核心评价定义和主要比较结论的数据图。",
        },
        "figure_refs": [figure(
            "2402.00861", "figure-2-performance-robustness.webp", "Figure 2", 7,
            "separate post-cutoff compression performance from temporal robustness",
            "多模型的逐月 Wikipedia 压缩率与 performance-robustness 二维散点。",
            "同一模型可以有较低测试压缩率却有较大时间漂移，两者不是同一统计量。",
            "The relative positions depend on the chosen corpus, time split, tokenizer and context policy.",
        )],
        "equation_refs": [
            {"label": "Ideal predictive code length", "latex": r"\ell(X)\simeq-\log_2 P(X)=-\sum_{i=1}^{n}\log_2P(x_i\mid x_{<i})", "role": "connect autoregressive likelihood to lossless compression", "symbols": {"X": "input sequence", "P": "language-model probability", "ell": "ideal code length in bits"}, "evidence": "paper.pdf pp. 2–3, Eqs. (1)–(2)", "interpretation": "A better calibrated predictive distribution assigns a shorter ideal code to unseen data."},
            {"label": "Performance and robustness observables", "latex": r"R_{23}=\frac{B_{23}^{\mathrm{compressed}}}{B_{23}^{\mathrm{raw}}},\qquad \Delta R=R_{23}-R_{17\text{--}22}", "role": "separate post-cutoff performance from temporal drift", "symbols": {"R23": "compression rate on 2023 data", "R17-22": "compression rate on the earlier period", "Delta R": "robustness gap; smaller is better"}, "evidence": "paper.pdf pp. 5–7, Section 5.2 and Figure 2", "interpretation": "A model may compress the test year well but still degrade sharply relative to its earlier-period baseline."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: source-coding argument, arithmetic coding and dated corpus", "paper.pdf pp. 5–8: cutoff, model comparison, context and tokenizer ablations", "source PDF SHA-256 29ceff618138b065480e471172016bf757818bae3506d6b76c0cd90300395ae6", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2403.03206", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2403.03206",
        "title_en": "Scaling Rectified Flow Transformers for High-Resolution Image Synthesis",
        "title_zh": "扩展整流流 Transformer 用于高分辨率图像合成",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("7b0c3330f1be25c0", "Flow Matching"),
        "verified_metadata": meta(
            "2403.03206", "v1", "Scaling Rectified Flow Transformers for High-Resolution Image Synthesis",
            ["Patrick Esser", "Sumith Kulal", "Andreas Blattmann", "Rahim Entezari", "Jonas Müller", "Harry Saini", "Yam Levi", "Dominik Lorenz", "Axel Sauer", "Frederic Boesel", "Dustin Podell", "Tim Dockhorn", "Zion English", "Kyle Lacey", "Alex Goodwin", "Yannik Marek", "Robin Rombach"],
            ["cs.CV", "cs.AI", "cs.LG"], "cs.CV", "2024-03-05T18:45:39Z",
            "Large-scale experiments combine biased timestep sampling for rectified flow with an MM-DiT that uses separate text and image weights, scaling text-to-image synthesis to eight billion parameters.",
        ),
        "sections": [
            sec("作者信息", r"作者：Patrick Esser、Sumith Kulal、Andreas Blattmann 等 17 人；arXiv:2403.03206v1。全文 28 页，后来成为 Stable Diffusion 3 技术路线的核心报告，最大 MM-DiT 模型约 8B parameters。"),
            sec("研究问题", r"rectified flow 以 data–noise 直线路径简化 transport geometry，却常在 \(t\in[0,1]\) 上均匀训练。论文问：不同时间的回归难度并不均匀时，怎样把训练质量集中到 perceptually relevant SNR；同时，text tokens 与 image tokens 是否应共享全部 Transformer weights，还是保留 modality-specific processing 再双向交换信息？"),
            sec("背景", r"生成过程把 data \(x_0\sim p_0\) 与 Gaussian noise \(\epsilon\sim\mathcal N(0,I)\) 连接为 \(z_t=a_t x_0+b_t\epsilon\)，再学习产生同一 marginal path 的 velocity field。rectified flow 取 \(a_t=1-t,b_t=t\)，理想轨迹更直，因而在有限 sampling steps 下可能更高效。", r"但中间 \(t\) 的 source/target 混合最强，velocity target 往往比端点难。改变 timestep density \(\pi(t)\) 等价于改变 loss weighting；论文比较 logit-normal、heavy-tailed mode sampler、CosMap 与 diffusion/EDM baselines，先在受控规模筛选，再进入大模型 scaling。"),
            sec("模型与方法", r"logit-normal sampler 先取 \(u\sim\mathcal N(m,s^2)\)，再令 \(t=\operatorname{sigmoid}u\)，可把训练集中在中间 SNR；主配置 \(m=0,s=1\)。高分辨率阶段还按像素数把 timestep 映射到相同 uncertainty，1024² 训练/采样采用 shift \(\alpha=3\)，并在最终 checkpoint 上做 DPO alignment。", r"MM-DiT 将 VAE image patches 与 CLIP-L/14、CLIP-G/14、T5-XXL text representations 投到共同 token dimension。每个 block 对 text 与 image 使用独立 modulation、linear/MLP weights，但把两种 token 拼接做 joint attention，所以信息双向流动而 modality-specific representation 不被强行共享。QK RMS normalization 用于抑制 attention-logit growth 与 entropy collapse。"),
            sec("核心结果与证据", r"Figure 1 优先展示最大 8B 模型的高分辨率输出：字体、多个对象的空间关系、长 prompt 与不同视觉风格都能在同一网格中直接检查。它证明模型可产生这些类型的样例，但精选图不能代替 aggregate benchmark 和 failure distribution。", r"24 种 sampler/EMA/dataset 组合的排序中，rf/lognorm(0,1) 总体 rank 1.54，优于 uniform rectified flow，并在少步采样保持优势。MM-DiT 对 DiT、CrossDiT、UViT 的 controlled comparison 中验证 loss、CLIP 与 FID 更好；QK normalization 避免 attention logits 持续增长。", r"scaling study 显示 image 与 video validation loss 随参数量、训练 FLOPs 平滑下降，并与 GenEval、T2I-CompBench 和 human preference 相关。GenEval overall 从 depth-18 的 0.58 增至 depth-38 1024²+DPO 的 0.74；表中 DALL-E 3 为 0.67。较大模型还更少依赖采样步数：相对 50 steps，5-step CLIP decrease 从 depth-15 的 4.30% 降到 depth-38 的 2.71%。"),
            sec("有效性与局限", r"8B 结果同时叠加 architecture、data curation、synthetic recaptioning、resolution shift、多个 text encoders 与 DPO，不能从最终样例单独归因到 rectified flow。闭源/开放 baselines 的数据、参数量、prompt filtering 和 inference budget 不同，human-preference win rate 也依赖 rater protocol。", r"论文报告 scaling 范围内未见饱和，不等于更大规模必然继续同一幂律；depth-38 在 \(3\times10^5\) steps 还需调 learning rate 避免 divergence。T5 对长文字 prompt 有明显作用但占用大量 memory；移除 T5 的总体 aesthetic 变化小，却会降低 typography 与复杂 prompt adherence。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2403.03206。全文 28 页，PDF SHA-256：7ba352b6ded12859cda4d47df203d5fe38ee884c45f3b67ff227549d82db1487。", r"复现需固定 VAE、text encoder revisions、dataset/recaption filters、\(\pi(t)\) parameters、loss parameterization、MM-DiT depth/width、QK normalization、EMA、resolution buckets、timestep shift、sampler steps、CFG、DPO data 与 GenEval/human-evaluation protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 建立可视化能力边界，再读 Sections 2–3 推导 flow objective 与 logit-normal sampler。随后看 Figure 2 理解 MM-DiT 的 modality separation，按 Tables 1–2 检查 formulation ablation；最后读 Figures 7–9 与 Tables 5–6，把 scaling、DPO、T5 和少步采样贡献拆开。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/2403.03206/figure-1-high-resolution-samples.webp",
            "label": "Figure 1", "visual_type": "comparison",
            "evidence": "paper.pdf p. 1, Figure 1",
            "alt_text": "8B rectified-flow text-to-image model 生成的多风格高分辨率样例网格，含文字与复杂空间关系。",
            "caption": "8B MM-DiT 的精选样例覆盖 typography、prompt following、spatial reasoning 与多种风格；总体能力仍需结合后文 benchmark。",
            "selection_rationale": "Figure 1 是全文最重要且最具可视性的原图，直接展示目标生成能力，优先于 loss 与 benchmark 数据图。",
        },
        "figure_refs": [figure(
            "2403.03206", "figure-1-high-resolution-samples.webp", "Figure 1", 1,
            "show representative high-resolution outputs of the final eight-billion-parameter model",
            "包含文字、多个对象、空间关系与多种艺术风格的生成图像网格。",
            "样例显示最终系统的 qualitative envelope，但不隔离 rectified-flow、architecture、data 与 DPO 的贡献。",
            "Curated samples must be interpreted together with aggregate GenEval, scaling and human-preference evidence.",
        )],
        "equation_refs": [
            {"label": "Rectified data-noise path", "latex": r"z_t=(1-t)x_0+t\epsilon,\qquad \epsilon\sim\mathcal N(0,I)", "role": "define the straight probability path used by rectified flow", "symbols": {"x0": "data sample", "epsilon": "Gaussian endpoint", "t": "flow time"}, "evidence": "paper.pdf p. 3, Eq. (13)", "interpretation": "A straighter learned transport can reduce integration error in the few-step regime if the velocity field is fitted accurately."},
            {"label": "Logit-normal timestep density", "latex": r"\pi_{\mathrm{ln}}(t;m,s)=\frac{1}{s\sqrt{2\pi}\,t(1-t)}\exp\!\left[-\frac{(\operatorname{logit}t-m)^2}{2s^2}\right]", "role": "bias training toward intermediate signal-to-noise scales", "symbols": {"m": "location in logit time", "s": "scale", "t": "sampled training timestep"}, "evidence": "paper.pdf p. 4, Eq. (19)", "interpretation": "The main m=0, s=1 setting spends less training probability near the easy endpoints than uniform sampling."},
            {"label": "Resolution-dependent timestep shift", "latex": r"t_m=\frac{\alpha t_n}{1+(\alpha-1)t_n},\qquad \alpha=\sqrt{m/n}", "role": "match uncertainty when changing the number of image pixels", "symbols": {"n,m": "source and target pixel counts", "t_n,t_m": "corresponding timesteps", "alpha": "resolution shift factor"}, "evidence": "paper.pdf p. 10, Eq. (23)", "interpretation": "Higher resolutions require a shift toward stronger noise to destroy comparable image information."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: flow objective, timestep densities and MM-DiT architecture", "paper.pdf pp. 6–12: controlled variants, high-resolution shift and scaling", "source PDF SHA-256 7ba352b6ded12859cda4d47df203d5fe38ee884c45f3b67ff227549d82db1487", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2403.00504", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2403.00504",
        "title_en": "Learning and Leveraging World Models in Visual Representation Learning",
        "title_zh": "在视觉表征学习中学习并利用世界模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("5958e2ecc77fb0d7", "World Models"),
        "verified_metadata": meta(
            "2403.00504", "v1", "Learning and Leveraging World Models in Visual Representation Learning",
            ["Quentin Garrido", "Mahmoud Assran", "Nicolas Ballas", "Adrien Bardes", "Laurent Najman", "Yann LeCun"],
            ["cs.CV", "cs.AI", "cs.LG"], "cs.CV", "2024-03-01T13:05:38Z",
            "Image World Models extend JEPA pretraining from masked prediction to conditioned latent prediction of photometric transformations and reuse the learned predictor for efficient downstream adaptation.",
        ),
        "sections": [
            sec("作者信息", r"作者：Quentin Garrido、Mahmoud Assran、Nicolas Ballas、Adrien Bardes、Laurent Najman、Yann LeCun；arXiv:2403.00504v1。全文 23 页，提出 Image World Models（IWM）并在 ImageNet 与下游分类/分割上评估。"),
            sec("研究问题", r"JEPA 通常只预测被遮挡的 latent patches，predictor 训练后常被丢弃。论文问：若把 color jitter、grayscale、blur、solarization 等全局变换视为 action，并显式告诉 predictor 发生了什么，它能否在 latent space 中学会变换的后果；这个 world model 是否可以作为可复用的下游 head，而不只是 pretraining 辅助项？"),
            sec("背景", r"representation invariance 与 world-model capacity 存在张力。若 predictor 不知道 action，最容易的解是让 encoder 抹去颜色等变化，得到 invariant representation；若 predictor 被 action 条件化且有足够容量，encoder 可以保留变化信息，predictor 再把 source latent 推到 target latent，即 equivariant behavior。", r"作者把 MRR 用作 world-model observable：对一个 source latent 施加 action prediction，再在 256 个 augmented target representations 中做 nearest-neighbor retrieval。真实 target 排名越靠前，mean reciprocal rank 越接近 1，说明 latent dynamics 更能恢复该变换。"),
            sec("模型与方法", r"source \(x\) 与 target \(y\) 来自同一图像。target 含 crop、flip、color jitter；source 在 target 上再加 jitter、grayscale、blur、solarization 与四块 mask。online ViT-B/16 encoder \(f_\theta\) 编码 source，EMA teacher \(f_{\theta}^{EMA}\) 编码 target；predictor \(p_\phi\) 同时接收 source patches、target mask positions 与 action parameters \(a_{x\to y}\)。", r"训练用 target-mask positions 上的 squared latent loss。ablation 改变 conditioning（none/sequence/feature）、transformation difficulty 与 predictor depth/width。之后冻结 encoder，finetune 已预训练 predictor 做 classification/segmentation，并与 encoder finetuning、joint finetuning、random predictor 和多任务 predictor 比较。"),
            sec("核心结果与证据", r"Figure 1 是可视化的闭环检验：对 source brain diagram 指定 brightness、contrast、saturation、hue action 后，预测 latent 的 nearest neighbor 与 target 的颜色/清晰度变化一致；grayscale inversion 仍有误差，因为信息已被不可逆删除。图比单个 MRR 更直观地显示 predictor 学到的是 transformation response 而非类别标签。", r"没有 conditioning 时 MRR 为 0.00；sequence 与 feature conditioning 分别为 0.82 与 0.79。对 18-layer predictor，jitter-only MRR 0.25，加入 destructive transforms 后 0.79，strong jitter 后 0.85；12-layer predictor 在 strong jitter 下为 0.81，但稳定达到 equivariance 的训练比例更低，表明 task difficulty 与 capacity 必须匹配。", r"predictor finetuning 中，default ImageNet top-1 为 82.9%，使用 teacher 与 null latents 后为 83.3%。论文报告 equivariant IWM 的 predictor finetuning 可匹配 invariant model 的 encoder finetuning，并在少量 finetuned parameters 下更高效；同一 predictor 联合适配 ImageNet、iNaturalist18、SUN397 与 Places205，平均表现接近四个独立 heads。"),
            sec("有效性与局限", r"所谓 world model 只预测人为定义的 image transformations，并不包含 action-conditioned temporal dynamics、3D geometry 或 agent-environment transition。Figure 1 使用 256-image bank 的 nearest neighbor，因此“看起来正确”受 bank composition 与 retrieval metric 限制。", r"MRR、equivariance 与 downstream quality 相关但不等价：论文自己的 Figure 4 显示 linear probing 与 MRR 负相关、predictor finetuning 与 MRR 正相关、attentive probing 相关较弱。结论依赖 ViT-B/16、ImageNet augmentations 与特定 finetuning protocols，尚不能推到一般 world-model learning。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2403.00504。全文 23 页，PDF SHA-256：fa435ab0b2219bdaaca9693b7dccf6ab285300a970b6001fe5476ac89ae80972。", r"复现需固定 ImageNet split、crop/flip/jitter/destructive augmentation parameters、mask geometry、action encoding、EMA decay、ViT-B/16 revision、predictor depth/width、MRR bank size 256、nearest-neighbor metric 与 finetuning parameter counts。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把 action-conditioned latent prediction 与 ordinary invariance 区分开；再读 Section 3 的 source/target/action construction 和 Tables 1–2 的三因素 ablation。随后读 Tables 3–7 的 predictor reuse，最后看 Figures 4–5：不同 abstraction level 要用不同 evaluation head，不能只靠 linear probe 排名。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/2403.00504/figure-1-latent-transformations.webp",
            "label": "Figure 1", "visual_type": "comparison",
            "evidence": "paper.pdf p. 1, Figure 1",
            "alt_text": "source brain image、四组 photometric actions、IWM nearest-neighbor predictions 与 target images。",
            "caption": "给定 photometric action 后，IWM 在 latent space 预测变换结果；nearest-neighbor 图像可直接对照 prediction 与 target。",
            "selection_rationale": "Figure 1 是文章最重要的可视化证据，直接展示 latent world model 的作用，优先于 MRR 和下游 accuracy 表。",
        },
        "figure_refs": [figure(
            "2403.00504", "figure-1-latent-transformations.webp", "Figure 1", 1,
            "visualize action-conditioned predictions in latent space",
            "四种 photometric action 下的 source、nearest-neighbor prediction 与 target 图像。",
            "prediction 跟随 brightness、contrast、saturation 与 hue，但不可逆 grayscale 仍暴露信息损失。",
            "Nearest-neighbor visualization depends on the finite 256-image retrieval bank and is not pixel reconstruction.",
        )],
        "equation_refs": [
            {"label": "Action-conditioned latent prediction", "latex": r"\hat z_y=p_\phi\!\left(f_\theta(x),a_{x\to y},m_a\right),\qquad z_y=f_{\theta}^{EMA}(y)", "role": "define the predictor as a latent world model conditioned on the transformation", "symbols": {"x,y": "source and target views", "a_x_to_y": "transformation parameters", "m_a": "target mask tokens", "p_phi": "world-model predictor"}, "evidence": "paper.pdf p. 4, Section 3", "interpretation": "Explicit action information prevents the predictor from being forced into a purely invariant solution."},
            {"label": "IWM pretraining loss", "latex": r"\mathcal L(x,y)=\sum_{i\in M_x^C}\left\|p_\phi\!\left(f_\theta(x),a_{x\to y},m_a\right)_i-f_{\theta}^{EMA}(y)_i\right\|_2^2", "role": "match predicted and teacher target latents at selected positions", "symbols": {"M_x^C": "target positions complementary to the source mask", "theta": "online encoder parameters", "phi": "predictor parameters"}, "evidence": "paper.pdf p. 4, Loss", "interpretation": "The objective trains transformation-aware latent prediction without reconstructing pixels."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: IWM construction, conditioning, MRR and capacity ablations", "paper.pdf pp. 6–9: predictor finetuning, multitask reuse and abstraction spectrum", "source PDF SHA-256 fa435ab0b2219bdaaca9693b7dccf6ab285300a970b6001fe5476ac89ae80972", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2402.19451", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2402.19451",
        "title_en": "Reduced density fluctuations via anti-aligning in active matter",
        "title_zh": "反对齐相互作用降低活性物质中的密度涨落",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("25f3280f90e7488d", "Active Matter"),
        "verified_metadata": meta(
            "2402.19451", "v2", "Reduced density fluctuations via anti-aligning in active matter",
            ["Horst-Holger Boltz", "Thomas Ihle"],
            ["cond-mat.stat-mech", "cond-mat.soft"], "cond-mat.stat-mech", "2024-02-29T18:48:54Z",
            "A Poisson-representation solution of an anti-aligning active lattice gas and off-lattice simulations show long-range suppression of density fluctuations, while warning that apparent noninteger hyperuniform exponents can hide a finite small-wave-number offset.",
        ),
        "sections": [
            sec("作者信息", r"作者：Horst-Holger Boltz、Thomas Ihle；arXiv:2402.19451v2。全文 10 页，结合一维可解格点过程与二维 anti-aligning Vicsek-like agent simulations。"),
            sec("研究问题", r"无全局序、无排斥体积的 self-propelled particles 是否仍能建立足够长程的反关联来压低密度涨落？更尖锐地说：有限尺寸模拟中看到 \(S(k)\sim k^{\alpha}\) 的非整数斜率时，能否据此宣称 hyperuniformity，还是它可能只是 \(S(k)=S_0+A k^2\) 在有限波数窗口中的假幂律？"),
            sec("背景", r"严格 hyperuniformity 要求 \(\lim_{k\to0}S(k)=0\)。活性系统常报告非整数 \(\alpha\)，但最低可访问波数为 \(2\pi/L\)，小而非零的 offset \(S_0\) 很容易与幂律混淆。反对齐会不断重排邻居，宏观上看似自混合，却可能通过方向—密度耦合形成非局域 anticorrelation。", r"一维模型含向右/向左运动的两类粒子，按内部方向以速率 \(v\) 跳到相邻格点，并以依赖局部两种 occupancy 的速率互相转换。Figure 1 同时画出 microscopic hopping/conversion 与从整数 occupancy \(n_i^{\pm}\) 到复 Poisson fields \(\alpha_i,\beta_i\) 的表示。"),
            sec("模型与方法", r"作者从 master equation 引入 Poisson representation，把离散概率分布写成局部 Poisson process 的复 rate 混合。对总密度场 \(\tilde\rho=\alpha+\beta\) 与极化场 \(\tilde m=\alpha-\beta\) 得到 coupled Langevin equations。conversion 引出的 imaginary noise 不是 imaginary observable，而是 sub-Poisson number statistics 的记号：它降低方差而非增加方差。", r"线性化并消去快速极化模后得到密度的扩散型 Langevin equation，但噪声是梯度相关的。解析解给出 \(S(k)=\rho_0-c^2(1-\cos k)/(Dk^2)\)，所以 \(S(k)=S_0+(c^2/24D)k^2+\cdots\)。二维部分直接积分 anti-aligning Vicsek equations，跨 \(N=2^5\) 到 \(2^{12}\)、多组 density/coupling 和 orientational noise 比较 \(S(k)\) 与 window number fluctuations。"),
            sec("核心结果与证据", r"Figure 1 说明关键机制链条：局部反对齐先改变两种方向粒子的转换统计，Poisson representation 再把这种非 Poisson correlation 编码为复场噪声；这比单看最终 \(S(k)\) 曲线更能解释为什么没有排斥也能压低密度涨落。", r"一维解析式预测低波数不是一般的 anomalous power law，而是 finite offset 加整数 \(k^2\) correction。若只在约半个 decade 上对 raw \(S(k)\) 拟合，会得到约 \(k^{0.25}\) 的伪 anomalous exponent；减去推断的 \(S_0\) 后数据与 \(k^2\) 一致。", r"二维无噪声 simulations 的 raw data 看似给出 \(\alpha\approx0.5\)，但同样可由 \(S(k)-S_0\propto k^2\) 描述。小 orientational noise 仍保留 suppression，强噪声使其崩解；不同 \(M=\rho\pi R^2\) 与 \(S_c=\Gamma R/v\) 下 offset 和表观斜率变化，支持“reduced fluctuations”而非已证明的 universal hyperuniform exponent。"),
            sec("有效性与局限", r"一维模型可解析但几何上高度受限，且复 Poisson fields 是辅助变量；从它到二维 off-lattice dynamics 的连接是机制类比，不是 universality proof。二维结果没有 \(k\to0\) 的解析控制，有限 \(L\) 不能区分非常小的 \(S_0>0\) 与真正 \(S_0=0\)。", r"作者因此有意使用“ostensible hyperuniformity”：数据证明长程涨落显著降低，却不能确定严格 hyperuniformity。数值采用确定性或加白噪声的特定 Vicsek-like equations，未包含 steric collisions、hydrodynamics 或实验噪声；拟合 \(S_0\) 与 exponent 的协方差也需更大系统检验。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2402.19451。全文 10 页，PDF SHA-256：827a61cccb4ca4ec2ccab85c861765ebf4611fc2d611d8f408f165f12864058d。", r"复现一维部分需固定 hopping/conversion rates、Gillespie clock、\(\rho_0=16\)、lattice size 与低 \(k\) 拟合窗口；二维部分需固定 Heun step、\(M,S_c,N,t=500\pi\)、样本数 \(10^4\)、noise convention 与 \(S_0\) inference。必须同时保存 raw \(S(k)\) 和 \(S(k)-S_0\)，否则无法诊断伪幂律。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 把 microscopic conversion、Poisson fields 和 imaginary noise 连起来；再读 Eqs. (24)–(30)，特别比较 \(S_0+A k^2\) 与纯 \(k^{\alpha}\)。随后并排看 Figures 3–6 的 raw/reduced structure factors，最后读 Discussion，保留作者对 strict hyperuniformity 的克制结论。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/2402.19451/figure-1-lattice-process.webp",
            "label": "Figure 1", "visual_type": "schematic",
            "evidence": "paper.pdf p. 2, Figure 1",
            "alt_text": "一维左右运动粒子的反对齐转换，以及 occupancy 到复 Poisson fields 的映射。",
            "caption": r"方向转换建立非 Poisson 反关联；复 Poisson fields \(\alpha_i,\beta_i\) 把这一涨落抑制写成可解的 Langevin dynamics。",
            "selection_rationale": "Figure 1 是文章唯一清晰的机制示意图，能解释涨落抑制的微观起点，优先于容易被误读为幂律的数据图。",
        },
        "figure_refs": [figure(
            "2402.19451", "figure-1-lattice-process.webp", "Figure 1", 2,
            "connect anti-aligning microscopic dynamics to the Poisson-field representation",
            "左右运动粒子的 hopping/conversion 图与局部 occupancy 分布到复 Poisson rates 的映射。",
            "反对齐通过方向转换修改局部 number statistics，Poisson representation 使其长程后果可解析。",
            "The schematic does not by itself establish strict two-dimensional hyperuniformity.",
        )],
        "equation_refs": [
            {"label": "Poisson-field Langevin dynamics", "latex": r"\partial_t\tilde\rho=-v\nabla\tilde m,\qquad \partial_t\tilde m=-v\nabla\tilde\rho-r_0\tilde m-r_1\tilde\rho\tilde m+i\sqrt{r_1\tilde\rho}\,\xi", "role": "encode density-polarization coupling and sub-Poisson fluctuations", "symbols": {"rho_tilde": "Poisson field for total density", "m_tilde": "Poisson field for orientational imbalance", "v": "self-propulsion rate", "xi": "real Gaussian white noise"}, "evidence": "paper.pdf pp. 4–5, Eqs. (23)–(24)", "interpretation": "The imaginary coefficient is an auxiliary representation of variance suppression; physical moments remain real."},
            {"label": "Low-wave-number structure factor", "latex": r"N S(k)=\rho_0-\frac{c^2}{Dk^2}(1-\cos k)=\underbrace{\left(\rho_0-\frac{c^2}{2D}\right)}_{S_0}+\frac{c^2}{24D}k^2+O(k^4)", "role": "distinguish a finite offset plus analytic correction from an anomalous power law", "symbols": {"S(k)": "density structure factor", "rho0": "mean occupancy", "c": "effective correlated-noise strength", "D": "effective diffusivity"}, "evidence": "paper.pdf p. 5, Eqs. (29)–(30)", "interpretation": "A finite measurement window can fit the crossover as a noninteger exponent even when the asymptotic correction is quadratic."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: Poisson representation, Langevin fields and analytic structure factor", "paper.pdf pp. 6–8: one- and two-dimensional finite-size simulations", "source PDF SHA-256 827a61cccb4ca4ec2ccab85c861765ebf4611fc2d611d8f408f165f12864058d", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2402.04997", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2402.04997",
        "title_en": "Generative Flows on Discrete State-Spaces: Enabling Multimodal Flows with Applications to Protein Co-Design",
        "title_zh": "离散状态空间上的生成流：面向蛋白质协同设计的多模态流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("0860001a6e00e36b", "Flow Matching"),
        "verified_metadata": meta(
            "2402.04997", "v2",
            "Generative Flows on Discrete State-Spaces: Enabling Multimodal Flows with Applications to Protein Co-Design",
            ["Andrew Campbell", "Jason Yim", "Regina Barzilay", "Tom Rainforth", "Tommi Jaakkola"],
            ["cs.LG", "cs.AI", "q-bio.BM"], "cs.LG", "2024-02-07T16:15:36Z",
            "Discrete Flow Models realize flow matching with continuous-time Markov chains and combine it with continuous SE(3) flows in Multiflow for joint protein sequence and backbone generation.",
        ),
        "sections": [
            sec("作者信息", r"作者：Andrew Campbell、Jason Yim、Regina Barzilay、Tom Rainforth、Tommi Jaakkola；arXiv:2402.04997v2。全文 60 页，正文提出 Discrete Flow Models（DFM）并以 Multiflow 做蛋白质 backbone–sequence co-generation。"),
            sec("研究问题", r"连续 flow matching 依赖速度场，离散序列却不能沿欧氏向量场平滑移动。论文问：能否在有限状态空间中定义一个精确的 probability flow，使训练保持 simulation-free、采样时仍可控制随机性；并把这一离散过程与 \(\mathbb R^3\times SO(3)\) 的连续蛋白结构流组合成单一多模态生成器？"),
            sec("背景", r"有限状态连续时间 Markov chain（CTMC）由初始分布 \(p_0\) 与 rate matrix \(R_t\) 决定。Kolmogorov forward equation \(\partial_t p_t=R_t^{\mathsf T}p_t\) 扮演连续空间 continuity/Fokker–Planck equation 的角色：它只规定概率质量怎样在类别之间流动，不要求类别本身有欧氏距离。", r"作者先选一个可显式采样的 conditional path \(p_{t|1}(x_t|x_1)\)，从 uniform 或 mask noise 线性插值到 data。神经网络只学习 denoising posterior \(p_{1|t}(x_1|x_t)\)；生成时再把 conditional rates 对这个 posterior 取期望，得到 marginal rate matrix。"),
            sec("模型与方法", r"DFM 以 cross-entropy 训练 clean-state predictor，训练目标与具体 rate matrix 解耦。满足同一 probability path 的 rates 不唯一：在最小跳跃的 \(R_t^*\) 上加入对 \(p_{t|1}\) 满足 detailed balance 的 \(\eta R_t^{DB}\)，不会改变边缘分布，却会改变 CTMC trajectory 的跳跃频率和 autocorrelation。于是 \(\eta\) 成为 inference-time stochasticity knob。", r"Multiflow 把每个 residue 表为 \(T^d=(x^d,r^d,a^d)\in\mathbb R^3\times SO(3)\times\{1,\ldots,20,M\}\)。translation、rotation 和 amino-acid sequence 的 conditional flows 在 residue 维和 modality 维上因子化，但同一个网络以完整 noisy protein 为条件同时预测三种终态；从 noise、给定 structure 或给定 sequence 出发分别实现 co-design、inverse folding 和 forward folding。"),
            sec("核心结果与证据", r"Figure 1 将方法浓缩成三幅机制图：A 是 mask-to-sequence probability flow，B 显示增大 \(\eta\) 会在保持同一 \(p_t\) 时增加 CTMC jumps，C 显示同一 Multiflow 权重可从纯噪声、已知 backbone 或已知 sequence 三个边界条件采样。图直接说明“同一边缘流、不同路径随机性”和多模态条件化。", r"text8 上，作者可在采样时联合调 \(\eta\) 与 temperature；\(\eta=15\) 改善 entropy–NLL Pareto frontier，而 \(\eta=0\) 接近 D3PM，支持 DFM 是离散 diffusion 的连续时间推广。该改进是 sampler flexibility 的结果，不是重新训练不同模型。", r"蛋白 co-design benchmark 中，Multiflow 的 Co-design-1 designability 为 0.86、diversity 143、novelty 0.61；PMPNN-8 structure designability 为 0.99。去掉 distillation 后 Co-design-1 designability 降到 0.42。相同权重做 inverse folding 得到 scRMSD \(2.2\pm2.6\) Å，接近 ProteinMPNN 的 \(1.9\pm2.7\) Å；forward folding RMSD 为 \(15.3\pm4.5\) Å，明显弱于 ESMFold 的 \(2.7\pm3.9\) Å。"),
            sec("有效性与局限", r"DFM 的 marginal correctness 由 Kolmogorov equation 与 conditional-rate construction 保证，但有限 Euler step、learned posterior error 与 temperature 会造成离散化和模型误差。详细平衡项只保持目标 marginal flow，并不意味着生成动力学具有物理 detailed balance。", r"蛋白实验只生成 backbone 与 sequence，不包含 side chains；PDB 训练集有 18,684 proteins，distillation 又使用 PMPNN 与自生成的 4,179 个样本，因此性能不等于纯粹从原始数据学得。Multiflow 是 general-purpose proof of concept，却没有同时达到专用 forward-folding 模型的精度。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2402.04997；DFM 代码：https://github.com/andrew-cr/discrete_flow_models；Multiflow 代码：https://github.com/jasonkyuyim/multiflow。全文 60 页，PDF SHA-256：182ddfb2871ce2d07e40b83f507b6ae356634af1961e049cc6d2fa67f5bed374。", r"复现需固定 conditional path、mask/uniform prior、Euler step、\(\eta\)、temperature、network revision、PDB split、distillation recipe、PMPNN samples、ESMFold/AF2 version，以及 designability 的 \(\mathrm{scRMSD}<2\) Å 阈值。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，再读 Section 2.2 的 Kolmogorov equation 与 Propositions 3.1–3.4，确认 \(p_t\)、trajectory 与 rate matrix 是三个不同对象。随后用 Table 1 对照连续/离散 flow matching，最后读 Tables 3–4；尤其要把 co-design 的强结果与 forward folding 的明显短板一起保留。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/2402.04997/figure-1-dfm-overview.webp",
            "label": "Figure 1", "visual_type": "schematic",
            "evidence": "paper.pdf p. 2, Figure 1",
            "alt_text": "离散 mask flow、CTMC 高低随机性轨迹以及蛋白结构与序列三种条件生成路径。",
            "caption": r"同一 \(p_t\) 可由不同随机性的 CTMC 轨迹实现；离散 sequence flow 再与连续 structure flow 组合为 Multiflow。",
            "selection_rationale": "Figure 1 是论文最重要的机制示意图，同时解释离散流、采样随机性和蛋白多模态条件生成，优先于性能表。",
        },
        "figure_refs": [figure(
            "2402.04997", "figure-1-dfm-overview.webp", "Figure 1", 2,
            "show the discrete probability path, CTMC stochasticity, and multimodal conditioning modes",
            "三联图展示 mask 序列的概率流、不同跳跃频率与蛋白 sequence/structure 联合生成。",
            "改变 CTMC 轨迹随机性不必改变目标边缘流；一个联合模型可切换多种条件边界。",
            "The schematic explains the construction, not the finite-step sampling error or protein benchmark distribution.",
        )],
        "equation_refs": [
            {"label": "Discrete probability-flow equation", "latex": r"\partial_t p_t(x)=\sum_{j\ne x}R_t(j,x)p_t(j)-\sum_{j\ne x}R_t(x,j)p_t(x)=\bigl(R_t^{\mathsf T}p_t\bigr)(x)", "role": "define probability transport on a finite state space", "symbols": {"p_t": "time-dependent categorical marginal", "R_t": "CTMC rate matrix", "x,j": "discrete states"}, "evidence": "paper.pdf p. 3, Eq. (4)", "interpretation": "Incoming minus outgoing probability mass replaces the divergence of a continuous velocity field."},
            {"label": "Posterior-averaged generative rate", "latex": r"R_t(x,j)=\mathbb E_{p_{1|t}(x_1|x)}\!\left[R_t(x,j\mid x_1)\right]", "role": "turn an explicit data-conditional process into the learned marginal generator", "symbols": {"x1": "clean endpoint", "p_1|t": "denoising posterior", "R_t(x,j|x1)": "conditional rate"}, "evidence": "paper.pdf p. 3, Eq. (7)", "interpretation": "The neural network predicts endpoints; analytic conditional rates then determine how probability jumps between current states."},
            {"label": "Inference-time stochasticity family", "latex": r"R_t^{\eta}=R_t^*+\eta R_t^{DB},\qquad \eta\ge0", "role": "change CTMC trajectory stochasticity without changing the marginal flow", "symbols": {"R_t^*": "base rate with minimal expected jumps for the chosen paths", "R_t^DB": "rate satisfying detailed balance for the conditional path", "eta": "sampling stochasticity"}, "evidence": "paper.pdf pp. 4–5, Proposition 3.3", "interpretation": "Detailed-balance exchanges cancel in the marginal equation but alter the number and timing of jumps."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: CTMC flow construction, training and rate-matrix family", "paper.pdf pp. 7–9: text8 and protein experiments", "paper.pdf Appendix: proofs and finite-step sampling details", "source PDF SHA-256 182ddfb2871ce2d07e40b83f507b6ae356634af1961e049cc6d2fa67f5bed374", "Evidence status: full-text verified; no independent reproduction performed."],
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
