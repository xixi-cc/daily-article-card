# physics+AI Daily Paper Cards

一个展示 physics+AI arXiv 精选论文的静态网站。每日 Codex 自动任务直接检查 arXiv daily listing，独立完成筛选、全文证据核验、S 级判定、中文论文卡片生成和 GitHub Pages 发布。

## 功能

- 每日自动收录 Codex 按固定 40 分标准评为 S 的论文
- 按无版本号 arXiv ID 去重
- 展示中文概述、核心贡献、方法、证据与局限
- 自动抓取论文首图，并提供截图兜底
- 支持标题、机构、摘要亮点和 arXiv ID 搜索
- 为每篇论文生成独立详情页
- 响应式界面与亮色、暗色主题

本项目不在 GitHub Actions 中调用外部 LLM API，也不需要 ModelScope token。Codex 直接完成 arXiv 检索、筛选、全文卡片写作、验证与发布；GitHub Actions 只执行确定性图片处理、构建和 Pages 部署。

Codex 的端到端筛选和发布合同见 [`docs/CODEX_DAILY_SCREENING_AND_PUBLICATION.md`](docs/CODEX_DAILY_SCREENING_AND_PUBLICATION.md)。论文卡片的 canonical 编辑、公式、证据、数据与发布标准见 [`docs/PAPER_CARD_STANDARD.md`](docs/PAPER_CARD_STANDARD.md)。Paper Collection 的长期补卡与 Daily feed 是两个独立数据流；Collection 卡不得进入 Daily 时间线或继承日报评级。

## 本地构建

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm ci
npx playwright install chromium
python scripts/build_site.py
cd site && python -m http.server 8000
```

主页面文件为 `site/physics_AI.html`。`site/index.html` 仅作为 GitHub Pages 的入口重定向。

## 数据与构建

- `papers.md`：经过 GPT 筛选并由 Codex 验证的论文数据源
- `scripts/fetch_paper_images.py`：抓取论文首图
- `scripts/build_paper_image_fallback_queue.py`：生成截图兜底队列
- `scripts/render_paper_image_fallbacks.mjs`：渲染兜底截图
- `scripts/register_paper_image_fallbacks.py`：登记论文图片
- `scripts/build_site.py`：生成主页、数据、详情页和封面
- `site/`：GitHub Pages 静态产物

运行完整的确定性构建：

```bash
python scripts/fetch_paper_images.py --max-items 30
python scripts/build_paper_image_fallback_queue.py --max-items 20
npm run paper-image:fallbacks
python scripts/register_paper_image_fallbacks.py
python scripts/build_site.py
```

## 部署

推送到 `master` 或 `main` 后，`.github/workflows/deploy.yml` 会构建并部署 `site/`。论文选择由 Codex 的每日自动任务完成；GitHub Actions 只执行确定性的图片处理、构建和 Pages 发布。

站点地址：<https://xixi-cc.github.io/physics_AI/>
