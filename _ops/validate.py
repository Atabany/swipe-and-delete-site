#!/usr/bin/env python3
"""Check generated pages before deployment; no third-party dependencies required."""
import html,json,re,sys,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,parse_qs,unquote
ROOT=Path(__file__).resolve().parent.parent
CONFIG=json.loads((ROOT/'_ops/config.json').read_text());BASE=CONFIG['base'].rstrip('/')+'/'
errors=[]
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.h1=0;self.title='';self.desc='';self.canon='';self.ids=set();self.links=[];self.images=[];self.ld=[];self.inTitle=False;self.inLd=False;self.buf='';self.text=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if t=='h1':self.h1+=1
  if t=='title':self.inTitle=True
  if t=='meta' and a.get('name')=='description':self.desc=a.get('content','')
  if t=='link' and a.get('rel')=='canonical':self.canon=a.get('href','')
  if t=='a':self.links.append(a.get('href',''))
  if t=='img':self.images.append(a)
  for k in ('src','poster','data-src'):
   if a.get(k):self.links.append(a[k])
  if t=='link' and a.get('rel') in ('stylesheet','icon'):self.links.append(a['href'])
  if t=='script' and a.get('type')=='application/ld+json':self.inLd=True;self.buf=''
 def handle_data(self,d):
  if self.inTitle:self.title+=d
  if self.inLd:self.buf+=d
  elif not self.inTitle:self.text.append(d)
 def handle_endtag(self,t):
  if t=='title':self.inTitle=False
  if t=='script' and self.inLd:self.inLd=False;self.ld.extend(json.loads(self.buf))
pages={}
for f in ROOT.glob('*.html'):
 if re.match(r'google[0-9a-f]+\.html',f.name):continue
 p=Page()
 try:p.feed(f.read_text())
 except Exception as e:errors.append(f'{f.name}: parse/JSON-LD error {e}')
 pages[f.name]=p
sitemap={x.text for x in ET.parse(ROOT/'sitemap.xml').getroot().findall('{*}url/{*}loc')};llms=(ROOT/'llms.txt').read_text();full=(ROOT/'llms-full.txt').read_text()
titles=set();descriptions=set();tags={}
for name,p in pages.items():
 expected=BASE+('' if name=='index.html' else name)
 if p.h1!=1:errors.append(f'{name}: expected one H1')
 if len(p.title)>60 or not p.title:errors.append(f'{name}: title length {len(p.title)}')
 if len(p.desc)>155 or not p.desc:errors.append(f'{name}: description length {len(p.desc)}')
 if p.title in titles:errors.append(f'{name}: duplicate title')
 if p.desc in descriptions:errors.append(f'{name}: duplicate description')
 titles.add(p.title);descriptions.add(p.desc)
 if p.canon!=expected:errors.append(f'{name}: canonical mismatch')
 if name!='404.html' and (expected not in sitemap or expected not in llms or expected not in full):errors.append(f'{name}: missing sitemap or LLM coverage')
 text=' '.join(p.text)
 for banned in [r'\$\d',r'\b#1\b',r'guaranteed (?:storage|ranking)',r'\bSwiftSweep\b',r'getphotocleaner\.com',r'6746700862',r'no data (?:is )?collected']:
  if re.search(banned,text,re.I):errors.append(f'{name}: unsupported or sibling claim {banned}')
 for img in p.images:
  if any(k not in img for k in ['alt','width','height']):errors.append(f'{name}: image missing alt/dimensions')
 for link in p.links:
  u=urlsplit(link)
  if u.scheme:
   if u.netloc=='apps.apple.com' and '6754815949' in u.path:
    q=parse_qs(u.query)
    if '6754815949' not in u.path or q.get('pt')!=[CONFIG['providerToken']] or q.get('mt')!=['8'] or not q.get('ct'):errors.append(f'{name}: invalid campaign link')
    else:tags.setdefault(q['ct'][0],set()).add(name)
   continue
  if not u.path:
   if u.fragment and u.fragment not in p.ids:errors.append(f'{name}: missing anchor {link}')
   continue
  target=ROOT/unquote(u.path)
  if target.is_dir():target/= 'index.html'
  if not target.exists():errors.append(f'{name}: missing target {link}')
  elif u.fragment and target.name in pages and u.fragment not in pages[target.name].ids:errors.append(f'{name}: target anchor missing {link}')
 for ld in p.ld:
  if ld.get('@type')=='FAQPage':
   for q in ld['mainEntity']:
    if q['name'] not in text or q['acceptedAnswer']['text'] not in text:errors.append(f'{name}: FAQ markup differs from visible text')
  if ld.get('@type')=='MobileApplication':
   f=json.loads((ROOT/'_ops/facts.json').read_text());r=ld['aggregateRating']
   if r['ratingValue']!=f['averageUserRating'] or r['ratingCount']!=f['userRatingCount']:errors.append(f'{name}: rating mismatch')
for tag,names in tags.items():
 if len(names)>1:errors.append(f'Campaign tag reused across pages: {tag}: {names}')
for path in sitemap:
 if path not in {BASE+('' if n=='index.html' else n) for n in pages if n!='404.html'}:errors.append(f'Unknown sitemap URL {path}')
for bot in ['OAI-SearchBot','Claude-SearchBot','PerplexityBot','Bingbot']:
 if 'User-agent: '+bot not in (ROOT/'robots.txt').read_text():errors.append('Missing crawler '+bot)
key=CONFIG['indexNowKey']
if (ROOT/(key+'.txt')).read_text()!=key:errors.append('IndexNow key mismatch')
for g in json.loads((ROOT/'_ops/guides.json').read_text()) if (ROOT/'_ops/guides.json').exists() else []:
 words=len(re.findall(r'\b\w+\b',re.sub('<[^>]+>',' ',g['intro']+' '.join(s['html'] for s in g['sections'])+' '.join(f['answer'] for f in g['faqs']))))
 if not 800<=words<=1300:errors.append(f'{g["slug"]}: guide length {words}, expected 800–1300')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'OK — {len(pages)} pages, links, campaigns, structured data, sitemap and guide lengths checked')
