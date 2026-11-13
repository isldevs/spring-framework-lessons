"""Align short display captions to the actual independently recognized narration."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text())
orig=d['phrases']
CAPTIONS=[
['Who creates your Java objects?'],
['Without Spring, your code','creates a repository,','then passes it into a service.'],
['With Spring, you register bean definitions.','The container uses them to create','managed objects','and wire their dependencies.'],
['Here, the service bean asks for a repository.','Spring supplies that bean.'],
['Your application calls getBean','to request the ready service.','In our Java run, its repository','is the same bean from the container.'],
['Here’s the whole flow.','Define your beans.','Spring creates them','and wires their dependencies.','Your application requests','the ready service.','That’s inversion of control—','for managed beans,','not every Java object.'],
]
def normalize(s):
 return re.findall(r'[a-z0-9]+',s.lower().replace('getBean','get bean').replace('getbean','get bean').replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
# Preserve raw ASR. A common lexical boundary splits inversion into in/version.
# Merge this one documented homophonic boundary for alignment, not for raw WER.
transforms=[];aligned=[];idx=0
while idx<len(words):
 if idx+1<len(words) and words[idx]['token']=='in' and words[idx+1]['token']=='version':
  first,second=words[idx],words[idx+1]
  aligned.append({**first,'word':'inversion','token':'inversion','end':second['end']})
  transforms.append({'source_tokens':['in','version'],'aligned_token':'inversion','start':first['start'],'end':second['end'],'reason':'ASR lexical word-boundary split; raw transcript and raw WER retained unchanged'})
  idx+=2
 else:aligned.append(words[idx]);idx+=1
words=aligned
(ROOT/'alignment-normalization.json').write_text(json.dumps(transforms,indent=2)+'\n')
expected=normalize(' '.join(c['text'] for c in orig))
observed=[w['token'] for w in words]
assert expected==observed, ('ASR mismatch requires inspection before caption alignment',expected,observed)
new=[];j=0
for c,rows in zip(orig,CAPTIONS):
 assert normalize(c['text'])==normalize(' '.join(rows))
 for i,text in enumerate(rows):
  count=len(normalize(text));start=c['start'] if i==0 else words[j]['start']
  j+=count
  end=c['end'] if i==len(rows)-1 else words[j]['start']
  assert c['start']-.03<=start<end<=c['end']+.03,(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words)
assert max(len(c['text']) for c in new)<=45
for a,b in zip(new,new[1:]):assert a['end']<=b['start']
d['captions']=new
scene_start=d['scenes'][-1]['start']
last=[w for w in words if w['start']>=scene_start-.03]
def anchor(token,occurrence=0):
 matches=[w for w in last if w['token']==token]
 return round(matches[occurrence]['start'],6)
absolute={'define':anchor('define'),'create':anchor('creates'),'wire':anchor('wires'),'request':anchor('your',1),'request_verb':anchor('requests'),'ready':anchor('ready'),'takeaway':anchor('thats'),'qualifier':anchor('for'),'complete_at':anchor('not'),'final_hold_start':d['final_hold_start']}
d['recap_cues']={'relative_to':'scene_start',**{key:round(value-scene_start,6) for key,value in absolute.items()}}
d['recap_cues_absolute']=absolute
d['caption_method']='Six complete scene utterances are each synthesized in one inference batch; exact scene edit bounds. Short display captions split at independently recognized faster-whisper base.en word starts (approximate 20ms grid). Spoken get bean is displayed as getBean. One ASR in/version word-boundary split is merged only for alignment (alignment-normalization.json); raw WER/transcript remain unchanged. Phrases retain the exact spoken script.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(new,indent=2,ensure_ascii=False))
