#!/usr/bin/env python3
"""Install the second evidence-audited Paper Collection card batch."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def section(title: str, *paragraphs: str) -> dict[str, object]:
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


CARDS = [
    {
        "arxiv_id": "1405.0791",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/1405.0791",
        "title_en": "Structure of Exact Renormalization Group Equations for field theory",
        "title_zh": "场论精确重整化群方程的结构",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("a225a99d3c053189", "Renormalization Group"),
        "verified_metadata": {
            "arxiv_id": "1405.0791",
            "version": "v1",
            "title": "Structure of Exact Renormalization Group Equations for field theory",
            "authors": ["C. Bervillier"],
            "categories": ["hep-th"],
            "primary_category": "hep-th",
            "published": "2014-05-05T06:48:59Z",
            "abstract": "The scale-dependent full action and full effective action, including rescaling and field renormalization, are connected by a simple Legendre transform after explicit cutoff references are removed.",
        },
        "sections": [
            section("作者信息", "作者：C. Bervillier；论文为 arXiv:1405.0791v1，主分类 hep-th。", "本卡核对 48 页全文。论文是 Wilson/Polchinski 型精确重整化群与有效平均作用量之间关系的结构性推导，不是数值模拟或实验论文。"),
            section("研究问题", "Wilson 型尺度依赖全作用量与 1PI 尺度依赖全有效作用量通常使用不同截止核和不同形式的 Legendre 变换。作者问：在同时纳入重标度与场重整化后，能否把两套 ERG 写成不显含 cutoff procedure、且仍由简单 Legendre 变换连接的场论方程？", "关键困难是场重整化不能只在固定点外加一个反常维数；它应由在固定点恰好边缘的冗余算符实现，并在两种作用量表述间保持结构。"),
            section("背景", "精确 RG 将逐层消去自由度写成泛函微分流。Wilson 的原始方程包含 coarse graining、动量重标度和场重标度；Polchinski 方程及 Wetterich 类方程则强调不同的 cutoff kernel。", "冗余算符对应场变量重定义，不改变物理可观测量。若其在固定点恰好边缘，就能沿 RG 流实现有限场归一化，并为反常维数提供几何上清楚的位置。"),
            section("模型与方法", r"作者从含三步变换的 Wilson 流出发：消去高动量模、恢复无量纲动量、再以 exactly marginal redundant operator 实现场重整化。场与作用量均用运行尺度无量纲化。", r"随后同时移除总体 UV 尺度 \(\Lambda_0\) 与对应 IR 尺度 \(\mu\)，把残留尺度仅作为 RG-time \(t\) 的参考。对偶变量满足 \(\Phi=\delta S/\delta\phi\) 与 \(\phi=-\delta\Gamma/\delta\Phi\)。", "作者逐项变换平移项、二阶泛函导数项和冗余算符，检查 Wilson 侧的流如何映射到有效作用量侧。"),
            section("核心结果与证据", r"两种尺度依赖全作用量由极简 Legendre 关系连接：\(\Gamma[\Phi,t]-S[\phi,t]+\phi\!\cdot\!\Phi=0\)。该式不含附加的 cutoff quadratic term，简化来自作者先完成的 UV/IR 极限与变量定义。", r"场重整化由固定点的 exactly marginal redundant operator 生成；Legendre 变换保持其冗余性与恰好边缘性。因此 \(\eta\) 不是随意插入的系数，而是固定点场归一化方向的标记。", r"最终流显式不引用真实动量截止函数，并在 \(\eta_*<2\) 条件下具有所需极限。这里的无 cutoff 是方程表达与极限结构的陈述，不意味着所有中间正则化步骤都可省略。"),
            section("有效性与局限", "推导依赖作者选定的全作用量、无量纲变量和边界条件；不能把简洁 Legendre 式直接替换到任意常见 FRG 约定而不重做变量映射。", r"去除显式 cutoff 的极限要求固定点反常维数满足 \(\eta_*<2\)。若理论或截断不满足该条件，文中的构造不能原样使用。", "文章主要证明形式结构，没有用具体相互作用模型比较临界指数、截断误差或数值稳定性；方法价值与计算优势仍需在模型级近似中检验。", "冗余算符表达场变量自由度，不产生新的物理本征方向；将其误当成独立相关耦合会错误计算临界面维数。"),
            section("复现与资源", "原文：https://arxiv.org/abs/1405.0791；PDF：https://arxiv.org/pdf/1405.0791。", "全文 PDF 共 48 页，SHA-256：53b3dad32080e21ac04d562eeca77c0de33af06a83035dedbad118b2ab3e5963。", "最小复核应从 Wilson 流的三项变换开始，固定 Fourier 与泛函导数约定，分别验证 Legendre 映射、二阶核的逆关系和冗余算符在固定点的零本征值。", "Evidence status: full-text verified; no independent reproduction performed."),
            section("阅读指南", "先读引言和 Sec. 2，明确作者所谓 full action、full effective action 与 usual effective average action 的差别。", "再沿 Secs. 3–4 追踪 UV/IR 极限及 Legendre 变量；每次出现无 cutoff 的表述，都检查它指的是最终表达还是推导中间步骤。", "最后读场重整化与 EMRO 部分；物理核心不是公式变短本身，而是场归一化方向如何在两套 RG 表述间保持。"),
        ],
        "cover": {
            "mode": "title_abstract",
            "abstract_text": "论文把包含重标度与场重整化的 Wilson 型尺度依赖全作用量，同尺度依赖的全有效作用量联系起来。通过先移除总体 UV/IR cutoff 并用恰好边缘冗余算符实现有限场归一化，两者满足不带额外二次核的简单 Legendre 关系。结果揭示两套 ERG 的共同几何结构，但依赖明确的变量约定与固定点条件，尚不等同于具体截断计算的数值改进。",
            "selection_rationale": "论文没有承担核心证据作用的物理可视化；主要贡献是一套泛函结构和变量构造，因此题目与摘要比装饰性示意图更准确。",
        },
        "figure_refs": [],
        "equation_refs": [
            {
                "label": "Cutoff-free Legendre relation",
                "latex": r"\Gamma[\Phi,t]-S[\phi,t]+\phi\cdot\Phi=0",
                "role": "map the scale-dependent full action to the full effective action",
                "symbols": {"S": "scale-dependent full action", "Gamma": "scale-dependent full effective action", "phi": "dimensionless renormalized Wilson field", "Phi": "dimensionless renormalized Legendre-dual field", "t": "RG time"},
                "evidence": "paper.pdf abstract and central derivation, pp. 33–39",
                "interpretation": "After the correlated UV/IR limits, the two ERG descriptions are dual without an explicit regulator-dependent quadratic term.",
            }
        ],
        "evidence_refs": [
            "paper.pdf pp. 3–12: Wilson ERG, dimensionless variables and field-renormalization setup",
            "paper.pdf pp. 20–32: UV/IR limits and removal of explicit cutoff references",
            "paper.pdf pp. 33–44: Legendre mapping and exactly marginal redundant operator",
            "source PDF SHA-256 53b3dad32080e21ac04d562eeca77c0de33af06a83035dedbad118b2ab3e5963",
            "Evidence status: full-text verified; no independent reproduction performed.",
        ],
    },
    {
        "arxiv_id": "1510.08707",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/1510.08707",
        "title_en": "Generic finite size scaling for discontinuous nonequilibrium phase transitions into absorbing states",
        "title_zh": "吸收态非平衡不连续相变的普适有限尺寸标度",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "theory_numerics",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("9be56e39c1ff6ed6", "Statistical Physics"),
        "verified_metadata": {
            "arxiv_id": "1510.08707",
            "version": "v1",
            "title": "Generic finite size scaling for discontinuous nonequilibrium phase transitions into absorbing states",
            "authors": ["M. M. de Oliveira", "M. G. E. da Luz", "C. E. Fiore"],
            "categories": ["cond-mat.stat-mech"],
            "primary_category": "cond-mat.stat-mech",
            "published": "2015-10-29T14:30:14Z",
            "abstract": "A quasi-stationary finite-size scaling theory for discontinuous nonequilibrium transitions into absorbing states is tested in five lattice models.",
        },
        "sections": [
            section("作者信息", "作者：M. M. de Oliveira、M. G. E. da Luz、C. E. Fiore；论文为 arXiv:1510.08707v1，主分类 cond-mat.stat-mech。", "本卡核对 6 页全文。工作结合双峰概率分布近似与五种晶格模型的准稳态 Monte Carlo。"),
            section("研究问题", "平衡一阶相变具有体积控制的有限尺寸标度：响应峰随体积增长，伪临界点偏移按逆体积衰减。含吸收态的非平衡系统没有普通平衡配分函数，而且有限系统最终必然落入吸收态；相同标度是否仍成立？", "作者还问这种行为是否依赖只有一个吸收态还是无限多个吸收态，以及不同微观反应规则能否共享同一尺度变量。"),
            section("背景", "直接长时间平均会被吸收态支配，使活性相的分布与涨落不可测。准稳态方法在系统将吸收时，用此前保存的活性构型替换它，从条件于存活的分布中取样。", "一阶共存附近，有限系统的序参量分布可近似为两支窄峰的叠加；峰权重随控制参数和体积呈指数竞争，由此可以解析推出响应函数与累积量的尺度。"),
            section("模型与方法", r"作者把准稳态序参量分布写成两个 Gaussian 相贡献，并以体积 \(V=L^d\) 控制峰宽与相权重。相等权重位置定义有限尺寸伪转变点 \(\lambda_V\)。", "数值部分覆盖五种短程晶格模型：ZGB、一种双物种接触过程、竞争接触过程以及两个 Schlögl 模型变体，既包含单吸收态也包含无限多吸收构型。", "对每个尺寸扫描控制参数，测量平均序参量、方差型响应、moment ratio 与概率分布，并检验重标度后曲线坍缩及伪临界点外推。"),
            section("核心结果与证据", r"两峰近似给出 \(|\lambda_V-\lambda_0|\sim V^{-1}\)：伪转变点以逆体积趋近热力学极限。序参量跃变保持有限，而方差型响应和 moment-ratio 极值随 \(V\) 增长。", r"Figure 1 的 ZGB 数据把 \(\chi\) 除以 \(L^2\)，并用 \(y^*=(Y-Y_0)L^2\) 重标度控制参数后实现不同系统尺寸的曲线坍缩；右下图显示转变点对 \(1/L^2\) 近线性。", "其余四个模型给出同类体积标度，包括具有无限多个吸收态的情形。证据支持共存分布的体积控制，而不是特定反应规则的偶然拟合。", "结论是这类非平衡吸收态一阶相变与平衡一阶相变共享有限尺寸标度结构，但准稳态分布代替了 Gibbs 分布。"),
            section("有效性与局限", "五个模型均为短程晶格模型，且数值尺寸有限；长程相互作用、守恒场、强各向异性或更高维临界端点可能引入额外尺度。", "准稳态替换改变了吸收事件后的轨迹，因此测得的是条件于存活的分布；它适合定位活性—吸收共存，却不是原始无条件动力学的等待时间分布。", "Gaussian 双峰近似远离共存点或在界面贡献显著时会有修正。数据坍缩支持主导体积指数，但不能排除次领先有限尺寸项。", "论文关于时间无序的讨论是初步延伸；不能从本组空间有限尺寸结果直接推出所有随机环境下的一阶性稳定。"),
            section("复现与资源", "原文：https://arxiv.org/abs/1510.08707；PDF：https://arxiv.org/pdf/1510.08707。", "全文 PDF 共 6 页，SHA-256：3fe882912821c9ba2db49a9f7d1eb27b90c667ac10e310287331e2aeab72c0cd。", "复现至少保存每个尺寸的完整准稳态序参量直方图、替换库参数、热化与采样长度；同时分别拟合峰高对体积、伪临界偏移对逆体积，并报告次领先修正。", "Evidence status: full-text verified; no independent reproduction performed."),
            section("阅读指南", "先读理论段落中的双 Gaussian 分布与相权重，确认逆体积偏移来自指数竞争。", "再看 Figure 1：依次检查原始跃变、响应峰、重标度坍缩和外推，避免只凭一张 collapsed curve 判断标度。", "最后横向比较五种模型及其吸收态数目；核心主张是体积标度对微观规则的稳健性，不是所有动力学量都具有平衡对应物。"),
        ],
        "cover": {
            "mode": "source_figure",
            "asset_path": "assets/collection-figures/1510.08707/figure-1-zgb-scaling.webp",
            "label": "Figure 1",
            "visual_type": "comparison",
            "evidence": "arXiv:1510.08707v1, paper.pdf p. 2, Figure 1",
            "alt_text": "ZGB 模型的序参量跃变、响应峰、有限尺寸曲线坍缩及转变点逆面积外推。",
            "caption": "四联图把一阶跃变、峰值随体积增长、尺度变量坍缩和伪临界点的逆体积外推放在同一证据链中。",
            "selection_rationale": "Figure 1 是论文最完整的物理证据图，同时展示原始数据与有限尺寸标度检验，可直接替代大段数值叙述。",
        },
        "figure_refs": [
            {
                "label": "Figure 1",
                "asset_path": "assets/collection-figures/1510.08707/figure-1-zgb-scaling.webp",
                "section": "核心结果与证据",
                "role": "show the full finite-size-scaling chain for the ZGB model",
                "evidence": "arXiv:1510.08707v1, paper.pdf p. 2, Figure 1",
                "alt_text": "ZGB 模型四联有限尺寸标度图。",
                "caption": "不同 L 的响应经体积与控制参数重标度后坍缩，伪转变点对逆面积外推。",
                "interpretation": "峰高、横轴尺度和伪临界偏移都由体积控制，形成比单一拟合更强的相互一致证据。",
            }
        ],
        "equation_refs": [
            {
                "label": "Inverse-volume transition shift",
                "latex": r"|\lambda_V-\lambda_0|\sim V^{-1}",
                "role": "extrapolate the finite-system coexistence point",
                "symbols": {"lambda_V": "finite-volume pseudotransition point", "lambda_0": "thermodynamic-limit transition point", "V": "system volume"},
                "evidence": "paper.pdf pp. 1–2, two-Gaussian finite-size argument",
                "interpretation": "The control-parameter window over which the two phases exchange weight narrows inversely with volume.",
            },
            {
                "label": "ZGB scaling variable",
                "latex": r"y^*=(Y-Y_0)L^2,\qquad \chi^*=\chi/L^2",
                "role": "collapse two-dimensional finite-size data",
                "symbols": {"Y": "control parameter", "Y_0": "thermodynamic transition point", "L": "linear size", "chi": "response function"},
                "evidence": "paper.pdf p. 2, Figure 1",
                "interpretation": "Both the transition window and the response peak scale with the two-dimensional volume.",
            },
        ],
        "evidence_refs": [
            "paper.pdf pp. 1–2: quasi-stationary two-Gaussian finite-size theory and Figure 1",
            "paper.pdf pp. 2–5: five lattice-model tests, response peaks, moment ratios and data collapse",
            "paper.pdf pp. 5–6: scope, temporal-disorder discussion and conclusions",
            "source PDF SHA-256 3fe882912821c9ba2db49a9f7d1eb27b90c667ac10e310287331e2aeab72c0cd",
            "Evidence status: full-text verified; no independent reproduction performed.",
        ],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(card["arxiv_id"])
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
