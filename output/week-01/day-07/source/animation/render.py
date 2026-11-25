#!/usr/bin/env python3
"""Original Pillow animation: Spring JUnit context smoke testing and reference identity.

Frames are rendered at native1080x1920/60FPS using final Kokoro/ASR edit timing.
JUnit and its test instance remain outside the managed application context.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, json, math, subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'source/assets'
W,H,FPS=1080,1920,60
NAVY='#080f20';WHITE='#f5f7ff';MUTED='#9daec9';CYAN='#5cddfa';PURPLE='#b397ff';GREEN='#94e568';RED='#ff7d91';CARD='#111e34';EDGE='#2a3c58'
FONTS={};TEXT_BOUNDS=[]
def font(size,bold=False,mono=False):
    key=(size,bold,mono)
    if key not in FONTS:FONTS[key]=ImageFont.truetype(str(ASSETS/('DejaVuSansMono.ttf' if mono else 'OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')),size)
    return FONTS[key]
def txt(im,s,x,y,size=44,color=WHITE,bold=False,mono=False,center=False):
    d=ImageDraw.Draw(im);f=font(size,bold,mono)
    if center:x-=d.textlength(s,font=f)/2
    x,y=round(x),round(y);bounds=d.textbbox((x,y),s,font=f)
    TEXT_BOUNDS.append({'text':s,'bbox':bounds,'size':size})
    d.text((x,y),s,font=f,fill=color)
def lines(im,ls,x,y,size=44,color=WHITE,bold=False,mono=False,gap=1.3,center=False):
    for i,s in enumerate(ls):txt(im,s,x,y+i*size*gap,size,color,bold,mono,center)
def box(im,xy,fill=CARD,outline=EDGE,r=22,width=2):ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,xy)),r,fill,outline,width)
def line(im,pts,color=CYAN,width=4):ImageDraw.Draw(im).line(pts,fill=color,width=width,joint='curve')
def ease(v):v=max(0,min(1,v));return v*v*(3-2*v)
def reveal(t,start,duration=.22):return ease((t-start)/duration)
def arrow(im,a,b,p=1,color=CYAN,width=5):
    p=max(0,min(1,p));e=(a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p)
    line(im,[a,e],color,width)
    if p>.01:
        angle=math.atan2(b[1]-a[1],b[0]-a[0]);n=13
        line(im,[(e[0]-n*math.cos(angle-.55),e[1]-n*math.sin(angle-.55)),e,(e[0]-n*math.cos(angle+.55),e[1]-n*math.sin(angle+.55))],color,width)
def check(im,x,y,color=GREEN):line(im,[(x-12,y),(x-3,y+12),(x+15,y-14)],color,5)
def cross(im,x,y,color=RED):
    line(im,[(x-12,y-12),(x+12,y+12)],color,5);line(im,[(x-12,y+12),(x+12,y-12)],color,5)
def tag(im,s,x,y,color=GREEN,size=26):
    tw=ImageDraw.Draw(im).textlength(s,font=font(size,True))
    box(im,(x,y,x+tw+30,y+size+24),fill='#15283a',outline=color,r=10,width=1);txt(im,s,x+15,y+8,size,color,True)
def make_bg():
    yy,xx=np.mgrid[0:H,0:W];glow=np.exp(-(((xx-850)/750)**2+((yy-760)/1050)**2));arr=np.zeros((H,W,3),dtype=np.uint8)
    for k,(a,b) in enumerate(zip((8,15,32),(5,10,17))):arr[:,:,k]=a+b*glow
    im=Image.fromarray(arr);d=ImageDraw.Draw(im)
    for x in range(90,1000,90):d.line((x,250,x,1520),fill='#142136',width=1)
    for y in range(270,1520,90):d.line((90,y,990,y),fill='#142136',width=1)
    return im
BG=make_bg()
def base(k,label,title):
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    txt(im,'JAVA / SPRING',980-ImageDraw.Draw(im).textlength('JAVA / SPRING',font=font(24)),270,24,MUTED)
    tag(im,label,100,350,GREEN,25);lines(im,title,100,425,62,WHITE,True,gap=1.13)
    return im

def context(im,xy=(120,810,960,1288),ready=True):
    box(im,xy,fill='#0d1d2d',outline=PURPLE,r=23,width=2)
    x,y,x2,y2=xy
    txt(im,'ApplicationContext',x+23,y+15,36,PURPLE,True)
    txt(im,'MANAGED DEMO BEANS',x+23,y+65,25,MUTED,True)
    if ready:tag(im,'READY',x2-142,y+17,GREEN,23)

def bean(im,name,x,y,w=330,h=135,sub=None,color=GREEN):
    box(im,(x,y,x+w,y+h),fill='#183a31',outline=color,r=18,width=3)
    txt(im,name,x+w/2,y+15,40,color,True,center=True)
    if sub:txt(im,sub,x+w/2,y+h-39,27,WHITE,center=True)

def graph(im,y=940,ready=True,field=True):
    context(im,(120,y-130,960,y+315),ready)
    bean(im,'OrderService',145,y,390,145,'service bean')
    bean(im,'Repo',610,y,325,145,'repo bean')
    if field:
        arrow(im,(540,y+95),(603,y+95),1,PURPLE,5)
        txt(im,'repository()',145,y+162,29,PURPLE,mono=True)

def query(im,text,y=625,label='TEST METHOD',size=38):
    box(im,(120,y,960,y+123),fill=CARD,outline=CYAN,r=18)
    txt(im,label,144,y+10,25,CYAN,True)
    txt(im,text,144,y+58,size,WHITE,mono=True)

def recipe(im,name,x,y,w=320,h=130):
    d=ImageDraw.Draw(im);fold=24
    d.polygon([(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)],fill='#171d36',outline=PURPLE,width=2)
    line(im,[(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)],PURPLE,2)
    txt(im,'@Bean',x+18,y+12,34,PURPLE,mono=True)
    txt(im,name,x+18,y+65,36,WHITE,mono=True)

def hook_scene(t,with_motion=True):
    im=base(0,'CONTEXT SMOKE TEST',['Context loaded.','Wiring checked?'])
    graph(im,818,True,True)
    # The graph exists; its expected identity is a pending test assertion.
    box(im,(120,1188,960,1308),fill=CARD,outline=CYAN,r=18)
    txt(im,'EXPECTED REPOSITORY?',145,1202,27,CYAN,True)
    txt(im,'assertSame',145,1244,38,WHITE,mono=True)
    txt(im,'?',895,1224,54,CYAN,True)
    if with_motion:
        p=(t/.8)%1;x=545+53*p
        ImageDraw.Draw(im).ellipse((x-7,906,x+7,920),fill=CYAN)
        line(im,[(145+700*p,1294),(min(930,181+700*p),1294)],CYAN,4)
    return im

def cover():return hook_scene(0,False)
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or [1.7,8,4.2,7,6.2,9,1.4][k]
    t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:return hook_scene(t)
    if k==1:
        load=at('configuration',1);repo=at('repo',3.2);injection=at('injection',5.8);ready=at('ready',6.5)
        im=base(k,'SPRING TEST SETUP',['Spring loads Config.','Then it supplies Repo.'])
        query(im,'@SpringJUnitConfig(Config.class)',label='JUNIT · SPRING TEST SUPPORT',size=38)
        if t>=load:arrow(im,(935,753),(935,822),reveal(t,load,.28),CYAN,5)
        context(im,(120,835,960,1308),t>=ready)
        recipe(im,'Repo repo()',145,950)
        recipe(im,'service(Repo)',145,1133)
        if t>=repo:
            arrow(im,(470,1010),(603,1010),reveal(t,repo,.24),CYAN,4)
            bean(im,'Repo',610,950,325,130,'repo bean')
        if t>=injection:
            arrow(im,(772,1085),(772,1128),reveal(t,injection,.24),GREEN,5)
            txt(im,'constructor',500,1085,27,GREEN,True)
            arrow(im,(470,1195),(603,1195),reveal(t,injection,.24),CYAN,4)
            bean(im,'OrderService',610,1133,325,130,'service bean')
        return im
    if k==2:
        request=at('request',.1);returned=at('return',.6)
        im=base(k,'REQUIRED BEAN LOOKUP',['Retrieve the required','service bean.'])
        query(im,'ctx.getBean(OrderService.class)',label='@Test · REQUIRED LOOKUP',size=38)
        graph(im,945,True,True)
        if t>=request:
            line(im,[(570,752),(570,1005)],CYAN,4)
            arrow(im,(570,1005),(541,1005),reveal(t,request,.25),CYAN,4)
        if t>=returned:
            box(im,(140,940,540,1095),fill=None,outline=CYAN,r=20,width=3)
            line(im,[(140,985),(105,985),(105,758)],GREEN,4)
            arrow(im,(105,758),(141,758),reveal(t,returned,.25),GREEN,4)
            txt(im,'same service instance',145,762,28,GREEN,True)
            tag(im,'REQUIRED BEAN FOUND',145,1193,GREEN,27)
        return im
    if k==3:
        repository=at('repository',1.2);actual=at('actual',.3);expected=at('expected',repository);assertion=at('assertion',3);passed=at('pass',4)
        im=base(k,'REFERENCE IDENTITY',['Check the exact','repository instance.'])
        query(im,'Repo repo = ctx.getBean(Repo.class);',label='@Test · WIRING ASSERTION',size=36)
        context(im,(120,810,960,1127),True)
        bean(im,'OrderService',145,940,390,140,'repository()')
        bean(im,'Repo',610,940,325,140,'repo bean')
        if t>=actual:
            arrow(im,(540,1020),(603,1020),reveal(t,actual,.25),PURPLE,5)
            txt(im,'service reference',145,1088,27,PURPLE,True)
        if t>=expected:
            arrow(im,(773,752),(773,932),reveal(t,expected,.25),CYAN,5)
            txt(im,'context ref',610,891,26,CYAN,True)
        box(im,(120,1157,960,1308),fill=CARD,outline=GREEN if t>=passed else EDGE,r=18)
        txt(im,'OBJECT IDENTITY',145,1164,24,GREEN if t>=passed else MUTED,True)
        txt(im,'assertSame(repo,',145,1200,36,WHITE if t>=assertion else MUTED,mono=True)
        txt(im,'  service.repository());',145,1248,36,WHITE if t>=assertion else MUTED,mono=True)
        if t>=passed:
            box(im,(604,934,941,1086),fill=None,outline=CYAN,r=20,width=3)
            check(im,908,1207)
        return im
    if k==4:
        result=at('result',.5);bean_cue=at('bean',2);wiring=at('wiring',3.6);passed=at('pass',4)
        im=base(k,'ACTUAL JUNIT RESULT',['One smoke test.','Specific guarantees.'])
        box(im,(120,625,960,1308),fill=CARD,outline=GREEN if t>=passed else PURPLE,r=22,width=2)
        txt(im,'JUNIT · SPRING CONTEXT TEST',145,649,28,PURPLE,True)
        txt(im,'contextLoadsAndWires()',145,714,38,WHITE,mono=True)
        if t>=result:
            check(im,169,837);txt(im,'Context loaded',204,814,42,GREEN,True)
        if t>=bean_cue:
            check(im,169,938);txt(im,'Required bean found',204,915,42,GREEN,True)
        if t>=wiring:
            check(im,169,1039);txt(im,'Expected Repo instance',204,1016,42,GREEN,True)
        if t>=passed:
            tag(im,'1 / 1 PASS',720,781,GREEN,27)
            txt(im,'ACTUAL TEST STDOUT',145,1132,25,MUTED,True)
            txt(im,'bean found: true',145,1177,37,GREEN,mono=True)
            txt(im,'wiring same: true',145,1235,37,GREEN,mono=True)
        return im
    if k==5:return recap_scene(u,t,recap,duration,cues)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',6.8))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};pc=proof_cues or {};duration=scene_duration or 9;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(pc.get(key,cues.get(key,default)))
    behavior=at('behavior',1.5);load=at('load',3.8);lookup=at('lookup',4.4);assertion=at('assert',5.1);complete=at('complete',duration-2)
    im=base(5,'CONFIGURATION + WIRING',['Quick wiring check.','Behavior needs tests.'])
    box(im,(120,625,960,757),fill=CARD,outline=PURPLE,r=18)
    txt(im,'JUnit / Spring',145,666,37,PURPLE,True)
    txt(im,'Config.class',627,666,37,PURPLE,True,mono=True)
    if t>=load:
        arrow(im,(443,693),(602,693),reveal(t,load,.24),CYAN,5)
        arrow(im,(848,763),(848,805),1,CYAN,4)
    context(im,(120,810,960,1116),True)
    bean(im,'OrderService',145,945,390,140,'service bean')
    bean(im,'Repo',610,945,325,140,'repo bean')
    arrow(im,(540,1030),(603,1030),1,PURPLE,5)
    if t>=lookup:
        txt(im,'getBean',145,905,30,CYAN,True,mono=True)
        arrow(im,(330,932),(330,943),1,CYAN,4)
    box(im,(120,1156,960,1308),fill='#112532',outline=GREEN if t>=assertion else EDGE,r=18)
    txt(im,'assertSame',145,1179,40,GREEN if t>=assertion else MUTED,mono=True)
    if t>=assertion:txt(im,'1 / 1 test passed',555,1182,36,GREEN,True)
    if t>=behavior:txt(im,'Order behavior: separate tests',145,1256,30,MUTED)
    if t>=complete:check(im,910,1208)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.4;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im

def mechanism_anchors(data):
    c=data.get('scene_cues_absolute',{});s=data['scenes'];l=c.get('load',{});q=c.get('lookup',{});i=c.get('identity',{});p=c.get('proof',{})
    return {'config_load_s':float(l.get('configuration',s[1]['start']+1)),
            'repo_created_s':float(l.get('repo',s[1]['start']+3.2)),
            'service_wired_s':float(l.get('injection',s[1]['start']+5.8)),
            'context_ready_s':float(l.get('ready',s[1]['start']+6.5)),
            'required_lookup_s':float(q.get('request',s[2]['start']+.1)),
            'required_found_s':float(q.get('return',s[2]['start']+.6)),
            'expected_repo_lookup_s':float(i.get('repository',s[3]['start']+1.2)),
            'identity_assert_s':float(i.get('assertion',s[3]['start']+3)),
            'identity_pass_s':float(i.get('pass',s[3]['start']+4)),
            'test_pass_s':float(p.get('pass',s[4]['start']+4)),
            'recap_complete_s':float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))}
def graph_ready_at(data):return mechanism_anchors(data)['context_ready_s']
def application_use_start(data):return mechanism_anchors(data)['required_lookup_s']
def read_timing():return json.loads((ROOT/'source/timing.json').read_text())
def caption(im,text):
    size=43;d=ImageDraw.Draw(im);out=[];row=''
    for word in text.split():
        v=(row+' '+word).strip()
        if d.textlength(v,font=font(size,True))>830 and row:out.append(row);row=word
        else:row=v
    if row:out.append(row)
    if len(out)>2:raise ValueError(('Caption exceeds two lines',text,out))
    box(im,(100,1322,980,1487),fill='#0a1326',outline=None,r=17)
    lines(im,out,540,1340+(2-len(out))*27,size,WHITE,True,gap=1.22,center=True)
def render_frame(t,data,with_caption=True):
    ss=data['scenes'];k=next((i for i,s in enumerate(ss) if s['start']<=t<s['end']),len(ss)-1);s=ss[k];duration=s['end']-s['start'];u=(t-s['start'])/duration
    key={1:'load',2:'lookup',3:'identity',4:'proof',5:'recap'}.get(k)
    cues={name:float(val)-s['start'] for name,val in data.get('scene_cues_absolute',{}).get(key,{}).items() if isinstance(val,(int,float))}
    if k==5:cues['complete']=float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))-s['start']
    im=scene(k,u,t-s['start'],data.get('recap_cues'),duration,cues)
    if with_caption and k!=6:
        c=next((c for c in data['captions'] if c['start']<=t<c['end']),None)
        if c:caption(im,c['text'])
    ImageDraw.Draw(im).line((100,1510,100+880*min(1,t/data['duration']),1510),fill=GREEN,width=3)
    return im
def srt_time(s):
    ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def write_srt(data):
    out=''
    for i,c in enumerate(data['captions'],1):out+=f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n\n"
    (ROOT/'subtitles.srt').write_text(out)
def preflight(data):
    TEXT_BOUNDS.clear();states=[]
    for s in data['scenes']:
        states.extend(np.linspace(s['start'],s['end']-1/FPS,31))
    for t in states:render_frame(float(t),data)
    cover();bad=[r for r in TEXT_BOUNDS if r['bbox'][0]<90 or r['bbox'][1]<250 or r['bbox'][2]>990 or r['bbox'][3]>1520]
    result={'samples':len(states),'unique_text_bounds':len({(r['text'],tuple(r['bbox'])) for r in TEXT_BOUNDS}),'safe_area':[90,250,990,1520],'violations':bad,'passed':not bad}
    out=ROOT/'source/evidence';out.mkdir(exist_ok=True);(out/'renderer-preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    if bad:raise ValueError(('Unsafe text bounds',bad[:8]))
    return result
def main():
    p=argparse.ArgumentParser();p.add_argument('--previews',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--preflight',action='store_true');a=p.parse_args()
    COVER.save(ROOT/'cover.png');data=read_timing();write_srt(data)
    if a.preflight:print(json.dumps(preflight(data),indent=2))
    if a.previews:
        out=ROOT/'source/evidence';out.mkdir(exist_ok=True);samples=[0]+[s['start']+(s['end']-s['start'])*.92 for s in data['scenes']];thumbs=[]
        for j,t in enumerate(samples):
            im=render_frame(t,data);im.save(out/f'preview-{j}.png');thumbs.append(im.resize((324,576),Image.Resampling.LANCZOS))
        contact=Image.new('RGB',(1296,1152),NAVY)
        for j,im in enumerate(thumbs):contact.paste(im,(j%4*324,j//4*576))
        contact.save(out/'mobile-contact-sheet.png')
        s=data['scenes'][-2];t=(data['recap_hold_start']+data['recap_hold_end'])/2;c={name:float(v)-s['start'] for name,v in data.get('scene_cues_absolute',{}).get('recap',{}).items() if isinstance(v,(int,float))};c['complete']=float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))-s['start']
        scene(5,1,t-s['start'],data.get('recap_cues'),s['end']-s['start'],c).save(ROOT/'recap.png')
        s=data['scenes'][-1];thanks_scene(1,s['end']-s['start'],s['end']-s['start']).save(ROOT/'thanks.png')
    if a.render:
        count=math.ceil(data['duration']*FPS)
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(ROOT/'source/animation/mix.wav'),'-map','0:v','-map','1:a','-vf','scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(count/FPS),'-movflags','+faststart',str(ROOT/'video.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for n in range(count):
            proc.stdin.write(render_frame(n/FPS,data).tobytes())
            if n%300==0:print(f'frame {n}/{count}',flush=True)
        proc.stdin.close()
        if proc.wait():raise RuntimeError('FFmpeg failed')
        print('Render complete',flush=True)
if __name__=='__main__':main()
