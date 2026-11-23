#!/usr/bin/env python3
"""List untranslated zh_TW entries together with the QML source around each use.

Run `python3 .docs/gen_zh_TW.py` first so zh_TW.po reflects the new template.pot;
entries with an empty msgstr are the ones to translate.

    python3 .docs/tools/extract_context.py [--all] [--out DIR] [--window N]

Writes DIR/context.json (default .docs/work/): a list of
{i, msgid, msgctxt, plural, notes, uses:[{loc, code}]}.
Hand this file to translators: reading the code is what tells "10 m" (wind height,
metres) from minutes, or "Wheel" (gear button) from the mouse wheel.
"""
import argparse, json, os
from po_util import ROOT, TRANSLATE, parse_po

ap = argparse.ArgumentParser()
ap.add_argument('--all', action='store_true', help='include translated entries too')
ap.add_argument('--out', default=os.path.join(ROOT, '.docs', 'work'))
ap.add_argument('--window', type=int, default=7, help='lines of code before/after the use')
args = ap.parse_args()

entries = [e for e in parse_po(os.path.join(TRANSLATE, 'zh_TW.po')) if args.all or not e['msgstr']]
out = []
for i, e in enumerate(entries):
    uses = []
    for loc in e['locs'][:2 if len(e['msgid']) <= 25 else 1]:
        path, _, line = loc.rpartition(':')
        try:
            with open(os.path.join(ROOT, path), encoding='utf-8') as f:
                src = f.read().split('\n')
            n = int(line)
            code = '\n'.join(s.strip()[:200] for s in src[max(0, n - 1 - args.window):n + args.window])
            uses.append({'loc': loc, 'code': code})
        except (OSError, ValueError):
            uses.append({'loc': loc})
    out.append({'i': i, 'msgid': e['msgid'], 'msgctxt': e['ctx'], 'plural': e['plural'],
                'notes': e['notes'], 'uses': uses})

os.makedirs(args.out, exist_ok=True)
path = os.path.join(args.out, 'context.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(f'{len(out)} entries -> {path}')
