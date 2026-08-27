#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 017."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2501.12948", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2501.12948",
        "title_en": "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
        "title_zh": "DeepSeek-R1：用强化学习激发大语言模型的推理能力",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["f7332aacefe6a6a2"], ["Control & Reinforcement Learning"]),
        "verified_metadata": meta("2501.12948", "v2", "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", ["DeepSeek-AI"], ["cs.CL", "cs.AI", "cs.LG"], "cs.CL", "2025-01-22T15:19:35Z", "Rule-based reinforcement learning, cold-start data, rejection sampling and distillation are combined to train and transfer long-form reasoning."),
        "sections": [
            sec("作者信息", r"DeepSeek-AI；arXiv:2501.12948v2。全文 87 页。论文区分 DeepSeek-R1-Zero、三阶段开发 checkpoint、最终 DeepSeek-R1，以及从 R1 蒸馏到 Qwen/Llama 的 1.5B–70B dense models。"),
            sec("研究问题", r"监督式 chain-of-thought 依赖昂贵人工轨迹，也可能把推理限制在示范分布内。论文问：只用可验证 reward 与 GRPO，base model 是否会自发延长推理、反思和改写策略；又如何修复纯 RL 输出的可读性、语言混杂和通用任务退化？"),
            sec("背景", r"GRPO 不训练单独的 value model，而在同一问题的一组 sampled responses 内用 reward 的相对位置估计 advantage。对数学/代码任务，答案可由规则 verifier 判定；format reward 约束思考标签，但不直接教授具体推理步骤。", r"Figure 2 显示最终系统不是一次 RL：cold-start SFT、reasoning RL、rejection-sampling SFT、all-scenario RL 依次作用，并以不同 checkpoint 产生训练数据。"),
            sec("模型与方法", r"R1-Zero 从 DeepSeek-V3-Base 直接做 GRPO；每个 prompt 采样一组输出，以组内标准化 reward 更新 clipped policy objective，并加 KL regularization。最终 R1 先用数千条 cold-start traces 建立可读格式，再做 reasoning RL。", r"随后从 checkpoint rejection-sample 约 600k reasoning 与 200k non-reasoning examples 做 SFT，再以 helpfulness/safety reward 做第二阶段 RL。蒸馏模型只做 SFT，不复现大模型的 RL dynamics。"),
            sec("核心结果与证据", r"Figure 2 把关键因果链画清：纯 RL 负责探索，cold start 固定表达协议，rejection sampling 把探索结果转成监督数据，第二次 RL 才覆盖通用偏好。", r"R1-Zero 的 AIME 2024 pass@1 从 15.6% 升至 77.9%，self-consistency 到 86.7%；同时平均 response length 持续增长。最终 R1 在 AIME 2024 报告 79.8，蒸馏的 32B model 报告 72.6。", r"增长与 reward-correlated behavior 同时出现，但不证明“aha moment”是人类式理解；benchmark、采样预算与 verifier 都是训练系统的一部分。"),
            sec("有效性与局限", r"论文明确列出 function calling、多轮交互、复杂 role-playing、JSON 输出和非中英文语言的不足；长回答也可能 overthink 简单问题。纯规则 reward 只覆盖可判分域，开放式任务仍依赖 reward model 与人工偏好。", r"训练数据、完整 RL infrastructure 和所有 intermediate checkpoints 未完全开放，不能 exact reproduce。AIME contamination、自一致采样成本与 test-time token budget 都应与 pass@1 分开；蒸馏成功不证明小模型能独立通过同样 RL 获得能力。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2501.12948；模型/代码：https://github.com/deepseek-ai/DeepSeek-R1。全文 87 页，PDF SHA-256：b191b0a365a64b4ab2791d117069ed17a2933d03554a662ced58b37df52018f4。", r"评估需固定 checkpoint、prompt template、thinking budget、temperature、samples/self-consistency、answer extractor、benchmark commit 与 contamination policy；训练复现还需 GRPO group size、clip/KL、reward/verifier 和各阶段数据。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2，区分 R1-Zero 的 emergence 与 R1 的工程化 pipeline；再读 GRPO objective 和 reward construction。随后逐行核对 Table 3 与 distillation tables，最后读 Section 6 limitations，不把长 CoT、可验证答案和一般智能混为一谈。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2501.12948/figure-2-r1-pipeline.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 6, Figure 2", "alt_text": "DeepSeek-R1 从 V3-Base 经 cold-start、两轮 RL、SFT 与 rejection sampling 的多阶段流程。", "caption": "R1 的最终能力来自探索、数据回收与偏好对齐的多阶段闭环，而非单次纯 RL。", "selection_rationale": "Figure 2 是全文最重要的机制图，优先于 AIME 单指标曲线。"},
        "figure_refs": [figure("2501.12948", "figure-2-r1-pipeline.webp", "Figure 2", 6, "explain the multi-stage R1 training pipeline", "Cold-start, RL, rejection-sampling SFT and all-scenario RL pipeline.", "Reasoning exploration and readable aligned behavior are introduced at different stages.", "The diagram does not isolate each stage's causal contribution without matched ablations.")],
        "equation_refs": [
            {"label": "Group-relative advantage", "latex": r"\hat A_i=\frac{r_i-\operatorname{mean}(r_1,\ldots,r_G)}{\operatorname{std}(r_1,\ldots,r_G)}", "role": "estimate advantage without a learned value model", "symbols": {"r_i": "reward for response i", "G": "responses sampled for one prompt"}, "evidence": "paper.pdf pp. 2–3", "interpretation": "The comparison baseline is the sampled group for the same question."},
            {"label": "Clipped GRPO objective", "latex": r"\mathcal J=\mathbb E\!\left[\min(\rho_i\hat A_i,\operatorname{clip}(\rho_i,1-\epsilon,1+\epsilon)\hat A_i)-\beta D_{\rm KL}\right]", "role": "update the policy with bounded importance ratios", "symbols": {"rho_i": "new-to-old policy ratio", "beta": "KL coefficient"}, "evidence": "paper.pdf p. 3", "interpretation": "Rule rewards define what is optimized; the objective alone does not guarantee faithful reasoning."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–9: GRPO, emergence and multi-stage R1 pipeline", "paper.pdf pp. 10–17 and supplements: benchmarks, PPO comparison and limitations", "source PDF SHA-256 b191b0a365a64b4ab2791d117069ed17a2933d03554a662ced58b37df52018f4", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2501.18322", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2501.18322",
        "title_en": "A Unified Perspective on the Dynamics of Deep Transformers", "title_zh": "深层 Transformer 动力学的统一视角",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["3ea17d1258ea9b9b"], ["Transformer Theory"]),
        "verified_metadata": meta("2501.18322", "v2", "A Unified Perspective on the Dynamics of Deep Transformers", ["Valérie Castin", "Pierre Ablin", "José Antonio Carrillo", "Gabriel Peyré"], ["cs.LG", "math.AP"], "cs.LG", "2025-01-30T13:04:54Z", "Mean-field transport PDEs connect deep self-attention, masked attention and Sinkformers to clustering, blow-up and covariance flows."),
        "sections": [
            sec("作者信息", r"作者：Valérie Castin、Pierre Ablin、José Antonio Carrillo、Gabriel Peyré；arXiv:2501.18322v2。全文 70 页，是 self-attention 连续深度极限的数学分析，重点不是语言 benchmark。"),
            sec("研究问题", r"当 Transformer depth 很大、layer step 很小时，token cloud 是否服从可解析的 measure-valued dynamics？不同 attention kernel、causal mask 与 Sinkhorn normalization 会导致 clustering、rank collapse、finite-time blow-up 还是稳定 transport？"),
            sec("背景", r"把第 \(\ell\) 层 token empirical measure 记为 \(\mu_\ell\)，residual attention 是 transport map 的显式 Euler step；深度重标度后得到 continuity equation。该 mean-field 视角保留 token distribution，却忽略 finite-width stochasticity、MLP、normalization 与训练中的参数变化。", r"Figure 1 在 Gaussian closure 下展示两种协方差轨迹：一类向低秩 cluster 收缩，另一类在有限时间发散。"),
            sec("模型与方法", r"作者对 Softmax、\(\ell_2\)、Sinkhorn 与 masked self-attention 建立 transport PDE，并证明 compactly supported measure 的 well-posedness 条件。Gaussian 初值在特定参数下保持 Gaussian，使 PDE 降为 mean/covariance ODE。", r"对 causal mask，引入 position–token joint measure 与 conditional Wasserstein metric；对 Sinkformer，symmetrization 恢复 Wasserstein gradient-flow 结构。深 Transformer 被解释为这些连续流的离散化。"),
            sec("核心结果与证据", r"Figure 1 是最物理化的结果：同一个 covariance equation 随参数 \(\epsilon\) 进入 clustering 或 blow-up sector，椭圆主轴与体积随深度连续变化。", r"理论给出 Gaussian self-attention 的 covariance dynamics、部分参数区的 finite-time blow-up，以及稳定区向 rank-deficient limit 的收敛。随机矩阵实验显示极限 rank 分布，并比较 Softmax、multi-head、\(\ell_2\) 与 Sinkhorn 的相似/不同渐近行为。", r"这些定理描述固定权重的层间动力学，不直接预测训练后真实 LLM 的语义表示或 generalization。"),
            sec("有效性与局限", r"连续深度需要小 residual step 和足够规则的 velocity field；实际 Transformer 含 LayerNorm、MLP、position encoding、finite heads 与随层变化参数。Gaussian closure 只对特定初始化/矩阵结构封闭。", r"measure collapse 可以是几何低秩化，却不等同于表示退化；blow-up 也可能被 normalization 截断。随机数值图用于支持典型行为，不能替代对所有 \(Q,K,V\) 的完整相图。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2501.18322。全文 70 页，PDF SHA-256：f04ccf7842980e1d41564d025f8f4ea6f69cb90a7c5bd4c5a635395fb0ef3207。", r"复现需固定 attention convention、residual-depth scaling、\(Q,K,V\)、Gaussian covariance、ODE/PDE solver、blow-up stopping rule、random-matrix ensemble 与 rank tolerance。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 introduction 的四类 attention PDE 与 Figure 1；再看 well-posedness 和 Gaussian covariance theorem。随后读 masked attention 的 conditional Wasserstein construction 与 Sinkformer gradient flow，最后用 appendix figures 检查哪些结论是定理、哪些仅为数值现象。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2501.18322/figure-1-covariance-dynamics.webp", "label": "Figure 1", "visual_type": "trajectory", "evidence": "paper.pdf p. 4, Figure 1", "alt_text": "二维 Gaussian token cloud 的协方差随深度发生 clustering 或 finite-time blow-up。", "caption": "深层 self-attention 的 Gaussian closure 可进入低秩聚类或有限时发散两类动力学。", "selection_rationale": "Figure 1 直接可视化全文核心动力学，比抽象定理列表更适合作为封面。"},
        "figure_refs": [figure("2501.18322", "figure-1-covariance-dynamics.webp", "Figure 1", 4, "visualize clustering and blow-up regimes", "Gaussian covariance ellipses evolving under Softmax self-attention.", "Parameter changes select contraction toward low rank or covariance divergence.", "The closure concerns idealized fixed-weight attention, not a full trained Transformer.")],
        "equation_refs": [
            {"label": "Attention transport PDE", "latex": r"\partial_t\mu_t+\nabla\!\cdot\!\bigl(\mu_t\,\Gamma_{\mu_t}\bigr)=0", "role": "describe the continuous-depth token distribution", "symbols": {"mu_t": "token probability measure", "Gamma": "measure-dependent attention velocity"}, "evidence": "paper.pdf pp. 2–5", "interpretation": "Residual layers become transport steps when depth tends to a continuum."},
            {"label": "Gaussian covariance flow", "latex": r"\dot\Sigma_t=V\Sigma_t+\Sigma_tV^\top+\Sigma_tA\Sigma_tV^\top+V\Sigma_tA^\top\Sigma_t", "role": "reduce attention PDE to a matrix ODE", "symbols": {"Sigma": "token covariance", "A": "K^T Q"}, "evidence": "paper.pdf Section 4", "interpretation": "Nonlinear covariance feedback produces contraction, rank loss or blow-up depending on the matrices."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–24: transport PDE, well-posedness and Gaussian dynamics", "paper.pdf pp. 24–39: masked attention and Sinkformer geometry", "source PDF SHA-256 f04ccf7842980e1d41564d025f8f4ea6f69cb90a7c5bd4c5a635395fb0ef3207", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2504.01938", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/2504.01938",
        "title_en": "A Unified Approach to Analysis and Design of Denoising Markov Models", "title_zh": "去噪马尔可夫模型分析与设计的统一方法",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["fec57c0ff64d46f6"], ["Generative Models"]),
        "verified_metadata": meta("2504.01938", "v2", "A Unified Approach to Analysis and Design of Denoising Markov Models", ["Yinuo Ren", "Grant M. Rotskoff", "Lexing Ying"], ["cs.LG", "math.NA", "stat.ML"], "cs.LG", "2025-04-02T17:46:43Z", "Generator identities unify forward corruption, exact time reversal, learned denoising and KL objectives for diffusions, jumps and Lévy-type processes."),
        "sections": [
            sec("作者信息", r"作者：Yinuo Ren、Grant M. Rotskoff、Lexing Ying；arXiv:2504.01938v2。全文 70 页。论文以 Markov generator 与 path-space KL 为核心，实验只是 geometric Brownian motion 和 jump process 的 proof of concept。"),
            sec("研究问题", r"score diffusion 的时间反演公式高度依赖 Brownian noise。论文问：能否对任意 Markov noising process 直接从 generator 推导 backward process、可学习目标与终点分布误差，并由此系统设计非 Gaussian、非连续的 denoising models？"),
            sec("背景", r"forward process 将数据 \(p_0\) 推到易采样 \(p_T\)；真实 reverse process 恢复数据，但其 generator 依赖未知的密度比/score。estimated reverse process 用模型替换这部分，并从近似 \(q_0\) 开始。", r"Figure 1 用红、蓝、黑三条 generator/path 关系图把 forward、true backward 和 estimated backward 的误差来源分开。"),
            sec("模型与方法", r"作者在一般状态空间上用 carré-du-champ / generator calculus 推导 time reversal，并用 Girsanov-type change of measure 连接 path-space KL 与局部 generator estimation loss。data-processing inequality 再把生成终点 KL 上界为初始化误差加积分训练误差。", r"框架专门化后恢复 diffusion score matching、finite-state jump/CTMC objectives，并允许一般 Lévy-type processes。设计原则是先选 forward generator，再从反演结构读出要估计的 observable。"),
            sec("核心结果与证据", r"Figure 1 是理论路线图：红色真实反演与蓝色估计反演的差异沿时间积累，而终点分布误差由路径 KL 控制；这比只写一个 score loss 更清楚地显示误差预算。", r"论文证明 terminal divergence 满足初始化 mismatch 与 generator estimation error 的上界；在 diffusion 和 jump special cases 中回收熟悉的连续/离散 denoising loss。", r"GBM 实验能恢复一维/二维目标分布，jump model 在 chessboard、Swiss roll、moons 上的 backward marginals 接近 forward references。作者明确声明目标不是击败现有模型，而是证明设计空间可行。"),
            sec("有效性与局限", r"KL 界可能松，且需要 absolute continuity、可积性与 generator domain 等条件；若 forward/reverse path measures 不相容，KL 可为无穷。终点 KL 小也不保证 perceptual quality 或 mode-wise rare-event fidelity。", r"实验是低维 proof of concept，没有大型图像/语言 scaling、速度或 sample-quality comparison。一般 Lévy generator 的可训练 parameterization、稳定 simulation 与 density-ratio estimation仍是主要工程难点。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2504.01938。全文 70 页，PDF SHA-256：79569261719f02ddf16d1f74c7d130c5ad8af33fa0d27145718943dcc9e0ca6d。", r"复现需固定 forward generator、horizon \(T\)、initial/reference laws、score或rate parameterization、time sampling、discretization、GBM/jump simulator、KL estimator 与低维 target sampler。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 Section 2 的 forward/backward generators；再读 Theorems 3.2–3.6 的反演与 KL 链。随后把 diffusion、CTMC、Lévy special cases 逐项代回，最后看低维 figures，只把它们视为构造验证而非 SOTA 证据。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2504.01938/figure-1-denoising-roadmap.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 1", "alt_text": "forward noising、真实 backward 与 estimated denoising processes 的 generator 路线图。", "caption": "一般 Markov generator 将时间反演、训练误差与最终 KL 偏差放进同一个结构。", "selection_rationale": "Figure 1 是全文统一框架的核心机制图，优先于低维样本图。"},
        "figure_refs": [figure("2504.01938", "figure-1-denoising-roadmap.webp", "Figure 1", 4, "show the generator-level error decomposition", "Forward, true backward and estimated backward Markov processes.", "Learning replaces the inaccessible reverse generator and path KL controls endpoint error.", "The bound needs regularity and may be loose for finite parameterizations.")],
        "equation_refs": [
            {"label": "Endpoint KL control", "latex": r"D_{\rm KL}(p_0\|q_T)\le D_{\rm KL}(p_T\|q_0)+D_{\rm KL}(\mathbb P^{\rm rev}\|\widehat{\mathbb P}^{\rm rev})", "role": "separate initialization and learned-dynamics error", "symbols": {"p_t": "forward marginals", "q_t": "estimated backward marginals"}, "evidence": "paper.pdf Section 3", "interpretation": "Data processing converts path mismatch into a terminal distribution bound."},
            {"label": "Diffusion reverse drift", "latex": r"b_t^{\rm rev}(x)=-b_{T-t}(x)+a_{T-t}(x)\nabla\log p_{T-t}(x)+\nabla\!\cdot a_{T-t}(x)", "role": "recover score-based reversal as a special case", "symbols": {"a": "diffusion tensor", "b": "forward drift"}, "evidence": "paper.pdf Section 4", "interpretation": "The familiar score term is one representation of the general reversed generator."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–18: generator reversal and KL error theory", "paper.pdf pp. 18–30: diffusion, jump, Lévy cases and experiments", "source PDF SHA-256 79569261719f02ddf16d1f74c7d130c5ad8af33fa0d27145718943dcc9e0ca6d", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2504.18506", "source_version": "v3", "source_pdf": "https://arxiv.org/pdf/2504.18506",
        "title_en": "Action-Minimization Meets Generative Modeling: Efficient Transition Path Sampling with the Onsager-Machlup Functional",
        "title_zh": "作用量最小化遇见生成建模：以 Onsager–Machlup 泛函高效采样跃迁路径",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["16deea2a8042b097"], ["Generative Models"]),
        "verified_metadata": meta("2504.18506", "v3", "Action-Minimization Meets Generative Modeling: Efficient Transition Path Sampling with the Onsager-Machlup Functional", ["Sanjeev Raja", "Martin Šípka", "Michael Psenka", "Tobias Kreiman", "Michal Pavelka", "Aditi S. Krishnapriyan"], ["cs.LG", "cond-mat.mtrl-sci", "physics.chem-ph", "q-bio.BM"], "cs.LG", "2025-04-25T17:17:17Z", "Scores extracted from atomistic generative models define Onsager–Machlup actions whose optimized paths approximate molecular transition pathways."),
        "sections": [
            sec("作者信息", r"作者：Sanjeev Raja、Martin Šípka、Michael Psenka、Tobias Kreiman、Michal Pavelka、Aditi S. Krishnapriyan；arXiv:2504.18506v3。全文 38 页，覆盖 Müller–Brown、alanine dipeptide、fast-folding proteins 与未见 tetrapeptides。"),
            sec("研究问题", r"生成模型擅长独立 equilibrium samples，却不直接给出带动力学意义的 rare transition paths。论文问：能否把 diffusion/flow model 的 learned score 解释为随机动力学 drift，用 Onsager–Machlup action 在给定端点间优化高概率路径，而不为 TPS 另训模型？"),
            sec("背景", r"过阻尼 Langevin path 的概率权重由 OM functional 决定，包含 drift mismatch 与 divergence/Laplacian correction。若 \(p_{\rm data}\propto e^{-\beta U}\)，score 与 force 成比例；生成模型提供可微的近似 score。", r"Figure 1 将 atomistic generative model、learned vector field/score、OM action landscape 与 transition paths 连成一条物理解释链。"),
            sec("模型与方法", r"路径由离散 beads 参数化，固定反应物/产物端点，以 gradient optimizer 最小化 full 或 truncated OM action。diffusion model 在选择的 noise time 提供 score；flow matching 通过 stochastic encoding/decoding 与 velocity-score relation 提取等效 drift。", r"Hutchinson trace estimator 近似 score divergence；优化得到的路径还用于训练 committor network，并通过 backward Kolmogorov relation估计 transition rate。"),
            sec("核心结果与证据", r"Figure 1 展示核心转换：原本只生成 i.i.d. equilibrium conformations 的模型，经 score-as-force 解释后成为 transition-path action。", r"在 alanine dipeptide 上，作者报告 OM optimization 每 1000-step path 所需 force evaluations 少于 metadynamics 与 shooting baselines；Müller–Brown 上由优化路径得到的 rate 为 \(1.3\times10^{-5}\)，接近文中 reference。", r"在 BBA、Trp-cage 等 coarse-grained proteins 上，路径穿过经验 committor \(q\approx0.5\) 的 transition-state region；未见 tetrapeptides 的 MSM metrics 与 50–100 ns MD 相当。"),
            sec("有效性与局限", r"作者明确指出方法不保证从正确 transition-path ensemble 无偏采样；action minimization 更接近最可能路径搜索，可能漏掉多通道熵贡献。learned score 的 force interpretation 依赖 equilibrium、temperature 与 coarse-graining assumptions。", r"端点、路径长度、diffusivity、noise-time 与 optimizer initialization 都会选择不同局部极小。committor/rate 结果需要额外 dynamics validation；低 force-evaluation count 也不等于相同硬件 wall time。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2504.18506；代码：https://github.com/ASK-Berkeley/Action-Minimization-Generative-Modeling。全文 38 页，PDF SHA-256：c5d7b59e338facfa30a108eb41db324b43165072e92077d8fe9351f97fe50663。", r"复现需固定 generative checkpoint、score extraction time、temperature/friction/diffusivity、beads/horizon、full/truncated action、trace samples、optimizer/seeds、endpoint definitions、force-field与 committor/MSM protocol。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 与 OM functional，核对 score–force 假设；再读 diffusion/flow score extraction 和 discretized action。随后审查 alanine/protein figures 与 force-evaluation table，最后读 limitations，把最可能路径、transition-path ensemble、committor 和 rate 四个对象分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2504.18506/figure-1-om-schematic.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "从原子生成模型的 learned score 到 Onsager–Machlup action optimization 与分子跃迁路径的流程。", "caption": "把 learned score 解释为 drift 后，可在 OM action 上直接优化稀有跃迁路径。", "selection_rationale": "Figure 1 同时呈现生成模型、作用量和物理路径，是全文最重要的机制可视化。"},
        "figure_refs": [figure("2504.18506", "figure-1-om-schematic.webp", "Figure 1", 2, "connect generative scores to transition paths", "Learned atomistic score, OM action and optimized molecular paths.", "The generative vector field supplies an effective drift for path-space optimization.", "Action minima are not guaranteed unbiased samples from the full transition ensemble.")],
        "equation_refs": [
            {"label": "Onsager–Machlup action", "latex": r"S[x]=\int_0^T\left[\frac{1}{4D}\|\dot x-b(x)\|^2+\frac12\nabla\!\cdot b(x)\right]dt", "role": "score the probability of a stochastic transition path", "symbols": {"b": "drift inferred from score or force", "D": "diffusivity"}, "evidence": "paper.pdf pp. 2–4", "interpretation": "Minimizing the discretized action seeks high-probability paths under the assumed Langevin dynamics."},
            {"label": "Equilibrium score-force relation", "latex": r"\nabla\log p_{\rm data}(x)=-\beta\nabla U(x)=\beta F(x)", "role": "interpret the learned score as a physical force", "symbols": {"beta": "inverse temperature", "U": "potential energy"}, "evidence": "paper.pdf pp. 3–4", "interpretation": "The identification is exact only for the stated equilibrium density and coordinates."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–9: OM construction and molecular experiments", "paper.pdf appendices: score extraction, committor/rate estimation and ablations", "source PDF SHA-256 c5d7b59e338facfa30a108eb41db324b43165072e92077d8fe9351f97fe50663", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2504.19353", "source_version": "v1", "source_pdf": "https://arxiv.org/pdf/2504.19353",
        "title_en": "Flow Along the K-Amplitude for Generative Modeling", "title_zh": "沿 K-振幅流动的生成建模",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["e7da69e250c4b5fa"], ["Generative Models"]),
        "verified_metadata": meta("2504.19353", "v1", "Flow Along the K-Amplitude for Generative Modeling", ["Weitao Du", "Shuning Chang", "Jiasheng Tang", "Yu Rong", "Fan Wang", "Shengchao Liu"], ["cs.LG", "cs.AI"], "cs.LG", "2025-04-27T20:38:24Z", "K-Flow decomposes data into Fourier, wavelet or PCA amplitudes and learns a coarse-to-fine flow over scaling components."),
        "sections": [
            sec("作者信息", r"作者：Weitao Du、Shuning Chang、Jiasheng Tang、Yu Rong、Fan Wang、Shengchao Liu；arXiv:2504.19353v1。全文 26 页，实验包含 CelebA-HQ 256、LSUN Church 256 与 ImageNet conditional generation。"),
            sec("研究问题", r"标准 flow matching 在同一时间连续更新全部 latent directions，没有显式利用图像能量集中在低频/低尺度的结构。论文问：能否先把样本分成 ordered K-amplitude components，再沿尺度从 coarse semantics 流到 fine detail，并获得可控编辑与更低 projection error？"),
            sec("背景", r"K-amplitude transform 可由 Fourier、Daubechies wavelet 或 PCA 给出；截断到尺度 \(k\) 的重构 \(\phi_k\) 随 \(k\) 增大收敛到原数据。低尺度分量具有更高 norm/energy，通常编码 identity、layout 等全局语义。", r"Figure 1 直接比较 Fourier、Wavelet、PCA 三种从低尺度模糊结构到高尺度细节的生成序列，是全文最具可视性的封面。"),
            sec("模型与方法", r"K-Flow 在相邻 amplitude states 之间学习 vector field，并把离散尺度 \(k\) 连续化；Wave-DiT 以多尺度 wavelet representation 提供 inductive bias。训练仍采用 flow-matching regression，但路径不再是简单 Gaussian–data 直线。", r"conditional generation 可在后段丢弃 class condition，测试类别信息主要进入低尺度的假设；固定高/低尺度 noise 则允许分别编辑语义与细节。"),
            sec("核心结果与证据", r"Figure 1 显示三种分解都先形成姿态/轮廓，再补纹理；Wavelet 的局部多尺度结构比 Fourier ringing 或 PCA data-basis 更直接。", r"CelebA-HQ 256 上 Fourier-DiT L/2、Wave-DiT L/2 的 FID/Recall 为 5.11/0.47 与 4.99/0.46。LSUN Church 上 two/three-scale K-Flow 为 5.37/0.47 与 5.19/0.49。", r"低尺度分量 norm 约为高尺度近两倍，并在 PCA projection-error 图上显示更低误差；这些是低尺度假设的经验支持，不是所有自然数据的谱定理。"),
            sec("有效性与局限", r"改进依赖分解 basis、尺度顺序、backbone 和同等 compute 的实现；表中不同模型的 architecture/parameter count 需逐项核对。FID/Recall 对 feature extractor 与样本数敏感，不能覆盖 identity preservation 或物理一致性。", r"Fourier/Wavelet 低频与语义的对应只是统计倾向；PCA basis 依赖训练数据，跨域时可能失效。分段 flow 增加 schedule 与 interface choices，若尺度过离散会限制连续 solver 的优势。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2504.19353。全文 26 页，PDF SHA-256：235ea85361cfa9a29fc57a9f6a02e8fd39bde9db1556b77d81602ab306c116bc。", r"复现需固定 autoencoder latent、Fourier/Wavelet/PCA basis、wavelet family、K/scales、continuous \(k\) schedule、DiT size、solver/steps/guidance、datasets、50k-sample FID/Recall 与 edit seeds。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 理解 coarse-to-fine path，再读 K-amplitude definition 和 continuous \(k\) dynamics；随后看 Figures 3–5 的 energy/projection evidence。最后对照 Tables 2–3 与 conditional editing figures，区分生成质量、谱归纳偏置和可控性。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2504.19353/figure-1-kflow-samples.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "Fourier、Wavelet 和 PCA K-amplitude 路径从低尺度轮廓逐步生成高尺度图像细节。", "caption": "K-Flow 把生成过程重排为从高能量的全局结构到低能量细节的尺度演化。", "selection_rationale": "Figure 1 是原文最直观的生成可视化，优先于 FID 数据表。"},
        "figure_refs": [figure("2504.19353", "figure-1-kflow-samples.webp", "Figure 1", 1, "visualize coarse-to-fine amplitude flow", "Fourier, wavelet and PCA generation sequences.", "Global structure appears at low scaling before fine texture is added.", "The visual ordering depends on the chosen decomposition and does not prove semantic disentanglement.")],
        "equation_refs": [
            {"label": "K-amplitude reconstruction", "latex": r"\phi_k=\mathcal T^{-1}\!\left[m_k\odot\mathcal T(\phi)\right],\qquad \lim_{k\to K}\phi_k=\phi", "role": "define the ordered coarse-to-fine states", "symbols": {"T": "Fourier, wavelet or PCA transform", "m_k": "scale mask"}, "evidence": "paper.pdf Sections 3.1–3.2", "interpretation": "Increasing k restores additional amplitude components until the original sample is recovered."},
            {"label": "K-flow matching loss", "latex": r"\mathcal L_{\rm KFM}=\mathbb E_{k,\phi}\left\|v_\theta(\phi_k,k)-\partial_k\phi_k\right\|_2^2", "role": "learn motion along the amplitude path", "symbols": {"v_theta": "scale-conditioned vector field", "phi_k": "partial reconstruction"}, "evidence": "paper.pdf Section 3", "interpretation": "The learned transport follows a structured spectral path rather than a direct noise-data interpolation."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–14: K-amplitude path, low-scaling hypothesis and Wave-DiT", "paper.pdf pp. 15–19: generation metrics and controllable experiments", "source PDF SHA-256 235ea85361cfa9a29fc57a9f6a02e8fd39bde9db1556b77d81602ab306c116bc", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        (OUT / f"{card['arxiv_id']}.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"installed": [card["arxiv_id"] for card in CARDS]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
