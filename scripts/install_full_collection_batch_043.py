#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 043."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-x5vj-8jq9", "arXiv v5 manuscript", "https://arxiv.org/pdf/2407.04495",
        "Speed-Accuracy Relations for Diffusion Models: Wisdom from Nonequilibrium Thermodynamics and Optimal Transport",
        "扩散模型的速度—精度关系：非平衡热力学与最优输运的启示", "theory_numerics",
        "68b0c66bdba0148b", "Generative Models",
        {"doi":"10.1103/x5vj-8jq9","arxiv_id":"2407.04495","version":"arXiv v5 full text","title":"Speed-Accuracy Relations for Diffusion Models: Wisdom from Nonequilibrium Thermodynamics and Optimal Transport","authors":["Kotaro Ikeda","Tomoya Uda","Daisuke Okanohara","Sosuke Ito"],"journal":"Physical Review X","volume":"15","issue":"3","article":"031031","published":"2025-07-30","abstract":"Stochastic-thermodynamic inequalities bound diffusion-model generation error by entropy production and identify Wasserstein geodesics as optimal protocols under specified dynamics.","comment":"ArXiv v5 full text cross-checked with the version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Kotaro Ikeda、Tomoya Uda、Daisuke Okanohara、Sosuke Ito；Physical Review X 15, 031031 (2025)，新式 DOI:10.1103/x5vj-8jq9。核验 arXiv:2407.04495v5 全文37页及 Crossref 期刊元数据；未发现关联更正或撤稿。"),
            sec("研究问题", "diffusion model 用 forward noising 和 learned reverse dynamics 在有限时间生成数据；reverse score/velocity estimation error 会累积为终态分布误差。论文问：能否用 stochastic thermodynamics 把 generation accuracy、process duration、temperature/noise schedule 与 entropy production 定量联系，并指出给定端点间的最优学习 protocol？"),
            sec("背景", "Fokker–Planck diffusion 的 probability current、current velocity 与 entropy production 构成非平衡热力学描述；optimal transport 中 2-Wasserstein geodesic 则最小化概率流的 kinetic action。作者把真实 reverse process 与 estimated reverse process 的分布差异写成 Wasserstein/response divergence。", "这里的 thermodynamic quantities 是生成随机动力学的数学同构与代价度量，不等于训练 GPU 的真实能耗。速度—精度关系约束给定连续 diffusion formulation，也不覆盖任意 discrete sampler、flow matching 或带纠错 guidance 的实现。"),
            sec("模型与方法", "作者在连续时间 forward SDE/Fokker–Planck 与 time-reversed dynamics 中定义 true score 和 learned score，使用 Cauchy–Schwarz、Kantorovich–Rubinstein duality 与 thermodynamic speed limits 推导 complete-estimation 和 incomplete-estimation bounds。conservative force 条件给更强的 loss hierarchy。", "数值部分用一维 Gaussian/mixture、二维 Swiss roll 与不同 noise schedules 检验 inequality；进一步在 latent-space image datasets 上估计相关项。optimal protocol 由端点 distributions 的 Wasserstein geodesic 给出，并与常用 suboptimal schedule 比较。"),
            sec("核心结果与证据", "核心不等式把沿 reverse process 的 entropy production integral 下界为 learned velocity mismatch，再下界为终态 1-Wasserstein error 的平方除以 duration 和 reference divergence。Figure 4 汇总 complete estimation 的层级以及只知道部分误差时的 generalized bound。", "几何解释是：在无 nonconservative force 的条件下，entropy production 控制 distribution-space movement speed；固定时间和端点时，2-Wasserstein geodesic 最小化 kinetic/thermodynamic action。它给理论最优路径，但不自动给神经 score estimator、network capacity 或有限训练样本的最优配置。", "Figures 6–7 对 mixtures 和 Swiss roll 观察到不同 noise schedules 均满足 bounds，靠近 optimal transport 的 protocol 有较低 action/更稳健生成；Figure 8 将关系应用于真实图像 latent space。估计依赖有限 samples 和 density/score approximations，复杂图像上不是像素质量指标的直接替代。"),
            sec("有效性与局限", "推导假设足够光滑的连续概率密度、有限 moments、已定义的 diffusion coefficient 与可比较的 true/estimated dynamics。部分更强式子要求 conservative velocity field；高维经验分布的 Wasserstein 和 score error 本身难精确估计。", "数值 validation 以低维 toy distributions 为主，图像只在 learned latent space 展示；没有与大规模 diffusion benchmark 的 FID、训练算力或 sampler wall-clock 做系统因果比较。inequality 是必要限制，通常不等号，不能单独预测实际生成质量。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2407.04495；期刊：https://doi.org/10.1103/x5vj-8jq9。核验 PDF SHA-256：385b36a5e76400973d3edcf1c6b4008be5e413df19da55cfad1db464a51da271。正文未给统一代码仓库链接。", "复现需固定 SDE convention、forward/reverse time mapping、D_t、noise schedule、score estimator、terminal sampling、Wasserstein/divergence estimator 与随机种子；应逐项计算 Figure 4 hierarchy 的两侧与置信误差。Evidence status: full-text verified theory/numerical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–5 的 diffusion/stochastic-thermodynamic notation；pp.8–13 推导 speed–accuracy inequalities，p.13 Figure 4 是主结果导航。pp.16–22 Figures 6–8 看 toy、Swiss-roll 与图像应用；最后查 appendices 的 regularity 和 incomplete-estimation assumptions。"),
        ],
        "figure-4-speed-accuracy-hierarchy.webp", "Figure 4", 13, "schematic",
        "扩散模型完整与不完整误差估计下的熵产生、速度损失和 Wasserstein 误差不等式层级。",
        "生成分布偏差受有限时间的耗散与速度误差控制；保守力条件进一步收紧层级。",
        "Figure 4 直接汇总论文所有主要界及其成立条件，是最适合作为证据卡入口的理论图。",
        [{"label":"Speed-accuracy bound","latex":r"\int_0^\tau T_t\dot S_t^{\rm tot}\,dt\ge\int_0^\tau |v_{\rm loss}(t)|^2dt\ge\frac{(\Delta\mathcal W_1)^2}{\tau D_0}","role":"bound terminal distribution error by dynamical dissipation and score-induced velocity loss","symbols":{"S_tot":"total entropy production","v_loss":"velocity mismatch","Delta_W1":"change in 1-Wasserstein discrepancy","D0":"reference Pearson divergence"},"evidence":"paper.pdf p. 13, Figure 4 and Eqs. (77), (79), (81), (83)","interpretation":"The hierarchy applies under the paper's continuous-diffusion and estimation assumptions; it is not a hardware-energy bound."}],
        ["paper.pdf pp. 2–5: diffusion and stochastic-thermodynamic setup","paper.pdf pp. 8–13, Figures 3–4: speed-accuracy bounds and hierarchy","paper.pdf pp. 16–20, Figures 6–7: mixture and Swiss-roll calculations","paper.pdf pp. 20–22, Figure 8: image latent-space application","source PDF SHA-256 385b36a5e76400973d3edcf1c6b4008be5e413df19da55cfad1db464a51da271","Evidence status: full-text verified theory/numerical study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-xbk2-ggcf", "arXiv v1 manuscript", "https://arxiv.org/pdf/2507.22199",
        "Self-Propulsion Symmetries Determine Entropy Production of Active Particles with Hidden States",
        "自推进对称性决定隐状态主动粒子的熵产生", "theory", "63b84d59a70324d1", "Active Matter",
        {"doi":"10.1103/xbk2-ggcf","arxiv_id":"2507.22199","version":"arXiv v1 full text","title":"Self-Propulsion Symmetries Determine Entropy Production of Active Particles with Hidden States","authors":["Jacob Knight","Farid Kaveh","Gunnar Pruessner"],"journal":"Physical Review Letters","volume":"136","issue":"19","article":"198302","published":"2026-05-15","abstract":"A perturbative path-integral framework shows that parity and time-reversal symmetries of hidden self-propulsion determine the observable partial entropy-production rate of active-particle trajectories.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Jacob Knight、Farid Kaveh、Gunnar Pruessner；Physical Review Letters 136, 198302 (2026)，新式 DOI:10.1103/xbk2-ggcf。核验 arXiv:2507.22199v1 全文16页含补充推导；未发现关联更正或撤稿。"),
            sec("研究问题", "实验常只观察 active particle 的位置 x(t)，而自推进状态 w(t) 被隐藏；对 position trajectory 做 time reversal 得到的 partial entropy production 可能远低于完整系统 EPR。论文问：隐藏自推进的哪些 symmetry 决定可见轨迹是否不可逆，leading nonzero order 如何从一般非 Gaussian hidden process 系统计算？"),
            sec("背景", "模型为 overdamped particle：ẋ=νw(t)+√(2D)ξ(t)。若同时观察 x、w，full path probability ratio 给 Ṡ_{x,w}；边缘化 w 后 position process 通常 non-Markovian，partial EPR 是 P[x(t)] 与 P[x(T−t)] 的 KL-rate。", "作者区分 hidden process 的 parity P:w→−w、time reversal T:w(t)→w(T−t) 与 combined PT。zero partial EPR 不意味着 underlying active process 无耗散，只说明选定 observable 的 forward/reverse path statistics 相同。"),
            sec("模型与方法", "将 conditional Gaussian path measure 对 ν 展开，用 hidden-state moments/cumulants 把 partial EPR 写成 perturbative series。P 与 T symmetry 决定奇偶阶 correlators 是否消失，从而确定第一个可能非零的 n*；PT symmetry 则给 Ṡ_x=0 的充要结构。", "应用包括 symmetric/asymmetric telegraph run-and-tumble process，以及 diffusion w(t) with stochastic resetting。作者解析计算 leading terms，并用 Figure 1 的 sample trajectories 对比 full observation（用颜色标 w）与只看 x 的情形；这些轨迹是机制示意，不是实验数据。"),
            sec("核心结果与证据", "symmetric zero-drift telegraph process 具有 P、T、PT symmetry；隐藏 w 后 position trajectories time-reversible，Ṡ_x=0，尽管 full EPR 含持续 active dissipation。非零 mean drift 的 asymmetry 在 ν²/D order 即可见。", "若 asymmetric telegraph 调到 zero net drift，简单 drift 信号消失，但 parity breaking 仍令 partial EPR 在更高的 (ν²/D)^3 级出现；resetting process 保持 parity、破坏 time reversal，leading term更迟至 (ν²/D)^4 并依赖 D_w^4/r^7。Figure 1 将三种对称性与可见轨迹公式并列。", "因此非平凡 hidden-state irreversibility 至少到 self-propulsion velocity 的 sixth order才可能显现，具体 order 由 P/T 决定。弱 activity 时高阶信号极小，单靠肉眼或低阶 statistics 很容易误判为 equilibrium。"),
            sec("有效性与局限", "结果是小 ν²/D perturbation，对有限 trajectory、measurement noise 与强 propulsion 的收敛/estimation 没有全面数值评估。自由空间主文模型无 external potential；文中指出 harmonic/anharmonic confinement 会改变可见 EPR，需要更多 correlators。", "partial EPR 是 full EPR 的 coarse-grained lower bound，不具唯一热力学解释；hidden state 若可推断、观测协议改变或 noise colored，公式需扩展。resetting 与 telegraph 是解析基准，不能代表所有细胞或 active colloid internal dynamics。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2507.22199；期刊：https://doi.org/10.1103/xbk2-ggcf。核验 PDF SHA-256：9dfe5a4717d2636a6f7c7b15ae5bb87407ba56ea0eff03600648004f3495877c。本文为解析研究，未给专用代码仓库。", "复现需固定 path-reversal convention、trajectory duration limit、ν、D、telegraph rates/velocities 或 resetting r,Dw，并逐阶验证 hidden cumulants、symmetry cancellations 与 Table I coefficients。Evidence status: full-text verified analytical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 Figure 1 理解 full/partial observation；pp.2–4 Eqs. (1)–(13) 看 path integral 与 P/T selection rules。p.4 Table I 比较 leading orders，补充 pp.8–16 给 cumulant expansion、telegraph 与 resetting derivation。"),
        ],
        "figure-1-hidden-propulsion-symmetries.webp", "Figure 1", 1, "trajectory",
        "三种自推进过程在完整观测与隐藏推进速度时的轨迹及 partial entropy-production leading terms。",
        "位置轨迹的可逆性不由完整耗散单独决定，而由隐藏推进过程的 P、T 与 PT 对称性筛选。",
        "Figure 1 同时呈现可见性变化、对称性破缺和 leading-order 公式，是全文主命题的直接图解。",
        [{"label":"Partial entropy-production rate","latex":r"\dot S_x=\lim_{T\to\infty}\frac1T\int\mathcal D x\,P[x]\ln\frac{P[x(t)]}{P[x(T-t)]}","role":"measure time-reversal breaking visible in position trajectories after marginalizing hidden propulsion","symbols":{"P_x":"marginal path probability","T":"trajectory duration","x":"observed position"},"evidence":"paper.pdf p. 2, Eq. (5)","interpretation":"This is a coarse-grained path-space KL rate and may vanish despite nonzero full entropy production."}],
        ["paper.pdf pp. 1–2, Figure 1: resolved versus hidden trajectories","paper.pdf pp. 2–4, Eqs. (1)–(16): path expansion and symmetry rules","paper.pdf p. 4, Table I: process-specific leading EPR orders","paper.pdf pp. 8–16: perturbative and example derivations","source PDF SHA-256 9dfe5a4717d2636a6f7c7b15ae5bb87407ba56ea0eff03600648004f3495877c","Evidence status: full-text verified analytical study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-yfb3-fgf2", "arXiv v3 manuscript", "https://arxiv.org/pdf/2504.17587",
        "Enhancing Gravitational-Wave Detection: A Machine Learning Pipeline Combination Approach with Robust Uncertainty Quantification",
        "增强引力波探测：带稳健不确定性量化的机器学习管线组合", "ai_empirical",
        "63171e6a4b189239", "AI for Science",
        {"doi":"10.1103/yfb3-fgf2","arxiv_id":"2504.17587","version":"arXiv v3 full text","title":"Enhancing Gravitational-Wave Detection: A Machine Learning Pipeline Combination Approach with Robust Uncertainty Quantification","authors":["Gregory Ashton","Ann-Kristin Malz","Nicolo Colombo"],"journal":"Physical Review Letters","volume":"136","issue":"1","article":"011402","published":"2026-01-08","abstract":"Logistic-regression and multilayer-perceptron meta-classifiers combine four gravitational-wave search pipelines, while conformal prediction supplies label-conditional confidence with finite-sample coverage under exchangeability.","comment":"ArXiv v3 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Gregory Ashton、Ann-Kristin Malz、Nicolo Colombo；Physical Review Letters 136, 011402 (2026)，新式 DOI:10.1103/yfb3-fgf2。核验 arXiv:2504.17587v3 全文11页；未发现关联更正或撤稿。"),
            sec("研究问题", "LIGO/Virgo/KAGRA 的多个 low-latency search pipelines 对同一 candidate 给出不同 IFAR、SNR 与 source estimates；常用 maximum-IFAR combination 丢掉跨管线一致性信息。论文问：meta-classifier 能否联合这些 features 提高 signal/noise 排序，并用 conformal prediction 给单事件可校准的 confidence？"),
            sec("背景", "数据来自 O3 mock data challenge（MDC），四条 pipelines 的 candidate features 被对齐；未触发 IFAR>1 hr 的管线用零填充。总计9946 rows，其中5908为 simulated or real signals；signal injection rate 高于真实 astrophysical rate，专为压力测试 low-latency infrastructure。", "作者不用 pipeline pastro 作输入，因为 MDC 的增强 signal fraction 使其不再现实校准。logistic regression 提供可解释线性组合，MLP 捕捉 nonlinear relations；两者输出本身都不是自动 calibrated probability。"),
            sec("模型与方法", "数据按10% calibration、10% test、其余 training 划分，并对多种 train/test permutations 重复。LR 用 pipeline IFAR/SNR/mass/spin等特征，MLP 用相同表格输入；与候选的 maximum IFAR baseline 比较 ROC/AUC。", "label-conditional conformal prediction 用 LR probability complement 作为 nonconformity score，在 calibration set 上分别构建 signal/noise阈值，输出 candidate 属于 singleton signal、singleton noise、both 或 empty 的 prediction set/confidence。coverage 依赖 exchangeability。"),
            sec("核心结果与证据", "Figure 1 的 test ROC 报告 MLP AUC 0.967±0.002、LR 0.944±0.005、maximum-IFAR 0.925±0.008；shaded 90% permutation intervals 显示两种 ML combination 在该 MDC 上提高 ranking。MLP 比 LR 更强，但后续主要用 LR 保持可解释和较小性能损失。", "Figure 2 比较 conditional confidence 与 maximum IFAR，显示同一 IFAR 可因多管线 agreement 获得不同 confidence。Figure 3 将公开 O3 candidates 的 pastro 与 ML confidence 并列，四象限可标记值得复查的 disagreement；由于 O3 与 MDC distribution 不同，这不是新 detection catalog。", "Appendix 的 feature-count 和 confidence-vs-SNR 检查表明 LR 少数特征已接近饱和，MLP 从更多特征获益。conformal guarantee 是对未来 exchangeable labeled samples 的 marginal/label-conditional coverage，而不是每个特定 event 的真实 astrophysical probability。"),
            sec("有效性与局限", "MDC signal prevalence、simulated injections、pipeline versions 与 missing-data pattern 不等同真实 observing run；dataset shift 会破坏 classifier calibration 和 conformal exchangeability。只有四 pipelines，不能保证未来新增搜索器或高质量 glitch family 上仍增益。", "AUC 是总体排序指标，未直接证明在 operational false-alarm tail 的发现率提升；permutation uncertainty 也不包含 waveform population/systematic detector uncertainty。real O3 examples 无 ground truth，论文只展示重新排序信息。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2504.17587；期刊：https://doi.org/10.1103/yfb3-fgf2。核验 PDF SHA-256：04f58b3b32dcc6240c94361c819259a4d2c160e25ae366d9618d46527716fcb5。数据来自文中引用的 O3 MDC 与公开 candidate products；应按当前 Data/Code statement 获取版本。", "复现需固定四 pipeline releases、candidate matching、IFAR threshold、zero imputation、feature transforms、split permutations、LR/MLP hyperparameters、calibration fraction 与 conformal α。Evidence status: full-text verified ML/MDC study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–2 数据构造和 Figure 1 ROC；pp.2–3 Figure 2 理解 confidence 与 IFAR 差别，p.4 Figure 3 看 real-candidate disagreement。再读 Appendix 的 CP、permutation、feature importance，保留 exchangeability 和 prevalence-shift 边界。"),
        ],
        "figure-1-gw-pipeline-roc.webp", "Figure 1", 2, "comparison",
        "LR、MLP 多管线组合与 maximum-IFAR 基线在 O3 MDC test data 上的 ROC 及置换不确定区间。",
        "在该模拟挑战集上，MLP 和 LR 的 AUC 均高于简单 maximum-IFAR 组合。",
        "Figure 1 是组合管线 ranking 增益的主要量化证据，并同时呈现数据划分置换带来的不确定性。",
        [{"label":"Conformal prediction set","latex":r"\Gamma_\alpha(x)=\{y:\;s(x,y)\le q_{1-\alpha}^{(y)}\}","role":"turn a meta-classifier score into label-conditional prediction sets","symbols":{"s":"nonconformity score","q":"calibration quantile","alpha":"target miscoverage"},"evidence":"paper.pdf pp. 2–3 and Appendix, conformal-prediction construction","interpretation":"Coverage requires exchangeability between calibration and future labeled candidates; the set is not a posterior astrophysical probability."}],
        ["paper.pdf pp. 1–2, Figure 1: MDC dataset and ROC/AUC comparison","paper.pdf pp. 2–3, Figure 2: label-conditional confidence versus IFAR","paper.pdf pp. 3–4, Figure 3: O3 candidate disagreement analysis","paper.pdf pp. 6–10, Figures 4–5: permutation, features and SNR appendix checks","source PDF SHA-256 04f58b3b32dcc6240c94361c819259a4d2c160e25ae366d9618d46527716fcb5","Evidence status: full-text verified ML/MDC study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1126-sciadv.aay2631", "arXiv v2 manuscript", "https://arxiv.org/pdf/1905.11481",
        "AI Feynman: A Physics-Inspired Method for Symbolic Regression", "AI Feynman：物理启发的符号回归方法",
        "ai_empirical", "a92d150747fd05c8", "AI for Science",
        {"doi":"10.1126/sciadv.aay2631","arxiv_id":"1905.11481","version":"arXiv v2 full text","title":"AI Feynman: A physics-inspired method for symbolic regression","authors":["Silviu-Marian Udrescu","Max Tegmark"],"journal":"Science Advances","volume":"6","issue":"16","article":"eaay2631","published":"2020-04-17","abstract":"A recursive symbolic-regression system combines neural fitting with dimensional analysis, symmetry, separability, transformations, polynomial fitting, and brute-force search to recover physics equations.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Silviu-Marian Udrescu、Max Tegmark；Science Advances 6, eaay2631 (2020)，DOI:10.1126/sciadv.aay2631。核验 arXiv:1905.11481v2 全文15页及代码/数据声明；未发现关联更正或撤稿。"),
            sec("研究问题", "symbolic regression 要从数值表恢复可解释公式，一般 expression search 呈组合爆炸。论文问：科学公式常见的 units、low-order polynomial、compositionality、smoothness、symmetry 与 separability 能否被自动检测，用递归降维把困难高维搜索拆成简单子问题？"),
            sec("背景", "AI Feynman 不让 neural network 直接输出 token equation；网络先拟合 smooth mystery function，再作为数值 oracle 检测平移/缩放 symmetry 和 additive/multiplicative separability。确认结构后重采样更少变量的新数据集并递归求解，最终由 polynomial fit 或 enumerative brute force 找 closed form。", "dimensional analysis 使用已知变量 units 构造无量纲组合；因此含单位 benchmark 得到额外先验。若 units 未知、数据域太窄或网络近似误导 symmetry test，递归分解可能错误。"),
            sec("模型与方法", "pipeline 依次尝试 dimensional analysis、polynomial fitting、symbolic brute force、NN symmetry、separability、equating variables 与 x/y transformations；每个成功 simplification 生成低维 mystery。Figure 1 是递归控制流，Figure 2 以九变量 Newton gravity 逐步展示无量纲化、两个 translational symmetries 与 multiplicative factorization。", "测试集含 Feynman Lectures 的100个 equations 和更困难的 physics-inspired bonus set；输入由真实公式采样，使用相对误差/复杂度 criterion 判断 exact recovery。与商用 Eureqa 和公开 methods 比较，并讨论 additive noise robustness。"),
            sec("核心结果与证据", "论文报告在无噪声 Feynman 100 equations 上恢复全部100个，而此前公开软件恢复71个；在 harder physics-inspired set 上 success rate 从约15%提高到90%。数字来自作者构造 benchmark、采样范围、function grammar 与 timeout，不等于任意科学数据的发现率。", "Figure 1 表明 performance 不是单一 NN 的结果，而是 physics priors、recursive decomposition 和 symbolic search 的组合。gravitational-force example 中 dimensional analysis 从九变量降维，NN 检测差分 symmetry，再把问题乘法分离为两个可由 polynomial/inversion 解的子式。", "noise tests 显示随着 noise 增大 recovery 下降，但 NN interpolation 与结构测试仍能在部分范围找到精确/近似式。没有独立 ablation 能把所有增益唯一归因于某一模块；benchmark formulas 与 algorithm priors 高度匹配是设计优势也是选择偏差。"),
            sec("有效性与局限", "方法假定 target 可由有限 elementary-function grammar 表达且采样覆盖足以显露 symmetry/separability；变量单位往往需要用户提供。真实实验的 heteroscedastic noise、hidden variables、systematic bias 与非解析响应可能产生漂亮但错误的公式。", "exact fit 与 dimensional consistency 不是因果或物理真实性证明，仍需 held-out regimes、limiting cases 与实验验证。brute-force cost 随剩余复杂度增长；NN hyperparameters和 thresholds 会影响分解，论文 benchmark 也不是盲测真实 discovery。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/1905.11481；期刊：https://doi.org/10.1126/sciadv.aay2631；代码：https://github.com/SJ001/AI-Feynman。核验 PDF SHA-256：bea0a57b25041b2fab181efdf543279de6f7ac88ab3aca2fff92173c56cd801f。", "复现需固定代码 commit、sampling domains、units table、NN architecture/training、symmetry thresholds、operator grammar、complexity penalty、noise model 与 time limit，并逐 equation 保存 recovered expression。Evidence status: full-text verified algorithm/benchmark study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–3 Figures 1–2 理解递归 workflow；pp.3–7 逐模块看 dimensional analysis、symmetry 与 separability。pp.8–11 检查 benchmark 和 noise tables，最后读 conclusions 与 code statement；将公式恢复和科学确认分开。"),
        ],
        "figure-1-ai-feynman-flowchart.webp", "Figure 1", 2, "schematic",
        "AI Feynman 从量纲分析、拟合和暴力搜索到神经网络结构检测与递归降维的流程图。",
        "算法反复寻找物理结构并生成更低维子问题，直到得到符号式或明确失败。",
        "Figure 1 清楚定义混合算法各模块与递归关系，避免把结果误归因于单一神经网络。",
        [{"label":"Dimensional reduction","latex":r"x_i'=\prod_jx_j^{U_{ji}},\qquad y'=y/y^*,\qquad MU=0,\;Mp=b","role":"replace dimensional variables by invariant dimensionless combinations","symbols":{"M":"matrix of unit exponents","U":"null-space basis","b":"output-unit vector"},"evidence":"paper.pdf p. 3, Eq. (1)","interpretation":"The reduction requires correct unit metadata and does not discover omitted physical dimensions."}],
        ["paper.pdf pp. 1–3, Figures 1–2: workflow and gravity example","paper.pdf pp. 3–7: dimensional, symmetry and separability modules","paper.pdf pp. 8–11: Feynman and harder-set benchmarks plus noise tests","paper.pdf pp. 11–13: conclusions and failure modes","source PDF SHA-256 bea0a57b25041b2fab181efdf543279de6f7ac88ab3aca2fff92173c56cd801f","Evidence status: full-text verified algorithm/benchmark study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1126-scirobotics.abd9285", "arXiv v2 submitted manuscript (2018)", "https://arxiv.org/pdf/1803.06425",
        "Reinforcement Learning with Artificial Microswimmers", "人工微泳者的强化学习",
        "ai_empirical", "913f9cbf33039eb7", "Control & Reinforcement Learning",
        {"doi":"10.1126/scirobotics.abd9285","arxiv_id":"1803.06425","version":"arXiv v2 submitted manuscript (2018); final journal metadata cross-check","title":"Reinforcement learning with artificial microswimmers","authors":["Santiago Muiños-Landin","Alexander Fischer","Viktor Holubec","Frank Cichos"],"journal":"Science Robotics","volume":"6","issue":"52","article":"eabd9285","published":"2021-03-17","abstract":"Real-time microscopy, laser steering, and tabular Q-learning enable thermophoretic microswimmers to learn grid-world navigation under Brownian noise and share experience across swimmers.","comment":"Evidence pages and source figure use arXiv:1803.06425v2 (2018), whose author list predates the four-author 2021 journal version; final metadata was cross-checked separately"},
        [
            sec("作者信息", "最终期刊元数据作者 Santiago Muiños-Landin、Alexander Fischer、Viktor Holubec、Frank Cichos；Science Robotics 6, eabd9285 (2021)，DOI:10.1126/scirobotics.abd9285。本卡页码证据来自 arXiv:1803.06425v2（2018，8页），该提交稿作者表较早且不等同最终 author list；因此不把提交稿当作逐字期刊版。"),
            sec("研究问题", "microswimmer 的 propulsion direction 会被 Brownian rotation/translation 扰乱，且粒子本身没有传感、记忆或计算器。论文问：能否用 microscopy feedback 外部感知真实粒子位置，用 laser steering 执行动作并以 Q-learning 存储经验，让物理 microswimmer 在 noisy gridworld 中学会到达目标、绕开障碍和共享策略？"),
            sec("背景", "实验粒子是约2.19 μm melamine spheres，约30%表面覆 gold nanoparticles；偏置532 nm heating laser 产生 self-thermophoretic propulsion。30×30 μm 视场被划为5×5 states，每个 state 有八个 steering actions。", "这是 hybrid embodied RL：agent body 和流体噪声真实存在，但 camera、image analysis、Q table、reward与laser controller均在外部计算机。它没有证明微粒内部产生 autonomously stored intelligence，也不涉及 deep RL。"),
            sec("模型与方法", "每次粒子跨 state 后按 Qt+Δt(s,a)=Qt(s,a)+α[R(s)+γmax Q(s′,a′)−Qt(s,a)] 更新。到 goal 给 reward，离开边界或进入 virtual obstacle 给 penalty；policy 为每个 state 的 argmax action。", "Brownian strength用 Peclet number Pe=lv/D 表征；文中 D≈0.23 μm²/s、grid length l=6 μm。作者比较不同 Pe 下 policy transfer、learning speed、best-vs-second action contrast，并让两粒子共享同一 Q matrix，记录实验 trajectories 而非纯模拟。"),
            sec("核心结果与证据", "Figure 2 在 Pe=80 展示 Q-sum 随约5500 steps/300余 episodes趋稳；从左下出发到 goal 的平均 transitions 从初期约90降至约7。trajectory 从多 loops 变为较直接路径，before/after policy maps 明显改变。", "Figure 3 显示固定 policy 下 Pe 从53增至135时平均 path length约从46 μm降至33 μm、到达时间从18 s降至6 s；Pe=150 的学习约1000 steps接近收敛，而 Pe=87需5000余 steps。低 Pe policy 更避开 boundary，说明 Brownian noise 不只减速，也改变风险策略。", "virtual obstacles 可通过 penalties 学会绕行；两个 swimmers 共享 Q matrix 时比单粒子更快收敛。‘collective learning’在这里是并行 experience sharing，不是粒子间局部通信或自发群体 policy。"),
            sec("有效性与局限", "state/action/reward 全由人预设，视场小且 target 固定；外部 controller 实时追踪和逐粒子 laser actuation，扩展到大量 swimmers 存在 sensing/assignment bandwidth 限制。实验 episodes 数少于现代 RL benchmarks，没有多 seed confidence intervals或替代算法比较。", "早期 arXiv 证据与2021最终论文在作者与修订状态上不同，本卡只把可页码化的提交稿用于核心实验数字，并以 Crossref/期刊记录给最终 metadata。潜在流动、容器缺陷与粒子差异是现实噪声，也限制精确复现。"),
            sec("复现与资源", "提交稿全文：https://arxiv.org/abs/1803.06425；最终期刊：https://doi.org/10.1126/scirobotics.abd9285。核验提交稿 PDF SHA-256：afa468a148bf169f609c3296f14edb83b2f72a8d992d2f90a0cead63be2bc113。", "复现需固定 particle coating、cell thickness、laser power/offset、frame exposure 180 ms、tracking、state size、α、γ、reward/penalty、Pe、episode termination 与 Q initialization；应保存 raw video和每步 state/action/Q。Evidence status: page-addressable submitted-manuscript experiment verified with explicit version boundary; no independent reproduction performed."),
            sec("阅读指南", "先读提交稿 pp.1–2 Figure 1 看装置、state/action和外部控制边界；p.3 Figure 2 是单粒子学习主证据，pp.4–5 Figure 3 看 Brownian noise、障碍和共享经验。最后读 Methods，并把2018提交稿证据与2021最终作者/元数据分开。"),
        ],
        "figure-2-microswimmer-learning.webp", "Figure 2", 3, "trajectory",
        "真实热泳微粒的 Q 值收敛、训练阶段轨迹、不同起点路径以及学习前后策略图。",
        "随着经验积累，微粒到目标的路径由循环游走转为近定向，并显著减少所需 state transitions。",
        "Figure 2 是提交稿中真实单微粒学习的核心可视证据，同时展示数值收敛、轨迹和 policy 变化。",
        [{"label":"Q-learning update","latex":r"Q_{t+\Delta t}(s,a)=Q_t(s,a)+\alpha\left[R(s)+\gamma\max_{a'}Q_t(s',a')-Q_t(s,a)\right]","role":"store transition experience and update the externally controlled swimmer policy","symbols":{"alpha":"learning rate","gamma":"discount factor","R":"state reward","s_prime":"next observed state"},"evidence":"submitted manuscript p. 4, Eq. (1)","interpretation":"Learning and memory reside in the external computer/Q table, while the swimmer supplies real noisy dynamics."}],
        ["submitted manuscript pp. 1–2, Figure 1: particle, actions and gridworld","submitted manuscript p. 3, Figure 2: single-swimmer learning trajectories","submitted manuscript pp. 4–5, Figure 3: Peclet number, obstacles and shared-Q results","submitted manuscript pp. 6–7: experimental methods","source PDF SHA-256 afa468a148bf169f609c3296f14edb83b2f72a8d992d2f90a0cead63be2bc113","Evidence status: page-addressable submitted-manuscript experiment verified with explicit version boundary; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ids: list[str] = []
    for item in CARDS:
        pid = str(item["arxiv_id"])
        (OUT / f"{pid}.json").write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ids.append(pid)
    print(json.dumps({"installed": ids}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
