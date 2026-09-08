#!/usr/bin/env python3
"""Check every generated detail and feed in Chromium using bundled assets only.

Run after build_site.py. Requires Python Playwright and its Chromium runtime.
No web server or public network is needed; external comments/analytics are blocked.
"""
import argparse
import asyncio
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote, urlsplit
from playwright.async_api import async_playwright

SITE = Path(__file__).resolve().parents[1] / 'site'
ORIGIN = 'http://paper-cards.test/'
SCAN = r'''() => {
 const raw = [], walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
 let node;
 while (node = walker.nextNode()) {
  if (node.parentElement.closest('script,style,mjx-assistive-mml,noscript,textarea')) continue;
  if (/\\[a-zA-Z]+|\\[()[\]]|\$[^$\n]+\$/.test(node.textContent)) raw.push(node.textContent.trim().slice(0,300));
 }
 return {formulas:document.querySelectorAll('mjx-container').length,
  errors:[...document.querySelectorAll('mjx-merror')].map(e=>e.textContent), raw,
  overflow:document.documentElement.scrollWidth > innerWidth + 1,
  cards:document.querySelectorAll('.feed-card').length};
}'''

async def audit(widths):
 results = []
 async with async_playwright() as playwright:
  browser = await playwright.chromium.launch()
  semaphore = asyncio.Semaphore(4)
  async def check(path, width):
   async with semaphore:
    page = await browser.new_page(viewport={'width':width, 'height':900})
    row = {'path':str(path.relative_to(SITE)), 'width':width}
    async def serve(route):
     if not route.request.url.startswith(ORIGIN):
      return await route.abort()
     target = SITE / unquote(urlsplit(route.request.url).path.lstrip('/'))
     if target.is_dir(): target = target / 'index.html'
     await route.fulfill(status=200 if target.is_file() else 404,
      body=target.read_bytes() if target.is_file() else b'',
      content_type=mimetypes.guess_type(str(target))[0] or 'application/octet-stream')
    await page.route('**/*', serve)
    try:
     await page.goto(ORIGIN + row['path'], wait_until='load')
     if await page.evaluate('Boolean(window.MathJax?.startup?.promise)'):
      await asyncio.wait_for(page.evaluate('MathJax.startup.promise'), 20)
     if row['path'] in ('index.html','collection.html'):
      # Exercise appended Daily groups, not just the initial visible batch.
      for _ in range(40):
       if not await page.locator('.lazy-sentinel').count(): break
       await page.locator('.lazy-sentinel').scroll_into_view_if_needed()
       await page.wait_for_timeout(200)
      await page.wait_for_timeout(700)
      # A fresh filter render must also be typeset.
      await page.locator('#search').fill('diffusion')
      await page.wait_for_timeout(700)
      filtered = await page.evaluate(SCAN)
      row['filter_errors'] = filtered['errors'] + filtered['raw']
      await page.locator('#search').fill('')
      await page.wait_for_timeout(700)
      for _ in range(40):
       if not await page.locator('.lazy-sentinel').count(): break
       await page.locator('.lazy-sentinel').scroll_into_view_if_needed()
       await page.wait_for_timeout(200)
      await page.wait_for_timeout(700)
     await asyncio.wait_for(page.evaluate('document.fonts.ready'), 15)
     row.update(await page.evaluate(SCAN))
    except Exception as error:
     row['failure'] = str(error)
    finally:
     await page.close()
    results.append(row)
    if len(results) % 100 == 0: print(f'Checked {len(results)} surfaces', flush=True)
  paths = [SITE/'index.html', SITE/'collection.html', *sorted(SITE.glob('papers/*/index.html')), *sorted(SITE.glob('collection-papers/*/index.html'))]
  assert len(paths) > 2, 'Build the site before running the browser check'
  await asyncio.gather(*(check(path,width) for width in widths for path in paths))
  await browser.close()
 return sorted(results,key=lambda row:(row['width'],row['path']))

if __name__ == '__main__':
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path,required=True)
 parser.add_argument('--widths',type=int,nargs='+',default=[390,1440])
 args = parser.parse_args()
 rows = asyncio.run(audit(args.widths))
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 failed = [r for r in rows if r.get('errors') or r.get('raw') or r.get('filter_errors') or r.get('failure') or r.get('overflow')]
 print(f'{len(rows)} surfaces; {len(failed)} failures')
 for row in failed: print(json.dumps(row,ensure_ascii=False))
 raise SystemExit(bool(failed))
