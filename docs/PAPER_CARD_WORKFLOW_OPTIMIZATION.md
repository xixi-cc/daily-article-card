# Paper Card production workflow

This workflow reduces repeated context loading and validation overhead without
lowering the scientific standard. The source PDF and matching TeX remain the
authority. MinerU output, compact evidence, scaffolds, and audit reports are
working aids.

## Evidence layers

Split an existing full evidence packet into a compact first-read layer and
lossless supplements:

```bash
python3 scripts/paper_card_evidence_layers.py \
  local-state/work-in-progress/<id>/evidence_packet.json \
  local-state/work-in-progress/<id>/evidence_layers \
  --target-tokens 5000
```

The command writes:

- `core.json`: metadata, quality boundary, decisive page evidence, captions,
  quantitative signals, and explicit reading routes;
- `supplements/equations.json`: MinerU equation candidates for discovery;
- `supplements/figures.json`: captions and extracted image candidates;
- `supplements/structure.json`: headings, sections, and full page-evidence map;
- `supplements/full_packet.json`: byte-for-byte copy of the original packet;
- `manifest.json`: hashes and sizes for every layer.

Read `core.json` first, then every artifact named by `required_on_demand`.
Always use the full packet and source PDF or TeX for final claim, equation,
number, and figure verification. The token target is a routing budget, not a
license to omit evidence.

## Deterministic draft scaffold

Create a provenance-aware draft before scientific writing:

```bash
python3 scripts/create_paper_card_scaffold.py \
  --metadata metadata.json \
  --program Collection \
  --paper-profile theory_numerics \
  --title-zh '中文标题' \
  --provenance provenance.json \
  --output local-state/work-in-progress/<id>/card_draft.json
```

For Daily, replace `--provenance` with `--selection-record`; the scaffold
accepts only the current direct-arXiv S-grade provenance. The output remains a
draft and cannot replace full-text review, page-level evidence, visual figure
inspection, or repository validation.

## Stage metrics and risk routing

Measure extraction, evidence, writing, review, and validation separately:

```bash
python3 scripts/paper_card_metrics.py start \
  --receipt local-state/work-in-progress/<id>/metrics.json \
  --card-id <id> --stage evidence

python3 scripts/paper_card_metrics.py finish \
  --receipt local-state/work-in-progress/<id>/metrics.json \
  --card-id <id> --stage evidence --status passed \
  --input-tokens 0 --output-tokens 0 \
  --artifact packet=local-state/work-in-progress/<id>/evidence_packet.json
```

Run a structural risk audit before and after a campaign:

```bash
python3 scripts/paper_card_metrics.py audit \
  --cards-dir data/curated_cards \
  --cards-dir data/collection_cards \
  --packet-root local-state/work-in-progress \
  --output local-state/work-in-progress/paper-card-risk-audit.json
```

Risk flags identify cards that need more attention, including legacy schema,
thin prose, minimum evidence, theory cards without equation review, large
packets, and long papers. They do not establish a scientific error or replace
the canonical validator.

## Batch boundary

Use authoring units of two or three cards so that context remains paper
specific. After each card, parse its JSON and run the cheapest relevant checks.
Amortize deterministic site build and full repository validation across at most
ten completed cards, or earlier when risk flags or visible assets warrant it.

Keep GPU extraction and TTS serialization rules separate from writing batch
size. Do not start asynchronous prefetch, concurrent MinerU calls, or parallel
writers unless the campaign explicitly authorizes them. Figure candidates may
be collected mechanically, but the chosen cover still requires visual review
against the source PDF.
