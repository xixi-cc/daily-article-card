#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 040."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1103-physrevlett.133.217101", "arXiv v2 manuscript", "https://arxiv.org/pdf/2406.19235",
        "Gauge Invariance of Equilibrium Statistical Mechanics", "平衡统计力学的规范不变性", "theory_numerics",
        "60da8b4e31b6d764", "Statistical Physics",
        {"doi":"10.1103/PhysRevLett.133.217101","arxiv_id":"2406.19235","version":"arXiv v2 full text","title":"Gauge Invariance of Equilibrium Statistical Mechanics","authors":["Johanna Müller","Sophie Hermann","Florian Sammüller","Matthias Schmidt"],"journal":"Physical Review Letters","volume":"133","issue":"21","article":"217101","published":"2024-11-18","abstract":"Local canonical shifts of particle positions and momenta form a noncommutative gauge group whose invariance yields exact equilibrium sum rules and leaves thermal observables unchanged under finite transformed-space sampling.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Johanna Müller、Sophie Hermann、Florian Sammüller、Matthias Schmidt；PRL 133, 217101 (2024)。全文 arXiv:2406.19235v2 共7页；Crossref 未列更正或撤稿。"),
            sec("研究问题","已有工作用 phase-space shifting 从 Noether invariance 导出 statistical-mechanical sum rules，但变换的物理和群结构未明确。论文问：任意局域坐标微分同胚及配套动量变换能否被识别为 microstate gauge transformation，其生成元代数又能否系统地产生可测的精确恒等式？"),
            sec("背景","规范变换的定义性特征是改变描述变量而不改变 observables。这里不是电磁 U(1) gauge field，而是经典粒子相空间的局域重参数化；把两者混同会过度解释。","作者在 grand canonical equilibrium 中研究标准 kinetic energy、interparticle potential u 与 external potential Vext，并要求变换 canonical、Jacobian 为1，从而保持 phase-space measure。"),
            sec("模型与方法","每个粒子作 ri→ri+ε(ri)，动量作 pi→[1+∇iε(ri)]^−1·pi。连续 vector field ε 需使位置映射为 smooth bijection；无穷小 generator σ(r) 同时作用于位置和动量。","作者计算 generator commutator，得到由 Lie bracket 组成的 noncommutative algebra；对 arbitrary observable A 热平均后推出一体、二体 hyperforce correlation sum rules。有限变换则通过在 transformed coordinates 直接做 Monte Carlo 检验。"),
            sec("核心结果与证据","不同局域 shifts 的作用次序一般不交换；commutator 仍是同类 shift generator，因此形成闭合 Lie algebra。把 operator identities 热平均后，Eq. (15) 把代数结构印到 force/hyperforce correlation functions，并导出不同位置的 exchange symmetry。","Figure 2 比较一维 hard rods 在两硬墙间的 unshifted 与 sinusoidally shifted sampling。虽然 Markov chains 和 coordinates 不同，density profile ρ(x) 与 one-body phase-space distribution f(x,p) 数值相同。","Figure 3 对 Lennard–Jones particles 的 LJ-wall confinement、单粒子 double well 和五粒子 double well 重复验证；shifted/unshifted equilibrium averages 重合，说明结果不依赖 hard-core 特例。数值证据是 invariance demonstration，不是对所有 Hamiltonians 的穷尽验证。"),
            sec("有效性与局限","理论要求 equilibrium trace、canonical smooth diffeomorphism 和标准 kinetic energy；不适用于任意非保体积映射、奇异 shift 或 nonequilibrium steady states。作者把与 stochastic-thermodynamic fluctuation theorems 的关系留作未来。","Monte Carlo examples 都是一维且体系很小，主要检验变量变换与采样实现；它们不能单独证明高维 interacting fluids 中所有 estimator 都具有相同 numerical efficiency。‘更深基础’是研究方向，不是已经建立的新基本理论。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2406.19235；期刊：https://doi.org/10.1103/PhysRevLett.133.217101。PDF SHA-256：3aa2ea2dd06b6015ae030121bf64e4f781a6df31ecffb5375f46ebe5ebd9e9f0。全文未给代码仓库。","复现需固定 grand ensemble、walls/LJ/double-well potentials、ε(x)、Jacobian/momentum map、MC proposal与采样长度；同时输出 unshifted/shifted ρ、f、force density及误差，并逐式验证 commutator 与 sum rules。Evidence status: full-text verified theory/Monte-Carlo study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Eqs. (1)–(6) 掌握 canonical shift 与 Lie algebra；pp.2–4 Eqs. (7)–(16) 看 sum-rule construction。Figure 2 是最直观数值检验，pp.5–6 Figure 3 展示软势推广；最后保留 equilibrium/canonical 限制。"),
        ],
        "figure-2-gauge-invariance.webp", "Figure 2", 4, "comparison",
        "一维 hard rods 在原坐标与有限 sinusoidal gauge shift 后的位移场、密度和相空间分布。",
        "坐标与采样链明显改变，但 ρ(x) 和 f(x,p) 在变换前后数值一致。",
        "Figure 2 直接把抽象 gauge invariance 转化为可比较的 Monte Carlo observables。",
        [{"label":"Canonical particle shift","latex":r"\tilde{\mathbf r}_i=\mathbf r_i+\boldsymbol\epsilon(\mathbf r_i),\qquad \tilde{\mathbf p}_i=[\mathbf 1+\nabla_i\boldsymbol\epsilon(\mathbf r_i)]^{-1}\mathbf p_i","role":"reparameterize microstates while preserving phase-space volume","symbols":{"epsilon":"smooth local shift field","r_i":"particle position","p_i":"particle momentum"},"evidence":"paper.pdf p. 1, Eqs. (1)–(2)","interpretation":"The map must be a smooth bijective canonical transformation; it is not an arbitrary displacement."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(6) and Figure 1: gauge map and noncommutative generators","paper.pdf pp. 3–4, Eqs. (7)–(16) and Figure 2: exact sum rules and hard-rod sampling","paper.pdf pp. 5–6, Figure 3: Lennard-Jones and double-well finite-shift checks","source PDF SHA-256 3aa2ea2dd06b6015ae030121bf64e4f781a6df31ecffb5375f46ebe5ebd9e9f0","Evidence status: full-text verified theory/Monte-Carlo study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.134.177301", "arXiv v1 manuscript", "https://arxiv.org/pdf/2407.07168",
        "Statistical Mechanics of Transfer Learning in Fully Connected Networks in the Proportional Limit", "比例极限下全连接网络迁移学习的统计力学", "ai_empirical",
        "f9013ded711d08ef", "Training Dynamics",
        {"doi":"10.1103/PhysRevLett.134.177301","arxiv_id":"2407.07168","version":"arXiv v1 full text","title":"Statistical Mechanics of Transfer Learning in Fully Connected Networks in the Proportional Limit","authors":["Alessandro Ingrosso","Rosalba Pacelli","Pietro Rotondo","Federica Gerace"],"journal":"Physical Review Letters","volume":"134","issue":"17","article":"177301","published":"2025-04-30","abstract":"A single-instance Franz-Parisi theory for finite-width transfer learning predicts how source-target feature relatedness renormalizes kernels and controls when freezing or fine-tuning improves generalization.","comment":"ArXiv v1 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Alessandro Ingrosso、Rosalba Pacelli、Pietro Rotondo、Federica Gerace；PRL 134, 177301 (2025)。全文 arXiv:2407.07168v1 共26页含附录；Crossref 未列更正或撤稿。"),
            sec("研究问题","lazy infinite-width kernel limit 中 features 基本不变，因此无法解释典型 transfer learning。论文问：当样本数 P 与 hidden width N 同时趋大且 α=P/N 有限时，如何对 source-pretrained weights 作 quenched average，并预测 freeze、fine-tune 或 scratch training 的 test error？"),
            sec("背景","transfer 是否有益取决于 source/target relatedness、数据量和网络宽度，不只是正则化。作者借用 spin-glass Franz–Parisi potential：source posterior 先独立形成，再用 coupling γ 把 target first-layer weights 拉向一个 quenched source configuration。","γ=0 表示 target scratch；γ→∞ 冻结 source features；有限 γ 描述 fine-tuning。该 mapping 是 Bayesian equilibrium learning theory，不等同于实际 SGD time dynamics。"),
            sec("模型与方法","主体分析 one-hidden-layer fully connected network，source 有 Ps 样本、target 有 Pt 样本；Gaussian priors 与 quadratic loss 形成 Boltzmann measure。single-instance 指不对具体 input dataset 再作 disorder average，只对 source weights 作 quenched replica calculation。","在 proportional limit 通过 order parameters Qs、Qt、Qst、Qtt 得到 source、target 和 cross kernels；kernel covariance 显式含 source-target input overlap。对 C-EMNIST 与 C-CIFAR binary tasks 做有限宽 Bayesian numerical experiments，并比较 theory curves、test loss 与 last-layer weight norms。"),
            sec("核心结果与证据","理论给出 renormalized source-target kernel：Qst 与 modified covariance 编码 transferred representation 的相关性，test error 可由 transfer action 的 derivatives 求得。若 source/target feature overlap 有用，kernel renormalization 可让 target generalization 优于 scratch；不相关迁移则可能无益。","Figure 1 中 C-EMNIST test loss 随 γ 持续下降并趋于 frozen-feature plateau；C-CIFAR 在部分宽度存在有限 γ optimum，而更宽网络的 optimum 推向大 γ。相同图的 weight norms 及测试损失 dots 与 theory solid curves 在误差范围内吻合。","Figure 2/3 进一步改变 dataset relatedness、width 和 source sample richness，表明 transfer benefit 不是单调 universal rule。作者还用 matched linear teacher 检查性能提升确由 transfer 而非仅 effective regularization；深层网络推广在附录是 tentative derivation。"),
            sec("有效性与局限","结论针对 Bayesian posterior、quadratic loss、Gaussian prior、全连接网络和 proportional thermodynamic limit；真实 SGD、cross-entropy、convolutional inductive bias 与大模型预训练不在精确理论范围。C-EMNIST/C-CIFAR 是缩放灰度 binary constructions，不代表完整视觉 benchmark。","nonlinear activation 依赖 Gaussian equivalence 与 replica-symmetric saddle；没有严格证明所有参数区 replica symmetry 稳定。有限网络实验支持公式但规模约500–1000 hidden units，不能直接外推到 foundation models。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2407.07168；期刊：https://doi.org/10.1103/PhysRevLett.134.177301。PDF SHA-256：ea539b508124f969bb0e6e078d31666783c4a70f032c7798b4267971cb5251fc。正文未给专用代码仓库。","复现需固定 C-EMNIST/C-CIFAR class split、resize/projection、Ps=800、Pt=100等样本规模、N1、activation、priors λ、inverse temperature、γ grid、Bayesian sampler和 source configurations；同时数值解 saddle equations。Evidence status: full-text verified theory/finite-network study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 Figure 1 和 Eq. (1) 理解 γ 三种训练极限；pp.3–5 看 replica action、renormalized kernels 与 benchmark。附录 pp.8–21 给完整推导和 generalization-error formula；区分精确单层结果与 tentative deep extension。"),
        ],
        "figure-1-transfer-theory.webp", "Figure 1", 2, "comparison",
        "single-instance Franz–Parisi transfer 架构，以及 C-EMNIST/C-CIFAR 的 test loss、weight norm 理论—实验曲线。",
        "transfer coupling γ 的最佳值依赖 task relation 与 width；有限宽理论与 Bayesian network experiments 一致。",
        "Figure 1 同时说明 quenched source 的建模方式并验证最核心的 generalization prediction。",
        [{"label":"Transfer Franz-Parisi potential","latex":r"f=\frac{1}{N_1}\mathbb E_{\theta_s}\log\!\int d\mu(\theta_t)e^{-\beta_t\mathcal L_t(\theta_t)-\frac{\gamma}{2}\|\mathbf w_s-\mathbf w_t\|^2}","role":"interpolate between target scratch training, fine-tuning, and frozen source features","symbols":{"gamma":"source-target first-layer coupling","theta_s":"quenched source weights","theta_t":"target weights"},"evidence":"paper.pdf p. 3, Eq. (1)","interpretation":"This is an equilibrium Bayesian model of transfer, not the temporal dynamics of SGD."}],
        ["paper.pdf pp. 1–2, Figure 1: transfer setting and finite-width theory/data agreement","paper.pdf pp. 3–5, Eqs. (1)–(6) and Figures 2–3: Franz-Parisi action, kernels and benchmarks","paper.pdf pp. 8–21: replica derivation, saddle equations and generalization error","source PDF SHA-256 ea539b508124f969bb0e6e078d31666783c4a70f032c7798b4267971cb5251fc","Evidence status: full-text verified theory/finite-network study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.135.187402", "arXiv v2 manuscript", "https://arxiv.org/pdf/2408.17360",
        "Nonreciprocal Spin-Glass Transition and Aging", "非互易自旋玻璃转变与老化", "theory_numerics",
        "c61bbb4b2f401acc", "Nonreciprocal Systems",
        {"doi":"10.1103/PhysRevLett.135.187402","arxiv_id":"2408.17360","version":"arXiv v2 full text","title":"Nonreciprocal Spin-Glass Transition and Aging","authors":["Giulia Garcia Lorenzana","Ada Altieri","Giulio Biroli","Michel Fruchart","Vincenzo Vitelli"],"journal":"Physical Review Letters","volume":"135","issue":"18","article":"187402","published":"2025-10-30","abstract":"Two identical spherical spin glasses coupled antagonistically retain a finite-temperature glass transition and exhibit exceptional-point-mediated oscillations superimposed on aging, unlike models with microscopic random nonreciprocity.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Giulia Garcia Lorenzana、Ada Altieri、Giulio Biroli、Michel Fruchart、Vincenzo Vitelli；PRL 135, 187402 (2025)。全文 arXiv:2408.17360v2 共10页；Crossref 未列更正或撤稿。"),
            sec("研究问题","随机非对称 microscopic couplings 常被认为会切断 spin-glass aging。论文问：若 nonreciprocity 发生在两个各自具有复杂 glassy internal dynamics 的宏观 agents 之间，而不是每个 microscopic spin pair 上，玻璃转变和 aging 是否仍必然消失？"),
            sec("背景","作者区分 microscopic nonreciprocity（随机 non-Hermitian interaction matrix）与 macroscopic nonreciprocity（两个相同复杂系统以相反符号整体耦合）。前者打乱能量景观的每个方向，后者保留两系统共享的内部 eigenmodes。","模型可能启发生态/生物 coarse-grained agents，但正文没有具体实验拟合；主要结论属于 spherical Sherrington–Kirkpatrick theory。"),
            sec("模型与方法","两个相同 spherical SK systems s1、s2 共用一张 symmetric random matrix J，并以 +α 与 −α antagonistic coupling 连接；Lagrange multipliers 保持各自球面约束。作者用 dynamical mean-field theory 求 response/correlation，并在 J eigenbasis 分析 quench dynamics。","线性 stability 的 non-Hermitian mode pairs 在 exceptional points 合并；有限 N Langevin simulations 检查 critical correlators、aging collapse 和长时最低 eigenmodes rotation。对照模型则让 microscopic couplings 随机非对称。"),
            sec("核心结果与证据","系统在 Tc=1 保留 finite-temperature transition：高温是 static disordered phase，临界 response/correlation 的 singularities 从 ω=0 平移到 ω/α=±1。transition 由 exceptional-point spectral singularity 介导，而 critical exponent structure 与 uncoupled spherical SK 对应。","Figure 2(c) 显示不同 waiting time t′ 的 autocorrelation 经 Edwards–Anderson normalization 后，叠加 slow aging envelope 与频率 α 的 oscillations。解析式含 cos(αΔt) 和 Δt/t′ aging factor，与模拟一致；振荡周期约1/α，而 coherence time 随 system age t′ 增长。","长期有限 N 极限中运动投影到 J 的最低能量 mode plane，形成半径缓慢演化、角速度 α 的旋转。若两系统 internal matrices 不完全相同，aging 获得有限寿命；因此 survival 依赖 shared internal structure，不是任意 nonreciprocity 都保留 glassiness。"),
            sec("有效性与局限","精确解析依赖 spherical SK、identical internal disorder、thermodynamic/long-time limit 顺序与 mean-field connectivity。真实有限维 glass、activated events 和结构不匹配可能削弱或终止 aging。","有限 N 最终 relaxation time 仍有限，严格 t→∞ 会离开 aging regime；数值只是有限规模支持。实验关联、p-spin 更丰富 phase diagram 和 universality beyond spherical case 需要后续研究。"),
            sec("复现与资源","全文：https://arxiv.org/abs/2408.17360；期刊：https://doi.org/10.1103/PhysRevLett.135.187402。PDF SHA-256：66a4c3cc12b8607dc7e520c5e1f7ff17defe461db896f46de7a9f028c633112d。全文未给代码仓库。","复现需固定 J ensemble、共享/不匹配 matrices、N、α、T、spherical constraint integrator、quench initial conditions、waiting-time grid和 normalization；分别比较 DMFT spectra、Figure 2 collapse 与最低 modes projection。Evidence status: full-text verified theory/simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–2 模型与 Figure 1 exceptional-point mechanism；p.3 Figure 2 是 nonreciprocal aging 的核心。pp.4–5 看 finite-N asymptotics 和 microscopic-nonreciprocity 对照，再查补充部分的 DMFT derivation 与数值细节。"),
        ],
        "figure-2-aging-correlations.webp", "Figure 2", 3, "comparison",
        "临界 response/correlation spectra 与不同 waiting time 下的归一化 aging correlation。",
        "谱奇点位于 ±α；时域相关同时具有频率 α 的振荡和随等待时间增长的慢 aging envelope。",
        "Figure 2 是 exceptional-point transition 与 nonreciprocal aging 两个核心命题的联合证据。",
        [{"label":"Nonreciprocal aging correlator","latex":r"C_d(t,t')=q_{EA}\left(\frac{2\sqrt{1+\Delta t/t'}}{2+\Delta t/t'}\right)^{3/2}\cos(\alpha\Delta t)","role":"separate slow aging envelope from persistent nonreciprocal oscillations","symbols":{"q_EA":"Edwards-Anderson order parameter","alpha":"antagonistic coupling","Delta t":"time difference","t_prime":"waiting time"},"evidence":"paper.pdf p. 3, Eq. (7) and Figure 2(c)","interpretation":"The expression is asymptotic for the identical spherical-SK pair after a subcritical quench."}],
        ["paper.pdf pp. 1–2, Figure 1 and Eqs. (1)–(5): coupled spherical glasses and exceptional points","paper.pdf p. 3, Figure 2 and Eqs. (6)–(7): critical spectra and aging correlator","paper.pdf pp. 4–5, Figures 3–5: finite-N asymptotics and microscopic-nonreciprocity contrast","source PDF SHA-256 66a4c3cc12b8607dc7e520c5e1f7ff17defe461db896f46de7a9f028c633112d","Evidence status: full-text verified theory/simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevlett.75.1226", "APS published full text", "https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.75.1226/fulltext",
        "Novel Type of Phase Transition in a System of Self-Driven Particles", "自驱动粒子系统中的新型相变", "numerical",
        "95a65196f5ad52df", "Statistical Physics",
        {"doi":"10.1103/PhysRevLett.75.1226","version":"APS published full text","title":"Novel Type of Phase Transition in a System of Self-Driven Particles","authors":["Tamás Vicsek","András Czirók","Eshel Ben-Jacob","Inon Cohen","Ofer Shochet"],"journal":"Physical Review Letters","volume":"75","issue":"6","pages":"1226-1229","published":"1995-08-07","abstract":"The original constant-speed local-alignment particle model shows numerical evidence for a continuous noise- or density-driven transition from disordered motion to spontaneous macroscopic transport.","comment":"Published APS full text cross-checked with Crossref metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Tamás Vicsek、András Czirók、Eshel Ben-Jacob、Inon Cohen、Ofer Shochet；PRL 75, 1226–1229 (1995)。APS 期刊全文共4页；Crossref 未列更正或撤稿。"),
            sec("研究问题","能否用最少的运动规则产生 spontaneous collective motion？论文提出后来称为 Vicsek model 的二维自驱粒子系统，问局域速度方向对齐与角噪声的竞争是否产生从零净输运到有限 flocking order 的 kinetic phase transition。"),
            sec("背景","模型借鉴 XY ferromagnet：alignment 类似 ferromagnetic interaction，noise η 类似温度。但粒子持续运动、邻居随时间改变且碰撞不守恒总动量，因此这是 far-from-equilibrium dynamic system，不是平衡 XY 模型的直接实现。","1995 年结果是奠基性有限尺寸数值证据；后来的理论对 transition order、banding 和 finite-size effects 有更精细认识，本卡只陈述原文自身结论。"),
            sec("模型与方法","N 个点粒子在 L×L 周期方盒以固定 speed v 更新；每步先把粒子方向设为半径 r=1 邻域中 velocities 的平均方向，再加均匀角噪声 η，随后按新方向平移。论文主要取 v=0.03，报告 0.003<v<0.3 范围结果相近。","扫描 density ρ=N/L²（原排版文字处符号略有 OCR 失真）与 η；order parameter va 是全体 normalized velocity vector 的模。系统规模从 N=40 到10000，多初态 runs 估计临界附近波动，并对 ηc(L)、ρc(L) 和 log-log slopes 做 finite-size analysis。"),
            sec("核心结果与证据","低密度/高噪声时 particles 随机移动或形成短暂小群；高密度/低噪声时所有粒子选择同一宏观方向，rotational symmetry spontaneous breaking，va 从近0变为有限。Figure 1 的 snapshots 展示 stationary、random、correlated 和 ordered motion 四种 regime。","Figure 2 显示固定 ρ 降低 η，或固定 η 增加 ρ，va 均连续上升；更大 L 的 scaling region 增宽。对 ρ=0.4 的 finite-size extrapolation 得 ηc(∞)=2.9±0.05（噪声参数 convention 按原文）。","Figure 3 的拟合给 noise-driven exponent β=0.45±0.07、density-driven exponent δ=0.35±0.06。作者强调 ηc(L)/ρc(L) 选择间接、临界附近 convergence 慢且波动大，不能排除两个 exponent 在 thermodynamic limit 相同。"),
            sec("有效性与局限","点粒子无 excluded volume、惯性、边界/流体耦合，angular noise 与 synchronous update 都是模型选择。原始论文的有限尺寸和运行长度远小于现代 studies，连续转变判断不能被视为关于所有 Vicsek-class variants 的最终结论。","critical point 通过让 log plot 最直来选，systematic uncertainty 显著；五次初态在 N=4000/10000 临界区仍约5%误差。生物群、细菌和 air-table disks 只是潜在应用/类比，不是本文实验验证。"),
            sec("复现与资源","全文：https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.75.1226/fulltext；期刊：https://doi.org/10.1103/PhysRevLett.75.1226。PDF SHA-256：95a65196f5ad52df06327d3beb97c1739af0079b16019cc6c7afc506714c7329。","复现需固定 synchronous order、r=1、v=0.03、periodic boundaries、angle-noise normalization、N/L/ρ、thermalization/sample time和 seeds；报告 va time series、susceptibility/bands以及现代 finite-size checks，勿只复刻直线拟合。Evidence status: full-text verified historical simulation study; no independent reproduction performed."),
            sec("阅读指南","先读 p.1 的 update rule 与 Figure 1；pp.2–3 Figures 2–3 是 phase transition 和 exponent evidence。p.4 重点读作者对 indirect critical-point selection、crossover 和有限尺寸误差的自我限定，再与后续 Vicsek literature 分开。"),
        ],
        "figures-2-3-flocking-transition.webp", "Figures 2–3", 3, "data_plot",
        "多尺寸平均速度随噪声/密度变化，以及原文对 noise- 和 density-driven critical exponents 的 log-log 拟合。",
        "降低噪声或增加密度使净集体速度连续出现；原文估计 β≈0.45、δ≈0.35。",
        "Figures 2–3 是原始 continuous-transition claim 的定量依据，也清楚暴露有限尺寸与拟合不确定性。",
        [{"label":"Flocking order parameter","latex":r"v_a=\frac{1}{Nv}\left|\sum_{i=1}^{N}\mathbf v_i\right|","role":"measure spontaneous global transport","symbols":{"v_a":"normalized collective velocity","v":"fixed particle speed","N":"particle number"},"evidence":"paper.pdf p. 2, Eq. (3)","interpretation":"va is near zero for isotropic motion and approaches one for coherent flocking."}],
        ["paper.pdf pp. 1–2, Eqs. (1)–(3) and Figure 1: update rule, regimes and order parameter","paper.pdf p. 3, Figures 2–3 and Eq. (4): finite-size transition curves and exponent fits","paper.pdf p. 4: uncertainty, crossover and scope discussion","source PDF SHA-256 95a65196f5ad52df06327d3beb97c1739af0079b16019cc6c7afc506714c7329","Evidence status: full-text verified historical simulation study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1103-physrevx.10.011037", "arXiv v2 manuscript", "https://arxiv.org/pdf/1809.09632",
        "Optimal Renormalization Group Transformation from Information Theory", "由信息论确定的最优重整化群变换", "theory_numerics",
        "f79a10f0333402b4", "Renormalization Group",
        {"doi":"10.1103/PhysRevX.10.011037","arxiv_id":"1809.09632","version":"arXiv v2 full text","title":"Optimal Renormalization Group Transformation from Information Theory","authors":["Patrick M. Lenggenhager","Doruk Efe Gökmen","Zohar Ringel","Sebastian D. Huber","Maciej Koch-Janusz"],"journal":"Physical Review X","volume":"10","issue":"1","article":"011037","published":"2020-02-14","abstract":"Perfect real-space mutual-information coarse graining is proved not to extend interaction range and to suppress generated disorder correlations, with arbitrary clean and dilute random Ising-chain transformations providing explicit tests.","comment":"ArXiv v2 full text cross-checked with version-of-record metadata; Crossref lists no correction or retraction relation"},
        [
            sec("作者信息","作者 Patrick M. Lenggenhager、Doruk Efe Gökmen、Zohar Ringel、Sebastian D. Huber、Maciej Koch-Janusz；PRX 10, 011037 (2020)。全文 arXiv:1809.09632v2 共27页；Crossref 未列更正或撤稿。"),
            sec("研究问题","real-space RG 需要选择 coarse variables；不合适的 block rule 会产生长程、高体耦合并让 effective Hamiltonian 难处理。论文问：最大化 block 与远方 environment 的 real-space mutual information (RSMI)，是否可从理论上定义一种保留 relevant long-distance information 且使 renormalized description 最简单的“最优”RG？"),
            sec("背景","将 visible block V 压缩为 hidden H，buffer B 隔开短程信息，environment E 表示长程物理。data processing inequality 给 I(H:E)≤I(V:E)；perfect RSMI rule 达到等号。","这里的 optimality 指 interaction range、many-body terms 和 disorder-correlation generation 受控，不是声称对所有计算成本或所有动力学 observables 都最优。"),
            sec("模型与方法","coarse rule 写成 conditional probability PΛ(H|V)，可用 RBM 参数 Λ 学习。作者证明若 IΛ(H:E)=I(V:E)，则 renormalized Hamiltonian 不产生跨 buffer 的新长程 interactions；在 disordered quasi-1D systems 中 perfect capture 还稳定于局部 disorder changes。","可解 clean 1D Ising chain 以二自旋 block 压成一个 hidden spin，Λ=(λ1,λ2) 连续包含 decimation、majority 和 arbitrary rules。通过 transfer matrix/cumulant expansion 计算 RSMI、nearest/next-nearest 和 higher-body couplings；random dilute chain 再测 distance correlation、KL divergence 与 disorder-distribution displacement。"),
            sec("核心结果与证据","perfect RSMI theorem 表明，若 hidden 保留 V 对 E 的全部信息，则环境给定 H 后与 block 条件独立，因而 effective interactions 不跨越原有 locality buffer。有限 capacity 时无法 perfect capture，但 retained MI 可作物理 complexity 的连续 proxy。","Figure 4 在 (λ1,λ2) 平面比较 I(H:E)/I(V:E)、NNN/NN ratio 与 four-body/two-body ratio；MI maxima 与 interaction ‘rangeness’、‘m-bodyness’ minima 对齐。Figure 5 沿多条 RG paths 显示 retained MI 增加时两类复杂度总体下降。","clean chain 的 RSMI optimum 是 exact decimation，cumulant order 增加时回到解析 NN coupling。random dilute chain 的 Figure 9 显示 RSMI optimum 同时使邻近 renormalized couplings 的 distance correlation、KL divergence 与 distribution displacement 消失或最小，支持 disorder simplicity claim。"),
            sec("有效性与局限","严格 locality proof 要求 perfect information capture，有限 hidden capacity 时只得到经验/perturbative correlation；RSMI landscape 可能简并，optimizer 也不保证找到 global maximum。disorder theorem 的稳定性范围以 quasi-1D/local changes 为主。","实证模型是一维 clean/dilute Ising chain，不能直接证明高维 frustrated、continuous-variable 或 quantum systems 的全部结论。动力学 relevant information 还应含 long-time behavior，作者明确说 equilibrium spatial RSMI 不能直接用于 dynamical coarse-graining。"),
            sec("复现与资源","全文：https://arxiv.org/abs/1809.09632；期刊：https://doi.org/10.1103/PhysRevX.10.011037。PDF SHA-256：a21ffcedace24222abcbc367f7aa8f6b63e5a6df06897fbad01033f57d37c091。全文未给本论文专用代码仓库。","复现需固定 block/buffer/environment sizes、Ising K、PΛ ansatz、Λ grid、cumulant truncation和 exact transfer matrix；disorder case还需固定 dilution distribution、samples、distance correlation/KL estimators。Evidence status: full-text verified theory/solvable-model study; no independent reproduction performed."),
            sec("阅读指南","先读 pp.1–4 Figures 1–2 和 formalism；pp.4–7 Figures 3–5 是 clean-chain complexity evidence。pp.8–11 看 capacity constraints，pp.12–14 Figure 9 看 disorder result；附录给 proofs/expansions，结尾明确 quantum/dynamics 尚开放。"),
        ],
        "figure-4-rsmi-complexity.webp", "Figure 4", 6, "field_map",
        "RG-rule 参数空间中的 retained mutual information、next-nearest/nearest coupling ratio 和 four-body/two-body ratio。",
        "RSMI 最大区域与长程及高体 effective couplings 的最小区域对应。",
        "Figure 4 把“保留长程信息”与“简化 renormalized Hamiltonian”在同一参数空间直接对照。",
        [{"label":"RSMI objective","latex":r"\max_{P_\Lambda(H|V)} I_\Lambda(H:E),\qquad I_\Lambda(H:E)\le I(V:E)","role":"select coarse variables that retain block information relevant to the distant environment","symbols":{"H":"coarse variable","V":"visible block","E":"distant environment","Lambda":"coarse-graining parameters"},"evidence":"paper.pdf pp. 3–4, RSMI definition and Figures 1–2","interpretation":"Equality defines perfect capture; finite-capacity rules generally only approach the bound."}],
        ["paper.pdf pp. 1–4, Figures 1–2 and Eqs. (1)–(10): RSMI setup and perfect-capture theorem","paper.pdf pp. 5–7, Figures 3–5 and Eqs. (11)–(20): arbitrary clean Ising-chain RG rules","paper.pdf pp. 12–14, Figures 8–9 and Eqs. (27)–(31): disorder correlations and distribution complexity","source PDF SHA-256 a21ffcedace24222abcbc367f7aa8f6b63e5a6df06897fbad01033f57d37c091","Evidence status: full-text verified theory/solvable-model study; no independent reproduction performed."],
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed = []
    for item in CARDS:
        pid = str(item["arxiv_id"])
        (OUT / f"{pid}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        installed.append(pid)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
