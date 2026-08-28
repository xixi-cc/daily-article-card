#!/usr/bin/env python3
"""Install full-text v2.3 Collection cards for backfill batch 044."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


CARDS = [
    card(
        "doi-10.1140-epje-s10189-023-00364-w", "arXiv v1 manuscript", "https://arxiv.org/pdf/2306.10791",
        "Active Ising Models of Flocking: A Field-Theoretic Approach",
        "簇拥主动伊辛模型：一种场论方法", "theory", "6cd1881cb7f6a7d0", "Active Matter",
        {"doi":"10.1140/epje/s10189-023-00364-w","arxiv_id":"2306.10791","version":"arXiv v1 full text","title":"Active Ising Models of flocking: a field-theoretic approach","authors":["Mattia Scandolo","Johannes Pausch","Michael E. Cates"],"journal":"The European Physical Journal E","volume":"46","issue":"10","article":"103","published":"2023-10","abstract":"Doi–Peliti field theories connect microscopic reaction rules to fluctuating hydrodynamics for several Active Ising Models, exposing when flocking and Model-C-like criticality do or do not arise.","comment":"ArXiv v1 full text cross-checked with the version-of-record metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Mattia Scandolo、Johannes Pausch、Michael E. Cates；The European Physical Journal E 46, 103 (2023)，DOI:10.1140/epje/s10189-023-00364-w。核验 arXiv:2306.10791v1 全文24页与期刊元数据；未发现关联更正或撤稿。"),
            sec("研究问题", "Active Ising Model（AIM）把自推进方向限制在一条轴上，以离散自旋对称性破缺描述flocking。论文问：不同微观翻转/碰撞规则怎样系统映射为可含噪声的场论与流体方程；二体局域对齐是否足以产生宏观有序；零自推进临界点是否必然落入平衡Model C普适类？"),
            sec("背景", "作者将向右/向左粒子视为两种反应扩散物种，随机翻转、二体对齐和三体多数规则分别由局域反应表示。Doi–Peliti coherent-state path integral给出精确bare action，再经Cole–Hopf变换转为密度ρ、磁化m及response fields。", "该映射保持所选微观Markov过程的信息，但随后的hydrodynamic和RG讨论仍需要长波、低梯度及相关尺度假设；它不是对所有含伊辛对称性的active matter模型的统一证明。"),
            sec("模型与方法", "对AIM0、AIM1与AIM2，作者从Master equation推导deterministic hydrodynamics及leading multiplicative noise，并对均匀有序/无序解做小波数线性稳定性分析。有限self-propulsion v将连续Ising式转变改为密度共存区：临界密度附近有序与无序均匀态都可失稳。", "在零推进极限，作者从mesoscopic action筛选d<4的relevant operators，并与Model C的order parameter m和conserved density δρ方程逐项比较；关键差异是本文AIM的ρ动力学独立于spin state，从而禁止Model C中允许的∇m²反馈项。"),
            sec("核心结果与证据", "AIM2中临界密度由随机翻转率γ与三体率τ给出ρc=(8γ/τ)^{1/2}，而不含二体率λ。令τ=0后，m=0均匀态对任意γ>0和任意λ都稳定，因此纯二体碰撞对齐在所取hydrodynamic limit中不能产生flocking。", "当γ=0且系统有限时，二体模型可由噪声缓慢到达全磁化吸收态；但该机制随L增大而消失，所以不能混同于确定性宏观有序。论文将有限尺寸stochastic absorption与thermodynamic-limit flocking明确分开。", "v≠0时ρc<ρ0<ρl存在长波不稳定区，支持一阶液气式flocking transition；v→0时该区收缩。零推进场论虽表面接近Model C，但缺少density current中的m²耦合，作者据此主张这些特定AIM不应自动归入Model C；完整RG结论留给后续工作。"),
            sec("有效性与局限", "主要结果来自解析映射、尺度分析和线性稳定性，没有对大规模simulation或experiment作新比较；线性不稳定本身不决定最终band morphology、coexistence densities或critical exponents。二体不flock结论针对本文反应规则及hydrodynamic limit，其他非局域、持续取向或速度耦合可改变答案。", "关于零推进普适类，本文建立了action和对称性边界，但没有在本篇完成全RG fixed-point计算。摘要中‘lie outside Model C’应读作由缺失operator和非平衡对称性支持的场论论证，而非数值测得的新临界指数。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2306.10791；期刊：https://doi.org/10.1140/epje/s10189-023-00364-w。核验PDF SHA-256：264d829a748963f31d4d0696e1fcd17a36d04b794c702708041adb526e5996d5。本文为解析研究，未给专用代码仓库。", "复现应固定reaction list、hopping convention、Cole–Hopf fields、system-size scaling、noise covariance、v与D定义，并从bare action逐式检查hydrodynamic truncation和stability eigenvalues。Evidence status: full-text verified analytical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–3 的模型族与Doi–Peliti路线；pp.4–9核对各反应action、流体方程和noise。pp.10–11是二体碰撞为何不flock的核心，pp.11–14比较零推进AIM与Model C；附录给coherent-state、变换和尺度细节。"),
        ],
        "title-abstract-active-ising.webp", "Title and abstract", 1, "schematic",
        "论文标题、作者与摘要，摘要列出Doi–Peliti方法、二体对齐例外和零推进Model C问题。",
        "该文没有数据型主图；标题页摘要如实概括三条场论结论并作为全文入口。",
        "原稿不含编号科学图，采用标题与摘要回退，避免把自制示意图伪装成来源图。",
        [{"label":"AIM2 hydrodynamics","latex":r"\partial_t m=D\nabla^2m-v\partial_x\rho-\mathcal F(m,\rho)+\text{noise},\qquad \partial_t\rho=D\nabla^2\rho-v\partial_xm+\text{conserved noise}","role":"connect microscopic spin reactions to magnetization and density fields","symbols":{"m":"magnetization density","rho":"particle density","v":"self-propulsion speed","F":"reaction-induced drift"},"evidence":"paper.pdf pp. 7–9, hydrodynamic equations and stability analysis","interpretation":"The form is model-specific and the displayed noise is shorthand for the derived multiplicative covariances."}],
        ["paper.pdf pp. 3–9: Doi–Peliti actions and hydrodynamic equations","paper.pdf pp. 9–11: homogeneous stability and two-body-collision result","paper.pdf pp. 11–14: zero-propulsion action and comparison with Model C","paper.pdf pp. 15–24: coherent-state, transformation and scaling appendices","source PDF SHA-256 264d829a748963f31d4d0696e1fcd17a36d04b794c702708041adb526e5996d5","Evidence status: full-text verified analytical study; no independent reproduction performed."],
    ),
    card(
        "doi-10.1140-epje-s10189-024-00466-z", "version of record", "https://link.springer.com/content/pdf/10.1140/epje/s10189-024-00466-z.pdf",
        "Metareview: A Survey of Active Matter Reviews", "元综述：主动材料综述文献全景调查",
        "theory", "d6eed589f725c1d2", "Active Matter",
        {"doi":"10.1140/epje/s10189-024-00466-z","version":"version of record","title":"Metareview: a survey of active matter reviews","authors":["Michael te Vrugt","Raphael Wittkowski"],"journal":"The European Physical Journal E","volume":"48","article":"12","published":"2025-03-04","abstract":"A metareview organizes more than one thousand reviews, books, perspectives and roadmaps across active-matter theory, experiments, biological systems, artificial swimmers and applications.","comment":"Open-access version of record; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Michael te Vrugt、Raphael Wittkowski；The European Physical Journal E 48, 12 (2025)，DOI:10.1140/epje/s10189-024-00466-z。核验开放期刊版38页（文献表占较大部分）与Crossref元数据；未发现关联更正或撤稿。"),
            sec("研究问题", "active matter已从自驱粒子统计力学扩展到微机器人、组织、智能材料和医学应用，相关综述超过千篇，单篇普通review难以覆盖。本文问：能否以‘review of reviews’形式建立主题导航，让新读者定位入门文献，并用已有综述的密度识别成熟领域、热点与潜在空白？"),
            sec("背景", "作者广义定义active-matter review：总结该领域而不呈现原创研究的科学出版物，包括传统综述、书籍/章节、perspective、roadmap、通俗介绍和部分editorial。每条文献通常只放入一个最合适章节，避免重复计数。", "这种定义适合导航而非系统综述的穷尽性统计：‘是否属于active matter’边界不清，跨主题文献的单标签会压缩交叉关系，最近出版物还可能未被收录。"),
            sec("模型与方法", "正文按books、general reviews、active colloids、特殊粒子、active materials、集体动力学、生物active matter、微泳者/微机器人、环境与医学应用、理论与计算方法等主题组织；每节简述概念，再指向对应综述群。", "Figure 1按年份给review数量，Figure 2把章节映射为面积与文献数量成比例的气泡。作者明确不显示active colloids盘，因为该词跨多个主题出现，也未完整survey molecular active matter；这些是可视统计的scope exclusions。"),
            sec("核心结果与证据", "Figure 2显示人工active particles、biological active matter与medical applications拥有最大的综述群，collective dynamics、active materials和理论/计算方法也形成大类。气泡面积反映作者收集并单次归类的review数量，不是论文产量、研究质量或重要性的直接指标。", "正文用主题化参考链覆盖从motile droplets、phoresis、active polymers和liquid crystals，到bacteria、cells/tissues、robotic swarms、drug delivery、environmental remediation，以及Brownian dynamics、continuum theory和machine learning。其主要产物是检索入口，而非对各子领域结论做统一meta-analysis。", "作者认为大量books与general reviews说明领域已成熟，同时专题综述快速增长说明分化加剧。‘未充分review’可能提示空白，但也可能来自术语差异、搜索遗漏或主题太新，不能仅由气泡大小判定研究优先级。"),
            sec("有效性与局限", "文章未提供PRISMA式检索式、数据库覆盖、时间截止、筛选者一致性或完整机器可读清单，因此无法将其当作可重复的系统综述。Google Scholar citation counts仅用于说明少数经典综述的影响，也会随时间变化。", "文献按章节单归类会低估跨学科重叠；非英语文献、书籍章节和新近在线出版更易漏收。文章不评价各review的方法质量，也不综合原始实验effect size；它更接近专家策展地图。"),
            sec("复现与资源", "期刊全文：https://doi.org/10.1140/epje/s10189-024-00466-z。核验PDF SHA-256：34c24f3468bbbd8363755193c94a7df70e4624f594d6ddb2ef15b5a36901ffd9。正文参考文献超过千条，但未声明独立代码或结构化数据仓库。", "若复现Figure 1–2，应固定数据库、检索日期、review定义、去重规则、章节taxonomy与跨主题tie-break，并公开DOI清单和排除理由。Evidence status: full-text verified metareview; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.1–3 的定义、scope和Figures 1–2；随后按问题跳到相应章节，不必线性通读。使用气泡图时同时读caption中的省略项；真正做systematic review时，应再回到原始论文并建立可复现检索策略。"),
        ],
        "figure-2-review-landscape.webp", "Figure 2", 3, "distribution",
        "主动材料各主题综述数量的气泡图，面积与作者归类的综述数量成比例。",
        "人工主动粒子、生物主动材料和医学应用在该策展文献集中形成最大的综述类别。",
        "Figure 2是全文主题taxonomy与相对文献密度的紧凑索引，并在caption中公开未完全覆盖项。",
        [],
        ["paper.pdf pp. 1–3, Figures 1–2: definitions, annual counts and topic map","paper.pdf pp. 3–20: physical, biological and theoretical subfield navigation","paper.pdf pp. 20–22: applications and concluding scope","paper.pdf pp. 22–38: curated review bibliography","source PDF SHA-256 34c24f3468bbbd8363755193c94a7df70e4624f594d6ddb2ef15b5a36901ffd9","Evidence status: full-text verified metareview; no independent reproduction performed."],
    ),
    card(
        "doi-10.2139-ssrn.4584928", "local SSRN manuscript build dated 2024-06-15", "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4584928",
        "Large Language Models and Financial Market Sentiment", "大语言模型与金融市场情绪",
        "ai_empirical", "82e35b0590248725", "Machine Learning",
        {"doi":"10.2139/ssrn.4584928","version":"page-addressable local SSRN manuscript build dated 2024-06-15; current SSRN metadata cross-check","title":"Large Language Models and Financial Market Sentiment","authors":["Shaun Alexander Bond","Hayden Klok","Min Zhu"],"journal":"SSRN Electronic Journal","published":"2023","abstract":"ChatGPT-derived sentiment from Reuters end-of-day market summaries is compared with dictionary and transformer classifiers for forecasting short-horizon S&P 500 returns and portfolio utility.","comment":"Evidence pages use a preserved 57-page manuscript built 2024-06-15; SSRN currently reports a later revision, so this card does not claim page identity with the latest file"},
        [
            sec("作者信息", "作者 Shaun Alexander Bond、Hayden Klok、Min Zhu；SSRN working paper，DOI:10.2139/ssrn.4584928，初次上线2023。本卡证据来自本地保留的57页PDF（文件构建日期2024-06-15）；当前SSRN页面标记后续修订，因此页码和结果只归属于该保存版本，不声称与最新文件逐字一致。"),
            sec("研究问题", "传统金融情绪词典难理解否定、语境和市场角色，专用transformer又受固定分类任务限制。论文问：用ChatGPT给Reuters每日美股收盘综述打正/中/负分，能否预测S&P 500次日回报反转，并在out-of-sample R²和投资者certainty-equivalent return（CER）上优于词典或较小transformer？"),
            sec("背景", "样本为2000-01-01至2020-07-31的Reuters end-of-day U.S. market summaries，共5,142个交易日、约136万词。作者将每日文本分别送入gpt-3.5-turbo-0301，temperature=0，提示其以financial advisor身份输出1–100的positivity、neutrality和negativity分数。", "比较器包括Loughran–McDonald、VADER、FinBERT和TwitterRoBERTa；后两者能建模上下文但参数远小于gpt-3.5。模型版本、API后端和Reuters抓取语料均会随时间失效，是复现边界。"),
            sec("模型与方法", "作者用滞后情绪预测下一日、周或月market excess return，控制历史return并报告Newey–West型推断；时间变化用expanding和rolling windows。out-of-sample阶段以historical-mean forecast为基准，计算Campbell–Thompson R²，并把预测映射为S&P 500与risk-free asset间的受约束配置，报告CER gain。", "另按economic uncertainty、policy uncertainty、recession和business conditions分组，并让ChatGPT/BARD回忆历史市场文本形成第二套text universe。该recall实验尤其可能包含训练数据记忆或时间泄漏，不能当作实时可交易信号的干净测试。"),
            sec("核心结果与证据", "日频in-sample结果显示多种负面情绪与次日回报负相关，作者解释为短期overreaction后反转；关系在高不确定性和较差市场条件下更强。相关与predictive regression不证明新闻情绪导致回报，亦可能反映共同冲击、文本选择和多重检验。", "Table 7的保存版本报告情绪模型相对historical mean具有正的out-of-sample表现；Figure 4给2006–2020滚动CER gain，TwitterRoBERTa和FinBERT曲线总体最高，ChatGPT紧随，且情绪组合大多高于控制组合。摘要所称ChatGPT略优须按具体metric理解，不能概括为所有基线和所有时段均第一。", "Figure 4还显示2008等阶段CER gain剧烈波动，VA有时接近或跌破控制表现；终点汇总会隐藏路径风险。交易策略计算未完整纳入现实成交成本、模型API成本、可得时滞和实时revision，因此positive CER不是可直接执行的收益承诺。"),
            sec("有效性与局限", "Reuters语料是单一英文市场综述源，sample止于2020，模型和市场制度均已变化。temperature=0仍非严格确定；历史文本可能进入LLM训练集，尤其‘回忆历史新闻’不具真正out-of-sample信息边界。", "大量classifier、正负分数、频率、窗口和状态切分带来multiple-testing风险；金融return预测signal很弱且regime-dependent。工作论文有后续修订，而本卡保存版本不是最新；数字引用须连同版本日期。"),
            sec("复现与资源", "SSRN页面：https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4584928；DOI：https://doi.org/10.2139/ssrn.4584928。保存PDF SHA-256：82e35b059024872524dff7b39128fd01e9ca51667f2c80441f7d4e192fafb2a5。未在保存稿中找到公开完整语料/代码仓库。", "复现需保存Reuters原文与抓取时间、API model snapshot、完整prompt/response、解析失败、classifier commits、return source、forecast split、portfolio constraints与交易成本；同时应做严格publication-time leakage audit。Evidence status: page-addressable preserved working-paper version verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.5–8 的5,142日数据、prompt和比较器；pp.17–23看in-sample与rolling coefficients，pp.24–28看out-of-sample、Table 7和Figure 4。最后读pp.29–35讨论及pp.36–57附录，并始终保留2024保存稿与当前SSRN修订的版本边界。"),
        ],
        "figure-4-cer-gain.webp", "Figure 4", 26, "data_plot",
        "2006–2020各情绪预测组合相对历史均值组合的滚动CER gain曲线。",
        "情绪组合在保存样本的大多数时期提高CER，但金融危机附近波动明显且不同分类器排序会变化。",
        "Figure 4展示路径而非只给终点统计，能同时呈现作者的经济价值主张与时变风险。",
        [{"label":"Predictive return regression","latex":r"r_{t+1}=\alpha+\beta s_t+\gamma r_t+\varepsilon_{t+1}","role":"test whether current text sentiment forecasts next-period market returns","symbols":{"r":"S&P 500 return","s":"classifier sentiment score","beta":"sentiment predictive coefficient"},"evidence":"preserved manuscript pp. 14–18, Eq. (1) and Tables 3–4","interpretation":"A predictive coefficient is associational and is sensitive to timing, controls and multiple testing."}],
        ["preserved manuscript pp. 5–8: Reuters corpus, prompt and classifiers","preserved manuscript pp. 17–23, Tables 3–6 and Figure 3: in-sample and temporal coefficients","preserved manuscript pp. 24–28, Table 7 and Figure 4: out-of-sample and CER results","preserved manuscript pp. 29–35: market-state tests and discussion","source PDF SHA-256 82e35b059024872524dff7b39128fd01e9ca51667f2c80441f7d4e192fafb2a5","Evidence status: page-addressable preserved working-paper version verified; no independent reproduction performed."],
    ),
    card(
        "doi-10.3389-fphy.2020.00200", "version of record", "https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2020.00200/pdf",
        "Automated Discovery of Local Rules for Desired Collective-Level Behavior Through Reinforcement Learning",
        "通过强化学习自动发现产生目标集体行为的局域规则", "ai_empirical", "92b6eba53ee7220b", "Control & Reinforcement Learning",
        {"doi":"10.3389/fphy.2020.00200","version":"version of record","title":"Automated Discovery of Local Rules for Desired Collective-Level Behavior Through Reinforcement Learning","authors":["Tiago Costa","Andres Laan","Francisco J. H. Heras","Gonzalo G. de Polavieja"],"journal":"Frontiers in Physics","volume":"8","article":"200","published":"2020-06-25","abstract":"Evolution strategies optimize modular neural local policies that make simulated self-propelled agents form rotating balls, tornadoes and full- or hollow-core mills.","comment":"Open-access version of record; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Tiago Costa、Andres Laan、Francisco J. H. Heras、Gonzalo G. de Polavieja；Frontiers in Physics 8, 200 (2020)，DOI:10.3389/fphy.2020.00200。核验13页开放期刊版、补充材料/视频声明和代码链接；未发现关联更正或撤稿。"),
            sec("研究问题", "经典collective-motion建模通常先手写alignment、attraction和repulsion规则，再反复调参观察群体形态。论文问：能否反过来指定目标宏观构型，以reinforcement-learning式reward和evolution strategies自动搜索个体局域policy，并让网络结构本身保持可解释？"),
            sec("背景", "模拟鱼在三维空间以速度、azimuth和elevation演化；每个agent只用自身速度及邻居相对位置/速度。目标包括rotating ball、tornado、full-core mill与hollow-core mill，global reward组合防碰撞、凝聚、旋转和最低速度等项。", "虽然标题称reinforcement learning，优化实际采用derivative-free evolution strategies：所有agents共享同一policy参数，通过成对随机扰动的多次simulation估计reward gradient。没有真实动物在线学习。"),
            sec("模型与方法", "policy由pair-interaction module和aggregation/attention module组成：前者逐邻居输出三种动作分布的均值/方差，后者给正权重，再归一加权成最终turning与speed commands。低维输入输出可绘制为attraction–repulsion、alignment、elevation、speed和neighbor weighting maps。", "Evolution strategies每轮采样K个正态参数扰动及其反向扰动，运行2K次群体模拟，并以扰动乘reward近似∇R更新共享网络。另以ray-tracing artificial retina替代显式邻居变量，测试更感知化但更难解释的输入。"),
            sec("核心结果与证据", "Figure 3的四个示例run中，reward在数千epochs内上升并趋于平台；100 epochs的散乱群体到8,000 epochs分别形成球、tornado与两种mill。补充independent quality indices支持形态收敛，并在agent数翻倍时仍观察到目标结构。", "Figure 5–6把学得policy可视化：rotating ball呈近邻repulsion、中距离alignment/attraction并偏重近邻；tornado沿z方向排斥更强，full-core mill前方repulsion更广，hollow-core mill的alignment与speed-up区域更大。可解释性来自模块化低维映射，不等于网络内部每个参数有生物意义。", "artificial-retina输入也能生成四种定性相似构型，但平均agent间距更大、结构较松散。作者没有将learned rules与真实鱼群轨迹做定量拟合；结果证明simulation中reward-to-pattern搜索可行，而非发现了真实生物法则。"),
            sec("有效性与局限", "目标由engineered global reward定义，搜索可能利用reward漏洞；四种构型和特定agent dynamics限制外推。Figure 3是example runs，理论上neural multi-agent ES没有收敛保证；补充多run robustness仍不等同全面hyperparameter和seed审计。", "显式输入让policy易画图，却假设精确获得所有邻居位置/速度；retina版本更现实但失去模块解释且更松散。无真实传感噪声、碰撞物理、能耗、个体异质性或sim-to-real验证。"),
            sec("复现与资源", "期刊：https://doi.org/10.3389/fphy.2020.00200；代码：https://gitlab.com/polavieja_lab/rl_collective_behaviour；补充材料与12段视频由期刊页面提供。核验PDF SHA-256：df26c5817bb8ff944ff4b27026b99428f467d1a62ad068d71e8d4537af1a21d7。", "复现需固定environment Table 1、agent count、reward terms、2K扰动数、σ与annealing、learning rate、network sizes、episode length、seed及质量指标。Evidence status: full-text verified simulation/learning study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.2–3 Figure 1和环境方程；pp.4–6 Figure 2及ES公式说明policy与优化。p.7 Figure 3看训练现象，pp.8–10 Figures 5–6看局域规则解释；p.11 Discussion核对无收敛保证、simulation和真实行为之间的边界。"),
        ],
        "figure-3-training-convergence.webp", "Figure 3", 7, "simulation_snapshot",
        "四种目标群体构型的reward训练曲线，以及100与8,000 epochs时的三维agent快照。",
        "共享局域policy经evolution strategies优化后，四类reward均趋稳并产生目标宏观形态。",
        "Figure 3同时展示优化轨迹和生成构型，是从global reward到collective pattern的直接模拟证据。",
        [{"label":"Evolution-strategy update","latex":r"\boldsymbol\omega\leftarrow\boldsymbol\omega+\lambda\frac{1}{2\sigma^2K}\sum_{i=1}^{2K}\boldsymbol\epsilon_iR_i","role":"estimate a shared-policy reward gradient from antithetic parameter perturbations","symbols":{"omega":"policy-network parameters","epsilon":"Gaussian perturbation","R":"episode reward","K":"number of perturbation pairs"},"evidence":"paper.pdf p. 6, Eq. (10)","interpretation":"This is a simulation-based gradient estimator and carries no general convergence guarantee for the neural multi-agent setting."}],
        ["paper.pdf pp. 2–3, Figure 1 and Table 1: agent dynamics and framework","paper.pdf pp. 4–6, Figure 2 and Eqs. (7)–(10): modular policy and ES","paper.pdf p. 7, Figure 3: reward curves and collective configurations","paper.pdf pp. 8–11, Figures 5–6: learned-rule interpretation and discussion","source PDF SHA-256 df26c5817bb8ff944ff4b27026b99428f467d1a62ad068d71e8d4537af1a21d7","Evidence status: full-text verified simulation/learning study; no independent reproduction performed."],
    ),
    card(
        "doi-10.52202-079017-1161", "arXiv v1 manuscript", "https://arxiv.org/pdf/2410.14240",
        "Almost-Linear RNNs Yield Highly Interpretable Symbolic Codes in Dynamical Systems Reconstruction",
        "近线性RNN在动力系统重建中产生高度可解释的符号编码", "theory_numerics", "7790bdcb2c163210", "Mechanistic Interpretability",
        {"doi":"10.52202/079017-1161","arxiv_id":"2410.14240","version":"arXiv v1 full text","title":"Almost-Linear RNNs Yield Highly Interpretable Symbolic Codes in Dynamical Systems Reconstruction","authors":["Manuel Brenner","Christoph Jürgen Hemmer","Zahra Monfared","Daniel Durstewitz"],"journal":"Advances in Neural Information Processing Systems","volume":"37","pages":"36829–36868","published":"2024","abstract":"Almost-linear RNNs restrict ReLU nonlinearities to a small subset of units, yielding parsimonious piecewise-linear regions and symbolic graphs for reconstructed chaotic and empirical dynamics.","comment":"ArXiv v1 full text cross-checked with NeurIPS proceedings metadata; no Crossref correction or retraction relation found"},
        [
            sec("作者信息", "作者 Manuel Brenner、Christoph Jürgen Hemmer、Zahra Monfared、Daniel Durstewitz；NeurIPS 2024 / Advances in Neural Information Processing Systems 37, 36829–36868，DOI:10.52202/079017-1161。核验 arXiv:2410.14240v1 全文40页含appendix和checklist。"),
            sec("研究问题", "RNN能从时间序列重建复杂动力学，但普通piecewise-linear RNN含M个ReLU时理论上有2^M个线性子区，数学分析仍困难。论文问：若只给P≪M个units非线性，其余保持线性，是否能在保留重建质量的同时自动得到最少子区、可转为symbolic dynamics图的模型？"),
            sec("背景", "标准PLRNN写成zt=Azt−1+W ReLU(zt−1)+h；每个ReLU激活pattern确定一个linear map。AL-RNN将前M−P个coordinates直接线性传递，只对最后P个用ReLU，因此潜在子区从2^M降到2^P，同时仍以额外linear units展开latent space。", "symbolic code把每个时刻所在子区标为离散symbol，边表示观测到的区域转移。可解释性是在拟合模型的latent partition内建立；latent region与真实物理state之间仍需验证。"),
            sec("模型与方法", "作者给hyperbolic、non-globally-diverging AL-RNN下fixed points与periodic orbits和符号序列之间对应的theorems。训练采用现有DS reconstruction算法；模型选择通过逐渐增加P观察geometry disagreement Dstsp与temporal Hellinger distance DH何时平台，或对nonlinear units施加regularization。", "实验包括Lorenz-63、Rössler两个已知chaotic systems，delay-embedded human ECG，以及20-region human fMRI cognitive-task time series；跨多次训练比较geometry、fixed-point位置、Jacobian eigenvalues与symbolic graphs。"),
            sec("核心结果与证据", "Figure 3显示Rössler在P=1、Lorenz-63在P=2附近出现显著性能跃升；Figure 5中对应2和3个实际子区的AL-RNN恢复已知topologically minimal PWL结构。Rössler的unstable spiral与回注区域、Lorenz的双lobe spiral和中央saddle在图结构中可读。", "Figure 5对20次训练分别报告子区内Dstsp、fixed-point位置和最大Jacobian eigenvalue差异，均接近零，支持已知chaotic benchmarks上的robust minimal representation。增加到P=10可更好逼近geometry，但牺牲极简拓扑，说明‘topological minimum’与‘geometric fidelity’不是同一目标。", "ECG用P=2形成3个子区并把Q-wave transition联系到一个latent unit；fMRI局部重建的四子区与task stages相关，平均分类accuracy 0.78±0.05，但生成时每7 steps重置到observation。该重置和categorical decoder使fMRI结果不能解读为自由长期生成的完整机制发现。"),
            sec("有效性与局限", "theorems要求模型在各子区hyperbolic且不global divergence，并描述AL-RNN自身而非证明它与未知真实系统topologically conjugate。是否已从有限含噪经验数据找到真正最小P没有一般判据，作者也将其列为开放问题。", "synthetic systems真值清楚但维度低；ECG/fMRI样本和preprocessing特定。region labels受latent basis和训练影响，生理解释主要是事后对应；few regions能否推广到其他实验动力系统仍未知。"),
            sec("复现与资源", "全文：https://arxiv.org/abs/2410.14240；论文代码：https://github.com/DurstewitzLab/ALRNN-DSR。核验PDF SHA-256：e6ae0c637d75d3ee0de3628aece784924fb97683c89e500f830bfbbcc75b9934。", "复现需固定code commit、teacher forcing、latent M、nonlinear P或regularization、observation preprocessing、train length、free-generation horizon、reset interval、metrics和20-run seeds。Evidence status: full-text verified theory/numerical study; no independent reproduction performed."),
            sec("阅读指南", "先读 pp.3–5 Eqs. (1)–(5)、Figures 1–2理解AL-RNN与symbolic coding；pp.5–6看theorems及假设。pp.7–9 Figures 3–7是chaotic/ECG主证据，p.10看fMRI与限制；pp.20–30附录给对照、数据和robustness。"),
        ],
        "figure-5-minimal-chaos.webp", "Figure 5", 8, "phase_diagram",
        "Rössler与Lorenz-63的最少AL-RNN线性子区、固定点、符号图和20次训练稳健性指标。",
        "AL-RNN从数据自动恢复已知chaotic attractor的极简分段线性拓扑，并在重复训练间保持接近一致。",
        "Figure 5将区域几何、动力机制、symbolic graph和重复训练误差连在一起，是可解释性主张的核心证据。",
        [{"label":"Almost-linear recurrent map","latex":r"z_t=Az_{t-1}+W\Phi^*(z_{t-1})+h,\qquad \Phi^*(z)=(z_1,\ldots,z_{M-P},[z_{M-P+1}]_+,\ldots,[z_M]_+)","role":"limit nonlinear switching to P of M latent units","symbols":{"M":"latent dimension","P":"number of ReLU units","Phi_star":"mixed linear/ReLU activation"},"evidence":"paper.pdf pp. 3–4, Eqs. (4)–(5)","interpretation":"The architecture has at most 2^P linear regions, but the number actually visited is data- and training-dependent."}],
        ["paper.pdf pp. 3–5, Eqs. (1)–(5) and Figures 1–2: AL-RNN and symbolic coding","paper.pdf pp. 5–6: fixed-point and periodic-orbit theorems","paper.pdf pp. 7–9, Figures 3–7: minimal chaotic and ECG reconstructions","paper.pdf p. 10, Figure 8: fMRI task-stage result and observation resets","source PDF SHA-256 e6ae0c637d75d3ee0de3628aece784924fb97683c89e500f830bfbbcc75b9934","Evidence status: full-text verified theory/numerical study; no independent reproduction performed."],
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
