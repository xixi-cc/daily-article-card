# Batch reconciliation and acceptance

Use `python3 scripts/card_batch.py` as the common local entry point. These tools
never claim, download, install or publish papers and never edit card content.
Scientific reading and comparison of new figures with the PDF remain separate.

For long Goal sessions, use the `context` subcommand described in
`CARD_CONTEXT.md`. It produces bounded controller views, one-paper packets and
short verified-pointer receipts without replaying unrelated paper histories.

## Production baseline for the 20260930 resumed campaign

- Cards: `/home/xixi/physics/xncao_academic_sites/local-state/github-refresh-20260911/daily`
- Catalog: `/home/xixi/physics/xncao_academic_sites/local-state/card-backfill-20260926/paper-collection`
- Frozen reconciliation: `/home/xixi/physics/xncao_academic_sites/local-state/card-resume-20260930/`
- Active run and receipts: `/home/xixi/physics/xncao_academic_sites/local-state/card-run-20260930/`
- Current item authority: `run-manifest.json` in the active run; check `runtime.json` for active ownership.

The ordinary `sites/daily-paper-card` checkout has older card data and unrelated
changes. Do not use it as the campaign's production source. The path receipt is
a baseline pin, not a process lock. Recheck active writers immediately before a
future write. Recheck local and remote HEAD immediately before each publication;
the original baseline is historical evidence, not a permanent branch pin. Do
not force-push or reset unrelated changes.

## 1. Reconcile without changing frozen history

```bash
python3 scripts/card_batch.py reconcile \
  --campaign /home/xixi/physics/xncao_academic_sites/local-state/card-backfill-20260926 \
  --repo /home/xixi/physics/xncao_academic_sites/local-state/github-refresh-20260911/daily \
  --catalog-repo /home/xixi/physics/xncao_academic_sites/local-state/card-backfill-20260926/paper-collection \
  --out /home/xixi/physics/xncao_academic_sites/local-state/card-resume-20260930/reconciliation-next \
  --check-remote
```

Always choose a new output directory. This campaign-specific reconciler checks
the 517 stopped entries, seven catalog omissions, metadata-only entry and two
accepted staged cards. It verifies the staged manifests, local catalog links,
production revisions, and a bounded Linux process/open-file snapshot. The
reconciler's outputs remain read-only pre-resume evidence; the user-authorized
20260930 `run-manifest.json` is the current routing state. Old progress summaries
and overlays remain immutable. Windows bridge internals
and future scheduled jobs are outside a Linux `/proc` snapshot's guarantee.

## 2. Deliver an explicit manifest

```json
{
  "cards": [
    {
      "id": "2609.00162",
      "program": "Daily",
      "card": "/absolute/path/to/2609.00162.json"
    }
  ]
}
```

For an uninstalled figure, `asset_sources` may map a public asset path to its
absolute staged source file. For example,
`"assets/card-figures/ID/fig1.png": "/absolute/staging/fig1.png"`. Without an
override, `assets/card-figures/` maps to `data/card_figures/` and
`assets/collection-figures/` maps to `data/collection_figures/`. Never satisfy
delivery by putting a figure only in generated `site/` output. Overrides do
not install assets: the installer must persist them in the canonical mapping
and run delivery again without overrides before building.

```bash
python3 scripts/card_batch.py delivery --manifest /absolute/batch.json \
  --out /absolute/new-delivery-receipt.json
```

The checker uses the repository's v2.3 validator and fails on incomplete
metadata, wrong identity/version, invalid Daily/Collection provenance, missing
sections, missing reproduction boundary, malformed math and missing persistent
figures. It also requires nonempty `paragraphs` or `bullets` for every section:
the site renderer does not read a standalone `content` field. Daily requires an
exact arXiv `vN` source version and UTC serialization accepted by the canonical
metadata validator; Collection can use a stable journal version identifier and
retain a valid day-precision ISO date.
The checker does not invent a timestamp or repair a heading automatically.
It is stricter about the standard's background section than the historical
validator; old published cards can therefore reveal pre-existing omissions.

## 3. Accept the generated batch in a browser

After the independently authorized installation/build, point the same manifest
at installed card JSON. The browser refuses a source that differs from the
installed card. Use an external output directory:

```bash
python3 scripts/card_batch.py browser \
  --repo /home/xixi/physics/xncao_academic_sites/local-state/github-refresh-20260911/daily \
  --manifest /absolute/batch.json --out /absolute/browser-receipts
```

Playwright uses its installed Chromium by default; `--chromium /absolute/binary`
is available if the host needs an explicit runtime. External network requests
are blocked, so local math and font packaging must work.

For each card, at 390 and 1440 px, inspect detail, standalone cover, actual feed
document and modal iframe. Use `physics_AI.html` / `collection.html` with a
paper-ID query, exact detail href, `.paper-modal` and `.paper-modal-frame`.
Never use an index redirect with a query, guess `#paper-modal`, or accept an
empty/404 detail. Await MathJax/fonts and scroll/decode lazy images. Reject math
errors, raw delimiters, missing images, overflow, clipped cover text and detail
sections that still render as `暂无内容`.
Chinese `mjx-utext` fallback is not a math error.

The receipt is checkpointed after each surface, including failures. Reusing the
same output directory skips only passing surfaces whose complete site, card,
manifest, checker/runtime fingerprint and screenshot hashes are unchanged.
Failures rerun; changed inputs require a new output directory. Receipts include
screenshots for visual inspection; mechanical success does not establish
scientific correctness or figure-source fidelity.

Run the normal strict validator, unit tests, build and release checks required
by `PAPER_CARD_STANDARD.md` once per accepted batch. This tool does not replace
JSON/render paragraph parity, scientific review or GitHub/Pages/Sites receipts.
