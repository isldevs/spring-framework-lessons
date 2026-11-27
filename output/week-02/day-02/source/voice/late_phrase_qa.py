"""Retain raw ASR; derive caption labels from the exact known synthesis input.

These are text alignment operations, not a listening review or a new ASR score.
"""
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
  if full[i:i+2]==['payment','gateway'] and ref[j]=='paymentgateway':
   count=2;target=['paymentgateway'];reason='CamelCase class label: two observed payment/gateway spans map to scripted PaymentGateway; no unheard timing span is created.'
  elif full[i:i+4]==['and','unrelated','logger','wont'] and ref[j:j+4]==['an','unrelated','logger','wont']:
   count=1;target=['an'];reason='Known synthesis input says An unrelated, while raw recognition says and unrelated. Reuse the observed token span for the scripted caption only; pronunciation remains unverified and raw error remains in the score.'
  else:raise AssertionError(('Unreviewed recognition difference',i,j,full[i:i+4],ref[j:j+4]))
  transforms.append({'raw_token_start':i,'raw_token_end':i+count,'observed_tokens':full[i:i+count],'script_tokens':target,'start':observed[i]['start'],'end':observed[i+count-1]['end'],'reason':reason})
  i+=count;j+=len(target)
 assert i==len(full) and j==len(ref),(i,j,len(full),len(ref))
 result={**a,'alignment_provenance':'Unmodified unprompted small.en full-stream ASR plus explicit known-input caption-label mappings. No raw word, timestamp, transcript, WER or model result is altered. These mappings do not establish auditory pronunciation.','script_alignment_transformations':transforms}
 (ROOT/'asr-alignment.json').write_text(json.dumps(result,indent=2)+'\n')
 (ROOT/'supplemental-asr.json').write_text(json.dumps({'needed':False,'reason':'Full-stream narration and outro have observed spans. One compound spelling and one An/and difference need known-input caption labels; no additional recognition was run.','script_alignment_transformations':transforms,'raw_asr_score_unchanged':True},indent=2)+'\n')
 pending=ROOT/'alignment-error.json'
 if pending.exists():
  (ROOT/'alignment-review-initial.json').write_text(json.dumps({'resolved_by':'Explicit caption-only An/and mapping in addition to PaymentGateway compound merge','initial_error':json.loads(pending.read_text()),'raw_asr_preserved':True,'auditory_pronunciation_unverified':True},indent=2)+'\n');pending.unlink()
 print(json.dumps({'alignment_ready':True,'caption_label_mappings':len(transforms),'raw_asr_score_unchanged':True},indent=2))
if __name__=='__main__':main()
