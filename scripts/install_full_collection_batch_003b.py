#!/usr/bin/env python3
"""Install visual evidence cards for full Collection backfill batch 003."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "collection_cards"


def sec(title: str, *paragraphs: str) -> dict[str, object]:
    return {"title": title, "paragraphs": list(paragraphs)}


def provenance(record_id: str, topic: str) -> dict[str, object]:
    return {"program": "Collection", "catalog": "Paper Collection", "catalog_record_id": record_id, "catalog_record_ids": [record_id], "catalog_topic": topic, "collection_date": "2026-08-23", "sampled_at": "2026-08-26", "selected_by": "full_collection_backfill", "sampling_seed": "not_applicable_full_collection", "candidate_count": 452}


CARDS = [
    {
        "arxiv_id": "1807.02128",
        "source_version": "v4",
        "source_pdf": "https://arxiv.org/pdf/1807.02128",
        "title_en": "Adaptive Path-Integral Autoencoder: Representation Learning and Planning for Dynamical Systems",
        "title_zh": "自适应路径积分自编码器：动力系统的表征学习与规划",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("48c4c9615019ef41", "Control & Reinforcement Learning"),
        "verified_metadata": {"arxiv_id": "1807.02128", "version": "v4", "title": "Adaptive Path-Integral Autoencoder: Representation Learning and Planning for Dynamical Systems", "authors": ["Jung-Su Ha", "Young-Jin Park", "Hyeok-Joo Chae", "Soon-Seo Park", "Han-Lim Choi"], "categories": ["cs.LG", "cs.RO", "stat.ML"], "primary_category": "cs.LG", "published": "2018-07-05T18:05:18Z", "abstract": "A semi-amortized variational model casts posterior refinement for latent stochastic trajectories as path-integral control and reuses the learned low-dimensional dynamics for planning."},
        "sections": [
            sec("作者信息", "作者：Jung-Su Ha、Young-Jin Park、Hyeok-Joo Chae、Soon-Seo Park、Han-Lim Choi；论文为 arXiv:1807.02128v4，主分类 cs.LG，交叉 cs.RO 与 stat.ML。", "本卡核对 19 页全文及附录。实验覆盖图像化摆运动与人体 motion-capture 序列。"),
            sec("研究问题", "序列 VAE 的 amortized inference network 必须用一次前向映射近似每条观测序列的后验，容易留下 amortization gap。增加重要性样本只缓解 Monte Carlo 误差，若 proposal 与真实后验错位，权重仍会塌缩。", "作者问：能否把潜在轨迹的后验推断重写成随机最优控制，用 inference network 给出初猜，再通过可微路径积分控制逐样本精化？同一潜动力学是否还能直接承担高维观测空间中的预测与规划？"),
            sec("背景", r"潜状态服从连续时间 SDE \(dz=f(z)dt+\sigma(z)dw\)，观测在离散时刻条件独立。普通 ELBO 与真实 log likelihood 的差正是 \(D_{\mathrm{KL}}(q\Vert p(z\mid x))\)。", "semi-amortized inference 在共享网络输出后为每个样本做局部优化。路径积分控制利用控制—推断对偶，把控制后的轨迹测度向最优后验测度做重要性重加权。"),
            sec("模型与方法", r"proposal 取受控 SDE：\(dz=f(z)dt+\sigma(z)[u(t)dt+dw(t)]\)。Girsanov 定理把 ELBO 写成观测代价、初态密度比、控制能量和随机积分之和，最优变分参数等价于一个 stochastic optimal-control 问题。", r"inference network 是反向 RNN，按 Bellman 最优性结构输出初态 Gaussian 及分段线性反馈 \(u(t,z)=u_k^{ff}-K_kz\)。随后 R 次 path-integral adaptation 用 \(\tilde w_l\propto e^{-S_u[z_l]}\) 对 L 条轨迹加权并匹配矩。", "完整适配与 Monte Carlo objective 均可反向传播；训练后用潜空间 SDE 作为先验，在目标图像代价下再次做路径积分控制，得到未来观测序列。"),
            sec("核心结果与证据", r"控制目标可写成 \(J=D_{\mathrm{KL}}(q_u\Vert p^*)-\log\xi\)，因此控制分布越接近最优轨迹测度，重要性权重方差越小；当 \(u=u^*\) 时理想权重等分。", "Pendulum 与 mocap 实验中，路径积分精化普遍提高训练 lower bound；但 Table 1 同时显示最紧 bound、重构和预测的最优方法并不完全相同，作者明确提醒 tighter bound 不自动推出更好生成模型。", "Figure 1 把潜状态的角度/角速度着色、观测重构、自由预测和四个目标规划放在同一图中：模型不是仅压缩图像，而是学习能被控制输入驱动的低维随机动力学。", "人体运动实验的三维潜流形按步态相位、偏航率和前进速度呈有序结构，并可生成不同转向/速度的规划序列；证据仍来自两个受控数据集。"),
            sec("有效性与局限", "计算量随重要性样本数 L 与 refinement 次数 R 线性增长；GPU 并行降低墙钟时间，但不消除样本退化与高维路径空间的统计代价。", "实验规模有限，缺少现代大规模视频数据、真实机器人闭环和系统性超参数消融；mocap prediction 甚至因缺乏合适指标未量化。", "路径积分线性可解结构要求控制和噪声通道满足特定关系，反馈策略又限制为分段线性形式；复杂多模态后验可能超出变分族。", "Table 1 说明更紧 ELBO 不保证测试预测最佳；评价必须分开 likelihood bound、重构、长期预测与任务规划。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1807.02128；PDF：https://arxiv.org/pdf/1807.02128；补充视频：https://youtu.be/xCp35crUoLQ。", "全文 PDF 共 19 页，SHA-256：7bc2c9002e832405171ef4ed888e7d4853ee082584e76cde77dd97de27bad403。", "复现应固定 L、R、resampling 开关与随机种子，保存每轮有效样本数、ELBO、重构和 rollout error；规划测试还应报告目标误差、碰撞率及潜控制能量。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先读 pp. 2–5，从 ELBO gap 到受控 SDE 和 Girsanov 权重，确认控制代价如何等价于变分 KL。", "再看 Figure 1 和 Figure 2，把潜空间着色与预测/规划序列一一对应；它们比单独的 lower-bound 表更能说明动力学表征。", "最后读 Table 1 与附录 Algorithm 1–2，关注 L、R 带来的计算—统计折衷，以及 tighter bound 与预测质量的不一致。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/1807.02128/figure-1-pendulum-latent-planning.webp", "label": "Figure 1", "visual_type": "comparison", "evidence": "arXiv:1807.02128v4, paper.pdf p. 8, Figure 1", "alt_text": "摆运动的二维潜空间按角度和角速度着色，并展示真实、预测及四种目标规划的图像序列。", "caption": "同一个潜在随机动力学同时组织物理状态、自由预测与目标驱动规划；红线区分观测重构和未来生成。", "selection_rationale": "Figure 1 是最关键的可视化证据，直接展示表征是否保留物理坐标以及学得动力学能否用于多目标规划，比 ELBO 数表更适合作为封面。"},
        "figure_refs": [{"label": "Figure 1", "asset_path": "assets/collection-figures/1807.02128/figure-1-pendulum-latent-planning.webp", "section": "核心结果与证据", "role": "connect latent geometry, prediction, and control-conditioned planning", "evidence": "arXiv:1807.02128v4, paper.pdf p. 8, Figure 1", "alt_text": "摆运动潜空间及图像预测与规划序列。", "caption": "左侧潜坐标按真实角度/角速度连续着色，中部显示真实、预测和四种目标规划，右侧给出目标图像。", "interpretation": "有序潜几何本身不够；同一潜 SDE 能从观测段延伸到多种低代价未来，才构成表征对规划有用的证据。"}],
        "equation_refs": [
            {"label": "Controlled latent SDE", "latex": r"dz(t)=f(z(t))dt+\sigma(z(t))\left[u(t)dt+dw(t)\right]", "role": "parameterize the variational trajectory measure", "symbols": {"z": "latent state", "f": "learned drift", "sigma": "diffusion map", "u": "variational control", "w": "Wiener process"}, "evidence": "paper.pdf p. 4, Eq. (9)", "interpretation": "Posterior refinement becomes control of the same stochastic dynamics used as the generative prior."},
            {"label": "Control-inference KL duality", "latex": r"J=D_{\mathrm{KL}}\!\left(q_u(z_{[0,T]})\Vert p^*(z_{[0,T]})\right)-\log\xi", "role": "turn approximate inference into stochastic optimal control", "symbols": {"q_u": "controlled proposal trajectory measure", "p_star": "optimal posterior-like trajectory measure", "xi": "normalization constant"}, "evidence": "paper.pdf p. 4, Eq. (11)", "interpretation": "Path-integral adaptation improves the proposal by reducing a trajectory-space KL divergence."},
        ],
        "evidence_refs": ["paper.pdf pp. 2–5: ELBO gap, controlled SDE and path-integral refinement", "paper.pdf pp. 5–6: planning objective in learned latent dynamics", "paper.pdf pp. 7–9: pendulum/mocap figures, Table 1 and qualified empirical conclusions", "paper.pdf Appendix A–C: Girsanov derivation and algorithms", "source PDF SHA-256 7bc2c9002e832405171ef4ed888e7d4853ee082584e76cde77dd97de27bad403", "Evidence status: full-text verified; no independent reproduction performed."],
    },
    {
        "arxiv_id": "1807.10425",
        "source_version": "v1",
        "source_pdf": "https://arxiv.org/pdf/1807.10425",
        "title_en": "STEAP: simultaneous trajectory estimation and planning",
        "title_zh": "STEAP：同步轨迹估计与规划",
        "curation_status": "full_text_verified",
        "card_standard_version": "2.3",
        "paper_profile": "ai_empirical",
        "style_reference": "physicist_daily_arxiv",
        "provenance": provenance("e021df620cf47de8", "Robotics"),
        "verified_metadata": {"arxiv_id": "1807.10425", "version": "v1", "title": "STEAP: simultaneous trajectory estimation and planning", "authors": ["Mustafa Mukadam", "Jing Dong", "Frank Dellaert", "Byron Boots"], "categories": ["cs.RO"], "primary_category": "cs.RO", "published": "2018-07-27T03:49:45Z", "abstract": "STEAP performs MAP inference over one continuous-time trajectory whose past is state estimation and whose future is motion planning, updating the factor graph incrementally with a Bayes tree."},
        "sections": [
            sec("作者信息", "作者：Mustafa Mukadam、Jing Dong、Frank Dellaert、Byron Boots；论文为 arXiv:1807.10425v1，主分类 cs.RO。", "本卡核对 19 页全文。证据包括二维移动机械臂、18-DOF PR2 仿真和 Vector 移动机械臂实机实验。"),
            sec("研究问题", "机器人通常先从传感器估计当前状态，再从该点规划未来；这种串联会切断未来无碰撞约束对历史估计的反馈，也会让估计误差污染规划初值。", "论文问：能否把从起点到终点的整条连续时间轨迹作为一个随机变量，在每个时刻用观测因子、障碍代价和边界条件共同做 MAP 推断，使过去部分自动成为平滑估计、未来部分自动成为重规划？"),
            sec("背景", "STEAM 用 Gaussian-process prior 和测量因子做连续时间轨迹估计；GPMP2 把障碍与起终点写成 likelihood 因子做运动规划。SLAP 虽同时运行定位和规划，却仍顺序求两个图。", "因 LTV-SDE 生成的 GP 是 Gauss–Markov 链，轨迹 prior 可分解为只连接相邻状态的稀疏因子；Bayes tree 又允许新测量只重线性化受影响的 cliques。"),
            sec("模型与方法", r"统一后验因子分解为 \(p(\boldsymbol\theta\mid e)\propto f^{gp}f^{meas}f^{obs}f^{fix}\)：GP prior 约束平滑动力学，测量因子约束已执行历史，障碍因子作用于整条轨迹，起点/目标因子固定边界。", "每一步先用 GP 插值执行短轨迹段并做碰撞检查，再加入新测量因子；Bayes tree 只重新消元被新因子触及的上层子树，未受影响的条件结构直接复用。", "算法在 SE(2)×R^n 的移动机械臂构型空间上使用局部 LTV-SDE prior，并以 signed-distance-field hinge loss 建模碰撞；比较 open loop、顺序 SLAP 与联合 STEAP。"),
            sec("核心结果与证据", "Figure 3 是机制核心：随着当前时刻从 t0 移到 t4，左侧因子图逐步加入测量，右侧红色历史估计与蓝色未来规划在同一 MAP 轨迹上同步更新，绿色真实轨迹用于解释执行噪声。", "二维仿真中 STEAP 在不同动力学/相机噪声下普遍提高成功率并降低目标与估计误差。18-DOF PR2 仿真中，平均每步约 17 ms，而 SLAP 约 130 ms；优势来自增量 Bayes-tree 更新而非每步全图重算。", "实机两个任务各 10 次：open-loop 均为 0/10，STEAP 为 9/10 与 10/10，总成功率 95%；轨迹估计误差相对原始定位约降低 50–60%。这些结果只覆盖已知静态环境。", "联合图允许信息双向流：已安全走过的路径与障碍因子抑制不合理历史估计，更准的当前状态又改善未来轨迹。"),
            sec("有效性与局限", "当前系统要求已知静态地图并预计算 signed distance field；动态环境需在线建图、动态障碍跟踪和增量距离场，可能成为主要瓶颈。", "实现面向 holonomic 系统，不直接支持非完整与硬不等式约束；软因子只能近似速度/构型限制。", "MAP 轨迹优化是局部方法，在拥挤或迷宫环境中可能落入碰撞局部极小；Bayes-tree 增量推断缺少与批量多初值同等成熟的逃逸机制。", "实机只有两个任务、20 次运行，地图、机器人和传感器固定；95% 不能外推到开放动态场景。有限 horizon 还造成目标附近越界后没有足够步数恢复。"),
            sec("复现与资源", "原文：https://arxiv.org/abs/1807.10425；PDF：https://arxiv.org/pdf/1807.10425；论文说明 GPMP2/STEAP 代码已开源并给出实验视频链接。", "全文 PDF 共 19 页，SHA-256：e021df620cf47de87bf7e9380d9aa72c53088a28a2d326cde8c1f48c960fd88e。", "复现需固定任务、噪声强度、图状态数、GP 插值密度、SDF 分辨率与变量消元顺序；分别保存成功率、目标误差、完整轨迹估计误差以及每步增量更新时间分布。", "Evidence status: full-text verified; no independent reproduction performed."),
            sec("阅读指南", "先看 Figure 2 和 Table 1，把 STEAM、GPMP2、SLAP 与 STEAP 的因子集合对应起来。", "再逐行读 Figure 3 与 Algorithm 1：红色历史、蓝色未来和新增测量因子共同说明“同步”不是并行运行两个模块。", "最后核对 Tables 2–4 与 Sec. 10；把仿真噪声鲁棒性、实机成功率、实时性和已知静态地图限制分别评价。"),
        ],
        "cover": {"mode": "source_figure", "asset_path": "assets/collection-figures/1807.10425/figure-3-steap-loop.webp", "label": "Figure 3", "visual_type": "schematic", "evidence": "arXiv:1807.10425v1, paper.pdf p. 7, Figure 3", "alt_text": "五个时间步的 STEAP 因子图及机器人环境轨迹，分别显示真实、估计和重规划路径。", "caption": "每次新测量同时修正红色历史估计和蓝色未来规划；左侧因子图展示同一连续轨迹后验如何增量更新。", "selection_rationale": "Figure 3 直接可视化论文最重要的联合推断机制，比成功率表更能解释为何估计与规划会相互改善。"},
        "figure_refs": [{"label": "Figure 3", "asset_path": "assets/collection-figures/1807.10425/figure-3-steap-loop.webp", "section": "核心结果与证据", "role": "visualize joint past estimation and future replanning over one factor graph", "evidence": "arXiv:1807.10425v1, paper.pdf p. 7, Figure 3", "alt_text": "STEAP 从 t0 到 t4 的因子图和真实、估计、规划轨迹。", "caption": "灰色节点推进时测量因子逐步加入，过去轨迹变红、未来轨迹保持蓝色并反复重规划。", "interpretation": "联合后验不是简单拼接定位器和规划器；同一因子图使障碍信息约束历史，传感器信息约束未来。"}],
        "equation_refs": [
            {"label": "STEAP posterior factorization", "latex": r"p(\boldsymbol\theta\mid e)\propto f^{\mathrm{gp}}f^{\mathrm{meas}}f^{\mathrm{obs}}f^{\mathrm{fix}}", "role": "combine dynamics, sensing, collision costs, and boundary conditions", "symbols": {"theta": "full continuous-time trajectory", "e": "all events and evidence", "f_gp": "Gaussian-process prior factors", "f_meas": "measurement factors", "f_obs": "obstacle factors", "f_fix": "start and goal factors"}, "evidence": "paper.pdf p. 5, Eq. (19)", "interpretation": "Past estimation and future planning are two portions of one MAP trajectory conditioned on all information."},
            {"label": "Sparse GP prior", "latex": r"f^{\mathrm{gp}}=\prod_i f_i^{\mathrm{gp}}(\theta_i,\theta_{i+1})", "role": "make continuous-time trajectory inference sparse", "symbols": {"theta_i": "support state at time i", "f_i_gp": "neighboring-state Gaussian-process factor"}, "evidence": "paper.pdf p. 6, Eq. (20)", "interpretation": "The Gauss–Markov chain permits local Bayes-tree updates instead of dense full-trajectory recomputation."},
        ],
        "evidence_refs": ["paper.pdf pp. 3–7: probabilistic inference, factorization and Figure 3 mechanism", "paper.pdf pp. 8–13: Bayes-tree incremental inference and implementation", "paper.pdf pp. 14–17: planar, PR2 and real-robot quantitative evidence", "paper.pdf pp. 17–18: known-map, holonomic and local-minimum limitations", "source PDF SHA-256 e021df620cf47de87bf7e9380d9aa72c53088a28a2d326cde8c1f48c960fd88e", "Evidence status: full-text verified; no independent reproduction performed."],
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for card in CARDS:
        path = OUT / f"{card['arxiv_id']}.json"
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing card: {path}")
        path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        installed.append(str(card["arxiv_id"]))
    print(json.dumps({"installed": installed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
