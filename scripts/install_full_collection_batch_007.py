#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 007."""

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
        "arxiv_id": "2210.11058", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2210.11058",
        "title_en": "Representation Learning with Diffusion Models", "title_zh": "用扩散模型学习语义表征",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("76d3033b1386cf39", "Generative Models"),
        "verified_metadata": meta("2210.11058", "v1", "Representation Learning with Diffusion Models", ["Jeremias Traub"], ["cs.CV"], "cs.CV", "2022-10-20T07:26:47Z", "A latent diffusion model is jointly conditioned on a KL-regularized representation encoder to obtain a tractable semantic latent space."),
        "sections": [
            sec("作者信息", "作者：Jeremias Traub；arXiv:2210.11058v1。本文是一篇 74 页硕士论文，本卡按全文而非摘要核对。"),
            sec("研究问题", "Latent diffusion model 能高质量生成，却会在正向扩散中逐级抹去样本信息，因此其中间变量不是稳定、可解释的语义坐标。论文问：能否给扩散模型增加一个可采样的表征自由度，同时兼顾无条件生成、重构与语义插值？"),
            sec("背景", "普通 LDM 从高斯末态反演压缩图像 latent；VAE 则用 KL 项把编码分布压向简单先验。LRDM 把两者耦合：表征编码器从干净 latent 提取 \(r\)，扩散 U-Net 在每个去噪时刻以 \(r\) 为条件。", "从物理角度看，\(r\) 像一组慢变量：它约束宏观语义，扩散轨道负责补齐未被它固定的微观细节；这只是学习到的尺度分工，并非可辨识性定理。"),
            sec("模型与方法", "编码器给出高斯近似后验 \(q_\phi(r\mid z_0)\)，先验取 \(p(r)=\mathcal N(0,I)\)。训练把 image-parameterized diffusion 重构项与 \(\lambda D_{\mathrm{KL}}\) 相加；\(\lambda\) 决定表征的信息容量与直接从先验采样的可行性。", "作者还考察 timestep-conditional t-LRDM、类别条件表征，以及形状/风格的分离实验。"),
            sec("核心结果与证据", "Figure 4.7 显示：VQ-AE 插值更像像素混合，DDIM 的变化不够平滑，而 LRDM 在身份与场景语义之间形成连续过渡。这是表征几何最直接的证据。", "LSUN Churches 上，\(\lambda=10^{-6},10^{-4},5\times10^{-4}\) 的 FID 分别为 457.70、58.08、10.54，而 reconstruction FID 分别为 6.03、8.63、13.30：更强先验匹配改善无条件采样，却牺牲重构。", "400 epoch 的 image-parameterized LDM 达到 FID 5.64；因此 LRDM 的贡献是语义 latent 与单一先验采样，不是胜过充分训练 LDM 的生成质量。"),
            sec("有效性与局限", "结论主要来自有限图像数据集与单篇硕士论文中的配置；没有证明 \(r\) 的语义因素唯一、独立或可跨域迁移。", "性能强烈依赖 \(\lambda\)：弱 KL 导致 aggregated posterior 偏离高斯先验，强 KL 则损害重构。t-LRDM 在相同 100 epoch 预算下更差，而且每次反向步计算更贵。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2210.11058；代码：https://github.com/jeremiastraub/diffusion。", "全文 74 页，PDF SHA-256：462de2436e79df363e84deefb002f1a4a7b8520580bbb394d953d9da88fca7d3。复现需固定 autoencoder、image/noise parameterization、表征尺寸、\(\lambda\)、训练 epoch 与采样步数。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Eq. (2.35) 与 Figure 4.4，理解表征分支怎样进入去噪网络；再看 Figure 4.7 和 Table 4.2，把语义连续性、重构质量和 prior sampling 分开。最后检查 \(\lambda\) 扫描，不要把漂亮插值等同于表征可辨识。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2210.11058/figure-4-7-semantic-interpolation.webp", "label": "Figure 4.7", "visual_type": "comparison", "evidence": "paper.pdf p. 41, Figure 4.7", "alt_text": "VQ-AE、DDIM 与 LRDM 的图像插值序列。", "caption": "LRDM 在端点之间给出更连续的语义变化；图像细节由条件扩散解码器补足。", "selection_rationale": "该图直接检验论文的核心对象——表征空间的语义几何，比单独的 FID 表更有解释力。"},
        "figure_refs": [figure("2210.11058", "figure-4-7-semantic-interpolation.webp", "Figure 4.7", 41, "compare representation geometry", "三种模型在图像端点之间的插值。", "LRDM 的路径主要沿语义属性连续变化。", "The visual evidence supports semantic smoothness, not unique disentanglement.")],
        "equation_refs": [{"label": "LRDM objective", "latex": r"\mathcal L_{\mathrm{LRDM}}=\mathbb E\!\left[\|z_0-z_{0,\theta}(z_t,t,r(z_0))\|_2^2\right]+\lambda D_{\mathrm{KL}}\!\left(q_\phi(r\mid z_0)\|p(r)\right)", "role": "couple diffusion reconstruction to a sampleable representation prior", "symbols": {"r": "learned representation", "lambda": "prior regularization strength", "z_t": "noised autoencoder latent"}, "evidence": "paper.pdf p. 23, Eq. (2.35)", "interpretation": "The KL term trades reconstruction information for agreement with the Gaussian representation prior."}],
        "evidence_refs": ["paper.pdf pp. 22–24: LRDM objective and graphical model", "paper.pdf pp. 39–46: interpolation and regularization study", "source PDF SHA-256 462de2436e79df363e84deefb002f1a4a7b8520580bbb394d953d9da88fca7d3", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2211.01364", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2211.01364",
        "title_en": "An optimal control perspective on diffusion-based generative modeling", "title_zh": "扩散生成模型的随机最优控制视角",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("1e672de62d14de31", "Control & Reinforcement Learning"),
        "verified_metadata": meta("2211.01364", "v3", "An optimal control perspective on diffusion-based generative modeling", ["Julius Berner", "Lorenz Richter", "Karen Ullrich"], ["cs.LG", "math.OC", "stat.ML"], "cs.LG", "2022-11-02T17:59:09Z", "Stochastic optimal control yields the diffusion ELBO, a path-space KL interpretation, and a sampler for unnormalized densities."),
        "sections": [
            sec("作者信息", "作者：Julius Berner、Lorenz Richter、Karen Ullrich；arXiv:2211.01364v3。全文 43 页。"),
            sec("研究问题", "扩散生成模型通常从 score matching 或变分推断推导。论文追问其背后是否存在统一的随机控制结构，以及该结构能否反过来构造只知道未归一化密度 \(\rho\) 的采样器。"),
            sec("背景", "Hamilton–Jacobi–Bellman 方程控制 log-density 的演化；verification theorem 把任意可行控制的代价与最优 value function 比较。Girsanov 定理则把 drift 改变写成路径测度的 KL。", "因此 diffusion ELBO 不只是代数技巧：它是控制代价对路径空间 KL 的上界表达。"),
            sec("模型与方法", "DIS 先从目标分布出发定义一条正向扩散 \(Y\)，使终态近似高斯；再从高斯初态训练受控反向过程 \(X^u\) 回到目标。目标函数包含控制轨道代价与端点密度比。", "控制场用神经网络与解析 score 插值共同参数化；训练模拟整条 Euler–Maruyama 轨道，并可用 importance weights 估计归一化常数与观测量。"),
            sec("核心结果与证据", "Figure 3 在 20 维 double-well 上展示从高斯初态向多阱目标演化的受控轨迹、终点样本与 KDE；它把抽象的路径测度匹配变成可见的输运过程。", "在 Gaussian mixture 与 Funnel 上，DIS 的 log-normalizer 误差优于论文实现的 PIS；double-well 上优势较小。10 seeds、每批 \(N=100,200,400,800\) 的观测量估计中，DIS 也总体优于 PIS。", "理论恒等式表明最小 DIS 代价等于端点 KL 减去 \(\log Z\)；但只有当反向过程的初态真正匹配正向终态时，最优控制才保证正确目标边缘。"),
            sec("有效性与局限", "若 \(p_{X_0}\neq p_{Y_T}\)，控制无法消除这项初态错配；增大扩散时间可缓解，却增加轨迹离散和反向传播成本。", "实验依赖目标 score 与完整轨迹梯度；离散 SDE 会给 importance estimator 引入偏差。作者还改进了 PIS 实现，因此跨论文预算比较需谨慎。", "路径空间 KL 控制的是整条随机轨道；终点密度、归一化常数与具体观测量的方差仍需分别检验。尤其在多峰目标上，终点 KDE 看似正确并不能排除低概率模态遗漏或 importance weights 被极少数轨道支配。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2211.01364；代码：https://github.com/juliusberner/sde_sampler。", "全文 43 页，PDF SHA-256：acc14bcda73d11c0a46913696e81622d5add9b147b042754a6b5c1486949e5ba。复现应固定 SDE 系数、时间网格、batch、目标 score、控制参数化和 importance-weight 计算。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Corollary 3.1 的 Eqs. (19)–(20)，确认损失、端点 KL 与 \(\log Z\) 的关系；再看 Figure 3。最后核对 Appendix 的离散化和初态近似，区分连续时间恒等式与实际 estimator。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2211.01364/figure-3-dis-trajectories.webp", "label": "Figure 3", "visual_type": "trajectory", "evidence": "paper.pdf p. 8, Figure 3", "alt_text": "受控扩散从高斯分布输运到 double-well 目标的轨迹和密度。", "caption": "DIS 学习整条受控随机轨道，而非仅拟合终点样本；右侧密度检验终态是否覆盖目标势阱。", "selection_rationale": "该图把随机控制、轨迹测度与目标采样三个核心概念连接起来，并同时显示路径演化、终点样本和目标密度，优先于单独的误差数据表。"},
        "figure_refs": [figure("2211.01364", "figure-3-dis-trajectories.webp", "Figure 3", 8, "visualize controlled stochastic transport", "double-well 上的 DIS 轨迹、样本和密度。", "高斯初态经受控扩散进入多阱目标。", "Endpoint agreement depends on both the learned control and the initial-marginal approximation.")],
        "equation_refs": [{"label": "DIS variational identity", "latex": r"D_{\mathrm{KL}}\!\left(P_{X_0^u}\|P_{Y_T}\right)-\log Z=\min_{u\in\mathcal U}\mathcal L_{\mathrm{DIS}}(u)", "role": "link stochastic-control cost to endpoint mismatch and normalization", "symbols": {"u": "control", "Z": "target normalizer", "P_X": "controlled endpoint law", "P_Y": "forward-diffusion terminal law"}, "evidence": "paper.pdf p. 7, Eq. (20)", "interpretation": "The learned control is exact only after accounting for the endpoint-prior mismatch."}],
        "evidence_refs": ["paper.pdf pp. 4–8: control-theoretic derivation and DIS", "paper.pdf pp. 9–13: numerical comparisons", "source PDF SHA-256 acc14bcda73d11c0a46913696e81622d5add9b147b042754a6b5c1486949e5ba", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2211.03595", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2211.03595",
        "title_en": "From Denoising Diffusions to Denoising Markov Models", "title_zh": "从去噪扩散到去噪马尔可夫模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("7a3611fad241760c", "Generative Models"),
        "verified_metadata": meta("2211.03595", "v3", "From Denoising Diffusions to Denoising Markov Models", ["Joe Benton", "Yuyang Shi", "Valentin De Bortoli", "George Deligiannidis", "Arnaud Doucet"], ["stat.ML", "cs.LG"], "stat.ML", "2022-11-07T14:34:27Z", "A generator-based framework extends denoising diffusion and score matching to discrete, manifold, and simplex state spaces."),
        "sections": [
            sec("作者信息", "作者：Joe Benton、Yuyang Shi、Valentin De Bortoli、George Deligiannidis、Arnaud Doucet；arXiv:2211.03595v3。全文 56 页。"),
            sec("研究问题", "标准 score diffusion 依赖欧氏空间的梯度与布朗运动。论文问：能否只用 Markov generator、参考测度与时间反演，统一处理 \(\mathbb R^d\)、离散状态、Riemannian 流形和概率单纯形？"),
            sec("背景", "连续时间 Markov 过程由生成元 \(L\) 描述局部演化；其 adjoint 控制密度的 forward equation。Feynman–Kac 把模型 likelihood 表成辅助过程上的加权期望，广义 Girsanov 再把它转换到已知 noising process。"),
            sec("模型与方法", "模型用正函数 \(\beta(x,t)\) 参数化可逆生成过程。Theorem 1 给出 ELBO；去掉与参数无关的项后得到 generalized implicit score matching，另有等价 denoising objective。最优解满足 \(\beta(x,t)\propto q_t(x)\)。", "同一构造在欧氏空间退化为 score diffusion，在有限状态空间变为 CTMC，在流形上使用几何扩散，在 simplex 上可用 Wright–Fisher 过程。"),
            sec("核心结果与证据", "Figure 6 在 \(SO(3)\) 上给出两种物体从二维视图推断三维姿态的真值与模型分布；模型复现由物体对称性产生的多峰旋转分布。", "14×14 MNIST inpainting 中，离散 DMM 的 PSNR/SSIM 为 16.63/0.757；连续模型 raw 为 16.72/0.706，rounded 为 16.75/0.723。不同状态空间改变了结构指标，而不只是像素误差。", "利用解析 \(SO(3)\) transition 的训练比相关流形 diffusion 基线约快 15%，likelihood 相近。simplex 的模型 log-likelihood 在 \(N=3,5,10,20\) 时均接近真实值。"),
            sec("有效性与局限", "统一公式依赖 Feller process、adjoint 与 Radon–Nikodym 等正则条件；无限维或奇异参考测度下未必成立。", "有限数据经验分布相对连续参考测度可为奇异，论文的 density 表达需平滑 noising 才可用。理论给出 objective 等价性，但没有一般有限样本误差或离散积分保证。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2211.03595；代码：https://github.com/oxcsml/denoising_markov_models。", "全文 56 页，PDF SHA-256：d1f2aff73c5a5d61c4b503b47f3610e02bdad5ef84c04fd2096029f24ab0b643。复现需固定生成元、参考测度、transition sampler、时间积分和 manifold 坐标约定。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Theorem 1 与 Eqs. (8)–(10)，把 likelihood、隐式 objective 与 denoising objective 对齐；再按 Euclidean、discrete、manifold 三个例子检查退化极限。最后看 Figure 6，区分对称性诱导的多峰与预测不确定性。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2211.03595/figure-6-so3-pose.webp", "label": "Figure 6", "visual_type": "distribution", "evidence": "paper.pdf p. 14, Figure 6", "alt_text": "两个物体及其在 SO(3) 上的真值和模型姿态分布。", "caption": "DMM 在旋转群上复现由物体对称性导致的多峰后验，展示框架超越欧氏像素空间的意义。", "selection_rationale": "这是论文最清晰的非欧氏状态空间可视化，比通用框图更能说明推广的物理内容。"},
        "figure_refs": [figure("2211.03595", "figure-6-so3-pose.webp", "Figure 6", 14, "show non-Euclidean generative density", "SO(3) 姿态分布的真值与模型比较。", "模型在旋转群上捕捉对称性诱导的多个姿态模态。", "The multimodality is geometric, not merely pixel-space uncertainty.")],
        "equation_refs": [{"label": "Generalized implicit score matching", "latex": r"\mathcal I_{\mathrm{ISM}}(\beta)=\int_0^T\mathbb E_{q_t(x_t)}\!\left[\frac{\widehat L^{*}\beta(x_t,t)}{\beta(x_t,t)}+\widehat L\log\beta(x_t,t)\right]dt", "role": "train a reverse Markov process without Euclidean scores", "symbols": {"beta": "positive model function", "L_hat": "space-time noising generator", "q_t": "noised data law"}, "evidence": "paper.pdf p. 7, Eq. (9)", "interpretation": "Replacing gradients by generator operations extends score matching across state spaces."}],
        "evidence_refs": ["paper.pdf pp. 6–8: likelihood bound and generalized objectives", "paper.pdf pp. 9–16: Euclidean, discrete, manifold and simplex experiments", "source PDF SHA-256 d1f2aff73c5a5d61c4b503b47f3610e02bdad5ef84c04fd2096029f24ab0b643", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2301.03728", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2301.03728",
        "title_en": "Scaling Laws for Generative Mixed-Modal Language Models", "title_zh": "生成式混合模态语言模型的缩放律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("a051e0c2f0e4205d", "Scaling Laws"),
        "verified_metadata": meta("2301.03728", "v1", "Scaling Laws for Generative Mixed-Modal Language Models", ["Armen Aghajanyan", "Lili Yu", "Alexis Conneau", "Wei-Ning Hsu", "Karen Hambardzumyan", "Susan Zhang", "Stephen Roller", "Naman Goyal", "Omer Levy", "Luke Zettlemoyer"], ["cs.CL", "cs.AI", "cs.LG"], "cs.CL", "2023-01-10T00:20:06Z", "More than 250 experiments produce pairwise mixed-modal scaling laws with a model- and data-dependent competition barrier."),
        "sections": [
            sec("作者信息", "作者：Armen Aghajanyan 等十人；arXiv:2301.03728v1。全文 20 页。"),
            sec("研究问题", "单模态 loss 常遵循参数量与数据量的幂律，但联合训练两种 tokenized modalities 会竞争容量，也可能共享结构。论文问：这种 synergy/competition 能否写成可外推的状态方程，并指导跨模态模型的 compute allocation？"),
            sec("背景", "单模态缩放律把不可约 loss、有限参数修正和有限数据修正相加。混合模态还需要 interaction term；其符号决定联合训练相对两个独立模型的收益。", "这里的 competition barrier 类似相边界：在 \((N,D_i,D_j)\) 空间中，interaction correction 变号，分隔协同与竞争区域。"),
            sec("模型与方法", "作者在七种模态、8M–30B 参数、5–100B tokens 上做超过 250 次训练。pairwise law 以两个单模态 loss 的平均为基线，再加入常数 synergy 与随参数量、总数据量衰减的竞争项。", "全部实验在 768 张 80GB A100 的集群上于两个月内完成，多数 run 使用 64 GPU；训练含 restart policy，因此拟合反映的是整套训练协议。"),
            sec("核心结果与证据", "Figure 4 的四张曲面显示不同模态对在模型/数据尺度上的 loss 地形；虚线 competition barrier 标出联合建模由有害转为有益的位置。", "由拟合得到 Speech|Text 的 compute-optimal 配置约为 \(N=28.35\)B、\(D=45.12\)B tokens。作者随后训练 30B 参数、50B tokens 模型，观测到跨过 barrier 后混合模型优于相应单模态模型。", "训练还呈现近似 coordinate-ascent 的模态轮流平台；interaction exponent 与 loss surface 平坦度、gradient spikes 及 optimal batch 存在经验相关。"),
            sec("有效性与局限", "公式只建模两两 interaction；三模态以上可能有不可约高阶耦合，不能由 pairwise 项唯一恢复。", "不同模态的 token 与 cross-entropy 单位依赖 tokenizer 和 vocabulary，loss 数值并非自然可比的物理量。最大规模验证只有一个 30B 点，且 restart policy、学习率和 batch 都可能改变表观缩放。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2301.03728；训练框架：https://github.com/facebookresearch/metaseq 与 https://github.com/facebookresearch/fairscale。", "全文 20 页，PDF SHA-256：715b04f5fe6c4ea1a9bb5fb313b2a580ff7e3fe52a07c375cd7a48951f161163。复现需保留 tokenizer、数据混合、restart 记录、GPU 数、batch 与每个拟合点的置信区间。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读单模态 law，再推 Eq. (4) 的 interaction term；随后用 Figure 4 理解 barrier 的几何。最后检查 30B 验证点与训练协议，避免把经验拟合外推成普适定律。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2301.03728/figure-4-competition-barrier.webp", "label": "Figure 4", "visual_type": "data_plot", "evidence": "paper.pdf p. 8, Figure 4", "alt_text": "四组混合模态 loss 曲面与虚线 competition barrier。", "caption": "模型与数据规模共同决定跨模态 interaction 的符号；虚线是协同和竞争之间的拟合边界。", "selection_rationale": "这是论文最重要的概念图，将缩放律从一维幂律提升为带相边界的多变量曲面。"},
        "figure_refs": [figure("2301.03728", "figure-4-competition-barrier.webp", "Figure 4", 8, "visualize the competition boundary", "混合模态缩放曲面及竞争边界。", "跨过虚线后，常数 synergy 超过有限尺度竞争修正。", "The barrier is an empirical fitted surface, not a universal phase transition.")],
        "equation_refs": [{"label": "Mixed-modal scaling law", "latex": r"L(N,D_i,D_j)=\frac{L(N,D_i)+L(N,D_j)}{2}-C_{ij}+\frac{A_{ij}}{N^{\alpha_{ij}}}+\frac{B_{ij}}{(|D_i|+|D_j|)^{\beta_{ij}}}", "role": "separate asymptotic synergy from finite-scale competition", "symbols": {"N": "parameter count", "D_i": "tokens from modality i", "C_ij": "asymptotic synergy", "alpha_ij": "model-size interaction exponent"}, "evidence": "paper.pdf p. 7, Eq. (4)", "interpretation": "The competition barrier occurs when the positive finite-scale terms equal the constant synergy."}],
        "evidence_refs": ["paper.pdf pp. 5–8: training protocol and mixed-modal law", "paper.pdf pp. 8–12: barrier, empirical phenomena and 30B test", "source PDF SHA-256 715b04f5fe6c4ea1a9bb5fb313b2a580ff7e3fe52a07c375cd7a48951f161163", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2302.01170", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2302.01170",
        "title_en": "Timewarp: Transferable Acceleration of Molecular Dynamics by Learning Time-Coarsened Dynamics", "title_zh": "Timewarp：学习时间粗粒化动力学以实现可迁移的分子动力学加速",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("0a9cdf115b6fa0ad", "Flow Matching"),
        "verified_metadata": meta("2302.01170", "v2", "Timewarp: Transferable Acceleration of Molecular Dynamics by Learning Time-Coarsened Dynamics", ["Leon Klein", "Andrew Y. K. Foong", "Tor Erlend Fjelde", "Bruno Mlodozeniec", "Marc Brockschmidt", "Sebastian Nowozin", "Frank Noé", "Ryota Tomioka"], ["stat.ML", "cond-mat.stat-mech", "cs.LG", "physics.chem-ph"], "stat.ML", "2023-02-02T15:48:39Z", "A transferable conditional normalizing flow proposes long molecular transitions, with Metropolis-Hastings correction targeting the Boltzmann distribution."),
        "sections": [
            sec("作者信息", "作者：Leon Klein、Andrew Y. K. Foong、Tor Erlend Fjelde、Bruno Mlodozeniec、Marc Brockschmidt、Sebastian Nowozin、Frank Noé、Ryota Tomioka；arXiv:2302.01170v2。全文 22 页。"),
            sec("研究问题", "全原子 MD 以飞秒步长积分，但构象跃迁常在微秒至毫秒发生，且每个新分子都要重新模拟。论文问：能否离线学习 \(10^5\!\text{--}\!10^6\,\mathrm{fs}\) 的粗时间转移核，并迁移到未见过的小肽，同时保持 Boltzmann 平衡分布？"),
            sec("背景", "只学习长步 proposal 会产生模型偏差。Timewarp 把它嵌入 Metropolis–Hastings 链：proposal 决定跨越势垒的效率，能量与反向 proposal density 的比值负责详细平衡。", "因此“动力学加速”在本文主要指 equilibrium sampling 的有效样本率，不等于复现真实的时间相关动力学。"),
            sec("模型与方法", "条件 normalizing flow 学习 \(p_\theta(x(t+\tau)\mid x(t))\)。permutation-equivariant transformer/RealNVP 同时支持快速采样与精确 likelihood；positions 和 auxiliary velocities 构成增广状态。", "每个 proposal 用 MH acceptance ratio 修正。作者也给出不做 MH 的快速探索模式，但明确承认它有偏。"),
            sec("核心结果与证据", "Figure 1 对同一未见 HT 二肽比较 30 分钟 MD 与 Timewarp：在 TICA 平面上，Timewarp 更快访问分离的 metastable basins，报告约 33 倍 ESS/s。", "对 100 个测试二肽，中位 ESS/s speedup 约 5；QW 与 HT 分别约 5 和 33。proposal acceptance 约 0.03%–2%，说明大跨步能在低接受率下仍有净收益。", "4AA 结果更混合：只有约三分之一在带 MH 时超过 MD，一些链不能覆盖全部构象，接受率可低于 0.01%。"),
            sec("有效性与局限", "迁移只验证到 2–4 个氨基酸的小肽，不能外推到蛋白折叠或配体结合。低 acceptance 会让有限时间链停滞；多 proposal batching 改善吞吐但不改变混合时间的根本困难。", "MH 模式渐近无偏，但仍需足够长链与正确能量；去掉 MH 的 exploration mode 不再采样精确 Boltzmann 分布。ESS/s 加速也不意味着物理时间轨迹正确。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2302.01170；代码：https://github.com/microsoft/timewarp。", "全文 22 页，PDF SHA-256：e16b5d7bdda21c3260e7281933ddee64350a33deb1af8a7425b5d9fdf4d22331。复现需固定 force field、温度、\(\tau\)、训练肽划分、MH batching 和 ESS estimator，并报告每条链的 acceptance 与 basin coverage。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1，把 wall-clock exploration 与真实动力学区分开；再读 Eqs. (5)–(6) 检查 detailed balance。最后看二肽总体分布和 4AA failure cases，不能只引用 33 倍最佳案例。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2302.01170/figure-1-timewarp-overview.webp", "label": "Figure 1", "visual_type": "trajectory", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "肽构象转移示意及 MD 与 Timewarp 在 TICA 空间中的轨迹。", "caption": "学习到的长步 proposal 跨越 metastable basins；MH 校正负责把高效探索重新约束到 Boltzmann 平衡分布。", "selection_rationale": "该图同时展示分子构象、粗时间步和相空间探索，是方法与物理目标的最完整可视化。"},
        "figure_refs": [figure("2302.01170", "figure-1-timewarp-overview.webp", "Figure 1", 2, "compare metastable exploration", "分子跃迁以及 MD 与 Timewarp 的 TICA 轨迹。", "长步 flow proposal 在相同 wall-clock 下访问更多 metastable regions。", "Faster equilibrium exploration does not establish correct dynamical kinetics.")],
        "equation_refs": [{"label": "Metropolis-Hastings correction", "latex": r"\alpha(X,\widetilde X)=\min\!\left\{1,\frac{\mu_{\mathrm{aug}}(\widetilde X)\,p_\theta(X\mid\widetilde X^{p})}{\mu_{\mathrm{aug}}(X)\,p_\theta(\widetilde X\mid X^{p})}\right\}", "role": "enforce detailed balance for learned long-step proposals", "symbols": {"mu_aug": "Boltzmann target with auxiliary velocities", "p_theta": "conditional flow proposal", "X_p": "positions in the augmented state"}, "evidence": "paper.pdf p. 5, Eq. (6)", "interpretation": "Exact proposal likelihoods allow the learned dynamics to be bias-corrected asymptotically."}],
        "evidence_refs": ["paper.pdf pp. 3–6: Boltzmann target, flow proposal and MH correction", "paper.pdf pp. 8–11: peptide transfer, ESS/s and failure cases", "source PDF SHA-256 e16b5d7bdda21c3260e7281933ddee64350a33deb1af8a7425b5d9fdf4d22331", "Evidence status: full-text verified; no independent reproduction performed."],
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
