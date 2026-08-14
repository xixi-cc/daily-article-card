# Fork setup

- Upstream: <https://github.com/Infinity4B/daily-arxiv-vla>
- Fork: <https://github.com/xixi-cc/daily-arxiv-vla>
- Pages: <https://xixi-cc.github.io/daily-arxiv-vla/>
- Default branch: `master`
- Required GitHub Actions secrets: none

## Local setup and build

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
npx playwright install chromium
python scripts/build_site.py
cd site && python -m http.server 8000
```

If the system Python does not provide `ensurepip`, an existing `uv` installation can create the same isolated requirements-based environment:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## Automated data update and deployment

```bash
python scripts/arxiv_crawler.py
python scripts/fetch_paper_images.py --max-items 30
python scripts/build_paper_image_fallback_queue.py --max-items 20
npm run paper-image:fallbacks
python scripts/register_paper_image_fallbacks.py
python scripts/build_site.py
```

The workflow is `.github/workflows/deploy.yml`. It supports manual dispatch, runs on pushes to `master` or `main`, and runs at `0 4 * * *` UTC. It crawls arXiv, fetches images, builds the site, commits updated `papers.md` and `site/`, uploads `site/` as a Pages artifact, and deploys it with GitHub Actions. It does not call an LLM and requires no API secret.

## Manual summaries with Codex

New crawler entries retain the upstream `待生成` placeholder. To summarize them with the ChatGPT/Codex subscription, open this repository in Codex and ask it to process a bounded number of pending entries, update `papers.md`, rebuild `site/`, verify the diff, and commit/push the result. This is an interactive workflow; the ChatGPT subscription is not exposed to GitHub Actions.

On a new public fork, enable inherited workflows from the repository's **Actions** tab; scheduled workflows are disabled by default until enabled.

## Sync from upstream

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

Fork-specific configuration change: the ModelScope summary step is disabled, and `workflow_dispatch` is enabled. GitHub Pages is configured in repository settings with **Source: GitHub Actions**.
