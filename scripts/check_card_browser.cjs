#!/usr/bin/env node
/* Explicit manifest -> detail, cover, feed, modal checks, with durable per-surface receipts. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');

function hash(file) { return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'); }
function treeHash(root) {
  const h = crypto.createHash('sha256');
  function walk(dir) {
    for (const name of fs.readdirSync(dir).sort()) {
      const file = path.join(dir, name), stat = fs.lstatSync(file);
      if (stat.isDirectory()) walk(file);
      else if (stat.isFile()) h.update(path.relative(root, file)).update('\0').update(hash(file));
      else throw new Error('Unsupported site symlink: ' + file);
    }
  }
  walk(root); return h.digest('hex');
}
function parseArgs(argv) {
  const opts = {};
  for (let i = 0; i < argv.length; i += 2) {
    if (!argv[i]?.startsWith('--') || !argv[i + 1]) throw new Error('Expected --name value');
    opts[argv[i].slice(2)] = argv[i + 1];
  }
  for (const key of ['repo', 'manifest', 'out']) if (!opts[key]) throw new Error('Missing --' + key);
  return opts;
}
const mime = {'.html':'text/html', '.js':'application/javascript', '.css':'text/css', '.json':'application/json',
  '.svg':'image/svg+xml', '.png':'image/png', '.webp':'image/webp', '.jpg':'image/jpeg', '.woff':'font/woff', '.woff2':'font/woff2'};

async function settle(frame, scope = 'body') {
  await frame.waitForFunction(() => !!window.MathJax?.startup?.promise);
  await frame.evaluate(async () => { await MathJax.startup.promise; await document.fonts.ready; });
  for (const image of await frame.locator(scope + ' img').all()) {
    await image.scrollIntoViewIfNeeded();
    await image.evaluate(im => Promise.race([im.decode(), new Promise((_, reject) => setTimeout(() => reject(new Error('image decode timeout')), 10000))]));
  }
}
async function measure(frame, selector, detail) {
  return frame.locator(selector).evaluate((root, detail) => {
    const raw = [];
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (n.parentElement.closest('script,style,mjx-container,noscript,textarea')) continue;
      if (/\\[()[\]]|\$\$|(?<!\\)\$[^$\n]+\$|\\[a-zA-Z]+/.test(n.textContent)) raw.push(n.textContent.trim().slice(0,160));
    }
    return {
      textLength:root.innerText.length,
      headings: [...root.querySelectorAll('h2')].map(x => x.innerText),
      emptySections: detail ? [...root.querySelectorAll('#detail-body .reading-card-section')]
        .filter(section => {
          const first = section.querySelector('.reading-card-content ul li');
          return !first || first.textContent.trim() === '暂无内容';
        }).map(section => section.querySelector('h2')?.textContent.trim() || '?') : [],
      mathCount:root.querySelectorAll('mjx-container').length,
      mathErrors:[...root.querySelectorAll('mjx-merror,[data-mjx-error]')].map(x => x.textContent),
      rawMath:raw,
      brokenImages:[...root.querySelectorAll('img')].filter(x => !x.complete || !x.naturalWidth).map(x => x.getAttribute('src')),
      overflow:document.documentElement.scrollWidth > innerWidth + 1,
      clippedText:[...root.querySelectorAll('.note-cover-title,.note-cover-abstract')].filter(x =>
        x.scrollHeight > x.clientHeight+1 && ['hidden','clip','auto','scroll'].includes(getComputedStyle(x).overflowY)
      ).map(x => x.className),
      // Wide equations inside an explicitly scrollable frame remain readable.
      // Reject clipping, but report deliberate equation scrolling separately.
      wideEquations: detail ? [...root.querySelectorAll('.display-math')].filter(x => (x.querySelector('mjx-math')?.getBoundingClientRect().width || 0) > x.clientWidth+1).map(x => {
        let node = x.querySelector('mjx-math'), scrollable = false;
        while (node && root.contains(node)) {
          if (['auto','scroll'].includes(getComputedStyle(node).overflowX) && node.scrollWidth > node.clientWidth) scrollable = true;
          node = node.parentElement;
        }
        return {scrollable};
      }) : [],
    };
  }, detail);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2)), repo = path.resolve(opts.repo), site = path.join(repo, 'site'), out = path.resolve(opts.out);
  if (out === repo || out.startsWith(repo + path.sep)) throw new Error('Output must be outside production repository');
  const manifest = JSON.parse(fs.readFileSync(opts.manifest)), entries = manifest.cards;
  if (!Array.isArray(entries) || !entries.length) throw new Error('Empty manifest');
  const seen = new Set();
  for (const e of entries) {
    if (!['Daily','Collection'].includes(e.program) || !/^[a-zA-Z0-9._-]+$/.test(e.id)) throw new Error('Invalid identity');
    const key = e.program + ':' + e.id;
    if (seen.has(key)) throw new Error('Duplicate ' + key); seen.add(key);
    const installed = path.join(repo, 'data', e.program === 'Daily' ? 'curated_cards' : 'collection_cards', e.id + '.json');
    if (hash(installed) !== hash(e.card)) throw new Error('Manifest is not the installed card: ' + key);
    e.source = JSON.parse(fs.readFileSync(e.card));
  }
  const widths = [390,1440], siteHash = treeHash(site);
  const fingerprint = crypto.createHash('sha256').update(JSON.stringify({siteHash, manifest:hash(opts.manifest),
    sources:entries.map(e=>hash(e.card)), checker:hash(__filename), widths, playwright:require('playwright/package.json').version,
    browser:opts.chromium || chromium.executablePath()})).digest('hex');
  const receiptPath = path.join(out, 'receipt.json');
  let receipt = {schema_version:1, fingerprint, site_sha256:siteHash, external_network_blocked:true,
    boundary:'Mechanical rendering only; scientific figure comparison remains a separate human/agent review.', results:[]};
  if (fs.existsSync(receiptPath)) {
    receipt = JSON.parse(fs.readFileSync(receiptPath));
    if (receipt.fingerprint !== fingerprint) throw new Error('Inputs changed: choose a new --out directory');
  }
  fs.mkdirSync(out, {recursive:true});
  const save = () => {
    fs.writeFileSync(receiptPath + '.tmp', JSON.stringify(receipt,null,2)+'\n');
    fs.renameSync(receiptPath + '.tmp', receiptPath);
  };
  const browser = await chromium.launch({headless:true, ...(opts.chromium ? {executablePath:opts.chromium} : {})});
  const origin = 'http://card-audit.local/';
  let reused = 0;
  try {
    for (const entry of entries) for (const width of widths) for (const surface of ['detail','cover','feed','modal']) {
      const key = [entry.program,entry.id,width,surface].join('-');
      const previous = receipt.results.find(r => r.key === key);
      if (previous?.passed && fs.existsSync(previous.screenshot) && hash(previous.screenshot) === previous.screenshot_sha256) { reused++; continue; }
      const page = await browser.newPage({viewport:{width,height:900}});
      page.setDefaultTimeout(15000); page.setDefaultNavigationTimeout(20000);
      const pageErrors = [], localErrors = [];
      page.on('pageerror', e => pageErrors.push(e.message));
      await page.route('**/*', async route => {
        const url = route.request().url();
        if (!url.startsWith(origin)) return route.abort();
        let file = path.resolve(site, '.' + decodeURIComponent(new URL(url).pathname));
        if (file !== site && !file.startsWith(site + path.sep)) return route.fulfill({status:403,body:''});
        try {
          if (fs.statSync(file).isDirectory()) file = path.join(file,'index.html');
          await route.fulfill({status:200, body:fs.readFileSync(file),contentType:mime[path.extname(file)]||'application/octet-stream'});
        } catch {
          localErrors.push(new URL(url).pathname);
          await route.fulfill({status:404,body:'Not found'});
        }
      });
      const daily = entry.program === 'Daily', detailPath = `${daily?'papers':'collection-papers'}/${entry.id}/`;
      const card = entry.source;
      const result = {key, id:entry.id, program:entry.program, width, surface, passed:false};
      try {
        let frame = page, selector = 'body', detail = surface === 'detail' || surface === 'modal';
        let url = origin + (surface === 'detail' ? detailPath : `${daily?'covers':'collection-covers'}/${entry.id}/`);
        if (surface === 'feed' || surface === 'modal') {
          // Use actual feed document, not index.html meta redirect (drops query).
          // Title is searchable across historical feed schemas; ID is not assumed searchable.
          url = origin + (daily?'physics_AI.html':'collection.html') + '?q=' + encodeURIComponent(card.title_en);
        }
        const response = await page.goto(url,{waitUntil:'load'});
        if (response.status() !== 200) throw new Error('HTTP ' + response.status());
        if (surface === 'feed' || surface === 'modal') {
          selector = `.feed-card-link[href="${detailPath}"]`;
          await page.locator(selector).waitFor();
          await settle(page,selector);
          if (surface === 'modal') {
            await page.locator(selector).click();
            await page.waitForFunction(() => document.querySelector('.paper-modal')?.getAttribute('aria-hidden') === 'false');
            const handle = await page.locator('.paper-modal-frame').elementHandle();
            frame = await handle.contentFrame();
            await frame.waitForURL('**/' + detailPath + '**');
            selector = 'body';
          }
        }
        await settle(frame,selector);
        if (detail) {
          await frame.locator('#detail-body').waitFor();
          const headings = await frame.locator('#detail-body h2').allTextContents();
          if (JSON.stringify(headings.map(x=>x.trim())) !== JSON.stringify(card.sections.map(x=>x.title))) throw new Error('Source/render heading mismatch');
        }
        result.metrics = await measure(frame,selector,detail);
        const m = result.metrics;
        if (detail && m.textLength < 900) throw new Error('Empty/wrong detail page');
        // All three cover surfaces must obey the same structured source decision.
        const coverSelector = surface === 'feed' ? selector : surface === 'cover' ? '.cover-preview-shell' : '.detail-hero-cover';
        const cover = frame.locator(coverSelector);
        await cover.waitFor();
        if (card.cover.mode === 'source_figure') {
          const images = await cover.locator('img').evaluateAll(xs=>xs.map(x=>new URL(x.src).pathname));
          if (!images.some(x=>x.endsWith('/'+card.cover.asset_path))) throw new Error('Cover asset/source mismatch');
        } else if (!await cover.locator('.note-cover-title').count()) throw new Error('Missing title/abstract cover');
        result.screenshot = path.join(out,key+'.png');
        if (surface === 'modal') await page.locator('.paper-modal-panel').screenshot({path:result.screenshot});
        else if (surface === 'feed') await page.locator(selector).screenshot({path:result.screenshot});
        else await page.screenshot({path:result.screenshot,fullPage:true});
        result.screenshot_sha256 = hash(result.screenshot);
        result.passed = !m.mathErrors.length && !m.rawMath.length && !m.brokenImages.length && !m.overflow && !m.clippedText.length && !m.emptySections.length && !m.wideEquations.some(x=>!x.scrollable);
      } catch (e) { result.error = e.message; }
      finally {
        result.pageErrors = pageErrors; result.missingLocalResources = localErrors;
        if (pageErrors.length || localErrors.length) result.passed = false;
        if (previous) receipt.results[receipt.results.indexOf(previous)] = result;
        else receipt.results.push(result);
        save(); await page.close();
      }
    }
  } finally { await browser.close(); }
  receipt.passed = receipt.results.length === entries.length*widths.length*4 && receipt.results.every(r=>r.passed);
  save();
  console.log(JSON.stringify({passed:receipt.passed,surfaces:receipt.results.length,reused,failures:receipt.results.filter(r=>!r.passed).map(r=>({key:r.key,error:r.error,metrics:r.metrics,pageErrors:r.pageErrors,missing:r.missingLocalResources}))}));
  if (!receipt.passed) process.exitCode = 1;
}
if (require.main === module) main().catch(e=>{console.error(e.message);process.exitCode=1;});
module.exports = {parseArgs,treeHash};
