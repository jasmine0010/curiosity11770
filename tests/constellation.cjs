// Static coverage of every recreated page, including local assets and embed safety.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const content = path.join(root, 'content/constellation');
const pages = [{slug:'home'}, ...JSON.parse(fs.readFileSync(path.join(content,'pages.json'),'utf8'))];
const inventory = JSON.parse(fs.readFileSync(path.join(content,'inventory.json'),'utf8'));
assert.deepEqual(pages.map(p=>p.slug).sort(), inventory.filter(p=>!p.error).map(p=>p.slug).sort(), 'Every public source page is recreated');
let embeds = 0;
for (const page of pages) {
  const file = path.join(root,'constellation',page.slug+'.html');
  const html = fs.readFileSync(file,'utf8');
  assert.equal((html.match(/<h1[ >]/g)||[]).length,1,`${page.slug}: one main heading`);
  assert(!/source-layout\.css|\/themes\/|yaqOZd|hJDwNd-AhqUyc/.test(html),`${page.slug}: no imported layout`);
  assert(!/<a class="c-action"[^>]*><span><a/.test(html),`${page.slug}: no nested action links`);
  assert(!/[↗↑]/.test(html),`${page.slug}: no decorative link arrows`);
  if (page.slug === 'home') {
    const destinations = html.match(/<nav class="c-destinations"[\s\S]*?<\/nav>/)?.[0] || '';
    assert.equal((destinations.match(/<a href=/g)||[]).length,6,'Mobile destination list covers all stars');
    assert(!/Find your|Choose a direction|A resource network/.test(html),'Map contains no added promotional copy');
  } else {
    assert(html.includes('class="c-masthead') && html.includes('class="c-content-section'),`${page.slug}: editorial layout`);
  }
  assert(!/googletagmanager|google-analytics|jscontroller=|jsaction=|data-code=|intermediate-frame-minified/.test(html),`${page.slug}: no source runtime`);
  assert(!/\son\w+\s*=/.test(html),`${page.slug}: no inline event handlers`);
  assert(html.includes('id="main"') && html.includes('href="#main"'),`${page.slug}: skip link`);
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
  for (const [,raw] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const url=raw.replaceAll('&amp;','&');
    if(url.startsWith('#')) assert(ids.has(url.slice(1)),`${page.slug}: missing anchor ${url}`);
    assert(!/^(javascript:|http:|data:text\/html)/i.test(url),`${page.slug}: unsafe URL`);
    if (/^(https:|mailto:|tel:|#)/.test(url)) continue;
    assert(url.startsWith('/'),`${page.slug}: use root-relative local links`);
    assert(fs.existsSync(path.join(root,url.split(/[?#]/)[0])),`${page.slug}: missing ${url}`);
  }
  for (const [,url] of html.matchAll(/url\(["']?([^)'"\s]+)["']?\)/g)) {
    assert(url.startsWith('/assets/constellation/'),`${page.slug}: background is local`);
    assert(fs.existsSync(path.join(root,url)),`${page.slug}: missing background`);
  }
  for (const [img] of html.matchAll(/<img\b[^>]*>/g)) {
    assert(/alt="[^"]*"/.test(img),`${page.slug}: image alt attribute`);
    assert(/src="\/assets\//.test(img),`${page.slug}: local image`);
  }
  for (const [frame] of html.matchAll(/<iframe\b[^>]*>/g)) {
    embeds++;
    assert(/src="https:\/\//.test(frame),`${page.slug}: iframe URL`);
    assert(/title="[^"]+"/.test(frame) && /sandbox="/.test(frame),`${page.slug}: accessible sandboxed frame`);
    assert(!/allow-top-navigation|allow-popups-to-escape-sandbox|allow-storage-access/.test(frame),`${page.slug}: iframe permissions`);
  }
  for (const [link] of html.matchAll(/<a\b[^>]*target="_blank"[^>]*>/g)) assert(/rel="noopener noreferrer"/.test(link));
}
const context={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'assets/constellation/search-index.js'),'utf8'),context);
const index=context.window.CONSTELLATION_SEARCH;
assert.equal(index.length,pages.length,'Search covers every page');
assert(index.some(p=>p.title.includes('CAD') && p.text.includes('Onshape')),'Guide text is searchable');
const map=JSON.parse(fs.readFileSync(path.join(content,'map.json'),'utf8'));
assert.equal(map.stars.length,6);
assert.equal(map.connections.length,6);
for(const star of map.stars) assert(fs.existsSync(path.join(root,star.href)),'Every star has a local destination');
assert.equal(new Set(map.connections.flat()).size,6,'The drawn constellation connects all six stars');
assert(map.fieldStars.length >= 20 && map.fieldStars.length <= 50,'The fixed field has a restrained number of stars');
assert.equal(map.comets.length,2,'The plate has two intentional comet paths');
assert(map.comets.every(comet=>Math.abs(comet.angle % 180) >= 15),'Comet routes are visibly diagonal');
const mapCss=fs.readFileSync(path.join(root,'assets/constellation/map.css'),'utf8');
assert(mapCss.includes('rotate(var(--angle)) translateX(var(--travel))'),'Comet tails follow the travel angle');
const home=fs.readFileSync(path.join(root,'constellation/home.html'),'utf8');
assert.equal((home.match(/class="chart-point /g)||[]).length,map.fieldStars.length,'Fixed field is rendered from editable data');
assert.equal((home.match(/class="chart-comet"/g)||[]).length,map.comets.length,'Comet paths are rendered from editable data');
assert(!/Math\.random|bg-star|red-nebula/.test(fs.readFileSync(path.join(root,'assets/constellation/site.js'),'utf8')),'Map has no procedural scatter or nebula');
console.log(`PASS: ${pages.length} Constellation pages, ${embeds} embeds, local images/links, search coverage, six star destinations.`);
