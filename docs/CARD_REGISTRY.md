# Cross-campaign paper disposition registry

The private durable registry lives at workspace `local-state/paper-card-registry/`.
It records papers not carded as well as existing cards, so a later campaign can
reuse evidence instead of repeating work. Keep it outside all Git repositories;
never publish its private evidence paths or source PDFs. SQLite events are
append-only with unique event IDs, payload hashes, FULL synchronization and
UPDATE/DELETE rejection. JSON/Markdown lists are replaceable derived snapshots.

## Before any claim, download or new card

```bash
python3 scripts/card_batch.py registry lookup --id 2609.00399v1 --program Daily
python3 scripts/card_batch.py registry lookup --id 2609.00867 --program Daily
python3 scripts/card_batch.py registry lookup --id doi:10.1103/PhysRevLett.135.187402 --program Collection
python3 scripts/card_batch.py registry lookup --title 'Exact paper title' --program Collection
```

`--registry /absolute/private-registry` overrides the workspace default. For
arXiv use the versionless work ID plus exact version; DOI comparison is case
insensitive. Preserve old-style arXiv IDs and verified stable Collection aliases.
Title normalization is a lookup aid; conflicting identities require manual
resolution, never automatic merging by similar titles.

- Existing card: reuse it or make an authorized revision; do not create a duplicate.
- Same-program prior disposition: skip repeated reading/card writing. Unknown
  reviewed versions remain unknown and require comparison with the saved evidence.
- Changed version: a review candidate, never automatic permission to download or restart.
- Staged, blocked, incomplete, or active unit: inspect and resume its existing evidence
  only when authorized, after confirming actual worker/process ownership.
- Unstarted/stopped: retain the stop decision until explicit scope authorization changes.
- Other-program record: preserve independent Daily/Collection eligibility. A Daily
  A/B outcome alone does not reject a Collection card. Reuse its evidence. An unresolved
  source exception or active owner in another program requires review before any claim.
- Not recorded: means no disposition found, not authorization to process the paper.

The registry prevents accidental repetition; it is not a paper-quality blacklist
or a scientific reviewer. Importing a checkpoint does not upgrade diagnostic
scores to final grades, infer a source version, or prove that a printed theorem
is false. Existing `withheld` states lacking an explicit disposition remain
`needs_review`, with their original reason and evidence.

## Always record the parent conclusion

Workers' proposals are not final dispositions. After parent scientific acceptance:

```bash
python3 scripts/card_batch.py registry accept --decision /absolute/parent-decision.json
```

The parent decision must contain `key`, `decision`, `scientific_acceptance: true`,
a hash-bound `receipt`, and a concrete `boundary` or `source_issue`. Preserve
`source_version`, title, grade/score if established, and `reopen_condition`.
Accepted decisions are `accepted_not_selected`, `accepted_source_exception`,
`accepted_staged`, or `accepted_for_release`. Staged acceptance is not publication.
A prior existing-card status is retained while its new review disposition is logged.
Do not infer publication from a worker, acceptance receipt or build.

For other completed dispositions, `registry record --input /absolute/record.json`
accepts one record or a list. Required fields: `paper_id`, `program`, `status`,
`reason`, `evidence` (named absolute path / SHA-256 references). Also retain
`source_version` (null if unknown), `title`, `reopen_condition`, and separate
formal/diagnostic scores. Supported statuses are `not_selected`,
`source_exception`, `incomplete`, `stopped_unstarted`, `staged_unpublished`,
`publication_blocked`, `has_card`, `in_progress`, and `needs_review`. Record a
new event for corrected evidence; never edit or delete the old conclusion.

## Automatic workflow integration and recovery

New `workflow init` journals bind the workspace registry by default, or an
explicit `--registry`. A missing registry fails closed. The `claimed` transition
checks prior dispositions and current source-card presence. Claimed/draft/sealed/
published and terminal no-card transitions append registry records automatically.
The `context packet` CLI checks the registry before preparing a new worker unit;
existing staged units remain available for scoped correction/review. A prepared
packet never authorizes execution. Python helper calls used by tests/importers
must explicitly bind their registry; they do not alter global state by default.

The workflow journal and SQLite registry are separate durable stores, not one
atomic transaction. If the journal commits but the registry update fails,
preserve both and repair idempotently:

```bash
python3 scripts/card_batch.py workflow sync-registry --state /absolute/current-journal
```

An old unbound journal must use `registry record/accept` to import its conclusions;
do not rewrite its initialization event. Registry state is not a cross-campaign
process lock: retain the single controller and check active owners before recovery.
Evidence pointers must refer to immutable receipts or artifact revisions.

At each accepted batch boundary or closeout, export the current list once:

```bash
python3 scripts/card_batch.py registry export
```

Outputs: `no-card-current.json` and `no-card-current.md`. Counts are per program
and distinguish scientific non-selection, source issues, unresolved dispositions,
publication blockers and unstarted scope. They are not all scientific rejections. Per the user decision of 2026-10-02,
Daily `not_selected` outcomes without a card are ignored in this current view
and its counts; their immutable history remains available to lookup/claim guards.
The snapshot reports the ignored count separately. Collection non-selection,
source exceptions, withheld states and publication blockers are separate records
and are not hidden by this Daily S-threshold view rule.
The database records immediately; the human list is refreshed at batch boundaries.
Refresh current card inventory after every release to supersede stale no-card
records and retain exact title/version/source-card hashes.

## Historical reconciliation performed 2026-10-02

The initial import reads the frozen September 26–29 overlay and corrected stop
receipt, subsequent September 30 manifest/accepted decisions and saved worker
receipts, current Daily/Collection source cards, and catalog/nomination metadata.
The import script and hash-backed receipt are local in the registry directory.
It downloads or reads no new paper and preserves the old campaign files.
The current list covers those checkpointed campaigns, not every paper ever
encountered or every unrecorded automation. Missing historical decisions require
an explicit evidence import; they must not be silently invented.
