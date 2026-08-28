#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 028."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "doi-10.1007-jhep03-2026-111", "source_version": "arXiv v2 / version-of-record metadata",
        "source_pdf": "https://arxiv.org/pdf/2502.05504v2",
        "title_en": "Physics-Conditioned Diffusion Models for Lattice Gauge Theory",
        "title_zh": "面向格点规范理论的物理条件扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["b86455323b635ac8"], ["Generative Models"]),
        "verified_metadata": {"doi": "10.1007/JHEP03(2026)111", "arxiv_id": "2502.05504", "version": "v2 / version of record", "title": "Physics-Conditioned Diffusion Models for Lattice Gauge Theory", "authors": ["Qianteng Zhu", "Gert Aarts", "Wei Wang", "Kai Zhou", "Lingxiao Wang"], "categories": ["hep-lat", "cs.LG"], "primary_category": "hep-lat", "published": "2025-02-08T09:50:27Z", "abstract": "A stochastic-quantization-conditioned diffusion sampler is tested in two-dimensional U(1) lattice gauge theory across couplings and lattice sizes, with Metropolis correction.", "comment": "JHEP 03 (2026) 111; arXiv v2 accepted manuscript"},
        "sections": [
            sec("作者信息", r"作者：Qianteng Zhu、Gert Aarts、Wei Wang、Kai Zhou、Lingxiao Wang；JHEP 03 (2026) 111，DOI:10.1007/JHEP03(2026)111；对应 arXiv:2502.05504v2。核验全文 28 页，并用期刊 DOI 核对出版状态。"),
            sec("研究问题", r"二维 U(1) 格点规范理论在大逆耦合 β 下会出现拓扑冻结：单链 HMC 很难跨越不同拓扑扇区。论文问：能否把随机量子化的物理结构写进扩散模型，使在 β=1 训练的网络无需重训便迁移到更大 β 和不同格点尺寸，同时以 accept–reject 修正保证目标分布？"),
            sec("背景", r"扩散模型学习正向加噪过程的反向 score；随机量子化则以已知作用量梯度驱动 Langevin 动力学。作者利用两者 SDE 结构的对应，把 β 作为物理条件进入 drift，并采用 fully convolutional 网络处理不同 L。", r"Figure 6 对比 β=7、L=16 的 1024 个样本：Wilson loop 的 HMC 与 DM 分布接近，但 HMC 的拓扑荷几乎锁在零附近，DM proposals 覆盖多个整数扇区。"),
            sec("模型与方法", r"模型只在 β=1、16×16 格点上用 30,720 个 HMC configurations 训练；测试覆盖 β=1,3,5,7,9,11 与 L=8,16,32，另报告 L=64。生成时使用 Metropolis-adjusted annealed Langevin algorithm（DM-MAALA），把网络 proposal 放入多链 Markov sampler。", r"Metropolis step 修正有限网络误差；所谓 exactness 是 Markov chain 在满足通常遍历性与详细平衡条件下以目标分布为不变分布，并不表示有限 burn-in、有限步长或有限样本无偏。"),
            sec("核心结果与证据", r"β=1 时 DM、HMC 与解析 Wilson loop/拓扑 susceptibility 一致；同一 convolutional model 可直接用于多个 L。β=7 时 Figure 6 与 Tables 2–4 显示 DM 保持 Wilson loops，并跨越 HMC 未访问的拓扑扇区。", r"边界同样明确：Wilson loop 外推到 β=11 仍与 exact values 接近，但拓扑 susceptibility 在 β≳5 后开始出现系统偏差；β=7、L=16 时 DM 为 0.0063(3)，解析值 0.0039。作者将其归因于训练集拓扑分布残留偏置，因此“缓解冻结”不等于任意耦合下无偏外推。", r"Appendix B 的单链 autocorrelation 比较显示 DM-based multi-chain proposals 更容易跨扇区；效率数字依赖并行多链、burn-in 和计算成本口径，不能只用 τQ 宣称端到端加速。"),
            sec("有效性与局限", r"验证限于 1+1D 紧致 U(1) 纯规范理论，具有可用解析 observables；非阿贝尔规范场、fermion determinant 的非局域性和 sign problem 尚未解决。网络训练数据来自 β=1 单一 coupling，方向性 score 偏差限制远距离外推。", r"样本量多为 1024；比较没有统一计入训练、并行链和 proposal 成本。Metropolis correction 只有在实际接受率、thermalization 与 chain mixing 被诊断时才提供渐近正确性，不能替代 finite-run convergence audit。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2502.05504；代码：https://github.com/zzzqt/DM4U1；期刊：https://doi.org/10.1007/JHEP03(2026)111。核验 PDF SHA-256：0b9548d039926d29e6e89f60fa806d22681f4079c78936f901fdb5aca12b87fa。", r"复现需固定 lattice action、β/L grid、gauge augmentation、HMC training-data thinning、U-Net、noise schedule、MAALA step sizes、链数、burn-in、acceptance、observable definitions 与 analytic finite-volume formulae。", r"Evidence status: full-text verified accepted manuscript plus version-of-record metadata; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.2–5 的 HMC/topological freezing，再读 pp.6–12 的 diffusion、physics conditioning 与 MAALA。核心证据看 pp.13–15 的 Figure 6 和 Tables 1–4；最后读 pp.15–16 与 Appendices B/E，特别保留 β≳5 的 topology extrapolation failure。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1007-jhep03-2026-111/figure-6-topology.webp", "label": "Figure 6", "visual_type": "distribution", "evidence": "paper.pdf p. 15, Figure 6", "alt_text": "β=7 时 HMC 与扩散模型的 Wilson loop 和拓扑荷直方图。", "caption": "局域 Wilson loop 相符，但 HMC 的拓扑荷冻结在零附近；DM proposals 覆盖多个扇区。", "selection_rationale": "Figure 6 同时展示保持局域 observable 与缓解拓扑冻结，是该方法最直接的成功证据，也方便读者识别有限样本边界。"},
        "figure_refs": [figure("doi-10.1007-jhep03-2026-111", "figure-6-topology.webp", "Figure 6", 15, "compare local and topological sampling at beta=7", "HMC 与 DM 的 Wilson loop、topological charge 分布。", "DM proposals 跨越 HMC 在该 run 中未访问的拓扑扇区。", "This finite sample does not establish unbiased extrapolation at all beta; Tables 3–4 show a susceptibility discrepancy.")],
        "equation_refs": [
            {"label": "Metropolis acceptance", "latex": r"A(x'|x)=\min\!\left(1,\frac{p(x')q(x|x')}{p(x)q(x'|x)}\right)", "role": "correct learned proposals toward the target measure", "symbols": {"p": "lattice target density", "q": "DM-MAALA proposal kernel"}, "evidence": "paper.pdf pp. 10–12, Section 4.2", "interpretation": "The correction supplies asymptotic exactness only for a properly equilibrated, ergodic chain."},
            {"label": "Topological susceptibility", "latex": r"\chi_Q=\langle Q^2\rangle/V", "role": "measure fluctuations across topological sectors", "symbols": {"Q": "integer topological charge", "V": "lattice volume"}, "evidence": "paper.pdf p. 4, Eq. (2.8); Appendix C", "interpretation": "A frozen chain underestimates susceptibility because it does not explore the relevant sectors."},
        ],
        "evidence_refs": ["paper.pdf pp. 6–12: diffusion/SQ correspondence and MAALA", "paper.pdf pp. 13–15: Figure 6 and Tables 1–4", "paper.pdf pp. 15–16 and Appendices B/E: extrapolation and autocorrelation boundaries", "source PDF SHA-256 0b9548d039926d29e6e89f60fa806d22681f4079c78936f901fdb5aca12b87fa", "Evidence status: full-text verified accepted manuscript plus VOR metadata; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1007-jhep05-2015-104", "source_version": "arXiv v2 / version of record",
        "source_pdf": "https://arxiv.org/pdf/1410.6809v2",
        "title_en": "Relative Entropy and Proximity of Quantum Field Theories", "title_zh": "相对熵与量子场论之间的邻近性",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["1828d76c91e190d7"], ["Field Theory"]),
        "verified_metadata": {"doi": "10.1007/JHEP05(2015)104", "arxiv_id": "1410.6809", "version": "v2 / version of record", "title": "Relative Entropy and Proximity of Quantum Field Theories", "authors": ["Vijay Balasubramanian", "Jonathan J. Heckman", "Alexander Maloney"], "categories": ["hep-th", "cond-mat.dis-nn"], "primary_category": "hep-th", "published": "2014-10-24T20:00:05Z", "abstract": "Euclidean QFT measures are compared with relative entropy, whose nearby-CFT limit is the Zamolodchikov metric and whose coarse graining quantifies lost distinguishability.", "comment": "JHEP 05 (2015) 104"},
        "sections": [
            sec("作者信息", r"作者：Vijay Balasubramanian、Jonathan J. Heckman、Alexander Maloney；JHEP 05 (2015) 104，DOI:10.1007/JHEP05(2015)104；arXiv:1410.6809v2。全文 7 页，是概念与微扰分析论文。"),
            sec("研究问题", r"两个 QFT 在有限测量下有多难区分？作者把 Euclidean path-integral weight 视为 field-configuration space 上的概率分布，用 KL relative entropy 定义理论邻近性，并问它如何连接 coupling-space geometry、RG coarse graining、fine tuning 与 EFT landscape。"),
            sec("背景", r"对同一 field space 上的分布 p、q，DKL(p||q)≥0 且不对称；大量独立样本误认概率按 exp[-N DKL] 衰减。QFT 版本比较的是 Euclidean configuration measures，不是同一 Hilbert space 上 density matrices 的 quantum relative entropy。", r"若两理论的 field/operator content 不同，作者要求把它们嵌入共同 master UV theory；这个选择以及 UV regularization 是定义的一部分。"),
            sec("模型与方法", r"对 actions Sp、Sq，有 DKL=<Sq-Sp>p+log(Zq/Zp)。用局域 operators Oi 的小 coupling deformation 展开到二阶，得到 connected two-point functions 的积分，即 Fisher metric。", r"UV contact terms 通常 scheme dependent；若给定 finite UV completion，regularization 可固定。对于 CFT 的 exactly marginal deformations，体积归一化后的二阶项化为 Zamolodchikov metric。"),
            sec("核心结果与证据", r"论文建立从 relative entropy 到 coupling-space metric 的局部关系：附近 CFT 的 DKL 二阶项由 Zamolodchikov metric 测量。对于 relevant deformation，cutoff dependence 记录实验分辨率；coarse graining 后 DKL 下降，表达 RG 丢失区分 UV theories 的信息。", r"作者还提出以 UV 与 IR distinguishability 的比率描述 fine tuning，并把 landscape EFT 是否可区分转成相对熵阈值。这些是框架与 toy examples，不是对真实 Standard Model landscape 的数值普查。", r"RG 单调性来自 stochastic/coarse-graining map 下 relative entropy 的 data-processing 性质；它不等于任意 scheme 下所有有限 counterterm 部分都形成普适 c-function。"),
            sec("有效性与局限", r"Euclidean weights 必须可归一化并可作为正概率测度；复杂作用量、sign problem 与 gauge redundancy 需要额外处理。连续 QFT 的 DKL 含 UV/volume divergences，只有指定 regulator、比较方向和 normalization 后才有操作意义。", r"近邻 metric 只保留 coupling difference 的二阶项；远距离理论的 KL 不对称且不满足三角不等式。landscape 与 fine-tuning 讨论依赖共同 master theory、可测 observables 与实验 cutoff，不能直接当成自然性定理。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/1410.6809；期刊：https://doi.org/10.1007/JHEP05(2015)104。核验 PDF SHA-256：4bdaec2b89d9f28f0830a79c7311fd7312035feb815f1e6569aef83a3a1db2c8。", r"复核需固定 Euclidean measure、master theory、UV/IR cutoffs、volume、operator normalization、coupling coordinates、counterterm scheme 与 p||q 的方向。", r"Evidence status: full-text verified version of record/arXiv v2; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.1–2 的 Eqs. (1)–(12)，确认 classical KL 与 QFT measure 的对应；再读 p.3 的 CFT/Zamolodchikov limit。最后读 pp.4–6 的 RG、fine tuning 与 flux-vacua examples，并逐项标出 regulator 与 master-theory assumptions。"),
        ],
        "cover": {"mode": "title_abstract", "label": "Relative entropy for QFTs", "visual_type": "title_abstract", "evidence": "paper.pdf pp. 1–6, definitions and applications", "alt_text": "相对熵作为量子场论邻近性度量的标题与摘要。", "caption": "Euclidean QFT measures 的 KL divergence 在近邻 CFT 极限化为 Zamolodchikov metric。", "abstract_text": "论文把 Euclidean QFT 定义的 field-configuration measures 用 relative entropy 比较，并将近邻 coupling geometry、RG 信息损失和 EFT distinguishability 放入同一框架。", "selection_rationale": "原文没有图；主要证据是定义、微扰展开与尺度分析，因此标题摘要比任意公式页截图更忠实。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "QFT relative entropy", "latex": r"D_{KL}(p\Vert q)=\langle S_q-S_p\rangle_p+\log(Z_q/Z_p)", "role": "compare Euclidean field-configuration measures", "symbols": {"S_p": "reference action", "Z_p": "reference partition function"}, "evidence": "paper.pdf p. 2, Eq. (6)", "interpretation": "The result depends on a shared regulated configuration space and on the ordered pair p||q."},
            {"label": "Perturbative Fisher metric", "latex": r"G^{\rm Fisher}_{ij}=\frac12\int d^Dx\sqrt g\,d^Dy\sqrt g\,\langle O_i(x)O_j(y)\rangle_{c,p}", "role": "give the local metric on coupling space", "symbols": {"O_i": "deforming operator", "g": "background metric"}, "evidence": "paper.pdf p. 2, Eqs. (10)–(12)", "interpretation": "For exactly marginal CFT deformations the regulated density reduces to the Zamolodchikov metric."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–2: KL definition and perturbative expansion", "paper.pdf p. 3: conformal theories and Zamolodchikov metric", "paper.pdf pp. 4–6: RG information, fine tuning and landscape examples", "source PDF SHA-256 4bdaec2b89d9f28f0830a79c7311fd7312035feb815f1e6569aef83a3a1db2c8", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1007-jhep05-2024-060", "source_version": "arXiv v2 / version of record", "source_pdf": "https://arxiv.org/pdf/2309.17082v2",
        "title_en": "Diffusion Models as Stochastic Quantization in Lattice Field Theory", "title_zh": "作为格点场论随机量子化的扩散模型",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["8d2c96b69f64b78d"], ["Field Theory"]),
        "verified_metadata": {"doi": "10.1007/JHEP05(2024)060", "arxiv_id": "2309.17082", "version": "v2 / version of record", "title": "Diffusion Models as Stochastic Quantization in Lattice Field Theory", "authors": ["Lingxiao Wang", "Gert Aarts", "Kai Zhou"], "categories": ["hep-lat", "cs.LG"], "primary_category": "hep-lat", "published": "2023-09-29T09:26:59Z", "abstract": "Diffusion denoising is related to stochastic quantization and used as a global proposal for two-dimensional lattice phi-four theory.", "comment": "JHEP 05 (2024) 060; code at github.com/Anguswlx/DMasSQ"},
        "sections": [
            sec("作者信息", r"作者：Lingxiao Wang、Gert Aarts、Kai Zhou；JHEP 05 (2024) 060，DOI:10.1007/JHEP05(2024)060；arXiv:2309.17082v2。全文 31 页，含 toy model 与二维 φ4 格点数值实验。"),
            sec("研究问题", r"随机量子化用作用量梯度驱动 fictitious-time Langevin process；diffusion model 则从数据学习 time-dependent score 并反向去噪。论文问两者能否建立直接对应，并让训练后的 DM 成为全局 proposal，降低临界区局域 MCMC 的 autocorrelation。"),
            sec("背景", r"正向 diffusion 将 target configurations 平滑到简单 prior；反向 SDE 使用 learned score 恢复数据分布。与 stochastic quantization 相比，关键差异是 drift 从数据学习且依赖 diffusion time。", r"Figure 8 在 κ=0.27、λ=0.022、L=32、1024 configurations 上比较 |M| autocorrelation：DM-MC 曲线约四步降到接近零，HMC 与局域 MC 保持长相关。"),
            sec("模型与方法", r"作者训练 U-Net score model，先用一维 double-well 检查 drift/effective action，再在二维 lattice φ4 的 symmetric 与 broken phases 生成 configurations。通过 probability-flow likelihood 估计 proposal density，并在每条 trajectory 后加入 Metropolis–Hastings accept–reject。", r"DM proposal 是全局更新；其训练仍需要参考 configurations。实验将 DM-MC、local Metropolis MC 与 HMC 比较，并以 magnetization distribution、action likelihood、acceptance 与 autocorrelation 做诊断。"),
            sec("核心结果与证据", r"DM 在两相中复现 magnetization distributions；estimated effective action 与 true action 在主要概率区相关。Figure 8 显示临界参数处 DM-MC 的 |M| decorrelation 明显更快。", r"作者用 tmax=100 报告 integrated autocorrelation times：local MC 79.984、HMC 41.354、DM-MC 2.360。该数字来自 1024 configurations 的单一设置且未用 automatic-window uncertainty，因此是实验性效率证据，不是普适动态临界指数。", r"MH acceptance 在附录扫描中通常约 0.4–0.6，但依赖 lattice size、κ 和训练 epochs。accept–reject 可纠正 proposal density，前提是 likelihood estimate、chain thermalization 与 ergodicity 均成立。"),
            sec("有效性与局限", r"模型只验证二维 scalar φ4；没有 dynamical fermions、non-Abelian gauge symmetry 或 sign problem。训练数据成本、网络训练成本和并行硬件未纳入 τint 数字，因而不能直接换算 wall-clock speedup。", r"near-critical 结果基于有限 L=32 与有限样本；effective-action reconstruction、Skilling–Hutchinson trace estimator 和 finite-epoch model error 都会影响 acceptance。作者将扩展到 gauge/fermion theories 明确留作未来工作。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2309.17082；代码：https://github.com/Anguswlx/DMasSQ；期刊：https://doi.org/10.1007/JHEP05(2024)060。PDF SHA-256：3c6e52dcbf2a73118d59cb87490bb843ddbebce1e46c73b93f68caa144f242bc。", r"复现需固定 φ4 action convention、κ/λ/L、training ensemble、U-Net、noise schedule、likelihood estimator probes、MH kernel、burn-in、tmax/windowing 与三种算法的 cost accounting。", r"Evidence status: full-text verified version of record/arXiv v2; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.3–10 的 SQ 与 diffusion correspondence，再看 pp.13–18 的 φ4 setup、两相 distributions 与 likelihood。核心效率证据是 pp.18–20 的 Figure 8、τint 和 Figure 9；附录 acceptance scans 用来判断参数敏感性。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1007-jhep05-2024-060/figure-8-autocorrelation.webp", "label": "Figure 8", "visual_type": "data_plot", "evidence": "paper.pdf p. 19, Figure 8", "alt_text": "局域 MC、HMC 和 DM-MC 的归一化磁化 autocorrelation 曲线。", "caption": "在该临界参数与有限样本设置中，DM 全局 proposals 比 local MC 和 HMC 更快 decorrelate。", "selection_rationale": "Figure 8 是论文性能主张的直接数据证据，并清楚显示比较对象和有限 Monte Carlo time window。"},
        "figure_refs": [figure("doi-10.1007-jhep05-2024-060", "figure-8-autocorrelation.webp", "Figure 8", 19, "compare critical-region autocorrelation", "三种 sampler 的 |M| normalized autocorrelation。", "DM-MC 在该测试中几步内 decorrelates。", "The plot uses 1024 samples at one finite lattice and excludes training-cost accounting.")],
        "equation_refs": [
            {"label": "DM proposal acceptance", "latex": r"p_{\rm accept}=\min\!\left(1,\frac{q(\phi_{i-1})p(\phi_{\rm prop})}{p(\phi_{i-1})q(\phi_{\rm prop})}\right)", "role": "make the learned global proposal an MH chain", "symbols": {"p": "target Boltzmann density", "q": "DM likelihood"}, "evidence": "paper.pdf p. 18, Eq. (4.13)", "interpretation": "Likelihood access lets the learned generator propose global moves while MH corrects its density mismatch."},
            {"label": "Integrated autocorrelation", "latex": r"\tau_{O,\mathrm{int}}=\frac12+\frac1{C_O(0)}\sum_{t=1}^{t_{\max}}C_O(t)", "role": "quantify sampler correlation length", "symbols": {"O": "observable", "t_max": "finite summation window"}, "evidence": "paper.pdf p. 19, Eq. (4.14)", "interpretation": "Reported values depend on the finite window and sample, so uncertainty/window diagnostics remain necessary."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–10: SQ and diffusion derivation", "paper.pdf pp. 13–18: phi4 setup and distribution tests", "paper.pdf pp. 18–20: Figure 8, integrated autocorrelations and limitations", "source PDF SHA-256 3c6e52dcbf2a73118d59cb87490bb843ddbebce1e46c73b93f68caa144f242bc", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1007-s00205-023-01903-7", "source_version": "arXiv v2 / open-access version of record", "source_pdf": "https://arxiv.org/pdf/2109.06500v2",
        "title_en": "The Dean–Kawasaki Equation and the Structure of Density Fluctuations in Systems of Diffusing Particles", "title_zh": "Dean–Kawasaki 方程与扩散粒子系统的密度涨落结构",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["ec6401f3ac40453e"], ["Statistical Physics"]),
        "verified_metadata": {"doi": "10.1007/s00205-023-01903-7", "arxiv_id": "2109.06500", "version": "v2 / version of record", "title": "The Dean–Kawasaki Equation and the Structure of Density Fluctuations in Systems of Diffusing Particles", "authors": ["Federico Cornalba", "Julian Fischer"], "categories": ["math.AP", "math.NA", "math.PR"], "primary_category": "math.AP", "published": "2021-09-14T07:56:35Z", "abstract": "Structure-preserving finite-difference and finite-element regularizations approximate fluctuations of independent diffusing particles to arbitrarily high order in suitable weak metrics.", "comment": "Archive for Rational Mechanics and Analysis 247, 76 (2023); open access"},
        "sections": [
            sec("作者信息", r"作者：Federico Cornalba、Julian Fischer；Archive for Rational Mechanics and Analysis 247, 76 (2023)，DOI:10.1007/s00205-023-01903-7；arXiv:2109.06500v2。全文 56 页，含严格定理、有限差分/有限元版本与数值检查。"),
            sec("研究问题", r"连续 Dean–Kawasaki SPDE 含 sqrt(ρ) 的乘性时空白噪声，极其奇异：已知非平凡 martingale solutions 只能是 N 个 Brownian particles 的经验测度，非整数 N 甚至无解。论文问：若把数值离散化本身视为自然 regularization，这个 SPDE 能否仍作为高精度模拟密度涨落的有效 recipe？"),
            sec("背景", r"N 个独立扩散粒子的经验密度涨落尺度为 N^{-1/2}。线性化 fluctuating hydrodynamics 只正确捕捉 leading fluctuation，弱误差通常止于 N^{-1}；非线性 sqrt(ρ) 噪声可能编码更高阶统计。", r"关键不是给奇异 continuum SPDE 构造普通函数解，而是比较 structure-preserving discrete SPDE 与粒子经验测度在 negative-Sobolev-type weak metrics 下的 laws。"),
            sec("模型与方法", r"作者研究 periodic domain 上的 finite-difference 与 finite-element schemes，保持离散 Laplacian、divergence/noise covariance 的 fluctuation–dissipation structure。Theorems 2/19 比较多时刻测试函数 observables 的概率律；Theorems 3/20 比较任意阶 centered moments。", r"误差分为三类：negative-density event、spatial discretization h^{p+1}、relative fluctuation N^{-j/2}。在平均每 cell 粒子数足够大、粗略为 h≫N^{-1/d} 时，negative part 概率呈指数小。"),
            sec("核心结果与证据", r"主 bound 表明对任意 j，离散 Dean–Kawasaki fluctuations 可在合适弱 metric 中达到 N^{-j/2} 的任意高阶相对精度，最终限制来自 h-discretization 与 rare negativity；这比只保留 leading Gaussian fluctuation 的线性化模型包含更多统计结构。", r"“arbitrary order” 是随 j 增加、同时要求更平滑 test functions 和相应 constants 的渐近 statement，不是固定网格上对所有 observables 的 uniform error。", r"Figure 4 对两个 initial-data examples 和多组 centered moments 给出 log–log error 对 h；初始 preasymptotic 后呈约 O(h²) 斜率。Figures 5–6 再检查 N-scaling 以及线性化模型的 saturation。"),
            sec("有效性与局限", r"严格结果针对无相互作用 Brownian particles、周期域、正且正则的 macroscopic initial density 和特定 mesh/noise assumptions。弱 metric 只测试有限组平滑 observables，不提供 pointwise density path 的强收敛。", r"h≫N^{-1/d} 是每 cell 平均粒子数大于一的 regime；更细网格下直接粒子模拟反而可能更便宜。非线性 discrete density 仍可能短暂为负，论文只给 exponentially small a posteriori control，并未构造一般连续 Dean–Kawasaki solution。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2109.06500；开放期刊：https://doi.org/10.1007/s00205-023-01903-7。核验 PDF SHA-256：30e771abf4c82fcd2373c555489e07ecf63699585c594ef5f63a9dc262a7281c。", r"复核需固定 d、periodic mesh、N/h scaling、initial density lower bound、discrete operators/noise basis、time integrator、test functions、weak metric order j 和 negative-part stopping/control。", r"Evidence status: full-text verified open-access article; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.1–3 的 continuum obstruction、Eqs. (1)–(5) 与 scaling regime；再读 pp.4–7 的 Theorems 2–3 和误差分解。证明路线看 pp.9–15，数值 evidence 直接看 pp.38–44 的 Figures 1–6；附录给 finite-element counterpart。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1007-s00205-023-01903-7/figure-4-convergence.webp", "label": "Figure 4", "visual_type": "data_plot", "evidence": "paper.pdf p. 42, Figure 4", "alt_text": "多阶矩误差随网格 h 的双对数曲线及二阶参考斜率。", "caption": "经过 preasymptotic 区后，离散 Dean–Kawasaki moment errors 呈约 O(h²) 收敛。", "selection_rationale": "Figure 4 直接检验理论中的 numerical-discretization error，而不是只展示一条 stochastic sample path。"},
        "figure_refs": [figure("doi-10.1007-s00205-023-01903-7", "figure-4-convergence.webp", "Figure 4", 42, "verify spatial convergence of fluctuation moments", "不同 centered moments 的 weak error 对 h 的 log-log plots。", "曲线在初始过渡后跟随二阶参考斜率。", "This verifies selected examples and observables, not the full theorem independently.")],
        "equation_refs": [
            {"label": "Dean–Kawasaki equation", "latex": r"\partial_t\rho=\tfrac12\Delta\rho+N^{-1/2}\nabla\!\cdot(\sqrt\rho\,\xi)", "role": "model finite-particle density fluctuations", "symbols": {"rho": "density field", "xi": "vector space-time white noise"}, "evidence": "paper.pdf p. 1, Eq. (1)", "interpretation": "The multiplicative conservative noise encodes fluctuation structure but makes the continuum equation singular."},
            {"label": "Weak fluctuation error", "latex": r"d_{\rm weak,2j-1}(\rho_h-E\rho_h,\mu^N-E\mu^N)\lesssim C(j)E\|\rho_h^-\|+h^{p+1}+N^{-j/2}", "role": "separate negativity, discretization and fluctuation errors", "symbols": {"h": "mesh scale", "j": "weak-metric/order parameter"}, "evidence": "paper.pdf p. 2, Eq. (3); pp. 4–6, Theorem 2", "interpretation": "High order in N is obtained in increasingly weak/smooth-test metrics and remains limited by mesh and negativity errors."},
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: singular continuum equation and main scaling", "paper.pdf pp. 4–7: Theorems 2–3 and error decomposition", "paper.pdf pp. 38–44: Figures 1–6 numerical convergence tests", "source PDF SHA-256 30e771abf4c82fcd2373c555489e07ecf63699585c594ef5f63a9dc262a7281c", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "doi-10.1007-s10955-014-1008-9", "source_version": "arXiv v2 / version of record", "source_pdf": "https://arxiv.org/pdf/1403.2364v2",
        "title_en": "Motility-Induced Phase Separation of Active Particles in the Presence of Velocity Alignment", "title_zh": "存在速度对齐时主动粒子的运动诱导相分离",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["802e950118ecc5be"], ["Active Matter"]),
        "verified_metadata": {"doi": "10.1007/s10955-014-1008-9", "arxiv_id": "1403.2364", "version": "v2 / version of record", "title": "Motility-Induced Phase Separation of Active Particles in the Presence of Velocity Alignment", "authors": ["Julien Barré", "Raphaël Chétrite", "Massimiliano Muratori", "Fernando Peruani"], "categories": ["physics.bio-ph", "cond-mat.soft"], "primary_category": "physics.bio-ph", "published": "2014-03-10T19:45:54Z", "abstract": "A coarse-grained entropy functional for density-dependent-speed particles with velocity alignment predicts MIPS inside the orientationally disordered phase and alignment-sensitive spinodals.", "comment": "Journal of Statistical Physics 158, 589–600 (2015)"},
        "sections": [
            sec("作者信息", r"作者：Julien Barré、Raphaël Chétrite、Massimiliano Muratori、Fernando Peruani；Journal of Statistical Physics 158, 589–600 (2015)，DOI:10.1007/s10955-014-1008-9；arXiv:1403.2364v2。全文 15 页。"),
            sec("研究问题", r"密度升高会降低 self-propelled particles 的 speed，从而产生 MIPS；但许多 active systems 还存在 velocity alignment，并在更强 alignment 时出现 orientational order。论文问：在尚未有极性序的 disordered phase，是否仍可导出 entropy-like functional，以及 alignment 如何移动 spinodal、critical diffusion 和 density fluctuations？"),
            sec("背景", r"模型包含 density-dependent speed v(ρ)、angular diffusion Dθ、spatial diffusion Dx 与 alignment sensitivity γ。作者从 microscopic Langevin/Fokker–Planck description 做 angular Fourier expansion，并以极化场相对密度的快弛豫将其绝热消去。", r"Figure 1 是固定密度下的示意 phase diagram：γ/Dθ<2 为 disordered regime，红色 spinodal 随 alignment 增强上升；其右侧 ordered region 不在本文 entropy closure 的适用域。"),
            sec("模型与方法", r"保留 density 和 polar mode，忽略更高 angular modes/gradients 后得到含 finite-N noise 的 density SPDE。通过 functional Fokker–Planck equation 寻找零流 stationary measure μ[ρ]∝exp[-NS[ρ]]，并假设局域 functional S=∫dx s(ρ)。", r"所得 s''(ρ) 同时含 v²+ρvv'、Dx、noise mobility b[ρ] 与 alignment denominator 1-γ/(2Dθ)。选择 v(ρ)=exp(-λρ) 后可显式求 spinodal s''=0 和 critical point。"),
            sec("核心结果与证据", r"主要分析结果是 disordered phase 内存在 entropy-like local functional；当 γ=0 时退化到无 alignment 的 MIPS 条件 dv/dρ=-v/ρ。alignment 改变 spinodal 与 binodal，因此 MIPS 可先于 orientational-order transition 出现。", r"对 exponential speed，spinodal 为 Dx^sp=e^{-2λρ}(λρ-1)/(2-γ/Dθ)，critical density ρc=3/(2λ)，critical diffusion 约为 0.0249/(2-γ/Dθ)。这些式子来自 closure，靠近 γ=2Dθ 时分母发散正提示 approximation 失效。", r"density fluctuations 随 s''→0 增强；作者只能可靠判断 approaching order 时 fluctuations 与 critical diffusion 增大，不能保证在 transition 邻域按近似公式真正发散。"),
            sec("有效性与局限", r"time-scale separation、polar truncation 和 smooth differentiable v(ρ) 只在 orientationally disordered phase 可信，不能描述 sharp exclusion interfaces 或 ordered patterns。density equation 对 microscopic dynamics 的精确性只在 infinite-N/infinite-density limit 成立。", r"entropy-like stationary functional 不把整个 active system 变成 equilibrium，也不证明 detailed balance 对所有 microscopic variables 成立。Figure 1 是近似理论示意而非直接 simulation fit；ordered phase 的 phase separation 可能有不同机制。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/1403.2364；期刊：https://doi.org/10.1007/s10955-014-1008-9。核验 PDF SHA-256：81edfe41f2ee9d85bbe8d6a40a6a633d5150d229c9e8d2807dcfaa4f49907e15。", r"复核需固定 microscopic SDE、Ito convention、angular-mode truncation、N/density limit、v(ρ)、γ/Dθ、Dx nondimensionalization、boundary conditions 与 spinodal/binodal construction。", r"Evidence status: full-text verified theory; no independent reproduction performed."),
            sec("阅读指南", r"先读 pp.2–5 的 microscopic model 和 coarse graining，再读 pp.7–9 的 functional Fokker–Planck 与 Eqs. (25)–(27)。核心物理读 pp.10–12 的 Figures 1–2、Eq. (28) 与 caution paragraph；不要把 disordered-phase divergence 外推进 ordered phase。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/doi-10.1007-s10955-014-1008-9/figure-1-phase-diagram.webp", "label": "Figure 1", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 10, Figure 1", "alt_text": "空间扩散对 alignment ratio 的示意相图，区分 homogeneous、MIPS 与 ordered regions。", "caption": "在 disordered phase 内，alignment 将 MIPS spinodal 推向更大的 spatial diffusion；order boundary 附近近似失效。", "selection_rationale": "Figure 1 凝练展示 MIPS 先于取向有序以及 spinodal 对 alignment 的敏感性，同时把理论适用边界画在图上。"},
        "figure_refs": [figure("doi-10.1007-s10955-014-1008-9", "figure-1-phase-diagram.webp", "Figure 1", 10, "summarize MIPS and ordering boundaries", "Dx 对 gamma/Dtheta 的 homogeneous、MIPS、order 示意相图。", "alignment-sensitive spinodal 位于 orientationally disordered region。", "The dashed divergence is an approximation and is not controlled at the order-disorder boundary.")],
        "equation_refs": [
            {"label": "Entropy curvature", "latex": r"s''(\rho)=-\frac{v^2(\rho)+\rho v(\rho)v'(\rho)}{(1-\bar\gamma/2)b[\rho]}+\frac{2D_x}{b[\rho]}", "role": "determine stability and density fluctuations", "symbols": {"bar_gamma": "gamma/Dtheta", "b": "density-noise mobility"}, "evidence": "paper.pdf p. 9, Eq. (27)", "interpretation": "The zero of s'' defines the approximate spinodal inside the disordered-phase closure."},
            {"label": "Exponential-speed spinodal", "latex": r"D_x^{\rm sp}(\rho)=\frac{e^{-2\lambda\rho}(\lambda\rho-1)}{2-\bar\gamma}", "role": "show alignment dependence of MIPS instability", "symbols": {"lambda": "speed-density decay rate", "bar_gamma": "alignment-to-angular-noise ratio"}, "evidence": "paper.pdf p. 11, Eq. (28)", "interpretation": "The apparent divergence near bar_gamma=2 lies exactly where the eliminated polar mode ceases to be fast."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: microscopic dynamics and density closure", "paper.pdf pp. 7–9: entropy functional and Eq. (27)", "paper.pdf pp. 10–12: Figures 1–2, spinodal and validity warning", "source PDF SHA-256 81edfe41f2ee9d85bbe8d6a40a6a633d5150d229c9e8d2807dcfaa4f49907e15", "Evidence status: full-text verified theory; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        card_id = str(card["arxiv_id"]).replace("/", "-")
        (OUT / f"{card_id}.json").write_text(
            json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        installed.append(card_id)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
