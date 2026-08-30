# Ziming Liu Collection MinerU Serial Paper Card Plan

Status: **authorized for local serial execution in Goal mode**

Frozen: 2026-08-31 (Asia/Shanghai)
Catalog SHA-256: `9acb9bd5d88fa12758123eaee075e266f3413913f1fb3ed143fb2e2002fae5ad`

## Scope and boundaries

- Source catalog: 916 records.
- Ziming Liu Paper Collection: 472 records and 472 unique works.
- Existing Collection cards: 8.
- Pending cards: 464, all normalized to arXiv sources.
- Run on the current local computer only. Do not use `office-ubuntu`.
- Process exactly one paper at a time. Do not run parallel extraction or card workers.
- Group ten serially processed papers into one micro-batch to amortize builds and validation.
- Keep Collection provenance. Do not assign Daily dates, grades, or notifications.
- Upload only official public arXiv PDFs to the configured MinerU Open API.
- Do not upload local or private documents.
- Build and validate locally. Do not push, deploy, or publish without separate authorization.

## Fixed serial data flow

For each leased campaign item:

1. Download the official versioned arXiv PDF and record URL, version, bytes, and SHA-256.
2. Submit the public PDF to MinerU Open API with English parsing and server model `auto`.
3. Preserve MinerU Markdown and extracted images as structured reading aids.
4. Independently extract page-delimited PDF text and create a page index.
5. Build a compact evidence packet containing verified metadata, page-addressable methods,
   results, conclusions, limitations, selected equations, captions, quantitative claims,
   resources, and the PDF hash.
6. Generate one staged Paper Card from that packet.
7. Reopen the source PDF or arXiv TeX for every published equation, ambiguous symbol, key
   quantitative claim, and selected figure.
8. Run the cheap per-card JSON and evidence checks, then leave the card staged while the next
   paper in the ten-paper micro-batch is processed.
9. After ten staged cards, use the single writer to install them, run the complete strict
   validation and site build once, and append a receipt for every card plus one batch receipt.

The campaign ledger records `pending`, `extracting`, `packet_ready`, `card_staged`,
`card_installed`, or `blocked` so an interruption never requires restarting completed papers.

## Token and scientific-quality contract

- Target compact packet: at most about 8,000 approximate input tokens, excluding a separately
  opened source page or image needed for verification.
- Do not truncate methods, results, or limitations merely to meet the target; mark the packet
  oversized and route it through a smaller page-bounded review.
- MinerU is not equation authority. The source PDF is visual authority; matching arXiv TeX,
  when available, is equation/table/caption authority.
- Each card needs at least three non-overlapping page-addressable evidence references covering
  methods, results, and limitations or resources.
- End the ledger with `full-text verified; no independent reproduction performed` unless a real
  reproduction was completed.
- Structural validation is not scientific validation.

## Checkpoints

- Process one paper at a time; batching does not permit concurrent MinerU or card workers.
- Run per-card JSON, required-section, evidence-reference, and asset checks before staging.
- Install at most ten staged cards through the single writer.
- Run Paper Card Standard synchronization, all unit tests, strict Collection validation, the
  local site build, and `git diff --check` once at the end of every five-card micro-batch.
- Save one receipt per card, one batch receipt, and one local commit after that batch passes.
- Stop immediately on ambiguous arXiv identity, corrupt PDF, MinerU authentication/rate-limit
  failure, unresolved formula corruption, or an unexpected tracked-worktree change.
- Preserve failed evidence and mark the item `blocked`; never silently downgrade a card to an
  abstract-only summary.

## Representative extraction benchmark

Exactly three authorized public-paper extraction samples were completed before bulk execution;
no Paper Cards were generated from them.

| arXiv | Pages | Raw text approx. tokens | MinerU Markdown approx. tokens | Result |
|---|---:|---:|---:|---|
| `1901.09813` | 11 | 19,457 | 17,418 | Strong structure; some symbol/spacing errors. |
| `2404.14265` | 13 | 15,365 | 12,529 | Equations and sections retained; exact math requires source check. |
| `2608.18419` | 11 | 16,011 | 12,392 | Figures/algorithm retained; malformed RoPE symbols observed. |

MinerU improved structure and modestly reduced complete-text size. The larger token saving must
come from the compact evidence packet, not from MinerU alone.

## Completion condition

The Goal is complete only when all 464 unique works are either installed as full-text-verified
Collection cards or explicitly recorded as blocked with evidence, and the complete local tree
passes Paper Card Standard synchronization, unit tests, strict Collection validation, site
build, and `git diff --check`. Publication remains a separate decision.
