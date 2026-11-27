from pathlib import Path
import json,re,difflib
R=Path(__file__).resolve().parent;d=json.loads((R.parent/'timing.json').read_text());a=json.loads((R/'asr.json').read_text())
norm=lambda s:re.findall(r'[a-z0-9]+',s.lower().replace("'",'').replace('’',''))
words=[dict(w,token=t) for s in a['segments'] for w in s['words'] for t in norm(w['word'])]
ref=[t for p in d['phrases'] for t in norm(p['text'])];hyp=[w['token'] for w in words];matched={};changes=[]
for tag,i,j,k,l in difflib.SequenceMatcher(None,ref,hyp,autojunk=False).get_opcodes():
 if tag=='equal':
  for x,y in zip(range(i,j),range(k,l)):matched[x]=words[y]
 else:
  changes.append({'tag':tag,'expected':ref[i:j],'observed':hyp[k:l],'observed_span':[words[min(k,len(words)-1)]['start'],words[max(k,l-1)]['end']]})
  if j>i:
   span=words[k:l] or [words[min(k,len(words)-1)]]
   for x in range(i,j):matched[x]={'start':span[0]['start'],'end':span[-1]['end']}
rows=[["What if this Spring bean doesn't exist?"],['A required audit publisher is missing.','Spring cannot finish creating the service.'],['Change the constructor parameter','to Optional of AuditPublisher.','Now absence is allowed.'],['With one matching publisher,','Spring supplies an Optional','containing that managed instance.'],['With no publisher,','Spring supplies an empty Optional.','The service skips this extra notification.'],['Both optional contexts start.','Our tests confirm the values.','Ambiguity can still fail.','Keep critical security dependencies required.'],['Thanks for watching.']]
caps=[];offset=0
for p,rs in zip(d['phrases'],rows):
 assert norm(' '.join(rs))==norm(p['text'])
 for i,text in enumerate(rs):
  n=len(norm(text));start=p['start'] if i==0 else max(p['start'],matched[offset]['start']);offset+=n
  end=p['end'] if i==len(rs)-1 else min(p['end'],matched[offset]['start'])
  assert start<end,(text,start,end)
  caps.append({'scene':p['scene'],'start':start,'end':end,'text':text})
d['captions']=caps;d['alignment_method']='Observed unprompted Whisper spans, with explicit known-input display mappings and sample-derived scene edges; no evenly divided timing.'
(R.parent/'timing.json').write_text(json.dumps(d,indent=2)+'\n');(R/'alignment-mappings.json').write_text(json.dumps(changes,indent=2)+'\n')
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(R.parent.parent/'subtitles.srt').write_text(''.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n\n" for i,c in enumerate(caps,1)))
print('aligned',len(caps),'explicit mappings',changes)
