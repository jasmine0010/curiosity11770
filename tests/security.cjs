// Run with: node tests/security.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const pages = JSON.parse(fs.readFileSync(path.join(root, 'content/pages.json'), 'utf8'));
for (const { path: file } of pages) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  assert(!/googletagmanager|google-analytics|window\.messages|_at_config|atari\.vw/.test(html), `${file}: copied runtime or analytics`);
  assert(!/allow-modals|allow-storage-access-by-user-activation|allow-popups-to-escape-sandbox/.test(html), `${file}: excessive embed permissions`);
  assert.equal((html.match(/<h1[ >]/g) || []).length, 1, `${file}: one page heading`);
  assert(html.includes('id="main"') && html.includes('class="skip-link"'), `${file}: skip navigation`);
  for (const [tag] of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) {
    assert(/rel="[^"]*\bnoopener\b/.test(tag), `${file}: opener isolation`);
  }
  for (const [tag] of html.matchAll(/<iframe\b[^>]*>/g)) assert(/sandbox=/.test(tag), `${file}: sandbox missing`);
  for (const [tag] of html.matchAll(/<img\b[^>]*>/g)) assert(/alt="[^"]+"/.test(tag), `${file}: image description`);
  for (const [, value] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    assert(!/^(?:javascript:|http:)/i.test(value), `${file}: unsafe URL ${value}`);
    if (/^(?:https:|mailto:|tel:|#)/.test(value)) continue;
    const clean = value.split(/[?#]/)[0];
    const target = clean.startsWith('/') ? path.join(root, clean) : path.resolve(root, path.dirname(file), clean);
    assert(fs.existsSync(target), `${file}: missing local target ${value}`);
  }
}
assert.equal(pages.length, 36);
console.log('PASS: 36 pages; local links/assets, headings, image descriptions, sandbox permissions, opener isolation, and removal of Google runtime/analytics.');
