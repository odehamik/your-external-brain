"""Build the plain-text edition and participant ZIPs from editions/markdown.
Run with Python 3.10+ using only the standard library. No network calls.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'editions/markdown'
TEXT = ROOT / 'editions/plain-text'
DIST = ROOT / 'downloads'
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def convert(source, content):
    def link(match):
        label, url = match.groups()
        parts = urlsplit(url)
        if parts.scheme:
            return label + ' — ' + url
        target = (source.parent / unquote(parts.path)).resolve()
        assert target.is_relative_to(SOURCE) and target.exists(), (source, url)
        rel = target.relative_to(SOURCE)
        if rel.suffix == '.md':
            rel = rel.with_suffix('.txt')
        return label + ' [folder location: ' + str(rel) + ']'
    content = LINK.sub(link, content)
    content = re.sub(r'(?<=[A-Za-z0-9_-])\.md\b', '.txt', content)
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.M)
    content = content.replace('**', '').replace('`', '')
    lines = content.splitlines()
    result = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s:|-]+\|$', lines[i + 1]):
            headers = [cell.strip() for cell in lines[i].strip('|').split('|')]
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                cells = [cell.strip() for cell in lines[i].strip('|').split('|')]
                result.append(cells[0])
                result.extend(f'{h}: {v}' for h, v in zip(headers[1:], cells[1:]))
                result.append('')
                i += 1
        else:
            result.append(lines[i])
            i += 1
    return '\n'.join(result) + '\n'


def build():
    # Git does not retain empty directories; restore the supplied archive room.
    (SOURCE / "_Muck/Archive").mkdir(parents=True, exist_ok=True)
    TEXT.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(exist_ok=True)
    expected = set()
    for p in sorted(SOURCE.rglob('*')):
        assert not p.is_symlink(), p
        rel = p.relative_to(SOURCE)
        if p.is_dir():
            (TEXT / rel).mkdir(exist_ok=True)
            continue
        target = TEXT / (rel.with_suffix('.txt') if rel.suffix == '.md' else rel)
        expected.add(target)
        # The same self-contained opening is used in both editions.
        content = p.read_text() if p.suffix == '.txt' else convert(p, p.read_text())
        if rel == Path('README.md'):
            content = 'PLAIN TEXT EDITION — GUIDED ENTRY\n\nOpen 00 OPEN ME FIRST.txt, then copy START-HERE.txt into your AI conversation. Folder locations in square brackets may not be clickable.\n\n' + content
        if rel == Path('_Machine/USE-WITH-ANY-MODEL.md'):
            content += '\nPlain Text edition: SKILL.txt contains ordinary instructions. Native discovery may require SKILL.md or another app-specific format. Nothing is installed by reading this folder.\n'
        target.write_text(content)
    actual = {p for p in TEXT.rglob('*') if p.is_file()}
    assert actual == expected, 'Unexpected generated files; inspect rather than silently remove them.'
    checked = 0
    for p in SOURCE.rglob('*.md'):
        for label, url in LINK.findall(p.read_text()):
            parts = urlsplit(url)
            if not parts.scheme:
                target = (p.parent / unquote(parts.path)).resolve()
                assert target.is_relative_to(SOURCE) and target.exists(), (p, url)
                checked += 1
    for p in actual:
        assert p.suffix == '.txt', p
        for rel in re.findall(r'\[folder location: ([^\]]+)\]', p.read_text()):
            assert (TEXT / rel).exists(), (p, rel)
    reports = {}
    for folder, label in [(SOURCE, 'Markdown'), (TEXT, 'Plain Text')]:
        files = [p for p in folder.rglob('*') if p.is_file()]
        for p in files:
            t = p.read_text()
            assert '/Users/' not in t, p
            assert not re.search(r'\b(fuck\w*|shit\w*|bullshit|bitch\w*)\b', t, re.I), p
            assert not re.search(r'PRACTICE-ARRIVAL|PRACTICE-EXPORT|The Missing Table', t), p
        archive = DIST / f'Your External Brain - {label}.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(folder.rglob('*')):
                z.write(p, Path(f'Your External Brain - {label}') / p.relative_to(folder))
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for p in files:
                assert z.read(str(Path(f'Your External Brain - {label}') / p.relative_to(folder))) == p.read_bytes()
        reports[label] = {'files': len(files), 'zip_sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}
    assert (SOURCE / 'START-HERE.txt').read_bytes() == (TEXT / 'START-HERE.txt').read_bytes()
    report = {'markdown_local_links': checked, 'editions': reports, 'behavior_test': 'Not performed; static checks do not establish model behavior or participant accessibility.'}
    (DIST / 'CHECKS.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    build()
