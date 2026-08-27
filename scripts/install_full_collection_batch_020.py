#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 020."""

from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import figure, meta, provenance, sec

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS: list[dict[str, object]] = [
    {
        "arxiv_id": "2507.07669", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2507.07669",
        "title_en": "Universal Spin Models are Universal Approximators in Machine Learning",
        "title_zh": "普适自旋模型也是机器学习中的普适逼近器",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["bd393ea82f3f94bc"], ["Machine Learning"]),
        "verified_metadata": meta(
            "2507.07669", "v2",
            "Universal Spin Models are Universal Approximators in Machine Learning",
            ["Tobias Reinhart", "Gemma De les Coves"],
            ["cond-mat.dis-nn"], "cond-mat.dis-nn", "2025-07-10T11:50:41Z",
            "Universal classical spin models are proved to approximate arbitrary probability distributions, transferring a structural universality criterion to RBMs, DBMs and DBNs.",
        ),
        "sections": [
            sec("作者信息", r"作者：Tobias Reinhart、Gemma De les Coves；arXiv:2507.07669v2。全文 10 页。工作把统计物理中“低能谱模拟任意自旋模型”的 universality 与机器学习中“逼近任意概率分布”的 universality 联系起来，并给出 RBM、常宽 DBM 与 DBN 的构造性推论。"),
            sec("研究问题", r"物理中的 universal spin model 能在截止能量 \(\Delta\) 以下重现任意目标 Hamiltonian；机器学习中的 universal approximator 则要求可把任意离散概率分布逼近到任意精度。论文问：这两种独立出现的“普适性”是否由同一个结构机制保证，以及如何把已知自旋模型分类直接转成能量模型的 universal approximation theorem？"),
            sec("背景", r"对有限自旋系统，Boltzmann 分布为 \(p(s)=e^{-H(s)}/Z\)。若 source system 在低能区逐态、唯一地复制 target energies，而其他构型被推到 \(\Delta\) 以上，则边缘 Boltzmann 分布只留下 \(O(e^{-\Delta})\) 的高能误差。关键对象是 flag system：隐藏自旋标记物理构型是否等于给定 \(x\)。", r"Figure 1 把全文逻辑压缩成一张映射图：左侧一个能模拟多类局域自旋系统的 universal spin model，经由 Boltzmann 权重，转化为右侧能生成任意离散分布的 universal approximator。"),
            sec("模型与方法", r"作者定义两个结构条件：flag completeness 要求模型可为任意 \(x\) 构造 flag；closure 要求具有不相交 flag spins 的系统可作任意非负线性组合。Theorem 1 证明二者对自旋模型 universality 既充分又必要。构造中，目标函数被拆成低能构型对应的加权 flags，再按局域能量项分解以控制辅助自旋数量。", r"RBM 的 Hamiltonian 写成 \(H(v,h)=v^\top b_v+h^\top b_h+v^\top Wh\)。一个隐藏节点即可 flag 一个可见构型，因此 RBM 满足两条件；DBM 通过 copy system 在层间传播构型并保持常宽。任意分布 \(p(t)>0\) 被编码为目标能量 \(-\log p(t)\)，零概率态置于高能区。"),
            sec("核心结果与证据", r"Figure 1 说明该证明不是“神经网络像自旋系统”的类比，而是低能模拟与概率边缘之间的严格函子式传递：同一组 flag/closure 条件同时控制 Hamiltonian 可表达性与分布可表达性。", r"Theorem 4 给出核心结论：任何 universal spin model 都是概率分布的 universal approximator。由此 RBM 与 DBM 立即得到统一证明；RBM 模拟含 \(k\) 个低能构型的函数需要 \(k\) 个隐藏 spins，常宽 DBM 可用宽度 \(n+1\)、\(k\) 个隐藏层处理 \(n\) 个可见 spins。", r"把目标按局域项 \(T=\sum_e T_e\) 分解后，辅助 spins 的构造开销从直接枚举的 \(O(2^{|V_T|})\) 降为 \(O(\sum_e2^{|e|})\)，对局域相互作用可为多项式。论文进一步以 effectively directional DBMs 证明常宽 DBN 也具 universal approximation 能力。"),
            sec("有效性与局限", r"这是有限离散自旋与任意大耦合/截止能量下的 representability theorem，不是优化、泛化或采样效率定理。\(O(e^{-\Delta})\) 精度要求增大能隙，可能导致参数尺度、混合时间与数值条件恶化；构造性上界也不代表最小网络。", r"证明依赖模型对 flag systems 的精确实现和非负线性组合闭合；连续变量、受限精度、稀疏参数、量子模型或局部学习规则需要另行处理。DBN 的结论还通过特定 effectively directional DBM 构造获得，不能推出任意训练所得 DBN 都具有有效表达或可训练性。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2507.07669。全文 10 页，PDF SHA-256：bd393ea82f3f94bc3c7a8b171a2dec4c3d06015dceaa598ab77747546a812f6f。", r"复核证明时应固定自旋取值约定、energy shift、cutoff \(\Delta\)、physical/auxiliary spin partition、flag truth states、零概率态处理与边缘化顺序。可从一个三比特目标 Hamiltonian 开始，逐态检查低能谱、partition function 与 \(O(e^{-\Delta})\) 误差。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1 和 simulation definition，明确“低能逐态复制”比只匹配 ground state 更强；再读 Theorem 1 的 flag completeness/closure 构造。随后核对 RBM 与常宽 DBM 的 flags，最后读 Theorems 4、6，并始终把表达普适性与训练可达性、采样复杂度分开。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2507.07669/figure-1-universality-map.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 1, Figure 1", "alt_text": "普适自旋模型经低能模拟映射到可生成多类概率分布的普适逼近器。", "caption": "低能 Hamiltonian 模拟通过 Boltzmann 权重转化为概率分布逼近；图示表达结构定理而非训练算法。", "selection_rationale": "Figure 1 是全文最重要且最直观的概念图，优先于后续代数构造。"},
        "figure_refs": [figure("2507.07669", "figure-1-universality-map.webp", "Figure 1", 1, "show the bridge between physical and machine-learning universality", "A universal spin model is mapped to a universal approximator over probability distributions.", "Low-energy simulation transfers to distributional approximation through Boltzmann marginals.", "The diagram does not address optimization, sampling or finite-precision efficiency.")],
        "equation_refs": [
            {"label": "RBM Hamiltonian", "latex": r"H(v,h)=v^\top b_v+h^\top b_h+v^\top Wh", "role": "realize configuration flags with visible-hidden couplings", "symbols": {"v": "visible spins", "h": "hidden spins", "W": "coupling matrix"}, "evidence": "paper.pdf p. 3, Eq. (7)", "interpretation": "A single hidden spin can flag one visible configuration; sums of disjoint flags remain RBMs."},
            {"label": "Distribution-to-energy encoding", "latex": r"H_T(t)=-\log p(t),\qquad \|p_M-p\|=O(e^{-\Delta})", "role": "turn low-energy simulation into probability approximation", "symbols": {"Delta": "simulation energy cutoff", "p_M": "visible marginal of the simulating model"}, "evidence": "paper.pdf pp. 4–5, Theorem 4 and Lemmas 2–3", "interpretation": "Increasing the cutoff suppresses unwanted high-energy configurations exponentially."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: simulation, flags, closure and RBM/DBM constructions", "paper.pdf pp. 4–6: universal approximation and DBN extension", "source PDF SHA-256 bd393ea82f3f94bc3c7a8b171a2dec4c3d06015dceaa598ab77747546a812f6f", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2508.14807", "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/2508.14807",
        "title_en": "Source-Guided Flow Matching",
        "title_zh": "源分布引导的流匹配",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["c1198d82f39f1679"], ["Flow Matching"]),
        "verified_metadata": meta(
            "2508.14807", "v2", "Source-Guided Flow Matching",
            ["Zifan Wang", "Alice Harting", "Matthieu Barreau", "Michael M. Zavlanos", "Karl H. Johansson"],
            ["cs.LG"], "cs.LG", "2025-08-20T15:56:25Z",
            "Guidance is moved from the learned vector field to a reweighted source distribution, preserving the pretrained transport map and enabling sampler-specific tradeoffs.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zifan Wang、Alice Harting、Matthieu Barreau、Michael M. Zavlanos、Karl H. Johansson；arXiv:2508.14807v2。全文 30 页。论文含精确输运定理、Wasserstein 误差界，以及二维分布、Darcy PDE inverse problem、CelebA imaging inverse problems 的数值验证。"),
            sec("研究问题", r"传统 guidance 在每个 flow time \(t\) 上给预训练 vector field 加一个条件漂移，既改变原有 transport geometry，也可能要求多次 Monte Carlo/梯度评估。论文问：能否保持 \(v_t\) 完全不变，只重新采样 source distribution，使同一 flow map 精确到达能量重加权后的 target distribution？"),
            sec("背景", r"无引导流把 \(q_0\) 经 \(T=\phi_1\) 推到 \(q_1\)。若目标希望偏向低能 \(J(x_1)\) 的样本，则 \(q'_1(x_1)\propto q_1(x_1)e^{-J(x_1)}\)。SGFM 把同一权重拉回 source：\(q'_0(x_0)\propto q_0(x_0)e^{-J(T(x_0))}\)，把 guidance 变成单一时刻的 sampling problem。", r"Figure 1/2 将区别画清：修改 vector field 会弯曲 trajectories；修改 source weights 则保留 optimal map 的直线配对，只改变哪些 source points 被频繁采样。"),
            sec("模型与方法", r"Theorem 1 用 pushforward 直接证明 \((\phi_1)_\#q'_0=q'_1\)。实际算法先训练普通 flow-matching \(v_t^\theta\)，再用 importance sampling、ULA/HMC 或 optimization 从近似 \(q'_0\) 取样，最后沿不改动的 ODE 积分。若采用 optimal flow matching，直线 transport 可减少 NFE。", r"Theorem 2 同时传播两类误差：若 vector-field uniform error 为 \(\epsilon\)、学习流为 \(L_v\)-Lipschitz，而 sampler 输出 \(\tilde q_0\)，则最终 \(W_2\) 偏差受 source mismatch 与 drift error 的指数放大共同控制。"),
            sec("核心结果与证据", r"Figure 1/2 显示 SGFM 的物理含义是改变初始 ensemble，而不是在路径中持续施力；对 optimal map，这保留 Wasserstein-geodesic 式直线轨迹。该图也提示失败条件：source reweighting 若高度集中，会把 sampling 难题前移而非消除。", r"二维实验中，importance-sampling 样本数增大时 Wasserstein error 持续下降，并且减少 NFE 对直线流影响较小。Darcy inverse problem 的 25-sample 中位数显示 SGFM-OPT-\(\chi^2\) validity 0.474，优于 SGFM-HMC 0.591、SGFM-OPT 0.907、\(g^{\rm cov-A}\) 0.993；但它不是所有 physical-consistency 指标都唯一最好。", r"CelebA 五类 inverse tasks 中，各 SGFM-OPT variant 均优于表中的 \(g\)-cov baselines；例如 super-resolution PSNR 最高约 33.33，而 PnP 为 31.33。PnP 在 deblurring 达 38.74，高于 SGFM 约 35.27，说明通用框架并非每个专用任务最优。"),
            sec("有效性与局限", r"精确性依赖 exact map \(T\) 与 exact \(q'_0\) sampler；在高维中二者都不可得。误差界含 \(e^{L_v}\)，高敏感流可显著放大 source 和 drift 偏差。optimization sampler 可能 mode collapse，少量逆问题样本也不足以证明覆盖全部后验解。", r"作者明确指出反向传播 through ODE 导致长 runtime；optimal vector field 需要 OT coupling，而 minibatch/entropic OT 近似会引入 bias 且难扩展。不同 sampler 的 cost、accuracy 与 diversity tradeoff 需按问题重做，实验没有给出一般最优选择。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2508.14807。全文 30 页，PDF SHA-256：b5a1a5a62f7964719cf2d5354ca17edb38b9304b12586dbe33871c23ca07a170。", r"复现需固定 source/target pairing、flow architecture、OT approximation、ODE solver/NFE、\(J\) 与 normalization、IS/HMC/ULA/optimization sampler、Darcy 64×64 finite-difference data、CelebA degradation operators 和 metric sample counts。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figures 1–2，把“改路径”与“改初态 ensemble”区分开；再读 Theorems 1–2，检查 pushforward 与误差放大项。随后比较 Darcy Table 1 和 CelebA Table 2，最后读 Appendix D 的 runtime/OT-coupling limitations，避免把 exact theorem 外推到近似高维采样。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2508.14807/figure-1-source-guidance.webp", "label": "Figures 1–2", "visual_type": "schematic", "evidence": "paper.pdf p. 5, Figures 1–2", "alt_text": "SGFM 通过重加权源分布保留直线最优输运，而对照方法修改向量场并形成弯曲轨迹。", "caption": "引导被移到初始 ensemble：保持预训练 flow map，不在中途改变向量场。", "selection_rationale": "Figures 1–2 是全文最重要的机制可视化，优先于逆问题数值表。"},
        "figure_refs": [figure("2508.14807", "figure-1-source-guidance.webp", "Figures 1–2", 5, "contrast source reweighting with vector-field guidance", "Source weights change while the optimal transport trajectories remain straight.", "SGFM converts guidance into sampling from a modified initial ensemble.", "The schematic assumes an accurate transport map and does not show high-dimensional sampling cost.")],
        "equation_refs": [
            {"label": "Exact source reweighting", "latex": r"q'_1(x_1)=Z_1^{-1}q_1(x_1)e^{-J(x_1)},\qquad q'_0(x_0)=Z_0^{-1}q_0(x_0)e^{-J(T(x_0))}", "role": "pull target guidance back through the transport map", "symbols": {"T": "time-one flow map", "J": "guidance energy"}, "evidence": "paper.pdf p. 4, Theorem 1", "interpretation": "The unchanged flow transports the reweighted source exactly to the reweighted target."},
            {"label": "Approximate-guidance error bound", "latex": r"W_2\!\left(q'_1,[\phi^\theta_1]_\#\tilde q_0\right)\le e^{L_v}W_2(q'_0,\tilde q_0)+\epsilon e^{L_v}", "role": "separate sampler and vector-field errors", "symbols": {"epsilon": "uniform vector-field error", "L_v": "Lipschitz constant", "tilde_q0": "sampler output distribution"}, "evidence": "paper.pdf p. 4, Theorem 2", "interpretation": "Both initial-distribution mismatch and drift error can be amplified by a sensitive flow."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–5: exact source guidance and Wasserstein bound", "paper.pdf pp. 8–10: 2D, Darcy and CelebA results", "paper.pdf pp. 28–29: limitations", "source PDF SHA-256 b5a1a5a62f7964719cf2d5354ca17edb38b9304b12586dbe33871c23ca07a170", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2509.21519", "source_version": "v5",
        "source_pdf": "https://arxiv.org/pdf/2509.21519",
        "title_en": "Provable Scaling Laws of Feature Emergence from Learning Dynamics of Grokking",
        "title_zh": "从顿悟学习动力学推导特征涌现的可证明标度律",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["785b72b087f4ceeb"], ["Training Dynamics"]),
        "verified_metadata": meta(
            "2509.21519", "v5",
            "Provable Scaling Laws of Feature Emergence from Learning Dynamics of Grokking",
            ["Yuandong Tian"], ["cs.LG", "cs.AI"], "cs.LG", "2025-09-25T20:08:09Z",
            "The Li2 framework separates grokking into lazy, independent-feature and interactive-feature stages and derives sample-size and optimizer-dependent feature-emergence laws.",
        ),
        "sections": [
            sec("作者信息", r"作者：Yuandong Tian；arXiv:2509.21519v5。全文 51 页。论文提出 \(\mathbf{Li}_2\) 三阶段框架，围绕二层非线性网络和群运算任务，从梯度动力学解释 grokking、特征局部极值、样本复杂度与 Muon 的作用。代码链接由作者在正文给出。"),
            sec("研究问题", r"grokking 表现为训练集先拟合、测试集很久后突然泛化。已有相变或表示观察不能完整回答：哪些 feature 会从梯度流中出现，何时稳定，样本数、weight decay、learning rate 与节点相互作用如何控制从 memorization 到 generalization 的延迟？"),
            sec("背景", r"模型先用随机 hidden features 做 ridge-regression 式记忆；当 output layer 拟合后，回传梯度 \(G_F\) 开始携带标签结构。作者把后续 feature dynamics 写成一个能量函数 \(\mathcal E\) 的 gradient ascent，其 local maxima 对应可学习特征。", r"Figure 1 将时间轴分成三段：I lazy learning 对应 sharp-optimum memorization；II 各 hidden node 沿 \(\mathcal E\) 独立学习；III 节点相互作用后补足缺失 features，并进入较平坦的 generalizing solution。"),
            sec("模型与方法", r"研究对象是二层网络 \(f(x)=W_2\sigma(W_1x)\)，以 centered feature matrix \(F\) 与 backpropagated signal \(G_F\) 描述表示动力学。Stage II 中每个节点近似独立，方向更新等价于最大化 nonlinear CCA 型能量 \(\mathcal E(w)\)；群算术与平方激活允许解析分类 local maxima。", r"作者进一步证明：若训练样本足够，population-energy 的 local maxima 在 empirical energy 中保持；Stage III 的 feature correlations 产生 repulsion，top-down modulation 将梯度集中到尚未学习的 Fourier/group features，Muon 的极分解更新可重新平衡不同奇异方向。"),
            sec("核心结果与证据", r"Figure 1 的价值在于给 grokking 一个可检验的因果顺序：先由随机特征记忆并形成标签相关 \(G_F\)，再出现独立 feature learning，最后才有交互式 feature completion；它不是单一 loss curve 的事后分段。", r"对阶为 \(M\) 的群运算，Theorem 4 给出保持一个 feature local optimum 所需样本量 \(n\gtrsim d_k^2M\log(M/\delta)\)。因此训练比例 \(p=n/M^2\sim M^{-1}\log M\)，Figure 5 的 modular-addition 相变在 20 seeds 上与该边界吻合。", r"Figure 3 在 \(M=71,K=2048,n=2016\) 下显示 \(\eta=2\times10^{-4}\) 时约 epoch 100 后 \(G_F\) 增强并发生 grokking，而 \(\eta=0\) 不发生；Figure 6 的 15-seed 实验还显示临界区较小 learning rate 更易落入 generalizable solution。"),
            sec("有效性与局限", r"严格局部极值与样本标度主要在群算术、特定激活和二层网络中证明；\(\mathcal E\) 的一般定义可扩展，但一般数据上的 local maxima 结构未被分类。多层扩展、真实语言模型与 finite-width stochastic optimization 仍主要是解释性外推。", r"作者明确指出当前理论没有统一覆盖所有 hyperparameter regimes；实验集中在 modular/group tasks，部分结论依赖近似独立节点、centering 与特定初始化。weight decay 是足够条件而非必要条件，Figure 3 的单一配置不能证明普遍因果。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2509.21519；代码：https://github.com/yuandong-tian/understanding/tree/main/ssl/real-dataset/cogo。全文 51 页，PDF SHA-256：9d4a6582703ee56209b08df5a3438a38586268b24b5d999b58de391b7c3ff88c。", r"复现需固定群 \(H\)、\(M,K,n\)、训练比例、activation、initialization scales、weight decay \(\eta\)、learning rate、optimizer、feature matching criterion、seed count 与 generalization threshold；应保存 \(G_F\)、权重差、特征相关矩阵和 train/test accuracy 全轨迹。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，建立三阶段动力学图；再读 Proposition 1/Lemma 1，理解 \(G_F\) 何时获得标签信号。随后读 Theorems 1–4 与 Figures 4–5，最后检查 Stage III 的 repulsion/top-down modulation 与 Muon theorem。不要把群算术中的可证 feature 直接等同于大模型语义特征。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2509.21519/figure-1-three-stage-grokking.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "从随机初始化，经懒惰学习、独立特征学习到交互特征学习的三阶段时间轴。", "caption": "grokking 被解释为从 sharp memorization 到独立、再到交互式特征涌现的动力学序列。", "selection_rationale": "Figure 1 是全文最清楚的机制总览，优先于多面板 loss 曲线。"},
        "figure_refs": [figure("2509.21519", "figure-1-three-stage-grokking.webp", "Figure 1", 2, "summarize the causal stages of grokking", "Training proceeds from random-feature memorization to independent and interactive feature learning.", "The framework assigns distinct gradient mechanisms to delayed generalization.", "The staged picture is rigorously specialized to the analyzed shallow-network settings.")],
        "equation_refs": [
            {"label": "Feature-energy dynamics", "latex": r"\dot w_j\propto\nabla_{w_j}\mathcal E(w_j)", "role": "describe independent feature emergence in Stage II", "symbols": {"w_j": "hidden-node direction", "mathcal_E": "nonlinear CCA-like energy"}, "evidence": "paper.pdf pp. 5–7, Eq. (6) and Theorem 1", "interpretation": "Stable local maxima of the energy landscape identify the features learned by individual hidden nodes."},
            {"label": "Feature-stability sample complexity", "latex": r"n\gtrsim d_k^2M\log(M/\delta),\qquad p=\frac{n}{M^2}\sim M^{-1}\log M", "role": "predict the generalization-memorization boundary", "symbols": {"M": "group order", "d_k": "representation dimension", "delta": "failure probability"}, "evidence": "paper.pdf p. 8, Theorem 4 and Figure 5", "interpretation": "The fraction of the full multiplication table needed for stable features decreases with group size."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–8: Li2 stages, energy landscape and sample law", "paper.pdf pp. 8–12: phase transitions, interaction dynamics and limitations", "source PDF SHA-256 9d4a6582703ee56209b08df5a3438a38586268b24b5d999b58de391b7c3ff88c", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2509.24882", "source_version": "v3",
        "source_pdf": "https://arxiv.org/pdf/2509.24882",
        "title_en": "Scaling Laws and Spectra of Shallow Neural Networks in the Feature Learning Regime",
        "title_zh": "特征学习区浅层神经网络的标度律与谱",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["e61f03c44e0d83b5"], ["Scaling Laws"]),
        "verified_metadata": meta(
            "2509.24882", "v3",
            "Scaling Laws and Spectra of Shallow Neural Networks in the Feature Learning Regime",
            ["Leonardo Defilippis", "Yizhou Xu", "Julius Girardin", "Emanuele Troiani", "Vittorio Erba", "Lenka Zdeborová", "Bruno Loureiro", "Florent Krzakala"],
            ["cs.LG", "cond-mat.dis-nn", "cs.AI", "stat.ML"], "cs.LG", "2025-09-29T14:58:13Z",
            "Matrix compressed sensing and LASSO reductions yield a phase diagram linking shallow-network excess-risk scaling to spikes, bulk spectra and heavy tails.",
        ),
        "sections": [
            sec("作者信息", r"作者：Leonardo Defilippis、Yizhou Xu、Julius Girardin、Emanuele Troiani、Vittorio Erba、Lenka Zdeborová、Bruno Loureiro、Florent Krzakala；arXiv:2509.24882v3。全文 53 页。论文分析 quadratic 与 diagonal shallow networks 的 feature-learning regime。"),
            sec("研究问题", r"经验 scaling laws 常把 loss 写成样本数或参数数的幂律，但非线性 feature learning 中为何会出现 plateau、crossover、double descent 与 weight-spectrum heavy tails 仍缺少统一推导。论文问：sample complexity \(n\)、维数 \(d\)、weight decay \(\lambda\) 如何共同决定 excess risk 和训练后谱？"),
            sec("背景", r"quadratic network 可把预测器写成低秩/半正定矩阵学习，并连接 matrix compressed sensing；diagonal network 则连接 LASSO。两者用有效样本数统一：diagonal 的 \(n_{\rm eff}=n\)，quadratic 的 \(n_{\rm eff}=n/d\)。teacher spectrum 假设满足幂律尾部，指数 \(\gamma\) 控制可恢复特征层级。", r"Figure 1 是全文主相图：横轴 \(n_{\rm eff}\)，纵轴 \(\lambda\)，六大区域同时标出 risk rate 与谱形——零峰、离散 spikes、连续 bulk 和 heavy tail。"),
            sec("模型与方法", r"作者以 high-dimensional state evolution/approximate message passing 给出 risk 与 spectrum 的 deterministic characterization，再在 \(n_{\rm eff},d\gg1\) 的不同标度区做渐近匹配。噪声强度 \(\Delta>0\)，正则项控制 soft-thresholding；Result 2 把学习权重谱表示为 noisy、thresholded teacher spectrum。", r"Result 3 将 excess risk 分为 bulk overfitting、未恢复特征的 underfitting 与已恢复 spikes 的 approximation error，从而把不同幂律区和谱拓扑一一对应；有限 \(d=100\)–800 的 simulations 与 non-asymptotic state-evolution 曲线比较。"),
            sec("核心结果与证据", r"Figure 1 把非单调风险解释成谱的重组：数据稀少时只有零峰/少量 spikes；接近 \(n_{\rm eff}\sim d\) 时 noise bulk 增强并产生 interpolation peak；更大样本下 outliers 重新分离，最终进入 heavy-tail/Bayes-optimal sector。", r"弱正则下，初始 fast-decay Phase IV 的 \(R\sim n_{\rm eff}^{-1+1/(2\gamma)}\) 在接近 \(d\) 时转入噪声主导 Phase V，risk 可在 \(n_{\rm eff}\sim d\) 附近达 \(R\sim\lambda^{-2/3}\)；随后 Phase VIa/VIb 恢复 \(R\sim d/n_{\rm eff}\)。强正则则经过 plateau Ib、慢速 II 与 \(R\sim\lambda^2d^2/n_{\rm eff}^2\) 的 Phase III。", r"Figure 2 的 \(d=800\) spectra 与理论 bulk/spike predictions 对齐；Figure 3 在 \(d=100,200,400,800\) 上显示 state evolution 与风险曲线良好吻合。只有 VIb 达 Bayes-optimal rate；论文据此给 heavy-tailed spectrum 与较好泛化一个模型内的第一性解释。"),
            sec("有效性与局限", r"核心 state-evolution 严格保证位于 proportional limit；把它延伸到跨越多个 \(n,d,\lambda\) 标度区是作者明确标注、由数值支持的 conjectural assumption，非完整非渐近定理。建立相应 multiplicative bounds 仍是开放问题。", r"结论针对平方/对角浅层模型、Gaussian-like design、特定 teacher spectral tail 与 ERM；不能直接覆盖深网络、SGD 动力学、分类 loss 或任意真实数据。谱 heavy tail 在该模型中与最佳区相关，不等于观测到 heavy tail 就能推出因果上的泛化优势。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2509.24882。全文 53 页，PDF SHA-256：d2b82fc0c490ca73e607d515807ea33a28817f9fc255c02f8bb8e136a7c10e56。", r"复现需固定 diagonal/quadratic parameterization、teacher spectrum 与 \(\gamma\)、\(\Delta,d,n,\lambda\) grid、state-evolution solver、ERM/LASSO tolerance、eigenvalue normalization 和 finite-size collapse。应分别保存 bulk、zero mass、outliers 与 risk decomposition。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，把每个 risk exponent 与谱形对应；再读 Results 1–3，而不是先陷入附录渐近展开。随后看 Figures 2–3 的有限尺寸证据，最后读 Section 2.4 的 conjecture，区分 proportional-limit 定理、跨标度推断和经验验证。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2509.24882/figure-1-risk-phase-diagram.webp", "label": "Figure 1", "visual_type": "phase_diagram", "evidence": "paper.pdf p. 6, Figure 1", "alt_text": "有效样本数与正则强度平面上的 excess-risk 区域及对应权重谱示意。", "caption": "风险标度与谱拓扑共享同一相图：plateau、overfitting bulk、outliers 和 heavy tails 对应不同学习区。", "selection_rationale": "Figure 1 同时承载论文的主要定量结果和物理直觉，是最重要的原文图。"},
        "figure_refs": [figure("2509.24882", "figure-1-risk-phase-diagram.webp", "Figure 1", 6, "connect risk scaling regimes to weight spectra", "A sample-size/regularization phase diagram labels risk exponents and spectral sketches.", "Crossovers in generalization coincide with changes between zero peaks, spikes, bulk and heavy tails.", "Several cross-regime rates rely on extending state evolution beyond its rigorously controlled proportional limit.")],
        "equation_refs": [
            {"label": "Effective sample size", "latex": r"n_{\rm eff}=\begin{cases}n,&\text{diagonal network},\\ n/d,&\text{quadratic network},\end{cases}", "role": "collapse two feature-learning models onto one phase diagram", "symbols": {"n": "number of samples", "d": "input dimension"}, "evidence": "paper.pdf p. 5, Eq. (10)", "interpretation": "Quadratic feature learning consumes an extra factor of dimension in sample complexity."},
            {"label": "Large-sample fast-decay rate", "latex": r"R_{n_{\rm eff},d}=\Theta(d/n_{\rm eff})\qquad(n_{\rm eff}\gg d,\ \lambda\ \text{weak})", "role": "identify the post-interpolation feature-learning regime", "symbols": {"R": "excess risk", "lambda": "weight decay"}, "evidence": "paper.pdf pp. 5–6, Result 1 and Figure 1", "interpretation": "After the noise-dominated crossover, additional samples separate informative outliers and reduce risk again."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: model reductions and phase diagram", "paper.pdf pp. 7–11: spectral decomposition, simulations and conjecture", "source PDF SHA-256 d2b82fc0c490ca73e607d515807ea33a28817f9fc255c02f8bb8e136a7c10e56", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2509.25300", "source_version": "v4",
        "source_pdf": "https://arxiv.org/pdf/2509.25300",
        "title_en": "Scaling Behaviors of LLM Reinforcement Learning Post-Training: An Empirical Study in Mathematical Reasoning",
        "title_zh": "大语言模型强化学习后训练的标度行为：数学推理实证研究",
        "curation_status": "full_text_verified", "card_standard_version": "2.3",
        "paper_profile": "ai_empirical", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance(["c6dc2d738541a81f"], ["Control & Reinforcement Learning"]),
        "verified_metadata": meta(
            "2509.25300", "v4",
            "Scaling Behaviors of LLM Reinforcement Learning Post-Training: An Empirical Study in Mathematical Reasoning",
            ["Zelin Tan", "Hejia Geng", "Xiaohang Yu", "Mulei Zhang", "Guancheng Wan", "Yifan Zhou", "Qiang He", "Xiangyuan Xue", "Heng Zhou", "Yutao Fan", "Zhongzhi Li", "Zaibin Zhang", "Guibin Zhang", "Chen Zhang", "Zhenfei Yin", "Philip Torr", "Lei Bai"],
            ["cs.LG", "cs.AI"], "cs.LG", "2025-09-29T17:10:35Z",
            "GRPO experiments across Qwen2.5 and Llama 3 families fit predictive resource-loss laws, reveal diminishing efficiency gains and quantify when data reuse remains effective.",
        ),
        "sections": [
            sec("作者信息", r"作者：Zelin Tan、Hejia Geng、Xiaohang Yu、Mulei Zhang、Guancheng Wan 等 17 位；arXiv:2509.25300v4。全文 21 页。研究以 GRPO 对 Qwen2.5 0.5B–72B dense models 做数学推理 post-training，并用 Llama 3 1B–70B 做跨架构检验。"),
            sec("研究问题", r"预训练 scaling laws 已较成熟，但 RL post-training 中模型大小 \(N\)、训练 FLOPs \(C\)、数据量 \(D\) 与重复使用如何共同控制 reasoning loss 尚不清楚。论文问：早期训练曲线能否预测后期和更大模型，larger model 的学习效率是否无限增长，以及数据稀缺时重复高质量样本何时有益或过拟合？"),
            sec("背景", r"主要指标定义为 test loss \(L=1-\mathrm{PassRate}\)，在固定 holdout math benchmark 上比较。作者将 compute-constrained、data-constrained 和 fixed-total-data reuse 三种 ensemble 分开，并对 base/instruct families 分别拟合。", r"Figure 1 汇总 inter-model 与 intra-model extrapolation：用 0.5B–32B 拟合的直线外推 held-out 72B，用早期 steps 外推同一模型后期；颜色随参数规模变化，展示大模型具有更陡 loss–resource slope。"),
            sec("模型与方法", r"经验式为 \(\log L(N,X)=-k(N)\log X+E(N)\)，其中 \(X=C\) 或 \(D\)。学习效率 \(k(N)\) 再拟合饱和式 \(K_{\max}/(1+N_0/N)\)，把随模型增大的边际收益限制在 \(K_{\max}\)。训练共覆盖 Qwen2.5 0.5B、1.5B、3B、7B、14B、32B、72B，正文称共 fine-tune 63 个 LLM runs。", r"data reuse 保持 \(D_{\rm unique}\tau=D_{\rm total}\)，通过不同子集大小与 repetition factor \(\tau\) 比较同总步数。课程难度分布保持一致；域迁移同时测 math、HumanEval、SuperGPQA 与 zebra puzzle。"),
            sec("核心结果与证据", r"Figure 1 的 held-out 72B 虚线与实测轨迹接近，intra-model 早期拟合也能外推快速提升阶段；Qwen 的 compute/data inter-与 intra-model fits 均报告 \(R^2>0.99\)。Llama 3 1B–70B 重复实验同样 \(R^2>0.99\)，但绝对性能不同：Llama-70B holdout accuracy 约 50%，Qwen-72B 约 59%。", r"\(k_C(N)\) 与 \(k_D(N)\) 随规模增加，但 32B 后增益开始减弱；这是有限范围内对饱和函数的支持，不是对 \(N\to\infty\) 的观测。Figure 7 显示固定 \(D_{\rm total}\) 时 \(\tau\le25\) 的 final loss 无显著退化，\(\tau=100\) 出现过拟合。", r"RL 改善主要迁移到未见过的数学任务；HumanEval 与 SuperGPQA 增益很小，较大模型的 zebra-puzzle 甚至退化。因此“总优化步数主导”仅在所测数学域和中等复用区成立，不能理解为样本唯一性普遍不重要。"),
            sec("有效性与局限", r"论文是单一主算法 GRPO、数学奖励、dense Qwen/Llama families 的经验研究；\(R^2\) 高只说明所采样资源窗口内 log-linear fit 好，不能证明机制或远尺度外推。test loss 强依赖题集难度与 PassRate estimator，\(K_{\max},N_0,E\) 不能跨环境直接解释。", r"作者明确指出未覆盖多域 RL、72B 以上规模和 MoE；饱和趋势因此尚未在更大尺度验证。63 runs 的超参、数据筛选和 rollout cost 会影响拟合；moderate reuse 的结论也受 curriculum 与 high-quality math data 条件限制。"),
            sec("复现与资源", r"原文：https://arxiv.org/abs/2509.25300。全文 21 页，PDF SHA-256：cab7b0093cb2a4a87d8f6541324d2bb7bd82acc270fe448e3516750fa5dac2f0。", r"复现需固定 Qwen/Llama checkpoints、GRPO group size/reward normalization、50k+ math problem pool、difficulty strata、rollout length、FLOP accounting、holdout PassRate sampling、fit windows、reuse \(\tau\) 和 domain-transfer prompts。拟合应报告 bootstrap intervals 与 held-out residuals。", r"Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", r"先看 Figure 1，区分跨模型和单模型外推；再读 Eqs. (1)–(8)，检查 \(k(N)\) 的饱和参数化。随后看 Figures 4–5 的跨架构结果，再读 Figures 6–9 的 reuse/domain-transfer 边界，最后核对 Limitations，避免把有限尺度拟合提升为普适 RL scaling law。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2509.25300/figure-1-rl-scaling.webp", "label": "Figure 1", "visual_type": "data_plot", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "Qwen2.5 不同模型规模的 test loss 随 post-training FLOPs 变化，以及跨模型和单模型外推。", "caption": "小模型与早期轨迹拟合可外推 72B 和后期快速提升区；有效范围仍受模型族与数学域限制。", "selection_rationale": "论文没有比数据图更强的任务可视化；Figure 1 是核心结论的最重要原文图，故作为封面。"},
        "figure_refs": [figure("2509.25300", "figure-1-rl-scaling.webp", "Figure 1", 2, "show inter-model and intra-model scaling predictions", "Four panels compare base and instruct models under held-out-size and early-trajectory extrapolation.", "Learning efficiency increases with model scale over the tested compute window.", "The fit is empirical, family-specific and does not validate asymptotic extrapolation beyond 72B.")],
        "equation_refs": [
            {"label": "Post-training resource law", "latex": r"\log L(N,X)=-k(N)\log X+E(N),\qquad X\in\{C,D\}", "role": "predict loss from model size and compute or data", "symbols": {"L": "one minus pass rate", "N": "model parameters", "C": "training FLOPs", "D": "training data volume"}, "evidence": "paper.pdf p. 2, Eq. (1)", "interpretation": "At fixed model size, the rapid-improvement regime is approximately linear on log resource axes."},
            {"label": "Efficiency saturation ansatz", "latex": r"k(N)=\frac{K_{\max}}{1+N_0/N}", "role": "model diminishing marginal efficiency gains", "symbols": {"K_max": "asymptotic fitted efficiency", "N_0": "saturation scale"}, "evidence": "paper.pdf p. 2, Eq. (2)", "interpretation": "The fitted slope rises with scale but approaches a finite ceiling within the proposed parametric model."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: resource law, fits and cross-architecture validation", "paper.pdf pp. 7–9: data reuse and domain transfer", "paper.pdf pp. 9–10: discussion, conclusion and limitations", "source PDF SHA-256 cab7b0093cb2a4a87d8f6541324d2bb7bd82acc270fe448e3516750fa5dac2f0", "Evidence status: full-text verified; no independent reproduction performed."],
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
