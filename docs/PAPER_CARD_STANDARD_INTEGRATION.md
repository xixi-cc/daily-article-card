# Paper Card Standard Integration

Current required version: 2.4

`docs/PAPER_CARD_STANDARD.md` is the single source of truth for every new physics+AI paper card. This file records the active consumers so that a standard revision is not considered complete until each one is synchronized.

## Active consumers

| Consumer | Responsibility | v2.4 requirement |
| --- | --- | --- |
| Codex `arxiv-daily` automation | Discover, screen, write, validate, and publish Daily cards | Read all three canonical documents before mutation; create only v2.4-or-later cards |
| `docs/CODEX_DAILY_SCREENING_AND_PUBLICATION.md` | Daily eligibility and publication contract | Require the non-specialist-physicist reader bridge, structured equations and figures, and the cover ladder |
| `data/curated_cards/*.json` | Daily card sources | New cards include `card_standard_version`, `audience_profile`, the reader-bridge section, `equation_refs`, `figure_refs`, and `cover` |
| `data/collection_cards/*.json` | Collection card sources | New or substantively revised cards follow the same card standard but retain Collection provenance |
| `scripts/validate_paper_cards.py` | Structural and evidence gate | Require the v2.4 audience declaration and reader bridge; reject malformed covers, unresolved figure assets, and raw or unbalanced TeX |
| `scripts/paper_card_evidence_layers.py` | Lossless evidence routing | Keep an exact full packet while providing a bounded core and explicit on-demand reading routes |
| `scripts/create_paper_card_scaffold.py` | Deterministic draft initialization | Create only provenance-aware v2.4 drafts with the reader bridge; never mark them installable or scientifically verified |
| `scripts/paper_card_metrics.py` | Stage measurement and risk routing | Record duration, token, and artifact hashes; route review without treating heuristics as scientific verdicts |
| `scripts/build_site.py` and `scripts/math_typography.py` | Feed, detail page, and standalone cover renderer | Derive all three surfaces from the same structured `cover` record, normalize unmistakable inline notation, and package local MathJax |
| `.github/workflows/deploy.yml` | GitHub Pages build gate | Run the synchronization check and card validator before deployment |
| GitHub `origin` | Canonical public source and Pages trigger | Every completed website update must be pushed without force and local `HEAD` must equal the target branch SHA |
| OpenAI Sites project | Owner-only hosted copy | Publish the same generated site after a validated repository change |

## Propagation rule

When the canonical standard version changes, update the Daily contract, automation prompt, validator, renderer when schema changes require it, tests, this matrix, and deployment workflow in the same bounded change. Run:

```bash
python3 scripts/check_card_standard_sync.py
python3 scripts/build_site.py
python3 scripts/validate_paper_cards.py
python3 -m unittest discover -s tests -q
npm run build
```

Historical cards retain their recorded version until they are substantively revised. Historical automation outputs, receipts, and release archives are append-only evidence and must not be rewritten merely to change the current standard. The separate Paper Collection catalog is an intake source, not a Paper Card renderer; only cards promoted into this repository's Collection data flow are governed here.

GitHub synchronization is a permanent publication invariant, not a one-time migration step. A Sites deployment does not complete an update unless the same validated source has also been committed and pushed to GitHub `origin` and the remote branch SHA has been verified.
