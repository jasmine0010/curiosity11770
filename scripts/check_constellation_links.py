"""Optional network check of external links; never modifies page content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
import json
ROOT=Path(__file__).resolve().parents[1]
CONTENT=ROOT/'content/constellation'
urls={}
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        url=attrs.get('href') if tag=='a' else attrs.get('src') if tag=='iframe' else None
        if url and url.startswith('https://'):urls.setdefault(url,set()).add(current)
for file in [*(CONTENT/'pages').rglob('*.html'),CONTENT/'footer.html']:
    current=str(file.relative_to(CONTENT)).replace('\\','/')
    Links().feed(file.read_text(encoding='utf-8'))
def check(item):
    url,pages=item
    record={'url':url,'pages':sorted(pages)}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'},method='HEAD'),timeout=15) as response:
            record.update(status=response.status,final_url=response.url)
            if 'accounts.google.com' in response.url:record['note']='Redirected to sign-in; public access could not be verified.'
    except Exception as error:record.update(status=getattr(error,'code',None),note=str(error))
    return record
with ThreadPoolExecutor(max_workers=8) as pool:records=list(pool.map(check,sorted(urls.items())))
(CONTENT/'external-resources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for r in records:
    if r.get('note'):print(r['status'],r['url'],r['note'],flush=True)
print('Checked',len(records),'external URLs;',sum(not r.get('note') for r in records),'responded without errors.')
