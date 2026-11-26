"""Retain raw ASR and document only the reviewed compound-token caption merges."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent

def norm(s):return re.findall(r'[a-z0-9]+',s.lower().replace('’','').replace("'",''))
def main(model=None):
 d=json.loads((ROOT.parent/'timing.json').read_text());a=json.loads((ROOT/'asr.json').read_text())
 ref=norm(' '.join(x['text'] for x in d['phrases']))
 observed=[dict(w,token=t) for seg in a['segments'] for w in seg['words'] for t in norm(w['word'])]
 full=[w['token'] for w in observed];i=j=0;transforms=[]
 while i<len(full) and j<len(ref):
  if full[i]==ref[j]:i+=1;j+=1;continue
  if full[i:i+2]==['auto','wired'] and ref[j]=='autowired':
   count=2;target=['autowired'];reason='Orthographic compound: two observed auto/wired spans map to scripted Autowired; raw recognition remains unchanged.'
  elif full[i:i+2]==['payment','gateway'] and ref[j]=='paymentgateway':
   count=2;target=['paymentgateway'];reason='CamelCase class label: two observed payment/gateway spans map to scripted PaymentGateway; no unheard timing span is created.'
  else:raise AssertionError(('Unreviewed recognition difference',i,j,full[i:i+4],ref[j:j+4]))
  transforms.append({'raw_token_start':i,'raw_token_end':i+count,'observed_tokens':full[i:i+count],'script_tokens':target,'start':observed[i]['start'],'end':observed[i+count-1]['end'],'reason':reason})
  i+=count;j+=len(target)
 assert i==len(full) and j==len(ref),(i,j,len(full),len(ref))
 result={**a,'alignment_provenance':'Unmodified unprompted small.en full-stream ASR plus explicit reviewed compound spelling merges for caption labels. No raw word, timestamp, transcript, WER or model result is altered.','script_alignment_transformations':transforms}
 (ROOT/'asr-alignment.json').write_text(json.dumps(result,indent=2)+'\n')
 (ROOT/'supplemental-asr.json').write_text(json.dumps({'needed':False,'reason':'Full final narration recognized; only reviewed compound spellings need caption labels.','script_alignment_transformations':transforms,'raw_asr_score_unchanged':True},indent=2)+'\n')
 pending=ROOT/'alignment-error.json'
 if pending.exists():
  (ROOT/'alignment-review-initial.json').write_text(json.dumps({'resolved_by':'Three explicit compound spelling caption-label merges','initial_error':json.loads(pending.read_text()),'raw_asr_preserved':True},indent=2)+'\n');pending.unlink()
 print(json.dumps({'alignment_ready':True,'compound_merges':len(transforms),'raw_asr_score_unchanged':True},indent=2))
if __name__=='__main__':main()
