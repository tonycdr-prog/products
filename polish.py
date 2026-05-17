from pathlib import Path
import re, html
root=Path('/tmp/products-deploy')
issues=[]

def human(folder):
    s=folder
    s=re.sub(r'^(PP-)+\d+-','',s,flags=re.I)
    s=s.replace('-', ' ')
    acr={'uk':'UK','ai':'AI','api':'API','seo':'SEO','vat':'VAT','hmrc':'HMRC','bsa':'BSA','cgt':'CGT','qr':'QR','cms':'CMS','smb':'SMB','cod':'COD','ocr':'OCR','gbp':'GBP','llm':'LLM','hn':'HN','tdd':'TDD','ifc':'IFC','dns':'DNS'}
    return ' '.join(acr.get(w.lower(), w.capitalize()) for w in s.split())

def brief_desc(d):
    p=d/'docs'/'PRODUCT_BRIEF.md'
    if not p.exists(): return None
    txt=p.read_text(errors='ignore')
    # What it does section content until next heading
    m=re.search(r'(?ims)^##?\s*What it does\s*\n+(.+?)(?=\n##?\s|\Z)', txt)
    if m:
        lines=[]
        for line in m.group(1).splitlines():
            line=line.strip().lstrip('*- ').strip()
            if line: lines.append(line)
        if lines: return re.sub(r'\s+',' ', ' '.join(lines))[:260]
    for line in txt.splitlines():
        line=line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            return re.sub(r'\s+',' ', line.lstrip('*- '))[:260]
    return None

# root index cards
idx=root/'index.html'
s=idx.read_text()
changes=0
# h2 title cleanup
for m in list(re.finditer(r'<a class="card" href="/products/([^/]+)/">(.*?)</a>', s, re.S)):
    folder=m.group(1); block=m.group(2); name=human(folder)
    nb=block
    nb=re.sub(r'<h2>.*?</h2>', f'<h2>{html.escape(name)}</h2>', nb, count=1, flags=re.S)
    pm=re.search(r'<p>(.*?)</p>', nb, re.S)
    desc=html.unescape(pm.group(1)).strip() if pm else ''
    bad=(not desc or desc.lower() in {'coming soon','todo','lorem ipsum'} or desc.startswith('#') or desc==folder or re.fullmatch(r'(PP-)+\d+-[a-z0-9-]+', desc, re.I))
    if bad:
        bd=brief_desc(root/folder) or f'{name} helps teams turn scattered inputs into a clearer, faster workflow with practical checks and ready-to-use outputs.'
        nb=re.sub(r'<p>.*?</p>', f'<p>{html.escape(bd)}</p>', nb, count=1, flags=re.S)
    if nb!=block:
        s=s[:m.start(2)] + nb + s[m.end(2):]
        changes+=1
idx.write_text(s)
if changes: issues.append(('index.html', changes, 'cleaned product card titles/descriptions'))

placeholder_patterns=[r'Coming soon',r'TODO',r'Lorem ipsum',r'\[INSERT[^\]]*\]',r'your@email\.com',r'yourdomain\.com',r'localhost:\d+']
for f in sorted(root.glob('*/index.html')):
    orig=f.read_text(errors='ignore')
    s=orig; name=human(f.parent.name); c=0; notes=[]
    # title
    if not re.search(r'<title>\s*[^<\s][^<]*</title>', s, re.I):
        if re.search(r'<head[^>]*>', s, re.I):
            s=re.sub(r'(<head[^>]*>)', r'\1\n  <title>'+html.escape(name)+'</title>', s, count=1, flags=re.I); c+=1; notes.append('added title')
    else:
        ns=re.sub(r'<title>\s*(?:Untitled|TODO|Coming soon|)\s*</title>', '<title>'+html.escape(name)+'</title>', s, count=1, flags=re.I)
        if ns!=s: s=ns; c+=1; notes.append('fixed title')
    if 'name="viewport"' not in s and "name='viewport'" not in s:
        s=re.sub(r'(<head[^>]*>\s*)', r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1" />', s, count=1, flags=re.I); c+=1; notes.append('added viewport')
    # placeholder visible text replacements
    desc=brief_desc(f.parent) or f'{name} gives users a focused way to check the problem, understand the next step, and export a practical result.'
    repls=[('Coming soon', desc),('TODO', desc),('Lorem ipsum', desc),('your@email.com','hello@example.com'),('yourdomain.com','example.com')]
    for old,new in repls:
        if old in s: s=s.replace(old,new); c+=1; notes.append('replaced placeholder copy')
    s2=re.sub(r'\[INSERT[^\]]*\]', desc, s)
    if s2!=s: s=s2; c+=1; notes.append('replaced insert placeholder')
    s2=re.sub(r'https?://localhost:\d+/?','/',s)
    if s2!=s: s=s2; c+=1; notes.append('removed localhost URL')
    # raw markdown in visible text: simple headings/list markers between tags
    s2=re.sub(r'>(\s*)#\s+([^<]+)<', r'>\1\2<', s)
    s2=re.sub(r'>(\s*)\*\s+([^<]+)<', r'>\1\2<', s2)
    if s2!=s: s=s2; c+=1; notes.append('removed markdown fragments')
    # if no style tag/css and no common framework class, add minimal design tokens
    if '<style' not in s.lower() and not re.search(r'class="[^"]*(bg-|text-|flex|grid|container)', s):
        style='''\n  <style>\n    :root{color-scheme:light;--bg:#f8fafc;--fg:#0f172a;--muted:#64748b;--card:#ffffff;--line:#e4e7eb;--primary:#1e3a5f;--accent:#059669}\n    *{box-sizing:border-box} body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--fg);line-height:1.5} main{width:min(1120px,calc(100% - 32px));margin:0 auto;padding:56px 0} h1,h2,h3{letter-spacing:-.03em;line-height:1.1} a,button{color:var(--primary)} button,.button,[role="button"]{min-height:44px;border-radius:12px;border:0;background:var(--primary);color:#fff;padding:12px 18px;font-weight:700} .card,section{border-color:var(--line)} p{color:var(--muted)}\n  </style>'''
        s=re.sub(r'(</head>)', style+r'\n\1', s, count=1, flags=re.I); c+=1; notes.append('added base design tokens')
    if s!=orig:
        f.write_text(s); issues.append((str(f.relative_to(root)), c, ', '.join(sorted(set(notes)))))

print('ISSUES')
for row in issues: print(row)
print('TOTAL', sum(r[1] for r in issues), 'BUILDS', len([r for r in issues if r[0] != 'index.html']))
