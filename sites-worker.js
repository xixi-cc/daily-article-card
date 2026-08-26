export function detailAliasPath(pathname) {
  const match = pathname.match(/^\/(papers|collection-papers)\/([^/]+)(?:\/(?:index(?:\.html)?)?)?$/);
  if (!match) return null;
  const [, root, identifier] = match;
  return `/_detail-routes/${root}/${identifier.replaceAll('.', '__dot__')}.html`;
}

export default {
  async fetch(request, env) {
    if (request.method === 'GET') {
      const requestedUrl = new URL(request.url);
      const aliasPath = detailAliasPath(requestedUrl.pathname);
      if (aliasPath) {
        const aliasUrl = new URL(requestedUrl);
        aliasUrl.pathname = aliasPath;
        const aliasResponse = await env.ASSETS.fetch(new Request(aliasUrl, request));
        if (aliasResponse.status !== 404) return aliasResponse;
      }
    }

    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404 || request.method !== 'GET') {
      return response;
    }

    const fallbackUrl = new URL(request.url);
    fallbackUrl.pathname = '/index.html';
    return env.ASSETS.fetch(new Request(fallbackUrl, request));
  },
};
