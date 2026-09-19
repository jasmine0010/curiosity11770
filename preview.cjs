// Start with: node preview.cjs
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const root = __dirname;
const server = http.createServer((req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    let name = decodeURIComponent(url.pathname).replace(/^\/+|\/+$/g, '') || 'home';
    if (name.split(/[\\/]/).some(part => part.startsWith('.')) || name.includes('\\')) {
      res.writeHead(404).end('Not found');
      return;
    }
    const assetTypes = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.woff2': 'font/woff2' };
    const assetType = name.startsWith('assets/') ? assetTypes[path.extname(name)] : undefined;
    const canonical = assetType || name.endsWith('.html') ? name : name + '.html';
    const target = path.resolve(root, canonical);
    if (!target.startsWith(root + path.sep) || !fs.existsSync(target) || !fs.statSync(target).isFile()) {
      res.writeHead(404).end('Not found');
      return;
    }
    // Google Sites navigation uses extensionless URLs; serve the saved HTML at
    // a canonical URL so relative links also work on nested season pages.
    if (url.pathname !== '/' + canonical) {
      res.writeHead(302, { Location: '/' + canonical + url.search }).end();
      return;
    }
    res.writeHead(200, { 'Content-Type': assetType || 'text/html; charset=utf-8', 'X-Content-Type-Options': 'nosniff' });
    res.end(req.method === 'HEAD' ? undefined : fs.readFileSync(target));
  } catch {
    res.writeHead(400).end('Invalid request');
  }
});
server.listen(Number(process.env.PORT || 8765), '127.0.0.1', () => {
  console.log(`Preview: http://127.0.0.1:${server.address().port}/home.html`);
});
