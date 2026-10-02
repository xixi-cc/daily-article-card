# Incremental state and stage measurements

Use `python3 scripts/card_batch.py workflow` for controller-owned logistics.
This complements `context` (short per-paper handoffs), `delivery` (pre-install
contract checks), and `browser` (changed-page acceptance). It does not download,
read, dispatch, grade, install, build or publish papers. Scientific acceptance
still follows the complete canonical Paper Card Standard.

## Scope and ownership

The current user decision stops all unstarted papers. This tool has no intake
resume or roster-expansion command. Import only an explicitly checked roster;
mark every unstarted item `already_started: false`. An existing PDF/checkpoint
is necessary evidence of started work; a metadata-only item remains subject to
the user's narrower scope and must not be promoted merely by importing it.
Keep the old campaign/overlays/stop receipts unchanged. New runtime output goes
to a new directory under workspace `local-state/`, outside production and frozen
campaign directories. Do not import an old queue automatically.

Only the parent writes this journal. Workers return immutable per-paper result
and evidence pointers through the existing `context receipt` flow. The Linux
file lock excludes simultaneous journal writers; it is not an agent/process
ownership registry. Check live agent/job identity before recovery. Keep fresh
one-paper workers, at most two active units, and one integrator.

Create `roster.json` with absolute local paths (illustrative keys only):

```json
{
  "authority": {"scope": "/absolute/user-scope-checkpoint.json"},
  "policy": {"max_active": 2, "max_batch": 10},
  "rows": [
    {"key": "Daily:2609.00001", "already_started": true,
     "source_version": "v1", "stage": "registered",
     "artifacts": {"checkpoint": "/absolute/existing-unit/checkpoint.json"}},
    {"key": "Collection:2608.00001", "already_started": false}
  ]
}
```

```bash
python3 scripts/card_batch.py workflow init --state /absolute/new-runtime --input /absolute/roster.json
```

Scope authority hashes are rechecked before each mutation; a changed scope
requires a new explicit ledger. All rows are frozen at initialization; there is no new-paper registration.
The parent may import an evidenced existing stage to avoid repeating completed
work. Importing is a logistical assertion, not an independent scientific audit.
Unstarted rows can never transition or receive measurements. Versionless IDs
identify works; Daily and Collection retain distinct keys/provenance. Resolve
ID/version/title conflicts with existing intake and delivery tools, rather than
using this ledger to equate incompatible versions.

## Per-paper events instead of full overlays

The stage chain is `registered -> claimed -> pdf_frozen -> fulltext_read ->
evidence_verified -> draft -> reviewed -> sealed -> published`. At any unfinished
stage a paper may end as `not_selected`, `source_exception`, or
`unable_to_finish`, with an explicit conclusion and durable evidence. Terminal
items cannot be reopened through this tool. A correction requires an explicitly
authorized new revision ledger with pointers to its predecessor; do not rewrite
old evidence. `sealed` releases a working slot, but is not publication proof.

```json
{
  "key": "Daily:2609.00001", "stage": "draft",
  "note": "Draft checkpoint; contract check saved, scientific review pending.",
  "artifacts": {"draft": "/absolute/unit/card.json",
                "delivery": "/absolute/unit/delivery.json"}
}
```

```bash
python3 scripts/card_batch.py workflow transition --state /absolute/new-runtime --input /absolute/event.json
python3 scripts/card_batch.py workflow report --state /absolute/new-runtime --out /absolute/batch-01-summary.json
python3 scripts/card_batch.py workflow audit --state /absolute/new-runtime --out /absolute/batch-01-integrity.json
python3 scripts/card_batch.py workflow batch --state /absolute/new-runtime --out /absolute/batch-01-proposal.json
```

`events.jsonl` contains only small events with artifact hashes, a sequence and
hash chain. Each write is locked, flushed and fsynced. Reports replay events;
write summaries once at batch boundaries, not after every paper event. Existing
snapshots are not overwritten. A broken/truncated journal fails closed; preserve
it for diagnosis and recover from a verified journal copy rather than silently
ignoring its tail. Hashes detect corruption, not malicious re-signing. `audit` verifies all referenced artifact hashes; batch proposals also verify
current sealed receipts. References are hashed once per event, not embedded in
the journal. Referenced
artifacts remain the source evidence and must stay immutable; stage labels alone
are not sufficient to accept them.

## Measured cost, with unknowns preserved

Save a runtime timing/usage receipt, then import one interval delta:

```json
{
  "key": "Daily:2609.00001", "measurement_id": "unit-01-reading-01",
  "stage": "reading", "started_at": "2026-10-02T01:00:00+08:00",
  "ended_at": "2026-10-02T01:10:00+08:00",
  "usage": {"input_tokens": null, "cached_input_tokens": null, "output_tokens": null},
  "artifacts": {"runtime_receipt": "/absolute/unit/reading-usage.json"}
}
```

```bash
python3 scripts/card_batch.py workflow measurement --state /absolute/new-runtime --input /absolute/measurement.json
```

Use `report --key Daily:2609.00001` for per-paper stage totals.

Stages: extraction, reading, evidence, writing, review, validation, publication.
Use unique measurement IDs, interval deltas, nonoverlapping usage sources and
explicit timezone timestamps. Do not feed the same cumulative runtime counter
at every stage. Input means **total input including cached input**; cached input
is its subset. When all three fields exist, the report computes
`input - cached_input + output` as an audit proxy. Missing fields stay unknown,
with counts and known subtotals; they never become a complete zero-cost total.
Do not equate this proxy with Goal tokens, money or account quota percentage.

Reports separately show summed measured elapsed intervals and their union in
wall-clock time for each stage. Neither represents human labor, CPU time, queue
waiting, or whole-campaign duration. Parallel stage unions must not be added as
a campaign wall time. Historic file mtimes cannot reconstruct these measurements.
Record rework as a new uniquely named measurement with a new source receipt.

## Review and release without repeated work

Run `delivery` against each completed draft before sealing. Store its immutable
receipt alongside scientific review and source/figure checks. Changed card,
source/version, assets, evidence, standard or validators invalidates relevant
acceptance: correct only that paper, then make new receipts. There is no blanket
cache that treats a prior mechanical pass as a scientific certification.

Accumulate at most ten accepted cards per deterministic validation batch. The
`batch` command proposes sealed keys only; the parent verifies acceptance,
installs cards, runs the full required build/validator, checks changed detail
pages at desktop/mobile widths and every new figure, then verifies deployment
and URLs. Do not repeat passed unchanged-page browser scans. Published stage
requires the actual release/live receipt; it must never be set from a build
alone. Exceptions do not block independent accepted cards.

Before claiming savings, compare measured small batches with comparable paper
complexity and review requirements: stage times, known/unknown token counts,
context sizes, rework and acceptance outcomes. Synthetic tests verify accounting
and recovery; they cannot establish an actual percentage saving.

## Cross-campaign repetition guard

New CLI journals bind the private registry automatically; see
[CARD_REGISTRY](CARD_REGISTRY.md). Claims check previous dispositions and existing
cards; terminal outcomes are recorded immediately. After a batch, export the
current no-card list once. Repair a partial registry write with `sync-registry`,
without repeating the scientific work. Legacy unbound journals stay immutable.
