#!/usr/bin/env python3
"""Refresh the static guide from the verified participant release (no network)."""
from pathlib import Path
import shutil,json,zipfile
root=Path(__file__).resolve().parents[1]
site=root/'site'
(site/'downloads').mkdir(exist_ok=True)
for name in ['Your External Brain - Markdown.zip','Your External Brain - Plain Text.zip','CHECKS.json']:
    shutil.copy2(root/'downloads'/name,site/'downloads'/name)
starter=(root/'editions/markdown/START-HERE.txt').read_text()
(site/'START-HERE.txt').write_text(starter)
(site/'starter.js').write_text('window.STARTER_TEXT = '+json.dumps(starter,ensure_ascii=False)+';\n')
artifacts=root/'.artifacts';artifacts.mkdir(exist_ok=True)
with zipfile.ZipFile(artifacts/'Your External Brain - Netlify Site.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(site.rglob('*')):
        if p.is_file():z.write(p,Path('Your External Brain - Site')/p.relative_to(site))
print('Static downloads and starter refreshed; Netlify ZIP created.')
