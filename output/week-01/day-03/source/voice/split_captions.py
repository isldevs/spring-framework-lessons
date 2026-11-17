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
['The class compiles,','but the context has no','registration for it.','Asking for Client fails.'],
['Register FactoryConfig,','then refresh.','Its @Bean method returns the Client','that Spring manages.'],
['Or add the @Component annotation','to Worker,','then configure a scan of its package.','Spring discovers and registers it.'],
['The scan covers lesson.scan.','Outside lives in another package,',"so its annotation isn't picked up."],
['Our three tests pass:','both registered beans are found;','the class outside the scan','stays missing.','Registration tells Spring','what to manage.'],
['Thanks for watching.'],
]
def normalize(s):
 s=s.lower().replace('getbean','get bean').replace('class path','classpath')
 s=re.sub(r'\bfactory\s*config\b','factoryconfig',s)
 s=re.sub(r'\blesson(?:\s+dot\s+|\.)scan\b','lessonscan',s)
 return re.findall(r'[a-z0-9]+',s.replace('’','').replace("'",''))

asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
canonical=[];i=0
while i<len(words):
 if i+2<len(words) and [x['token'] for x in words[i:i+3]]==['lesson','dot','scan']:
  canonical.append({**words[i],'token':'lessonscan','end':words[i+2]['end'],'recognized_components':['lesson','dot','scan']});i+=3
 elif i+1<len(words) and [x['token'] for x in words[i:i+2]]==['factory','config']:
  canonical.append({**words[i],'token':'factoryconfig','end':words[i+1]['end'],'recognized_components':['factory','config']});i+=2
 elif i+1<len(words) and [x['token'] for x in words[i:i+2]]==['class','path']:
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
# Reveal the action on its spoken keyword, rather than waiting for a phrase end.
call=anchor(3,'returns');definition=anchor(3,'bean')
instance=anchor(3,'client');lookup=round(max(instance+.40,scenes[3]['end']-1.1),6)
assert scenes[3]['end']-lookup>=.75
assert scenes[3]['start']<=definition<call<instance<lookup<scenes[4]['start']
scan=anchor(4,'scan');scan_lookup=round(scenes[4]['end']-1.25,6)
scan_instance=round(min(scan+.40,scan_lookup-.45),6)
scan_definition=round(min(scan+.12,scan_instance-.15),6)
scanning={'annotation':anchor(4,'component'),'scan':scan,'definition':scan_definition,'instance':scan_instance,'lookup':scan_lookup}
assert scanning['annotation']<scan<scan_definition<scan_instance<scan_lookup<scenes[5]['start']
request=round(scenes[2]['start']+.12,6);failed=round(request+.30,6)
# Outside's exclusion is already the point when its name appears, not seconds later.
outside=anchor(5,'outside');miss=round(outside+.30,6)
proof={'bean':anchor(6,'found'),'scan':round(anchor(6,'outside')-.10,6),'outside':anchor(6,'missing'),'takeaway':anchor(6,'registration'),'complete':round(min(word_end(6,'manage')+.03,d['recap_hold_start']-.05),6)}
start=scenes[6]['start']
absolute={'register':start,'bean':proof['bean'],'factory':proof['bean'],'scan':proof['scan'],'definition':proof['takeaway'],'lookup':anchor(6,'manage'),'complete':proof['complete'],'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end']}
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['scene_cues_absolute']={
 'missing':{'request':request,'fail':failed,'definition':anchor(2,'registration'),'registration':anchor(2,'registration')},
 'factory':{'register':scenes[3]['start'],'configuration':anchor(3,'factoryconfig'),'definition':definition,'call':call,'instance':instance,'lookup':lookup},
 'scanning':scanning,
 'boundary':{'outside':outside,'annotation':anchor(5,'annotation'),'miss':miss},
 'proof':proof,'recap':absolute,
}
record={'text_transformations':[{'display':'@Bean','spoken':'bean'},{'display':'@Component','spoken':'component'},{'display':'FactoryConfig','spoken':'Factory Config'},{'display':'lesson.scan','spoken':'lesson dot scan'}],
 'timing_sources':'Untouched unprompted full-stream ASR, with sample-derived scene/utterance bounds overriding boundary drift only.',
 'raw_wer_unchanged':True,
 'orthographic_alignment_normalization':'Java class/package spellings merge independently recognized word spans; raw transcript and WER remain untouched.',
 'derived_animation_anchors':{'missing_lookup':'scene2start+.12s; expected failure .30s later','factory_definition':'bean word start','factory_call':'returns word start','factory_instance':'Client word start','factory_lookup':'after instance+.40s and about1.1s before next scene','scan_definition_instance':'scan+.12/.40s; lookup1.25s before next scene','outside_missing':'Outside word start+.30s','recap':'observed proof/takeaway words, then complete2s hold'},
 'scene_start_clamps':'Caption first/last boundaries use known synthesis edits; intermediate ASR boundaries stay within their utterance. Raw ASR is preserved.',
 'hook_ending_asr_s':word_end(1,'bean')}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Seven coherent scene utterances; exact sample-derived edit boundaries. Intermediate caption/event anchors use independent unprompted base.en ASR (~20ms grid). Annotation display punctuation is explicit. Raw WER unchanged. Derived factory/scanning/lookup/recap stages are explanatory timings, not runtime measurements. Exact2s reading hold precedes separate spoken Thanks.'
d['opening_cover_hold']=False;d['hook_text_display']=orig[0]['text'];d['hook_asr_last_word_end']=record['hook_ending_asr_s']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute,'scene_cues_absolute':d['scene_cues_absolute'],'hook_asr_last_word_end':d['hook_asr_last_word_end']},indent=2,ensure_ascii=False))
