#!/usr/bin/env python3
"""Install the first full-catalog v2.3 Collection backfill batch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *bullets: str) -> dict[str, object]:
    return {"title": title, "bullets": list(bullets)}


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


CARDS = [
    {
        "arxiv_id": "0712.3329",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/0712.3329",
        "title_en": "Universal Intelligence: A Definition of Machine Intelligence",
        "title_zh": "普适智能：机器智能的形式化定义",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("9c814e3ecbd108ed", "World Models"),
        "verified_metadata": {
            "arxiv_id": "0712.3329", "version": "v1",
            "title": "Universal Intelligence: A Definition of Machine Intelligence",
            "authors": ["Shane Legg", "Marcus Hutter"],
            "categories": ["cs.AI"], "primary_category": "cs.AI",
            "published": "2007-12-20T05:50:54Z",
            "abstract": "The paper extracts common features from informal definitions of intelligence and formalizes a machine-independent measure based on expected reward over computable environments, weighted by algorithmic probability. It connects the measure to AIXI and surveys competing machine-intelligence tests.",
        },
        "sections": [
            sec("作者信息", "作者：Shane Legg 与 Marcus Hutter；论文对应 arXiv:0712.3329v1，主分类 cs.AI。", "本卡核对完整 50 页论文；它是一篇定义与理论分析论文，不包含训练实验或现代大模型基准。"),
            sec("研究问题", "若机器的传感器、执行器和内部结构可以与人类完全不同，如何给出不依赖人类任务清单的智能定义？作者从专家对人类智能的描述中抽取三项负载条件：智能体需要在广泛环境中，通过交互学习并实现目标。", "目标不是构造一个立即可运行的 IQ 测试，而是给出能比较任意策略的理论标尺，并检查该标尺是否把随机、专用、学习型与理论最优智能体排成合理次序。"),
            sec("背景", "静态题库容易混入文化与物种偏置，也不能测量适应过程；Turing test 又把人类相似性与任务能力混在一起。论文因此采用强化学习式 agent–environment 回路，把动作、观察和奖励作为最小接口。", "与固定任务平均不同，环境集合取所有可计算、奖励可求和的概率环境；Occam 权重使简单环境贡献更大，从而把任务广度与描述复杂度放在同一求和式中。"),
            sec("模型与方法", "策略 \\(\\pi\\) 根据交互历史选择动作；环境 \\(\\mu\\) 返回观察与奖励，\\(V_\\mu^\\pi\\) 是策略在该环境中的期望总回报。奖励可求和条件保证每个环境贡献有限。", "环境复杂度由相对于参考 universal Turing machine 的 Kolmogorov complexity \\(K(\\mu)\\) 给出，算法概率 \\(2^{-K(\\mu)}\\) 实现对简单环境的指数偏好。", "作者逐一比较随机策略、短视学习器、专用棋类程序和更强的历史利用策略，再把上确界与 AIXI 联系起来；这一部分是定义的内部一致性检查，不是经验测量。"),
            sec("核心结果与证据", "核心定义为 \\(\\Upsilon(\\pi)=\\sum_{\\mu\\in E}2^{-K(\\mu)}V_\\mu^\\pi\\)（正文 p. 22）：智能是所有可计算环境上目标达成能力的算法概率加权平均。", "专用智能体可在一个复杂环境中取得高回报，却因其他环境上的 \\(V_\\mu^\\pi\\) 很低而得到较低总分；能利用更多规律和更长历史的策略在作者的简单构造中获得更高排序。", "AIXI 在该环境先验与贝叶斯混合下达到理论上界 \\(\\bar\\Upsilon=\\max_\\pi\\Upsilon(\\pi)\\)（pp. 26–27）。该结论依赖 AIXI 的理论最优性，同时也继承其不可计算性。", "论文还用表 1 比较多种机器智能定义的动态性、一般性、客观性和可实现性；该表包含作者判断，不能视为独立实验排名。"),
            sec("有效性与局限", "\\(K(\\mu)\\) 不可计算，因此纯定义不能直接成为有限测试；实际近似必须采样环境、限制程序长度并选择时间预算。", "Kolmogorov complexity 依赖参考 universal machine。虽然不同机器只造成加法常数，有限复杂度下智能体的相对排序仍可能改变，论文明确把自然参考机视为未解决问题。", "回报函数由环境给定，定义衡量的是目标达成能力而非目标的伦理价值、计算能耗或安全性；高 \\(\\Upsilon\\) 不自动等于可取的系统。", "AIXI 与全环境求和是理想化数学对象。正文没有给出现代神经网络上的估计误差、有限样本收敛或可执行 benchmark。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/0712.3329；PDF：https://arxiv.org/pdf/0712.3329。", "全文 PDF 共 50 页，SHA-256：03c6a3e6ed63e4aff3aa3c868d2efcb9cc6eb7b4a837a523df872d178f650593。", "可复现的最小实验是在有限 program-length 截断下枚举小环境，比较随机、有限记忆和规划策略；必须报告参考机、环境编码、奖励归一化、截断长度和计算预算。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 15–23 的交互框架和 \\(\\Upsilon\\) 定义，再读 pp. 24–30 的智能体排序与不可计算性。", "关注 pp. 27–30 对 reference-machine dependence 与 practical test 的讨论，它们决定该公式能否从定义变成测量。", "最后读 pp. 39–43 的批评回应；把“形式定义”“理论最优智能体”和“可实施评测”三个层次分开。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "作者把智能定义为策略在所有可计算、奖励可求和环境中的期望回报，并以环境的算法概率作为权重。这个普适标尺把任务广度、目标达成能力与 Occam 偏好写进同一求和式，其理论上界由 AIXI 达到；但 Kolmogorov complexity 与 AIXI 都不可计算，有限测试还依赖参考通用机、环境编码和计算预算。", "selection_rationale": "论文的核心贡献是形式定义而非可视化结果；原文示意图仅展示通用交互回路，因此题目与摘要更准确地传达关键内容。"},
        "figure_refs": [],
        "equation_refs": [{"label": "Universal intelligence", "latex": "\\Upsilon(\\pi)=\\sum_{\\mu\\in E}2^{-K(\\mu)}V_\\mu^\\pi", "role": "aggregate goal-directed performance over computable environments", "symbols": {"pi": "agent policy", "mu": "computable reward-summable environment", "E": "environment class", "K(mu)": "Kolmogorov complexity", "V_mu^pi": "expected total reward"}, "evidence": "paper.pdf p. 22, universal-intelligence definition", "interpretation": "Performance is broad rather than task-specific, while the algorithmic prior suppresses complex environments exponentially."}],
        "evidence_refs": ["paper.pdf pp. 15–23: agent–environment formalism and universal-intelligence definition", "paper.pdf pp. 24–30: agent ordering, AIXI upper bound, computability and reference-machine caveats", "paper.pdf pp. 39–43: proposed approximation and responses to criticisms", "source PDF SHA-256 03c6a3e6ed63e4aff3aa3c868d2efcb9cc6eb7b4a837a523df872d178f650593", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "0812.4360", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/0812.4360",
        "title_en": "Driven by Compression Progress: A Simple Principle Explains Essential Aspects of Subjective Beauty, Novelty, Surprise, Interestingness, Attention, Curiosity, Creativity, Art, Science, Music, Jokes",
        "title_zh": "由压缩进步驱动：从主观美到好奇心与创造力的统一原则",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("3526acd9c1713a6c", "Transformer Theory"),
        "verified_metadata": {"arxiv_id": "0812.4360", "version": "v2", "title": "Driven by Compression Progress: A Simple Principle Explains Essential Aspects of Subjective Beauty, Novelty, Surprise, Interestingness, Attention, Curiosity, Creativity, Art, Science, Music, Jokes", "authors": ["Juergen Schmidhuber"], "categories": ["cs.AI", "cs.NE"], "primary_category": "cs.AI", "published": "2008-12-23T10:14:18Z", "abstract": "A computationally limited observer receives intrinsic reward when its predictor or compressor improves on the accumulated history. The proposal identifies subjective beauty with compressibility and interestingness with compression progress, then relates this drive to curiosity, attention, discovery and creative behavior."},
        "sections": [
            sec("作者信息", "作者：Juergen Schmidhuber；论文为 arXiv:0812.4360v2，主分类 cs.AI，交叉 cs.NE。", "本卡核对完整 36 页版本。文章综合作者 1990–2008 年的压缩进步与人工好奇心工作，主要贡献是统一原则和算法框架。"),
            sec("研究问题", "纯预测误差会奖励不可预测噪声：一个智能体可能持续追逐随机电视雪花，却没有学到任何结构。论文问的是，何种内部奖励能够选择“当前仍可学习”的新规律，而不是已知模式或不可压缩噪声。", "作者把主观美定义为当前压缩器下的短描述，把有趣性定义为描述长度随学习下降的速率；因此有趣性是主观美随时间的导数，而不是数据本身的固定属性。"),
            sec("背景", "Shannon surprise 只衡量当前模型下的低概率事件，不能区分以后可形成规律的异常与本质随机事件。压缩进步则比较同一历史在模型更新前后的编码代价。", "这一观点属于计算学习与强化学习的理论建模，不是审美心理学的统计定律。文章将音乐、图像、笑话和科学发现作为解释性案例，并提出未来受控实验。"),
            sec("模型与方法", "控制器 \\(s(t)\\) 在历史 \\(h(\\le t)\\) 上选择动作；压缩器 \\(p(t)\\) 对同一历史给出代价 \\(C(p,h)\\)，代价可含编码长度与运行时间。", "独立的改进器寻找 \\(p(t+1)\\)，随后用旧、新压缩器在同一扩展历史上的差异产生 \\(r_{\\mathrm{int}}\\)。强化学习器最大化未来内部奖励，并可与外部奖励 \\(r_{\\mathrm{ext}}\\) 组合。", "异步设计把行动与模型改进分离：若改进器暂时没有找到更好压缩器，内部奖励为零；一旦发现规律，奖励回溯到产生相关数据的策略。"),
            sec("核心结果与证据", "文章的核心可计算量是 \\(I(D,O(t))\\sim\\partial_t B(D,O(t))\\)：数据 \\(D\\) 对观察者 \\(O\\) 的有趣性由其主观可压缩性改善速度决定（p. 7, Eq. 1）。", "更具体的算法奖励为 \\(r_{\\mathrm{int}}(t+1)=f[C(p(t),h),C(p(t+1),h)]\\)（p. 19, Eq. 5）；取 \\(f(a,b)=a-b\\) 时，只有真正减少编码代价的更新获得正奖励。", "该机制预测：完全熟悉的规则因无进一步压缩而无趣，白噪声因压缩器无法改善也无趣，处于学习曲线陡峭区的结构最有趣。", "论文回顾多个既有 curiosity implementations，但没有在统一基准上报告新实验、误差条或消融；关于艺术、科学和笑话的例子是机制解释，不是量化验证。"),
            sec("有效性与局限", "内部奖励依赖选定的压缩器类、搜索算法和计算预算；同一数据对不同观察者、甚至同一观察者的不同时刻会得到不同有趣性。", "压缩进步不保证社会价值或安全性。智能体可能主动制造容易学却有害的数据，因此作者保留外部奖励与约束通道。", "最优通用强化学习和 Kolmogorov 压缩器不可计算；实际系统只能使用有限模型和启发式改进器。", "人类审美、创造力与意识的主张跨度很大，文章只给出可检验方向，并未建立神经或行为实验上的因果证据。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/0812.4360；PDF：https://arxiv.org/pdf/0812.4360。", "全文 PDF 共 36 页，SHA-256：e971d466392c52f0a5212fcacc022c1cffab16fcf120ff25106bd71ed685557d。", "最小复现实验可设置三类流：重复周期、逐步显露的可学习规律和白噪声；固定压缩器更新预算，比较预测误差奖励与压缩进步奖励的访问分布。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 3–9 的定义链，特别区分 compressibility、compression progress 与 Shannon surprise。", "再读 pp. 17–21 的算法框架和 Eqs. (5)–(7)，确认内部奖励使用同一历史的前后模型比较。", "最后把艺术与意识章节当作假设生成材料；若关心可证伪性，优先阅读 p. 16 的 conclusion/outlook 与行为实验建议。"),
        ],
        "cover": {"mode": "title_abstract", "abstract_text": "论文提出一种计算型好奇心：智能体只有在更新后的预测器或压缩器能更短地描述同一段历史时，才获得内部奖励。熟悉模式已无压缩进步，白噪声也无法被进一步压缩；真正驱动探索的是仍处于学习曲线陡峭区的结构。该原则统一解释新奇、惊奇、注意和创造性探索，但其结果依赖压缩器类别与有限计算预算，文中的艺术和科学案例主要是机制阐释。", "selection_rationale": "论文的关键对象是时间变化的压缩代价而非某一幅审美图片；题目与摘要能避免把示例图误当成普适实验结果。"},
        "figure_refs": [],
        "equation_refs": [
            {"label": "Subjective interestingness", "latex": "I(D,O(t))\\sim\\frac{\\partial B(D,O(t))}{\\partial t}", "role": "define interestingness as the rate of compression improvement", "symbols": {"D": "observed data", "O(t)": "observer at time t", "B": "subjective beauty or compressibility", "I": "subjective interestingness"}, "evidence": "paper.pdf p. 7, Eq. (1)", "interpretation": "The same datum can cease to be interesting after the observer has learned its regularity."},
            {"label": "Compression-progress reward", "latex": "r_{\\mathrm{int}}(t+1)=f\\!\\left[C(p(t),h),C(p(t+1),h)\\right]", "role": "turn model improvement into intrinsic reinforcement", "symbols": {"r_int": "intrinsic reward", "C": "compression cost", "p(t)": "old compressor", "p(t+1)": "improved compressor", "h": "same accumulated history"}, "evidence": "paper.pdf p. 19, Eq. (5)", "interpretation": "Comparing two compressors on the same data prevents irreducible noise from being rewarded merely for high prediction error."}
        ],
        "evidence_refs": ["paper.pdf pp. 3–9: beauty, interestingness, surprise and curiosity definitions", "paper.pdf pp. 17–21: controller/compressor loop and intrinsic-reward equations", "paper.pdf pp. 12–16: prior implementations, examples and outlook", "source PDF SHA-256 e971d466392c52f0a5212fcacc022c1cffab16fcf120ff25106bd71ed685557d", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "0912.3000", "source_version": "v2", "source_pdf": "https://arxiv.org/pdf/0912.3000",
        "title_en": "The role of noise and advection in absorbing state phase transitions", "title_zh": "噪声与平流如何重塑吸收态相变",
        "curation_status": "full_text_verified", "card_standard_version": "2.3", "paper_profile": "theory_numerics", "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("63787595893799b0", "Statistical Physics"),
        "verified_metadata": {"arxiv_id": "0912.3000", "version": "v2", "title": "The role of noise and advection in absorbing state phase transitions", "authors": ["C. Barrett-Freeman", "M. R. Evans", "D. Marenduzzo", "J. Tailleur"], "categories": ["cond-mat.stat-mech"], "primary_category": "cond-mat.stat-mech", "published": "2009-12-15T21:05:51Z", "abstract": "The paper studies a one-dimensional reaction–diffusion field with advection and multiplicative noise. Arbitrarily weak advection changes the directed-percolation transition, while changing the noise amplitude from square-root to density-proportional turns a metastability line into a genuine phase boundary."},
        "sections": [
            sec("作者信息", "作者：C. Barrett-Freeman、M. R. Evans、D. Marenduzzo、J. Tailleur；机构位于 University of Edinburgh 与相关研究中心。", "本卡核对 arXiv:0912.3000v2 的 8 页全文，主分类 cond-mat.stat-mech。"),
            sec("研究问题", "Directed percolation 的吸收态临界性在加入定向输运后是否稳定？更具体地，平流是否只把密度轮廓平移，还是会改变低密度相的动力学稳定性和相变阶数？", "第二个问题是涨落模型的形式：人口统计型 \\(\\sqrt\\rho\\) 噪声与线性 \\(\\rho\\) 噪声都在 \\(\\rho=0\\) 消失，但它们是否产生相同相图？"),
            sec("背景", "无平流时，Reggeon-field-theory/Langevin 描述属于 DP 普适类；无噪声时，对流 Fisher–KPP 方程在边界驱动下可形成指数低密度轮廓。本文研究二者同时存在的开放一维系统。", "吸收态数值积分对低密度尤其敏感。作者分别使用 Dickman 离散算法和 Dornic 等人的分裂步算法，确保平方根噪声不会产生非物理负密度。"),
            sec("模型与方法", "主方程为 \\(\\partial_t\\rho=D\\partial_{xx}\\rho+v\\partial_x\\rho+a\\rho-b\\rho^2+\\Gamma_0 g(\\rho)\\eta\\)，在一维区间上施加入口/出口边界并扫描平流速度 \\(v\\) 与噪声强度 \\(\\Gamma_0\\)。", "作者比较 \\(g(\\rho)=\\sqrt\\rho\\) 与 \\(g(\\rho)=\\rho\\)。总质量 \\(M=\\int\\rho\\,dx\\) 被压缩为零维随机方程，通过 Itô 变量变换转成有效势中的加性噪声扩散。", "相界由系统尺度交叉、平均序参量、密度轮廓与到达吸收态的平均首达时间共同定位；零维模型用于解释 spinodal，而非替代空间模拟。"),
            sec("核心结果与证据", "任意非零平流都是相关扰动：随着 \\(v\\) 增加，高密度相到低密度相的转变变为不连续，因此不再属于 DP 普适类。", "平方根噪声下，指数轮廓最终仍会吸收；弱噪声时其寿命指数大、呈亚稳态。零维有效势预测 spinodal，取经验映射 \\(\\beta\\simeq2.3v\\) 后与一维首达时间轮廓吻合（Figs. 4–5）。", "线性噪声把结论定性改变：小噪声指数轮廓成为真正稳态，\\(\\Gamma_c=\\sqrt{2a}\\) 的可归一化条件把原 spinodal 变成相界。", "Figure 6 汇总 \\(a=0.5\\) 的相图：红方块分隔高/低密度相，三角形标出低密度区内线性噪声的第二相变；黑叉为平方根噪声边界。"),
            sec("有效性与局限", "结论来自一维连续场、特定边界和 logistic 反应项；更高维、可压缩流、空间无序或不同反应网络可能改变相图。", "零维 \\(\\beta\\simeq2.3v\\) 是与一维数据匹配得到的经验关系，不能当作严格 coarse-graining。", "线性与平方根噪声对应不同微观涨落机制；不能只因二者在吸收态消失就互换。论文的核心警告正是噪声振幅的密度依赖会改变相变类别。", "模拟给出有限尺寸证据；线性噪声大噪声边界附近，作者也指出需要更多数据区分连续转变与 \\(v=0\\) 极限。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/0912.3000；PDF：https://arxiv.org/pdf/0912.3000。", "全文 PDF 共 8 页，SHA-256：3cd848105a172918172440549538be9dc60665de3c87075012f509895b015856。", "复现需分别实现两种噪声的 positivity-preserving 积分，扫描 \\(L,v,\\Gamma_0\\)，保存首达时间分布而非只看有限时快照。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 1–2 的方程与两种噪声，再看 Figs. 1–3 确认平流诱导的不连续转变。", "pp. 3–5 的零维有效势是机制核心；逐项检查 Itô 变换和稳态分布是否可归一化。", "Figure 6 最适合把两种噪声的拓扑差异放在一起看；最后读 pp. 5–6 的结论与河流种群应用边界。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/0912.3000/figure-6-phase-diagram.webp", "label": "Figure 6", "visual_type": "phase_diagram", "evidence": "arXiv:0912.3000v2, paper.pdf p. 5, Figure 6", "alt_text": "平流速度 v 与噪声强度 Gamma_0 平面中的高密度、指数低密度和吸收相区域。", "caption": "噪声从平方根形式改为线性形式后，低密度区出现真实相界，展示噪声建模对吸收态相图的定性影响。", "selection_rationale": "Figure 6 是论文最集中的物理可视化，直接比较两种噪声的相界拓扑；它比单条序参量曲线更能替代冗长文字。"},
        "figure_refs": [{"label": "Figure 6", "asset_path": "assets/collection-figures/0912.3000/figure-6-phase-diagram.webp", "section": "核心结果与证据", "role": "compare phase topology for density-linear and square-root noise", "evidence": "arXiv:0912.3000v2, paper.pdf p. 5, Figure 6", "alt_text": "v–Gamma_0 相图，标出高密度、指数低密度与吸收区。", "caption": "红方块、棕三角和黑叉分别表示不同相界或噪声模型。", "interpretation": "噪声振幅的密度依赖不只是数值细节；它决定指数轮廓是亚稳态还是真正稳态，并改变相界数目。"}],
        "equation_refs": [
            {"label": "Advected stochastic Fisher–KPP field", "latex": "\\partial_t\\rho=D\\partial_{xx}\\rho+v\\partial_x\\rho+a\\rho-b\\rho^2+\\Gamma_0 g(\\rho)\\eta", "role": "governing stochastic reaction–diffusion–advection equation", "symbols": {"rho": "population density", "D": "diffusivity", "v": "advection speed", "a,b": "growth and saturation coefficients", "Gamma_0": "noise strength", "g(rho)": "density-dependent noise amplitude", "eta": "white noise"}, "evidence": "paper.pdf p. 2, Eq. (2)", "interpretation": "Changing only g(rho) from square-root to linear noise changes the low-density phase from metastable to stationary."},
            {"label": "Square-root-noise effective potential", "latex": "V_{\\mathrm{eff}}(u)=-\\frac{a u^2}{4}+\\frac{\\beta\\Gamma^2u^4}{32}+\\frac{\\log u}{2}", "role": "diagnose metastability of the total mass", "symbols": {"u": "2 sqrt(M)/Gamma", "M": "total mass", "a": "linear growth", "beta": "effective nonlinear coefficient", "Gamma": "noise strength"}, "evidence": "paper.pdf p. 4, Eq. (5)", "interpretation": "The logarithmic singularity keeps the absorbing state as the only normalizable stationary measure even when a long-lived finite-mass minimum exists."}
        ],
        "evidence_refs": ["paper.pdf pp. 1–3: stochastic field equation, numerical schemes and advection-driven discontinuity", "paper.pdf pp. 3–5: zero-dimensional effective potentials, first-passage analysis and Figures 4–6", "paper.pdf pp. 5–6: linear-noise phase boundary, conclusion and application scope", "source PDF SHA-256 3cd848105a172918172440549538be9dc60665de3c87075012f509895b015856", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"installed": [card["arxiv_id"] for card in CARDS]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
