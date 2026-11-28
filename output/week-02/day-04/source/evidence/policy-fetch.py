#!/usr/bin/env python3
"""Capture official policy metadata/hashes and short excerpts; no full copyrighted article copies."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone
import urllib.request,urllib.error,hashlib,json,re,concurrent.futures
OUT=Path(__file__).resolve().parent
SOURCES=[
 ('youtube-disclosure','https://support.google.com/youtube/answer/14328491?hl=en',['meaningfully altered','realistic','own voice']),
 ('youtube-monetization','https://support.google.com/youtube/answer/1311392?hl=en',['inauthentic','mass-produced','reused content']),
 ('youtube-shorts-thumbnail','https://support.google.com/youtube/answer/10343433?hl=en',['thumbnail','frame']),
 ('meta-ai-label','https://about.fb.com/news/2026/02/meta-prepares-for-2026-us-midterms/',['realistic-sounding','disclose','AI info']),
 ('meta-originality','https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/',['produced directly','unoriginal','monetization']),
 ('meta-reels-cover','https://business-auth.facebook.com/business/learn/lessons/what-are-fb-ig-reels',['cover image','Facebook','interface'])]
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[];self.in_title=False;self.title=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t=='title':self.in_title=True
  if t in ('p','div','section','h1','h2','h3','li','br'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript') and self.skip:self.skip-=1
  if t=='title':self.in_title=False
 def handle_data(self,s):
  if not self.skip:
   self.parts.append(s)
   if self.in_title:self.title.append(s)
def fetch(s):
 slug,url,needles=s;rec={'slug':slug,'requested_url':url,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 policy reference review'})
  with urllib.request.urlopen(req,timeout=35) as r:
   raw=r.read();rec.update({'http_status':r.status,'final_url':r.url,'content_type':r.headers.get('Content-Type'),'response_sha256':hashlib.sha256(raw).hexdigest(),'response_bytes':len(raw)})
  p=Text();p.feed(raw.decode('utf-8',errors='replace'));text=' '.join(' '.join(p.parts).split());rec['title']=' '.join(p.title).strip()
  found=[]
  for n in needles:
   m=re.search(re.escape(n),text,re.I)
   if m:found.append({'needle':n,'index':m.start()})
  rec['terms_found']=found
  # One short exact excerpt per page, maximum25words total.
  if found:
   i=max(0,found[0]['index']);start=text.rfind('. ',0,i)+2
   if start<0 or i-start>160:start=max(0,text.rfind(' ',0,max(0,i-40)))
   excerpt=' '.join(text[start:].split()[:25]);rec['exact_excerpt']=excerpt;rec['excerpt_word_count']=len(excerpt.split())
  else:rec['exact_excerpt']='';rec['review_limit']='Expected terms not found; do not infer page supports requested claim.'
 except Exception as e:
  rec['http_status']=getattr(e,'code',None);rec['error']=str(e)
 return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(fetch,SOURCES))
(OUT/'policy-official-snapshots.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
for r in records:
 (OUT/f"policy-{r['slug']}.txt").write_text(r.get('title','')+'\n'+r['requested_url']+'\nHTTP '+str(r.get('http_status'))+'\nResponseSHA256 '+str(r.get('response_sha256'))+'\n\nExact excerpt (<=25words):\n'+r.get('exact_excerpt','')+'\n'+r.get('review_limit','')+r.get('error','')+'\n')
print(json.dumps(records,indent=2,ensure_ascii=False))
