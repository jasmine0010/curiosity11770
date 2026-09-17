// Run with: node tests/security.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const cp = require('node:child_process');
const root = path.resolve(__dirname, '..');
const files = cp.execFileSync('git', ['ls-files', '*.html'], { cwd: root, encoding: 'utf8' }).trim().split('\n');
let links = 0, frames = 0;
let handler;
for (const file of files) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  assert(!/googletagmanager\.com\/gtag\/js|function gtag\(|gtag\('js'/.test(html), file);
  assert(!/allow-modals|allow-storage-access-by-user-activation|allow-popups-to-escape-sandbox/.test(html), file);
  assert(!/href="http:\/\/www\.explodingbacon\.com\//.test(html), file);
  for (const [tag] of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) {
    assert(/\brel="[^"]*\bnoopener\b/.test(tag), file);
    links++;
  }
  frames += [...html.matchAll(/<iframe\b/g)].length;
  const current = html.match(/window.messages = \[\];[\s\S]*?\n\}\);/)[0];
  if (handler) assert.equal(current, handler, file);
  handler = current;
  // Confirm all non-script markup/content is identical except the approved attributes.
  const baseline = cp.execFileSync('git', ['show', `HEAD:${file}`], { cwd: root, encoding: 'utf8', maxBuffer: 10e6 });
  const normalize = s => s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/g, '')
    .replace(/ allow-modals| allow-storage-access-by-user-activation| allow-popups-to-escape-sandbox/g, '')
    .replace(/ rel="noopener"/g, '')
    .replace(/https:\/\/lh[0-9]+(?:-[a-z]+)?\.googleusercontent\.com\/[^\s"'<>);&]+|\/assets\/placeholders\/[123]\.png/g, 'PLACEHOLDER_IMAGE')
    .replace(/http:\/\/www\.explodingbacon\.com\//g, 'https://explodingbacon.com/');
  assert.equal(normalize(html), normalize(baseline), `${file}: unexpected content change`);
}
assert.equal(files.length, 36);
assert.equal(links, 159);
assert.equal(frames, 4);
const source = {};
let src = 'https://drive.google.com/file/d/example/preview';
let receive;
const window = { addEventListener: (name, callback) => { assert.equal(name, 'message'); receive = callback; } };
const document = { baseURI: 'https://example.org/home.html', querySelectorAll: () => [{ contentWindow: source, getAttribute: () => src }] };
vm.runInNewContext(handler, { window, document, URL });
const valid = { source, origin: 'https://drive.google.com', data: { magic: 'SHIC' } };
for (const event of [
  { ...valid, origin: 'https://evil.example' },
  { ...valid, origin: 'https://drive.google.com.evil.example' },
  { ...valid, origin: 'null' },
  { ...valid, source: {} },
  { ...valid, source: null },
  ...[null, 'SHIC', [], {}, { magic: 1 }, { magic: 'other' }, Object.create({ magic: 'SHIC' })].map(data => ({ ...valid, data }))
]) receive(event);
assert.equal(window.messages.length, 0);
for (const url of ['http://drive.google.com/preview', 'data:text/html,test', 'https://[invalid']) {
  src = url;
  receive(valid);
}
assert.equal(window.messages.length, 0);
src = 'https://drive.google.com/file/d/example/preview';
receive(valid);
assert.equal(window.messages.length, 1);
assert.equal(window.messages[0], valid);
for (let i = 0; i < 1000; i++) receive(valid);
assert.equal(window.messages.length, 100);
window.messages = null;
assert.doesNotThrow(() => receive(valid));
console.log('PASS: 36 pages, 159 links, 4 embeds; unchanged content; sender validation and queue flood protection.');
