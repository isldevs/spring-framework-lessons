"""Align actual Bean naming speech and observed ASR words; preserve raw scores."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
['Two names. One ambiguous type.'],
['This factory method registers','a Client named alpha.','The annotation supplies','its explicit bean name.'],
['Ask for alpha by name,','and Spring returns that bean.','Add the type argument','to check its type too.'],
['With just one Client,','a type-only lookup returns','the same object.','Now register beta','as a second Client.'],
['Both beans have clear names,','but both match Client.','With no primary selected,','this type-only lookup is ambiguous.'],
['Our tests verify named results','and type failure.','Names identify beans;',"they don't resolve this type tie."],
['Thanks for watching.']]
def normalize(s):
 return re.findall(r'[a-z0-9]+',s.lower().replace('look up','lookup').replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
canonical=[];i=0
while i<len(words):
 if i+1<len(words) and words[i]['token']=='look' and words[i+1]['token']=='up':
  canonical.append({**words[i],'token':'lookup','end':words[i+1]['end'],'recognized_components':['look','up']});i+=2
 else:canonical.append(words[i]);i+=1
words=canonical
expected=normalize(' '.join(c['text'] for c in orig));observed=[w['token'] for w in words]
assert expected==observed,('Inspect raw ASR mismatch before alignment',expected,observed)
new=[];j=0;by_scene={}
for c,rows in zip(orig,CAPTIONS):
 tokens=normalize(c['text']);by_scene[c['scene']]=words[j:j+len(tokens)]
 assert tokens==normalize(' '.join(rows)),(tokens,rows)
 for i,text in enumerate(rows):
  count=len(normalize(text));start=c['start'] if i==0 else words[j]['start'];j+=count
  end=c['end'] if i==len(rows)-1 else words[j]['start']
  start=max(c['start'],start);end=min(c['end'],end)
  assert c['start']<=start<end<=c['end'],(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words) and len(orig)==len(CAPTIONS)==7
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
name=anchor(2,'alpha');definition=round(name+.10,6);instance=round(definition+.35,6)
request=anchor(3,'alpha');returned=round(request+.30,6);check=anchor(3,'type')
single=anchor(4,'type');single_return=round(single+.30,6)
second_register=anchor(4,'now');second_definition=round(anchor(4,'beta')+.10,6);second_instance=round(second_definition+.35,6)
query=anchor(5,'match');candidates=round(query+.10,6);failure=round(query+.30,6)
proof={'named':anchor(6,'named'),'type':anchor(6,'type'),'takeaway':anchor(6,'names'),'complete':round(min(word_end(6,'tie')+.03,d['recap_hold_start']-.05),6)}
start=scenes[6]['start'];absolute={'register':start,'named':proof['named'],'type':proof['type'],'names':proof['takeaway'],'complete':proof['complete'],'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['scene_cues_absolute']={
 'registration':{'register':scenes[2]['start'],'name':name,'definition':definition,'instance':instance},
 'named':{'request':request,'return':returned,'check':check},
 'single':{'lookup':single,'return':single_return},
 'second':{'register':second_register,'definition':second_definition,'instance':second_instance},
 'ambiguity':{'query':query,'candidates':candidates,'failure':failure,'primary':anchor(5,'primary')},
 'proof':proof,'recap':absolute}
assert definition<instance<request<returned<check<single<single_return<second_register<second_definition<second_instance<query<candidates<failure<scenes[6]['start']
assert scenes[3]['end']-returned>1 and scenes[3]['end']-check>1
assert scenes[4]['end']-single_return>1 and scenes[5]['end']-failure>1
assert scenes[4]['end']-second_instance>=.40
assert proof['complete']<d['recap_hold_start']
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['opening_cover_hold']=False;d['hook_text_display']=orig[0]['text'];d['hook_asr_last_word_end']=word_end(1,'type')
record={'text_transformations':[],'timing_sources':'Unmodified unprompted full-stream ASR with sample-derived utterance boundaries. No expected words inserted.','raw_wer_unchanged':True,'orthographic_alignment_normalization':'Optional look up/lookup compound alignment only; no such raw discrepancy in the current zero-WER run.','derived_animation_anchors':{'registration':'observed alpha word; definition+.10s, instance+.35s','named_lookup':'observed alpha request, returned reference+.30s; typed guard on type word','single_type':'observed type word and return+.30s','second':'observed now/beta registration; definition+.10s, instance+.35s','ambiguity':'observed match word, two candidates+.10s and failure+.30s','proof_recap':'observed named/type/names/tie words, then exact2s reading hold'},'scene_start_clamps':'Known synthesis edits constrain caption first/last boundaries and ASR drift. Intermediate ASR word times are approximately20ms-grid estimates.','hook_ending_asr_s':d['hook_asr_last_word_end']}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Sample-derived scene/first/last-caption edits; intermediate unprompted base.en ASR words. Raw recognition score unchanged. Derived0.30s lookup responses explain causality, not runtime performance. Exactly2s complete recap hold precedes separate spoken Thanks.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':len(new),'caption_max':max(len(c['text']) for c in new),'scene_cues_absolute':d['scene_cues_absolute'],'hook_end':d['hook_asr_last_word_end']},indent=2))
