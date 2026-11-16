"""Align ApplicationContext captions and render anchors to independent ASR.

Raw ASR text/WER remain unchanged. Public code spelling normalization is explicit:
ApplicationContext -> application context; getBean -> get bean.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
p=ROOT.parent/'timing.json';d=json.loads(p.read_text());orig=d['phrases']
CAPTIONS=[
["What's inside ApplicationContext?"],
['Bean definitions are recipes.','Managed instances','are the actual objects.'],
['Register configuration,','then refresh.','Spring reads the definitions','and creates our singleton beans.'],
['Calling getBean returns the service,','already wired to its repository.'],
['The context also publishes events.','Close it,','and managed cleanup runs.'],
['Our tests confirm: same service,','one event, cleanup called.','Definitions describe;','instances do the work.'],
['Thanks for watching.'],
]
def normalize(s):
 s=s.lower().replace('applicationcontext','application context').replace('getbean','get bean').replace('clean up','cleanup')
 return re.findall(r'[a-z0-9]+',s.replace('’','').replace("'",''))
asr=json.loads((ROOT/'asr-alignment.json').read_text());words=[]
for s in asr['segments']:
 for w in s['words']:
  for token in normalize(w['word']):words.append(dict(w,token=token))
canonical=[]
i=0
while i<len(words):
 if i+1<len(words) and words[i]['token']=='clean' and words[i+1]['token']=='up':
  canonical.append({**words[i],'token':'cleanup','end':words[i+1]['end'],'recognized_components':['clean','up']});i+=2
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
  # ASR word times can precede sample-derived scene edits by one 20ms grid cell.
  start=max(c['start'],start);end=min(c['end'],end)
  assert c['start']<=start<end<=c['end'],(c,text,start,end)
  new.append({'scene':c['scene'],'start':round(start,6),'end':round(end,6),'text':text})
assert j==len(words) and len(orig)==len(CAPTIONS)==7
assert max(len(c['text']) for c in new)<=40
for a,b in zip(new,new[1:]):assert a['end']<=b['start']
d['captions']=new
scene_map={s['scene']:s for s in d['scenes']}
def anchor(number,token,occurrence=0):
 hits=[w for w in by_scene[number] if w['token']==token]
 assert len(hits)>occurrence,(number,token,occurrence)
 return round(max(scene_map[number]['start'],hits[occurrence]['start']),6)
def word_end(number,token,occurrence=0):
 hits=[w for w in by_scene[number] if w['token']==token]
 return round(min(scene_map[number]['end'],hits[occurrence]['end']),6)
creation=anchor(3,'creates')
repo=round(creation+.08,6)
service=round(min(repo+.60,scene_map[4]['start']-.20),6)
init={'register':scene_map[3]['start'],'configuration':anchor(3,'configuration'),'refresh':anchor(3,'refresh'),'definitions':anchor(3,'definitions'),'create':creation,'repo':repo,'service':service}
assert init['register']<init['refresh']<init['definitions']<repo<service<scene_map[4]['start']
proof={'same':anchor(6,'same'),'event':anchor(6,'event'),'cleanup':anchor(6,'cleanup'),'takeaway':anchor(6,'definitions'),'complete':round(min(word_end(6,'called')+.10,d['recap_hold_start']-.10),6)}
scene_start=scene_map[6]['start'];hold_start=d['recap_hold_start']
absolute={'register':scene_start,'definitions':round(scene_start+.35,6),'create':round(scene_start+.80,6),'lookup':proof['same'],'event':proof['event'],'close':proof['cleanup'],'complete':proof['complete'],'recap_hold_start':hold_start,'recap_hold_end':d['recap_hold_end']}
d['recap_cues']={'relative_to':'scene_start',**{k:round(v-scene_start,6) for k,v in absolute.items()}}
d['recap_cues_absolute']=absolute
d['scene_cues_absolute']={
 'distinction':{'recipe':scene_map[2]['start'],'definitions':anchor(2,'definitions'),'instance':anchor(2,'managed'),'objects':anchor(2,'objects')},
 'initialization':init,
 'mechanism':dict(init),
 'lookup':{'request':anchor(4,'get'),'return':anchor(4,'returns'),'returns':anchor(4,'returns'),'wired':anchor(4,'wired'),'repository':anchor(4,'repository')},
 'services':{'event':anchor(5,'events'),'publish':anchor(5,'publishes'),'close':anchor(5,'close'),'cleanup':anchor(5,'cleanup')},
 'proof':proof,
 'recap':absolute,
}
record={'text_transformations':[{'display':'ApplicationContext','spoken':'application context','reason':'Conventional Java type spelling; words and raw ASR unchanged'},{'display':'getBean','spoken':'get bean','reason':'Conventional Java method spelling; words and raw ASR unchanged'}],
 'orthographic_alignment_normalization':"If observed as separate 'clean up', merge timing spans for the spoken noun cleanup. Raw ASR text/strict WER remain unchanged.",
 'timing_sources':'asr-alignment.json: untouched full-stream ASR, plus separate unprompted final-phrase crop only if required',
 'raw_wer_unchanged':True,
 'derived_animation_anchors':{'repo':'creates word start + .08s','service':'repo anchor + .60s, capped .20s before lookup scene','recap_register_definitions_create':'sample-derived recap scene start plus 0/.35/.80s, overview staging before observed proof words','recap_complete':'called word end + .10s, capped .10s before recap hold'},
 'scene_start_clamps':'First/last cue boundaries use exact sample-derived utterance edits. Intermediate ASR times are clamped within their utterance. Raw ASR may place the short Thanks word inside the preceding quiet hold; known synthesis boundaries take precedence and raw ASR is preserved. No word insertion',
 'hook_ending_asr_s':word_end(1,'context')}
(ROOT/'alignment-normalization.json').write_text(json.dumps(record,indent=2)+'\n')
d['caption_method']='Seven coherent single-batch utterances; exact sample-derived scene edits. Caption and event anchors use independent unprompted base.en ASR (~20ms grid). Public ApplicationContext/getBean spelling is explicitly normalized to the spoken words for comparison. Raw transcript/WER unchanged; independent outro crop used only if required. Repo/service and recap substeps are documented illustrative timings, not runtime measurements. Exact2s recap reading hold precedes separate spoken Thanks.'
d['opening_cover_hold']=False
d['hook_text_display']="What's inside ApplicationContext?"
d['hook_asr_last_word_end']=record['hook_ending_asr_s']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'captions':new,'recap_cues_absolute':absolute,'scene_cues_absolute':d['scene_cues_absolute'],'hook_asr_last_word_end':d['hook_asr_last_word_end']},indent=2,ensure_ascii=False))
