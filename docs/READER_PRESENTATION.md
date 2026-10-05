# Reader presentation revision — 2026-10-05

The user requested one “论文卡” catalog with Daily (five contiguous calendar days
per page), publication-date and research-category (approximately ten papers per page,
rounded up to a whole number of responsive grid rows) views. Search, consolidated subject tags and existing S/A/B grades intersect.
The catalog consolidates 138 original tags into 21 reader subjects and displays
at most three subjects per card, plus its existing grade. Original fine tags remain searchable and continue to resolve old filtered links.
Pagination includes first/previous/numbered/next/last pages and a page selector.
Unrated historical cards remain visible in All. Filters do not broaden admission
or turn unreviewed records into cards.

Daily and Collection production records, grades, evidence, feeds and detail URLs
remain independent. `assets/all-data.json` merges only reader-facing rows by work
identity, retaining source aliases and independent grade/date records. Existing
favorite keys and comments continue to resolve. All three old catalog entry URLs
render the same interface without redirecting away URL state.

`scripts/card_presentation.py` derives Chinese previews from existing Chinese
abstract/problem content, never from author production notes. It uses complete
sentences and does not clip mathematical expressions. Verified authors, journal
and numbering replace the detailed production metadata in the hero. The original
author/provenance section remains in scientific JSON; its duplicate reader-facing
section is omitted. Scientific methods, results, equations, evidence locators and
validity boundaries remain in the article.

## Reviewed cover revisions

The user's explicit request supersedes the previous typography-only fallback:
prefer meaningful original schematic/visualization figures; where none is useful,
use an actual excerpt of the source title and abstract. Existing card decisions
and historical review receipts remain intact.

The renderer reads `data/cover_overrides_legacy.json` and
`data/cover_overrides_structured.json`. Each override, keyed by `Program:card_id`
or an unambiguous card ID, declares `mode` (`source_figure` or `source_excerpt`),
`asset_path` under `assets/reader-covers/`, `label`, `evidence`, `alt_text`,
`caption`, and a source PDF hash/version where available. Assets live in
`data/reader-covers/`; build copies them into the site. Private source paths belong
only in local review receipts. A source excerpt must not be called a scientific
figure, a download failure must not be described as no figures, and attribution
does not grant or claim a new license on source material.

New cover overrides require actual source comparison and readable complete
panels, axes and legends. Feed, detail hero and standalone cover use the same
reviewed override. The builder rejects invalid modes, escaping paths, missing
assets or attribution fields. Frozen scientific JSON is not rewritten merely to
change presentation. New card production still follows the canonical scientific
standard and admission rules.

## Validation

Run standard synchronization, Python tests, deterministic build, card validation,
production build and browser interaction checks. Check pagination boundaries,
unknown dates, intersecting filters, back/forward state, images, modal/detail
navigation, favorites, local MathJax and narrow-screen overflow. A local preview
is not a public release; publish only when separately requested.
