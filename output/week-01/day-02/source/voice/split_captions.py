"""Align DI captions and progressive graph anchors to independent ASR words."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
['How does a repository reach your service?'],
['Configured scanning finds annotated classes','and registers bean definitions.'],
['A single constructor needs a repository.','Spring resolves that parameter by type.'],
['Spring creates the repository,','then passes its reference','into the service constructor.'],
['Our Java run confirms','the same repository bean.','Only then does the application','use the service.'],
['Scan, register, resolve, inject, then use.','Spring supplies dependencies;','your service doesn’t construct them.'],
['Thanks for watching.'],
]
def normalize(s):
 return re.findall(r'[a-z0-9]+',s.lower().replace('getbean','get bean').replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
expected=normalize(' '.join(c['text'] for c in orig));observed=[w['token'] for w in words]
assert expected==observed,('Inspect raw ASR mismatch before alignment',expected,observed)
(ROOT/'alignment-normalization.json').write_text(json.dumps({'text_transformations':[],'timing_sources':'asr-alignment.json; raw full-stream ASR plus independent unprompted final-phrase crop where needed','raw_wer_unchanged':True,'scan_anchor':'exact scene6 sample edit because ASR first word has zero duration'},indent=2)+'\n')
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
def scene_words(number):
 s=next(s for s in d['scenes'] if s['scene']==number)
 return [w for w in words if s['start']-.03<=w['start']<s['end']-.03]
def anchor(number,token,occurrence=0):
 hits=[w for w in scene_words(number) if w['token']==token]
 assert len(hits)>occurrence,(number,token,occurrence)
 return round(hits[occurrence]['start'],6)
absolute={key:anchor(6,key) for key in ['register','resolve','inject','use']}
absolute['scan']=scene_start  # First word uses exact scene edit; ASR gives it zero duration.
absolute['complete']=round(min(absolute['use']+.65,hold_start-.1),6)
absolute.update({'recap_hold_start':hold_start,'recap_hold_end':d['recap_hold_end']})
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scene_start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['scene_cues_absolute']={
 'discovery':{'scan':anchor(2,'scanning'),'find':anchor(2,'finds'),'register':anchor(2,'registers')},
 'resolution':{'constructor':anchor(3,'constructor'),'repository':anchor(3,'repository'),'resolve':anchor(3,'resolves'),'type':anchor(3,'type')},
 'injection':{'create':anchor(4,'creates'),'pass':anchor(4,'passes'),'reference':anchor(4,'reference'),'constructor':anchor(4,'constructor')},
 'proof':{'confirm':anchor(5,'confirms'),'same':anchor(5,'same'),'application':anchor(5,'application'),'use':anchor(5,'use')},
}
d['caption_method']='Seven complete scene utterances, one inference batch per scene; exact sample-derived scene edits. Short display captions and DI step anchors use unprompted faster-whisper base.en word starts (approximate20ms grid). Raw full-stream ASR/WER retained unchanged. The short late Thanks crop is independently transcribed without a prompt when omitted by the full decoder; its absolute word timing is supplemental-asr.json. Scan starts at the exact scene edit because its ASR word duration is zero. Recap complete cue is a derived animation completion .65s after spoken use, with an additional exact2s reading hold before Thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute,'scene_cues_absolute':d['scene_cues_absolute']},indent=2,ensure_ascii=False))
