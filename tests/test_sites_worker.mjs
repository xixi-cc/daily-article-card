import assert from 'node:assert/strict';
import test from 'node:test';

import worker, { detailAliasPath } from '../sites-worker.js';


test('detail route IDs containing dots map to safe static aliases', () => {
  assert.equal(
    detailAliasPath('/collection-papers/0912.3000/'),
    '/_detail-routes/collection-papers/0912__dot__3000.html',
  );
  assert.equal(
    detailAliasPath('/papers/2608.06428'),
    '/_detail-routes/papers/2608__dot__06428.html',
  );
  assert.equal(detailAliasPath('/collection'), null);
});


test('worker resolves a detail alias before the static host redirects the dotted path', async () => {
  const requests = [];
  const env = {
    ASSETS: {
      async fetch(request) {
        const path = new URL(request.url).pathname;
        requests.push(path);
        if (path === '/_detail-routes/collection-papers/1510__dot__08707.html') {
          return new Response('card', { status: 200 });
        }
        return new Response('missing', { status: 404 });
      },
    },
  };

  const response = await worker.fetch(
    new Request('https://example.test/collection-papers/1510.08707/'),
    env,
  );
  assert.equal(response.status, 200);
  assert.equal(await response.text(), 'card');
  assert.deepEqual(requests, ['/_detail-routes/collection-papers/1510__dot__08707.html']);
});
