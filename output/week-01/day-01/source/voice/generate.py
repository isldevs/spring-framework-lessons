"""Local Kokoro adult-male explanatory narration; six coherent scene utterances."""
import argparse,json
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent.parent
CHUNKS=[
(1,'Who creates your Java objects?',0.20),
(2,'Without Spring, your code creates a repository, then passes it into a service.',0.24),
(3,'With Spring, you register bean definitions. The container uses them to create managed objects and wire their dependencies.',0.25),
(4,'Here, the service bean asks for a repository. Spring supplies that bean.',0.24),
(5,'Your application calls get bean to request the ready service. In our Java run, its repository is the same bean from the container.',0.26),
(6,'Here’s the whole flow. Define your beans. Spring creates them and wires their dependencies. Your application requests the ready service. That’s inversion of control—for managed beans, not every Java object.',2.0),
]
def main():
 p=argparse.ArgumentParser();p.add_argument('--speed',type=float,default=1.02);p.add_argument('--voice',default='am_puck80_fenrir20');p.add_argument('--sample',action='store_true');a=p.parse_args()
 sessopt=ort.SessionOptions();sessopt.intra_op_num_threads=3;sessopt.inter_op_num_threads=1
 session=ort.InferenceSession(str(ROOT/'models/kokoro-v1.0.onnx'),sess_options=sessopt,providers=['CPUExecutionProvider'])
 k=Kokoro.from_session(session,str(ROOT/'models/voices-v1.0.bin'))
 style=(.8*k.get_voice_style('am_puck')+.2*k.get_voice_style('am_fenrir')).astype(np.float32) if a.voice=='am_puck80_fenrir20' else a.voice
 (ROOT/'segments').mkdir(exist_ok=True)
 audio=[];t=0.;phrases=[];scenes=[];phoneme_checks=[]
 for idx,(scene,text,pause) in enumerate(CHUNKS):
  if a.sample and idx>1:break
  print('synth',idx,text,flush=True)
  resolved,phonemes,batches=k._prepare(text,style,a.speed,'en-us',False,0.18,0.045)
  assert len(batches)==1, 'Scene must be synthesized as one continuous utterance'
  phoneme_checks.append({'scene':scene,'text':text,'phonemes':phonemes,'inference_batches':len(batches)})
  print('single scene batch; phonemes',len(phonemes),flush=True)
  x,sr,timings=k.create_timed(text,voice=style,speed=a.speed,lang='en-us',sentence_pause=0.18,clause_pause=0.045,continuous=False)
  assert sr==24000
  # Trim only outside quiet padding; keep a 15ms consonant guard.
  nz=np.where(np.abs(x)>0.001)[0]
  if len(nz):x=x[max(0,nz[0]-360):min(len(x),nz[-1]+360)]
  x=resample_poly(x,2,1).astype(np.float32)
  # Quiet endpoint microfades prevent clicks without changing delivery.
  n=min(192,len(x)//4);x[:n]*=np.linspace(0,1,n);x[-n:]*=np.linspace(1,0,n)
  sf.write(ROOT/'segments'/f'{idx+1:02d}.wav',x,48000,subtype='PCM_24')
  dur=len(x)/48000
  phrases.append({'scene':scene,'start':round(t,6),'end':round(t+dur,6),'text':text})
  scenes.append({'scene':scene,'start':round(t,6),'end':round(t+dur+pause,6)})
  audio.extend([x,np.zeros(round(pause*48000),np.float32)]);t+=dur+pause
  print('duration',dur,'total',t,'phoneme timings',len(timings),flush=True)
 word_checks={word:k._prepare(word,style,a.speed,'en-us',False,0.18,0.045)[1] for word in ['bean','being','beans','get bean','get being']}
 (ROOT/'pronunciation-g2p.json').write_text(json.dumps({'word_distinctions':word_checks,'scenes':phoneme_checks},indent=2,ensure_ascii=False)+'\n')
 y=np.concatenate(audio)
 y*=min(0.84/np.max(np.abs(y)),1.6)
 dest=OUT/('sample.wav' if a.sample else 'narration.wav')
 sf.write(dest,y,48000,subtype='PCM_24')
 meta={'sample_rate':48000,'voice':a.voice,'voice_blend':{'am_puck':0.8,'am_fenrir':0.2} if a.voice=='am_puck80_fenrir20' else None,'delivery_target':'Younger to middle adult male; smooth, connected explanation. No pitch shifting. Perceived age and naturalness require listening acceptance.','speed':a.speed,'one_inference_batch_per_scene':True,'final_hold_seconds':2.0,'final_hold_start':round(len(y)/48000-2.0,6),'duration':len(y)/48000,'scenes':scenes,'phrases':phrases,'captions':phrases,'caption_method':'Scene utterance boundaries are exact synthesis edit points. Shorter display captions will use independent ASR word timing.'}
 (ROOT.parent/('sample-timing.json' if a.sample else 'timing.json')).write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(meta,indent=2),flush=True)
if __name__=='__main__':main()
