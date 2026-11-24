"""Align final Multiple contexts speech to independent observed ASR words."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());phrases=d['phrases']
CAPTIONS=[
 ['Two contexts. Different beans?'],
 ['Yes. Register alpha','in context A, and beta in B.','Each independent context','has its own registry.'],
 ['Context A finds alpha,','but beta is missing.','Sharing one Java application',"doesn't connect these registries."],
 ['Create a fresh parent and child.','Set the parent before','refreshing the child.','The registries stay separate.'],
 ['The child checks locally first.','A missing named bean','can be found in its parent.'],
 ['The parent cannot search','its children.','Our tests confirm both directions:','child to parent works;',"parent to child doesn't."],
 ['Thanks for watching.']]
def normalize(s):return re.findall(r'[a-z0-9]+',s.lower().replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
substitutions=asr.get('script_alignment_substitutions',[])
for correction in substitutions:
 i=correction['token_index']
 assert words[i]['token']==correction['observed']
 # Keep words[i]['word'] exactly as recognized. Only the separate caption
 # alignment token uses the known synthesis label, with provenance below.
 words[i]['token']=correction['script']
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
registration={'alpha':anchor(2,'alpha'),'beta':anchor(2,'beta'),'registry':anchor(2,'registry')}
isolation={'request':scenes[3]['start'],'alpha':anchor(3,'alpha'),'found':round(anchor(3,'alpha')+.15,6),'beta':anchor(3,'beta'),'missing':anchor(3,'missing'),'same_app':anchor(3,'sharing')}
link={'fresh':anchor(4,'create'),'set':anchor(4,'set'),'refresh':anchor(4,'refreshing'),'separate':anchor(4,'registries')}
fallback={'local':anchor(5,'locally'),'missing':anchor(5,'missing'),'parent':anchor(5,'parent'),'return':round(min(anchor(5,'parent')+.20,scenes[5]['end']-.25),6)}
proof={'reverse':anchor(6,'parent'),'missing':anchor(6,'children'),'tests':anchor(6,'tests'),'upward':anchor(6,'child'),'downward':anchor(6,'parent',2),'complete':round(min(word_end(6,'doesnt')+.03,d['recap_hold_start']-.05),6)}
d['scene_cues_absolute']={'registration':registration,'isolation':isolation,'link':link,'fallback':fallback,'proof':proof}
absolute={**proof,'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['recap_cues_absolute']=absolute
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scenes[6]['start'],6) for k,v in absolute.items()}}
d['opening_cover_hold']=False;d['hook_text_display']=phrases[0]['text'];d['hook_asr_last_word_end']=word_end(1,'beans')
record={'text_transformations':substitutions,'timing_sources':'Unmodified unprompted full-stream ASR with sample-derived utterance boundaries. Two known synthesis caption labels registries/stay align to observed registry/stays spans; raw transcript and error score are unchanged. No timing spans inserted.','raw_wer_unchanged':True,'derived_animation_anchors':'Named script words; alpha result+.15s and parent reference return+.20s illustrate cause and effect, not measured Spring runtime.','scene_start_clamps':'Known synthesis edits constrain caption first/last boundaries and ASR drift. Intermediate ASR word times are approximately20ms-grid estimates.','hook_ending_asr_s':d['hook_asr_last_word_end']}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Sample-derived scene/first/last-caption edits; intermediate unprompted small.en ASR word spans. Two known synthesis labels registries/stay map to observed registry/stays with explicit provenance. Raw recognition score unchanged. Derived lookup returns illustrate causality, not runtime performance. Exactly2s complete recap hold precedes separate spoken Thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def stamp(v):
 ms=round(v*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
(ROOT.parent.parent/'subtitles.srt').write_text('\n'.join(f"{i}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n" for i,c in enumerate(new,1)))
print(json.dumps({'captions':len(new),'caption_max':max(len(c['text']) for c in new),'scene_cues_absolute':d['scene_cues_absolute'],'recap_cues_absolute':absolute,'hook_end':d['hook_asr_last_word_end']},indent=2))
