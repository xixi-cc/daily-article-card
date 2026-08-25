import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { resolve } from 'node:path';
import { sites } from '@openai/sites-vite-plugin';
import { defineConfig } from 'vite';

function sitesStaticAssets() {
  return {
    name: 'sites-static-assets',
    async closeBundle() {
      const outputDirectory = resolve('dist');
      const clientDirectory = resolve(outputDirectory, 'client');
      const serverDirectory = resolve(outputDirectory, 'server');
      const siteDirectory = resolve('site');

      for (const entry of await readdir(siteDirectory, { withFileTypes: true })) {
        await cp(resolve(siteDirectory, entry.name), resolve(outputDirectory, entry.name), {
          recursive: entry.isDirectory(),
        });
      }

      await mkdir(serverDirectory, { recursive: true });
      await cp(resolve('sites-worker.js'), resolve(serverDirectory, 'index.js'));
      const entries = await readdir(outputDirectory, { withFileTypes: true });

      await rm(clientDirectory, { recursive: true, force: true });
      await mkdir(clientDirectory, { recursive: true });
      for (const entry of entries) {
        if (['.openai', 'client', 'server'].includes(entry.name)) continue;
        await cp(resolve(outputDirectory, entry.name), resolve(clientDirectory, entry.name), {
          recursive: entry.isDirectory(),
        });
      }
    },
  };
}

export default defineConfig({
  base: './',
  publicDir: false,
  plugins: [sites(), sitesStaticAssets()],
});
