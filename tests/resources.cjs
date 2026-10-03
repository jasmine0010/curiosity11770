// Check that the migration preserves the complete resource collection and its media.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const pages = JSON.parse(read('content/pages.json')).filter(p => p.resource_content);
const originals = JSON.parse(read('content/constellation/pages.json')).filter(p => /^(?:translated-)?north-star-resources\//.test(p.slug));
const landing = read('resources.html');
assert.equal(pages.length, originals.length + 1, 'One landing page and every original guide');
const text = html => html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
let embeds = 0;
for (const original of originals) {
  const page = pages.find(p => p.resource_original === original.slug);
  assert(page, `Transferred ${original.slug}`);
  const source = read(`content/constellation/pages/${original.slug}.html`);
  const copied = read(page.resource_content);
  const built = read(page.path);
  assert.equal(text(copied), text(source), `${page.path}: all guide wording retained`);
  assert(landing.includes(`href="/${page.path}"`), `${page.path}: directly linked from Resources`);
  assert(built.includes('class="site-header"') && built.includes('class="site-footer"'), `${page.path}: Curiosity layout`);
  assert(built.includes('href="/resources.html"'), `${page.path}: Resources parent link`);
  assert(!built.includes('href="/constellation/'), `${page.path}: no Constellation navigation`);
  for (const [, media] of source.matchAll(/(?:src|href)="([^\"]+)"/g)) {
    if (media.startsWith('/constellation/')) continue;
    assert(copied.includes(media), `${page.path}: retained image, embed, or external link ${media}`);
  }
  embeds += (source.match(/<iframe\b/g) || []).length;
}
for (const slug of ['north-star-resources', 'translated-north-star-resources']) {
  const source = read(`content/constellation/pages/${slug}.html`);
  for (const [, media] of source.matchAll(/src="([^\"]+)"/g)) {
    assert(landing.includes(media), `Landing page retains ${media}`);
  }
}
assert(!landing.includes('href="/constellation/'), 'Resources links stay within Curiosity');
assert(landing.includes('id="spanish-resources"'), 'Spanish resources are part of the same landing page');
assert(read('portfolio-support.html').includes('/resources/portfolio-examples.html'), 'Portfolio Support uses internal resources');
console.log(`PASS: ${originals.length} complete guides, ${embeds} embeds, landing images, direct hierarchy, and Curiosity navigation.`);
