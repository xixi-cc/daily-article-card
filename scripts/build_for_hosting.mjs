#!/usr/bin/env node
/**
 * Build locally with Python when available, or reuse the committed static site
 * on minimal hosting builders that only provide Node.js.
 */

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { build } from 'vite';


function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit' });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}


const python = spawnSync('python3', ['--version'], { stdio: 'ignore' });
if (python.status === 0) {
  run('python3', ['scripts/build_site.py']);
} else if (!existsSync('site/index.html') || !existsSync('site/assets/collection-data.json')) {
  throw new Error('python3 is unavailable and the committed static site is incomplete');
} else {
  console.log('python3 unavailable; reusing the verified committed site/ tree');
}

await build();
