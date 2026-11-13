"""Align display captions and Config overview cues to independent ASR word timing."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
['Who creates your Java objects?'],
['Without Spring, your code','creates a repository,','then passes it into a service.'],
['With Spring, you register bean definitions.','The container uses them to create','managed objects','and wire their dependencies.'],
['Here, the service bean asks for a repository.','Spring supplies that bean.'],
['Your application calls getBean','to request the ready service.','In our Java run, its repository','is the same bean from the container.'],
['Your app starts Spring with Config.','Spring calls Config’s bean methods,','creates Repo,','and wires Service.','Your app retrieves the ready service.','Managed beans only.'],
['Thanks for watching.'],
]
def normalize(s):
 return re.findall(r'[a-z0-9]+',s.lower().replace('getbean','get bean').replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
# Raw ASR remains untouched. Alignment exceptions are retained separately.
transforms=[]
expected=normalize(' '.join(c['text'] for c in orig));observed=[w['token'] for w in words]
assert expected==observed, ('ASR mismatch requires inspection before caption alignment',expected,observed)
(ROOT/'alignment-normalization.json').write_text(json.dumps(transforms,indent=2)+'\n')
new=[];j=0
for c,rows in zip(orig,CAPTIONS):
 assert normalize(c['text'])==normalize(' '.join(rows))
 for i,text in enumerate(rows):
  count=len(normalize(text));start=c['start'] if i==0 else words[j]['start'];j+=count
  end=c['end'] if i==len(rows)-1 else words[j]['start']
  assert c['start']-.03<=start<end<=c['end']+.03,(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words) and len(orig)==len(CAPTIONS)==7
assert max(len(c['text']) for c in new)<=45
for a,b in zip(new,new[1:]):assert a['end']<=b['start']
d['captions']=new
s6=next(s for s in d['scenes'] if s['scene']==6);scene_start=s6['start'];hold_start=d['recap_hold_start']
last=[w for w in words if scene_start-.03<=w['start']<hold_start]
def anchor(token,occurrence=0):
 matches=[w for w in last if w['token']==token]
 assert len(matches)>occurrence,(token,occurrence,last)
 return round(matches[occurrence]['start'],6)
absolute={'startup':scene_start,'config_load':anchor('config'),'methods':anchor('calls'),'define':anchor('config'),'create':anchor('creates'),'wire':anchor('wires'),'retrieve':anchor('retrieves'),'request':anchor('retrieves'),'request_verb':anchor('retrieves'),'ready':anchor('ready'),'qualifier':anchor('managed'),'recap_hold_start':hold_start,'recap_hold_end':d['recap_hold_end']}
absolute['return_complete']=round(min(absolute['ready']+.5,hold_start-.1),6)
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scene_start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['caption_method']='Seven complete scene utterances synthesized in one inference batch each; exact scene edit boundaries. Display captions and Config overview cues use independent unprompted faster-whisper base.en word starts (approximate20ms grid). Spoken get bean is displayed as getBean. Raw ASR transcript/WER are retained; alignment exceptions, if any, are documented in alignment-normalization.json. Scene6 has the two-second diagram reading hold before scene7 thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute},indent=2,ensure_ascii=False))
