#!/usr/bin/env python3
"""Write translations into .docs/gen_zh_TW.py.

    python3 .docs/tools/apply_translations.py TRANSLATIONS.json [--dir DIR] [--label 1.9.1] [--dry-run]

TRANSLATIONS.json is a list aligned with DIR/context.json (same length and order).
Plural entries go to PLURAL (msgstr[0] only). An entry with a msgctxt goes to
CTX_TRANSLATIONS when its msgid already has a different translation in TRANSLATIONS,
otherwise to TRANSLATIONS. Keys already present with the same value are skipped;
conflicting duplicates are reported, never overwritten.
"""
import argparse, json, os, re
from po_util import ROOT

ap = argparse.ArgumentParser()
ap.add_argument('translations')
ap.add_argument('--dir', default=os.path.join(ROOT, '.docs', 'work'))
ap.add_argument('--label', default='new')
ap.add_argument('--dry-run', action='store_true')
args = ap.parse_args()

ctx = json.load(open(os.path.join(args.dir, 'context.json'), encoding='utf-8'))
tr = json.load(open(args.translations, encoding='utf-8'))
assert len(ctx) == len(tr), f'{len(ctx)} entries in context.json but {len(tr)} translations'

gen = os.path.join(ROOT, '.docs', 'gen_zh_TW.py')
src = open(gen, encoding='utf-8').read()
# Load the dicts by running the generator up to (not including) its main loop.
ns = {'__file__': gen}
exec(src.split('raw_entries = re.split')[0], ns)
existing, ctx_existing, plural_existing, multiline = ns['TRANSLATIONS'], ns['CTX_TRANSLATIONS'], ns['PLURAL'], ns['MULTILINE']

j = lambda k, v: f'    {json.dumps(k, ensure_ascii=False)}:\n        {json.dumps(v, ensure_ascii=False)},\n'
single, ctxs, plurals = [], [], []
for c, t in zip(ctx, tr):
    raw = c['msgid'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')  # key as it appears in template.pot
    if not t:
        print('SKIP (empty):', c['msgid'][:60]); continue
    if any(raw.startswith(k) for k in multiline):
        continue  # handled by MULTILINE (prefix match)
    if c['plural']:
        if raw not in plural_existing:
            plurals.append((raw, t))
        continue
    if c['msgctxt'] and (c['msgctxt'], raw) in ctx_existing:
        continue
    if c['msgctxt'] and raw in existing and existing[raw] != t:
        ctxs.append((c['msgctxt'], raw, t)); continue
    if raw in existing:
        if existing[raw] != t:
            print('CONFLICT (kept existing):', raw[:60], '|', existing[raw], '|', t)
        continue
    single.append((raw, t)); existing[raw] = t

if single:
    block = f'    # --- {args.label} additions ---\n' + ''.join(j(k, v) for k, v in single)
    a = src.index('TRANSLATIONS = {')
    b = src.index('\n}\n', a)
    src = src[:b + 1] + block.rstrip('\n') + src[b:]
if ctxs:
    line = ''.join(f'    ({json.dumps(c, ensure_ascii=False)}, {json.dumps(m, ensure_ascii=False)}): {json.dumps(t, ensure_ascii=False)},\n'
                   for c, m, t in ctxs)
    a = src.index('CTX_TRANSLATIONS = {')
    b = src.index('\n}\n', a)
    src = src[:b + 1] + line.rstrip('\n') + src[b:]
if plurals:
    line = ''.join(f'    {json.dumps(m, ensure_ascii=False)}: {json.dumps(t, ensure_ascii=False)},\n' for m, t in plurals)
    a = src.index('PLURAL = {')
    b = src.index('\n}\n', a)
    src = src[:b + 1] + line.rstrip('\n') + src[b:]

print(f'{len(single)} single, {len(ctxs)} with msgctxt, {len(plurals)} plural')
if not args.dry_run:
    open(gen, 'w', encoding='utf-8').write(src)
