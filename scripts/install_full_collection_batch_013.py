#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 013."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_ids: list[str], topics: list[str]) -> dict[str, object]:
    return {
        "program": "Collection", "catalog": "Paper Collection",
        "catalog_record_id": record_ids[0], "catalog_record_ids": record_ids,
        "catalog_topic": topics[0], "collection_date": "2026-08-23",
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


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2405.20320", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2405.20320",
        "title_en": "Improving the Training of Rectified Flows",
        "title_zh": "改进整流流训练：一次 Reflow 已足够接近直线",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["4ff2d8a087e1ef50"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2405.20320", "v2", "Improving the Training of Rectified Flows",
            ["Sangyun Lee", "Zinan Lin", "Giulia Fanti"],
            ["cs.CV", "cs.AI", "cs.LG"], "cs.CV", "2024-05-30T17:56:04Z",
            "A geometric argument motivates stopping Reflow after one rewiring round and improving the remaining training with endpoint-focused timesteps and perceptual robust losses.",
        ),
        "sections": [
            sec("作者信息", r"作者：Sangyun Lee、Zinan Lin、Giulia Fanti；arXiv:2405.20320v2。全文 29 页，方法称 2-rectified flow++，在 CIFAR-10、AFHQ、FFHQ 与 ImageNet 64×64 上评估 1–2 NFE 生成。"),
            sec("研究问题", r"Reflow 通过反复用上一轮 flow 产生的 noise–data coupling 重新训练，使 ODE trajectories 变直；但多轮训练昂贵且会累积模型误差。论文问：第一轮 rewiring 后轨迹是否已经近乎无交叉，使第二次以后 Reflow 没有几何收益；若是，低 NFE 质量差是否主要是优化问题？"),
            sec("背景", r"rectified flow 沿 \(x_t=(1-t)x+t z\) 训练 velocity field。第一轮将独立 noise/data coupling 重连成生成器诱导 coupling；若两条插值线要相交，所需 noise 往往离开高维 Gaussian typical annulus 或具有异常 autocorrelation，因此在实际高维数据上交叉稀少。", r"Figure 1 展示从交叉直线到 1-rectified flow 的无交叉轨迹，再把生成配对线性化得到 2-rectified flow；论文的核心判断是步骤 (c) 已几乎直，继续到 (d) 收益有限。"),
            sec("模型与方法", r"作者把 2-rectified flow loss 分成不可约 conditional variance 与可优化误差；由于 induced coupling 近确定性，前者接近零。实测 loss 在 \(t=0,1\) 两端高，于是用 \(p_t(u)\propto e^{4u}+e^{-4u}\) 的 U-shaped timestep density，而不是把权重集中在中间。", r"进一步以 pseudo-Huber 降低 outlier gradient variance，并加入 LPIPS perceptual term；还把预训练 VP/VE diffusion posterior 通过 time/scale conversion 初始化为 Reflow model。CIFAR-10 最后用 50,000 real-data/inverted-noise pairs 微调 5,000 iterations。"),
            sec("核心结果与证据", r"Figure 1 是机制图：第一轮 rewiring 消除 trajectory crossings，第二轮使用生成器配对后线性插值；它解释为何论文把资源投向一次 Reflow 的训练质量，而不是递归增加轮数。", r"Table 1 的 CIFAR-10 1-NFE FID 从 vanilla 2-RF 的 12.21 降到 7.14（EDM init+大 batch）、5.17（U-shaped \(p_t\)）、3.42（LPIPS-Huber），加 real-data fine-tuning 后为 3.07；相对 12.21 下降约 75%。AFHQ 1-NFE 从 12.39 降到 4.11，FFHQ 从 8.84 降到 5.21。", r"在 ImageNet 64×64，1/2 NFE FID 为 4.31/3.64；在 CIFAR-10 为 3.07/2.40。Heun solver 随 NFE 增加仍继续改善，说明“近直”不等于 learned vector field 无离散化或拟合误差。"),
            sec("有效性与局限", r"“一次 Reflow 足够”来自高维 typicality 直觉与经验图，不是对任意分布、低维 manifold 或有限网络的定理；作者自己的 edge cases 允许近邻 data 或 \(t\to1\) 时出现例外。不同 improvement 叠加了 initialization、batch、loss、timestep sampling 和 real-data fine-tuning，最终 FID 不能归因于单一因素。", r"FID 是样本分布的有限统计量，未衡量 mode-wise failure、训练成本或数据泄漏；ImageNet 只到 64×64。real-data fine-tuning 破坏了纯 data-free Reflow 的设定，且部分 FID 因成本只计算一次。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2405.20320；代码：https://github.com/sangyun884/rfpp。全文 29 页，PDF SHA-256：455b0f2e01add04232883d279f5e2c10942394746e6b2f0b26a8f00c787c5341。", r"复现需固定 EDM/DDPM checkpoint、Reflow pairing、\(p_t\) 参数 \(a=4\)、pseudo-Huber constant、LPIPS weighting、batch/iterations、real-data inversion NFE、ODE solver 与 50,000-sample FID protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 与 Section 3 的 trajectory-intersection argument；再读 Eq. (4) 的 loss decomposition，理解为何 2-RF 与 1-RF 的最佳 timestep density 相反。随后逐行看 Table 1 的 cumulative ablation，最后用 Tables 3–4 区分 1-NFE、2-NFE 与多步 solver 表现。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2405.20320/figure-1-rectified-reflow.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "四阶段示意图展示交叉线性 coupling、无交叉 rectified trajectories、重新线性插值和重复 Reflow。", "caption": "第一轮 Reflow 先重连交叉轨迹，再对生成配对做线性插值；论文认为此时已近直，无需继续递归。", "selection_rationale": "Figure 1 是全文核心几何机制图，优先于 FID 表和生成样例。"},
        "figure_refs": [figure("2405.20320", "figure-1-rectified-reflow.webp", "Figure 1", 3, "explain why one Reflow round can suffice", "从交叉 coupling 到无交叉 flow，再到近直 2-rectified flow 的四阶段示意。", "高维 typicality 使第二轮配对的线性轨迹很少相交。", "This is a geometric intuition supported empirically, not a universal proof.")],
        "equation_refs": [
            {"label": "Rectified-flow interpolation", "latex": r"x_t=(1-t)x+t z,\qquad v_\theta(x_t,t)\approx z-x", "role": "define the straight conditional path and learned velocity", "symbols": {"x": "data endpoint", "z": "Gaussian endpoint", "t": "flow time"}, "evidence": "paper.pdf pp. 2–3, Eqs. (1)–(3)", "interpretation": "Reflow changes the endpoint coupling so these straight conditional paths become mutually compatible."},
            {"label": "Endpoint-focused timestep density", "latex": r"p_t(u)=\frac{e^{au}+e^{-au}}{\int_0^1(e^{as}+e^{-as})\,ds},\qquad a=4", "role": "allocate training to the high-loss endpoints of 2-rectified flow", "symbols": {"u": "sampled timestep", "a": "U-shape concentration"}, "evidence": "paper.pdf p. 5, Section 4.1", "interpretation": "Unlike first-round flow training, the difficult tasks after rewiring lie near both endpoints."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: Reflow geometry and timestep loss", "paper.pdf pp. 6–9: cumulative ablations and low-NFE benchmarks", "source PDF SHA-256 455b0f2e01add04232883d279f5e2c10942394746e6b2f0b26a8f00c787c5341", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2406.04843", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2406.04843",
        "title_en": "Variational Flow Matching for Graph Generation",
        "title_zh": "用于图生成的变分流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8ecf7e0a0641b115"], ["Flow Matching"]),
        "verified_metadata": meta("2406.04843", "v2", "Variational Flow Matching for Graph Generation", ["Floor Eijkelboom", "Grigory Bartosh", "Christian Andersson Naesseth", "Max Welling", "Jan-Willem van de Meent"], ["cs.LG", "stat.ML"], "cs.LG", "2024-06-07T11:16:17Z", "Flow matching is recast as variational inference over trajectory endpoints, yielding CatFlow for categorical graph variables."),
        "sections": [
            sec("作者信息", r"作者：Floor Eijkelboom、Grigory Bartosh、Christian Andersson Naesseth、Max Welling、Jan-Willem van de Meent；arXiv:2406.04843v2。全文 31 页，提出 VFM 与 categorical special case CatFlow。"),
            sec("研究问题", r"标准 flow matching 直接回归 marginal velocity，却隐藏了穿过当前点 \(x\) 的所有可能终点 \(x_1\)。论文问：能否显式学习 posterior endpoint distribution \(p_t(x_1\mid x)\)，并在 conditional velocity 对 \(x_1\) 线性时，用低维 mean-field marginals 精确恢复同一 velocity，从而自然处理 categorical graph nodes/edges？"),
            sec("背景", r"marginal field 是 conditional fields 对 endpoint posterior 的平均：\(u_t(x)=\mathbb E_{p_t(x_1|x)}u_t(x|x_1)\)。VFM 用 \(q_t^\theta(x_1|x)\) 近似这一 posterior，并把训练写成 KL/cross-entropy。若 field 对 endpoint 线性，速度只依赖一阶矩，因此不需要学习 endpoint components 的全部相关结构。", r"图被表示为 fully connected categorical variables：每个 node 取 \(K_v\) 类，每条 edge 取 \(K_e+1\) 类（额外一类表示 absent）。这不是带三维坐标的 geometric graph generation。"),
            sec("模型与方法", r"CatFlow 对每个 component 输出 categorical probabilities \(\mu_t^d(x)\)，再定义 \(v_t^{\theta,d}(x)=(\mu_t^d(x)-x^d)/(1-t)\)。Figure 1 显示当前位置、预测的 simplex point 与速度方向；这种参数化保证 \(t\to1\) 时 trajectory 指向 simplex corner。", r"训练目标退化为逐 component cross-entropy，而生成仍是连续 ODE integration，不是逐类别 CTMC sampling。graph network 保持 permutation equivariance；Theorem 2 说明在相应条件下生成分布对 vertex relabeling exchangeable。"),
            sec("核心结果与证据", r"Figure 1 说明 CatFlow 的关键 inductive bias：网络不直接回归任意 vector，而先预测 simplex 上的 endpoint distribution，再沿其 mean 方向流动；这排除了指向不可能 categorical endpoint 的 misaligned paths。", r"abstract graphs 上，CatFlow 在 Ego-small 的 degree/clustering/orbit MMD 为 0.013/0.024/0.008，在 Community-small 为 0.018/0.086/0.007，达到或匹配表中最佳。", r"10,000 个 molecule samples 上，QM9 validity/uniqueness/FCD 为 99.81%/99.95%/0.441；ZINC250k 为 99.21%/100.00%/13.211。相对普通 flow matching，CatFlow 在小模型和 5%–20% data ablation 下退化更慢，并报告更快 convergence。"),
            sec("有效性与局限", r"mean-field 的“无损”只针对 conditional velocity 对 endpoint 线性的情形；它保证相同 first-moment field，不保证学到真实 endpoint joint correlations。CatFlow 在 simplex embedding 中积分连续 ODE，因此与严格离散 CTMC、chemical reaction dynamics 或物理分子轨迹不同。", r"实验仅含 categorical graphs；fully connected edge representation 的计算/内存随 nodes 二次增长，论文明确指出不适合大图。QM9 novelty 不适合作为主指标，ZINC 的接近 100% novelty 也不能证明 drug usefulness；validity/FCD 对 preprocessing 和 valency protocol 敏感。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2406.04843。全文 31 页，PDF SHA-256：ef9aada33f5376f38333b63f76a27fbea86cae2f6baca59e2f1cd55f0b298b83。", r"复现需固定 graph categorical encoding、permutation-equivariant network、interpolant、ODE solver/tolerances、RDKit kekulization、hydrogen removal、10,000-sample protocol、validity rule、FCD model 与 MMD kernels。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Eqs. (6)–(12)，抓住 endpoint posterior 与 first-moment sufficiency；再看 Figure 1 和 Eqs. (15)–(20)，区分“预测类别分布”与“连续积分”。最后检查 Tables 1–2 和 Figure 3，并把 graph topology、molecular validity 与 large-graph scalability 分开判断。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2406.04843/figure-1-catflow-simplex.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 5, Figure 1", "alt_text": "当前位置、categorical endpoint distribution 的 simplex 表示以及指向其均值的 CatFlow velocity。", "caption": r"CatFlow 先预测 simplex 上的 endpoint probabilities \(\mu_t(x)\)，再令 velocity 指向该点，保证终态收敛到 categorical simplex。", "selection_rationale": "Figure 1 是全文最重要的参数化示意图，直接取代对 variational mean-field construction 的冗长叙述。"},
        "figure_refs": [figure("2406.04843", "figure-1-catflow-simplex.webp", "Figure 1", 5, "show how endpoint probabilities parameterize the vector field", "三个 simplex panel 展示 interpolant、预测 mean endpoint 与 CatFlow velocity。", "线性 conditional field 只需要 endpoint posterior 的一阶矩。", "The continuous trajectory in the simplex is a generative construction, not physical graph dynamics.")],
        "equation_refs": [
            {"label": "Variational flow matching", "latex": r"\mathcal L_{\mathrm{VFM}}(\theta)=-\mathbb E_{t,x,x_1}\log q_t^\theta(x_1\mid x)", "role": "fit the posterior distribution over trajectory endpoints", "symbols": {"q": "variational endpoint posterior", "x": "current interpolated state", "x1": "data endpoint"}, "evidence": "paper.pdf p. 3, Eqs. (9)–(10)", "interpretation": "Minimizing this cross-entropy is equivalent to minimizing the endpoint-posterior KL up to a constant."},
            {"label": "CatFlow vector field", "latex": r"v_t^\theta(x)=\frac{\mu_t(x)-x}{1-t},\qquad \mu_t(x)=\mathbb E_{q_t^\theta(x_1|x)}[x_1]", "role": "turn categorical endpoint probabilities into a continuous flow", "symbols": {"mu_t": "mean point in the probability simplex", "t": "flow time"}, "evidence": "paper.pdf p. 5, Eqs. (15)–(20)", "interpretation": "The field points toward a valid simplex endpoint rather than an unconstrained regression target."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–6: VFM, mean-field theorem and CatFlow", "paper.pdf pp. 8–10: graph and molecule experiments", "source PDF SHA-256 ef9aada33f5376f38333b63f76a27fbea86cae2f6baca59e2f1cd55f0b298b83", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2407.15595", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2407.15595",
        "title_en": "Discrete Flow Matching", "title_zh": "离散流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["a22a128c6c4c47c2"], ["Flow Matching"]),
        "verified_metadata": meta("2407.15595", "v2", "Discrete Flow Matching", ["Itai Gat", "Tal Remez", "Neta Shaul", "Felix Kreuk", "Ricky T. Q. Chen", "Gabriel Synnaeve", "Yossi Adi", "Yaron Lipman"], ["cs.LG", "cs.AI"], "cs.LG", "2024-07-22T12:33:27Z", "A general probability-path and probability-velocity formulation extends flow matching to high-dimensional discrete data."),
        "sections": [
            sec("作者信息", r"作者：Itai Gat、Tal Remez、Neta Shaul、Felix Kreuk、Ricky T. Q. Chen、Gabriel Synnaeve、Yossi Adi、Yaron Lipman；arXiv:2407.15595v2。全文 39 页，最大模型 1.7B parameters。"),
            sec("研究问题", r"连续 flow matching 用 continuity equation 与 vector field 输运 density；语言和 code 却位于 \(D=[d]^N\) 的有限状态空间。论文问：能否用 CTMC probability flux 定义离散 continuity equation，并从可采样 conditional paths 与 learned denoiser/noise posterior 构造 exact marginal probability velocity？"),
            sec("背景", r"每个 token 独立按 \(\delta_{X_t^i}+h u_t^i(\cdot,X_t)\) 在小时间 \(h\) 内跳变。合法 probability velocity 满足各列和为零且 off-diagonal rates 非负；这正是连续 divergence-free bookkeeping 的离散版本。", r"Figure 2 把 \(\mathbb R^N\) 的流线、离散格点上的 probability transfers，以及两种 divergence 并排：连续 divergence 是微分通量，离散 divergence 是所有邻接 state 的 incoming minus outgoing flux。"),
            sec("模型与方法", r"作者用 scheduler \(\kappa_t\) 在 source 与 target categorical distributions 之间构造 general probability paths。Theorem 2 证明 conditional velocities 对 posterior \(p_t(x_0,x_1|z)\) 边缘化后生成 marginal path；Theorem 3 给出 closed-form rates。", r"对 mask path，denoiser parameterization 为 \(u_t^i(x_i,z)=\dot\kappa_t[p_{1|t}(x_i|z)-\delta_{z^i}(x_i)]/(1-\kappa_t)\)。网络用 cross-entropy 学 posterior；sampling 可加入 corrector 与 adaptive safe step，且能做非自回归 infilling。"),
            sec("核心结果与证据", r"Figure 2 是理论核心：连续空间的 local derivative 被有限状态图上的 flux sum 替代，因而“flow”描述的是概率质量随时间移动，不是 token 在欧氏空间中连续运动。", r"1.7B text model 的 unconditional generative perplexity（Llama-3 8B evaluator）为 9.7；论文对照 1.7B autoregressive baseline 22.3 与 Llama-2 7B 的 8.3。该指标由外部模型打分，不等同于 held-out likelihood。", r"code 上 HumanEval Pass@1/Pass@10 为 6.7%/13.4%，1-shot MBPP 为 6.7%/20.6%。CIFAR-10 达到 FID 3.63 at 1024 NFE；高 NFE 暴露离散 Euler sampling 的计算代价。"),
            sec("有效性与局限", r"marginal path correctness 是 \(h\to0\) 的一阶 statement；有限 step、posterior approximation、scheduler 与 floating-point precision 都会引入偏差。token-wise simultaneous jumps 是生成算法，不应解释为真实语言动力学。", r"generative perplexity 依赖 evaluator、entropy 与 repetition filtering，和 autoregressive likelihood 不完全可比。code pass rates 仍低，image FID 需要 1024 NFE；1.7B scaling 结论不能推出更大模型仍保持同样优势。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2407.15595。全文 39 页，PDF SHA-256：5ff582a1ccb3e6584b23450a8f4ff05b3829d4fa29a9d240e5d31d15b0e140bd。", r"复现需固定 coupling、mask/noise source、\(\kappa_t\)、posterior parameterization、safe step、corrector temperature、NFE、precision、tokenizer、evaluator checkpoint 与 HumanEval/MBPP execution harness。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2 与 Eqs. (12)–(20)，逐项对照连续/离散 divergence；再读 Theorems 2–3 和 Table 1，确认 denoiser/noise-prediction 公式为何同形。最后看 Tables 2–4，并同时记录 evaluator dependence、NFE 与 code execution rate。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2407.15595/figure-2-discrete-continuous-flow.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "连续二维流、离散二维状态跳转及两种 divergence operator 的并排示意图。", "caption": "离散流用 state-to-state probability flux 的收支替代连续空间的微分 divergence。", "selection_rationale": "Figure 2 是全文最关键的数学概念图，优先于代码样例和 FID 曲线。"},
        "figure_refs": [figure("2407.15595", "figure-2-discrete-continuous-flow.webp", "Figure 2", 4, "map continuous flow matching concepts to a finite state space", "连续流线、离散格点跳转以及两个 divergence 示意。", "概率速度是离散状态之间的通量生成元，而非欧氏位移。", "The analogy is exact at the continuity-equation level, not a claim that discrete tokens possess physical trajectories.")],
        "equation_refs": [
            {"label": "Discrete Euler jump", "latex": r"X_{t+h}^i\sim\delta_{X_t^i}(\cdot)+h\,u_t^i(\cdot,X_t),\qquad \sum_{x_i}u_t^i(x_i,z)=0", "role": "define an infinitesimal categorical transition", "symbols": {"u_t": "probability velocity", "h": "time step", "i": "token index"}, "evidence": "paper.pdf p. 4, Eqs. (12)–(13)", "interpretation": "Off-diagonal nonnegative rates and zero total mass make the update a valid PMF for small h."},
            {"label": "Discrete denoiser velocity", "latex": r"u_t^i(x_i,z)=\frac{\dot\kappa_t}{1-\kappa_t}\left[p_{1|t}(x_i\mid z)-\delta_{z^i}(x_i)\right]", "role": "construct marginal flux from a learned clean-token posterior", "symbols": {"kappa_t": "path scheduler", "p_1|t": "probability denoiser", "z": "current sequence"}, "evidence": "paper.pdf p. 6, Eq. (24)", "interpretation": "The formula has the same algebraic form as continuous x-prediction while acting on categorical fluxes."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: probability velocity and discrete continuity equation", "paper.pdf pp. 8–10: language, code and image experiments", "source PDF SHA-256 5ff582a1ccb3e6584b23450a8f4ff05b3829d4fa29a9d240e5d31d15b0e140bd", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2407.19716", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2407.19716",
        "title_en": "Activity Waves in Condensed Phases of Quincke Rollers",
        "title_zh": "Quincke 滚子凝聚相中的活性波",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "experiment", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["d3400a0e66398ffc"], ["Active Matter"]),
        "verified_metadata": meta("2407.19716", "v1", "Activity Waves in Condensed Phases of Quincke Rollers", ["Meng Fei Zhang", "Bao Ying Fan", "Zeng Tao Liu", "Tian Hui Zhang"], ["cond-mat.soft"], "cond-mat.soft", "2024-07-29T05:40:34Z", "Periodically driven Quincke rollers form active liquids and crystals supporting distinct sound-like and shock-like activity waves."),
        "sections": [
            sec("作者信息", r"作者：Meng Fei Zhang、Bao Ying Fan、Zeng Tao Liu、Tian Hui Zhang；arXiv:2407.19716v1。全文 12 页，是周期方波电场驱动 Quincke rollers 的显微实验。"),
            sec("研究问题", r"同一类 active colloids 在液态和晶态凝聚相中能否成为 excitable medium？更具体地，周期激活的 dense bands 在两相中是否共享同一传播机制，还是 liquid 的局部排斥与 crystal 的 collective memory 会产生 sound-like 与 shock-like 两类波？"),
            sec("背景", r"Quincke rotation 在电场超过阈值 \(E_c\) 后把 dielectric spheres 转化为自推进 rollers。方波电场同步开启/关闭 propulsion 与 dipolar repulsion；改变峰值 \(E_p\) 和频率 \(f\) 可在 stripes、active liquid、active crystal、non-excitable crystal 与 flocking 之间切换。", r"液体允许粒子重排，晶体则 cage particles。相同 dense band 因此可能靠“粒子穿过波”或“粒子随波长程移动”两种完全不同的微观机制传播。"),
            sec("模型与方法", r"实验从显微视频做 particle tracking 与 PIV，测 local area fraction、velocity magnitude/direction、density peak position、band width 和 collision outcome。active liquid 的 band rear 出现低密度带并在每周期分裂；active crystal 的 density front 尖锐，band 内 velocities 高度对齐。", r"作者通过关场半小时擦除 crystal band 的 charge/propulsion memory，再重新加场：第一周期 band 因 repulsion 分裂，随后重新建立两条反向传播的 shock waves，用作 memory mechanism 的干预性检验。"),
            sec("核心结果与证据", r"Figure 2 用原始显微图与 PIV velocity fields 展示波的萌生：active liquid 和 active crystal 都形成传播 dense bands，但晶体的前沿更尖、速度场更集体对齐。图像直接把相态、密度结构和流场对应起来。", r"active-liquid sound wave 宽度约 300 µm，density peak 的传播速度高于 band 内单粒子最大速度；粒子前后反向运动导致 band splitting，两个 wave collision 后看似互相穿过。", r"active-crystal shock wave 的示例宽度约 450 µm，粒子可随 band 定向运动几十周期；collision 时 waves annihilate 或合并后改向。memory-erasure experiment 支持 density-dependent charge relaxation/collective propulsion memory，而不是单纯静态密度梯度。"),
            sec("有效性与局限", r"“sound”与“shock”是基于传播、碰撞和 front morphology 的现象学命名；论文没有给出守恒流体方程、声速色散或 Rankine–Hugoniot shock relation，因此不能等同于被动介质中的线性声波或热力学冲击波。", r"机制判断来自特定 particle size、cell、电场 waveform、area fraction 与 PIV/tracking protocol。charge memory 没有被直接逐粒子测量；关场实验支持但不能唯一排除结构松弛、hydrodynamic coupling 等替代机制。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2407.19716。全文 12 页，PDF SHA-256：f58b66ec38eaa7364bb3060a118ab286edcb619cc8bfc890b102aba7c1dc621c。", r"复现需保存 sphere/cell geometry、fluid conductivity/viscosity、\(E_c,E_p,f\)、duty cycle、global area fraction、camera rate、tracking/PIV parameters、density threshold、peak-fitting rule、关场时长与原始 collision movies。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2 建立装置、相态和 velocity-field 图像；再把 Figures 3–4 的 density/velocity profiles 并排读，区分 liquid splitting 与 crystal collective transport。最后看 Figure 5 的 collision 和 Figure 6 的 phase diagram，并保留“类声/类冲击”的现象学边界。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2407.19716/figure-2-wave-emergence.webp", "label": "Figure 2", "visual_type": "micrograph", "evidence": "paper.pdf p. 3, Figure 2", "alt_text": "active liquid 与 active crystal 中 dense activity waves 的显微快照和对应 PIV velocity fields。", "caption": "同一周期驱动在液态与晶态凝聚相中激发形态和速度场不同的传播 band。", "selection_rationale": "Figure 2 是全文最重要且最具可视性的原始实验图，优先于 phase diagram 和一维 profile。"},
        "figure_refs": [figure("2407.19716", "figure-2-wave-emergence.webp", "Figure 2", 3, "visualize the emergence and flow field of waves in both condensed phases", "四张显微快照与四张 PIV 速度场。", "液体 band 的分裂式传播与晶体 band 的集体定向传播在图中直接可辨。", "The image establishes morphology and velocity organization, not a hydrodynamic dispersion relation.")],
        "equation_refs": [
            {"label": "Local area fraction", "latex": r"\phi_A(x,t)=\frac{N_A(x,t)\,\pi a^2}{A}", "role": "quantify the density profile across a propagating band", "symbols": {"N_A": "particles in a spatial bin", "a": "particle radius", "A": "bin area"}, "evidence": "paper.pdf pp. 3–4, Figures 3–4 density profiles", "interpretation": "Tracking the peak of this coarse-grained density distinguishes wave motion from individual-particle motion."},
            {"label": "Measured wave speed", "latex": r"c_{\rm wave}=\frac{\Delta x_{\rm peak}}{\Delta t}", "role": "separate density-band propagation from particle speed", "symbols": {"x_peak": "position of the density maximum", "Delta t": "time across drive cycles"}, "evidence": "paper.pdf pp. 3–4, Figures 3–4", "interpretation": "In the active liquid, the density peak can propagate faster than any individual roller because particles relay the band by splitting."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: wave emergence, profiles, collisions and memory test", "paper.pdf p. 6: drive-dependent phase diagram", "source PDF SHA-256 f58b66ec38eaa7364bb3060a118ab286edcb619cc8bfc890b102aba7c1dc621c", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2408.03314", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2408.03314",
        "title_en": "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters",
        "title_zh": "按题目自适应扩展测试时计算可优于扩展模型参数",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["d15073157caacd9d", "f094d310059a6320"], ["Scaling Laws", "Scaling Laws"]),
        "verified_metadata": meta("2408.03314", "v1", "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters", ["Charlie Snell", "Jaehoon Lee", "Kelvin Xu", "Aviral Kumar"], ["cs.LG", "cs.CL"], "cs.LG", "2024-08-06T17:35:05Z", "Prompt-difficulty-conditioned allocation of revisions and verifier-guided search improves the efficiency of test-time compute on MATH."),
        "sections": [
            sec("作者信息", r"作者：Charlie Snell、Jaehoon Lee、Kelvin Xu、Aviral Kumar；arXiv:2408.03314v1。全文 38 页，使用 PaLM 2-S*、MATH 500-test split、process reward model（PRM）与 revision model。该论文在 Collection 中有两个 catalog records，共用同一卡片。"),
            sec("研究问题", r"固定 inference budget 不应对每道题用同一策略：easy questions 可能只需 best-of-\(N\)，中等题可受益于 sequential revision 或 verifier search，超出 base model 能力的 hardest questions 则可能怎么搜都无效。论文问：能否以 model-relative difficulty 为近似 sufficient statistic，为每题选择 compute allocation，使 test-time scaling 比统一 best-of-\(N\) 更高效？"),
            sec("背景", r"研究分两类机制：改变 proposal distribution 的 sequential self-revision，以及保持 proposal model、用 PRM 在 best-of-\(N\)、beam search、lookahead search 中选择。难度按 base model 从 2048 samples 估计的 pass@1 分成五个 quantiles；部署近似则用 verifier predicted score 代替 ground truth。", r"compute-optimal policy 不是新网络，而是在给定 budget \(N\) 和 difficulty bin 下，经 two-fold cross-validation 选择表现最好的 test-time hyperparameters/strategy。"),
            sec("模型与方法", r"revision model 逐次读取先前答案并生成修订；PRM 为每个 reasoning step 打分。作者比较 parallel samples、sequential revisions 及其混合比例，并比较 best-of-\(N\)、beam 与 lookahead search。", r"FLOPs exchange 用 pretraining \(X\approx6P D_{\rm pre}\)、inference \(Y\approx2P D_{\rm inf}\) 估算。把参数放大 \(M\) 倍与给小模型增加 inference tokens 做总 FLOPs matching，并显式考察 \(R=D_{\rm inf}/D_{\rm pre}\) 的不同负载。"),
            sec("核心结果与证据", r"Figure 1 汇总主结果：按 difficulty 自适应选择 revision/search policy 后，曲线相对 uniform/parallel baselines 上移；revision 设置可用约 4× 更少 test-time compute 超过 best-of-\(N\)，PRM search 在低/中 budget 也接近相同量级的节省。", r"顺序修订的 pass@1 随 revision steps 持续提高，甚至超过训练时的 4 steps；但高 budget 下纯 sequential 并非总是最优，parallel–sequential 存在随难度与 budget 变化的最佳比例。beam search 低 budget 较好，随后收益饱和，lookahead 的额外展开并未在等 compute 下获益。", r"与约 14× 参数模型做 FLOPs matching 时，小模型+test-time compute 只在 easy/intermediate bins 或低 inference load \(R\ll1\) 下常占优；hardest bins 与 \(R\gg1\) 时，更多 pretraining 更有效。标题结论因此是条件性的，不是统一替代参数 scaling。"),
            sec("有效性与局限", r"oracle difficulty 用 2048 samples 和 ground-truth correctness，部署不可直接获得；model-predicted difficulty 仍需额外 inference，论文没有把这一探索成本完整计入主预算。策略又在相同 500-test-question pool 上 two-fold 选择，bin 内样本量有限。", r"实验只覆盖 MATH、PaLM 2-S*、特定 PRM/revision checkpoints；FLOPs 采用 \(6PD\)/\(2PD\) 近似，忽略 memory、latency、parallel hardware 和 serving reuse。对 base model 几乎从不答对的题，test-time compute 增益很小，因此不能把“14×”理解为普遍模型替代率。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2408.03314。全文 38 页，PDF SHA-256：ded7b20b51493258c5ce2a1a024cd33dd752de1fa3373d1207620da4cfe24545。", r"复现需固定 PaLM 2-S*/PRM/revision checkpoints、MATH split、2048-sample difficulty estimation、five-bin boundaries、two-fold policy selection、generation token accounting、search branching、verifier aggregation 与 \(R\) scenarios。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，但把左侧 2–4× efficiency 与右侧 14× FLOPs-matched 条件分开。再读 Eq. (1) 的 per-prompt optimal policy 和 difficulty construction；随后比较 Figures 3、6–8 的 search/revision regimes，最后读 Figure 9，确认 pretraining 与 inference compute 不是一比一可交换。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2408.03314/figure-1-compute-optimal-scaling.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "compute-optimal revisions/search 的 scaling curves 与相对 14 倍大模型的 FLOPs-matched 条形图。", "caption": "自适应策略的收益强烈依赖题目难度、budget 和 inference/pretraining load；简单题更能用 test-time compute 换取性能。", "selection_rationale": "Figure 1 是作者的主结果总览；文章没有能同时表达 4× efficiency 与 14× 条件比较的机制示意图。"},
        "figure_refs": [figure("2408.03314", "figure-1-compute-optimal-scaling.webp", "Figure 1", 2, "summarize difficulty-conditioned test-time scaling and FLOPs-matched comparison", "上下两组 scaling curves 与按难度分箱的 pretraining comparison bars。", "compute-optimal gains集中在 base model 已有非平凡成功率的 prompts。", "The result is conditional on MATH, the studied models, difficulty estimator, and serving-load ratio.")],
        "equation_refs": [
            {"label": "Per-prompt compute-optimal policy", "latex": r"\theta_q^*(N)=\arg\max_\theta\;\mathbb E_{y\sim\mathrm{Target}(\theta,N,q)}\!\left[\mathbf 1\{y=y^*(q)\}\right]", "role": "define optimal allocation for a prompt and compute budget", "symbols": {"theta": "test-time strategy hyperparameters", "N": "generation budget", "q": "prompt"}, "evidence": "paper.pdf p. 5, Eq. (1)", "interpretation": "The practical method approximates this inaccessible oracle policy using discrete difficulty bins."},
            {"label": "Pretraining–inference FLOPs model", "latex": r"X\simeq6P D_{\rm pre},\qquad Y\simeq2P D_{\rm inf},\qquad R=\frac{D_{\rm inf}}{D_{\rm pre}}", "role": "compare parameter scaling with extra test-time tokens", "symbols": {"P": "model parameters", "D_pre": "pretraining tokens", "D_inf": "inference tokens"}, "evidence": "paper.pdf pp. 14–15, Section 7", "interpretation": "Which allocation wins depends on deployment load R as well as question difficulty."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: main results, optimal policy and difficulty bins", "paper.pdf pp. 8–15: search, revisions and FLOPs-matched exchange", "source PDF SHA-256 ded7b20b51493258c5ce2a1a024cd33dd752de1fa3373d1207620da4cfe24545", "Evidence status: full-text verified; no independent reproduction performed."],
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
