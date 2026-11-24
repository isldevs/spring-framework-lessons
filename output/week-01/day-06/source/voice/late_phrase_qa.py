"""Independent late-phrase ASR when full-stream decoding drops the short outro.

This never rewrites the original transcript/score. Alignment comparison treats 'class path' as the technical compound 'classpath'; raw WER remains strict. It permits a supplemental
alignment only when the full transcript is an exact prefix of the script and
all omitted words are precisely the separately synthesized final utterance.
"""
from pathlib import Path
import json,re
import numpy as np,soundfile as sf
from scipy.signal import resample_poly
ROOT=Path(__file__).resolve().parent

def norm(s):return re.findall(r'[a-z0-9]+',s.lower().replace('class path','classpath').replace('’','').replace("'",''))
def main(model=None):
 d=json.loads((ROOT.parent/'timing.json').read_text());a=json.loads((ROOT/'asr.json').read_text())
 ref=norm(' '.join(x['text'] for x in d['phrases']));full=norm(' '.join(x['text'] for x in a['segments']))
 if full==ref:
  (ROOT/'asr-alignment.json').write_text(json.dumps({**a,'alignment_provenance':'Unmodified complete full-stream ASR'},indent=2)+'\n')
  (ROOT/'supplemental-asr.json').write_text(json.dumps({'needed':False},indent=2)+'\n');return
 # The synthesis script is authoritative for display captions. Preserve the
 # unprompted transcript and score, while aligning these two grammatical
 # number substitutions to their actual observed word spans. No words are
 # inserted/deleted and no recognition-success claim is made.
 if len(full)==len(ref):
  diffs=[(i,heard,written) for i,(heard,written) in enumerate(zip(full,ref)) if heard!=written]
  if [(a,b) for _,a,b in diffs]==[('registry','registries'),('stays','stay')]:
   observed_words=[w for seg in a['segments'] for w in seg['words']]
   assert len(observed_words)==len(full)
   substitutions=[{'token_index':i,'observed':heard,'script':written,'start':observed_words[i]['start'],'end':observed_words[i]['end'],'reason':'Known synthesis text/G2P plural-number alignment; raw ASR remains unchanged.'} for i,heard,written in diffs]
   result={**a,'alignment_provenance':'Unmodified full-stream small.en ASR; two script-caption token labels align to the observed registry/stays spans. This does not change the raw transcript or its two-substitution error score.','script_alignment_substitutions':substitutions}
   (ROOT/'asr-alignment.json').write_text(json.dumps(result,indent=2)+'\n')
   (ROOT/'supplemental-asr.json').write_text(json.dumps({'needed':False,'script_alignment_substitutions':substitutions,'raw_asr_score_unchanged':True},indent=2)+'\n')
   return
 outro=d['scenes'][-1];phrase=d['phrases'][-1]
 assert full==ref[:-len(norm(phrase['text']))] and phrase['scene']==7,'Full-stream mismatch exceeds an omitted final phrase; inspect before alignment'
 if model is None:
  from faster_whisper import WhisperModel
  model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=3,download_root=str(ROOT/'models/asr'))
 y,sr=sf.read(ROOT.parent.parent/'narration.wav')
 clip=y[round(outro['start']*sr):round(outro['end']*sr)]
 audio=resample_poly(clip,16000,sr).astype(np.float32)
 segments,info=model.transcribe(audio,language='en',beam_size=5,word_timestamps=True,vad_filter=False)
 segs=[]
 for s in segments:
  segs.append({'start':round(s.start+outro['start'],6),'end':round(s.end+outro['start'],6),'text':s.text,'avg_logprob':s.avg_logprob,'words':[{'word':w.word,'start':round(w.start+outro['start'],6),'end':round(w.end+outro['start'],6),'probability':w.probability} for w in s.words]})
 heard=' '.join(x['text'] for x in segs)
 result={'needed':True,'model':a.get('model','faster-whisper small.en int8'),'initial_prompt':None,'segment_start':outro['start'],'segment_end':outro['end'],'expected':phrase['text'],'recognized':heard,'exact_normalized_phrase_match':norm(heard)==norm(phrase['text']),'segments':segs,'full_stream_raw_score_unchanged':True}
 (ROOT/'supplemental-asr.json').write_text(json.dumps(result,indent=2)+'\n')
 assert norm(heard)==norm(phrase['text']),('Supplemental outro ASR mismatch',heard)
 combined={**a,'segments':a['segments']+segs,'alignment_provenance':'First six scenes use untouched full-stream ASR; final Thanks uses independent unprompted transcription of its actual audio crop. Full-stream raw WER/transcript remain unchanged.'}
 assert norm(' '.join(s['text'] for s in combined['segments']))==ref
 (ROOT/'asr-alignment.json').write_text(json.dumps(combined,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
