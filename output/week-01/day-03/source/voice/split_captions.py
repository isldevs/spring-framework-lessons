"""Align constructor-injection captions and animation anchors to independent ASR.
The full-stream raw transcript and WER are never silently rewritten.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
['How does an order service','get its payment gateway?'],
['Require a payment gateway','in the constructor,','and keep its reference in a final field.'],
['Boot scans the components.','One gateway bean matches','that interface type.'],
['Spring passes it into','the service constructor','before the application places an order.'],
['Our Boot test confirms the same bean.','A fake gateway passes','a separate service test.'],
['Require, resolve, inject, then use.','Constructor injection makes','required dependencies explicit.'],
['Thanks for watching.'],
]
def normalize(s):
 return re.findall(r'[a-z0-9]+',s.lower().replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
expected=normalize(' '.join(c['text'] for c in orig));observed=[w['token'] for w in words]
assert expected==observed,('Inspect raw ASR mismatch before alignment',expected,observed)
new=[];j=0;by_scene={}
for c,rows in zip(orig,CAPTIONS):
 tokens=normalize(c['text']);by_scene[c['scene']]=words[j:j+len(tokens)]
 assert tokens==normalize(' '.join(rows))
 for i,text in enumerate(rows):
  count=len(normalize(text));start=c['start'] if i==0 else words[j]['start'];j+=count
  end=c['end'] if i==len(rows)-1 else words[j]['start']
  assert c['start']-.04<=start<end<=c['end']+.04,(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words) and len(orig)==len(CAPTIONS)==7
assert max(len(c['text']) for c in new)<=45
for a,b in zip(new,new[1:]):assert a['end']<=b['start']
d['captions']=new
scene_map={s['scene']:s for s in d['scenes']}
def anchor(number,token,occurrence=0):
 hits=[w for w in by_scene[number] if w['token']==token]
 assert len(hits)>occurrence,(number,token,occurrence)
 return round(max(scene_map[number]['start'],hits[occurrence]['start']),6)
scene_start=scene_map[6]['start'];hold_start=d['recap_hold_start']
absolute={key:anchor(6,key) for key in ['require','resolve','inject','use']}
absolute['require']=scene_start
absolute['complete']=round(min(absolute['use']+.65,hold_start-.1),6)
absolute.update({'recap_hold_start':hold_start,'recap_hold_end':d['recap_hold_end']})
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scene_start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
injection={'pass':anchor(4,'passes'),'constructor':anchor(4,'constructor'),'application':anchor(4,'application'),'place':anchor(4,'places'),'order':anchor(4,'order')}
injection['ready']=round(min(injection['constructor']+.35,injection['place']-.15),6)
assert injection['constructor']<=injection['ready']<injection['place']
d['scene_cues_absolute']={
 'requirement':{'require':scene_map[2]['start'],'constructor':anchor(2,'constructor'),'reference':anchor(2,'reference'),'final':anchor(2,'final'),'field':anchor(2,'field')},
 'discovery':{'boot':scene_map[3]['start'],'scan':anchor(3,'scans'),'match':anchor(3,'matches'),'interface':anchor(3,'interface'),'type':anchor(3,'type')},
 'injection':injection,
 'proof':{'boot':anchor(5,'boot'),'confirm':anchor(5,'confirms'),'same':anchor(5,'same'),'bean':anchor(5,'bean'),'fake':anchor(5,'fake'),'boot_test':anchor(5,'test',0),'test':anchor(5,'test',1)},
}
(ROOT/'alignment-normalization.json').write_text(json.dumps({'text_transformations':[],'timing_sources':'asr-alignment.json; raw full-stream ASR plus independent unprompted final-phrase crop only when needed','raw_wer_unchanged':True,'first_word_anchors':'require starts at exact scene6 sample edit; scene-start clamps only for ASR rounding','derived_animation_anchors':{'injection_ready':'constructor word start + .35s, capped .15s before place word start','recap_complete':'.65s after use word start, before the exact recap hold'}},indent=2)+'\n')
d['caption_method']='Seven coherent utterances, one inference batch per scene; exact sample-derived scene edits. Captions and constructor-injection cues use independent unprompted faster-whisper base.en word starts (approximate20ms grid). Raw transcript/WER remain unchanged. Supplemental independent outro transcription is used only if required and preserved separately. Captions retain ordinary spaced payment gateway/order service wording. Animation-ready and complete anchors are documented derived timings; recap has an exact2s reading hold before spoken Thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute,'scene_cues_absolute':d['scene_cues_absolute']},indent=2,ensure_ascii=False))
