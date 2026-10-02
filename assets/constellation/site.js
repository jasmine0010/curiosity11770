/* Navigation, search, and the fixed constellation plate. No dependencies. */
(() => {
  const menu = document.querySelector('.c-menu');
  const nav = document.getElementById('c-nav');
  const toggle = document.querySelector('.c-search-toggle');
  const panel = document.getElementById('c-search');
  const query = document.getElementById('c-query');
  const results = document.getElementById('c-results');
  const status = document.getElementById('c-search-status');
  function closeMenus() {
    nav.classList.remove('is-open'); menu.setAttribute('aria-expanded', 'false');
    nav.querySelectorAll('details').forEach(d => { d.open = false; });
  }
  menu.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open'); menu.setAttribute('aria-expanded', String(open));
  });
  function closeSearch() { panel.hidden = true; toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
  toggle.addEventListener('click', () => {
    if (!panel.hidden) return closeSearch();
    closeMenus(); panel.hidden = false; toggle.setAttribute('aria-expanded', 'true'); query.focus();
  });
  document.querySelector('.c-search-close').addEventListener('click', closeSearch);
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    if (!panel.hidden) closeSearch();
    else { const summary = document.activeElement.closest('details')?.querySelector('summary'); closeMenus(); (summary || menu).focus(); }
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.c-header')) closeMenus();
  });
  nav.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', () => {
    if (detail.open) nav.querySelectorAll('details').forEach(other => { if (other !== detail) other.open = false; });
  }));
  const normalize = value => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  query.addEventListener('input', () => {
    const words = normalize(query.value).trim().split(/\s+/).filter(Boolean);
    results.replaceChildren();
    if (!words.length) { status.textContent = 'Enter a word or phrase to search all pages.'; return; }
    const matches = (window.CONSTELLATION_SEARCH || []).filter(p => words.every(word => normalize(p.title + ' ' + p.text).includes(word)));
    status.textContent = matches.length ? `${matches.length} page${matches.length === 1 ? '' : 's'} found.` : 'No pages found. Try another search.';
    matches.forEach(page => {
      const li = document.createElement('li'), a = document.createElement('a'), p = document.createElement('p');
      a.href = page.url; a.textContent = page.title;
      const start = Math.max(0, normalize(page.text).indexOf(words[0]) - 45);
      p.textContent = (start ? '…' : '') + page.text.slice(start, start + 190) + (page.text.length > start + 190 ? '…' : '');
      li.append(a, p); results.append(li);
    });
  });
  const map = document.getElementById('constellation');
  if (!map) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const pause = document.getElementById('motion-toggle');
  let paused = reduced.matches;
  function drawConnections() {
    const bounds = map.getBoundingClientRect();
    map.querySelectorAll('.star-connection').forEach(line => {
      const from = document.getElementById('star-' + line.dataset.from).getBoundingClientRect();
      const to = document.getElementById('star-' + line.dataset.to).getBoundingClientRect();
      const x = from.left + from.width/2 - bounds.left, y = from.top + from.height/2 - bounds.top;
      const dx = to.left + to.width/2 - bounds.left - x, dy = to.top + to.height/2 - bounds.top - y;
      line.style.left = x + 'px'; line.style.top = y + 'px'; line.style.width = Math.hypot(dx,dy) + 'px';
      line.style.transform = `rotate(${Math.atan2(dy,dx)}rad)`;
    });
  }
  new ResizeObserver(drawConnections).observe(map);
  drawConnections();
  function updateMotion() {
    document.body.classList.toggle('motion-paused', paused);
    pause.disabled = reduced.matches;
    pause.textContent = reduced.matches ? 'Reduced motion' : paused ? 'Play animation' : 'Pause animation';
    pause.setAttribute('aria-pressed', String(paused));
  }
  pause.addEventListener('click', () => { paused = !paused; updateMotion(); });
  reduced.addEventListener('change', () => { paused = reduced.matches; updateMotion(); });
  updateMotion();
  let burstSeed = 11770;
  const burstRandom = () => {
    burstSeed = (burstSeed * 1664525 + 1013904223) >>> 0;
    return burstSeed / 4294967296;
  };
  map.querySelectorAll('.star-link').forEach(star => {
    function burst() {
      if (paused || reduced.matches) return;
      for (let i = 0; i < 25; i++) {
        const spark = document.createElement('i');
        spark.className = 'spark ' + ['red', 'orange', 'yellow', 'white'][i % 4];
        spark.setAttribute('aria-hidden', 'true');
        const angle = Math.PI * 2 * i / 25;
        const distance = 80 + burstRandom() * 50;
        spark.style.cssText = `left:50%;top:50%;--dx:${Math.cos(angle) * distance}px;--dy:${Math.sin(angle) * distance}px`;
        star.append(spark);
        setTimeout(() => spark.remove(), 1100);
      }
    }
    star.addEventListener('pointerenter', burst);
    star.addEventListener('focus', burst);
  });
})();
