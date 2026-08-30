# MinerU representative sample benchmark — 2026-08-31

Scope: exactly three pending public arXiv works — `1901.09813`, `2404.14265`, and `2608.18419`. This is an extraction benchmark only: no Paper Cards were generated and no tracked repository files were modified.

## Execution boundary

- Engine: configured MinerU Open API (`open-api`), `--lang en`, `--api-model auto`.
- The user explicitly authorized remote upload of these three official public arXiv PDFs. No API token, credential, or private document is present in the output.
- `mineru-open-api` version `v0.5.9` passed its local token-format check. The service/CLI did not disclose a resolved model name beyond requested `auto`.
- An independent official-PDF inspection Skill was unavailable in this environment. Local `pdfinfo`, `pdftotext`, and rendered PDF page inspection were used instead. The sources had selectable text and legible rendered pages; `2608.18419` produced a non-fatal embedded-font warning in some Poppler text operations.
- Approximate tokens are `ceil(Unicode characters / 4)`, not a tokenizer measurement.

## Results

| arXiv | PDF pages / bytes | raw text chars / approx tokens | MinerU Markdown chars / approx tokens | checked PDF pages | outcome |
|---|---:|---:|---:|---|---|
| 1901.09813 | 11 / 720,000 | 77,826 / 19,457 | 69,670 / 17,418 | 3, 6 | Title/sections, histogram and Word Transformation diagram content retained; equations have local symbol/spacing errors. |
| 2404.14265 | 13 / 2,449,070 | 61,457 / 15,365 | 50,115 / 12,529 | 4, 6 | Equation-heavy Forman-Ricci/global-flow material retained with equation tags; exact math still needs source checking. |
| 2608.18419 | 11 / 1,845,050 | 64,042 / 16,011 | 49,567 / 12,392 | 2, 7 | Figure 1, Algorithm 1, Figure 6 and surrounding formulas retained; some RoPE symbols are malformed/replacement characters. |

For every paper, all image paths referenced by Markdown exist (`0` missing targets). The image-file count may exceed the Markdown-link count because MinerU writes intermediate or unreferenced image crops.

## Visual and structural checks

- **1901.09813:** Compared page 3 (Figure 2 histogram and dense formulas) and page 6 (Figure 3/Word Transformation and formula-heavy text). Corresponding figure captions, section headings, images, and formula-bearing blocks are present. Math typography and some inline symbols are not faithful enough for final equation reuse.
- **2404.14265:** Compared pages 4 and 6, both equation-heavy. The Markdown preserves the Forman-Ricci curvature block, equations (3)–(11) context, section transitions, and result text. It is suitable as a structured reading aid, not as a substitute for author PDF/TeX mathematical verification.
- **2608.18419:** Compared page 2 (Figure 1 and Algorithm 1) and page 7 (Figure 6 and RoPE equations). Algorithm and image/caption structure is preserved. The RoPE-region malformed symbols make formula copying unsafe without the source PDF/TeX.

## Artifact layout

Each `<card-id>` directory contains `source/<arXiv-id>.pdf`, SHA-256 and provenance files, raw `pdftotext` output, rendered verification pages, and MinerU output at `source/mineru/<arXiv-id>.md` with `source/mineru/images/`.

See [benchmark.json](benchmark.json) for hashes, exact paths, counts, and per-paper quality notes.
