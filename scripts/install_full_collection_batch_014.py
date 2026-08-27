#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 014."""

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
        "arxiv_id": "2408.10205", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2408.10205",
        "title_en": "KAN 2.0: Kolmogorov-Arnold Networks Meet Science",
        "title_zh": "KAN 2.0：Kolmogorov–Arnold 网络与科学发现的双向接口",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["4031a860f6cbc640"], ["AI for Science"]),
        "verified_metadata": meta(
            "2408.10205", "v1", "KAN 2.0: Kolmogorov-Arnold Networks Meet Science",
            ["Ziming Liu", "Pingchuan Ma", "Yixuan Wang", "Wojciech Matusik", "Max Tegmark"],
            ["cs.LG", "cs.AI", "physics.comp-ph", "physics.data-an"], "cs.LG",
            "2024-08-19T17:59:04Z",
            "A bidirectional framework combines scientific priors with interpretable KANs and adds multiplication nodes, symbolic compilation, attribution, and structure extraction.",
        ),
        "sections": [
            sec("作者信息", r"作者：Ziming Liu、Pingchuan Ma、Yixuan Wang、Wojciech Matusik、Max Tegmark；arXiv:2408.10205v1。全文 28 页，是 pykan 的方法扩展和多组科学发现案例，不是单一 benchmark 论文。"),
            sec("研究问题", r"普通神经网络适合连续函数逼近，却不天然暴露变量、模块和符号结构；物理推理则依赖乘法、守恒量、对称性与解析表达式。论文问：能否把科学先验编译进 KAN，再从训练后的 KAN 反向抽取可解释的科学结构？"),
            sec("背景", r"KAN 把可学习的一元函数放在边上，以节点求和组合它们。原始加法 KAN 虽有可视化优势，却会把简单乘积 (xy) 绕写成多个加法/平方节点；这使网络图的结构不再等同于物理表达式的结构。", r"Figure 1 给出双向循环：Science→KAN 包括加入辅助变量、模块结构和符号公式；KAN→Science 包括 feature attribution、module discovery 与 symbolic regression。它比单列功能更直接地表达全文主张。"),
            sec("模型与方法", r"MultKAN 在普通 KANLayer 后插入 multiplication layer，使若干子节点显式相乘；当所有乘法节点数为零时退化为原 KAN。kanpiler 把 SymPy expression 编译成固定/可微调 KAN，从而把已知物理公式作为结构先验而非训练后拟合。", r"作者还定义从输出向输入反传的 node/edge attribution，用于剪枝输入；tree converter 把网络转为计算树，module attribution 寻找可复用子结构。工作流再用于 conserved quantities、Lagrangians、Schwarzschild hidden symmetry 与 constitutive laws。"),
            sec("核心结果与证据", r"Figure 1 是框架图：上行把科学知识嵌入 KAN，下行把训练后的图转回科学假设；中央 MultKAN 的显式乘法节点正是连接 symbolism 与 connectionism 的关键接口。", r"在 (f(x,y)=xy) 上，普通 KAN 需要两个加法节点，MultKAN 用一个乘法节点表达同一结构。kanpiler 对解析函数的 spline approximation 报告 loss 随 grid intervals (N) 约按 (N^{-8}) 缩放。", r"案例也展示失败边界：Schwarzschild hidden-symmetry 任务中 KAN 单独停在约 (10^{-3}) loss，MLP 可到 (10^{-8})；用 MLP 跨过 domain-wall optimization 后再由 KAN fine-tune，才达到约 (10^{-15})。constitutive-law 例子则把含先验的初始约 (10^{-2}) loss 经展开、扰动、剪枝和符号化降到 (3\times10^{-11})。"),
            sec("有效性与局限", r"这些结果主要是设计良好的 synthetic/physics case studies，并未证明 KAN 在噪声大、维度高或数据有限的真实科学任务中普遍优于 MLP、symbolic regression 或 sparse identification。图结构可读不等于因果机制正确；attribution 也依赖训练解与参数化。", r"许多流程需要人工加入辅助变量、选择先验、剪枝阈值和 symbolification library。Schwarzschild 案例显示 KAN 仍可能有严重 optimization barrier；极低训练 loss 只验证给定数据/方程残差，不是新物理定律的独立实验确认。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2408.10205；代码：https://github.com/KindXiaoming/pykan。全文 28 页，PDF SHA-256：f7c1070cd3be933f8690e9b7a903441ed10f7d7e35fb2d574b645ae66059dace。", r"复现需固定 pykan version、KAN widths/grids/spline order、multiplication arities、training schedule、regularization、attribution normalization、pruning/symbolification thresholds、辅助变量和每个案例的采样域。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 Figure 2，理解 Science↔KAN 循环以及为何显式乘法改变可解释性；再读 Sections 3.1–3.4 的 auxiliary variables、kanpiler、attribution 与 modules。最后挑 Figures 10–13 的一个物理案例逐步检查，并把“发现结构”“拟合残差”和“实验验证”分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2408.10205/figure-1-science-kan.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "Science 与 KAN 之间的双向箭头，展示先验注入和特征、模块、符号公式抽取。", "caption": "科学知识可编译进 KAN；训练后的 KAN 又可反向提供特征、模块和符号假设。", "selection_rationale": "Figure 1 是全文最重要的概念图，优先于 loss 曲线和单个案例数据图。"},
        "figure_refs": [figure("2408.10205", "figure-1-science-kan.webp", "Figure 1", 1, "summarize the bidirectional science–KAN workflow", "Science 与 KAN 双向连接的框架图。", "显式乘法、先验编译和结构抽取共同构成作者所说的 symbolic–connectionist bridge。", "The diagram is a research program; each claimed discovery still requires case-specific validation.")],
        "equation_refs": [
            {"label": "MultKAN composition", "latex": r"\operatorname{MultKAN}(x)=(\Psi_L\circ\Psi_{L-1}\circ\cdots\circ\Psi_0)x,\qquad \Psi_l=M_l\circ\Phi_l", "role": "insert explicit multiplication after each KAN layer", "symbols": {"Phi_l": "ordinary KAN layer", "M_l": "multiplication layer"}, "evidence": "paper.pdf p. 4, Eq. (5)", "interpretation": "The computation graph can represent multiplicative physical structure directly instead of synthesizing it through sums."},
            {"label": "Scientific residual objective", "latex": r"\mathcal L_H=\frac1N\sum_{i=1}^{N}\left|f(z^{(i)})\cdot\nabla H(z^{(i)})\right|^2", "role": "learn a conserved quantity along a vector field", "symbols": {"f": "dynamical vector field", "H": "candidate invariant"}, "evidence": "paper.pdf pp. 11–12, conserved-quantity section", "interpretation": "Vanishing directional derivative is a physics constraint, but finite-sample residual minimization alone does not establish a universal invariant."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–7: framework, MultKAN, auxiliary variables and kanpiler", "paper.pdf pp. 8–17: attribution, modules and physics case studies", "source PDF SHA-256 f7c1070cd3be933f8690e9b7a903441ed10f7d7e35fb2d574b645ae66059dace", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2408.15431", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2408.15431",
        "title_en": "Integer Topological Defects Reveal Anti-Symmetric Forces in Active Nematics",
        "title_zh": "整数拓扑缺陷揭示活性向列中的反对称力",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["a3b5ca6af4d894fb"], ["Nonreciprocal Systems"]),
        "verified_metadata": meta(
            "2408.15431", "v2", "Integer Topological Defects Reveal Anti-Symmetric Forces in Active Nematics",
            ["Zihui Zhao", "Yisong Yao", "He Li", "Yongfeng Zhao", "Yujia Wang", "Hepeng Zhang", "Hugues Chaté", "Masaki Sano"],
            ["cond-mat.soft"], "cond-mat.soft", "2024-08-27T16:40:07Z",
            "A particle model and hydrodynamic closure show that nonlinear antisymmetric active forces can explain accumulation around imposed +1 defects in cellular active nematics.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zihui Zhao、Yisong Yao、He Li、Yongfeng Zhao、Yujia Wang、Hepeng Zhang、Hugues Chaté、Masaki Sano；arXiv:2408.15431v2。全文 13 页，把已有 NPC 整数缺陷实验与 bottom-up particle/hydrodynamic model 对接。"),
            sec("研究问题", r"传统 active-nematic force (-\zeta\nabla\cdot Q) 对 +1 aster 与 target 预测相反的径向流；实验却在 aster、spiral、target 的 core 都看到细胞积累。论文问：哪类被常规线性 active stress 忽略的力能统一解释这种 pattern-independent accumulation？"),
            sec("背景", r"+1 defect 可由 director 与径向方向的 tilt θ0 连续参数化：aster 为 θ0=0，target 为 θ0=π/2，中间是 spiral。Figure 1 将三类 director texture、线性力方向、微加工 ridge 和 NPC accumulation 放在一起，直观暴露 “线性理论对 target 给出 outward force，实验仍 inward accumulation” 的矛盾。"),
            sec("模型与方法", r"作者扩展 dense Vicsek-style nematic particles：位置以速度 (v_0) 更新，极性包含 nematic alignment、随机 reversal、angular noise、soft repulsive torque 和外加 +1 pattern。扫描 (v_0,C_r,C_p) 后，三类 +1 texture 都存在中心积累区。", r"随后从 kinetic equation 截断角 Fourier modes (f_0,f_1,f_2)，得到 density ρ、polar momentum (w) 和 density-weighted nematic tensor (\widetilde Q) 的 hydrodynamics。极性方程除 (-\zeta\nabla\cdot\widetilde Q) 外含两个 nonlinear terms，系数 γ1 与 γ2；粒子模型给出 repulsive regime 中通常 γ1>0、γ2<0。"),
            sec("核心结果与证据", r"Figure 1 是实验–理论冲突的关键图：线性 active force 对 aster 指向 core、对 target 指向外，但 NPC 在 target core 的荧光核密度仍显著增加，因此仅以 ζ 的正负分类不够。", r"particle simulations 在 target、π/4 spiral、aster 上均给出中心 accumulation，并在 ((v_0,C_r)) plane 形成有限参数区；PDE 数值结果复现该趋势。控制计算独立改变 ζ 与 γ1−γ2，并扩展到 −1 defects，支持反对称项而非单个拟合参数造成分类改变。", r"令 (S=1) 且密度均匀后，总力分解为 bend/splay 系数 (A\pm B)，其中 (A=-2\zeta)、(B=2(\gamma_1-\gamma_2))。只要 (B\neq0)，one-constant extensile/contractile 二分就不完备，存在传统 I/III 区之外的行为。"),
            sec("有效性与局限", r"整数缺陷由外部 ridge/field 稳定，不等同于自由演化 active nematic 中自发产生的缺陷；particle-to-PDE closure 使用 scaling ansatz、mode truncation 和被删减的 nonlinear terms。结果是定性机制一致性，不是对每个 NPC 速度/应力场的参数无关拟合。", r"γ1−γ2 的符号来自给定 repulsive microscopic model，实验中并未直接测量这两个系数。固定 (S=1)、uniform density 的 bend/splay 重写只用于物理解读，在 defect core 正是 order 与 density 变化最强的区域。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2408.15431。全文 13 页，PDF SHA-256：dfb13230b6067ac4b64283bc97789eafd18f98e89ce7ae105de110a7f2b8501d。", r"复现需固定 (L,\rho_0,v_0,k,\eta,C_p,C_r)、defect radius/boundary、time step、initial ensemble、radial-bin normalization、kinetic closure coefficients、PDE discretization 与 ζ/γ1/γ2 control scans。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 的 target paradox；再对照 Eqs. (1)–(2) 与 particle Eqs. (3)–(4)，确认线性理论为何失败。随后读 Eqs. (6)–(11) 的 closure 和 Figure 3 phase map，最后用 Eq. (16) 的 bend/splay 分解理解 γ1−γ2 为何破坏 extensile/contractile 二分。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2408.15431/figure-1-integer-defects.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "+1 aster、spiral、target 的 director/force 示意，以及 ridge substrate 和 NPC 核积累显微图。", "caption": "线性 active stress 对 target 预测 outward force，实验却仍在 core 积累；这一矛盾要求加入反对称 nonlinear forces。", "selection_rationale": "Figure 1 同时呈现几何纹理、理论预测和实验反例，是全文最具解释力的可视化。"},
        "figure_refs": [figure("2408.15431", "figure-1-integer-defects.webp", "Figure 1", 2, "show the defect geometry and the failure of linear-force classification", "+1 defect sketches, predicted force arrows, ridge image and accumulated nuclei.", "Target-pattern accumulation contradicts the direction predicted by the usual linear active stress alone.", "The image motivates additional forces; it does not directly measure gamma1 or gamma2.")],
        "equation_refs": [
            {"label": "Conventional linear active force", "latex": r"\gamma v=f^a=-\zeta\nabla\cdot Q", "role": "state the standard extensile/contractile description", "symbols": {"zeta": "linear activity", "Q": "nematic tensor"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "For imposed +1 textures this term changes radial direction with defect tilt and cannot explain accumulation for every texture."},
            {"label": "Bend–splay force decomposition", "latex": r"-\zeta\nabla\cdot\widetilde Q+\gamma_1[(\widetilde Q\cdot\nabla)\widetilde Q]^T+\gamma_2\widetilde Q(\nabla\cdot\widetilde Q)\simeq(A+B)(n\cdot\nabla)n+(A-B)n(\nabla\cdot n)", "role": "separate symmetric and antisymmetric active-force sectors", "symbols": {"A": "-2 zeta", "B": "2(gamma1-gamma2)", "n": "director"}, "evidence": "paper.pdf p. 6, Eq. (16)", "interpretation": "A nonzero antisymmetric coefficient B gives independent bend and splay responses beyond the one-constant dichotomy."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–3: +1 defects, standard force and particle model", "paper.pdf pp. 4–6: kinetic closure, phase classification and bend/splay decomposition", "source PDF SHA-256 dfb13230b6067ac4b64283bc97789eafd18f98e89ce7ae105de110a7f2b8501d", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2409.17808", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2409.17808",
        "title_en": "Generative Modeling of Molecular Dynamics Trajectories",
        "title_zh": "分子动力学轨迹的生成建模",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["bb22eac7e125b74a"], ["Generative Models"]),
        "verified_metadata": meta(
            "2409.17808", "v1", "Generative Modeling of Molecular Dynamics Trajectories",
            ["Bowen Jing", "Hannes Stärk", "Tommi Jaakkola", "Bonnie Berger"],
            ["cs.LG", "q-bio.BM"], "cs.LG", "2024-09-26T17:56:27Z",
            "MDGen generates entire molecular trajectories with stochastic interpolants and conditioning masks for simulation, transition paths, upsampling, and design tasks.",
        ),
        "sections": [
            sec("作者信息", r"作者：Bowen Jing、Hannes Stärk、Tommi Jaakkola、Bonnie Berger；arXiv:2409.17808v1。全文 23 页，模型名 MDGen，主要数据是 3,309 个 tetrapeptides 的 explicit-solvent trajectories，并含 protein/long-trajectory proof of concept。"),
            sec("研究问题", r"现有 ML surrogate 多学习单步 transition kernel 或 equilibrium ensemble，难以在同一模型中做 forward rollout、固定两端点的 transition-path sampling 与时间上采样。论文问：能否把整条 (T\times L) trajectory 当作一个生成对象，通过不同 conditioning masks 统一这些任务？"),
            sec("背景", r"分子状态同时有 rigid-frame (SE(3)) 几何、周期 torsions、residue identities 与跨时间相关。逐 Cartesian coordinate 扩散会浪费全局平移/旋转对称性；逐步自回归又把误差沿长轨迹累积。", r"Figure 1 左侧用同一个 grid 展示 interpolation、upsampling、inpainting 等 mask；右侧把 (T\times L) invariant tokens 送入跨 frame/residue 的 transformer。它替代了对多任务条件机制的冗长描述。"),
            sec("模型与方法", r"每个 residue/frame 以相对 key frames 的 roto-translation offsets 和 7 个 torsion angles 表示；这些 tokens 对整体 (SE(3)) 变换不变。连续几何由 stochastic interpolants 从 Gaussian noise 生成，amino-acid identities 用 Dirichlet flow matching；同一 architecture 通过 mask 指定已知端点、稀疏 frames 或 residues。", r"forward model 每次生成 10 ns，推理时串联为 100 ns；interpolation 在首尾结构条件下生成 1 ns path；upsampling 从每 10 ps 保存一帧恢复到 100 fs，即 100× finer temporal grid。"),
            sec("核心结果与证据", r"Figure 1 说明 MDGen 的统一性不是口号：任务差异只在 trajectory grid 的 observed/masked cells，而生成器始终处理同一种 (T\times L) 几何 token array。", r"100 ns-equivalent forward rollouts 的 torsion-all JSD 为 0.109；100 ns replicate-MD baseline 为 0.076，10 ns/1 ns/100 ps baselines 分别 0.125/0.240/0.364。MSM transition-flux entries 与 reference 的 mean Spearman ρ 为 (0.67\pm0.01)。", r"模型平均约 60 GPU-s 生成 100 ns-equivalent trajectory，而 MD 约 3 GPU-h；按最慢 TICA mode 的 decorrelation wall time，100 个 peptides 中 78 个报告 10–1000× speedup。upsampling 从 10 ps 到 100 fs 能恢复部分 fast torsional autocorrelation；transition-path task 对每对 metastable states 采样 1,000 条 1 ns paths。"),
            sec("有效性与局限", r"生成的 frame index 与训练数据时间间隔对应，但模型不积分物理力方程，也不保证 detailed balance、energy conservation、正确 path action 或绝对 kinetic rates。串联 10 ns blocks 可能积累 distribution shift；JSD/MSM correlation 不能证明 rare events 的速率无偏。", r"speedup 对比依赖 GPU、MD implementation、batching 和 “equivalent trajectory” 定义。训练以小 peptides 为主；100k-frame Hyena、protein ensembles 与 design 都是 proof of concept。upsampling 由 coarse frames 条件生成 plausible fast motion，不是从信息论上恢复唯一被丢失的 microscopic path。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2409.17808；代码：https://github.com/bjing2016/mdgen。全文 23 页，PDF SHA-256：6f76aea6f743803fcc0a24019a56a0fcd334244e597d96b16af71d5bec54d654。", r"复现需固定 MD force field/solvent/thermostat、train/validation/test peptide split、frame interval、key-frame convention、torsion wrapping、conditioning masks、stochastic-interpolant schedule、rollout chaining、TICA/MSM lag/clustering 与 wall-clock hardware。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 Table 1，把所有任务写成同一 mask algebra；再读 Eqs. (3)–(6) 的 invariant representation 与 stochastic interpolant。然后逐项核对 Figure 2/Table 2 的 equilibrium、kinetic 和 runtime diagnostics，最后看 Figures 3–5，并把 conditional path plausibility 与真实动力学速率分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2409.17808/figure-1-mdgen-overview.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "trajectory grid 上的 interpolation、upsampling、inpainting masks，以及跨 frame 和 residue 的 transformer。", "caption": r"不同 MD 任务只改变 \(T\times L\) trajectory grid 上哪些 cells 被条件化；MDGen 统一生成其余 cells。", "selection_rationale": "Figure 1 是全文最重要的任务/架构示意图，优先于单个 peptide 的数据曲线。"},
        "figure_refs": [figure("2409.17808", "figure-1-mdgen-overview.webp", "Figure 1", 2, "show the unified masked-trajectory formulation", "多种 trajectory-conditioning masks 与时空 transformer 示意。", "Forward simulation, endpoint interpolation, upsampling and inpainting share one generative object.", "A shared representation does not make every generated trajectory physically calibrated.")],
        "equation_refs": [
            {"label": "Invariant molecular token", "latex": r"\chi_t^l=\big((R,t),(\psi,\phi,\omega,\chi_1,\ldots,\chi_4)\big)\in SE(3)\times\mathbb T^7", "role": "encode one residue at one trajectory frame", "symbols": {"SE(3)": "rigid roto-translation", "T7": "seven periodic torsions"}, "evidence": "paper.pdf p. 4, Eq. (3)", "interpretation": "Relative key-frame transforms remove arbitrary global roto-translation while preserving internal motion."},
            {"label": "Stochastic interpolant", "latex": r"x_s=\alpha_s x_0+\beta_s x_1+\sigma_s\epsilon,\qquad \epsilon\sim\mathcal N(0,I)", "role": "connect Gaussian noise and trajectory-token data", "symbols": {"s": "generative time", "x1": "data trajectory", "x0": "base sample"}, "evidence": "paper.pdf p. 3, stochastic-interpolants section", "interpretation": "The learned velocity generates a joint trajectory array rather than integrating atomistic forces frame by frame."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: task masks, invariant tokens and stochastic interpolants", "paper.pdf pp. 5–10: forward, transition-path and upsampling evaluations", "source PDF SHA-256 6f76aea6f743803fcc0a24019a56a0fcd334244e597d96b16af71d5bec54d654", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2409.17858", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2409.17858",
        "title_en": "How Feature Learning Can Improve Neural Scaling Laws",
        "title_zh": "特征学习何时能改善神经网络缩放律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["de7541eb8ecbcd8f"], ["Scaling Laws"]),
        "verified_metadata": meta(
            "2409.17858", "v2", "How Feature Learning Can Improve Neural Scaling Laws",
            ["Blake Bordelon", "Alexander Atanasov", "Cengiz Pehlevan"],
            ["stat.ML", "cs.LG"], "stat.ML", "2024-09-26T18:02:31Z",
            "A solvable feature-learning model predicts when source difficulty changes training-time and compute-optimal scaling exponents beyond the lazy kernel limit.",
        ),
        "sections": [
            sec("作者信息", r"作者：Blake Bordelon、Alexander Atanasov、Cengiz Pehlevan；arXiv:2409.17858v2，ICLR 2025。全文 32 页，以 two-layer linear network 的 dynamical mean-field theory 为主，并用 nonlinear MLP/CNN 和 transformer observations 做外部检验。"),
            sec("研究问题", r"kernel/lazy theory 把 features 冻结，常能推出 loss 对时间、width 与 data 的 power laws，却无法解释 rich feature learning 是否改变指数。论文问：相对于初始 NTK 的 source exponent β 在什么范围内，feature evolution 会改变 asymptotic learning exponent 和 fixed-compute 的最优 width/time 配比？"),
            sec("背景", r"data/architecture 由 kernel spectrum exponent α 与 target source exponent β 描述。易任务 β>1 位于初始 infinite-width NTK 的 RKHS 内；hard tasks β<1 在其外。参数 γ 控制 feature-learning strength，γ→0 给出 lazy limit。", r"Figure 1 直接画出 χ(β) 以及 lazy/rich 两张 ((\alpha,\beta)) phase diagrams，标明时间、模型 bottleneck 与 SGD-noise terms 的主导区域；这是全文最重要的理论地图。"),
            sec("模型与方法", r"作者研究 projected gradient descent 下的 two-layer linear network，并在 width (N)、batch (B)、time (t) 的极限中导出 DMFT equations。loss scaling 由 spectrum/source tail、finite-width cutoff 与 SGD variance 竞争决定。", r"fixed compute 取 (C=Nt)，在各 phase 内平衡 time-limited 与 width-limited terms 得到 compute-optimal (N^*(C),t^*(C))。numerics 对 32 个 random-matrix instances 比较 DMFT；随后训练 circle 上 power-law Fourier targets 的 ReLU MLP、vision CNN，并检查 C4 transformer scaling。"),
            sec("核心结果与证据", r"Figure 1 的核心结论是分段的：hard regime β<1 中，lazy learning 为 (L\sim t^{-\beta})，rich feature learning 变为 (L\sim t^{-2\beta/(1+\beta)})，因此指数提高但不超过 1；β>1 的 easy regimes 不改变主 exponent。", r"在 hard regime 把 (t^{-\chi}) 与 (N^{-\alpha\beta}) 于 (C=Nt) 下平衡，得到 compute-optimal loss (L^*(C)\sim C^{-\alpha\beta\chi/(\alpha\beta+\chi)})，其中 rich χ 为 (2\beta/(1+\beta))。这改变资源分配，不是简单常数倍 speedup。", r"Figure 2 的 DMFT 与 random experiments 显示 finite-γ crossover；ReLU MLP 的 Fourier tasks 和 CNN vision results 支持 hard/easy 分区。作者还估计 CNN kernel spectrum α≈2、target source β≈0.075，并在 C4 transformer cross-entropy 中观察到更符合 feature-learning exponent 的趋势，但这些是有限规模经验支持。"),
            sec("有效性与局限", r"严格可解对象是 two-layer linear network 与特定 projected dynamics；把 α、β 从 finite neural kernels/data spectra 估计后外推到深 nonlinear nets，并不是定理。asymptotic crossover time 可随小 γ 很大，实际训练可能仍停在 lazy-like transient。", r"hard/easy 是相对于初始 kernel RKHS 的谱定义，不等于人类对任务难度的直觉。compute (C=Nt) 忽略 depth、activation memory、communication、data reuse 和 inference cost；SGD-noise phases 还依赖 batch scaling。CNN/transformer evidence 支持趋势，未唯一识别同一 DMFT mechanism。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2409.17858；代码：https://github.com/Pehlevan-Group/FeatureLearningScalings。全文 32 页，PDF SHA-256：dea4d29f6615724b67bb45ecd30780bd75cc304e3076e8981014cadb577639e8。", r"复现需固定 spectral construction、α/β convention、γ parameterization、width/batch/time ranges、DMFT solver tolerance、random seeds、Fourier target normalization、kernel eigenspectrum estimator 与 regression window。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先读 Figure 1，把 β<1、(1<\beta<2-1/\alpha) 与 super-easy 区分；再看 Eq. (10) 的 χ(β) 和 Table 1 的 compute exponents。随后读 Figures 2–4 验证 transient/finite-width balance，最后把 MLP/CNN/transformer sections 当作 toy theory 的 stress tests，而非普适证明。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2409.17858/figure-1-scaling-phases.webp", "label": "Figure 1", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "learning exponent χ(β) 曲线以及 lazy 与 rich regimes 的 α–β phase maps。", "caption": "Feature learning 只在初始 kernel RKHS 外的 hard tasks（β<1）改变主缩放指数，并重排 fixed-compute phase boundary。", "selection_rationale": "Figure 1 是理论主结果的 phase diagram，优先于后续单数据集拟合图。"},
        "figure_refs": [figure("2409.17858", "figure-1-scaling-phases.webp", "Figure 1", 2, "map the source exponent to lazy and rich scaling regimes", "χ(β) 曲线及 lazy/rich α–β phase maps。", "The exponent changes only for targets outside the initial-kernel RKHS.", "The phase diagram is exact for the solvable model; application to deep networks is empirical.")],
        "equation_refs": [
            {"label": "Feature-learning exponent", "latex": r"\chi(\beta)=\beta\max\!\left(1,\frac{2}{1+\beta}\right),\qquad L(t)\sim t^{-\chi(\beta)}", "role": "state the asymptotic time-scaling transition", "symbols": {"beta": "target source exponent", "chi": "learning exponent"}, "evidence": "paper.pdf p. 7, Eq. (10)", "interpretation": "For beta below one, chi=2 beta/(1+beta) exceeds the lazy exponent beta; above one the exponent is unchanged."},
            {"label": "Hard-task compute optimum", "latex": r"L^*(C)\sim C^{-\frac{\alpha\beta\chi}{\alpha\beta+\chi}},\qquad C=Nt,\quad \chi=\frac{2\beta}{1+\beta}", "role": "balance training time against the finite-width bottleneck", "symbols": {"alpha": "kernel spectral exponent", "N": "model width", "t": "training steps"}, "evidence": "paper.pdf pp. 8–9, Table 1 and Figure 4", "interpretation": "Feature learning changes the optimal allocation because it changes the time exponent, not the width cutoff."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–7: source regimes, solvable model and exponent derivation", "paper.pdf pp. 8–12: compute optimum and nonlinear-network tests", "source PDF SHA-256 dea4d29f6615724b67bb45ecd30780bd75cc304e3076e8981014cadb577639e8", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2410.02667", "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2410.02667",
        "title_en": "GUD: Generation with Unified Diffusion",
        "title_zh": "GUD：用统一扩散连接扩散式与自回归式生成",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["5907a6891e0aea7f", "f23761c03fd9497a"], ["Renormalization Group", "Flow Matching"]),
        "verified_metadata": meta(
            "2410.02667", "v1", "GUD: Generation with Unified Diffusion",
            ["Mathis Gerdes", "Max Welling", "Miranda C. N. Cheng"],
            ["cs.LG", "hep-th", "stat.ML"], "cs.LG", "2024-10-03T17:58:49Z",
            "Component-dependent diffusion bases, priors, and schedules continuously interpolate simultaneous diffusion with sequential autoregressive generation.",
        ),
        "sections": [
            sec("作者信息", r"作者：Mathis Gerdes、Max Welling、Miranda C. N. Cheng；arXiv:2410.02667v1。全文 16 页，在 CIFAR-10 与 PCAM 32×32 上做 proof-of-concept；同一论文在 Collection 有两个 catalog records，共用此卡片。"),
            sec("研究问题", r"标准 diffusion 在 pixel basis 中同时抹去所有 components，自回归模型则按顺序生成 token。RG 又提示应在 frequency/multiscale basis 中先消去高频。论文问：把 basis、endpoint prior 和每个 component 的 noising schedule 都开放后，diffusion 与 autoregression 是否只是同一连续设计空间的两个极限？"),
            sec("背景", r"普通 scalar schedule γ(t) 对所有维度相同，改变它通常只是在同一 diagonal path 上重参数化时间。GUD 允许 γi(t) 不同，因此在 component-wise SNR space 中选择真正不同的 paths。若各 component 的 active noising intervals 完全不重叠，reverse process 就逐 component 条件生成，达到 autoregressive limit。"),
            sec("模型与方法", r"先以可逆线性变换 (M=S^{-1}U) 选择 diffusion-diagonal basis；(U) 可取 PCA、FFT 或 Haar，(S) 决定 whitening/data-matched prior。随后为每一 component 指定 Ornstein–Uhlenbeck noising rate βi(t) 与 integrated schedule γi(t)。", r"linear schedules 用 ordering variable (l_i) 和 inverse-softness (a) 错开 onset；(a) 越大，active intervals overlap 越少、越接近 autoregressive。另一个 (b) 构造 left-to-right column schedule；Haar variant 在尺度层级 (a) 与层内列顺序 (b) 上双重 soft-condition。"),
            sec("核心结果与证据", r"Figure 4 以同一 CIFAR-10 图像展示四种 forward corruption：标准同时扩散、variance-matched noise、column-sequential 以及 Haar+column sequential。信息被抹去的顺序在像素空间中直接可见，是 GUD 设计自由度最清楚的图像证据。", r"CIFAR-10 PCA experiment 显示 quality 随 softness 改变，standard diffusion 附近接近最优但不同 prior 在 NLL/FID 上排序不同；作者明确说明 FID 在计算资源耗尽时仍显著下降，不能把该曲线视为收敛 benchmark。", r"PCAM column-wise models 在 (b=0.3,0.5) 的 NLL 为 3.90、3.94 bits/dim，并可重复向右 extension。三层 Haar+CIFAR-10、300k steps 的 schedule family 最低 NLL 为 3.17 bits/dim；这些结果证明统一参数化可训练，不证明超过最佳 diffusion/autoregressive model。"),
            sec("有效性与局限", r"RG connection 主要是信息逐尺度消除的结构类比；论文没有证明 learned score flow 等价于特定 field-theory RG transformation，也未导出 universality class。PCA/FFT/Haar basis 都由人为选择，最优 component ordering 和 softness 尚未解决。", r"实验分辨率仅 32×32，训练 300k steps，部分 FID 未收敛；多数结论是 schedule ablation 和可视化。NLL、FID、sequential extension 各衡量不同性质；连续插值存在不等于中间 schedule 在 latency、likelihood 或 sample quality 上优于两个端点。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2410.02667。全文 16 页，PDF SHA-256：ce2b8e1870b17c819f74f859e4b8e64c5c68d52d21ac0b24692db27db4e0cbde。", r"复现需固定 PCA covariance/data split、whitening convention、γ endpoints、a/b/r sampling ranges、OU parameterization、score-network conditioning、prior covariance、Haar levels、300k-step optimizer 与 NLL/FID checkpoint。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 的 component-SNR paths 与 Figure 4 的实际 corruption；再读 Eqs. (13)–(18)，确认 basis/prior/schedule 三类自由度。随后用 Eq. (20) 和 Figure 6 理解 softness→autoregressive limit，最后读 Figures 3、5、7，并把“统一框架可表达”与“生成质量最优”分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2410.02667/figure-4-diffusion-paths.webp", "label": "Figure 4", "visual_type": "comparison", "evidence": "paper.pdf p. 9, Figure 4", "alt_text": "一张 CIFAR-10 图像在标准、variance-matched、逐列和 Haar 逐列 schedules 下的 forward corruption sequences。", "caption": "Component-dependent schedules 让信息同时、逐列或按 Haar 尺度顺序消失，从而连续连接 diffusion 与 autoregressive generation。", "selection_rationale": "Figure 4 是文章中最具可视性的机制图，优先于 NLL/FID 数据曲线。"},
        "figure_refs": [figure("2410.02667", "figure-4-diffusion-paths.webp", "Figure 4", 9, "visualize how different schedules erase information", "四行 CIFAR-10 forward-process snapshots。", "Basis and component schedule determine which spatial or multiscale information disappears first.", "The visualization demonstrates controllability, not superior sample quality.")],
        "equation_refs": [
            {"label": "Component-wise linear schedule", "latex": r"\gamma_i(t)=\gamma_{\min,i}+(\gamma_{\max,i}-\gamma_{\min,i})t", "role": "assign each diffusion component its own noising path", "symbols": {"gamma_i": "integrated noising schedule", "i": "basis component"}, "evidence": "paper.pdf p. 8, Eq. (20)", "interpretation": "Offsets derived from ordering variables separate the active intervals; decreasing their overlap makes generation more autoregressive."},
            {"label": "Component signal-to-noise ratio", "latex": r"\operatorname{SNR}_i(t)=\Sigma^{(\chi)}_{ii}(0)e^{-\gamma_i(t)}", "role": "measure which components have already been erased", "symbols": {"Sigma": "data covariance in the chosen basis", "chi": "transformed coordinates"}, "evidence": "paper.pdf pp. 5–6, Eq. (18)", "interpretation": "Whitening removes variance-induced hierarchy so schedule choice alone controls soft conditioning."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: GUD construction, basis/prior freedom and soft-conditioning limit", "paper.pdf pp. 8–10: PCA, column-wise and Haar experiments", "source PDF SHA-256 ce2b8e1870b17c819f74f859e4b8e64c5c68d52d21ac0b24692db27db4e0cbde", "Evidence status: full-text verified; no independent reproduction performed."],
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
