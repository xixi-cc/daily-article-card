#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 004."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_id: str, topic: str) -> dict[str, object]:
    return {
        "program": "Collection",
        "catalog": "Paper Collection",
        "catalog_record_id": record_id,
        "catalog_record_ids": [record_id],
        "catalog_topic": topic,
        "collection_date": "2026-08-23",
        "sampled_at": "2026-08-26",
        "selected_by": "full_collection_backfill",
        "sampling_seed": "not_applicable_full_collection",
        "candidate_count": 452,
    }


MATH_REPLACEMENTS = {
    "(h_t=f(h_{t-1},s_{t-1},a_{t-1}))": r"\(h_t=f(h_{t-1},s_{t-1},a_{t-1})\)",
    "(s_t\\sim p(s_t\\mid h_t))": r"\(s_t\sim p(s_t\mid h_t)\)",
    "(p(o_t\\mid h_t,s_t))": r"\(p(o_t\mid h_t,s_t)\)",
    "(p(r_t\\mid h_t,s_t))": r"\(p(r_t\mid h_t,s_t)\)",
    "(s_t)": r"\(s_t\)",
    "(hat\\rho^{(N)}=N^{-1}\\sum_{i=1}^N\\delta_{\\theta_i})": r"\(\hat\rho^{(N)}=N^{-1}\sum_{i=1}^N\delta_{\theta_i}\)",
    "(partial_t\\rho_t=2\\xi(t)\\nabla_\\theta\\cdot[\\rho_t\\nabla_\\theta\\Psi(\\theta;\\rho_t)])": r"\(\partial_t\rho_t=2\xi(t)\nabla_\theta\cdot[\rho_t\nabla_\theta\Psi(\theta;\rho_t)]\)",
    "(lim_{t\\to\\infty}\\lim_{\\alpha\\to\\infty}\\hat f_\\alpha(z;\\rho_t^\\alpha)=h(z)^\\top H^{-1}y)": r"\(\lim_{t\to\infty}\lim_{\alpha\to\infty}\hat f_\alpha(z;\rho_t^\alpha)=h(z)^\top H^{-1}y\)",
    "(O(N^{-1/2}\\sqrt{\\log N+z}))": r"\(O(N^{-1/2}\sqrt{\log N+z})\)",
    "(T=o(\\log\\log N))": r"\(T=o(\log\log N)\)",
    "(D/\\sqrt N)": r"\(D/\sqrt N\)",
    "(\\varepsilon\\ll1/D)": r"\(\varepsilon\ll1/D\)",
    "(2\\xi(t)\\tau/D)": r"\(2\xi(t)\tau/D\)",
    "(H_{\\rho_0})": r"\(H_{\rho_0}\)",
    "(N\\to\\infty)": r"\(N\to\infty\)",
    "(alpha\\to\\infty)": r"\(\alpha\to\infty\)",
    "(mathbb R^D)": r"\(\mathbb R^D\)",
    "(\\rho_t)": r"\(\rho_t\)",
    "(N\\gg D)": r"\(N\gg D\)",
    "(alpha)": r"\(\alpha\)",
    "(N)": r"\(N\)",
    "(D)": r"\(D\)",
    "(V)": r"\(V\)",
    "(U)": r"\(U\)",
    "(z_t=[x_g,u_g])": r"\(z_t=[x_g,u_g]\)",
    "(Sigma_\\xi^{-1}=\\Lambda_\\xi=\\alpha\\Theta)": r"\(\Sigma_\xi^{-1}=\Lambda_\xi=\alpha\Theta\)",
    "(Theta=\\mathrm{diag}(Q,R))": r"\(\Theta=\mathrm{diag}(Q,R)\)",
    "(x_s)": r"\(x_s\)",
    "(x_g)": r"\(x_g\)",
    "((x_i))": r"\((x_i)\)",
    "(D(x_s,x_g)=\\sum_i d(x_i,x_{i+1}))": r"\(D(x_s,x_g)=\sum_i d(x_i,x_{i+1})\)",
    "(D_\\phi)": r"\(D_\phi\)",
    "((x^{(h+1)},z^{(h)})=R_h(x^{(h)}))": r"\((x^{(h+1)},z^{(h)})=R_h(x^{(h)})\)",
    "(x^{(h)}=R_h^{-1}(x^{(h+1)},z^{(h)}))": r"\(x^{(h)}=R_h^{-1}(x^{(h+1)},z^{(h)})\)",
    "(z^{(h)})": r"\(z^{(h)}\)",
    "(p(z)=\\frac{1}{2b}e^{-|z|/b})": r"\(p(z)=\frac{1}{2b}e^{-|z|/b}\)",
    "O(log L)": r"\(O(\log L)\)",
    "O(L²)": r"\(O(L^2)\)",
    "O(d)": r"\(O(d)\)",
    "O(1)": r"\(O(1)\)",
    r"\hat\rho^{\(N\)}": r"\hat\rho^{(N)}",
}


def normalize_math(value: object) -> object:
    """Repair inline math delimiters in prose."""
    if isinstance(value, str):
        for old, new in MATH_REPLACEMENTS.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [normalize_math(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_math(item) for key, item in value.items()}
    return value


CARDS = [
    {
        "arxiv_id": "1811.04551",
        "source_version": "v5",
        "source_pdf": "https://arxiv.org/pdf/1811.04551",
        "title_en": "Learning Latent Dynamics for Planning from Pixels",
        "title_zh": "从像素学习用于规划的潜在动力学",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("6b3ebe959a8a7238", "Control & Reinforcement Learning"),
        "verified_metadata": {
            "arxiv_id": "1811.04551",
            "version": "v5",
            "title": "Learning Latent Dynamics for Planning from Pixels",
            "authors": ["Danijar Hafner", "Timothy Lillicrap", "Ian Fischer", "Ruben Villegas", "David Ha", "Honglak Lee", "James Davidson"],
            "categories": ["cs.LG", "cs.AI", "stat.ML"],
            "primary_category": "cs.LG",
            "published": "2018-11-12T04:30:10Z",
            "abstract": "PlaNet learns a recurrent latent state-space model from pixels and uses online latent-space planning for continuous control.",
        },
        "sections": [
            sec("作者信息", "作者：Danijar Hafner、Timothy Lillicrap、Ian Fischer、Ruben Villegas、David Ha、Honglak Lee、James Davidson；论文为 arXiv:1811.04551v5。", "本卡核对 21 页全文。实验覆盖六个 DeepMind Control Suite 像素控制任务，每个设置报告 5 个随机种子与测试轨迹分位区间。"),
            sec("研究问题", "若环境方程未知，基于模型的控制必须一边从图像学习动力学，一边用模型向未来规划。困难不只是重建下一帧，而是保持对奖励和受控状态的多步预测精度；规划器还会主动寻找模型误差并利用它。", r"论文问：能否在不恢复显式物理坐标的情况下，学习一个足以支持长时域控制的潜在状态 (s_t)，并以在线优化动作序列替代训练一个独立策略？"),
            sec("背景", "纯确定性 RNN 能长时记忆，却无法表示同一状态的多种未来；纯随机 state-space model 能表示不确定性，却容易在采样链中遗忘。像素重建损失又会把容量浪费在与控制无关的纹理上。", "PlaNet 的立场接近系统辨识：不要求生成模型在所有像素指标上完美，而要求潜在传播子在规划时域内保留可预测的动力学与奖励信息。"),
            sec("模型与方法", r"recurrent state-space model（RSSM）把状态拆成确定性记忆 (h_t=f(h_{t-1},s_{t-1},a_{t-1})) 与随机分量 (s_t\sim p(s_t\mid h_t))，并由 (p(o_t\mid h_t,s_t)) 与 (p(r_t\mid h_t,s_t)) 解码观测和奖励。", "训练使用变分序列目标；latent overshooting 进一步让多步 prior 直接匹配未来 posterior，迫使随机传播子跨越多个时间步保持一致。", "控制时用 cross-entropy method（CEM）反复采样、筛选并重拟合动作序列分布；只执行第一段动作，得到新观测后再滚动规划。"),
            sec("核心结果与证据", "Figure 2 给出机制对照：RNN 只有确定路径，SSM 只有随机路径，RSSM 用两条路径耦合记忆与多未来。它解释了为什么模型设计不是简单增加隐变量，而是在可记忆性与不确定性之间分工。", "Figure 1 的六个环境包含接触、部分可观测与稀疏奖励；PlaNet 仅用 64×64 RGB 观测，在 500 个 episode 内达到与 D4PG 使用约 100,000 个 episode 相近或更高的最终表现，论文据此报告平均约 200 倍的 episode 效率差。", "消融表明 RSSM 普遍优于纯确定或纯随机设计，CEM 优于 random shooting；但 latent overshooting 对 RSSM 本身略降性能，对较弱 DRNN 则显著改善，因此它不是所有架构上的单调增益。", "Appendix 的 50-step open-loop 视频预测和状态探针显示潜变量保留了位置、速度与奖励信息；这支持“可用于控制的状态表示”，但不是对真实动力学方程的唯一辨识。"),
            sec("有效性与局限", "200 倍是按论文从既有 D4PG 曲线估算达到 PlaNet 最终分数所需 episode，不是同一代码、同一算力和同一观测管线下的严格墙钟比较。", "全部任务来自同一控制套件和低分辨率固定相机；域随机化、真实传感噪声、长时不可逆误差和安全约束均未检验。", "CEM 每个环境步需评估大量候选序列，样本效率不等同于推理效率。规划器仍可能利用模型偏差，且 receding horizon 不能保证全局最优。", "开环像素预测漂亮并不充分：真正因果证据来自奖励/状态探针和闭环控制消融。latent overshooting 的混合结果也要求按模型族单独验证。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1811.04551；PDF：https://arxiv.org/pdf/1811.04551；作者公开了 PlaNet 实现。", "全文 PDF 共 21 页，SHA-256：abac727526e6a45669d3ab9957126587e22aacf4dc9bcd60ffe5c853108e5bcc。", "最小复现应固定环境 action repeat、5 个 seed episodes、模型更新频率、CEM 的 horizon/iteration/candidate/elite 数，并保存每个随机种子的 episode-return 曲线、规划耗时和开环预测误差。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 2 和 Eq. (4)，把确定性记忆与随机状态的职责分开；再看 Figure 3 理解 one-step ELBO 与 multi-step overshooting 的差别。", "随后读 Figures 4–5 与 Table 1，分别核对模型结构、数据收集策略和 episode 效率，不要把三种比较混为一项。", "最后看 Appendices D–E 的多任务、overshooting 与开环预测诊断；特别注意作者对 RSSM 上 overshooting 负增益的诚实报告。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/1811.04551/figure-1-control-domains.webp",
            "label": "Figure 1",
            "visual_type": "simulation_snapshot",
            "evidence": "arXiv:1811.04551v5, paper.pdf p. 2, Figure 1",
            "alt_text": "PlaNet 的六个像素控制环境：Cartpole、Reacher、Cheetah、Finger、Cup 与 Walker。",
            "caption": "六类仅从图像观测的连续控制任务同时包含接触、遮挡和稀疏奖励，直观展示论文所要求的潜在动力学覆盖范围。",
            "selection_rationale": "这是原文最直观的任务可视化，比性能曲线更适合作为封面；机制图 Figure 2 另在正文解释。",
        },
        "figure_refs": [
            {"label": "Figure 1", "asset_path": "assets/collection-figures/1811.04551/figure-1-control-domains.webp", "section": "核心结果与证据", "role": "show the physical diversity of the pixel-control tasks", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "六个 DeepMind Control Suite 像素任务。", "caption": "任务同时考验部分可观测、接触动力学和稀疏奖励。", "interpretation": "PlaNet 的证据范围比单一 cart-pole 更广，但仍局限于模拟器。"},
            {"label": "Figure 2", "asset_path": "assets/collection-figures/1811.04551/figure-2-rssm-designs.webp", "section": "核心结果与证据", "role": "contrast deterministic, stochastic, and recurrent state-space dynamics", "evidence": "paper.pdf p. 4, Figure 2", "alt_text": "RNN、SSM 与 RSSM 三种潜在动力学图模型。", "caption": "RSSM 用确定性路径保持记忆，用随机路径表示多种未来。", "interpretation": "双路径是模型能同时处理长时依赖与随机性的核心结构。"},
        ],
        "equation_refs": [
            {"label": "RSSM transition and observation model", "latex": r"h_t=f(h_{t-1},s_{t-1},a_{t-1}),\quad s_t\sim p(s_t\mid h_t),\quad o_t\sim p(o_t\mid h_t,s_t)", "role": "separate deterministic memory from stochastic latent dynamics", "symbols": {"h_t": "deterministic recurrent state", "s_t": "stochastic latent state", "a_t": "action", "o_t": "image observation"}, "evidence": "paper.pdf p. 4, Eq. (4)", "interpretation": "The deterministic path transports memory while the stochastic path represents uncertain futures."},
            {"label": "Latent overshooting", "latex": r"\mathbb E_{q(s_{t-d}\mid o_{\le t-d},a_{<t-d})}\,p(s_{t-1}\mid s_{t-d},a_{<t})}\!\left[D_{\mathrm{KL}}\!\left(q(s_t\mid o_{\le t},a_{<t})\Vert p(s_t\mid s_{t-1},a_{t-1})\right)\right]", "role": "train multi-step predictive consistency in latent space", "symbols": {"d": "overshooting distance", "q": "inference posterior", "p": "learned transition prior"}, "evidence": "paper.pdf p. 5, Eq. (6)", "interpretation": "Future posteriors supervise transitions reached through multiple model steps rather than only one-step predictions."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: tasks, RSSM architecture, ELBO and latent overshooting", "paper.pdf pp. 6–8: CEM planning and primary/ablation results", "paper.pdf Appendices C–E: implementation details, multi-task and prediction diagnostics", "source PDF SHA-256 abac727526e6a45669d3ab9957126587e22aacf4dc9bcd60ffe5c853108e5bcc", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "1902.06015",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/1902.06015",
        "title_en": "Mean-field theory of two-layers neural networks: dimension-free bounds and kernel limit",
        "title_zh": "双层神经网络的平均场理论：无维数界与核极限",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("eaaf43f1277a07d8", "Training Dynamics"),
        "verified_metadata": {"arxiv_id": "1902.06015", "version": "v1", "title": "Mean-field theory of two-layers neural networks: dimension-free bounds and kernel limit", "authors": ["Song Mei", "Theodor Misiakiewicz", "Andrea Montanari"], "categories": ["stat.ML", "cond-mat.stat-mech", "cs.LG", "math.ST"], "primary_category": "stat.ML", "published": "2019-02-16T00:01:01Z", "abstract": "The paper proves finite-time mean-field approximation bounds for two-layer-network SGD whose required width can be independent of parameter dimension, extends them to noisy SGD, and derives the kernel limit."},
        "sections": [
            sec("作者信息", "作者：Song Mei、Theodor Misiakiewicz、Andrea Montanari；论文为 arXiv:1902.06015v1，交叉统计学习、统计物理与数学统计。", "本卡核对 62 页全文。主体给出定理和适用条件，绝大部分篇幅用于 PDE—粒子—梯度流—SGD 四级近似的概率界。"),
            sec("研究问题", r"双层网络的平均场极限把 (N) 个神经元的 SGD 变成参数空间 (mathbb R^D) 上概率测度 (\rho_t) 的非线性 PDE。早期非渐近界要求宽度 (N\gg D)，使“无限宽描述”在高维参数中显得昂贵。", "论文要区分两个有限尺度：宽度控制经验测度的粒子涨落，步长控制每次高维随机更新。能否让前者的下界不再显含 D，同时保留对无界激活、加噪 SGD 和核极限的严格联系？"),
            sec("背景", r"网络输出是经验测度 (hat\rho^{(N)}=N^{-1}\sum_{i=1}^N\delta_{\theta_i}) 对单神经元特征的积分。population risk 因而成为含单体势 (V) 和二体核 (U) 的测度泛函。", "连续时间平均场方程是自洽输运；加噪 SGD 再产生 Fokker–Planck 扩散。证明的关键不是形式取极限，而是把每一步误差拆成 PDE→非线性独立粒子→相互作用粒子→梯度下降→随机梯度下降。"),
            sec("模型与方法", r"无噪声动力学满足 (partial_t\rho_t=2\xi(t)\nabla_\theta\cdot[\rho_t\nabla_\theta\Psi(\theta;\rho_t)])。加权衰减和 Gaussian 参数噪声给出扩散方程，扩散系数为 (2\xi(t)\tau/D)。", "Theorems 1–2 在有界/Lipschitz 势、次 Gaussian 梯度和受控初始化下，对有限时间区间内网络风险与 PDE 风险给出高概率一致界。fixed coefficients 与 general coefficients 分开处理。", r"核极限另引入输出尺度 (alpha)。先取 (N\to\infty) 得 mean-field 流，再取 (alpha\to\infty)，参数只在初始化附近线性响应，最终恢复由初始特征核 (H_{\rho_0}) 决定的 kernel ridge regression。"),
            sec("核心结果与证据", r"Theorem 1 的主宽度项为 (O(N^{-1/2}\sqrt{\log N+z}))，不显含参数维数 (D)；D 仍进入步长误差，因此需要 (\varepsilon\ll1/D)。这意味着宽度和离散化不能被一句“dimension-free”同时抹去。", "对中心各向异性 Gaussian 分类，Theorem 3 将达到近最优风险所需宽度从先前的 O(d) 改进为 O(1)，但仍需 O(d) 个样本/更新并假定特定良好初始化。", r"noisy SGD 的 fixed-coefficient 情形保持无维数宽度界；general-coefficient 的 Theorem 2(B) 仍含 (D/\sqrt N) 型依赖且只控制更短的 (T=o(\log\log N)) 时间。作者明确把它列为尚未 dimension-free 的例外。", r"Proposition 19 给出 (lim_{t\to\infty}\lim_{\alpha\to\infty}\hat f_\alpha(z;\rho_t^\alpha)=h(z)^\top H^{-1}y)，即零正则 kernel ridge 解。核描述因此是 mean-field 理论中的短位移/大尺度子极限，而不是与平均场竞争的无关理论。"),
            sec("有效性与局限", "无维数只针对有限时间风险近似中的最小宽度项；步长仍须随 D 缩小，常数依赖数据与激活的正则性，长时间指数因子也可很大。", "无界激活和 noisy general coefficients 的界更弱，后者并未消除维数依赖。定理不覆盖深层网络、mini-batch 工程细节或自适应优化器。", "核极限的顺序是先 N→∞、再 α→∞，且需要初始化核矩阵可逆；交换极限或有限 α 下的 feature learning 不由 Proposition 19 自动决定。", "论文证明动力学近似，不等同于对任意数据分布证明 PDE 达到 Bayes 最优；Theorem 3 的全局结论属于专门 Gaussian 任务。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1902.06015；PDF：https://arxiv.org/pdf/1902.06015。", "全文 PDF 共 62 页，SHA-256：fef012af450fe3b1f0635deb52b7d985a31af3f7a8156fb858069b094ebb8c41。", "复核可按 Appendix B–E 分别实现四段耦合误差，记录各段随 N、D、ε、T 的标度；核极限则固定同一初始化核，扫描 α 并比较 mean-field 输出与线性核流。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 Introduction 与 Sec. 3 的 Remarks 3.1–3.3；它们比公式标题更清楚地区分真正无维数部分和仍依赖 D 的部分。", "随后读 Sec. 4 与 Appendix H，把 mean-field、lazy/kernel 和有限宽三种极限按取极限顺序画出来。", "证明阅读可沿 Appendix B 的 PDE→ND→PD→GD→SGD 路线，再对照 C–E 看无界系数和噪声在哪一步引入更差常数。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "把神经元视作参数粒子后，双层网络 SGD 由概率测度上的非线性输运 PDE 描述。论文证明：在固定有限时间内，控制平均场误差所需的网络宽度可以不随单神经元参数维数增长；维数仍通过步长条件进入。加噪、无界系数是更弱的例外，而大输出尺度下的 lazy dynamics 则从同一平均场方程退化为 kernel ridge regression。", "selection_rationale": "原文没有信息性示意图，主要贡献是定理的尺度结构；按 v2.3 使用题目与物理摘要，避免用公式截图或不存在的数据图充当封面。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Noisy mean-field PDE", "latex": r"\partial_t\rho_t=2\xi(t)\nabla_\theta\cdot\left[\rho_t\nabla_\theta\Psi_\lambda(\theta;\rho_t)\right]+2\xi(t)\frac{\tau}{D}\Delta_\theta\rho_t", "role": "approximate noisy SGD by interacting transport plus diffusion", "symbols": {"rho_t": "parameter distribution", "xi(t)": "learning-rate schedule", "tau": "noise strength", "D": "single-neuron parameter dimension", "Psi_lambda": "regularized self-consistent potential"}, "evidence": "paper.pdf p. 6, Eq. (7)", "interpretation": "Dimension enters the diffusion normalization and, through discretization control, the admissible step size."},
            {"label": "Kernel limit", "latex": r"\lim_{t\to\infty}\lim_{\alpha\to\infty}\hat f_\alpha(z;\rho_t^\alpha)=h(z)^\top H^{-1}y", "role": "recover zero-regularization kernel ridge regression from mean-field dynamics", "symbols": {"alpha": "output scaling parameter", "H": "initialization kernel matrix", "h(z)": "kernel vector to training inputs", "y": "training labels"}, "evidence": "paper.pdf p. 59, Proposition 19", "interpretation": "The kernel regime is a large-alpha limit in which the initialization kernel remains effectively frozen."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–8: model, PDE and Theorems 1–3", "paper.pdf Sec. 4 and Appendix H: coupled mean-field/kernel limits", "paper.pdf Appendices B–E: non-asymptotic interpolation bounds", "source PDF SHA-256 fef012af450fe3b1f0635deb52b7d985a31af3f7a8156fb858069b094ebb8c41", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "1910.03003",
        "source_version": "v2",
        "source_pdf": "https://arxiv.org/pdf/1910.03003",
        "title_en": "Stochastic Optimal Control as Approximate Input Inference",
        "title_zh": "将随机最优控制表述为近似输入推断",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("28b45f9fa02765a4", "Control & Reinforcement Learning"),
        "verified_metadata": {"arxiv_id": "1910.03003", "version": "v2", "title": "Stochastic Optimal Control as Approximate Input Inference", "authors": ["Joe Watson", "Hany Abdulsamad", "Jan Peters"], "categories": ["cs.LG", "cs.RO", "eess.SY", "stat.ML"], "primary_category": "cs.LG", "published": "2019-10-07T18:41:52Z", "abstract": "Input Inference for Control casts stochastic optimal control as EM and Gaussian message passing, yielding time-varying feedback controllers with Bayesian regularization."},
        "sections": [
            sec("作者信息", "作者：Joe Watson、Hany Abdulsamad、Jan Peters；论文为 arXiv:1910.03003v2，交叉机器学习、机器人与控制。", "本卡核对 21 页全文。主体推导 I²C，并在 pendulum、cart-pole 与 double cart-pole 三个模拟系统上比较 iLQR 和 GPS。"),
            sec("研究问题", "非线性随机控制的全局 Bellman 方程通常不可解，轨迹优化于是每轮局部线性化，并依赖 line search、trust region 或手调正则来防止更新崩溃。", "论文问：能否把动作序列当成待估计的随机输入，把目标代价写成伪观测 likelihood，再用 Bayesian filtering/smoothing 的不确定性传播自然地产生探索、反馈增益和更新正则？"),
            sec("背景", "control-as-inference 常引入 optimality variable，但许多表述仍需额外策略参数化。I²C 直接在状态—动作联合轨迹上做近似推断，将动作与状态置于同一 Gaussian 图模型。", "线性 Gaussian 图中的前向消息相当于预测/滤波，后向消息编码未来目标信息。精度矩阵在控制语言中对应二次 value function 的 Hessian，因此 Kalman smoothing 与 LQR Riccati 递推共享代数结构。"),
            sec("模型与方法", r"把目标轨迹写成伪观测 (z_t=[x_g,u_g])，其噪声精度取 (Sigma_\xi^{-1}=\Lambda_\xi=\alpha\Theta)，其中 (Theta=\mathrm{diag}(Q,R)) 编码 LQ 代价，(alpha) 是待估计尺度。", "E-step 在每轮局部线性 Gaussian 动力学上做 forward-backward message passing，得到完整 state-action posterior；M-step 更新 α，并从联合后验条件化得到 time-varying linear Gaussian feedback controller。", "作者用相邻迭代 trajectory distribution 的 KL 上界限制 α 更新，形成具有概率意义的 trust region；这同时限制线性化误差并保留动作协方差。"),
            sec("核心结果与证据", "Figure 2 把 I²C 的动力学、控制输入、过程噪声与目标伪观测放进同一 Forney factor graph；控制量不是外加的确定优化变量，而是图中的随机边。", "在确定性线性系统、宽动作先验和高目标精度极限下，后向消息的 precision/scaled mean 与 LQR value-function 参数逐项对应，Figure 3 数值显示状态轨迹和反馈/前馈增益重合。", "非线性轨迹优化中 iLQR 收敛更快、最终预测代价更低；I²C 前期会用若干 EM 轮“预热”先验。可是在加入模型过程噪声的 100 次评估中，I²C 的实际代价更接近其预测代价，显示保守不确定性传播的校准优势。", "论文的优势因此不是在无噪基准上全面击败 iLQR，而是得到带 covariance 的反馈控制器、可解释的初始化/正则化和较一致的预测—执行差。"),
            sec("有效性与局限", "核心算法依赖局部线性化和 Gaussian 近似；多峰后验、硬接触和强非线性会被压成单峰矩，可能丢失最优控制分支。", "I²C 在报告的轨迹优化曲线上慢于且最终差于 iLQR；Bayesian 正则的价值主要体现在随机执行的校准与稳定性，不应写成普遍性能胜利。", "实验只有三个模拟任务，动力学模型已知且每轮可线性化；真实机器人、模型学习误差和高维感知未覆盖。", "KL 限制和 α 初值仍是超参数；概率解释使其更有原则，但不消除调参与局部最优。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1910.03003；PDF：https://arxiv.org/pdf/1910.03003；论文脚注给出 input-inference-for-control 代码仓库。", "全文 PDF 共 21 页，SHA-256：28b45f9fa02765a42ead460feee771db6567773fede2532863c4a48ae6ae251c。", "复现需分别保存预测 cost 与随机 rollout cost，不能只画优化曲线；固定线性化频率、过程噪声、α 初值、KL bound 和探索 covariance，并复核 LQR 极限下每个增益矩阵。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 2 和 Algorithm 1，理解动作作为随机输入参与消息传递；再读 Table 1 对照 precision、scaled mean 与 LQR value function。", "随后读 Sec. 2.1.1 和 Appendix B.5，核对 I²C 恢复 maximum-entropy finite-horizon LQR 所需的极限条件。", "最后把 Figure 4 的优化速度、Table 2 的随机执行校准和 Sec. 5 的作者结论分开评价。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/1910.03003/figure-2-factor-graph.webp", "label": "Figure 2", "visual_type": "schematic", "evidence": "arXiv:1910.03003v2, paper.pdf p. 3, Figure 2", "alt_text": "I²C 线性 Gaussian 动力系统的 Forney factor graph。", "caption": "状态、动作、过程噪声与目标伪观测被放在同一 Gaussian 图中；前后向消息共同产生轨迹后验和反馈控制器。", "selection_rationale": "该图直接呈现论文最重要的控制即推断结构，比代价曲线更能说明方法。"},
        "figure_refs": [{"label": "Figure 2", "asset_path": "assets/collection-figures/1910.03003/figure-2-factor-graph.webp", "section": "核心结果与证据", "role": "show controls as inferred random variables in a Gaussian factor graph", "evidence": "paper.pdf p. 3, Figure 2", "alt_text": "I²C 的线性 Gaussian Forney factor graph。", "caption": "蓝色中间变量用于封闭形式的 Gaussian 消息推导。", "interpretation": "后向消息把未来代价传回当前动作，前向消息传播动力学不确定性。"}],
        "equation_refs": [
            {"label": "Cost as observation precision", "latex": r"\Sigma_\xi^{-1}=\Lambda_\xi=\alpha\Theta,\qquad \Theta=\operatorname{diag}(Q,R)", "role": "encode quadratic state-action cost as a Gaussian pseudo-observation", "symbols": {"Sigma_xi": "pseudo-observation covariance", "alpha": "inferred cost scale", "Q": "state cost matrix", "R": "action cost matrix"}, "evidence": "paper.pdf p. 3, discussion below Eq. (4)", "interpretation": "Higher control cost becomes higher observation precision rather than an external deterministic penalty."},
            {"label": "Gaussian belief fusion", "latex": r"\Sigma_x=(\Lambda_{\vec x}+\Lambda_{\cev x})^{-1},\qquad \mu_x=\Sigma_x(\nu_{\vec x}+\nu_{\cev x})", "role": "combine forward dynamics and backward optimality messages", "symbols": {"Lambda": "message precision", "nu": "precision-weighted mean", "mu_x": "posterior mean", "Sigma_x": "posterior covariance"}, "evidence": "paper.pdf p. 3, Eq. (5)", "interpretation": "The posterior trajectory balances predictive uncertainty with information arriving from future objectives."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–6: probabilistic formulation, EM, factor graph and LQR correspondence", "paper.pdf pp. 7–8: nonlinear trajectory optimization and stochastic evaluation", "paper.pdf Appendix B: message derivations and dynamic-programming equivalence", "source PDF SHA-256 28b45f9fa02765a42ead460feee771db6567773fede2532863c4a48ae6ae251c", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2005.03648",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/2005.03648",
        "title_en": "Plan2Vec: Unsupervised Representation Learning by Latent Plans",
        "title_zh": "Plan2Vec：通过潜在规划进行无监督表征学习",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("3c07c1608916f3ba", "Field Theory"),
        "verified_metadata": {"arxiv_id": "2005.03648", "version": "v1", "title": "Plan2Vec: Unsupervised Representation Learning by Latent Plans", "authors": ["Ge Yang", "Amy Zhang", "Ari S. Morcos", "Joelle Pineau", "Pieter Abbeel", "Roberto Calandra"], "categories": ["cs.LG", "cs.AI", "stat.ML"], "primary_category": "cs.LG", "published": "2020-05-07T17:52:23Z", "abstract": "Plan2Vec builds a local-neighbor graph over observation sequences and distills graph shortest-path distances into a global latent metric for reactive planning."},
        "sections": [
            sec("作者信息", "作者：Ge Yang、Amy Zhang、Ari S. Morcos、Joelle Pineau、Pieter Abbeel、Roberto Calandra；论文为 arXiv:2005.03648v1。", "本卡核对 20 页全文。Paper Collection 原分类为 Field Theory；这里保留目录标签，但内容实质属于无监督表征学习与视觉规划。"),
            sec("研究问题", "局部视觉相似度只能判断两个观测是否可直接过渡，不能给出跨越长走廊、障碍或不同数据轨迹的全局可达距离。显式 Dijkstra 搜索能组合局部边，却要在每次目标查询时遍历大量节点。", "论文问：能否先利用离线轨迹建立拓扑图，再把图上的 shortest-path geodesic 蒸馏进一个参数化距离函数，使长时域规划从逐次图搜索变成近似常数代价的值查询？"),
            sec("背景", "状态空间若落在弯曲流形上，欧氏像素距离会把隔墙但视觉相近的点错误拉近。图最短路提供由局部可行边诱导的内禀距离，类似从局部度量重建全局 geodesic。", "与生成式 world model 不同，Plan2Vec 不预测下一帧；它只学习局部邻接和全局距离。与普通 replay-buffer value learning 不同，它可以从图中抽取跨越不同原始轨迹的计划作为监督。"),
            sec("模型与方法", "第一阶段用真实相邻帧作正例、非邻接帧作负例训练局部 metric，并在图像数据集上建立加权近邻图。图中新增边是模型推断的局部可达关系。", r"第二阶段对起点 (x_s) 和目标 (x_g) 做图搜索，得到路径 ((x_i)) 及目标距离 (D(x_s,x_g)=\sum_i d(x_i,x_{i+1}))，再回归全局 embedding/metric (D_\phi)。", r"memoryless sampling 从图中采样子计划，避免把监督局限于原始线性轨迹；训练后 (D_\phi) 可直接作 goal-conditioned value 或 A* heuristic。"),
            sec("核心结果与证据", "Figure 1 清楚给出两级结构：轨迹先变成局部图，启发式搜索产生 shortest-path target，再由 value regression 把规划结果压进全局表示。关键监督来自“路径积分”，而不是像素重建。", "在 C-maze 中二维 embedding 展开了障碍造成的全局拓扑；与 DQN 相比，Plan2Vec 用更少 rollout 学到更高成功率。把 learned metric 用作 A* heuristic 时，200-step StreetLearn 路径平均每步扩展约 1.6 个节点，而 L1 heuristic 为 2.7、Dijkstra 为 11.8。", "StreetLearn 一步目标成功率在 Tiny/Small/Medium 子集为 92.2±2.9%、57.2±4.3%、51.4±6.9%，高于文中 SPTM、VAE 与随机基线。Rope 数据的视觉计划能跨接两条原始轨迹，同时保持相邻绳形局部变化。", "论文所称线性 memory/computation 是对蒸馏后 reactive lookup 相对穷举图搜索的渐近描述；训练阶段仍需建图和求最短路。"),
            sec("有效性与局限", "局部 metric 的假阳性会给图添加物理上不可执行的捷径，随后最短路蒸馏会放大该错误。方法依赖局部邻接泛化足够可靠。", "Plan2Vec 学的是距离/值，不生成动作；实际控制仍需把连续观测对映射为低层动作，论文任务多以数据集导航或局部转移可用为前提。", "StreetLearn 的训练与测试来自同一城市图像分布，C-maze 和 Rope 规模有限；对动态环境、不可逆动作与强 stochastic transition 的证据不足。", "线性推理优势不包括离线 Dijkstra target 生成和图存储成本。类别删除实验的泛化还依赖道路网络保持连通。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2005.03648；PDF：https://arxiv.org/pdf/2005.03648；论文公开了代码与补充视频。", "全文 PDF 共 20 页，SHA-256：c75963d530aa827b5bda450608e20e63786c1c7c8597d39d652c9cfc3a738860。", "复现应分别记录局部边 precision/recall、图连通性、全局距离误差、搜索节点扩展数和最终成功率；只看成功率无法判断失败来自局部图、距离蒸馏还是控制接口。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 1，把局部 metric、图搜索和全局 value regression 三个对象分开；再读 Sec. 3 的 memoryless sampling。", "然后按 C-maze→Rope→StreetLearn 顺序阅读，三者分别检验拓扑展开、跨轨迹组合和视觉不显著的长程导航。", "最后核对 Figure 8 与 Table 2：一个测搜索开销，一个测 goal-reaching 成功率，不能互相替代。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2005.03648/figure-1-plan2vec-schematic.webp", "label": "Figure 1", "visual_type": "schematic", "evidence": "arXiv:2005.03648v1, paper.pdf p. 2, Figure 1", "alt_text": "Plan2Vec 从轨迹数据建图、搜索并回归全局距离的流程图。", "caption": "局部邻接图提供 geodesic，搜索生成长程监督，再由参数化距离把逐次规划压缩成快速查询。", "selection_rationale": "该图一眼呈现论文完整因果链，比单独的成功率或搜索成本图更适合作为封面。"},
        "figure_refs": [{"label": "Figure 1", "asset_path": "assets/collection-figures/2005.03648/figure-1-plan2vec-schematic.webp", "section": "核心结果与证据", "role": "summarize graph construction, search, and metric distillation", "evidence": "paper.pdf p. 2, Figure 1", "alt_text": "Plan2Vec 高层流程示意图。", "caption": "真实局部转移训练邻接 metric，图搜索产生全局 shortest-path target。", "interpretation": "表示学习的监督由离线规划生成，因此把局部可达性积分成全局几何。"}],
        "equation_refs": [
            {"label": "Shortest-path target", "latex": r"D(x_s,x_g)=\min_{\tau:x_s\leadsto x_g}\sum_i d(x_i,x_{i+1})", "role": "define the graph geodesic distilled into the latent metric", "symbols": {"x_s": "start observation", "x_g": "goal observation", "tau": "graph path", "d": "learned local edge metric"}, "evidence": "paper.pdf pp. 2–3, Figure 1 and generalized value metric", "interpretation": "Global distance is the path integral of locally feasible transitions, not direct pixel similarity."},
            {"label": "Plan2Vec regression", "latex": r"\mathcal L(\phi)=\left\|D_\phi(x_s,x_g)-\sum_i d(x_i,x_{i+1})\right\|_2^2", "role": "amortize graph planning into a parametric distance lookup", "symbols": {"D_phi": "learned global distance", "phi": "representation parameters", "x_i": "states on a planned path"}, "evidence": "paper.pdf Sec. 3 and Figure 1", "interpretation": "The expensive shortest-path computation is paid during training and distilled for reactive use."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–4: graph construction, generalized value metric and memoryless sampling", "paper.pdf pp. 5–8: C-maze, Rope and StreetLearn experiments", "paper.pdf Appendix: dataset details, additional trajectories and hyperparameters", "source PDF SHA-256 c75963d530aa827b5bda450608e20e63786c1c7c8597d39d652c9cfc3a738860", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "2010.00029",
        "source_version": "v5",
        "source_pdf": "https://arxiv.org/pdf/2010.00029",
        "title_en": "RG-Flow: A hierarchical and explainable flow model based on renormalization group and sparse prior",
        "title_zh": "RG-Flow：基于重整化群与稀疏先验的层级可解释流模型",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("ef2edf90e2952e25", "Renormalization Group"),
        "verified_metadata": {"arxiv_id": "2010.00029", "version": "v5", "title": "RG-Flow: A hierarchical and explainable flow model based on renormalization group and sparse prior", "authors": ["Hong-Ye Hu", "Dian Wu", "Yi-Zhuang You", "Bruno Olshausen", "Yubei Chen"], "categories": ["cs.LG", "cond-mat.dis-nn", "cs.AI", "cs.CV", "stat.ML"], "primary_category": "cs.LG", "published": "2020-09-30T18:04:04Z", "abstract": "RG-Flow arranges invertible local maps as a renormalization hierarchy, separates latent variables by scale, and uses a sparse Laplacian prior to improve disentanglement."},
        "sections": [
            sec("作者信息", "作者：Hong-Ye Hu、Dian Wu、Yi-Zhuang You、Bruno Olshausen、Yubei Chen；论文为 arXiv:2010.00029v5。", "本卡核对 32 页全文。工作把实空间 RG/MERA 的局域层级结构移植到 normalizing flow，并在合成多尺度图像与 CelebA 上验证。"),
            sec("研究问题", "普通 flow 用全局耦合的可逆映射把图像压到各向同性 Gaussian；虽然似然可精确计算，潜变量往往不对应明确的尺度、位置或语义。", "论文问：若把每层可逆变换组织成“粗粒化 + 分出短尺度变量”的 RG 过程，能否让不同层的 latent 对应不同长度尺度，并利用因果锥的局域性加速局部修复？稀疏先验能否进一步破除高层表示的旋转简并？"),
            sec("背景", "实空间 RG 逐层积分掉短程自由度，把长波变量送往更高层；MERA 的 disentangler 在 decimation 前削弱局部关联。可逆流不能真正丢弃自由度，因此 RG-Flow 把被 decimate 的细节保存为当前层 latent。", "局部 bijector 使每个 latent 只影响输出中的一个生成因果锥；反向也只有局部像素进入其推断因果锥。层级深度随图像边长 L 仅对数增长。"),
            sec("模型与方法", r"第 (h) 层局部可逆变换满足 ((x^{(h+1)},z^{(h)})=R_h(x^{(h)}))，逆过程为 (x^{(h)}=R_h^{-1}(x^{(h+1)},z^{(h)}))。四分之三局部自由度被分到 (z^{(h)})，剩余粗变量继续上行。", "网络交错使用局部 disentangler 与 decimator，所有尺度 latent 构成双曲树状表示。作者用生成图像对 latent 的 Jacobian 定义 receptive field，直接测量每个变量的空间作用域。", r"低层局部变量近似独立；高层 receptive field 重叠时，将标准 Gaussian prior 换成 (p(z)=\frac{1}{2b}e^{-|z|/b}) 的 Laplacian 稀疏先验，借轴向稀疏性促进语义方向分离。"),
            sec("核心结果与证据", "Figure 5 把尺度结构可视化：逆 RG 从粗脸逐层加细节；低层 latent 的 receptive field 是眼角等局部小斑点，高层变量覆盖整张脸。它是“不同尺度信息分离”的直接证据，而非仅看 likelihood。", "Figure 6 中高层变量对应 gender、emotion、light、azimuth、hair、skin，中层控制 eyes、eyebrows、bang、collar，低层只影响单眼或眉毛；作者通过逐一扫描 latent 并查看 receptive field 进行语义标注。", "局部损坏只沿一条 O(log L) 深度因果锥影响 latent，因此 inpainting 优化变量数为 O(log L)；全局 Real NVP 需调整 O(L²) 个变量。Figure 8 的 CelebA 修复在相同允许变量数下更清晰。", "Laplacian prior 在合成数据上打破 Gaussian 的连续旋转对称，并提高作者报告的 disentanglement 指标；但高层因素很少的 3D Chairs 上仍难找到稳定可解释方向。"),
            sec("有效性与局限", "这里的“RG”是受物理粗粒化启发的网络架构，不是从某个 microscopic Hamiltonian 推导的 exact RG，也没有计算临界指数或证明 universal fixed point。", "语义变量主要通过人工查看 latent sweep 与 receptive field 命名，存在后验选择；CelebA 的性别等属性也可能与数据偏差和相关特征纠缠。", "O(log L) 指局部损坏涉及的 latent 数量，在固定局部核和层级结构下成立；总生成、训练和搜索最优修复的墙钟复杂度不因此全部变成对数。", "Laplacian prior 牺牲旋转对称性换取轴向稀疏，但 disentanglement 不是普遍保证；作者自己报告当高层生成因子较少时效果不稳。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/2010.00029；PDF：https://arxiv.org/pdf/2010.00029；论文提供项目代码链接。", "全文 PDF 共 32 页，SHA-256：cbd0a2377aea2df249202abfde0dd37037c181e5e3e4bb7d7d6b596f570650。", "复现应固定 bijector kernel、层数、decimation 规则和 prior；逐层保存 latent sweep、Jacobian receptive field、likelihood 与 disentanglement 指标，并分别计数 inpainting 的活跃 latent 和真实优化时间。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 2，把“积分掉”改译为“分出但保留为 latent”；这是可逆 flow 与物理 RG 的关键差别。", "再看 Figures 5–6，从 receptive-field 支撑随 h 扩张理解尺度，而不是先接受语义标签。", "最后读 Secs. 3.5、4.6 与 Appendices E–G，分别审查 O(log L) 因果锥、Laplacian 对称性破缺和失败案例。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/2010.00029/figure-5-multiscale-generation.webp", "label": "Figure 5", "visual_type": "real_space", "evidence": "arXiv:2010.00029v5, paper.pdf p. 11, Figure 5", "alt_text": "CelebA 图像的逐尺度生成与不同 RG 层级潜变量的 receptive fields。", "caption": "逆 RG 从粗粒度脸逐层补充细节；潜变量 receptive field 从局部斑点扩展到整张脸，直接显示层级长度尺度。", "selection_rationale": "这是论文最重要且最直观的尺度可视化；Figure 2 的架构图作为正文机制图补充。"},
        "figure_refs": [
            {"label": "Figure 2", "asset_path": "assets/collection-figures/2010.00029/figure-2-rg-hierarchy.webp", "section": "模型与方法", "role": "show forward coarse-graining and inverse generation", "evidence": "paper.pdf p. 5, Figure 2", "alt_text": "RG-Flow 的逐层粗粒化与逆生成示意图。", "caption": "每层把粗变量送往更高层，同时把细节保存在当前层 latent。", "interpretation": "可逆性意味着细节没有被积分后丢弃，而是被显式分层保存。"},
            {"label": "Figure 5", "asset_path": "assets/collection-figures/2010.00029/figure-5-multiscale-generation.webp", "section": "核心结果与证据", "role": "visualize scale-separated generation and receptive fields", "evidence": "paper.pdf p. 11, Figure 5", "alt_text": "不同 RG 层的脸部生成和 receptive fields。", "caption": "低层变量局部作用，高层变量覆盖全局结构。", "interpretation": "层级 receptive field 是 RG-Flow 可解释性的操作性定义。"},
        ],
        "equation_refs": [
            {"label": "Forward RG split", "latex": r"(x^{(h+1)},z^{(h)})=R_h(x^{(h)})", "role": "separate coarse variables from fine-scale latent variables", "symbols": {"x_h": "observable/coarse representation at level h", "z_h": "fine-scale latent split at level h", "R_h": "local bijective RG transform"}, "evidence": "paper.pdf p. 5, Eq. (3)", "interpretation": "Coarse information continues upward while fine information remains explicitly stored at its own scale."},
            {"label": "Sparse latent prior", "latex": r"p(z_l)=\frac{1}{2b}\exp\!\left(-\frac{|z_l|}{b}\right)", "role": "encourage axis-aligned sparse high-level representations", "symbols": {"z_l": "latent component", "b": "Laplacian scale"}, "evidence": "paper.pdf p. 7, Eq. (7)", "interpretation": "Unlike an isotropic Gaussian, the Laplacian prior favors coordinate axes and can break rotational degeneracy among latent directions."},
        ],
        "evidence_refs": ["paper.pdf pp. 4–8: normalizing-flow objective, RG hierarchy and receptive fields", "paper.pdf pp. 9–14: multiscale representations, semantics, mixing and inpainting", "paper.pdf Appendices E–G: sparse-prior mechanism, quantitative inpainting and failure case", "source PDF SHA-256 cbd0a2377aea2df249202abfde0dd37037c181e5e3e4bb7d7d6b596f570650", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        normalized_card = normalize_math(card)
        path.write_text(json.dumps(normalized_card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
