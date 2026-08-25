# Repository setup

- Repository: <https://github.com/xixi-cc/physics_AI>
- Pages: <https://xixi-cc.github.io/physics_AI/>
- Default branch: `master`
- Required GitHub Actions secrets: none

This repository began as a public fork, but its inherited paper collection and topic-specific crawler have been removed. Git history retains provenance and recovery information. The active data source is the user's GPT-curated `arXiv 物理与AI日报`, consumed by a scheduled Codex task.

The workflow in `.github/workflows/deploy.yml` supports manual dispatch and push-triggered deployment. It performs deterministic image handling, site generation, and GitHub Pages publication without calling an LLM API.
