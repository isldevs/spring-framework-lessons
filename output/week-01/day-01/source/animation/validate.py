#!/usr/bin/env python3
"""Independently inspect the encoded artifact and preserve machine evidence."""
from pathlib import Path
import subprocess,json,re,math,importlib.util
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'source/evidence';V=ROOT/'video.mp4'
def run(cmd,stem,raw=False):
 p=subprocess.run(cmd,capture_output=True,text=not raw)
 if not raw:
  (E/f'final-{stem}.stdout.txt').write_text(p.stdout)
  (E/f'final-{stem}.stderr.txt').write_text(p.stderr)
  (E/f'final-{stem}.command.json').write_text(json.dumps({'command':cmd,'exit_code':p.returncode},indent=2)+'\n')
 if p.returncode:raise RuntimeError((stem,p.returncode,p.stderr))
 return p
p=run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(V)],'ffprobe')
probe=json.loads(p.stdout);(E/'final-ffprobe.json').write_text(json.dumps(probe,indent=2)+'\n')
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['codec_name'],v['width'],v['height'],v['pix_fmt'])==('h264',1080,1920,'yuv420p')
assert v['r_frame_rate']=='60/1' and v['avg_frame_rate']=='60/1'
assert all(v[k]=='bt709' for k in ['color_space','color_transfer','color_primaries'])
assert v['color_range']=='tv' and a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2
D=float(probe['format']['duration']);assert 35<=D<45
run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],'decode')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-af','loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json','-f','null','-'],'audio-loudness')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-af','silencedetect=noise=-50dB:d=0.15','-f','null','-'],'audio-silence')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-vf','blackdetect=d=0.01:pix_th=0.015:pic_th=0.99','-an','-f','null','-'],'black-detect')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-loop','1','-framerate','60','-i',str(ROOT/'cover.png'),'-filter_complex',f'[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[cover];[0:v][cover]ssim=stats_file={E}/final-opening-ssim-frames.txt','-frames:v','60','-an','-f','null','-'],'opening-ssim')
# Confirm PTS increments independently from the encoded stream.
f=run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(V)],'frame-timestamps')
ts=[float(x['best_effort_timestamp_time']) for x in json.loads(f.stdout)['frames']]
assert abs(ts[0])<.001 and all(abs(b-a-1/60)<2e-6 for a,b in zip(ts,ts[1:]))
# Source cover bytes exactly match the first second before lossy encoding.
spec=importlib.util.spec_from_file_location('render',ROOT/'source/animation/render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
data=r.read_timing();cover=np.asarray(Image.open(ROOT/'cover.png'))
assert all(np.array_equal(np.asarray(r.render_frame(n/60,data)),cover) for n in range(60))
# Important content: all bright foreground pixels are constrained to safe bounds.
# Background grid and dark panels are decorative, excluded by brightness threshold.
samples=sorted(set([n/60 for n in range(60)]+[s['start']+(s['end']-s['start'])*j/16 for s in data['scenes'] for j in range(17) if s['start']+(s['end']-s['start'])*j/16<data['duration']]+[(c['start']+c['end'])/2 for c in data['captions']]))
bounds=[]
for t in samples:
 im=np.asarray(r.render_frame(t,data));mask=(im.max(axis=2)>=90);ys,xs=np.where(mask)
 bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())];bounds.append({'time':t,'bright_content_bounds':bb})
 assert bb[0]>=90 and bb[1]>=250 and bb[2]<=990 and bb[3]<=1520,(t,bb)
(E/'final-source-safe-bounds.json').write_text(json.dumps(bounds,indent=2)+'\n')
# Parse actual SRT, compare exact rounded timing data and check non-overlap.
srt=(ROOT/'subtitles.srt').read_text();blocks=srt.strip().split('\n\n');end=0
actual_caption_text=[]
for i,b in enumerate(blocks,1):
 ls=b.splitlines();assert int(ls[0])==i
 def seconds(s):
  h,m,v=s.split(':');z,ms=v.split(',');return int(h)*3600+int(m)*60+int(z)+int(ms)/1000
 st,en=map(seconds,ls[1].split(' --> '));assert end<=st<en<=D;end=en
 assert abs(st-data['captions'][i-1]['start'])<.00051 and abs(en-data['captions'][i-1]['end'])<.00051
 displayed=' '.join(ls[2:]);expected=data['captions'][i-1]['text'].replace('get bean','getBean')
 assert displayed==expected,(displayed,expected)
 actual_caption_text.append(displayed)
assert len(blocks)==len(data['captions'])
def normalized_words(text):
 text=text.lower().replace('get bean','getbean').replace('’',"'").replace("'",'')
 return re.findall(r'[a-z0-9]+',text)
phrases=data.get('phrases',data['captions'])
assert normalized_words(' '.join(actual_caption_text))==normalized_words(' '.join(x['text'] for x in phrases))
assert len(data['scenes'])==7
assert data['scenes'][-2]['scene']==6 and data['scenes'][-1]['scene']==7
assert normalized_words(phrases[-1]['text'])==['thanks','for','watching']
assert normalized_words(actual_caption_text[-1])==['thanks','for','watching']
# The recap hold is scene 6, before the separate Thanks scene, not at EOF.
# Select the final 120 complete frame intervals inside the explicit hold window.
hold_seconds=float(data.get('recap_hold_seconds',0));assert hold_seconds>=2.0
hold_start=float(data['recap_hold_start']);hold_end=float(data['recap_hold_end'])
recap_scene=data['scenes'][-2];thanks_scene=data['scenes'][-1]
assert recap_scene['start']<=hold_start<hold_end<=recap_scene['end']+.000001
assert abs(hold_end-hold_start-hold_seconds)<.000002
assert abs(thanks_scene['start']-hold_end)<.000002
assert abs(float(data['thanks_start'])-thanks_scene['start'])<.000002
assert abs(float(data['thanks_end'])-thanks_scene['end'])<.000002
hold_frames=120
hold_first=math.ceil(hold_start*60-1e-7)
hold_samples=[hold_first/60+j/60 for j in range(hold_frames)]
# Check 120 frame presentations within the source hold. The final displayed
# frame may extend to the next 60 FPS boundary, where the Thanks scene begins.
assert hold_samples[0]>=hold_start-1e-6 and hold_samples[-1]<hold_end+.000001
recap_crop=(100,330,980,1310)
reference=r.render_frame(hold_end-.03,data).crop(recap_crop)
reference_array=np.asarray(reference)
assert all(np.array_equal(np.asarray(r.render_frame(t,data).crop(recap_crop)),reference_array) for t in hold_samples),'Recap diagram changes during the two-second reading hold'
reference.save(E/'final-recap-hold-reference.png')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-loop','1','-framerate','60','-i',str(E/'final-recap-hold-reference.png'),'-filter_complex',f'[0:v]trim=start_frame={hold_first},setpts=PTS-STARTPTS,crop=880:980:100:330[recap];[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[ref];[recap][ref]ssim=stats_file={E}/final-recap-hold-ssim-frames.txt','-frames:v',str(hold_frames),'-an','-f','null','-'],'recap-hold-ssim')
hold_ssims=[float(re.search(r'All:([0-9.]+)',x).group(1)) for x in (E/'final-recap-hold-ssim-frames.txt').read_text().splitlines()]
assert len(hold_ssims)==hold_frames and min(hold_ssims)>.995,('Encoded recap differs from its complete reading hold',min(hold_ssims))
# Verify the end of the encoded movie shows the Thanks scene rather than
# prematurely stopping at the recap. Exclude optional captions/progress rail.
thanks_frame=int(v['nb_read_frames'])-1
thanks_t=thanks_frame/60
assert thanks_t>=thanks_scene['start']
thanks_reference=r.render_frame(thanks_t,data).crop(recap_crop)
thanks_reference.save(E/'final-thanks-reference.png')
run(['ffmpeg','-hide_banner','-nostats','-i',str(V),'-loop','1','-framerate','60','-i',str(E/'final-thanks-reference.png'),'-filter_complex',f'[0:v]trim=start_frame={thanks_frame},setpts=PTS-STARTPTS,crop=880:980:100:330[ending];[1:v]scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p[ref];[ending][ref]ssim=stats_file={E}/final-thanks-ssim-frames.txt','-frames:v','1','-an','-f','null','-'],'thanks-ssim')
thanks_ssim=float(re.search(r'All:([0-9.]+)',(E/'final-thanks-ssim-frames.txt').read_text()).group(1))
assert thanks_ssim>.995,('Encoded closing does not match Thanks source',thanks_ssim)
# Sample actual decoded frames at all scene late points, not source previews.
thumbs=[]
for i,s in enumerate(data['scenes']):
 t=s['start']+.8*(s['end']-s['start']);dest=E/f'final-decoded-scene-{i+1}.png'
 run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(V),'-frames:v','1',str(dest)],f'decoded-scene-{i+1}')
 thumbs.append(Image.open(dest).resize((360,640),Image.Resampling.LANCZOS))
contact=Image.new('RGB',(1080,math.ceil(len(thumbs)/3)*640),'#080f20')
for i,im in enumerate(thumbs):contact.paste(im,(i%3*360,i//3*640))
contact.save(E/'final-decoded-mobile-contact.png')
summary={'duration':D,'video_duration':float(v['duration']),'audio_duration':float(a['duration']),'frames':int(v['nb_read_frames']),'timestamps_checked':len(ts),'fps':v['r_frame_rate'],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'pixel_format':v['pix_fmt'],'color_space':v['color_space'],'color_transfer':v['color_transfer'],'color_primaries':v['color_primaries'],'audio_sample_rate':a['sample_rate'],'audio_channels':a['channels'],'srt_cues':len(blocks),'source_safe_bounds_samples':len(samples),'source_first_second_exact_cover':True,'caption_words_match_script':True,'approved_scenes_count':len(data['scenes'])}
loud=(E/'final-audio-loudness.stderr.txt').read_text();metrics=json.JSONDecoder().raw_decode(loud[loud.rfind('{'):])[0]
ssimlog=(E/'final-opening-ssim.stderr.txt').read_text();ssims=[float(re.search(r'All:([0-9.]+)',x).group(1)) for x in (E/'final-opening-ssim-frames.txt').read_text().splitlines()]
summary.update({'integrated_loudness_lufs':float(metrics['input_i']),'true_peak_dbtp':float(metrics['input_tp']),'loudness_range_lu':float(metrics['input_lra']),'first_second_ssim_average':float(re.search(r'All:([0-9.]+)',ssimlog).group(1)),'first_second_ssim_minimum':min(ssims),'first_second_compared_frames':len(ssims),'decode_error_log_empty':not (E/'final-decode.stderr.txt').read_text().strip(),'black_intervals_detected':len(re.findall(r'black_start:',(E/'final-black-detect.stderr.txt').read_text())),'silence_intervals':re.findall(r'silence_start: ([0-9.]+)',(E/'final-audio-silence.stderr.txt').read_text())})
assert summary['decode_error_log_empty'] and summary['black_intervals_detected']==0
assert summary['first_second_ssim_minimum']>.995
assert summary['true_peak_dbtp']<0 and -18<summary['integrated_loudness_lufs']<-14
silence_log=(E/'final-audio-silence.stderr.txt').read_text()
silence_pairs=re.findall(r'silence_start: ([0-9.]+).*?silence_end: ([0-9.]+)',silence_log,re.S)
closing_quiet_after=max(thanks_scene['start'],float(phrases[-1]['end'])-.5)
for st,en in silence_pairs:
 st=float(st);en=float(en)
 assert (hold_start-.05<=st<en<=hold_end+.05) or st>=closing_quiet_after,('Unexpected internal silence outside recap hold or closing tail',st,en)
summary.update({'recap_hold_start':hold_start,'recap_hold_end':hold_end,'recap_hold_seconds':hold_seconds,'recap_hold_is_before_thanks':True,'recap_hold_source_samples':len(hold_samples),'recap_hold_crop':list(recap_crop),'recap_hold_source_pixel_identical':True,'recap_hold_decoded_frames':len(hold_ssims),'recap_hold_ssim_minimum':min(hold_ssims),'recap_hold_ssim_average':sum(hold_ssims)/len(hold_ssims),'thanks_start':thanks_scene['start'],'thanks_end':thanks_scene['end'],'thanks_frame_checked':thanks_frame,'thanks_final_frame_ssim':thanks_ssim,'thanks_caption_and_script_match':True,'intentional_recap_hold_or_closing_quiet_allowed':True})
(E/'final-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
