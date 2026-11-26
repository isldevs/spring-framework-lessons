"""Observed phrase captions and illustrative edit cues for constructor injection."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());phrases=d['phrases']
CAPTIONS=[
 ['No Autowired? This still works.'],
 ['This Spring-managed service','has one constructor.','Spring selects it automatically.','Autowired is optional here.'],
 ['Spring reads its parameter type:','PaymentGateway. In our context,','one matching bean is available.'],
 ['Spring supplies that instance','through the constructor.','The service keeps the reference.'],
 ['Now an order calls','the injected gateway.','Our test checks the same instance','and the returned result.'],
 ['Creating an object with new','still means supplying arguments yourself.','Let Spring wire','the beans it manages.'],
 ['Thanks for watching.']]
def normalize(s):return re.findall(r'[a-z0-9]+',s.lower().replace('’','').replace("'",''))
a=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for seg in a['segments']:
 for w in seg['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
transforms=a.get('script_alignment_transformations',[])
for correction in sorted(transforms,key=lambda x:x['raw_token_start'],reverse=True):
 start,end=correction['raw_token_start'],correction['raw_token_end']
 assert [w['token'] for w in words[start:end]]==correction['observed_tokens']
 first=words[start]
 words[start:end]=[{**first,'token':token,'start':correction['start'],'end':correction['end'],'caption_alignment_only':True} for token in correction['script_tokens']]
assert normalize(' '.join(c['text'] for c in phrases))==[w['token'] for w in words]
new=[];offset=0;by_scene={}
for c,rows in zip(phrases,CAPTIONS):
 tokens=normalize(c['text']);assert tokens==normalize(' '.join(rows))
 by_scene[c['scene']]=words[offset:offset+len(tokens)]
 for i,text in enumerate(rows):
  n=len(normalize(text));start=c['start'] if i==0 else words[offset]['start'];offset+=n
  end=c['end'] if i==len(rows)-1 else words[offset]['start']
  start=max(c['start'],start);end=min(c['end'],end)
  assert c['start']<=start<end<=c['end'],(text,start,end)
  assert 3<=len(text.split())<=7,(text,len(text.split()))
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert offset==len(words)
for x,y in zip(new,new[1:]):assert x['end']<=y['start']
# The first complete hook is one cue and is part of the opening cover composition.
assert new[0]['text']==phrases[0]['text'] and new[0]['start']==0 and new[0]['end']==phrases[0]['end']
d['captions']=new
scenes={s['scene']:s for s in d['scenes']}
def anchor(number,token,occurrence=0):
 h=[w for w in by_scene[number] if w['token']==token];assert len(h)>occurrence,(number,token)
 return round(max(scenes[number]['start'],h[occurrence]['start']),6)
def word_end(number,token,occurrence=0):
 h=[w for w in by_scene[number] if w['token']==token];assert len(h)>occurrence,(number,token)
 return round(min(scenes[number]['end'],h[occurrence]['end']),6)
managed={'one':anchor(2,'one'),'select':anchor(2,'selects'),'optional':anchor(2,'optional')}
resolve={'parameter':anchor(3,'paymentgateway'),'search':anchor(3,'context'),'match':anchor(3,'matching')}
inject={'supply':anchor(4,'supplies'),'store':anchor(4,'keeps'),'ready':round(min(word_end(4,'reference')+.08,phrases[3]['end']-.03),6)}
execute={'call':anchor(5,'calls'),'result':round(min(word_end(5,'gateway')+.20,phrases[4]['end']-.15),6),'instance':anchor(5,'same'),'verify':round(min(word_end(5,'result')+.03,phrases[4]['end']-.05),6)}
recap={'manual':anchor(6,'new'),'load':anchor(6,'spring'),'resolve':anchor(6,'wire'),'supply':anchor(6,'beans'),'execute':anchor(6,'manages'),'complete':round(min(word_end(6,'manages')+.05,d['recap_hold_start']-.05),6)}
d['scene_cues_absolute']={'managed':managed,'resolve':resolve,'inject':inject,'execute':execute,'recap':recap}
absolute={**recap,'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['recap_cues_absolute']=absolute
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scenes[6]['start'],6) for k,v in absolute.items()}}
d['opening_cover_hold']=True
d['opening_cover_recognizable_through_s']=1.0
d['opening_transition_start_s']=1.0;d['opening_transition_end_s']=2.0
d['hook_text_display']=phrases[0]['text'];d['hook_asr_last_word_end']=word_end(1,'works')
d['caption_method']='Final sample-derived utterance/first/last-cue boundaries; intermediate unprompted small.en observed word spans. Three documented compound spelling merges preserve raw transcript/score/times. First hook is one exact0-to-utterance-end cue for the cover. No evenly divided caption timing.'
record={'text_transformations':transforms,'raw_asr_score_unchanged':True,'timing_sources':'Unmodified unprompted full-stream ASR with sample-derived scene/edge boundaries. Approximate20ms ASR grid; no invented subword boundaries.','first_hook_caption':new[0],'derived_animation_anchors':'Gateway result+.20s and ready/verification+.08/.03s illustrate ordering, not runtime. Recap load/resolve/supply/execute highlights align to Spring/wire/beans/manages in the concluding scope phrase; they are illustrative summary edits rather than narrated method calls.','hook_ending_asr_s':d['hook_asr_last_word_end'],'caption_word_count_range':[min(len(c['text'].split()) for c in new),max(len(c['text'].split()) for c in new)]}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
p.write_text(json.dumps(d,indent=2)+'\n')
def stamp(v):
 ms=round(v*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
(ROOT.parent.parent/'subtitles.srt').write_text('\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n" for i,c in enumerate(new,1)))
print(json.dumps({'captions':len(new),'max_characters':max(len(c['text']) for c in new),'cue_word_min':min(len(c['text'].split()) for c in new),'cue_word_max':max(len(c['text'].split()) for c in new),'duration':d['duration'],'scene_cues_absolute':d['scene_cues_absolute'],'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end'],'hook_utterance_end':new[0]['end']},indent=2))
