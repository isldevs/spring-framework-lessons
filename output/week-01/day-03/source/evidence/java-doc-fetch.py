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
 ('annotation-context',API+'org/springframework/context/annotation/AnnotationConfigApplicationContext.html',['must be called in order','register','manually refreshed']),
 ('bean-annotation',API+'org/springframework/context/annotation/Bean.html',['produces a bean','factory method','bean name']),
 ('configuration',API+'org/springframework/context/annotation/Configuration.html',['bean definitions','AnnotationConfigApplicationContext','register']),
 ('component',API+'org/springframework/stereotype/Component.html',['candidates for auto-detection','classpath scanning','value']),
 ('component-scan',API+'org/springframework/context/annotation/ComponentScan.html',['basePackages','basePackageClasses','detect','scanned']),
 ('bean-definition',API+'org/springframework/beans/factory/config/BeanDefinition.html',['A BeanDefinition describes','getFactoryBeanName','getFactoryMethodName']),
 ('bean-reference',REF+'core/beans/java/bean-annotation.html',['@Bean','register','method']),
 ('classpath-scanning',REF+'core/beans/classpath-scanning.html',['@Component','@ComponentScan','basePackages'])
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
