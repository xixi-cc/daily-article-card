#!/usr/bin/env python3
"""Install the final three independently addressable Collection cards."""
from __future__ import annotations

import json
from pathlib import Path

from install_full_collection_batch_014 import sec
from install_full_collection_batch_032 import card


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def title_abstract_card(*args: object, abstract_text: str, **kwargs: object) -> dict[str, object]:
    """Create a v2.3 card whose cover deliberately uses verified title/abstract text."""
    item = card(*args, **kwargs)
    item["cover"] = {
        "mode": "title_abstract",
        "abstract_text": abstract_text,
        "selection_rationale": (
            "The author-uploaded full text is page-addressable, but its figures are not redistributed "
            "in this repository; the verified title and abstract therefore form the safest faithful cover."
        ),
    }
    item["figure_refs"] = []
    return item


CARDS = [
    card(
        "doi-10.1007-s12648-024-03117-3",
        "Indian Journal of Physics version of record",
        "https://link.springer.com/content/pdf/10.1007/s12648-024-03117-3.pdf",
        "Dynamics of driven Janus particles with pure repulsive interactions over obstacle arrays in active bath",
        "活性浴中纯排斥相互作用驱动 Janus 粒子穿越障碍阵列的动力学",
        "numerical",
        "7a530139c13c4d20",
        "Active Matter",
        {
            "doi": "10.1007/s12648-024-03117-3",
            "version": "version of record",
            "title": "Dynamics of driven Janus particles with pure repulsive interactions over obstacle arrays in active bath",
            "authors": ["K. X. Yang", "M. Zahid", "Y. G. Cao"],
            "journal": "Indian Journal of Physics",
            "volume": "98",
            "issue": "10",
            "pages": "3635–3640",
            "published": "2024-02-29",
            "abstract": (
                "Overdamped Langevin simulations compare driven repulsive Janus particles in active and thermal noise "
                "over a triangular obstacle array, revealing active-noise depinning thresholds and cluster changes."
            ),
            "comment": "Six-page version of record; no correction or retraction relation found in Crossref",
        },
        [
            sec(
                "作者信息",
                "作者 K. X. Yang、M. Zahid、Y. G. Cao，郑州大学物理与微电子学院；Indian Journal of Physics 98(10), 3635–3640 (2024)，DOI:10.1007/s12648-024-03117-3。核验六页期刊版、Crossref元数据与完整参考文献。",
            ),
            sec(
                "研究问题",
                "只含排斥势的 Janus 粒子在周期障碍阵列中受恒定外驱时，active bath 是否会产生不同于thermal noise的钉扎、非线性速度–力关系与移动团簇？障碍刚度 Ke 和粒子间screened-Coulomb强度 As 又如何调节这些集体状态？",
            ),
            sec(
                "背景",
                "active bath的有色噪声具有有限相关时间，持续碰撞可使被动粒子的有效噪声和相互作用依赖外部约束。论文把这种constraint-dependent resistance称为active friction，并用thermal white noise作为对照。",
                "这里的 Janus particle 是二维数值粒子，不包含显式半球化学、流体场或自推进方向；‘Janus’主要沿用被active bath驱动的实验语境。因此结果是最小Langevin模型中的机制检验，不是具体胶体实验的定量预测。",
            ),
            sec(
                "模型与方法",
                "系统含 N=400 个粒子和 N0=400 个障碍，二者初始均为三角晶格并采用二维周期边界。粒子–粒子势由 r^-12 nuclear repulsion 与 screened Coulomb repulsion组成；障碍势为 Ke(r-r0)^2。外力 fd 沿 x 方向，测量稳态平均速度 V。",
                "thermal noise满足delta correlation，active noise相关函数按 exp(-|t-t'|/tau)/tau 衰减。作者固定 dt=0.001，先演化 10^5 steps 平衡，再对 2×10^5 steps 取平均；比较多组 Ke 与 As，并用structure factor Bragg-peak平均强度衡量移动有序度。",
            ),
            sec(
                "核心结果与证据",
                "Figure 1显示active-noise曲线存在有限depinning threshold fc，且 fc 随障碍刚度增大；thermal-noise曲线从很小驱动力即出现有限速度。超过阈值后active曲线明显非线性，而thermal对照近似线性。",
                "Figures 2–3显示弱障碍时active bath介导的有效吸引使粒子在障碍间形成周期移动团簇；提高 Ke 后团簇散开并呈plastic-like flow，Bragg peak先显著下降再恢复。thermal-noise对照基本保持沿驱动方向的移动六角结构。",
                "Figure 4在固定 Ke=0.01 时改变 As：两条active-noise曲线均有阈值，强排斥 As=2 的阈值更高；thermal curves仍近似线性。Figures 5–6进一步表明弱 As 时团簇和plastic flow更明显，强 As 时运动更相干。论文没有给fc的临界标度拟合，不能把图中拐点解释为已建立的普适depinning exponent。",
            ),
            sec(
                "有效性与局限",
                "结果来自单一粒子数、单一障碍排列和有限参数切片；未报告system-size、time-step、initial-condition或多seed误差条，因此阈值位置和Bragg强度的数值精度有限。active noise被建模为给定相关函数，没有显式bath particles或hydrodynamic interaction。",
                "作者将团簇变化解释为constraint-dependent effective attraction/repulsion，但没有测量pair potential或two-particle force；这是与轨迹及structure factor一致的机制解释。障碍阵列、势函数和低温设置改变后是否保留相同相图，全文未验证。",
            ),
            sec(
                "复现与资源",
                "期刊：https://doi.org/10.1007/s12648-024-03117-3；version-of-record PDF SHA-256：4b1c91488130409d07ec081dfdb4999ab4b33fb101756254f89d680d5acad060。正文未给代码或数据仓库。",
                "复现需固定 N、N0、triangular lattice constant、Ke、As、screening length、noise strength/correlation time、dt、equilibration/averaging windows和随机种子，并分别报告velocity与structure-factor uncertainty。Evidence status: full-text verified numerical study; no independent reproduction performed.",
            ),
            sec(
                "阅读指南",
                "先读 p.3636 的Eqs. (1)–(8)确认噪声与势函数，再看 pp.3636–3637 Figure 1 的depinning对照；p.3638 Figures 2–4连接团簇、Bragg peak和速度曲线，pp.3638–3639 Figures 5–6检验 As 依赖，最后读 p.3640结论。",
            ),
        ],
        "figure-4-depinning-curves.webp",
        "Figure 4",
        4,
        "data_plot",
        "平均速度随外驱力变化：active noise在两种粒子间排斥强度下均出现有限阈值，thermal noise对照近似线性。",
        "固定障碍刚度时，增强粒子间排斥使active-noise depinning threshold右移，而thermal-noise曲线没有有限钉扎区。",
        "Figure 4直接隔离粒子间排斥强度，并以thermal-noise基线呈现论文最核心的有限阈值与非线性速度–力证据。",
        [
            {
                "label": "Overdamped driven Langevin dynamics",
                "latex": r"\gamma\dot{\mathbf R}_i=-\sum_{j\ne i}\nabla_iU_{\rm rep}(R_{ij})-\sum_j\nabla_iU_{\rm obs}(\mathbf R_i-\mathbf r_j)+\mathbf f_d+\mathbf f_i^{L}",
                "role": "define driven particle motion in the repulsive obstacle landscape",
                "symbols": {
                    "gamma": "viscous coefficient",
                    "R_i": "particle position",
                    "U_rep": "particle-particle repulsion",
                    "U_obs": "particle-obstacle potential",
                    "f_d": "constant drive",
                    "f_i^L": "thermal or active noise",
                },
                "evidence": "paper.pdf p. 2, Eq. (1)",
                "interpretation": "All reported phases follow from this coarse-grained overdamped model rather than explicit bath dynamics.",
            }
        ],
        [
            "paper.pdf pp. 1–2: model and noise correlations",
            "paper.pdf pp. 2–3, Figures 1–3: stiffness-dependent depinning and order",
            "paper.pdf pp. 3–5, Figures 4–6: repulsion-strength dependence",
            "source PDF SHA-256 4b1c91488130409d07ec081dfdb4999ab4b33fb101756254f89d680d5acad060",
            "Evidence status: full-text verified numerical study; no independent reproduction performed.",
        ],
    ),
    card(
        "doi-10.1038-s42256-020-0146-9",
        "Nature Machine Intelligence review version of record",
        "https://www.nature.com/articles/s42256-020-0146-9.pdf",
        "Machine learning for active matter",
        "面向活性物质的机器学习",
        "theory_experiment",
        "410bd81b48760e99",
        "Active Matter",
        {
            "doi": "10.1038/s42256-020-0146-9",
            "version": "version of record",
            "title": "Machine learning for active matter",
            "authors": ["Frank Cichos", "Kristian Gustavsson", "Bernhard Mehlig", "Giovanni Volpe"],
            "journal": "Nature Machine Intelligence",
            "volume": "2",
            "issue": "2",
            "pages": "94–103",
            "published": "2020-02-14",
            "abstract": (
                "A review organizes machine-learning applications to active-matter imaging, time series, model discovery, "
                "navigation and collective control, then states opportunities and methodological cautions."
            ),
            "comment": "Review article; the figures synthesize results from cited primary studies",
        },
        [
            sec(
                "作者信息",
                "作者 Frank Cichos、Kristian Gustavsson、Bernhard Mehlig、Giovanni Volpe；Nature Machine Intelligence 2, 94–103 (2020)，DOI:10.1038/s42256-020-0146-9。核验十页期刊全文；文章是领域综述，不是新的统一benchmark。",
            ),
            sec(
                "研究问题",
                "机器学习已进入活性粒子成像、轨迹分类、数据驱动动力学、导航和群体控制。综述问：哪些方法已在何种active-matter任务上成功，active matter又能为learning与embodied intelligence提供什么测试床，以及黑箱、泛化和simulation-to-reality会造成哪些科学风险？",
            ),
            sec(
                "背景",
                "active matter从分子马达到细菌、动物群体和机器人，持续消耗能量并远离热平衡。其自由度多、尺度跨度大且常缺少闭合守恒律，因此数据驱动方法适合做检测、降维、预测和策略搜索，但不能自动取代mechanistic explanation。",
                "Box 1按supervised、semi-supervised与unsupervised组织CNN、RNN、reservoir computing、GAN、reinforcement learning、genetic algorithms、PCA和clustering。这是一张术语与用途地图，并非这些算法在同一数据上的性能排名。",
            ),
            sec(
                "模型与方法",
                "作者按任务而非算法罗列已发表实例：Figure 2是显微粒子检测和细菌群动态相分类；Figure 3是reservoir forecasting与anomalous-diffusion classification；Figure 4覆盖microswimmer、复杂流和glider navigation；Figure 5关注节能编队、机器人自组织及sensory delay。",
                "证据跨实验、数值模拟和机器人平台，训练集、指标与任务不同。综述引用 primary papers 支撑案例，但没有系统检索协议、纳入排除标准或统一effect size，因此应作为narrative landscape review阅读。",
            ),
            sec(
                "核心结果与证据",
                "Figure 2a所引primary work显示CNN在低SNR particle detection上优于若干传统定位方法；Figure 2b用t-SNE与k-means区分swarming bacteria的单细胞、raft和biofilm-related states。它们说明ML可改善数据提取，但分类标签仍需实验与机制解释。",
                "Figure 3a的reservoir model可在示例chaotic field中预测约六个Lyapunov times；Figure 3b的RNN在短、不规则或intermittent trajectories上估计anomalous exponent优于标准MSD。两例都受训练分布和生成数据模型约束。",
                "Figures 4–5展示reinforcement learning与evolutionary approaches可搜索复杂流中的导航、滑翔与协同游动策略，也可由群体轨迹反推self-organization rule。综述将这些归纳为互惠关系：ML帮助理解/控制active systems，active systems则提供具物理约束的embodied-learning平台。",
            ),
            sec(
                "有效性与局限",
                "作者明确警告catastrophic forgetting、overconfidence、black-box interpretation、preprocessing bias与distribution shift。模拟策略可能存在reality gap，且在一个agent、flow或sensor set上优良的policy未必能推广到另一物理平台。",
                "截至2020年的案例规模和算法已经陈旧；综述未覆盖foundation models、modern neural operators或diffusion policies。Figure中的结果来自不同论文，不能据此声称某一ML family普遍优于另一类，也不能把预测精度等同于发现因果机制。",
            ),
            sec(
                "复现与资源",
                "期刊：https://doi.org/10.1038/s42256-020-0146-9；version-of-record PDF SHA-256：7a24a32e5fe28bbf6c728e1133684b0ea8cccd3ff1987b43167c4a45bb509542。综述无统一代码或数据集，应沿各Figure caption的primary references分别复核。",
                "复现单个案例需固定raw data、labels、preprocessing、train/test split、network、baseline、random seeds与physical evaluation；导航任务还需报告observation/action space、reward与sim-to-real test。Evidence status: full-text verified narrative review; no independent reproduction performed.",
            ),
            sec(
                "阅读指南",
                "先读 pp.94–96 Figure 1和Box 1建立active-matter/ML词汇，再看 pp.97–99 Figures 2–5按数据分析、model discovery、navigation和collective control阅读。最后精读 pp.99–101 opportunities/challenges与五条实践建议，并回到primary references核验具体数字。",
            ),
        ],
        "figure-5-collective-dynamics.webp",
        "Figure 5",
        6,
        "comparison",
        "机器学习参与的三类集体动力学案例：节能游动、机器人群自组织和带感觉延迟的聚集或分离。",
        "不同active platforms展示策略学习、behavior inference与sensorimotor feedback如何连接到群体结构。",
        "Figure 5覆盖数值、机器人实验与反馈动力学，最能体现综述强调的active matter与machine learning双向关系。",
        [
            {
                "label": "Anomalous diffusion scaling",
                "latex": r"\langle |\mathbf r(t)-\mathbf r(0)|^2\rangle\propto t^{\alpha}",
                "role": "define the trajectory exponent classified by recurrent models",
                "symbols": {
                    "r": "particle position",
                    "t": "lag time",
                    "alpha": "anomalous diffusion exponent",
                },
                "evidence": "paper.pdf p. 4, Figure 3b and surrounding discussion",
                "interpretation": "Machine learning estimates alpha from finite trajectories; it does not by itself identify the microscopic mechanism.",
            }
        ],
        [
            "paper.pdf pp. 1–3, Figure 1 and Box 1: active-matter and ML taxonomy",
            "paper.pdf pp. 3–6, Figures 2–5: data, models, navigation and collective dynamics",
            "paper.pdf pp. 6–8: opportunities, challenges and guidelines",
            "source PDF SHA-256 7a24a32e5fe28bbf6c728e1133684b0ea8cccd3ff1987b43167c4a45bb509542",
            "Evidence status: full-text verified narrative review; no independent reproduction performed.",
        ],
    ),
    title_abstract_card(
        "doi-10.1063-1.2803837",
        "author-uploaded eight-page journal full text",
        "https://www.researchgate.net/publication/30767130_Simulation_of_hydrodynamically_interacting_particles_near_a_no-slip_boundary",
        "Simulation of hydrodynamically interacting particles near a no-slip boundary",
        "无滑移边界附近流体动力学相互作用粒子的模拟",
        "theory_numerics",
        "0d71d07519234ebd",
        "Fluid Dynamics",
        {
            "doi": "10.1063/1.2803837",
            "version": "author-uploaded journal full text cross-checked with Caltech thesis appendix",
            "title": "Simulation of hydrodynamically interacting particles near a no-slip boundary",
            "authors": ["James W. Swan", "John F. Brady"],
            "journal": "Physics of Fluids",
            "volume": "19",
            "issue": "11",
            "pages": "113306-1–113306-8",
            "published": "2007-11-14",
            "abstract": (
                "A wall-reflected Green-function construction extends Stokesian dynamics while preserving symmetric, "
                "positive-definite mobility and resistance tensors, with a torque-driven particle doublet as a test."
            ),
            "comment": "Author-uploaded full text; formulas cross-checked against Appendix A of Swan's 2010 Caltech thesis",
        },
        [
            sec(
                "作者信息",
                "作者 James W. Swan、John F. Brady；Physics of Fluids 19, 113306 (2007)，DOI:10.1063/1.2803837。核验作者上传的八页期刊全文，并与 Swan 2010 Caltech 博士论文 Appendix A 中同一wall-reflected mobility formulas交叉检查。",
            ),
            sec(
                "研究问题",
                "如何把单个no-slip plane wall的长程many-body reflection与近场sphere–sphere、sphere–wall lubrication纳入Stokesian dynamics，同时保证grand mobility/resistance tensors对称且正定，从而可用于Brownian dynamics？既有multipole和wall Rotne–Prager近似为何破坏这些性质？",
            ),
            sec(
                "背景",
                "在零Reynolds数下，force/torque/stresslet与translation/rotation/rate-of-strain由grand mobility tensor线性联系。reciprocal theorem要求该tensor symmetric positive definite；否则Brownian covariance不能物理构造，且可能产生非正耗散。",
                "unbounded Stokesian dynamics用Stokeslet multipoles、Faxén laws与lubrication correction组合远近场。加入墙后，Green function包含source position经image映射的显式依赖，若导数只对separation vector处理就会遗漏高阶项并破坏reciprocity。",
            ),
            sec(
                "模型与方法",
                "作者采用Blake对no-slip wall的Stokeslet reflection，写 G=J+Jw；对球面force density做multipole expansion并在stresslet阶截断，再对每个reflected singularity施加translation、rotation和strain Faxén operators，逐项构造self-wall与pair-wall mobility blocks。",
                "grand resistance取 R=M^-1，并叠加已知近场particle–particle和particle–wall lubrication divergences。文章指出：直接反射由multipole truncation得到的mobility，或把unbounded Rotne–Prager tensor当作可反射flow field，都会漏掉保持symmetry所需的quadrupolar/octupolar contributions。",
            ),
            sec(
                "核心结果与证据",
                "pp.113306-2–4逐式给出wall Green function、surface-moment expansion与Faxén construction；所得self/pair blocks满足force–rotation与torque–translation等reciprocal transpose relations。Appendices A–C列出reflected Stokeslet贡献和wall self/pair terms，便于tabulation。",
                "Figures 2–3用两等半径球、沿连心线施加大小相等方向相反的torque作物理检验。无界流体中doublet只自转；靠墙后translation–rotation coupling使其绕质心共同转动。对称模型给连接线张力严格为零，非对称近似则需要伪张力保持间距。",
                "Figure 3显示归一化rotation rate在近接触且接近墙面处最大，约位于 r=2.1a、h=1.01a。作者还说明free surface可用image particles实现，而finite-viscosity flat interface的Green function可由free-surface与solid-wall结果按viscosity ratio线性组合。",
            ),
            sec(
                "有效性与局限",
                "推导限制于rigid spheres、Newtonian Stokes flow、平面不可变形边界及stresslet-level far-field truncation；近场lubrication补偿不使有限截断成为exact many-body solution。双球例检验symmetry和趋势，不是大规模Brownian suspension benchmark。",
                "文章称可推广到任意confining geometry的前提是已知相应wall-reflected Stokeslet；复杂曲面、deformable interfaces、finite Reynolds number、non-spherical particles或overlap configuration需额外Green functions和近场处理。parallel-wall superposition只是近似。",
            ),
            sec(
                "复现与资源",
                "作者上传全文：https://www.researchgate.net/publication/30767130_Simulation_of_hydrodynamically_interacting_particles_near_a_no-slip_boundary；DOI：https://doi.org/10.1063/1.2803837。Caltech thesis：https://thesis.caltech.edu/5845/1/thesis.pdf，SHA-256：8ef0d4f57f73bafa27258f2c0e478d61dd0a7cd5bc684dc3a22e663eaeca8bee；其Appendix A从thesis p.178开始，仅作公式交叉检查。",
                "复现应以paper pp.1–8为分页权威，逐块检查M的transpose symmetry与eigenvalues，并固定multipole order、lubrication subtraction/addition、particle height/separation和normalization。Evidence status: full-text verified analytical/numerical method; no independent reproduction performed.",
            ),
            sec(
                "阅读指南",
                "先读 pp.113306-1–2 Eq. (1)与Figure 1确定block convention；pp.113306-2–3 Eqs. (6)–(17)是reflection与Faxén核心；p.113306-4比较两个失败近似，p.113306-5 Figures 2–3看symmetry test，最后查 pp.113306-6–8 Appendices A–C。",
            ),
        ],
        "unused.webp",
        "Title and abstract",
        1,
        "schematic",
        "Verified title and abstract of the author-uploaded full text.",
        "The cover preserves the source boundary without redistributing a figure.",
        "A title-and-abstract cover is the faithful non-redistributive choice for this author-uploaded source.",
        [
            {
                "label": "Grand mobility relation",
                "latex": r"\begin{pmatrix}\mathbf U-\mathbf U^{\infty}\\\boldsymbol\Omega-\boldsymbol\Omega^{\infty}\\-\mathbf E^{\infty}\end{pmatrix}=-\mathbf M\begin{pmatrix}\mathbf F\\\mathbf L\\\mathbf S\end{pmatrix},\qquad \mathbf R=\mathbf M^{-1}",
                "role": "couple force moments to particle velocity moments in Stokes flow",
                "symbols": {
                    "M": "grand mobility tensor",
                    "R": "grand resistance tensor",
                    "F": "force",
                    "L": "torque",
                    "S": "stresslet",
                    "U": "translation",
                    "Omega": "rotation",
                    "E": "rate of strain",
                },
                "evidence": "author-uploaded paper p. 1, Eq. (1)",
                "interpretation": "Reciprocity and positive dissipation require a symmetric positive-definite mobility tensor.",
            },
            {
                "label": "Wall-reflected Green function",
                "latex": r"\mathbf G(\mathbf x,\mathbf y;H)=\mathbf J(\mathbf x,\mathbf y)+\mathbf J^{W}(\mathbf x,\mathbf y;H)",
                "role": "separate the free-space Stokeslet from its no-slip-wall reflection",
                "symbols": {
                    "G": "total Stokes Green function",
                    "J": "free-space Stokeslet",
                    "J^W": "wall-reflected field",
                    "H": "wall location",
                },
                "evidence": "author-uploaded paper p. 2, Eq. (7)",
                "interpretation": "Source-coordinate derivatives of the reflected term must be retained before applying Faxén operators.",
            },
        ],
        [
            "author-uploaded paper pp. 1–3: grand mobility and wall-reflection construction",
            "author-uploaded paper pp. 3–5, Figures 2–3: symmetry failures and doublet test",
            "author-uploaded paper pp. 5–8: conclusions and explicit mobility appendices",
            "Caltech thesis Appendix A, thesis pp. 178–183: independent formula cross-check",
            "Evidence status: full-text verified analytical/numerical method; no independent reproduction performed.",
        ],
        abstract_text=(
            "The authors construct symmetric, positive-definite mobility and resistance tensors for spherical particles "
            "near a no-slip plane wall by reflecting the Stokeslet and applying the full source-coordinate Faxén operators."
        ),
    ),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for item in CARDS:
        paper_id = str(item["arxiv_id"])
        (OUT / f"{paper_id}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        installed.append(paper_id)
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
