"""Prepare generated public files for GitHub Pages without changing local URLs."""
from pathlib import Path
import argparse
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base-path', default='/curiosity11770')
args = parser.parse_args()
base = '/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
if not re.fullmatch(r'(?:/[A-Za-z0-9_.-]+)*', base):
    parser.error('Base path must contain only URL path segments.')
output = ROOT / '_site'
output.mkdir(exist_ok=True)
pages = json.loads((ROOT / 'content/pages.json').read_text(encoding='utf-8'))
files = {ROOT / page['path'] for page in pages}
for directory in ['assets', 'constellation', 'pleiades-page']:
    files.update(p for p in (ROOT / directory).rglob('*') if p.is_file())
for source in sorted(files):
    target = output / source.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() in {'.html', '.css', '.js', '.svg'}:
        text = source.read_text(encoding='utf-8')
        # Root-relative HTML, CSS, and JS URLs; leave external and relative URLs alone.
        text = re.sub(r'''(["'(=])/(?=[A-Za-z0-9])''', lambda m: m[1] + base + '/', text)
        target.write_text(text, encoding='utf-8')
    else:
        shutil.copy2(source, target)
shutil.copy2(output / 'home.html', output / 'index.html')
(output / '.nojekyll').touch()
print(f'Prepared {len(files)} public files in _site for {base or "/"}.')
