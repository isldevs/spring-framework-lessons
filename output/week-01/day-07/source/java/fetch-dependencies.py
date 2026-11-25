#!/usr/bin/env python3
"""Pinned Spring Framework/JUnit verification classpath; TLS and published checksums on."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,urllib.request,zipfile,json
ROOT=Path(__file__).resolve().parent;LIB=ROOT/'lib';LIB.mkdir(exist_ok=True)
COORDINATES=[*[('org.springframework',a,'6.2.11') for a in ['spring-context','spring-aop','spring-beans','spring-core','spring-expression','spring-jcl','spring-test']],('io.micrometer','micrometer-observation','1.15.4'),('io.micrometer','micrometer-commons','1.15.4'),('org.eclipse.jdt','ecj','3.40.0'),('org.junit.platform','junit-platform-console-standalone','1.12.2')]
def fetch(c):
 g,a,v=c;name=f'{a}-{v}.jar';url=f"https://repo.maven.apache.org/maven2/{g.replace('.', '/')}/{a}/{v}/{name}";p=LIB/name
 data=p.read_bytes() if p.exists() else urllib.request.urlopen(url,timeout=60).read()
 expected=urllib.request.urlopen(url+'.sha1',timeout=30).read().decode().strip().split()[0]
 assert hashlib.sha1(data).hexdigest()==expected,name
 p.write_bytes(data)
 return name,hashlib.sha256(data).hexdigest(),url
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(fetch,COORDINATES))
(ROOT/'dependencies.sha256').write_text(''.join(f'{h}  lib/{n}\n' for n,h,u in sorted(results)))
(ROOT/'dependency-sources.json').write_text(json.dumps([{'artifact':n,'sha256':h,'url':u,'published_sha1_verified':True} for n,h,u in sorted(results)],indent=2)+'\n')
licenses=ROOT/'licenses';licenses.mkdir(exist_ok=True)
for n,h,u in results:
 with zipfile.ZipFile(LIB/n) as z:
  for entry in z.namelist():
   leaf=entry.rsplit('/',1)[-1]
   if entry.startswith('META-INF/') and ('LICENSE' in leaf.upper() or 'NOTICE' in leaf.upper()) and not entry.endswith('/'):
    (licenses/(n[:-4]+'-'+leaf)).write_bytes(z.read(entry))
 print(n,'published checksum verified')
# ECJ additional license evidence.
for name,url in [('ecj-EPL-2.0.html','https://www.eclipse.org/legal/epl-2.0/')]:
 try:(licenses/name).write_bytes(urllib.request.urlopen(url,timeout=30).read())
 except Exception as e:print('Additional license URL:',name,type(e).__name__)
