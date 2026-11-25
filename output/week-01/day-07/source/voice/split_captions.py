"""Align final Context smoke test speech to independent observed ASR words."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());phrases=d['phrases']
CAPTIONS=[
 ['Context loaded. Wiring checked?'],
 ["Spring's JUnit support loads",'our configuration before the test.','It creates a repository','and supplies it to our service.'],
 ['Retrieve the required service bean','from the context.'],
 ['Compare its repository',"with the context's repository.","Assert they're the same object.","Matching values aren't enough."],
 ['Run the smoke test.','It passes: context loaded,','required bean found,','expected dependency confirmed.'],
 ['This checks wiring','for our configuration.','Test order behavior separately.','Load, look up, assert.'],
 ['Thanks for watching.']]
def normalize(s):return re.findall(r'[a-z0-9]+',s.lower().replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
substitutions=asr.get('script_alignment_transformations',[])
for correction in sorted(substitutions,key=lambda x:x['raw_token_start'],reverse=True):
 a,b=correction['raw_token_start'],correction['raw_token_end']
 assert [w['token'] for w in words[a:b]]==correction['observed_tokens']
 first=words[a]
 replacement=[{**first,'token':token,'start':correction['start'],'end':correction['end'],'caption_alignment_only':True} for token in correction['script_tokens']]
 words[a:b]=replacement
expected=normalize(' '.join(c['text'] for c in phrases));observed=[w['token'] for w in words]
assert expected==observed,('Inspect raw ASR mismatch before alignment',expected,observed)
new=[];j=0;by_scene={}
for c,rows in zip(phrases,CAPTIONS):
 tokens=normalize(c['text']);by_scene[c['scene']]=words[j:j+len(tokens)]
 assert tokens==normalize(' '.join(rows)),(tokens,rows)
 for i,text in enumerate(rows):
  count=len(normalize(text));start=c['start'] if i==0 else words[j]['start'];j+=count
  end=c['end'] if i==len(rows)-1 else words[j]['start']
  start=max(c['start'],start);end=min(c['end'],end)
  assert c['start']<=start<end<=c['end'],(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words) and len(phrases)==len(CAPTIONS)==7
assert max(len(c['text']) for c in new)<=40
for a,b in zip(new,new[1:]):assert a['end']<=b['start']
d['captions']=new
scenes={s['scene']:s for s in d['scenes']}
def anchor(number,token,occurrence=0):
 hits=[w for w in by_scene[number] if w['token']==token];assert len(hits)>occurrence,(number,token,occurrence)
 return round(max(scenes[number]['start'],hits[occurrence]['start']),6)
def word_end(number,token,occurrence=0):
 hits=[w for w in by_scene[number] if w['token']==token];assert len(hits)>occurrence,(number,token,occurrence)
 return round(min(scenes[number]['end'],hits[occurrence]['end']),6)
load={'configuration':anchor(2,'configuration'),'repo':anchor(2,'repository'),'injection':anchor(2,'supplies'),'ready':round(min(word_end(2,'service')+.05,phrases[1]['end']-.03),6)}
lookup={'request':scenes[3]['start'],'return':round(min(word_end(3,'service')+.15,phrases[2]['end']-.15),6)}
identity={'repository':anchor(4,'repository',1),'actual':anchor(4,'repository'),'expected':anchor(4,'repository',1),'assertion':anchor(4,'assert'),'pass':round(min(word_end(4,'object')+.10,phrases[3]['end']-.1),6)}
proof={'result':scenes[5]['start'],'pass':anchor(5,'passes'),'bean':anchor(5,'bean'),'wiring':anchor(5,'dependency')}
recap={'scope':scenes[6]['start'],'behavior':anchor(6,'behavior'),'load':anchor(6,'load'),'lookup':anchor(6,'look'),'assert':anchor(6,'assert'),'complete':round(min(word_end(6,'assert')+.03,d['recap_hold_start']-.05),6)}
# The recognizer gives Load a zero-duration span at the compound lookup start.
# Stagger ONLY illustrative diagram edits; do not alter raw word timestamps.
recap_derivation={'needed':False}
if recap['lookup']<=recap['load']:
 original=recap['lookup'];recap['lookup']=round(min(recap['load']+.16,recap['assert']-.08),6)
 assert recap['load']<recap['lookup']<recap['assert']
 recap_derivation={'needed':True,'observed_load_start':recap['load'],'observed_lookup_start':original,'derived_lookup_reveal':recap['lookup'],'basis':'ASR Load has zero duration at lookup start. Diagram reveals are staggered by160ms for readability within the phrase; this is an illustrative edit, not an observed subword boundary or Spring runtime.'}
d['recap_edit_derivation']=recap_derivation
d['scene_cues_absolute']={'load':load,'lookup':lookup,'identity':identity,'proof':proof,'recap':recap}
absolute={**recap,'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['recap_cues_absolute']=absolute
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scenes[6]['start'],6) for k,v in absolute.items()}}
d['opening_cover_hold']=False;d['hook_text_display']=phrases[0]['text'];d['hook_asr_last_word_end']=word_end(1,'checked')
record={'text_transformations':substitutions,'timing_sources':'Unmodified unprompted full-stream ASR with sample-derived utterance boundaries. Any caption-only label transformations are explicitly listed; raw transcript and error score are unchanged. No timing spans invented.','raw_wer_unchanged':True,'derived_animation_anchors':'Script keyword spans; required service return+.15s and identity success+.10s illustrate cause and effect, not measured Spring runtime.','scene_start_clamps':'Known synthesis edits constrain caption first/last boundaries and ASR drift. Intermediate ASR word times are approximately20ms-grid estimates.','hook_ending_asr_s':d['hook_asr_last_word_end'],'recap_edit_derivation':recap_derivation}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Sample-derived scene/first/last-caption edits; intermediate unprompted small.en ASR word spans. Raw recognition and error score remain unchanged; any caption-only transformations retain explicit provenance. Derived lookup/identity results illustrate causality, not runtime performance. Exactly2s complete recap hold precedes separate spoken Thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def stamp(v):
 ms=round(v*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
(ROOT.parent.parent/'subtitles.srt').write_text('\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n" for i,c in enumerate(new,1)))
print(json.dumps({'captions':len(new),'caption_max':max(len(c['text']) for c in new),'scene_cues_absolute':d['scene_cues_absolute'],'recap_cues_absolute':absolute,'hook_end':d['hook_asr_last_word_end']},indent=2))
