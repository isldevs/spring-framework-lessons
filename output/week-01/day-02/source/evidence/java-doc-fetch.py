#!/usr/bin/env python3
"""Retrieve exact official documentation evidence; never synthesize excerpts."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import hashlib, json, re, urllib.request
OUT=Path(__file__).resolve().parent
API='https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/'
REF='https://docs.spring.io/spring-framework/reference/6.2/'
PAGES=[
 ('annotation-context',API+'org/springframework/context/annotation/AnnotationConfigApplicationContext.html',['register','refresh()','Create a new AnnotationConfigApplicationContext']),
 ('factory-postprocessor',API+'org/springframework/beans/factory/config/BeanFactoryPostProcessor.html',['not bean instances','before','modify']),
 ('abstract-context',API+'org/springframework/context/support/AbstractApplicationContext.html',['destroying all beans','Close this application context']),
 ('bean-definition',API+'org/springframework/beans/factory/config/BeanDefinition.html',['A BeanDefinition describes','scope','lazy']),
 ('bean-definition-reference',REF+'core/beans/definition.html',['BeanDefinition','metadata','singleton']),
 ('application-context',API+'org/springframework/context/ApplicationContext.html',['application events','resources','BeanFactory','internationalization']),
 ('configurable-context',API+'org/springframework/context/ConfigurableApplicationContext.html',['Close this application context','destroying all beans','refresh']),
 ('event-publisher',API+'org/springframework/context/ApplicationEventPublisher.html',['event multicaster','synchronous','hand-off']),
 ('disposable-bean',API+'org/springframework/beans/factory/DisposableBean.html',['release resources','destroy()','destruction']),
 ('lazy-singletons',REF+'core/beans/dependencies/factory-lazy-init.html',['eagerly','lazy-initialized','singleton'])
]
class Extract(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style'] and self.skip:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def fetch(entry):
 name,url,needles=entry
 with urllib.request.urlopen(url,timeout=45) as resp:
  data=resp.read();status=resp.status;resolved=resp.geturl()
 assert status==200,(name,status)
 (OUT/f'java-doc-{name}.html').write_bytes(data)
 p=Extract();p.feed(data.decode('utf-8'));text=re.sub(r'\s+',' ',' '.join(p.parts)).strip()
 (OUT/f'java-doc-{name}.txt').write_text(text+'\n')
 excerpts=[]
 for needle in needles:
  matches=list(re.finditer(re.escape(needle),text,re.I))
  for match in matches[:3]:
   start=max(0,match.start()-150);end=min(len(text),match.end()+500)
   excerpts.append({'needle':needle,'verbatim_context':text[start:end]})
 return {'name':name,'url':url,'resolved_url':resolved,'http_status':status,'html_sha256':hashlib.sha256(data).hexdigest(),'excerpts':excerpts}
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,PAGES))
(OUT/'java-doc-official-documentation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['name','url','http_status','html_sha256']} for r in results],indent=2))
