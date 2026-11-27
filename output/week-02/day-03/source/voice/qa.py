"""Objective voice QA and independent speech recognition; no subjective listening claim."""
import os,json,re,argparse,hashlib
from pathlib import Path
os.environ['HF_HUB_DISABLE_XET']='1'
import numpy as np,soundfile as sf
from scipy.signal import resample_poly
from faster_whisper import WhisperModel
from huggingface_hub import snapshot_download
ROOT=Path(__file__).resolve().parent;OUT=ROOT.parent.parent
parser=argparse.ArgumentParser();parser.add_argument('--asr-model',default='base.en');args=parser.parse_args()
print('Loading Whisper '+args.asr_model,flush=True)
asr_model=args.asr_model
if args.asr_model=='small.en':
 pinned=json.loads((ROOT/'asr-model.json').read_text())
 snapshot=Path(snapshot_download(pinned['repo_id'],revision=pinned['revision'],cache_dir=str(ROOT/'models/asr'),allow_patterns=list(pinned['files'])))
 for filename,digest in pinned['files'].items():assert hashlib.sha256((snapshot/filename).read_bytes()).hexdigest()==digest
 asr_model=str(snapshot)
model=WhisperModel(asr_model,device='cpu',compute_type='int8',cpu_threads=4,download_root=str(ROOT/'models/asr'))
raw,raw_sr=sf.read(OUT/'narration.wav'); asr_audio=resample_poly(raw,16000,raw_sr).astype(np.float32)
segments,info=model.transcribe(asr_audio,language='en',beam_size=5,word_timestamps=True,vad_filter=False)
segs=[]
for s in segments:
 d={'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'words':[{'word':w.word,'start':w.start,'end':w.end,'probability':w.probability} for w in s.words]};segs.append(d);print(d,flush=True)
(ROOT/'asr.json').write_text(json.dumps({'model':'faster-whisper '+args.asr_model+' int8','language':info.language,'segments':segs},indent=2)+'\n')
def normalize(text):
 return re.findall(r'[a-z0-9]+',text.lower().replace('’','').replace("'",''))
meta=json.loads((ROOT.parent/'timing.json').read_text())
ref=normalize(' '.join(c['text'] for c in meta['phrases']))
transcript=' '.join(c['text'].strip() for c in segs);hyp=normalize(transcript)
prev=list(range(len(hyp)+1))
for i,a in enumerate(ref,1):
 curr=[i]
 for j,b in enumerate(hyp,1):curr.append(min(curr[-1]+1,prev[j]+1,prev[j-1]+(a!=b)))
 prev=curr
summary={'model':'faster-whisper '+args.asr_model+' int8','narration_sha256':hashlib.sha256((OUT/'narration.wav').read_bytes()).hexdigest(),'reference_words':len(ref),'asr_words':len(hyp),'edit_distance':prev[-1],'normalized_word_error_rate':prev[-1]/len(ref),'transcript':transcript,'normalization':'lowercase, strip apostrophes, punctuation to word boundaries; no ASR prompt'}
(ROOT/'asr-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(summary,flush=True)
y,sr=sf.read(OUT/'narration.wav');rms=np.sqrt(np.mean(y*y));nz=np.where(np.abs(y)>0.001)[0]
metrics={'duration_s':len(y)/sr,'sample_rate':sr,'channels':1,'peak_dbfs':float(20*np.log10(np.max(np.abs(y)))),'rms_dbfs':float(20*np.log10(rms)),'clipped_samples':int(np.sum(np.abs(y)>=0.9999)),'speech_above_minus60db_onset_s':float(nz[0]/sr),'speech_above_minus60db_end_s':float(nz[-1]/sr),'endpoint_first_sample':float(y[0]),'endpoint_last_sample':float(y[-1])}
print(metrics,flush=True)
try:
 import librosa
 z=resample_poly(y,1,3)
 f0,voiced,vp=librosa.pyin(z,fmin=60,fmax=400,sr=16000,frame_length=1024,hop_length=160)
 f=f0[voiced & np.isfinite(f0)]
 metrics.update({'f0_voiced_frames':int(len(f)),'f0_10pct_hz':float(np.percentile(f,10)),'f0_50pct_hz':float(np.percentile(f,50)),'f0_90pct_hz':float(np.percentile(f,90)),'f0_std_semitones':float(np.std(12*np.log2(f/np.median(f))))})
except Exception as e:metrics['prosody_error']=str(e)
(ROOT/'qa-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(metrics,flush=True)

