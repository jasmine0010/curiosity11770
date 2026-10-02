"""Build Constellation from editable local content (Python standard library only)."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
import json

ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'content/constellation'
ASSETS=ROOT/'assets/constellation'

class TextOnly(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)

def text_only(markup):
    parser=TextOnly();parser.feed(markup)
    return ' '.join(' '.join(parser.parts).split())

def build():
    pages=json.loads((CONTENT/'pages.json').read_text(encoding='utf-8'))
    stars=json.loads((CONTENT/'map.json').read_text(encoding='utf-8'))
    def link(slug,label):return f'<a href="/constellation/{escape(slug)}.html">{escape(label)}</a>'
    def group(title,root):
        children=[p for p in pages if p['slug'].startswith(root+'/')]
        return '<details><summary>'+escape(title)+'</summary><div class="c-dropdown">'+link(root,'Overview')+''.join(link(p['slug'],p['title']) for p in children)+'</div></details>'
    nav=link('home','Home')+'<a class="c-curiosity-link" href="/home.html">Curiosity Home Site</a>'
    nav+=group('North Star | Resources','north-star-resources')
    nav+=group('TRANSLATED North Star | Resources','translated-north-star-resources')
    nav+='<details><summary>More</summary><div class="c-dropdown">'+''.join(link(p['slug'],p['title']) for p in pages if '/' not in p['slug'] and 'north-star' not in p['slug'])+'</div></details>'
    header=f'''<a class="c-skip" href="#main">Skip to content</a>
<header class="c-header"><a class="c-brand" href="/constellation/home.html" aria-label="Constellation home"><span class="c-brand-mark" aria-hidden="true">✳</span><span><strong>Constellation</strong></span></a><button class="c-menu" type="button" aria-controls="c-nav" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button><nav id="c-nav" aria-label="Main navigation">{nav}</nav><button class="c-search-toggle" type="button" aria-label="Search Constellation" aria-expanded="false" aria-controls="c-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6"/></svg></button></header>
<section id="c-search" class="c-search" hidden><div class="c-search-inner"><div class="c-search-heading"><label for="c-query">Search Constellation</label><button class="c-search-close" type="button">Close search</button></div><input type="search" id="c-query" placeholder="Search resources, guides, and teams" autocomplete="off"><p id="c-search-status" role="status"></p><ul id="c-results"></ul></div></section>'''
    index=[]
    all_pages=[{'slug':'home','title':'Constellation','source':'https://constellation.curiosity11770.marlborough.org/home'}]+pages
    for p in all_pages:
        home=p['slug']=='home'
        current_url='/constellation/'+p['slug']+'.html'
        page_header=header.replace(f'href="{current_url}"',f'href="{current_url}" aria-current="page"')
        if home:
            nodes=[]
            for star in stars['stars']:
                position=star.get('position','')
                designation=star.get('designation','')
                nodes.append(f'<a id="{escape(star["id"])}" class="star-link {escape(star["class"].replace("nav-star", "").replace("north-star", "is-north"))}" href="{escape(star["href"])}" style="{escape(position)}"><span class="nav-star {"north-star" if "north-star" in star["class"] else ""}" aria-hidden="true"></span><span class="star-designation" aria-hidden="true">{escape(designation)}</span><span class="star-label">{escape(star["label"])}</span></a>')
            connections=''.join(f'<div class="star-connection" data-from="{a}" data-to="{b}" aria-hidden="true"></div>' for a,b in stars['connections'])
            list_items=''.join(f'<a href="{escape(star["href"])}">{escape(star["label"])}</a>' for star in stars['stars'])
            field_nodes=[]
            for point in stars.get('fieldStars',[]):
                size=point['size'];tone=point['tone']
                if size not in ('micro','minor') or tone not in ('cool','neutral','warm'):
                    raise ValueError('Invalid chart point style')
                x=float(point['x']);y=float(point['y'])
                if not (0<=x<=100 and 0<=y<=100):raise ValueError('Chart point outside plate')
                field_nodes.append(f'<i class="chart-point chart-point--{size} chart-point--{tone}" style="left:{x:g}%;top:{y:g}%"></i>')
            comet_nodes=[]
            for comet in stars.get('comets',[]):
                x=float(comet['x']);y=float(comet['y']);angle=float(comet['angle']);travel=float(comet['travel']);duration=float(comet['duration']);delay=float(comet['delay'])
                if not (0<=x<=100 and 0<=y<=100 and -180<=angle<=180 and 0<travel<=250 and 20<=duration<=60 and -60<=delay<=0):raise ValueError('Invalid comet path')
                comet_nodes.append(f'<i class="chart-comet" style="left:{x:g}%;top:{y:g}%;--angle:{angle:g}deg;--travel:{travel:g}px;--duration:{duration:g}s;--delay:{delay:g}s"></i>')
            body='''<h1 class="c-sr-only">Constellation</h1><section class="c-map-hero"><div class="galaxy-container"><div class="chart-grid" aria-hidden="true"></div><div class="chart-topline" aria-hidden="true"><span>TEAM CURIOSITY / 11770</span><span>CONSTELLATION · PLATE 01</span></div><div class="starfield" id="starfield" aria-hidden="true">'''+''.join(field_nodes)+''.join(comet_nodes)+'''</div><div class="chart-compass" aria-hidden="true"><span>N</span><i></i></div><nav class="constellation" id="constellation" aria-label="Explore Constellation">'''+connections+''.join(nodes)+'''</nav><div class="chart-scale" aria-hidden="true"><span>0</span><i></i><span>10°</span></div><div class="chart-coordinates" aria-hidden="true">RA 07h 42m / DEC +18° 06′</div><button id="motion-toggle" type="button" aria-pressed="false">Pause animation</button></div></section><nav class="c-destinations" aria-label="Constellation destinations"><div class="c-destination-grid">'''+list_items+'</div></nav>'
            styles='<link rel="stylesheet" href="/assets/constellation/map.css">'
        else:
            image=p.get('heroImage','')
            art=f'<div class="c-masthead-art" style="--masthead-image:url({escape(image,quote=True)})" aria-hidden="true"></div>' if image else '<div class="c-masthead-art" aria-hidden="true"></div>'
            heading=p.get('heading',p['title'])
            if heading is None:
                masthead=f'<section class="c-masthead c-masthead--untitled"><h1 class="c-sr-only">{escape(p["title"])}</h1>{art}</section>'
            else:
                masthead=f'<section class="c-masthead"><div class="c-masthead-title"><h1>{escape(heading)}</h1></div>{art}</section>'
            body=masthead+(CONTENT/'pages'/(p['slug']+'.html')).read_text(encoding='utf-8')
            styles=''
        if not home:
            body+=(CONTENT/'footer.html').read_text(encoding='utf-8')
        index.append({'title':p['title'],'url':'/constellation/'+p['slug']+'.html','text':text_only(body)})
        lang='es' if p['slug'].startswith('translated-') else 'en'
        output=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#050303"><meta name="description" content="{escape(p['title'])} — Team Curiosity's Constellation"><title>{escape(p['title'])} — Constellation</title><link rel="icon" href="/assets/constellation/star.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="/assets/constellation/site.css">{styles}<script src="/assets/constellation/search-index.js" defer></script><script src="/assets/constellation/site.js" defer></script></head><body class="{'map-page' if home else 'content-page'}">{page_header}<main id="main" tabindex="-1">{body}</main></body></html>'''
        target=ROOT/'constellation'/(p['slug']+'.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(output,encoding='utf-8')
    (ASSETS/'search-index.js').write_text('window.CONSTELLATION_SEARCH = '+json.dumps(index,ensure_ascii=False).replace('<','\\u003c')+';\n',encoding='utf-8')
    print(f'Built {len(all_pages)} Constellation pages.')

if __name__=='__main__':build()
