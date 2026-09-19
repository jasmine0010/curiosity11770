"""Rebuild the static site: python scripts/build_site.py (standard library only)."""
from pathlib import Path
import json, html, re, base64
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
pages = json.loads((ROOT / 'content/pages.json').read_text(encoding='utf-8'))
# SVG wrappers crop only transparent margins; the supplied raster stays untouched.
logo_data = base64.b64encode((ROOT / 'assets/design/team-logo.png').read_bytes()).decode('ascii')
for filename, white in [('mark.svg', True), ('team-logo-red.svg', False)]:
    effect = '<defs><filter id="white" color-interpolation-filters="sRGB"><feFlood flood-color="#f3f1eb"/><feComposite in2="SourceAlpha" operator="in"/></filter></defs>' if white else ''
    filter_attr = ' filter="url(#white)"' if white else ''
    (ROOT / 'assets/design' / filename).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="212 190 1068 1095">{effect}<image width="1500" height="1500" href="data:image/png;base64,{logo_data}"{filter_attr}/></svg>', encoding='utf-8')
MARK = '<img class="brand-mark" src="/assets/design/team-logo-red.svg" alt="Curiosity team logo" width="54" height="54">'
FOOTER_MARK = '<img class="brand-mark" src="/assets/design/team-logo-red.svg" alt="Curiosity team logo" width="86" height="88">'
def link(url, label, cls=''):
    return f'<a class="{cls}" href="{url}">{label}</a>'
def nav(current):
    items=[('about-us.html','About Us'),('2024-25-season.html','2024–25 Season'),('curiosity-cares.html','Curiosity Cares'),('past-seasons.html','Past Seasons'),('blog.html','Blog')]
    def active(item):
        if item == current:
            return True
        if item == '2024-25-season.html' and current.startswith('2024-25-season/'):
            return True
        if item == 'past-seasons.html' and (current.startswith('past-seasons/') or (re.match(r'20\d{2}-\d{2}-season(?:/|\.html)', current) and not current.startswith('2024-25-season'))):
            return True
        if item == 'curiosity-cares.html' and current in {'portfolio-support.html', 'female-empowerment-summit.html'}:
            return True
        return False
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/home.html" aria-label="Curiosity 11770 home">{MARK}<span>Curiosity<small>Robotics · 11770</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span>+</span></button><nav id="site-nav" aria-label="Main navigation">{''.join(f'<a href="/{u}"'+(' aria-current="page"' if active(u) else '')+f'>{t}</a>' for u,t in items)}<a class="nav-contact" href="/contact.html"{' aria-current="page"' if current == 'contact.html' else ''}>Contact</a></nav></header>'''
def footer():
    return f'''<footer class="site-footer"><div class="footer-top"><a class="footer-cta" href="/contact.html">Connect with Us!</a></div><div class="footer-bottom"><a class="brand" href="/home.html">{FOOTER_MARK}<span>Curiosity<small>Robotics · 11770</small></span></a><p>Marlborough School<br>Los Angeles, California</p><div><a href="https://www.instagram.com/curiosity11770/" target="_blank" rel="noopener noreferrer">Instagram</a><a href="mailto:team11770@marlborough.org">Email</a></div><div><a href="/professional-partners.html">Professional Partners</a><a href="/community-partners.html">Community Partners</a><a href="https://constellation.curiosity11770.marlborough.org/home">Constellation</a><a href="https://constellation.curiosity11770.marlborough.org/north-star-resources">Resources</a></div></div><div class="colophon"><span>© Team Curiosity 11770</span><span>Courage. Connection. Collaboration.</span><a href="#top">Back to top</a></div></footer>'''
HOME = (ROOT / 'content/home.html').read_text(encoding='utf-8')
SEASONS = [
    ('2024-25', 'Into the Deep', 'Rosalind Plankton', 'Rosalind Franklin'),
    ('2023-24', 'Centerstage', 'Katherine Droneson', 'Katherine Johnson'),
    ('2022-23', 'PowerPlay', 'Mae Jemicone', 'Mae Jemison'),
    ('2021-22', 'Freight Frenzy', '', ''),
    ('2020-21', 'Ultimate Goal', '', ''),
    ('2019-20', 'Skystone', 'Marie Curi(osity)', ''),
    ('2018-19', 'Rover Ruckus', '', ''),
    ('2017-18', 'Relic Recovery', '', ''),
    ('2016-17', 'Velocity Vortex', '', ''),
]
SEASON_META = {year: game for year, game, _, _ in SEASONS}
KICKOFF_ANCHOR = 'kickoff-2024-09-07'
kickoff_section = next(s for p in pages if p['path'] == 'blog.html' for s in p['sections'] if '<h2>kickoff | 9/7/24</h2>' in s)
kickoff_paragraph = re.search(r'<p>(.*?)</p>', kickoff_section, re.S).group(1)
kickoff_excerpt = ' '.join(re.split(r'(?<=[.!?])\s+(?=[A-Z])', kickoff_paragraph)[:3])

def season_directory(limit=None, heading='h2'):
    rows = []
    for year, game, robot, namesake in SEASONS[:limit]:
        label = year.replace('-', '–')
        short_year = year[2:4] + '<span class="season-slash">/</span>' + year[-2:]
        base = ('' if int(year[:4]) >= 2020 else 'past-seasons/') + year + '-season'
        overview = '/' + base + '.html'
        robot_path = base + '/robot.html'
        detail = f'<p class="season-game">{html.escape(game)}</p>' if robot else ''
        if namesake:
            detail += f'<p class="season-namesake">Named after {html.escape(namesake)}.</p>'
        links = f'<a class="text-arrow" href="{overview}" aria-label="{label} season overview">Season overview</a>'
        if any(p['path'] == robot_path for p in pages):
            links += f'<a class="text-arrow" href="/{robot_path}" aria-label="{label} robot">Robot</a>'
        rows.append(f'<article class="season-entry"><p class="season-year" aria-label="{label}"><span aria-hidden="true">{short_year}</span></p><div class="season-identity"><{heading}>{html.escape(robot or game)}</{heading}>{detail}</div><div class="season-entry-links">{links}</div></article>')
    return '<div class="season-directory">' + ''.join(rows) + '</div>'

HOME = HOME.replace('<!-- SEASON_DIRECTORY -->', season_directory(3, 'h3')).replace('<!-- KICKOFF_EXCERPT -->', kickoff_excerpt)

def clean_section(section):
    # Preserve the original words while removing the scrape's inconsistent casing.
    heading_case = {
        'BACK TO SCHOOL (AND THIS BLOG) | 8/29/24': 'Back to school (and this blog) | 8/29/24',
        'COMMUNITY Partnerships': 'Community Partnerships',
        'CURIOSITY CARES': 'Curiosity Cares',
        'Championship UPDATES | 4/19/21': 'Championship updates | 4/19/21',
        'KICKOFF | 9/18/21': 'Kickoff | 9/18/21',
        'ROBOT: Katherine droneson': 'Robot: Katherine Droneson',
        'ROBOT: Mae Jemicone': 'Robot: Mae Jemicone',
        'ROBOT: ROSALIND PLANKTON': 'Robot: Rosalind Plankton',
        'dIRECT SUPPORT FROM CURIOSITY (ONLINE MEETING + FEEDBACK)': 'Direct support from Curiosity (online meeting + feedback)',
        'fEMALE EMPOWERMENT SUMMIT | jAGDeEP SHERGILL': 'Female Empowerment Summit | Jagdeep Shergill',
        'feedback (2-8 PAGE DOCUMENT WITH SUGGESTIONS/EDITS)': 'Feedback (2-8 page document with suggestions/edits)',
        'Supporting women in stem': 'Supporting women in STEM',
        'Get In Touch with us!': 'Get in touch with us!',
        'kickoff | 9/7/24': 'Kickoff | 9/7/24',
        'qualifiers | 2/20/22': 'Qualifiers | 2/20/22',
    }
    section = re.sub(r'<h2>(.*?)</h2>', lambda m: '<h2>' + heading_case.get(m[1], m[1]) + '</h2>', section)
    def fix(m):
        url=html.unescape(m.group(1))
        if url.startswith('https://www.google.com/url?'):
            url=parse_qs(urlparse(url).query).get('q',[url])[0]
        # Correct a duplicated calendar URL present in the original scrape.
        if url.count('https://calendar.google.com/')>1:
            url=url[:url.find('https://calendar.google.com/',1)]
        return 'href="'+html.escape(url,quote=True)+'"'
    return re.sub(r'href="([^"]*)"',fix,section).replace('\ufffd','—')

def plain_text(fragment):
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).replace('\xa0', ' ').strip()

def team_roster(page):
    """Turn the scrape's mixed image/text stream into a consistent portrait directory."""
    cleaned = [clean_section(section) for section in page['sections']]
    intro = ''
    intro_match = re.search(r'<p>(Meet Curiosity[^<]+)</p>', cleaned[0], re.I) if cleaned else None
    if intro_match:
        intro = f'<p>{intro_match.group(1)}</p>'

    entries = []
    for section in cleaned:
        tokens = re.findall(r'<(h2|p)>(.*?)</\1>', section, re.S | re.I)
        consumed = set()
        for index, (tag, value) in enumerate(tokens):
            text = plain_text(value)
            if tag.lower() != 'h2' or text.lower() in {'meet the team', 'meeting the team'}:
                continue
            detail = ''
            if index + 1 < len(tokens) and tokens[index + 1][0].lower() == 'p':
                candidate = plain_text(tokens[index + 1][1])
                if not re.search(r"['’]2\d", candidate) and candidate.upper().rstrip(':') not in {'OUR CAPTAINS', 'MENTORS'}:
                    detail = candidate
                    consumed.add(index + 1)
            entries.append((text, detail))
        for index, (tag, value) in enumerate(tokens):
            if tag.lower() != 'p' or index in consumed:
                continue
            text = plain_text(value)
            marker = text.upper().rstrip(':')
            if marker in {'OUR CAPTAINS', 'MENTORS'} or text.lower().startswith('meet curiosity'):
                continue
            if text in {robot for _, _, robot, _ in SEASONS if robot}:
                continue
            if re.search(r"['’]2\d", text) or re.match(r'^(Mr|Ms|Mrs|Dr)\.', text):
                entries.append((text, ''))

    # One scraped roster contains portraits without names. Keep their absence explicit.
    image_count = sum(section.count('<img') for section in cleaned)
    if len(entries) < 3:
        entries.extend((f'[Placeholder member name {index:02d}]', '') for index in range(1, max(0, image_count - len(entries)) + 1))

    seen = set()
    unique_entries = []
    for entry in entries:
        if entry not in seen:
            unique_entries.append(entry)
            seen.add(entry)

    mentors = [entry for entry in unique_entries if re.match(r'^(Mr|Ms|Mrs|Dr)\.', entry[0])]
    members = [entry for entry in unique_entries if entry not in mentors]

    def identity(name, detail):
        match = re.match(r'^(.*?)\s*\(([^)]+)\)\s*(.*)$', name)
        if not match:
            return name, detail
        display_name = match.group(1).strip()
        role = match.group(3).strip().replace('CO-CAPTAIN', 'Co-Captain')
        metadata = match.group(2).strip()
        if role:
            metadata += ' · ' + role
        if detail:
            metadata += (' · ' if metadata else '') + detail
        return display_name, metadata

    def cards(group):
        output = []
        for name, detail in group:
            display_name, metadata = identity(name, detail)
            safe_name = html.escape(display_name)
            detail_html = f'<span>{html.escape(metadata)}</span>' if metadata else ''
            output.append(f'<figure class="member-card"><img src="/assets/design/avatar-placeholder.svg" alt="[Placeholder portrait for {safe_name}]" loading="lazy"><figcaption><strong>{safe_name}</strong>{detail_html}</figcaption></figure>')
        return ''.join(output)

    sections = []
    if intro:
        sections.append(f'<section class="team-intro">{intro}</section>')
    sections.append('<figure class="team-group-photo"><img src="/assets/placeholders/2.png" alt="[Placeholder team group photograph]" loading="lazy"><figcaption>[Placeholder caption: team · season · event]</figcaption></figure>')
    if members:
        sections.append(f'<section class="team-roster"><div class="member-grid">{cards(members)}</div></section>')
    if mentors:
        sections.append(f'<section class="team-roster team-mentors"><h2>Mentors</h2><div class="member-grid">{cards(mentors)}</div></section>')
    return sections

def page_body(page):
    title=page['title']; name=page['path']
    page_kind = ''
    if name.endswith('/robot.html'):
        page_kind = 'robot-page'
    elif name.endswith('/meet-the-team.html'):
        page_kind = 'team-page'
    elif name.endswith('/highlights.html'):
        page_kind = 'highlights-page'
    elif name.endswith('/outreach.html') or name == 'curiosity-cares.html':
        page_kind = 'outreach-page'
    elif name == 'blog.html':
        page_kind = 'blog-page'
    category='About Us' if name=='about-us.html' else 'Team Curiosity'
    if 'season' in name: category='Season archive'
    season_match=re.search(r'(20\d{2}-\d{2})-season',name)
    season_context = ''
    if season_match and season_match.group(1) in SEASON_META:
        year = season_match.group(1)
        season_context = f'<p class="season-context">{year.replace("-", "–")} / {html.escape(SEASON_META[year])}</p>'
    masthead_kind = page_kind.removesuffix('-page') if page_kind else ('season' if season_match else 'generic')
    masthead_art = ''
    if masthead_kind == 'blog':
        masthead_art = '<time class="masthead-date">9 / 7 / 24</time>'
    hero=f'''<section class="page-hero section-pad"><div class="masthead-top"><div><a class="breadcrumb" href="/home.html">Home /</a><span class="eyebrow">{category}</span></div>{season_context}</div><div class="masthead-title"><h1>{html.escape(title)}</h1></div><div class="masthead-art" aria-hidden="true">{masthead_art}</div></section>'''
    sibling=''
    nav_season_match=re.match(r'(202[0-4]-\d{2})-season',name)
    if nav_season_match:
        season=nav_season_match.group(1)+'-season'
        options=[(season+'.html','Overview'),(season+'/robot.html','Robot'),(season+'/meet-the-team.html','Meet the Team'),(season+'/highlights.html','Highlights'),(season+'/outreach.html','Outreach')]
        sibling='<nav class="section-nav" aria-label="Season navigation">'+''.join(f'<a href="/{u}"'+(' aria-current="page"' if u==name else '')+f'>{t}</a>' for u,t in options if any(p['path']==u for p in pages))+'</nav>'
    parts=[]
    source_sections = [] if page_kind == 'team-page' else page['sections']
    for i,section in enumerate(source_sections):
        section=clean_section(section)
        if page_kind == 'robot-page':
            section = re.sub(r'<p>\s*([A-Za-z][A-Za-z /&amp;-]{1,30}):\s*(.*?)</p>', r'<p class="robot-spec"><strong>\1</strong><span>\2</span></p>', section, flags=re.S)
            section = re.sub(r'<img\b[^>]*>', '', section)
        elif page_kind == 'team-page':
            section = section.replace('<p>OUR CAPTAINS:</p>', '<h2>Our captains</h2>').replace('<p>MENTORS</p>', '<h2>Mentors</h2>')
        elif page_kind == 'highlights-page':
            section = re.sub(r'<p>(At [^<]+:)</p>', r'<h2 class="highlight-event">\1</h2>', section)
        elif page_kind == 'blog-page':
            section = re.sub(r'<h2>(.*?)\s*\|\s*([^<]+)</h2>', r'<h2><span>\1</span><time>\2</time></h2>', section)
        if i==0:
            section=re.sub(r'^<h2>.*?</h2>\s*','',section,count=1,flags=re.S)
        photos=re.findall(r'<img\b[^>]*>',section)
        if len(photos)>1:
            section=re.sub(r'<img\b[^>]*>','',section)
            section+='<div class="editorial-gallery">'+''.join(photos)+'</div>'
        if page_kind == 'robot-page':
            detail_index = 0
            def add_mechanism_detail(match):
                nonlocal detail_index
                detail_index += 1
                detail = ''
                if detail_index in (2, 4):
                    variant = 'a' if detail_index == 2 else 'b'
                    detail = f'<figure class="mechanism-detail mechanism-detail-{variant}"><img src="/assets/placeholders/robot-cad.png" alt="[Placeholder mechanism detail image]"><figcaption>[Placeholder mechanism label]</figcaption></figure>'
                return match.group(0) + detail
            section = re.sub(r'<p class="robot-spec">.*?</p>', add_mechanism_detail, section, flags=re.S)
        anchor = f' id="{KICKOFF_ANCHOR}"' if name == 'blog.html' and page['sections'][i] == kickoff_section else ''
        if section.strip(): parts.append(f'<section class="editorial-block"{anchor}><span class="block-index">{len(parts)+1:02d} /</span><div class="editorial-content">{section}</div></section>')
    if page_kind == 'team-page':
        parts = team_roster(page)
    if page_kind == 'robot-page':
        existing_details = sum(part.count('mechanism-detail mechanism-detail-') for part in parts)
        for detail_number in range(existing_details, 2):
            variant = 'a' if detail_number == 0 else 'b'
            fallback_detail = f'<figure class="mechanism-detail mechanism-detail-{variant}"><img src="/assets/placeholders/robot-cad.png" alt="[Placeholder mechanism detail image]"><figcaption>[Placeholder mechanism label]</figcaption></figure>'
            parts.insert(min(len(parts), detail_number + 1), fallback_detail)
    if name=='past-seasons.html':
        parts = ['<p class="archive-intro">Click to learn more about each of our past seasons:</p>', season_directory()]
    if name=='about-us.html':
        parts.insert(0,'<figure class="page-photo caption-crop"><img src="/assets/placeholders/3.png" alt="Curiosity team celebrating together"><figcaption>[Placeholder caption: Team Curiosity · Los Angeles]</figcaption></figure>')
    if page_kind == 'outreach-page':
        parts.insert(0,'<figure class="outreach-collage"><img src="/assets/placeholders/2.png" alt="[Placeholder candid team photograph]" loading="lazy"><img src="/assets/placeholders/3.png" alt="[Placeholder outreach photograph]" loading="lazy"><figcaption>[Placeholder caption: season · activity · location]</figcaption></figure>')
    if page_kind == 'robot-page':
        parts.insert(0,'<figure class="robot-showcase"><div class="robot-visual robot-visual-cad"><img src="/assets/placeholders/robot-cad.png" alt="CAD rendering of a Curiosity competition robot"></div><div class="robot-visual robot-visual-built"><img src="/assets/placeholders/robot-built.jpg" alt="Photograph of a Curiosity competition robot"></div></figure>')
    if re.fullmatch(r'202[0-4]-\d{2}-season.html',name):
        year = name[:7]
        parts.insert(0,f'<figure class="page-photo"><img src="/assets/placeholders/1.png" alt="Team Curiosity in the competition pit - placeholder photo"><figcaption>[Placeholder caption: {year.replace("-", "–")} · {html.escape(SEASON_META[year])} · event/location]</figcaption></figure>')
    if name=='contact.html':
        parts.insert(0,'<div class="contact-lead"><p>We’d love to hear from you.</p>'+link('mailto:team11770@marlborough.org','team11770@marlborough.org','text-arrow')+'</div>')
    season_robot_class = ''
    if page_kind == 'robot-page' and season_match:
        season_robot_class = ' robot-season-' + season_match.group(1)
    content_class = 'page-content section-pad' + (f' {page_kind}{season_robot_class}' if page_kind else '')
    rendered_parts = ''.join(parts).replace('<div class="editorial-gallery">', '<div class="editorial-gallery gallery-featured">', 1)
    if page_kind in {'highlights-page', 'outreach-page'}:
        rendered_parts = re.sub(r'(<div class="editorial-gallery gallery-featured">.*?</div>)', r'\1<p class="editorial-caption">[Placeholder caption: season · event · location]</p>', rendered_parts, count=1, flags=re.S)
    masthead = f'<div class="page-masthead masthead-{masthead_kind}">{hero}{sibling}</div>'
    return masthead+f'<div class="{content_class}">'+rendered_parts+'</div>'

for page in pages:
    title='Curiosity - FTC #11770' if page['path']=='home.html' else page['title']+' | Curiosity 11770'
    body=HOME if page['path']=='home.html' else page_body(page)
    output=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0b0b0b"><meta name="description" content="Curiosity 11770. A robotics team of girls and gender minorities from Marlborough School, Los Angeles. Participating in FIRST Tech Challenge since 2016."><title>{html.escape(title)}</title><link rel="icon" href="/assets/design/team-logo-red.svg?v=20260919" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/design/site.css?v=20260919s"><script src="/assets/design/site.js?v=20260919b" defer></script></head><body id="top">{nav(page['path'])}<main id="main">{body}</main>{footer()}</body></html>'''
    (ROOT/page['path']).write_text(output,encoding='utf-8')
print(f'Built {len(pages)} pages.')
