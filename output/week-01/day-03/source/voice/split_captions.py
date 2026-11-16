"""Align bean-registration captions to independent ASR and sample-derived edits.

Raw transcript and strict WER are preserved. Public @Bean/@Component punctuation
spells the annotation names spoken naturally as bean/component.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
["Why isn't this a Spring bean?"],
['A class on the classpath',"isn't automatically registered.",'Give Spring a registration path.'],
['Register configuration','with a @Bean method.','Spring calls the factory','and manages its result.'],
['Or add the @Component annotation,','then scan the package','containing your class.'],
['Miss that package,','and even an annotated class','stays unregistered.'],
['Our tests retrieve both.','Two paths, one result:','Spring knows which beans to manage.'],
['Thanks for watching.'],
]
def normalize(s):
 s=s.lower().replace('getbean','get bean').replace('class path','classpath')
 return re.findall(r'[a-z0-9]+',s.replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
canonical=[];i=0
while i<len(words):
 if i+1<len(words) and words[i]['token']=='class' and words[i+1]['token']=='path':
  canonical.append({**words[i],'token':'classpath','end':words[i+1]['end'],'recognized_components':['class','path']});i+=2
 else:canonical.append(words[i]);i+=1
words=canonical
expected=normalize(' '.join(c['text'] for c in orig));observed=[w['token'] for w in words]
assert expected==observed,('Inspect raw ASR mismatch before alignment',expected,observed)
new=[];j=0;by_scene={}
for c,rows in zip(orig,CAPTIONS):
 tokens=normalize(c['text']);by_scene[c['scene']]=words[j:j+len(tokens)]
 assert tokens==normalize(' '.join(rows))
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
 hits=[w for w in by_scene[number] if w['token']==token]
 return round(min(scenes[number]['end'],hits[occurrence]['end']),6)
call=anchor(3,'calls');definition=round(min(word_end(3,'method')+.06,call-.12),6)
instance=anchor(3,'result');lookup=round(instance+.40,6)
assert scenes[3]['end']-lookup>=1.0
assert scenes[3]['start']<definition<call<instance<lookup<scenes[4]['start']
scan=anchor(4,'scan');span=scenes[4]['end']-.08-scan
assert span>.75
scan_lookup=round(scenes[4]['end']-1.50,6)
scan_instance=round(min(scan+.38,scan_lookup-.45),6)
scan_definition=round(min(scan+.12,scan_instance-.15),6)
scanning={'annotation':anchor(4,'component'),'scan':scan,'definition':scan_definition,'instance':scan_instance,'lookup':scan_lookup}
assert scanning['annotation']<scanning['scan']<scanning['definition']<scanning['instance']<scanning['lookup']<scenes[5]['start']
proof={'bean':anchor(6,'retrieve'),'scan':anchor(6,'both'),'takeaway':anchor(6,'two'),'complete':round(min(word_end(6,'manage')+.10,d['recap_hold_start']-.05),6)}
start=scenes[6]['start']
absolute={'register':start,'bean':proof['bean'],'factory':proof['bean'],'scan':proof['scan'],'definition':anchor(6,'spring'),'lookup':anchor(6,'manage'),'complete':proof['complete'],'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['scene_cues_absolute']={
 'missing':{'request':round(scenes[2]['start']+.35,6),'fail':anchor(2,'registered'),'definition':anchor(2,'registration'),'registration':anchor(2,'registration')},
 'factory':{'register':scenes[3]['start'],'configuration':anchor(3,'configuration'),'definition':definition,'call':call,'instance':instance,'lookup':lookup},
 'scanning':scanning,
 'boundary':{'outside':scenes[5]['start'],'annotation':anchor(5,'annotated'),'miss':anchor(5,'unregistered')},
 'proof':proof,
 'recap':absolute,
}
record={'text_transformations':[{'display':'@Bean','spoken':'bean','reason':'Java annotation spelling; punctuation omitted for strict speech-word comparison'},{'display':'@Component','spoken':'component','reason':'Java annotation spelling; punctuation omitted for strict speech-word comparison'}],
 'timing_sources':'asr-alignment.json: unprompted full-stream ASR plus separate unprompted final-phrase crop only if required',
 'raw_wer_unchanged':True,'orthographic_alignment_normalization':"Recognized 'class path' uses one technical compound classpath for caption alignment; raw transcript and strict WER are unchanged.",
 'derived_animation_anchors':{'factory_definition':'method word end +.06s, capped .12s before calls','factory_lookup':'instance reveal +.40s; current1.011125s reading window before next scene','scan_registration_instance_lookup':'definition scan+.12s, instance scan+.38s; lookup next scene start−1.50s, instance capped .45s before lookup','missing_request':'sample-derived scene2start+.35s','recap_steps':'known scene start and observed retrieve/both/Spring/manage word anchors; illustrative overview stages'},
 'scene_start_clamps':'First/last cue boundaries use exact sample-derived utterance edits. Intermediate ASR times are clamped within their utterance. ASR short-outro drift into the reading hold is overridden by known synthesis edits, with raw timestamps retained. No words inserted.',
 'hook_ending_asr_s':word_end(1,'bean')}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Seven coherent scene utterances; exact sample-derived edit boundaries. Intermediate caption/event anchors use independent unprompted base.en ASR (~20ms grid). Annotation display punctuation is explicit. Raw WER unchanged. Derived factory/scanning/lookup/recap stages are explanatory timings, not runtime measurements. Exact2s reading hold precedes separate spoken Thanks.'
d['opening_cover_hold']=False;d['hook_text_display']=orig[0]['text'];d['hook_asr_last_word_end']=record['hook_ending_asr_s']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute,'scene_cues_absolute':d['scene_cues_absolute'],'hook_asr_last_word_end':d['hook_asr_last_word_end']},indent=2,ensure_ascii=False))
