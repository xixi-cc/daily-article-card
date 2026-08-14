# Fork setup

- Upstream: <https://github.com/Infinity4B/daily-arxiv-vla>
- Fork: <https://github.com/xixi-cc/daily-arxiv-vla>
- Pages: <https://xixi-cc.github.io/daily-arxiv-vla/>
- Default branch: `master`
- Required GitHub Actions secret: `MODELSCOPE_ACCESS_TOKEN` (ModelScope API token)

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

## Data update and deployment

```bash
python scripts/arxiv_crawler.py
python scripts/generate_summaries.py
python scripts/fetch_paper_images.py --max-items 30
python scripts/build_paper_image_fallback_queue.py --max-items 20
npm run paper-image:fallbacks
python scripts/register_paper_image_fallbacks.py
python scripts/build_site.py
```

The workflow is `.github/workflows/deploy.yml`. It runs on pushes to `master` or `main` and at `0 4 * * *` UTC, commits updated `papers.md` and `site/`, uploads `site/` as a Pages artifact, and deploys it with GitHub Actions.

Add `MODELSCOPE_ACCESS_TOKEN` under **Settings -> Secrets and variables -> Actions -> New repository secret**. On a new public fork, enable inherited workflows from the repository's **Actions** tab; scheduled workflows are disabled by default until enabled.

## Sync from upstream

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

Fork-specific code/configuration changes: none. This file is documentation only; GitHub Pages is configured in repository settings with **Source: GitHub Actions**.
