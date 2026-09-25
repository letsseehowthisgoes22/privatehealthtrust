"""Validate crawlable local links, SEO identity, schema, and directory coverage."""
from pathlib import Path
from urllib.parse import urlparse,unquote
from collections import Counter
import json,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];errors=[];titles=[];canons=[]
for path in sorted(root.rglob('*.html')):
 s=BeautifulSoup(path.read_text(),'html.parser');name=str(path.relative_to(root))
 for selector,label in [('title','title'),('h1','h1'),('meta[name="description"]','description'),('link[rel="canonical"]','canonical')]:
  if len(s.select(selector))!=1:errors.append(f'{name}: expected one {label}')
 titles.append(s.title.text if s.title else '')
 canonical=s.select_one('link[rel="canonical"]')
 if canonical:canons.append(canonical['href'])
 ids=[x['id'] for x in s.select('[id]')]
 if len(ids)!=len(set(ids)):errors.append(f'{name}: duplicate IDs')
 for script in s.select('script[type="application/ld+json"]'):
  try:json.loads(script.string or script.text)
  except Exception as exc:errors.append(f'{name}: invalid schema {exc}')
 for node in s.select('[href], [src]'):
  raw=node.get('href',node.get('src',''));u=urlparse(raw)
  if u.scheme in ['mailto','tel','data','javascript']:continue
  if u.netloc and u.netloc!='privatehealthtrust.com':continue
  target=(root/unquote(u.path.lstrip('/'))) if u.path.startswith('/') or u.netloc else path.parent/unquote(u.path)
  if not u.path:target=path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{name}: missing local link {raw}')
  elif u.fragment and target.suffix=='.html':
   ts=s if target==path else BeautifulSoup(target.read_text(),'html.parser')
   if not ts.find(id=unquote(u.fragment)):errors.append(f'{name}: missing anchor {raw}')
for label,values in [('title',titles),('canonical',canons)]:
 for value,count in Counter(values).items():
  if count>1:errors.append(f'Duplicate {label}: {value}')
urls=[x.text for x in ET.parse(root/'sitemap.xml').findall('.//{*}loc')]
if set(urls)!=set(canons):errors.append('Sitemap and canonical URLs differ: '+str(set(urls)^set(canons)))
data=json.loads((root/'data/providers.json').read_text())
if len(data['rehabs'])!=15 or len(data['case_managers'])!=9:errors.append('Incorrect directory counts')
for page,key in [('provider-directory.html','rehabs'),('private-case-managers.html','case_managers')]:
 s=BeautifulSoup((root/page).read_text(),'html.parser')
 if len(s.select('[data-card]'))!=len(data[key]):errors.append(page+': missing rendered cards')
 for r in data[key]:
  if not s.find(id=r['id']):errors.append(page+': missing '+r['id'])
for filename in ['llms.txt','provider-directory.md','robots.txt','social-card.png']:
 if not (root/filename).exists():errors.append('Missing '+filename)
print(json.dumps({'html_pages':len(titles),'sitemap_urls':len(urls),'featured_programs':len(data['rehabs']),'case_managers':len(data['case_managers']),'caron_program_entries':len(data['caron']),'errors':errors},indent=2))
raise SystemExit(bool(errors))
