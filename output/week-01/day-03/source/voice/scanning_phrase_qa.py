"""Independent unprompted recognition of the actual component-scanning utterance.

Preserves full-stream raw ASR/WER; does not insert expected text.
"""
from pathlib import Path
import json,numpy as np,soundfile as sf
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent
m=json.loads((R.parent/'timing.json').read_text());phrase=m['phrases'][3]
y,sr=sf.read(R.parent.parent/'narration.wav');clip=y[round(phrase['start']*sr):round(phrase['end']*sr)]
model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=3,download_root=str(R/'models/asr'))
segments,info=model.transcribe(resample_poly(clip,16000,sr).astype(np.float32),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
ss=[]
for s in segments:
 ss.append({'start':s.start+phrase['start'],'end':s.end+phrase['start'],'text':s.text,'avg_logprob':s.avg_logprob,'words':[{'word':w.word,'start':w.start+phrase['start'],'end':w.end+phrase['start'],'probability':w.probability} for w in s.words]})
a={'model':'faster-whisper base.en int8','initial_prompt':None,'scene':4,'segment_start':phrase['start'],'segment_end':phrase['end'],'expected':phrase['text'],'recognized':' '.join(s['text'] for s in ss),'segments':ss,'full_stream_raw_score_unchanged':True}
(R/'supplemental-scanning-asr.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))
