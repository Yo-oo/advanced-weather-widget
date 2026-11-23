"""Tiny PO reader shared by the helper scripts (no external dependencies)."""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TRANSLATE = os.path.join(ROOT, 'translate')


def _unquote(parts):
    return ''.join(json.loads(p) for p in parts)


def parse_po(path):
    """Return a list of entries: {ctx, msgid, msgstr, plural, locs, notes, obsolete}."""
    with open(path, encoding='utf-8') as f:
        blocks = re.split(r'\n\n+', f.read())
    out = []
    for b in blocks:
        lines = b.split('\n')
        obsolete = all(l.startswith('#~') or not l.strip() for l in lines if l.strip())
        if obsolete:
            continue
        fields, cur = {}, None
        locs, notes = [], []
        for l in lines:
            if l.startswith('#: '):
                locs += l[3:].split()
            elif l.startswith('#. '):
                notes.append(l[3:])
            elif l.startswith('#'):
                continue
            else:
                m = re.match(r'(msgctxt|msgid_plural|msgid|msgstr\[0\]|msgstr)\s+(".*")$', l)
                if m:
                    cur = m.group(1)
                    fields.setdefault(cur, []).append(m.group(2))
                elif re.match(r'msgstr\[\d+\]', l):
                    cur = None
                elif l.startswith('"') and cur:
                    fields[cur].append(l)
        if 'msgid' not in fields:
            continue
        msgid = _unquote(fields['msgid'])
        if msgid == '':
            continue  # header
        msgstr = _unquote(fields.get('msgstr', fields.get('msgstr[0]', ['""'])))
        out.append({
            'ctx': _unquote(fields['msgctxt']) if 'msgctxt' in fields else None,
            'msgid': msgid,
            'msgstr': msgstr,
            'plural': 'msgid_plural' in fields,
            'locs': locs,
            'notes': notes,
        })
    return out
