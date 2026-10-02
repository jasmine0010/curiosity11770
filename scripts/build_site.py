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
    items=[('about-us.html','About Us'),('curiosity-cares.html','Curiosity Cares'),('past-seasons.html','Past Seasons'),('blog.html','Blog')]
    def active(item):
        if item == current:
            return True
        if item == 'past-seasons.html' and (current.startswith('past-seasons/') or (re.match(r'20\d{2}-\d{2}-season(?:/|\.html)', current) and not current.startswith('2024-25-season'))):
            return True
        return False
    primary_links = ''.join(f'<a href="/{u}"'+(' aria-current="page"' if active(u) else '')+f'>{t}</a>' for u,t in items)
    home_current = ' aria-current="page"' if current == 'home.html' else ''
    portfolio_current = ' aria-current="page"' if current == 'portfolio-support.html' else ''
    summit_current = ' aria-current="page"' if current == 'female-empowerment-summit.html' else ''
    peer_links = f'''<a href="/constellation/home.html">Constellation</a><a href="/constellation/north-star-resources.html">Resources</a><a href="/portfolio-support.html"{portfolio_current}>Portfolio Support</a><a href="/female-empowerment-summit.html"{summit_current}>Female Empowerment Summit</a>'''
    partners_current = ' aria-current="page"' if current == 'professional-partners.html' else ''
    peer_links += f'<a href="/professional-partners.html"{partners_current}>Professional Partners</a>'
    community_current = ' aria-current="page"' if current == 'community-partners.html' else ''
    peer_links += f'<a href="/community-partners.html"{community_current}>Community Partners</a>'
    mobile_peer_links = peer_links.replace('<a ', '<a class="nav-peer-mobile" ')
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/home.html" aria-label="Curiosity 11770 home">{MARK}<span>Curiosity<small>Robotics · 11770</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span>+</span></button><nav id="site-nav" aria-label="Main navigation"><a class="nav-mobile-only nav-home" href="/home.html"{home_current}>Home</a>{primary_links}<a class="nav-contact" href="/contact.html"{' aria-current="page"' if current == 'contact.html' else ''}>Contact</a><button class="nav-more-toggle" aria-expanded="false" aria-controls="nav-more-panel">More <span aria-hidden="true">+</span></button>{mobile_peer_links}<div class="nav-more-panel" id="nav-more-panel">{peer_links}</div></nav></header>'''
def footer(current):
    contact_icons = '''<div class="footer-contact-links">
<a href="mailto:team11770@marlborough.org" aria-label="Email Curiosity" title="Email"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14"/><path d="m3 6 9 7 9-7"/></svg></a>
<a href="https://www.instagram.com/curiosity11770/" aria-label="Curiosity on Instagram" title="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor" stroke="none"/></svg></a>
<a href="https://calendar.google.com/calendar/u/0/appointments/schedules/AcZssZ1Sw3Eg1f-OWK_ZqXltUXvDKfFpQQPkXNSiPlyMK_eExfI_SwNIidLi9rAYx8wHGO8Br6H7qF9a" aria-label="Schedule a meeting with Curiosity" title="Schedule a meeting"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16v16H4zM4 10h16M8 2v6M16 2v6M8 14h3M13 14h3M8 17h3"/></svg></a>
</div>'''
    top = '' if current == 'contact.html' else '<div class="footer-top"><a class="footer-cta" href="/contact.html">Connect with Us!</a>'+contact_icons+'</div>'
    return f'''<footer class="site-footer">{top}<div class="footer-bottom"><a class="brand" href="/home.html">{FOOTER_MARK}<span>Curiosity<small>Robotics · 11770</small></span></a><p>Marlborough School<br>Los Angeles, California</p><div><a href="https://www.instagram.com/curiosity11770/" target="_blank" rel="noopener noreferrer">Instagram</a><a href="mailto:team11770@marlborough.org">Email</a></div><div><a href="/professional-partners.html">Professional Partners</a><a href="/community-partners.html">Community Partners</a><a href="/constellation/home.html">Constellation</a><a href="/constellation/north-star-resources.html">Resources</a></div></div><div class="colophon"><span>© Team Curiosity 11770</span><span>Courage. Connection. Collaboration.</span><a href="#top">Back to top</a></div></footer>'''
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

def season_directory(limit=None, heading='h2', use_game_names=False):
    rows = []
    for year, game, robot, namesake in SEASONS[:limit]:
        label = year.replace('-', '–')
        base = ('' if int(year[:4]) >= 2020 else 'past-seasons/') + year + '-season'
        overview = '/' + base + '.html'
        robot_path = base + '/robot.html'
        title = game if use_game_names else robot or game
        detail = f'<p class="season-game">{html.escape(game)}</p>' if robot and not use_game_names else ''
        links = f'<a class="text-arrow" href="{overview}" aria-label="{label} season overview">Season overview</a>'
        if any(p['path'] == robot_path for p in pages):
            links += f'<a class="text-arrow" href="/{robot_path}" aria-label="{label} robot">Robot</a>'
        rows.append(f'<article class="season-entry"><p class="season-year">{label}</p><div class="season-identity"><{heading}>{html.escape(title)}</{heading}>{detail}<div class="season-entry-links">{links}</div></div></article>')
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
    return re.sub(r'href="([^"]*)"',fix,section).replace('\ufffd','–').replace('—','–')

def normalize_site_text(value):
    """Keep season labels consistent and avoid em dashes in public output."""
    value = value.replace('—', '–')
    return re.sub(r'\b(20\d{2})\s*-\s*(\d{2})(?=\s+Season\b)', r'\1–\2', value)

def plain_text(fragment):
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).replace('\xa0', ' ').strip()

def team_roster(page):
    """Turn the scrape's mixed image/text stream into a consistent portrait directory."""
    cleaned = [clean_section(section) for section in page['sections']]
    intro = ''
    intro_match = re.search(r'<p>(Meet Curiosity[^<]+)</p>', cleaned[0], re.I) if cleaned else None
    if intro_match:
        intro = f'<p>{intro_match.group(1)}</p>'

    if page.get('profile_cards'):
        cards = ''.join(f'<figure class="member-card"><img class="member-profile-card" src="{html.escape(card["src"], quote=True)}" alt="{html.escape(card["alt"], quote=True)}" loading="lazy"></figure>' for card in page['profile_cards'])
        sections = [f'<section class="team-intro">{intro}</section>'] if intro else []
        sections.append(f'<section class="team-roster"><div class="member-grid">{cards}</div></section>')
        return sections

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
            portraits = page.get('portraits', {})
            portrait = portraits.get(display_name.lower()) or portraits.get(display_name.split()[0].lower())
            portrait_src = html.escape(portrait or '/assets/design/avatar-placeholder.svg', quote=True)
            portrait_alt = f'Illustrated portrait of {safe_name}' if portrait else f'[Placeholder portrait for {safe_name}]'
            portrait_class = ' class="member-illustration"' if portrait else ''
            if portrait and page.get('portrait_style') == 'photo':
                portrait_alt = f'Portrait of {safe_name}'
                portrait_class = ' class="member-photo"'
            output.append(f'<figure class="member-card"><img{portrait_class} src="{portrait_src}" alt="{portrait_alt}" loading="lazy"><figcaption><strong>{safe_name}</strong>{detail_html}</figcaption></figure>')
        return ''.join(output)

    sections = []
    if intro:
        sections.append(f'<section class="team-intro">{intro}</section>')
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
    elif name == 'contact.html':
        page_kind = 'contact-page'
    category='About Us' if name=='about-us.html' else 'Team Curiosity'
    if 'season' in name: category='Season archive'
    season_match=re.search(r'(20\d{2}-\d{2})-season',name)
    season_context = ''
    if season_match and season_match.group(1) in SEASON_META:
        year = season_match.group(1)
        season_context = f'<p class="season-context">{year.replace("-", "–")} / {html.escape(SEASON_META[year])}</p>'
    masthead_kind = page_kind.removesuffix('-page') if page_kind else ('season' if season_match else 'generic')
    masthead_art = ''
    header_title = html.escape(title)
    if name == 'female-empowerment-summit.html':
        masthead_kind = 'summit'
        header_title = '<span>Female Empowerment</span> <span>Summit</span>'
    if masthead_kind == 'blog':
        masthead_art = '<time class="masthead-date">9 / 7 / 24</time>'
    crumbs = ['<a href="/home.html">Home</a>']
    if season_match:
        crumbs.append('<a href="/past-seasons.html">Season archive</a>')
        if '/' in name and not name.startswith('past-seasons/'):
            season_url = '/' + season_match.group(1) + '-season.html'
            season_label = season_match.group(1).replace('-', '–')
            crumbs.append(f'<a href="{season_url}">{season_label}</a>')
    crumbs.append(f'<span aria-current="page">{html.escape(title)}</span>')
    breadcrumb = '<nav class="page-breadcrumb" aria-label="Breadcrumb">' + '<span class="breadcrumb-separator" aria-hidden="true">/</span>'.join(crumbs) + '</nav>'
    hero=f'''<section class="page-hero section-pad"><div class="masthead-top">{breadcrumb}{season_context}</div><div class="masthead-title"><h1>{header_title}</h1></div><div class="masthead-art" aria-hidden="true">{masthead_art}</div></section>'''
    sibling=''
    nav_season_match=re.match(r'(202[0-4]-\d{2})-season',name)
    if nav_season_match:
        season=nav_season_match.group(1)+'-season'
        options=[(season+'.html','Overview'),(season+'/robot.html','Robot'),(season+'/meet-the-team.html','Meet the Team'),(season+'/highlights.html','Highlights'),(season+'/outreach.html','Outreach')]
        sibling='<nav class="section-nav" aria-label="Season navigation">'+''.join(f'<a href="/{u}"'+(' aria-current="page"' if u==name else '')+f'>{t}</a>' for u,t in options if any(p['path']==u for p in pages))+'</nav>'
    if name == 'contact.html':
        contact_content = (ROOT / 'content/contact.html').read_text(encoding='utf-8')
        return f'<div class="page-masthead masthead-{masthead_kind}">{hero}</div><div class="page-content section-pad contact-page">{contact_content}</div>'
    parts=[]
    source_sections = [] if page_kind == 'team-page' else page['sections']
    for i,section in enumerate(source_sections):
        section=clean_section(section)
        if page_kind == 'robot-page':
            if not page.get('robot_specs_inline'):
                section = re.sub(r'<p>\s*([A-Za-z][A-Za-z /&amp;-]{1,60}):\s*(.*?)</p>', r'<p class="robot-spec"><strong>\1</strong><span>\2</span></p>', section, flags=re.S)
            section = re.sub(r'<img\b[^>]*>', '', section)
        elif page_kind == 'team-page':
            section = section.replace('<p>OUR CAPTAINS:</p>', '<h2>Our captains</h2>').replace('<p>MENTORS</p>', '<h2>Mentors</h2>')
        elif page_kind == 'highlights-page':
            section = re.sub(r'<p>(At [^<]+:)</p>', r'<h2 class="highlight-event">\1</h2>', section)
            section = re.sub(r'(<p>League Champions.*?</p>)', r'<h2 class="highlight-event">League results</h2>\1', section, flags=re.S)
            section = re.sub(r'(?:<p>.*?</p>\s*)+', lambda match: '<ul class="highlight-list">' + re.sub(r'<p>(.*?)</p>', r'<li>\1</li>', match.group(0), flags=re.S) + '</ul>', section, flags=re.S)
        elif page_kind == 'blog-page':
            section = re.sub(r'<h2>(.*?)\s*\|\s*([^<]+)</h2>', r'<h2><span>\1</span><time>\2</time></h2>', section)
        if i==0:
            section=re.sub(r'^<h2>.*?</h2>\s*','',section,count=1,flags=re.S)
        photos=re.findall(r'<img\b[^>]*>',section)
        if len(photos)>1 and name not in {'professional-partners.html', 'community-partners.html'}:
            section=re.sub(r'<img\b[^>]*>','',section)
            section+='<div class="editorial-gallery">'+''.join(photos)+'</div>'
        if page_kind == 'robot-page' and not page.get('robot_images'):
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
        if section.strip():
            index = '' if page_kind == 'highlights-page' else f'<span class="block-index">{len(parts)+1:02d} /</span>'
            parts.append(f'<section class="editorial-block"{anchor}>{index}<div class="editorial-content">{section}</div></section>')
    if page_kind == 'team-page':
        parts = team_roster(page)
    if page_kind == 'robot-page' and not page.get('robot_images'):
        existing_details = sum(part.count('mechanism-detail mechanism-detail-') for part in parts)
        for detail_number in range(existing_details, 2):
            variant = 'a' if detail_number == 0 else 'b'
            fallback_detail = f'<figure class="mechanism-detail mechanism-detail-{variant}"><img src="/assets/placeholders/robot-cad.png" alt="[Placeholder mechanism detail image]"><figcaption>[Placeholder mechanism label]</figcaption></figure>'
            parts.insert(min(len(parts), detail_number + 1), fallback_detail)
    if name=='past-seasons.html':
        parts = ['<p class="archive-intro">Click to learn more about each of our past seasons:</p>', season_directory(use_game_names=True)]
    if name=='about-us.html':
        parts.insert(0,'<figure class="page-photo about-team-photo"><img src="/assets/general/about-team.png" alt="Curiosity team celebrating the 2024–25 SoCal Championship Inspire Award with their banner and trophy."></figure>')
    if page_kind == 'outreach-page' and not page.get('hide_outreach_collage') and not page.get('outreach_photo') and not page.get('outreach_images'):
        parts.insert(0,'<figure class="outreach-collage"><img src="/assets/placeholders/2.png" alt="[Placeholder candid team photograph]" loading="lazy"><img src="/assets/placeholders/3.png" alt="[Placeholder outreach photograph]" loading="lazy"><figcaption>[Placeholder caption: season · activity · location]</figcaption></figure>')
    if page_kind == 'robot-page' and not page.get('robot_images'):
        parts.insert(0,'<figure class="robot-showcase"><div class="robot-visual robot-visual-cad"><img src="/assets/placeholders/robot-cad.png" alt="CAD rendering of a Curiosity competition robot"></div><div class="robot-visual robot-visual-built"><img src="/assets/placeholders/robot-built.jpg" alt="Photograph of a Curiosity competition robot"></div></figure>')
    if re.fullmatch(r'202[0-4]-\d{2}-season.html',name) and not page.get('overview_images'):
        year = name[:7]
        parts.insert(0,f'<figure class="page-photo"><img src="/assets/placeholders/1.png" alt="Team Curiosity in the competition pit - placeholder photo"><figcaption>[Placeholder caption: {year.replace("-", "–")} · {html.escape(SEASON_META[year])} · event/location]</figcaption></figure>')
    if page.get('portfolio_pdf') and page.get('overview_images'):
        lead = page['overview_images'][0]
        parts.append(f'<figure class="season-portfolio-photo"><img src="{html.escape(lead["src"], quote=True)}" alt="{html.escape(lead["alt"], quote=True)}" loading="lazy"></figure>')
    if page.get('portfolio_pdf'):
        pdf_src = html.escape(page['portfolio_pdf'], quote=True)
        portfolio = f'<div class="season-portfolio-document"><object data="{pdf_src}#view=FitH" type="application/pdf" aria-label="2020–21 Curiosity Engineering Portfolio"><p><a href="{pdf_src}">View the engineering portfolio PDF</a></p></object></div>'
        parts = [f'<div class="season-portfolio-layout">{portfolio}<div class="season-portfolio-copy">' + ''.join(parts) + '</div></div>']
    if page.get('overview_images'):
        images = page['overview_images']
        lead = images[0]
        if page.get('overview_layout') == 'asymmetric-pairs':
            side = page['overview_side_image']
            parts.insert(0, f'<div class="season-overview-opening"><figure><img src="{html.escape(lead["src"], quote=True)}" alt="{html.escape(lead["alt"], quote=True)}" loading="lazy"></figure><figure><img src="{html.escape(side["src"], quote=True)}" alt="{html.escape(side["alt"], quote=True)}" loading="lazy"></figure></div>')
        if not page.get('portfolio_pdf') and page.get('overview_layout') not in {'stacked', 'mosaic', 'asymmetric-pairs'}:
            parts.insert(0, f'<figure class="season-overview-lead"><img src="{html.escape(lead["src"], quote=True)}" alt="{html.escape(lead["alt"], quote=True)}" loading="lazy"></figure>')
        photos = ''.join(f'<figure><img src="{html.escape(image["src"], quote=True)}" alt="{html.escape(image["alt"], quote=True)}" loading="lazy"></figure>' for image in images[1:])
        if page.get('overview_layout') == 'mosaic':
            parts.insert(0, f'<div class="season-overview-mosaic"><figure><img src="{html.escape(lead["src"], quote=True)}" alt="{html.escape(lead["alt"], quote=True)}" loading="lazy"></figure>{photos}</div>')
        elif page.get('overview_layout') == 'stacked':
            parts.insert(0, f'<div class="season-overview-feature"><figure class="season-overview-feature-main"><img src="{html.escape(lead["src"], quote=True)}" alt="{html.escape(lead["alt"], quote=True)}" loading="lazy"></figure><div class="season-overview-side">{photos}</div></div>')
        elif page.get('portfolio_pdf'):
            parts.insert(0, f'<div class="season-overview-photos season-overview-photos-top">{photos}</div>')
        elif photos:
            gallery_class = ' season-overview-pairs' if page.get('overview_layout') == 'gallery-pairs' else ''
            if page.get('overview_layout') == 'asymmetric-pairs':
                gallery_class = ' season-overview-asymmetric'
            if page.get('overview_gallery_reverse_widths'):
                gallery_class += ' season-overview-reverse-widths'
            parts.append(f'<div class="season-overview-photos{gallery_class}">{photos}</div>')
    if page.get('robot_images'):
        images = page['robot_images']
        lead = images[0]
        lead_src = html.escape(lead['src'], quote=True)
        lead_alt = html.escape(lead['alt'], quote=True)
        supporting = ''.join(f'<figure><img src="{html.escape(image["src"], quote=True)}" alt="{html.escape(image["alt"], quote=True)}" loading="lazy"></figure>' for image in images[1:])
        gallery_class = ' robot-documentation-featured' if page.get('robot_layout') == 'featured-details' else ''
        gallery_position = 1 if page.get('robot_images_after_intro') else 0
        if page.get('robot_layout') == 'into-the-deep':
            photos = ''.join(f'<figure><img src="{html.escape(image["src"], quote=True)}" alt="{html.escape(image["alt"], quote=True)}" loading="lazy"></figure>' for image in images)
            parts.insert(gallery_position, f'<div class="robot-deep-grid">{photos}</div>')
        elif page.get('robot_layout') == 'center-lift':
            photos = ''.join(f'<figure><img src="{html.escape(image["src"], quote=True)}" alt="{html.escape(image["alt"], quote=True)}" loading="lazy"></figure>' for image in images)
            parts.insert(gallery_position, f'<div class="robot-mechanism-grid">{photos}</div>')
        else:
            parts.insert(gallery_position, f'<div class="robot-documentation{gallery_class}"><figure class="robot-concept-sheet"><a href="{lead_src}" target="_blank" rel="noopener" aria-label="Open the full-size robot concept sheet"><img src="{lead_src}" alt="{lead_alt}"></a></figure><div class="robot-supporting-photos">{supporting}</div></div>')
    if page.get('outreach_images'):
        images = page['outreach_images']
        poster = images[0]
        poster_src = html.escape(poster['src'], quote=True)
        poster_alt = html.escape(poster['alt'], quote=True)
        photos = ''.join(f'<figure><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></figure>' for photo in images[1:])
        parts.insert(0, f'<div class="outreach-documentation"><figure class="outreach-poster"><a href="{poster_src}" target="_blank" rel="noopener" aria-label="Open the full-size outreach poster"><img src="{poster_src}" alt="{poster_alt}"></a></figure><div class="outreach-supporting-photos">{photos}</div></div>')
    if page.get('outreach_photo'):
        photo = page['outreach_photo']
        parts.append(f'<figure class="outreach-closing-photo"><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></figure>')
    if page.get('highlight_images'):
        images = page['highlight_images']
        if page.get('highlight_layout') == 'split-pairs':
            top_photos = ''.join(f'<figure><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></figure>' for photo in images[:2])
            parts.insert(0, f'<div class="highlight-photo-row highlight-photo-top">{top_photos}</div>')
            images = images[2:]
        photos = ''.join(f'<figure><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></figure>' for photo in images)
        photo_class = ' highlight-photo-trio' if len(images) == 3 else ''
        if page.get('highlight_layout') == 'natural-trio':
            photo_class += ' highlight-photo-natural'
        parts.append(f'<div class="highlight-photo-row{photo_class}">{photos}</div>')
    season_robot_class = ''
    if page.get('archive_posters'):
        posters = ''.join(f'<figure><a href="{html.escape(photo["src"], quote=True)}" target="_blank" rel="noopener" aria-label="Open full-size poster"><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></a></figure>' for photo in page['archive_posters'])
        poster_class = ' archive-poster-stack' if page.get('archive_poster_layout') == 'stacked' else ''
        if page.get('archive_poster_layout') == 'trio':
            poster_class = ' archive-poster-trio'
        parts.insert(0, f'<div class="archive-poster-gallery{poster_class}">{posters}</div>')
    if page.get('archive_images'):
        photos = ''.join(f'<figure><img src="{html.escape(photo["src"], quote=True)}" alt="{html.escape(photo["alt"], quote=True)}" loading="lazy"></figure>' for photo in page['archive_images'])
        parts.append(f'<div class="archive-photo-gallery">{photos}</div>')
    if page_kind == 'robot-page' and season_match:
        season_robot_class = ' robot-season-' + season_match.group(1)
    content_class = 'page-content section-pad' + (f' {page_kind}{season_robot_class}' if page_kind else '')
    if name in {'professional-partners.html', 'community-partners.html'}:
        content_class += ' partners-page'
    if name == 'curiosity-cares.html':
        content_class += ' cares-page'
    if name == 'portfolio-support.html':
        content_class += ' portfolio-support-page'
    if page.get('overview_images'):
        content_class += ' season-overview-page'
    if re.fullmatch(r'202[0-4]-\d{2}-season(?:/(?:robot|meet-the-team|highlights|outreach))?\.html', name):
        content_class += ' season-page-content'
    rendered_parts = ''.join(parts).replace('<div class="editorial-gallery">', '<div class="editorial-gallery gallery-featured">', 1)
    if page_kind in {'highlights-page', 'outreach-page'}:
        rendered_parts = re.sub(r'(<div class="editorial-gallery gallery-featured">.*?</div>)', r'\1<p class="editorial-caption">[Placeholder caption: season · event · location]</p>', rendered_parts, count=1, flags=re.S)
    archive_class = " archive-masthead" if name == "past-seasons.html" else (" masthead-robot-documented" if page.get('robot_images') else "")
    if page.get('robot_images') and season_match:
        archive_class += ' masthead-robot-' + season_match.group(1)
    if name == '2020-21-season/meet-the-team.html':
        archive_class += ' masthead-team-2020-21'
    if name == '2020-21-season/outreach.html':
        archive_class += ' masthead-outreach-2020-21'
    if name == '2020-21-season.html':
        archive_class += ' masthead-overview-2020-21'
    header_2021 = {
        '2021-22-season.html': 'overview',
        '2021-22-season/meet-the-team.html': 'team',
        '2021-22-season/highlights.html': 'highlights',
        '2021-22-season/outreach.html': 'outreach',
    }.get(name)
    if header_2021:
        archive_class += f' masthead-{header_2021}-2021-22'
    header_2022 = {
        '2022-23-season.html': 'overview',
        '2022-23-season/meet-the-team.html': 'team',
        '2022-23-season/highlights.html': 'highlights',
    }.get(name)
    if header_2022:
        archive_class += f' masthead-{header_2022}-2022-23'
    header_2023 = {
        '2023-24-season.html': 'overview',
        '2023-24-season/meet-the-team.html': 'team',
        '2023-24-season/highlights.html': 'highlights',
    }.get(name)
    if header_2023:
        archive_class += f' masthead-{header_2023}-2023-24'
    header_2024 = {
        '2024-25-season.html': 'overview',
        '2024-25-season/meet-the-team.html': 'team',
        '2024-25-season/highlights.html': 'highlights',
    }.get(name)
    if header_2024:
        archive_class += f' masthead-{header_2024}-2024-25'
    masthead = f'<div class="page-masthead masthead-{masthead_kind}{archive_class}">{hero}{sibling}</div>'
    return masthead+f'<div class="{content_class}">'+rendered_parts+'</div>'

for page in pages:
    title='Curiosity - FTC #11770' if page['path']=='home.html' else page['title']+' | Curiosity 11770'
    body=HOME if page['path']=='home.html' else page_body(page)
    output=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0b0b0b"><meta name="description" content="Curiosity 11770. A robotics team of girls and gender minorities from Marlborough School, Los Angeles. Participating in FIRST Tech Challenge since 2016."><title>{html.escape(title)}</title><link rel="icon" href="/assets/design/team-logo-red.svg?v=20260919" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/design/site.css?v=20260919s"><link rel="stylesheet" href="/assets/design/typography.css?v=20261002b"><script src="/assets/design/site.js?v=20260923a" defer></script></head><body id="top">{nav(page['path'])}<main id="main">{body}</main>{footer(page['path'])}</body></html>'''
    output = normalize_site_text(output).replace('site.css?v=20260919s', 'site.css?v=20261003t').replace('site.js?v=20260923a', 'site.js?v=20261002b')
    (ROOT/page['path']).write_text(output,encoding='utf-8')
print(f'Built {len(pages)} pages.')

from build_constellation import build as build_constellation
build_constellation()

