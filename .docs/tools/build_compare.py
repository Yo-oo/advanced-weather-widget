#!/usr/bin/env python3
"""Put zh_TW next to every other language for the entries in context.json.

    python3 .docs/tools/build_compare.py [--dir DIR] [--langs de fr ...]

Writes DIR/compare.json: [{i, msgid, ctx, zh_TW, <lang>: msgstr, ...}].
Use it for a cross-language QA pass after zh_TW is filled in (run extract_context.py --all
or keep the context.json from the translation pass). Other languages vary in quality:
treat a single-language outlier sceptically.
"""
import argparse, glob, json, os
from po_util import ROOT, TRANSLATE, parse_po

ap = argparse.ArgumentParser()
ap.add_argument('--dir', default=os.path.join(ROOT, '.docs', 'work'))
ap.add_argument('--langs', nargs='*')
args = ap.parse_args()

ctx = json.load(open(os.path.join(args.dir, 'context.json'), encoding='utf-8'))
langs = args.langs or sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(TRANSLATE, '*.po'))
                             if not p.endswith('zh_TW.po'))
tables = {l: {(e['ctx'], e['msgid']): e['msgstr'] for e in parse_po(os.path.join(TRANSLATE, l + '.po'))}
          for l in ['zh_TW'] + langs}
rows = []
for c in ctx:
    k = (c['msgctxt'], c['msgid'])
    r = {'i': c['i'], 'msgid': c['msgid'], 'ctx': c['msgctxt'], 'zh_TW': tables['zh_TW'].get(k)}
    for l in langs:
        if tables[l].get(k):
            r[l] = tables[l][k]
    rows.append(r)
path = os.path.join(args.dir, 'compare.json')
json.dump(rows, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f'{len(rows)} rows, languages: {", ".join(langs)} -> {path}')
