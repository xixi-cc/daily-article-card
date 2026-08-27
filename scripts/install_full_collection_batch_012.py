#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 012."""

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
        "arxiv_id": "2404.09937", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2404.09937",
        "title_en": "Compression Represents Intelligence Linearly",
        "title_zh": "压缩能力与语言模型基准表现近似线性相关",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("fad8258cd8949414", "World Models"),
        "verified_metadata": meta(
            "2404.09937", "v2", "Compression Represents Intelligence Linearly",
            ["Yuzhen Huang", "Jinghan Zhang", "Zifei Shan", "Junxian He"],
            ["cs.CL", "cs.AI", "cs.IT", "cs.LG"], "cs.CL", "2024-04-15T17:03:41Z",
            "Across 31 public LLMs and 12 benchmarks, bits per character on recent external corpora is strongly linearly anticorrelated with average benchmark performance.",
        ),
        "sections": [
            sec("作者信息", r"作者：Yuzhen Huang、Jinghan Zhang、Zifei Shan、Junxian He；arXiv:2404.09937v2。全文 22 页，实验覆盖 31 个公开 base LLM、12 个 benchmark 与 knowledge/code/math 三类外部语料。"),
            sec("研究问题", r"语言模型的 next-token likelihood 同时定义预测误差与理想码长。论文问：不构造标注题库，只测模型对最新原始文本的压缩效率，能否预测其 knowledge、coding 与 mathematical reasoning benchmark 平均分？这里的“intelligence”严格只是这些平均分的代理量，不是一般智能的操作定义。"),
            sec("背景", r"对语料 \(X=(x_1,\ldots,x_N)\)，理想码长是 \(-\log_2p_{\rm model}(X)\)。不同 tokenizer 的 bits per token 不可直接比，故作者除以字符数 \(T\) 得到 BPC。为避免长 context 额外占优，所有模型统一在 1900-token context 下评估。", r"压缩语料取实验时最新的 Common Crawl、GitHub Python code 与 arXiv math papers，分别匹配 knowledge/common sense、coding 与 math benchmarks；另用 MIN-K% PROB 检查 benchmark contamination，主实验取 \(k=20\%\)。"),
            sec("模型与方法", r"作者对 9 个 general-purpose model series 以及 specialized code/math models统一运行 benchmark 与 sliding-window likelihood。每个模型是散点，用 Pearson \(\rho\) 衡量 benchmark score 与 BPC 的相关性，并做线性回归，以 RMSE \(e\) 表示偏离直线的典型幅度。", r"总体分数是三个领域平均 benchmark score，总体 BPC 是三类 corpus BPC 的平均。该设计让 compression 成为无监督观测量，但 model family、训练语料、参数量和 tokenizer 仍是共同变化的隐变量。"),
            sec("核心结果与证据", r"Figure 1 给出核心结果：31 个模型的总体分数与平均 BPC 近似线性反相关，\(\rho=-0.931\)，线性拟合 RMSE \(e=0.031\)。三个分领域面板也分别得到 \(-0.935\)、\(-0.937\) 和 \(-0.953\) 的 Pearson correlation。", r"图的物理读法是：BPC 越小，模型给外部文本的 cross entropy 越低；在该模型集合内，这一单一无监督量沿着与 benchmark 能力相近的一维方向变化。作者还显示若 corpus 与任务领域错配，相关性变弱；不同抽样大小的 BPC 会收敛，但小 corpus 噪声更大。", r"MIN-K% 检查没有给出普遍污染信号，但对个别数学模型出现异常分布；论文因此把这些点解释为可能的 overfitting/contamination，而不是压缩—能力关系的反例。"),
            sec("有效性与局限", r"这是跨模型相关性，不是因果实验：更大训练量、更强 architecture 或更好 data 同时改善 BPC 与 benchmark，不能据此断言“训练压缩必然产生智能”。样本由 31 个公开 base models 构成，许多点属于同一 model family，独立性弱于 31 个完全独立系统。", r"结论只覆盖 1900-token 短/中 context、三类英文语料与 12 个 benchmarks。benchmark average、corpus recency、tokenizer normalization 和 MIN-K% 本身都有识别误差；BPC 不能替代 reasoning reliability、factuality、safety 或长上下文能力。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2404.09937；代码与数据：https://github.com/hkust-nlp/llm-compression-intelligence。全文 22 页，PDF SHA-256：bce3546c70d58f704ea52bc42ae1cc5cbc8c4b37c59ee68c83b37d62037d62df。", r"复现需固定 model/tokenizer revision、1900-token window、sliding stride、corpus snapshot 与字符计数规则，并同时保存每模型的 raw BPC、benchmark scores、family label、linear-fit residual 和 MIN-K% distributions。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Eq. (2) 与 Section 3.2，确认 BPC 的 tokenizer-normalized 定义；再看 Figure 1 的总体与三领域斜率。随后读 Section 3.3 和 Figure 5 检查 contamination，最后读 Appendix D–E，判断 corpus choice、sample size 和 instruction tuning 会怎样破坏这条经验直线。"),
        ],
        "cover": {
            "mode": "source_figure", "asset_path": "assets/collection-figures/2404.09937/figure-1-compression-intelligence.webp",
            "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 1, Figure 1",
            "alt_text": "31 个公开语言模型的平均 benchmark 分数与 bits per character 的总体及分领域散点和线性拟合。",
            "caption": r"模型在外部语料上的 BPC 越低，12 项 benchmark 的平均分越高；总体相关系数为 \(\rho=-0.931\)。",
            "selection_rationale": "文章没有机制示意图；Figure 1 集中呈现主假设、全体模型和三个分领域的定量证据。",
        },
        "figure_refs": [figure("2404.09937", "figure-1-compression-intelligence.webp", "Figure 1", 1, "show the empirical compression–benchmark relation", "总体与三个领域的 BPC–score 散点及线性拟合。", r"总体 \(\rho=-0.931\)，三个分领域均约为 \(-0.94\) 到 \(-0.95\)。", "Correlation across related model families does not identify compression as the causal source of capability.")],
        "equation_refs": [
            {"label": "Bits per character", "latex": r"\mathrm{BPC}=-\frac{\log_2p_{\rm model}(X)}{T}=\frac{1}{T}\sum_{i=1}^{N}-\log_2p_{\rm model}(x_i\mid x_{<i})", "role": "compare compression across tokenizers", "symbols": {"X": "external corpus", "N": "number of model tokens", "T": "number of characters"}, "evidence": "paper.pdf p. 4, Eq. (2)", "interpretation": "Character normalization removes the most direct tokenizer-length confound."},
            {"label": "Linear empirical relation", "latex": r"\bar s \simeq a+b\,\overline{\mathrm{BPC}},\qquad \rho(\bar s,\overline{\mathrm{BPC}})=-0.931", "role": "summarize the fitted cross-model relation", "symbols": {"s_bar": "average benchmark score", "BPC_bar": "average over the three corpora", "rho": "Pearson correlation"}, "evidence": "paper.pdf p. 1 and pp. 6–7, Figure 1", "interpretation": "The fit is predictive within the sampled model population, not a mechanistic law."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: BPC protocol and main correlations", "paper.pdf pp. 7–11: domain results, contamination and ablations", "source PDF SHA-256 bce3546c70d58f704ea52bc42ae1cc5cbc8c4b37c59ee68c83b37d62037d62df", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2405.00751", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2405.00751",
        "title_en": "F³low: Frame-to-Frame Coarse-grained Molecular Dynamics with SE(3) Guided Flow Matching",
        "title_zh": "F³low：以 SE(3) 引导流匹配实现逐帧粗粒化分子动力学",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("d45bc2d69a4c687d", "Flow Matching"),
        "verified_metadata": meta("2405.00751", "v1", "F³low: Frame-to-Frame Coarse-grained Molecular Dynamics with SE(3) Guided Flow Matching", ["Shaoning Li", "Yusong Wang", "Mingyu Li", "Jian Zhang", "Bin Shao", "Nanning Zheng", "Jian Tang"], ["q-bio.QM", "cs.AI", "cs.LG"], "q-bio.QM", "2024-05-01T04:53:14Z", "A force-free autoregressive SE(3) flow model samples the next coarse-grained protein backbone frame conditioned on the previous frame."),
        "sections": [
            sec("作者信息", r"作者：Shaoning Li、Yusong Wang、Mingyu Li、Jian Zhang、Bin Shao、Nanning Zheng、Jian Tang；arXiv:2405.00751v1。全文 12 页，GEM workshop at ICLR 2024。"),
            sec("研究问题", r"传统 coarse-grained MD 学习 energy 或 force，再逐时间步积分；误差会沿长轨迹累积，而且只保留 \(C_\alpha\) 时须重建 backbone。论文问：能否直接学习条件转移 \(C_s\mapsto C_{s+1}\)，在 \(SE(3)^N\) 上逐帧生成四原子 backbone，从而绕开显式 force calculation 并扩大构象空间探索？"),
            sec("背景", r"每个 residue 由 rigid frame \(T_i\in SE(3)\) 表示，蛋白构象 \(C=[T_1,\ldots,T_N]\in SE(3)^N\)。平移限制在 zero-center-of-mass subspace，旋转 prior 取 isotropic Gaussian on \(SO(3)\)，使输入分布保持 \(SE(3)\)-invariant、vector field 保持 equivariant。", r"相邻 MD 帧来自同一 Boltzmann distribution，不能简单当作两个独立端点分布做普通 flow matching。F³low 改为从 normal prior 采样下一帧，并用前一帧 \(C_s\) 作为 guidance。"),
            sec("模型与方法", r"模型学习 \(C_{s+1}\sim P_\theta(C_{s+1};z,C_s)\)，再自回归重复 \(S\) 次形成 trajectory。前帧通过 initial-guess interpolation 注入：translation 用 \((1-\gamma)\mathrm{OT}(z^x,x_1)+\gamma x_0\)，rotation 用 exponential/log maps；实验取 \(\gamma=0.5\)、guidance weight 1。", r"网络采用 FramePred 与 invariant point attention，输入是四个 backbone heavy atoms \(C-C_\alpha-N-O\)。三种 fast-folding proteins 分别为 Chignolin 10AA、Trpcage 20AA、Homeodomain 54AA；每篇训练单卡 RTX 4090，采样 8 条并行轨迹、每条 150,000 frames，去掉前 10%。"),
            sec("核心结果与证据", r"Figure 1 对比两种动力学：传统 CGMD 先由 energy gradient 得到 bead forces 再积分；F³low 则以前一 frame 为条件，从 prior 直接采下一 frame。图同时显示模型把表示从 \(C_\alpha\) beads 提升到完整 backbone frames。", r"在 TICA/MSM reweighted free-energy surfaces 上，F³low 覆盖 Chignolin 与 Trpcage 的主要 basin；对 Homeodomain，CG-MLFF 快速困在 native region，而 F³low 用 8 个起点比对方 32 个起点探索更广的 unfolded regions。", r"Table 1 的最低 RMSD（Å）显示 F³low 相对 CG-MLFF 更接近 crystal：Chignolin backbone 0.36 vs 0.89，Trpcage 0.62 vs 2.41，Homeodomain 0.53 vs 2.11；其数值也接近 reference MD 的 0.27、0.58、0.54。"),
            sec("有效性与局限", r"模型生成的是学习到的 transition kernel，不是由已知 Hamiltonian 积分得到的物理时间演化；论文没有证明 detailed balance、正确动力学时间尺度或 equilibrium stationary distribution。free-energy surfaces 又由 reference-derived TICA coordinates 与 MSM reweighting 构造。", r"只评估 3 个 fast-folding proteins，训练与采样都依赖同一大型 MD dataset；最低 RMSD 是极值统计，会随 1.2 million samples 增加而改善。作者也明确指出 \(SO(3)\) guided-flow 理论证明尚留作未来工作。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2405.00751。全文 12 页，PDF SHA-256：1e80410c57931a3281a7d5dc90c2e3f3f03e06faa7011cd9a847335e500a66e6。", r"复现需固定 MD trajectory split、4-atom frame construction、OT matching、\(\gamma=0.5\)、network checkpoint、sampling integrator、8×150k frames、TICA lag/components、MSM/PCCA parameters 与 RMSD atom selection。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 分清 force integration 与 learned transition sampling；再读 Section 2.1 的 \(SE(3)\) flow 与 Eqs. (6)–(7) 的前帧 guidance。随后看 Figure 2 和 Table 1，但把 free-energy coverage、minimum RMSD 与真实 kinetics 三种论断严格分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2405.00751/figure-1-frame-to-frame-flow.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "传统 CGMD 的 force integration 与 F³low 在 SE(3) backbone frames 间逐帧生成的对比示意图。", "caption": r"F³low 不显式计算力，而是在 \(SE(3)^N\) 上以前一构象为 guidance 直接采样下一 frame。", "selection_rationale": "Figure 1 是全文最重要的机制图，清楚替代了对 force-free、backbone-level 和 autoregressive 三点的长篇文字描述。"},
        "figure_refs": [figure("2405.00751", "figure-1-frame-to-frame-flow.webp", "Figure 1", 2, "contrast force-based CGMD with frame-to-frame generative sampling", "从 unfolded 到 folded 的传统 force pipeline 和 F³low backbone-frame transition。", "该方法把显式力积分换成 learned conditional transition kernel。", "The generated frame index is not automatically a calibrated physical time coordinate.")],
        "equation_refs": [
            {"label": "Frame-to-frame transition", "latex": r"C_{s+1}\sim P_\theta(C_{s+1};z,C_s),\qquad C_s\in SE(3)^N", "role": "define autoregressive coarse-grained simulation", "symbols": {"C_s": "previous backbone conformation", "z": "normal prior", "N": "number of residues"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "Repeated conditional sampling generates a trajectory without explicit forces."},
            {"label": "Previous-frame guidance", "latex": r"\tilde x_0=(1-\gamma)\operatorname{OT}(z^x,x_1)+\gamma x_0,\qquad \gamma=0.5", "role": "inject the former conformation into the flow source", "symbols": {"x0": "previous-frame translations", "x1": "target-frame translations", "gamma": "initial-guess weight"}, "evidence": "paper.pdf p. 4, Eqs. (6)–(7)", "interpretation": "The source remains stochastic while retaining geometric memory of the previous frame."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: SE(3) frame-to-frame flow and guidance", "paper.pdf pp. 4–7: free-energy surfaces, RMSD and trajectories", "source PDF SHA-256 1e80410c57931a3281a7d5dc90c2e3f3f03e06faa7011cd9a847335e500a66e6", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2405.05621", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2405.05621",
        "title_en": "Enhancing (quasi-)long-range order in a two-dimensional driven crystal",
        "title_zh": "在二维驱动晶体中增强（准）长程有序",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("c31017887f2c476d", "Condensed Matter"),
        "verified_metadata": meta("2405.05621", "v2", "Enhancing (quasi-)long-range order in a two-dimensional driven crystal", ["R. Maire", "A. Plati"], ["cond-mat.soft", "cond-mat.stat-mech"], "cond-mat.soft", "2024-05-09T08:37:34Z", "A harmonic theory and driven hard-disk simulations show that long-wavelength phonons thermalize to the center-of-mass bath temperature, enabling tunable enhancement of two-dimensional translational order."),
        "sections": [
            sec("作者信息", r"作者：R. Maire、A. Plati；arXiv:2405.05621v2。全文 18 页，包含 harmonic-crystal 解析理论与 active hard-disk event-driven simulations。"),
            sec("研究问题", r"平衡二维晶体受 Hohenberg–Mermin–Wagner 长波涨落限制，只能有 translational quasi-long-range order。若局域驱动保动量、全局热浴又给所有 mode 加噪，是否仍能把低 \(k\) phonons 冷却到独立于总 kinetic temperature 的尺度，从而任意增强准长程有序？"),
            sec("背景", r"模型把 phonon mode 同时耦合到 global bath \((T_{\rm com},\gamma_{\rm com})\) 与 momentum-conserving local bath \((T_{\rm loc},\gamma_{\rm loc}k^2)\)。因为局域浴的 damping/noise 随 \(k^2\) 消失，\(k\to0\) 的有效温度由 global/center-of-mass bath 控制，而短波可保持在另一温度。", r"这把通常单一温度的 equipartition 改成 scale-dependent \(T_k\)。当 \(T_{\rm com}=0\) 时，长波 density modes 被压低并出现 \(S(k)\sim k^2\) hyperuniformity；非零 \(T_{\rm com}\) 恢复 quasi-long-range order，但 exponent 可由驱动和耗散连续调节。"),
            sec("模型与方法", r"理论从二维 harmonic lattice 的 Fourier modes 推导静态 velocity/displacement correlators、structure factor、relative displacement 与 translational correlation。大尺度 MSD 系数 \(\kappa\) 与 \(T_{\rm com}/K\) 成正比，\(K\) 是 elastic modulus；因此真正控制长程有序的是 center-of-mass temperature，而非总 kinetic temperature。", r"数值系统为 packing fraction 约 0.75 的 hard disks：free flight 中受 global white bath 与 damping，碰撞按 restitution \(\alpha\) 和 injection \(\Delta\) 的 momentum-conserving active rule。改变 \(\Delta,\alpha,\gamma_{\rm com},T_{\rm com}\)，测 \(S(k)\)、static velocity factor、long-time MSD plateau 和 translational correlation \(g_G(r)\)。"),
            sec("核心结果与证据", r"Figure 2 并排显示三种 \(T_{\rm com}=0\) 系统。平衡 hard disks 的 \(S(k\to0)\) 有限、MSD 随 \(N\) 对数增长、\(g_G(r)\) 幂律衰减；只有 active collisions 时出现 crossover；再加入 global damping 后，\(S(k)\sim k^2\)、MSD 在大 \(N\) 饱和、\(g_G(r)\) 趋于常数，三种观测共同指向 true long-range translational order。", r"理论给出 \(\mathrm{MSD}_{T_{\rm com}}(t\to\infty)=\kappa(T_{\rm com})\log N\) 且 \(\kappa\sim T_{\rm com}/K\)。对 active hard disks，近似 \(K(T)\propto T\)，于是 \(\kappa\sim T_{\rm com}/T\)：即使 global noise amplitude 固定，也可通过提高 driven steady-state temperature \(T\) 任意减小长波涨落。", r"Appendix Figure 4 进一步显示降低 \(T_{\rm com}\) 会压低 \(S(k\to0)\) plateau 并减弱 \(g_G(r)\) 的幂律衰减；\(T_{\rm com}\to0\) 时恢复 \(k^2\) scaling 与长程有序。"),
            sec("有效性与局限", r"HMW theorem 的规避依赖非平衡、动量守恒噪声与 global damping 的特殊尺度结构；这不是平衡定理的反例。harmonic theory 忽略 defects、dislocations 与 nonlinear elasticity，hard-disk crystal 又需保持在稳定晶相。", r"active collision 的有效 local temperature 其实依赖 \(\alpha,\Delta,T_{\rm com},\gamma_{\rm com}\) 等全部参数，不能视作完全独立 bath。所谓“任意增强”是在模型和稳定相范围内调小 \(\kappa\)，并不证明实验系统能无限提高有序度而无 melting、finite-size 或 dissipation constraints。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2405.05621。全文 18 页，PDF SHA-256：db68f976161feaec9039c1a942e51381c2fb54ed27a96d9f1d5b7d74e0f2f374。", r"复现需固定 packing fraction、\(N\)、event-driven/time-step hybrid integrator、\(\alpha,\Delta,\gamma_{\rm com},T_{\rm com}\)、COM convention、wave-vector bins 与 finite-size fit。应同步保存 \(S(k)\)、velocity factor、MSD plateau 和 \(g_G(r)\)，避免用单一 observable 判断长程有序。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Section II 的 mode-dependent temperature，再看 Figure 2：三列分别是同一长波物理的 reciprocal-space、finite-size 和 real-space 投影。随后读 Eqs. (25)–(28) 区分 \(T_{\rm com}\) 与 \(T\)，最后读 Appendix G–H 检查 active bath 的非平衡修正。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2405.05621/figure-2-long-range-order.webp", "label": "Figure 2", "visual_type": "data_plot", "evidence": "paper.pdf p. 8, Figure 2", "alt_text": "三种二维晶体的结构因子、长时 MSD 随粒子数和 translational correlation 对比。", "caption": r"当 \(T_{\rm com}=0\) 且 active collisions 配合 global damping 时，\(S(k)\sim k^2\)、MSD 饱和、\(g_G(r)\) 趋于常数。", "selection_rationale": "文章没有清晰机制示意图；Figure 2 用三个互相校验的 observable 直接展示长程有序，是最重要的证据图。"},
        "figure_refs": [figure("2405.05621", "figure-2-long-range-order.webp", "Figure 2", 8, "cross-check long-range order in reciprocal, finite-size, and real-space observables", "结构因子、MSD plateau 与 translational correlation 三联图。", r"\(k^2\) hyperuniformity、MSD saturation 和 correlation plateau 是同一低波数 suppression 的三种表现。", "The result is for T_com=0 and a stable driven crystalline regime.")],
        "equation_refs": [
            {"label": "Long-wavelength effective temperature", "latex": r"T_k=\frac{\gamma_{\rm com}T_{\rm com}+\gamma_{\rm loc}k^2T_{\rm loc}}{\gamma_{\rm com}+\gamma_{\rm loc}k^2},\qquad \lim_{k\to0}T_k=T_{\rm com}", "role": "identify which bath controls infrared phonons", "symbols": {"T_com": "global center-of-mass bath temperature", "T_loc": "momentum-conserving local-bath temperature", "k": "wave number"}, "evidence": "paper.pdf pp. 3–4, Eqs. (10)–(13)", "interpretation": "Local momentum-conserving noise decouples quadratically in the infrared."},
            {"label": "Finite-size displacement growth", "latex": r"\mathrm{MSD}(t\to\infty)=\kappa(T_{\rm com})\log N,\qquad \kappa\sim\frac{T_{\rm com}}{K}\sim\frac{T_{\rm com}}{T}", "role": "connect COM temperature to quasi-long-range-order exponent", "symbols": {"N": "particle number", "K": "elastic modulus", "T": "steady-state kinetic temperature"}, "evidence": "paper.pdf p. 8, Eqs. (25)–(28)", "interpretation": "Driving can raise T and stiffness without proportionally heating the infrared COM mode."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: harmonic theory and infrared temperature", "paper.pdf pp. 6–10: active hard-disk simulations and finite-size scaling", "source PDF SHA-256 db68f976161feaec9039c1a942e51381c2fb54ed27a96d9f1d5b7d74e0f2f374", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2405.06008", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2405.06008",
        "title_en": "Wilsonian Renormalization of Neural Network Gaussian Processes",
        "title_zh": "神经网络高斯过程的 Wilson 型重整化",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("a88b9bb69dd7ec7c", "Renormalization Group"),
        "verified_metadata": meta("2405.06008", "v3", "Wilsonian Renormalization of Neural Network Gaussian Processes", ["Jessica N. Howard", "Ro Jefferson", "Anindita Maiti", "Zohar Ringel"], ["cs.LG", "cond-mat.dis-nn", "hep-th", "stat.ML"], "cs.LG", "2024-05-09T18:00:00Z", "Integrating out unlearnable Gaussian-process kernel modes produces a Wilsonian flow whose infrared scale is set by dataset size."),
        "sections": [
            sec("作者信息", r"作者：Jessica N. Howard、Ro Jefferson、Anindita Maiti、Zohar Ringel；arXiv:2405.06008v3。全文 45 页，把 GP regression 的 kernel eigenmodes 当作 Wilsonian degrees of freedom。"),
            sec("研究问题", r"深度网络 scaling law 常被类比为 RG，但“scale”与“integrate out”往往没有精确定义。论文问：在可解析的 Gaussian-process limit 中，能否按 kernel learnability 排序，显式积分掉数据无法约束的 modes，并写出对剩余 predictor 有相同低模统计的 effective action？"),
            sec("背景", r"kernel eigenfunctions \(\phi_k(x)\) 与 eigenvalues \(\lambda_k\) 提供 feature-space momentum basis。对平均样本数 \(\eta\) 和 ridge/noise \(\sigma^2\)，mode predictor 为 \(\bar f_k=\lambda_k y_k/(\lambda_k+\sigma^2/\eta)\)；当 \(\lambda_k\ll\sigma^2/\eta\) 时，该 mode 几乎不从数据学习。", r"因此 dataset size 设定 infrared resolution：增大 \(\eta\) 会使更多小-\(\lambda_k\) modes 跨过 learnability threshold。Wilsonian cutoff \(\kappa\) 不按空间波长，而按 kernel spectrum 把 \(k>\kappa\) 的高序号、低 eigenvalue modes 积掉。"),
            sec("模型与方法", r"作者用 replica formulation 对 Poisson-distributed training sets 做 dataset average，将 GP action 分成 \(f_<\) 与 \(f_>\)。若 feature distribution \(P[\phi]\) 为 Gaussian，逐 shell 积分只 renormalize ridge：\(\sigma_c^2=\sigma^2+c\)，其中 \(c\) 是已积分 eigenvalues 的累计 variance。", r"若 \(P[\phi]\) 有小的 non-Gaussian cumulants，RG 会生成 input-dependent ridge/noise，等价于对 data measure 做空间重加权。MNIST/CIFAR10 用 NNGP kernels 验证 feature-mode joint distributions 在可学习区近似 Gaussian，并用 threshold \(\mathcal L_k\approx T\) 确定 cutoff。"),
            sec("核心结果与证据", r"Figure 2 展示 MNIST 与 CIFAR10 不同分类任务的两对 feature modes：二维散点与两个 marginals 均接近 Gaussian。它解释了为何最简 RG flow 在真实数据的低阶 modes 上可用，而不是只把 Gaussianity 当作形式假设。", r"Gaussian flow 的 universal result 是 \(\sigma_c^2=\sigma^2+c\)：被积掉的 unlearnable modes 不消失为零，而是作为额外 ridge/noise 反馈到剩余 modes。停止点由 \(\lambda_\kappa\sim\sigma_c^2/\eta\) 或 learnability factor \(\mathcal L_\kappa=T\) 确定。", r"若 spectrum \(\lambda_k\propto k^{-(1+\alpha)}\) 且 target 与 GP matched，论文恢复 data scaling exponent \(\alpha_D=\alpha/(1+\alpha)\)，并在 MNIST/CIFAR10 的 MSE-vs-\(\eta\) 上得到与 empirical curves 相符的趋势；高-\(k\) non-Gaussianity 则造成纯 Gaussian prediction 漏掉的定性修正。"),
            sec("有效性与局限", r"严格可解部分属于 GP/NNGP 与 replica/dataset-average framework，不包含有限宽网络的 feature learning。Gaussian feature assumption 对低 modes 较好，但 Appendix 显示高 \(k\) 可出现 heavy-tailed/Cauchy-like deviations，恰是 cutoff 接近数据分辨率时最敏感的区域。", r"cutoff 依赖人为 threshold \(T\)，有限 \(\eta\) 下 Taylor/replica approximations 和 kernel eigensystem 的数值估计都有误差。MNIST/CIFAR10 是回归化分类任务；由此得到的 universality class 尚不能直接推广到现代训练中的 optimizer、representation drift 与 nonstationarity。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2405.06008。全文 45 页，PDF SHA-256：1e4f23fd1d5212cfc7aada9b0e548279f70ec49acc8f82bf9614001c7fd67a04。", r"复现需固定 NNGP architecture/kernel、dataset preprocessing、task pair、kernel eigensolver、sample-size grid、ridge \(\sigma^2\)、threshold \(T\)、replica truncation 与 feature-mode normality test，并分别报告 Gaussian 与 non-Gaussian flow。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Eqs. (10)–(12) 看 mode learnability，再读 Sections III–IV 的 shell integration 与 scaling exponent。Figure 2 用来检验 Gaussian premise；最后读 Section V 和 Appendix F，理解 high-mode non-Gaussianity 如何把常数 ridge 变成 input-dependent coupling。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2405.06008/figure-2-gaussian-feature-modes.webp", "label": "Figure 2", "visual_type": "distribution", "evidence": "paper.pdf p. 19, Figure 2", "alt_text": "MNIST 与 CIFAR10 四组 kernel feature-mode 联合分布及 Gaussian marginal fits。", "caption": "真实数据的低阶 feature modes 近似联合 Gaussian，使只 renormalize ridge 的最简 Wilsonian flow 有经验依据。", "selection_rationale": "文章没有机制示意图；Figure 2 最直观地展示核心近似的经验基础，优先于单一 loss scaling 曲线。"},
        "figure_refs": [figure("2405.06008", "figure-2-gaussian-feature-modes.webp", "Figure 2", 19, "test the Gaussian feature premise on real datasets", "MNIST/CIFAR10 feature-mode scatter plots and marginal Gaussian fits。", "低阶 modes 的近 Gaussianity 支持 universal ridge flow；高阶 modes 的偏离限制其适用域。", "Visual Gaussianity is illustrative and does not prove all modes or datasets are Gaussian.")],
        "equation_refs": [
            {"label": "Mode learnability", "latex": r"\bar f_k=\frac{\lambda_k}{\lambda_k+\sigma^2/\eta}y_k,\qquad \mathcal L_k=\frac{\eta\lambda_k}{\sigma^2+\eta\lambda_k}", "role": "separate learnable and unlearnable kernel modes", "symbols": {"lambda_k": "kernel eigenvalue", "eta": "mean dataset size", "sigma2": "ridge/noise parameter"}, "evidence": "paper.pdf p. 7, Eq. (11), and p. 17, Eq. (37)", "interpretation": "Modes below the data-dependent spectral resolution contribute mostly as uncertainty."},
            {"label": "Gaussian Wilsonian flow", "latex": r"\sigma_c^2=\sigma^2+c,\qquad c=\sum_{k>\kappa}\lambda_k", "role": "encode integrated unlearnable modes as a renormalized ridge", "symbols": {"kappa": "spectral cutoff", "c": "cumulative variance of eliminated modes", "sigma_c2": "effective ridge"}, "evidence": "paper.pdf p. 14, Eqs. (33)–(34)", "interpretation": "Eliminated modes feed back universally as additional effective noise in the Gaussian case."},
        ],
        "evidence_refs": ["paper.pdf pp. 6–14: feature-space action and Gaussian shell RG", "paper.pdf pp. 15–24: scaling laws, real-data modes and non-Gaussian corrections", "source PDF SHA-256 1e4f23fd1d5212cfc7aada9b0e548279f70ec49acc8f82bf9614001c7fd67a04", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2405.17538", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2405.17538",
        "title_en": "Bayesian RG Flow in Neural Network Field Theories",
        "title_zh": "神经网络场论中的贝叶斯重整化群流",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("b6ca098cb4d12fdb", "Renormalization Group"),
        "verified_metadata": meta("2405.17538", "v3", "Bayesian RG Flow in Neural Network Field Theories", ["Jessica N. Howard", "Marc S. Klinger", "Anindita Maiti", "Alexander G. Stapleton"], ["hep-th", "cond-mat.dis-nn", "cs.LG"], "hep-th", "2024-05-27T18:00:00Z", "Neural-network field theory is combined with Fisher-information Bayesian coarse graining to define flows through statistical field theories."),
        "sections": [
            sec("作者信息", r"作者：Jessica N. Howard、Marc S. Klinger、Anindita Maiti、Alexander G. Stapleton；arXiv:2405.17538v3。全文 41 页，提出 BRG–NNFT correspondence，并给出解析与数值 proof of concept。"),
            sec("研究问题", r"NNFT 把随机神经网络 ensemble 映到 statistical field theory；Bayesian RG（BRG）按 Fisher metric 在 parameter space 中丢弃不可区分方向。论文问：这两张映射能否交换，即先 coarse-grain 参数再做 NNFT，和先得到场论再沿 induced flow coarse-grain，是否给出同一族 \(S_\Lambda[\phi]\)？"),
            sec("背景", r"Fisher information \(I_{AB}\) 把模型参数方向分成 stiff 与 sloppy：大的 eigenvalue 意味着输出分布对该方向敏感，小 eigenvalue 意味着许多参数值在给定精度下不可区分。cutoff \(\Lambda\) 因而不是默认的 momentum，而是 information-geometric distinguishability scale。", r"NNFT 映射 \((\phi_\theta,\pi)\mapsto S[\phi]\)，使无限 ensemble 的 output correlators 等于 Euclidean SFT correlators。BRG 映射 \(\pi\mapsto\pi_\Lambda\)；两者复合生成 \(S_\Lambda[\phi]\)。若 Fisher cutoff 恰与 momentum cutoff 对齐，才恢复通常的 ERG。"),
            sec("模型与方法", r"在 MAP 附近按 Fisher diagonal/eigenmodes 划分 \(\lambda_A<\Lambda\) 与 \(\lambda_A\ge\Lambda\)。精确 prescription 对 sloppy subspace marginalize，再赋予 information-invariant Jeffreys prior；数值实现则保留 stiff parameters，把 sloppy parameters 从原 prior 重采样。", r"解析部分处理 arbitrary-depth infinite-width networks 与 Gaussian likelihood，其 predictive distribution 保持 Gaussian random process。special generalized cos-net 的 NNFT dual 是带 UV cutoff \(R\) 的 free scalar field，BRG 改变 effective variance，等价于 momentum-shell ERG。数值部分训练 asymptotically wide ReLU network ensemble，再逐 cutoff 重采样 sloppy directions。"),
            sec("核心结果与证据", r"Figure 2 是全文的交换图：上边是 NNFT，左边先对网络参数做 BRG，右边是 induced field-theory BRG；下边把 \((\phi_\theta,\pi_\Lambda)\) 映到 \(S_\Lambda[\phi]\)。它说明框架的主命题不是“网络像场论”，而是两种 coarse-graining composition 的一致性。", r"对 generalized cos-net，单一 effective-variance flow 同时 renormalize free scalar 的 mass 与 momenta/field normalization，并把 architecture scale \(R\) 解释为 UV cutoff；这是 BRG 与 Wilson momentum-shell ERG 精确重合的特殊例子。", r"数值 ensemble 中，平均 MSE 在 critical cutoff \(\Lambda_C\) 前几乎不变，尽管许多 sloppy directions 已被重采样；越过 \(\Lambda_C\) 后 loss 与 predictive variance 陡增。这支持 Fisher spectrum 确实区分了对 performance 不敏感与敏感的参数方向。"),
            sec("有效性与局限", r"解析 correspondence 依赖 infinite width、Gaussian random process、Gaussian data/L2 loss 等强条件；free-scalar momentum-shell 等价只在 generalized cos-net 的特殊 architecture 成立。一般网络中 Fisher scale 不等于 spatial momentum，所谓 RG 是 information-space coarse graining。", r"数值实验使用 diagonal Fisher proxy、有限 ensemble 与 asymptotically wide toy network；重采样 prior 也不同于精确 Jeffreys-prior prescription。Fisher metric 的 parameterization、MAP choice 和计算成本会影响 sloppy/stiff split，尚未证明能改善现代大模型的压缩、泛化或解释性。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2405.17538。全文 41 页，PDF SHA-256：7fcf4b1ff545459ed73f84748993bb981910e277c53bd7549f94074bbf9bf14e。", r"复现需固定 architecture/width、prior、training data、loss、ensemble size、MAP/terminal checkpoint、Fisher estimator、diagonalization convention、cutoff grid、sloppy resampling seed，以及每个 \(\Lambda\) 下的 mean/covariance 与 MSE。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 2 并逐边核对两个 map；再读 Section 3.2 的 Fisher cutoff 与 Eq. (54)。随后读 Section 4.1.1 的 cos-net/free-field special case，最后看 Figures 9–11，把“critical information scale”的数值证据与一般大模型主张区分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2405.17538/figure-2-nnft-brg-diagram.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "paper.pdf p. 12, Figure 2", "alt_text": "NNFT 与 Bayesian RG 的交换图，从神经网络参数分布映射到一族统计场论作用量。", "caption": r"交换图定义 BRG–NNFT：\((\phi_\theta,\pi)\) 与其 coarse-grained \((\phi_\theta,\pi_\Lambda)\) 分别映到 \(S[\phi]\) 与 \(S_\Lambda[\phi]\)。", "selection_rationale": "Figure 2 是论文的核心概念图，作者明确称全文故事由此图概括；它优先于后面的 loss 数据图。"},
        "figure_refs": [figure("2405.17538", "figure-2-nnft-brg-diagram.webp", "Figure 2", 12, "define the commuting BRG–NNFT construction", "网络/参数分布与场论作用量之间的四节点交换图。", "BRG 在参数空间的 coarse graining 通过 NNFT 诱导出场论空间中的 flow。", "Commutativity is established within the assumptions analyzed in the paper, not for arbitrary finite modern networks.")],
        "equation_refs": [
            {"label": "Information-shell split", "latex": r"\mathcal M_\Lambda^{<}=\{\theta^A:\lambda_A^*<\Lambda\},\qquad \mathcal M_\Lambda^{>}=\{\theta^A:\lambda_A^*\ge\Lambda\}", "role": "separate sloppy and stiff parameter directions", "symbols": {"lambda_A": "Fisher sensitivity at the MAP", "Lambda": "distinguishability cutoff", "M": "parameter manifold"}, "evidence": "paper.pdf p. 18, Eq. (53)", "interpretation": "The scale is defined by statistical distinguishability rather than spatial wavelength."},
            {"label": "Renormalized posterior", "latex": r"\pi_\Lambda(\theta_<,\theta_>)=\pi_\Lambda^{<}(\theta_<)\pi_\Lambda^{>}(\theta_>),\qquad \pi_\Lambda^{>}=\int_{\mathcal M_\Lambda^{<}}d\theta_<\,\pi_*(\theta_<,\theta_>)", "role": "marginalize irrelevant directions and retain relevant posterior information", "symbols": {"pi_*": "trained posterior", "pi_Lambda": "coarse-grained posterior", "theta_<": "sloppy parameters"}, "evidence": "paper.pdf p. 19, Eq. (54)", "interpretation": "BRG averages fine parameter distinctions below the chosen Fisher scale."},
        ],
        "evidence_refs": ["paper.pdf pp. 11–20: NNFT–BRG map and Fisher coarse graining", "paper.pdf pp. 21–33: analytic cos-net and numerical ensemble tests", "source PDF SHA-256 7fcf4b1ff545459ed73f84748993bb981910e277c53bd7549f94074bbf9bf14e", "Evidence status: full-text verified; no independent reproduction performed."],
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
