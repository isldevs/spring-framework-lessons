#!/usr/bin/env python3
"""Generate an original quiet NumPy ambient score + synchronized lookup cues.
No sampled/third-party music. Measured two-pass EBU R128 normalization.
"""
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import maximum_filter1d,gaussian_filter1d
import json, subprocess,re
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
SR=48000
data=json.loads((ROOT/'source/timing.json').read_text());n=int(round(data['duration']*SR));t=np.arange(n)/SR
sr,raw=wavfile.read(ROOT/'narration.wav')
assert sr==SR
speech=raw.astype(np.float64)/np.iinfo(raw.dtype).max
if speech.ndim>1:speech=speech.mean(axis=1)
speech=np.pad(speech,(0,max(0,n-len(speech))))[:n]
# Soft harmonic pad: D minor add9, with smooth independent swells and stereo phase.
bed=np.zeros((n,2))
for k,freq in enumerate([146.8324,174.6141,220.0,329.6276]):
    swell=(.62+.38*np.sin(2*np.pi*(.043+k*.007)*t+k)**2)
    for c in range(2):
        bed[:,c]+=.0022*swell*np.sin(2*np.pi*freq*t+(.13*c*(k+1)))*(.7+.3*np.sin(2*np.pi*.13*t+k))
# Duck bed where speech is active; never a hard noise gate.
env=gaussian_filter1d(maximum_filter1d(np.abs(speech),size=2401),sigma=1800)
duck=1-.45*np.clip(env/.1,0,1)
fade=np.minimum(1,t/1.1)*np.minimum(1,(data['duration']-t)/.65)
bed*= (duck*fade)[:,None]
fx=np.zeros((n,2));events=[]
cues=data['scene_cues_absolute'];recap=data['recap_cues_absolute']
# Each subtle ping marks the same narrated reveal used by the animation.
marks=[(cues['load']['injection'],'Spring supplies Repo to the service constructor'),
       (cues['lookup']['return'],'required service reference retrieved'),
       (cues['identity']['pass'],'repository identity assertion holds'),
       (cues['proof']['pass'],'actual JUnit smoke test passes'),
       (recap['complete'],'complete configuration wiring smoke-test overview')]
for i,(start,purpose) in enumerate(marks,1):
    events.append({'time':round(start,6),'purpose':purpose})
    j=int(start*SR);tt=np.arange(int(.20*SR))/SR
    a=.010*np.sin(2*np.pi*(660+110*i)*tt)*np.exp(-tt*28)*(1-np.exp(-tt*180))
    fx[j:j+len(a),:]+=a[:,None]*np.array([[.85,1.]])
for name,a in [('background.wav',bed),('effects.wav',fx),('premix.wav',speech[:,None]*np.ones((1,2))+bed+fx)]:
    wavfile.write(OUT/name,SR,np.int16(np.clip(a,-1,1)*32767))
(OUT/'sound-events.json').write_text(json.dumps(events,indent=2)+'\n')
cmd=['ffmpeg','-hide_banner','-i',str(OUT/'premix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-']
r=subprocess.run(cmd,capture_output=True,text=True,check=True)
m=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0];(OUT/'loudness-first-pass.json').write_text(json.dumps(m,indent=2)+'\n')
filt=f"loudnorm=I=-16:TP=-1.5:LRA=7:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
r=subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(OUT/'premix.wav'),'-af',filt,'-ar','48000','-c:a','pcm_s24le',str(OUT/'mix.wav')],capture_output=True,text=True,check=True)
(OUT/'loudness-second-pass.txt').write_text(r.stderr)
print('Original bed and lookup cues mixed, two-pass loudnorm complete.')
