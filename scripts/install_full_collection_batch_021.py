#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 021."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2510.01631", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2510.01631",
        "title_en": "Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls",
        "title_zh": "解密大模型预训练中的合成数据：标度律、收益与陷阱的系统研究",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8e2b6b945b541727"], ["Scaling Laws"]),
        "verified_metadata": meta(
            "2510.01631", "v1",
            "Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls",
            ["Feiyang Kang", "Newsha Ardalani", "Michael Kuchnik", "Youssef Emad", "Mostafa Elhoushi", "Shubhabrata Sengupta", "Shang-Wen Li", "Ramya Raghavendra", "Ruoxi Jia", "Carole-Jean Wu"],
            ["cs.LG", "cs.AI", "cs.CL"], "cs.LG", "2025-10-02T03:24:42Z",
            "More than one thousand controlled pretraining runs show that synthetic data helps conditionally: rephrased-natural mixtures scale well, while pure textbook-style data can degrade.",
        ),
        "sections": [
            sec("作者信息", r"作者：Feiyang Kang、Newsha Ardalani、Michael Kuchnik、Youssef Emad、Mostafa Elhoushi 等 10 位；arXiv:2510.01631v1。全文 25 页。作者报告超过 1,000 个 LLM variants、最高 3B 参数、最高 200B tokens，并消耗超过 \(10^5\) GPU-hours；正文实验细节另给出约 70k A100-hours 的主 sweep。"),
            sec("研究问题", r"高质量自然文本有限，合成数据被视为替代来源，但“更干净”与“更少多样性”同时存在。论文问：纯 rephrased、QA-rephrased、textbook-generated 数据和它们与 CommonCrawl 的混合，分别如何改变 data/model scaling；最佳 synthetic ratio 是否随模型和预算变化；单轮 synthetic training 是否出现 model-collapse 型标度恶化？"),
            sec("背景", r"作者统一使用 Llama-3 风格 decoder-only 架构、相同 tokenizer/optimization protocol，并把验证损失拟合为 \(\widehat L(D)=B D^{-\beta}+E\) 或 \(\widehat L(N)=A N^{-\alpha}+E\)。其中 \(E\) 是数据混合的拟合 irreducible loss，不应解释为真实熵率的无偏测量。", r"Figure 4 不再只比较两条 loss 曲线，而是在 HQ、QA、TXBK 三类合成数据上直接画出不同 \(N,D\) 下的最优混合比例，揭示“合成数据是否有用”不是二元问题。"),
            sec("模型与方法", r"自然基线为 unfiltered CommonCrawl；HQ/QA 数据通过模型重写自然文档，TXBK 为模型生成的教材式文本。主 scaling sweep 使用 0%、33%、67%、100% 比例，并在固定 1B 模型扫描 \(D=1\)–200B tokens、固定 50B tokens 扫描 \(N=100\)M–3B；每条件通常有 3–5 个 variants。", r"额外 grid search 在模型规模和 data budget 上寻找最佳比例；generator ablation 比较 Llama-3 3B/8B/70B 生成的数据。data law 用不超过 100B 的点预测 200B，model law 用不超过 2B 的模型预测 3B，避免把更远的 400B 外推当作观测。"),
            sec("核心结果与证据", r"Figure 4 显示 HQ rephrased 的最佳比例在所测尺度约 30%，QA 从小规模约 50% 向大规模约 30% 收敛；TXBK 在小预算通常低于 5%，随规模上升但仍显著更低。这比“固定 50% synthetic”规则更接近一个带 data-type 依赖的相图。", r"data-scaling holdout 的 RMABE 为 0.41%，model-scaling holdout 为 0.30%。在较大数据预算下，约 1/3 rephrased synthetic + 2/3 natural 达到同 validation loss 可快 5–10 倍；纯 rephrased 并不比自然文本更快，纯 TXBK 在多域尤其小预算下损失更高。", r"33% HQ + 67% CC 给出最低拟合 \(E\)；8B generator 明显优于 3B，但 70B 不再改善 downstream validation loss。作者因此只得到 mixed evidence：单轮 rephrased mixtures 未见预期退化，TXBK mixtures 则出现 model-collapse 理论所预言的坏趋势。"),
            sec("有效性与局限", r"实验上限是 3B/200B，远低于现代 frontier pretraining；400B 模型曲线只是参数外推。主要指标为 perplexity/loss，缺少深入 human evaluation；数据领域以网页与英文任务为主，generator family 和 prompts 也有限。", r"研究只做单轮 \(n=1\) synthetic generation，不检验递归多代 model collapse。CommonCrawl 本身并非无偏自然分布，训练/评估泄漏与语料质量难以完全排除。5–10× 是达到同 loss 的 token efficiency，不是 wall-clock 或总生成成本加速。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2510.01631。全文 25 页，PDF SHA-256：a7e3ac5091b434b390013576c19664e9e30ff9dfe235d496b144cc64076f4703。", r"复现需固定 CommonCrawl snapshot、HQ/QA/TXBK prompts、generator checkpoint、dedup/contamination filters、mixture sampler、tokenizer、\(N,D\) grid、seeds、fit window 与 RMABE definition。应同时核算 synthetic generation FLOPs，而非只计 downstream pretraining tokens。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 4，建立 data type–model size–budget 三维依赖；再读 Figures 1–3 的 holdout scaling fits，区分实测范围和外推。随后看 generator ablation 与 model-collapse discussion，最后核对 Limitations，避免把“约 30%”当作跨语料、跨模型的普适常数。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2510.01631/figure-4-mixture-ratios.webp", "label": "Figure 4", "visual_type": "data_plot", "evidence": "paper.pdf p. 8, Figure 4", "alt_text": "HQ、QA 与 textbook 合成数据在不同模型规模和数据预算下的最佳混合比例。", "caption": "最佳合成比例取决于数据类型与尺度；rephrased 数据趋近约 30%，textbook 数据需要更低比例。", "selection_rationale": "Figure 4 是论文最重要的操作性结果，优先于单一 scaling curve。"},
        "figure_refs": [figure("2510.01631", "figure-4-mixture-ratios.webp", "Figure 4", 8, "show scale- and type-dependent synthetic-data ratios", "Three panels report best grid-searched mixture ratios for HQ, QA and textbook data.", "Rephrased data approaches a roughly 30 percent optimum while textbook data remains much lower.", "The optimum is empirical and limited to the tested corpora, models and budgets.")],
        "equation_refs": [
            {"label": "Data scaling law", "latex": r"\widehat L(D)=B D^{-\beta}+E", "role": "fit validation loss across token budgets", "symbols": {"D": "training tokens", "E": "fitted irreducible loss"}, "evidence": "paper.pdf p. 5, Section 4.1.3", "interpretation": "Different mixtures change both the convergence exponent and the fitted loss floor."},
            {"label": "Model scaling law", "latex": r"\widehat L(N)=A N^{-\alpha}+E", "role": "compare mixtures across model sizes", "symbols": {"N": "non-embedding model parameters", "alpha": "model-scaling exponent"}, "evidence": "paper.pdf p. 6, Section 4.1.4", "interpretation": "Synthetic mixtures that help with more data need not retain the same advantage as model size grows."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–8: controlled protocol, scaling fits and mixture ratios", "paper.pdf pp. 8–11: generator ablation, collapse discussion and limitations", "source PDF SHA-256 a7e3ac5091b434b390013576c19664e9e30ff9dfe235d496b144cc64076f4703", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2510.15174", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2510.15174",
        "title_en": "A Simple Mean Field Model of Feature Learning",
        "title_zh": "特征学习的一个简单均场模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["53f45db2a0ac7222"], ["Training Dynamics"]),
        "verified_metadata": meta(
            "2510.15174", "v1", "A Simple Mean Field Model of Feature Learning",
            ["Niclas Göring", "Chris Mingard", "Yoonsoo Nam", "Ard Louis"],
            ["cs.LG"], "cs.LG", "2025-10-16T22:28:44Z",
            "A self-consistent mean-field posterior predicts a finite-width feature-learning transition, and an ARD extension captures self-reinforcing selection of task-relevant input coordinates.",
        ),
        "sections": [
            sec("作者信息", r"作者：Niclas Göring、Chris Mingard、Yoonsoo Nam、Ard Louis；arXiv:2510.15174v1。全文 39 页，稿件标注为 ICLR 2026 conference paper。研究二层 ReLU 网络在 SGLD posterior 下的有限宽 feature learning，并用 sparse parity 与 single-index tasks 验证。"),
            sec("研究问题", r"无限宽 NNGP/kernel theory 的表示在训练中不动，无法描述网络突然对齐 task-relevant directions 的 feature learning。完整有限宽 Bayesian posterior 又含所有 neuron-neuron interactions，难以计算。论文问：能否用统计物理均场闭合得到可解的 symmetry-breaking transition，并解释普通 MF 为何低估 transition 后的泛化增益？"),
            sec("背景", r"网络写为 \(f(x)=N^{-\gamma}\sum_i a_i\phi(w_i^\top x)\)。SGLD 对应带 data-induced interaction kernel \(G(w_i,w_{i'})\) 的 Gibbs posterior；infinite width 退化为固定 NNGP。finite width 下，相关输入坐标的 weight marginals 可自发破缺旋转/置换对称，产生非零 feature order parameters。", r"Figure 2 把近似层级画成 many-body problem：SGLD posterior 保留全耦合，MF 用 self-consistent effective field 替代其他 neurons，NNGP 则完全删除 data-dependent coupling。"),
            sec("模型与方法", r"plain MF 假设 \(p(W\mid D)\approx\prod_i p_{\rm MF}(w_i,a_i)\)，并要求单 neuron 分布产生的 feature coefficients \(m_A\) 反过来重建同一 mean field。该闭合把 \(N\times d\) 高维 posterior 化为单个 \(d\)-维积分/固定点问题。", r"plain MF 捕捉 feature-alignment onset，却低估 transition 后 anisotropy。作者引入 MF-ARD：给每个 input coordinate 一个由 posterior second moment 自洽更新的 variance/precision，使被选坐标获得更大波动和更强信号，形成 self-reinforcing input feature selection。"),
            sec("核心结果与证据", r"Figure 2 清楚显示三种理论的物理差别：MF 仍保留平均相互作用，因此可发生 symmetry breaking；NNGP 没有耦合，只能平滑 kernel learning。它也说明 MF-ARD 的修正不是再加深网络，而是让 effective prior 对坐标产生自洽各向异性。", r"在 \(d=35\)、4-sparse parity、\(N=512\) ReLU 上，SGLD 的 order parameter 随样本 \(P\) 在 \(P_c\) 附近突增；plain MF 半定量预测 onset，但 generalization error 降得太弱。MF-ARD 恢复相关坐标的强非 Gaussian marginals，并在 Figure 1/5 中定量贴近 SGLD learning curves 与 \(P\)–noise phase boundary。", r"Theorem 4.1 表明 ARD 机制可消除 plain MF 中 input dimension \(d\) 带来的 \(O(d)\) 样本惩罚；single-index Gaussian teacher 的补充实验也复现相变。结论支持“feature selection 的正反馈”而非单纯 symmetry breaking 决定 transition 后增益。"),
            sec("有效性与局限", r"均场 factorization 忽略 neuron-neuron correlations；MF-ARD 以坐标独立 precisions 表示选择，对旋转后的稠密特征、组合结构或 feature correlations 可能不充分。实验以二层网络、SGLD/Bayesian posterior 和合成教师为主，不直接等价于 SGD 训练深网。", r"Figure 5 的吻合依赖超参数和数值固定点求解；相变位置只有 semi-quantitative precision。理论解释的是 equilibrium/posterior structure，有限训练时间、metastability 与 optimizer implicit bias 尚未统一。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2510.15174。全文 39 页，PDF SHA-256：e3f4c8e1a9f9d9793c6de5a7e968e5ed6862ab3af758f0d8fe98ae91f33ee364。", r"复现需固定 \(N,d,k,P,\kappa,\gamma\)、ReLU normalization、SGLD step/temperature/burn-in、parity support、MF quadrature/Monte Carlo、fixed-point damping 与 ARD precision update。应保存 \(m_S\)、coordinate marginals、specialization 和 test MSE。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2，区分 SGLD、MF、MF-ARD 与 NNGP；再读 Eqs. (5)–(7) 的 self-consistency。随后看 Figures 3–5 的 order parameter、marginals 与 phase diagram，最后读 Theorem 4.1，注意其样本优势来自特定 ARD feature-selection mechanism。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2510.15174/figure-2-mean-field-hierarchy.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "从全耦合 SGLD posterior 到均场有效场、再到无耦合 NNGP 的近似层级。", "caption": "均场保留 data-dependent 平均相互作用，因此能发生 feature-learning 对称破缺；NNGP 不能。", "selection_rationale": "Figure 2 是全文最重要的物理机制图，优先于单一误差曲线。"},
        "figure_refs": [figure("2510.15174", "figure-2-mean-field-hierarchy.webp", "Figure 2", 4, "visualize the many-body to mean-field reduction", "The fully interacting neuron posterior is replaced by a self-consistent one-neuron effective field.", "Retaining the mean interaction permits a symmetry-breaking feature-learning transition absent in NNGP.", "Mean-field factorization suppresses inter-neuron correlations and requires the ARD correction for strong coordinate selection.")],
        "equation_refs": [
            {"label": "Two-layer network", "latex": r"f(x)=N^{-\gamma}\sum_{i=1}^{N}a_i\phi(w_i^\top x)", "role": "define the finite-width feature-learning model", "symbols": {"N": "hidden width", "gamma": "width scaling exponent", "phi": "activation"}, "evidence": "paper.pdf p. 3, Eq. (1)", "interpretation": "Finite width leaves an interacting posterior over neuron directions rather than a fixed kernel."},
            {"label": "Mean-field factorization", "latex": r"p(W,a\mid D)\approx\prod_{i=1}^{N}p_{\rm MF}(w_i,a_i),\qquad m_A=N^{1-\gamma}\langle aJ_A(w)\rangle_{p_{\rm MF}}", "role": "close the neuron ensemble through feature order parameters", "symbols": {"m_A": "feature coefficient", "J_A": "activation overlap with basis feature A"}, "evidence": "paper.pdf p. 4, Eqs. (6)–(7)", "interpretation": "Each neuron is independent conditional on an effective field that it helps generate self-consistently."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: posterior, MF closure and theory hierarchy", "paper.pdf pp. 7–10: parity experiments, ARD and phase diagrams", "source PDF SHA-256 e3f4c8e1a9f9d9793c6de5a7e968e5ed6862ab3af758f0d8fe98ae91f33ee364", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2510.16732", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2510.16732",
        "title_en": "A Comprehensive Survey on World Models for Embodied AI",
        "title_zh": "具身智能世界模型综述",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["0d7d5968a1175e12"], ["Robotics"]),
        "verified_metadata": meta(
            "2510.16732", "v3", "A Comprehensive Survey on World Models for Embodied AI",
            ["Xinqing Li", "Xin He", "Le Zhang", "Min Wu", "Xiaoli Li", "Yun Liu"],
            ["cs.CV"], "cs.CV", "2025-10-19T07:12:32Z",
            "A three-axis taxonomy organizes embodied world models by decision coupling, temporal prediction and spatial representation, with datasets and metrics spanning robotics, driving and video.",
        ),
        "sections": [
            sec("作者信息", r"作者：Xinqing Li、Xin He、Le Zhang、Min Wu、Xiaoli Li、Yun Liu；arXiv:2510.16732v3。全文 24 页。文章是结构化综述，不提出单一新模型；作者维护 AwesomeWorldModels bibliography，并汇总 robotics、autonomous driving、general video 的数据与指标。"),
            sec("研究问题", r"“world model”覆盖 latent dynamics、video generator、planning simulator 和 representation learner，术语高度混杂。综述问：如何用少量互相正交的轴分类这些模型，并把 pixel realism、state understanding、physical consistency、closed-loop task success 与 real-time cost 放在同一评估框架中？"),
            sec("背景", r"具身 agent 需要从历史观测和动作预测未来状态，形式上学习 \(p(s_{t+1:t+H}\mid s_{\le t},a_{t:t+H-1})\) 或其观测/latent counterpart。模型既可服务特定 policy，也可作为通用环境模拟器；预测对象可以是单步状态、整段 video difference 或可渲染 3D scene。", r"Figure 1 用三行可视化代替长篇枚举：功能轴、时间轴、空间表示轴彼此独立，因此同一工作应被定位为三元组合，而不是只贴“video world model”标签。"),
            sec("模型与方法", r"第一轴区分 decision-coupled 与 general-purpose：前者贴近控制目标、sample efficient，但跨任务泛化弱；后者覆盖广，却可能与 downstream control misalign。第二轴区分 sequential simulation/inference 与 global difference prediction：前者闭环细致但误差逐步累积，后者并行高效但易抹平局部动力学。", r"第三轴分 global latent vector、token feature sequence、spatial latent grid、decomposed rendering representation。它们分别在 rollout speed、multimodal granularity、空间拓扑、几何可渲染性之间取舍。作者再以表格把代表作映射到数据、action conditioning、预测形式与任务。"),
            sec("核心结果与证据", r"Figure 1 的主要贡献是把领域从一条“模型规模更大”的线性谱系改写为三轴设计空间：例如 decision-coupled recurrent latent model 与 general-purpose global video model 即便都预测未来，也优化不同物理对象和控制延迟。", r"数据资源被分为 robotics manipulation/navigation、driving 和 general video；指标则至少分三层：PSNR/SSIM/FVD 等 pixel quality，object/state/geometry consistency，以及 planning/control success。综述强调高 pixel fidelity 不能保证 action-conditioned causal response 或长期物理一致。", r"作者归纳的共同瓶颈是 long-horizon error accumulation、统一数据稀缺、real-time compute、复杂交互与多模态 action grounding。最重要的评估建议是把 open-loop visual prediction 与 closed-loop task outcome 同时报出，并增加违反动力学约束的专门指标。"),
            sec("有效性与局限", r"综述的 quantitative tables 汇集不同 resolution、horizon、dataset split 和 protocol，数字不可直接排名；许多系统为闭源或只报告筛选视频。taxonomy 是作者的组织框架，不是唯一分类，且快速变化的领域可能产生跨轴混合模型。", r"文章主要覆盖视觉世界模型，触觉、语言交互、uncertainty calibration 和真实机器人安全评价较薄。它总结“需要 physical consistency metrics”，但没有提供经社区验证的统一量尺；因而不应把表格列数或 benchmark win 视为世界模型能力的充分证据。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2510.16732；维护列表：https://github.com/Li-Zn-H/AwesomeWorldModels。全文 24 页，PDF SHA-256：c6440fb0151ca584995f2d8eb76a5665f3ef0cc3eee18362dbf98e662dc9ed4b。", r"复核综述需记录检索截止日、纳入标准、每个工作的版本、数据 split、horizon、resolution、action space、是否 closed-loop、metric implementation 与代码/权重可用性。跨论文比较应先 protocol-normalize。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把任何目标模型写成三轴坐标；再读 data/metrics section，检查它究竟预测 pixels、states 还是 task return。随后按 robotics、driving、video 三张表追踪代表作，最后读 challenges，优先关注 long-horizon consistency 与 closed-loop evidence。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2510.16732/figure-1-world-model-taxonomy.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 3, Figure 1", "alt_text": "世界模型按功能、时间建模和空间表示三条轴分类，并配有代表性结构图。", "caption": "同一个具身世界模型应同时由 decision coupling、temporal prediction 和 spatial representation 三个坐标描述。", "selection_rationale": "Figure 1 是综述最重要的统一分类图，优先于密集比较表。"},
        "figure_refs": [figure("2510.16732", "figure-1-world-model-taxonomy.webp", "Figure 1", 3, "organize embodied world models along three independent axes", "Rows classify functionality, temporal modeling and spatial representation with representative methods.", "The taxonomy exposes different physical and computational tradeoffs hidden by a single world-model label.", "The map is a survey framework rather than an empirical ranking or exhaustive ontology.")],
        "equation_refs": [
            {"label": "Action-conditioned world dynamics", "latex": r"p_\theta(s_{t+1:t+H}\mid s_{\le t},a_{t:t+H-1})", "role": "state the predictive object shared by embodied world models", "symbols": {"s_t": "world or latent state", "a_t": "agent action", "H": "prediction horizon"}, "evidence": "paper.pdf pp. 2–3, background and problem formulation", "interpretation": "Different model families choose distinct state representations and factorisations of the same conditional rollout problem."},
            {"label": "Sequential factorization", "latex": r"p_\theta(s_{t+1:t+H}\mid\cdot)=\prod_{\tau=1}^{H}p_\theta(s_{t+\tau}\mid s_{\le t+\tau-1},a_{\le t+\tau-1})", "role": "contrast recurrent rollout with global prediction", "symbols": {"tau": "rollout step"}, "evidence": "paper.pdf p. 3, temporal-modeling taxonomy", "interpretation": "Fine-grained feedback comes with linearly growing latency and compounding model error."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: formal setting and three-axis taxonomy", "paper.pdf pp. 11–16: datasets, metrics and quantitative comparisons", "paper.pdf pp. 17–20: challenges and trends", "source PDF SHA-256 c6440fb0151ca584995f2d8eb76a5665f3ef0cc3eee18362dbf98e662dc9ed4b", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2510.25883", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2510.25883",
        "title_en": "The Information-Theoretic Imperative: Compression and the Epistemic Foundations of Intelligence",
        "title_zh": "信息论命令：压缩与智能的认识论基础",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["2fcf56099e45a899"], ["Information Theory"]),
        "verified_metadata": meta(
            "2510.25883", "v2",
            "The Information-Theoretic Imperative: Compression and the Epistemic Foundations of Intelligence",
            ["Christian Dittrich", "Jennifer Flygare Kinne"],
            ["cs.AI", "cs.IT"], "cs.AI", "2025-10-29T18:28:06Z",
            "The Compression Efficiency Principle proposes that recurrent distribution shifts impose a growing exception tax on shortcut representations and favor shift-stable invariants across biological and artificial systems.",
        ),
        "sections": [
            sec("作者信息", r"作者：Christian Dittrich、Jennifer Flygare Kinne；arXiv:2510.25883v2。全文 68 页。文章提出 Information-Theoretic Imperative（ITI）与 Compression Efficiency Principle（CEP），综合神经科学、深度学习与 MDL 证据，并给出可证伪实验协议；它是理论综述/研究纲领，不是已完成的大规模实验。"),
            sec("研究问题", r"任务优化网络能预测灵长类 ventral-stream responses，尽管生物与人工系统的基底、训练和资源完全不同。论文问：这种 representational convergence 是否来自一个 substrate-independent 约束？为什么 distribution shift 丰富时，稳定不变量会比依赖 shortcut 后不断打补丁的表示更优？"),
            sec("背景", r"CEP 把 predictive negative log-likelihood 视作 codelength，并比较 shift family \(\varepsilon\) 下的 excess codelength/regret。shortcut representation 在每个新环境中需要 exception patches，累计代价近似随环境多样性 \(E\) 线性增长；invariant representation 支付较高初始成本，但后续代价次线性或饱和。", r"Figure 1 把 biological wet substrate 与 artificial dry substrate 并列：代谢/布线选择与计算/目标优化都在丰富 shifts 下把系统推向 compression-efficient、shift-stable basin；两侧证据互补，但单侧都不能唯一确定机制。"),
            sec("模型与方法", r"作者用 MDL regret \(\Delta L_\varepsilon=L_\varepsilon(M)-L_\varepsilon(M^\star)\) 表示相对最优 predictor 的额外编码代价。简化模型令 shortcut cost \(L_{\rm short}(E)\approx L_0+c_{\rm patch}E\)，invariant cost \(L_{\rm inv}(E)\approx L_1+o(E)\)，交点 \(E^\star\) 给出从 patching 到 invariant compression 的 crossover。", r"因果性不是 CEP 的初始假设：只有当 environments 提供 intervention-rich shifts 且 causal mechanisms 近似 modular 时，shift-stable invariants 才预计与 causal factors 对齐。论文设计 shortcut-flipping、多环境 augmentation、active sensing 等 substrate-symmetric protocols，并预先说明 falsifiers。"),
            sec("核心结果与证据", r"Figure 1 的中心逻辑不是宣称 brain energy 与 GPU FLOPs 可直接换算，而是比较 trade-off frontier 的拓扑：两种基底都应出现 regret scaling separation、crossover 和 robustness–compression coupling。", r"CEP 的核心预测是 shortcut-flipping 下两类策略的累计 regret 分离：patching 近线性，invariant strategy 次线性；当 \(E>E^\star\) 后后者占优。另一个预测是同一 substrate/任务内，frontier-relative compression efficiency 与 OOD robustness 正相关，并随 shift family 改变所学 invariances。", r"文章列举 biological coding efficiency、代谢约束、ventral hierarchy tolerance，以及深网 scaling、augmentation 和 shortcut failures 作为一致性证据；但这些是多源相关/机制线索，尚未完成文中提出的统一 matched-protocol 检验。"),
            sec("有效性与局限", r"CEP 是可证伪框架而非从第一性物理推导出的唯一规律。representation convergence 也可能来自共享数据统计、任务几何、architecture bias 或 measurement alignment；Figure 1 明确承认 biological evidence 不能排除 substrate-specific explanation，artificial evidence 也不能单独确定约束机制。", r"codelength、metabolic energy、parameters 与 FLOPs 不可直接同量纲比较，必须在各 substrate 内做 frontier normalization。\(E\)、patch cost 和 invariant complexity 的操作化依赖实验设计；如果 shortcut-flipping 不产生稳健的 scaling separation，或 compression efficiency 与 OOD robustness 解耦，CEP 核心主张将受否定。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2510.25883。全文 68 页，PDF SHA-256：94d2a8c5b702d671ef1b8dd84da0c337547b5d6fae38a5490c6ab4ff54eff714。", r"实施建议从文中 shortcut-flipping protocol 开始：固定 invariant cue、逐环境翻转 shortcut cue，预注册 \(E\)、online codelength、update cost、OOD accuracy、representation similarity 和 crossover estimator；biological/artificial 结果只比较无量纲 frontier coordinates。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，注意双基底证据各自“不充分”的标注；再读 Sections 2–3 的 exception-tax 数学化与 causal caveat。随后直接读 Section 6 的 predictions/falsifiers，再回看神经科学和深度学习证据，区分解释框架、现有支持与尚未执行的关键实验。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2510.25883/figure-1-dual-substrate.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 8, Figure 1", "alt_text": "生物和人工系统在不同约束与 shift family 下汇聚到共享的稳定表示盆地。", "caption": "双基底证据支持共享 trade-off 拓扑，但任一侧单独都不足以确定压缩机制。", "selection_rationale": "Figure 1 是全文最重要的概念论证图，并显式展示证据边界。"},
        "figure_refs": [figure("2510.25883", "figure-1-dual-substrate.webp", "Figure 1", 8, "show the dual-substrate convergence argument", "Biological selection and artificial optimization are routed toward a shared basin of shift-stable representations.", "The framework compares trade-off topology rather than raw energy and compute units.", "The figure states that each substrate alone is insufficient to identify a universal mechanism.")],
        "equation_refs": [
            {"label": "Excess codelength under shift", "latex": r"\Delta L_\varepsilon(M)=L_\varepsilon(M)-L_\varepsilon(M^\star)", "role": "measure compression inefficiency relative to the best predictor", "symbols": {"epsilon": "environmental shift family", "M_star": "reference efficient model"}, "evidence": "paper.pdf pp. 11–14, Section 2", "interpretation": "CEP is operationalized through regret under recurring distribution changes, not raw model size alone."},
            {"label": "Exception-tax crossover", "latex": r"L_{\rm short}(E)\simeq L_0+c_{\rm patch}E,\qquad L_{\rm inv}(E)=L_1+o(E),\qquad L_{\rm short}(E^\star)=L_{\rm inv}(E^\star)", "role": "predict when invariant compression dominates shortcut patching", "symbols": {"E": "effective environment diversity", "E_star": "crossover richness"}, "evidence": "paper.pdf pp. 20–22, Figure 2 and CEP formalization", "interpretation": "Repeated shift-specific exceptions accumulate until the initially costlier invariant representation becomes cheaper."},
        ],
        "evidence_refs": ["paper.pdf pp. 8–15: dual-substrate argument and CEP quantities", "paper.pdf pp. 20–22: exception tax and crossover", "paper.pdf pp. 45–55: protocols, predictions and falsifiers", "source PDF SHA-256 94d2a8c5b702d671ef1b8dd84da0c337547b5d6fae38a5490c6ab4ff54eff714", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2512.01868", "source_version": "v4",
        "source_pdf": "https://arxiv.org/pdf/2512.01868",
        "title_en": "The Mean-Field Dynamics of Transformers",
        "title_zh": "Transformer 的均场动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["bc1bcd4f795ee4f1"], ["Transformer Theory"]),
        "verified_metadata": meta(
            "2512.01868", "v4", "The Mean-Field Dynamics of Transformers",
            ["Philippe Rigollet"], ["cs.LG", "math-ph", "math.DS", "math.PR"], "cs.LG", "2025-12-01T16:51:00Z",
            "Self-attention is modeled as an interacting particle flow on the sphere, yielding global clustering, metastable multi-cluster states, normalization-dependent contraction and a logarithmic long-context transition.",
        ),
        "sections": [
            sec("作者信息", r"作者：Philippe Rigollet；arXiv:2512.01868v4。全文 21 页。文章建立 pure self-attention 的 interacting-particle/mean-field 框架，综合 Wasserstein gradient flows、Kuramoto synchronization、mean-shift clustering 与近期聚类定理；它主要解释 attention dynamics，不是完整训练 Transformer 的端到端理论。"),
            sec("研究问题", r"深层 attention 常出现 token similarity 增大、rank/representation collapse，但有限层实验也保留多个语义 clusters。论文问：softmax attention 的连续深度极限为何产生聚类；多 cluster 为什么能长时间 metastable 后才合并；normalization 和 context length \(n\) 如何改变 contraction rate 与 collapse threshold？"),
            sec("背景", r"把每个 token \(x_i\in\mathbb S^{d-1}\) 看作球面粒子，attention weight 是 \(e^{\beta\langle x_i,x_j\rangle}\) 的归一化相互作用。Post-LN 被理想化为切空间投影，得到 Self-Attention（SA）flow；去掉归一化得到 USA。粒子数 \(n\to\infty\) 时经验测度满足 continuity equation。", r"ALBERT 的层间 pairwise-inner-product histogram 向 1 聚集，提供真实模型中的现象锚点；理论则研究理想化 attention-only flow 的长期极限。"),
            sec("模型与方法", r"SA velocity 将 weighted mean token 投影到 \(x_i\) 的切空间，保持单位球；对应一个 interaction energy 的 Wasserstein gradient ascent。\(d=2,\beta=0\) 退化到 Kuramoto synchronization，有限 \(\beta\) 与 mean-shift mode seeking 建立联系。", r"作者回顾 finite-particle 与 mean-field global clustering theorem，再分析 well-separated groups 的 metastability：组内先快速塌缩，cluster centers 在 \(T_2\) 前缓慢移动，且 \(\log T_2\sim\beta\)。equiangular ansatz 将多体流降成单一 cosine similarity \(\rho(t)\)，可得精确指数速率和 long-context threshold。"),
            sec("核心结果与证据", r"Figure 3 在 \(n=32\) 上给出 \((t,\beta)\) 聚类概率相图：从 \(d=8\) 到 128、1024，红蓝边界变尖并逼近 equiangular prediction。它说明高维 concentration 使随机 tokens 近乎等角，从而让一维降维具有预测力。", r"全局定理表明对 \(d\ge3\) 的一般初态，SA/USA 几乎必然最终集中到单 cluster；局部 hemisphere 条件下以显式指数速率收敛。低温大 \(\beta\) 下并不立即 collapse，而是能量 staircase：多 cluster plateaus 持续指数长时间后逐次合并。", r"normalization 改变速率而不简单消除聚类：equiangular model 中 USA rate \(\lambda_\beta=2e^\beta\) 随 \(\beta\) 爆增，SA rate 保持受控。long context 中若 \(\beta\) 固定，softmax 趋向 uniform mixing 并加速 collapse；临界 scaling \(\beta_n=\Theta(\log n)\) 才能维持 content-adaptive sparsity。"),
            sec("有效性与局限", r"模型省略 MLP、residual mixing、multi-head、learned Q/K/V、causal masks、positional encoding、训练和 finite-depth effects；因此 theorem 证明的是理想化 attention flow，不是任意实际 Transformer 必然 collapse。ALBERT histogram 是相关现象，不是对具体 ODE 的参数识别。", r"\(d=2\) 的部分 theorem 需要单独 Kuramoto 结果；noisy/an\-isotropic dynamics 与 uniform-in-time mean-field convergence 仍开放。多 cluster 在有限深网络中可能是有用表示，而 asymptotic single-cluster 结论不直接决定有限层性能。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2512.01868。全文 21 页，PDF SHA-256：8597f94eb8fb1b4655d255934276bb1f0bf1ca78053c78eed921c6975bb56df0。", r"复现 Figure 3 需固定 SA/USA convention、\(n=32\)、\(d=8,128,1024\)、\(\beta,t\) grid、random sphere initialization、ODE tolerance、cluster criterion \(\langle x_i,x_j\rangle\ge0.999\) 与 seed count。还应保存 energy staircase 和 \(\rho(t)\)，比较不同 normalization。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Sections 3–4，把 attention 写成球面粒子 flow，并看 ALBERT histogram；再读 global/local clustering theorems。随后看 Figure 2 的 metastable staircase 与 Figure 3 相图，最后读 normalization 和 \(\beta_n\sim\log n\) 的 long-context transition，并对照模型省略项。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2512.01868/figure-3-clustering-transition.webp", "label": "Figure 3", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 13, Figure 3", "alt_text": "不同维数下随机球面 tokens 的聚类概率随深度和 inverse temperature 的相图。", "caption": "高维时聚类边界变尖并逼近等角模型预测，揭示 context、temperature 与 representation collapse 的相变结构。", "selection_rationale": "Figure 3 是全文最重要的可视化相图，优先于单条能量曲线。"},
        "figure_refs": [figure("2512.01868", "figure-3-clustering-transition.webp", "Figure 3", 13, "show the high-dimensional clustering transition", "Heat maps display complete-clustering probability over depth and inverse temperature for increasing dimension.", "Concentration of measure sharpens the transition toward the equiangular mean-field prediction.", "The simulations use idealized attention-only dynamics with random spherical tokens.")],
        "equation_refs": [
            {"label": "Spherical self-attention flow", "latex": r"\dot x_i=P_{x_i}^{\perp}\!\left(\frac{\sum_j e^{\beta\langle x_i,x_j\rangle}x_j}{\sum_k e^{\beta\langle x_i,x_k\rangle}}\right)", "role": "model normalized attention as interacting particles", "symbols": {"P_x_perp": "projection onto the sphere tangent space", "beta": "inverse attention temperature"}, "evidence": "paper.pdf pp. 3–4, Eq. (SA)", "interpretation": "Each token moves toward its softmax-weighted neighbours while normalization keeps it on the sphere."},
            {"label": "Long-context critical scaling", "latex": r"\beta_n=\Theta(\log n)", "role": "separate uniform mixing from content-adaptive attention", "symbols": {"n": "context length"}, "evidence": "paper.pdf pp. 14–15, Theorem 7", "interpretation": "A fixed temperature becomes effectively too hot as context grows; logarithmic scaling preserves selective interactions."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: attention particle flows and clustering theorems", "paper.pdf pp. 8–13: metastability, equiangular rates and phase diagram", "paper.pdf pp. 13–17: normalization and long-context transition", "source PDF SHA-256 8597f94eb8fb1b4655d255934276bb1f0bf1ca78053c78eed921c6975bb56df0", "Evidence status: full-text verified; no independent reproduction performed."],
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
