# Codex Daily Screening and Publication Contract

Version: 1.0
Effective date: 2026-08-25
Status: canonical

Codex owns the complete Daily workflow: arXiv discovery, scientific screening, full-text card curation, repository mutation, deployment, and public verification. The ChatGPT task `arXiv 物理与AI日报` is no longer an input, gate, or authority for this pipeline.

## 1. Daily batch boundary

- Use Asia/Shanghai report dates and the latest stable arXiv daily listing as the batch boundary; do not use a rolling 24-hour window.
- Search primary new submissions in `cs.LG`, `cs.AI`, `cs.CL`, `cs.RO`, `stat.ML`, `math.PR`, `math.AP`, `cond-mat.stat-mech`, `cond-mat.soft`, and `nlin`.
- Run targeted supplementary scans of `cs.IT`, `cs.CV`, `cs.NE`, `cs.SY`, and `physics.comp-ph` when they contain work relevant to foundations of AI, physics of AI, AI for physics, stochastic dynamics, field theory, statistical mechanics, or embodied/world-model theory.
- Count primary new submissions once. Use cross-lists for discovery but do not double-count them. Exclude replacements and withdrawals from the new-paper count while recording relevant status changes.
- If no new stable listing is available, write a no-new-batch terminal record and make no repository change.

## 2. Reproducible screening

For every batch, save an append-only search log, candidate inventory, score sheet, selected-paper manifest, and terminal status under `automation_outputs/arxiv_daily_cards/`.

Screen in two stages:

1. Inspect authoritative metadata and abstracts for the complete batch. Record inclusion/exclusion reasons; do not select by keyword alone.
2. Retrieve and inspect the full text of every plausible S candidate before assigning the final S grade. A title or abstract can nominate a candidate but cannot establish an S-grade technical claim.

Deduplicate by versionless arXiv ID. Check corrections, withdrawals, and version changes before publication.

## 3. Research taste and 40-point rubric

Score each serious candidate from 0 to 5 on eight axes:

1. fundamental theoretical insight;
2. mathematical depth and rigor;
3. physics content and physical interpretability;
4. relevance to foundations or mechanisms of modern AI;
5. universality, correct state variables, or cross-regime explanatory power;
6. originality of formulation rather than benchmark increment;
7. fit with the user's research directions;
8. long-term scientific value.

Use the total only as a necessary guide:

- `S`: normally 34–40, and must contain a genuinely load-bearing theoretical, mechanistic, mathematical, or formulation-level contribution. A high sum from broad relevance alone is insufficient.
- `A`: normally 28–33, worth following but not published to the Daily card site.
- `B` or lower: do not publish.

There is no quota. S may be zero. Never promote a paper to fill a daily target.

Highest priority:

- foundations and first-principles explanations of modern AI;
- identification of correct degrees of freedom, sufficient states, latent dynamics, operators, probability flows, generators, path measures, or information-theoretic variables;
- training, representation, optimizer, world-model, or agent dynamics with a concrete mechanism;
- stability, failure modes, causal/interventional capability, memory, scaling, emergence, and universality;
- rigorous statistical mechanics, stochastic processes, SPDEs, nonequilibrium response, field theory, active matter, and mathematical structures that can inform AI without relying on superficial analogy.

Deprioritize benchmark-only gains, generic architecture variants, keyword-level physics analogies, ungrounded position pieces, and engineering improvements without a durable mechanism or formulation.

## 4. Selection-note voice

Write each final S assessment in the user's preferred Daily arXiv style:

- `Core question`: the sharp problem or conceptual confusion.
- `Core idea`: the minimal model/equation chain and central mechanism.
- `Theoretical framework`: the mathematical and physical objects actually used.
- `Why it fits`: which research taste criterion it satisfies.
- `Why it matters`: only the concrete change in formulation, prediction, or capability.
- `Critical assessment`: idealizations, missing controls, finite regimes, and alternative explanations.
- `Reading priority`: decisive theorem, equation, figure, or experiment.

Use this note as an editorial scaffold for the card, not as claim evidence. Recheck every card statement against the paper.

## 5. Card production and publication

- Follow the current canonical `docs/PAPER_CARD_STANDARD.md`; new cards must use version 2.4 or later.
- Download the official PDF to ignored temporary or automation-output storage and preserve it unchanged.
- Build page-addressable full-text evidence before writing card prose.
- New Daily cards must set `card_standard_version`, `audience_profile`, `paper_profile`, `style_reference`, `selection_record`, `verified_metadata`, `equation_refs`, `figure_refs`, `cover`, `sections`, and `evidence_refs` according to the standard. Their reader bridge must make the input-to-observable chain understandable to an AI-literate physicist without specialist model-training experience.
- Select the cover only after full-text review: prefer the most important physical visualization over a data plot; when no meaningful source figure exists, render the exact title plus a faithful condensed abstract.
- Render only S papers. Preserve A/B score sheets in automation evidence but do not add them to `papers.md` or the public site.
- Treat one listing as an atomic publication unit. If runtime is insufficient, preserve completed evidence and resume without regenerating verified work.
- Run all structural, equation, cover-priority, figure-path, browser-rendering, deterministic build, unique-ID, and JSON/render parity checks before commit.
- Every completed website update must be pushed to GitHub `origin` without force. Verify that local `HEAD` equals the target GitHub branch SHA, verify GitHub Actions and Pages, then fetch the public index and every new detail URL. A Sites-only deployment never completes publication.

## 6. Fail closed

Stop before mutation when the listing is incomplete, full text is unavailable, metadata conflicts, scientific evidence is insufficient for S, the card fails the equation/style standard, the worktree contains unrelated changes that cannot be isolated, credentials fail, a push is ambiguous, or deployment/public verification is not conclusive. Record the exact boundary and retain append-only evidence.

Do not use ChatGPT reports, ModelScope, or any external LLM API as a hidden upstream decision maker. Codex must own and record the selection judgment itself.
