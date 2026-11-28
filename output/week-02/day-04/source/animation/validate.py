from pathlib import Path
import subprocess,json,hashlib,math,importlib.util
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];E=R/'source/evidence';Q=R/'qa'
def run(cmd,name):
 p=subprocess.run(cmd,capture_output=True);(E/(name+'.stdout.txt')).write_bytes(p.stdout);(E/(name+'.stderr.txt')).write_bytes(p.stderr);(E/(name+'.command.json')).write_text(json.dumps(cmd));assert p.returncode==0,(name,p.stderr[-200:]);return p
spec=importlib.util.spec_from_file_location('render',R/'source/animation/render.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
d=json.loads((R/'source/timing.json').read_text());p=run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(R/'video.mp4')],'ffprobe');probe=json.loads(p.stdout);v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'],v['codec_name'],v['r_frame_rate'])==(1080,1920,'h264','60/1');assert a['codec_name']=='aac' and a['sample_rate']=='48000';assert all(v[x]=='bt709' for x in ['color_space','color_transfer','color_primaries']);duration=float(probe['format']['duration']);assert 35<=duration<45
run(['ffmpeg','-v','error','-i',str(R/'video.mp4'),'-f','null','-'],'decode')
run(['ffmpeg','-hide_banner','-i',str(R/'video.mp4'),'-af','loudnorm=I=-16:TP=-1.5:print_format=json','-f','null','-'],'loudness')
run(['ffmpeg','-hide_banner','-i',str(R/'video.mp4'),'-vf','blackdetect=d=0.05:pix_th=0.02','-an','-f','null','-'],'black');assert 'black_start:' not in (E/'black.stderr.txt').read_text()
run(['ffmpeg','-hide_banner','-i',str(R/'video.mp4'),'-af','silencedetect=noise=-45dB:d=0.6','-vn','-f','null','-'],'silence')
cover=np.asarray(Image.open(R/'cover.png').convert('RGB'));assert np.array_equal(cover,np.asarray(m.render_frame(0,d)))
opening=[]
for t in [0,.5,1,1.25,1.5,1.75,2]:
 path=R/'first-frame.png' if t==0 else Q/f'opening-{t:.1f}s.png'
 run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(R/'video.mp4'),'-frames:v','1',str(path)],'frame-'+str(t))
 im=np.asarray(Image.open(path).convert('RGB'));src=np.asarray(m.render_frame(t,d));mae=float(np.abs(im.astype(float)-src.astype(float)).mean());assert mae<4,(t,mae);opening.append({'time':t,'mean_absolute_rgb_error':mae})
 if t==0:Image.open(path).save(Q/'opening-0.0s.png')
for name,xy,size in [('cover-grid-square',(0,420,1080,1500),(360,360)),('cover-feed-3x4',(0,240,1080,1680),(360,480)),('cover-feed-9x16',(0,0,1080,1920),(270,480))]:Image.open(R/'cover.png').crop(xy).resize(size).save(Q/(name+'.png'))
roi=(100,450,990,915);assert all(np.array_equal(np.asarray(m.render_frame(t,d,False).crop(roi)),np.asarray(m.render_frame(0,d,False).crop(roi))) for t in np.arange(61)/60)
assert not np.array_equal(np.asarray(m.render_frame(0,d)),np.asarray(m.render_frame(1/60,d)))
first=math.ceil(d['recap_hold_start']*60);last=math.ceil(d['recap_hold_end']*60);base=np.asarray(m.render_frame(first/60,d,False))
assert last-first==120 and all(np.array_equal(base,np.asarray(m.render_frame(i/60,d,False))) for i in range(first,last))
for i,s in enumerate(d['scenes']):run(['ffmpeg','-y','-v','error','-ss',str(s['start']+(s['end']-s['start'])*.85),'-i',str(R/'video.mp4'),'-frames:v','1',str(Q/f'encoded-scene-{i}.png')],f'scene-{i}')
frames=int(v['nb_read_frames']);run(['ffmpeg','-y','-v','error','-ss',str((frames-1)/60),'-i',str(R/'video.mp4'),'-frames:v','1',str(Q/'last-frame.png')],'last-frame')
thumbs=[Image.open(Q/f'encoded-scene-{i}.png').resize((270,480)) for i in range(7)];contact=Image.new('RGB',(1080,960),m.NAVY)
for i,im in enumerate(thumbs):contact.paste(im,(i%4*270,i//4*480))
contact.save(Q/'encoded-mobile-preview.png')
fontsha=hashlib.sha256((R/'source/assets/Inter-Variable.ttf').read_bytes()).hexdigest()
(R/'thumbnail-style.json').write_text(json.dumps({'font':'Inter','font_sha256':fontsha,'weight':900,'axes':{'opsz':32,'wght':900},'size':96,'headline':['Why Spring','Fails With','Circular','Dependencies'],'highlight':'Circular','color':'#FFFFFF','highlight_background':'#0866FF','radius':20,'padding':[18,8],'safe_area':[90,250,990,1520]},indent=2))
layouts=[m.caption_layout(c['text']) for c in d['captions']];assert all(3<=len(c['text'].split())<=7 for c in d['captions']);(R/'subtitle-style.json').write_text(json.dumps({'font':'Inter','weight':700,'size':52,'center':[540,1380],'background_alpha':209,'corner_radius':12,'padding':[26,14],'max_width':840,'layouts':layouts},indent=2))
j=json.loads((E/'java-verification-result.json').read_text());assert j['tests_found']==2 and j['tests_failed']==0
for rel,expected in j['source_sha256'].items():assert hashlib.sha256((R/'source/java'/rel).read_bytes()).hexdigest()==expected
l=(E/'loudness.stderr.txt').read_text();loud=json.JSONDecoder().raw_decode(l[l.rfind('{'):])[0]
raw=(R/'video.mp4').read_bytes();assert raw.find(b'moov')<raw.find(b'mdat')
summary={'duration':duration,'frames':frames,'fps':v['r_frame_rate'],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'audio_sample_rate':a['sample_rate'],'color':'Rec.709 SDR','decode_pass':True,'black_intervals':0,'fast_start':True,'opening':opening,'source_cover_frame0_exact':True,'headline_stable_61_samples':True,'motion_begins':1/60,'recap_source_frames_checked':120,'recap_hold_start':d['recap_hold_start'],'recap_hold_end':d['recap_hold_end'],'java_tests':2,'loudness':loud,'sha256':hashlib.sha256(raw).hexdigest(),'listening_acceptance':'INCOMPLETE: unavailable auditory capability','browser_phone_playback':'UNTESTED'}
(E/'final-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
