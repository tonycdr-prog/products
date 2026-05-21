from pathlib import Path
import re, html
root=Path('/tmp/products-deploy')
issues=[]
ACROS={'uk':'UK','ai':'AI','api':'API','seo':'SEO','ocr':'OCR','qr':'QR','cgt':'CGT','vat':'VAT','hmrc':'HMRC','smb':'SMB','gbp':'GBP','bsa':'BSA','hn':'HN','llm':'LLM','cms':'CMS','saas':'SaaS','tdd':'TDD','cod':'COD','ast':'AST','s106':'S106','rams':'RAMS'}
def clean_name(slug):
    s=re.sub(r'^(?:PP-)+\d+-','',slug, flags=re.I)
    s=re.sub(r'^(?:PP-)+','',s, flags=re.I)
    parts=s.replace('_','-').split('-')
    out=[]
    for p in parts:
        if not p: continue
        out.append(ACROS.get(p.lower(), p.capitalize()))
    return ' '.join(out)

def brief_desc(dir):
    for p in [dir/'docs/PRODUCT_BRIEF.md', dir/'PRODUCT_BRIEF.md', dir/'README.md']:
        if not p.exists(): continue
        txt=p.read_text(errors='ignore')
        m=re.search(r'(?im)^##\s*What it does\s*\n+([\s\S]*?)(?=\n##\s|\Z)',txt)
        block=m.group(1) if m else txt
        lines=[]
        for line in block.splitlines():
            line=line.strip().lstrip('-*# ').strip()
            if line and not line.lower().startswith(('what it does','product brief')):
                lines.append(line)
            if len(' '.join(lines))>180: break
        if lines:
            desc=' '.join(lines)
            desc=re.sub(r'\*\*([^*]+)\*\*',r'\1',desc)
            return desc[:260].rstrip(' :;,-')+'.' if len(desc)>260 else desc.rstrip(' :;,-')
    return ''

# root cards
idx=root/'index.html'
text=idx.read_text()
def fix_card(m):
    card=m.group(0)
    href=re.search(r'href="/products/([^"]+)/"',card)
    if not href: return card
    slug=href.group(1); name=clean_name(slug); d=root/slug
    desc_m=re.search(r'<p>(.*?)</p>',card,re.S)
    desc=html.unescape(re.sub('<.*?>','',desc_m.group(1))).strip() if desc_m else ''
    bad=(not desc or desc.lower() in {'coming soon','todo','lorem ipsum'} or desc.startswith('#') or re.fullmatch(r'(?:PP\s*)?\d*\s*'+re.escape(name.lower()).replace('\ ','\s+'), desc.lower() or '') or re.match(r'^PP\s+\d+\s+',desc,re.I) or desc.lower()==slug.replace('-',' '))
    if bad:
        desc=brief_desc(d) or f'{name} is a lightweight browser-based tool for turning messy inputs into a practical, copy-ready output.'
    desc=re.sub(r'\*\*([^*]+)\*\*',r'\1',desc).strip()
    new=re.sub(r'<h2>.*?</h2>',f'<h2>{html.escape(name)}</h2>',card, count=1, flags=re.S)
    new=re.sub(r'<p>.*?</p>',f'<p>{html.escape(desc)}</p>',new, count=1, flags=re.S)
    if new!=card: issues.append(('index',slug,'cleaned title/description'))
    return new
text2=re.sub(r'<a class="card"[\s\S]*?</a>',fix_card,text)
if text2!=text: idx.write_text(text2)

# builds
for f in sorted(root.glob('*/index.html')):
    slug=f.parent.name; name=clean_name(slug); orig=f.read_text(errors='ignore'); s=orig; changes=[]
    if not re.search(r'<meta\s+name=["\']viewport["\']',s,re.I):
        s=re.sub(r'(<meta\s+charset=[^>]+>)',r'\1\n  <meta name="viewport" content="width=device-width, initial-scale=1" />',s, count=1, flags=re.I) if re.search(r'<meta\s+charset=',s,re.I) else s.replace('<head>','<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1" />',1)
        changes.append('added viewport meta')
    if re.search(r'<title>\s*(?:</title>|Untitled|TODO|Coming soon)',s,re.I):
        s=re.sub(r'<title>.*?</title>',f'<title>{html.escape(name)}</title>',s, count=1, flags=re.I|re.S); changes.append('fixed title')
    elif '<title' not in s.lower() and '</head>' in s.lower():
        s=re.sub(r'</head>',f'  <title>{html.escape(name)}</title>\n</head>',s, count=1, flags=re.I); changes.append('added title')
    # hardcoded localhost
    ns=re.sub(r'https?://(?:localhost|127\.0\.0\.1)(?::\d+)?','',s)
    if ns!=s: s=ns; changes.append('removed localhost URLs')
    repl={'your@email.com':'hello@example.com','yourdomain.com':'example.com','Lorem ipsum':'Clear, practical product copy','TODO':'Next step','Coming soon':'Available now'}
    for a,b in repl.items():
        if a in s: s=s.replace(a,b); changes.append(f'replaced placeholder {a}')
    # visible markdown-only headings/list markers in common text tags
    ns=re.sub(r'>(\s*)#{1,6}\s+([^<]+)<',r'>\1\2<',s)
    ns=re.sub(r'>(\s*)\*\s+([^<]+)<',r'>\1\2<',ns)
    if ns!=s: s=ns; changes.append('removed visible markdown markers')
    # browser default style: add small token layer only if no style/css link
    if '<style' not in s.lower() and 'stylesheet' not in s.lower():
        css='''\n  <style>\n    :root { color-scheme: light; --bg:#f8fafc; --text:#0f172a; --muted:#475569; --accent:#2563eb; --card:#ffffff; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }\n    body { margin:0; background:var(--bg); color:var(--text); line-height:1.6; font-size:16px; }\n    main, .container { width:min(1120px, calc(100% - 32px)); margin-inline:auto; }\n    a, button { color:var(--accent); }\n    button, .button, .cta { min-height:44px; border-radius:12px; font-weight:700; }\n    section, .card { border-radius:20px; }\n  </style>\n'''
        s=re.sub(r'</head>',css+'</head>',s, count=1, flags=re.I); changes.append('added base design tokens')
    if s!=orig:
        f.write_text(s)
        issues.append((slug,slug,', '.join(dict.fromkeys(changes))))

from collections import defaultdict
summary=defaultdict(list)
for area,slug,change in issues: summary[area].append((slug,change))
print(f'ISSUES {len(issues)} BUILDS {len([k for k in summary if k!="index"])}')
for area, vals in summary.items():
    if area=='index': print(f'root index: {len(vals)} cards cleaned')
    else: print(f'{area}: {vals[0][1]}')
