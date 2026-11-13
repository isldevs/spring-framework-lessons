#!/usr/bin/env python3
"""Original Pillow/NumPy motion design. Full resolution frames piped to FFmpeg.
Run from any directory: python source/animation/render.py [--previews|--render].
Timing is from actual locally synthesized Kokoro speech, not estimated duration.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, math, subprocess, argparse, wave
ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'source/assets'
W,H,FPS=1080,1920,60
NAVY='#080f20'; WHITE='#f5f7ff'; MUTED='#9daec9'; CYAN='#5cddfa'; PURPLE='#b397ff'; GREEN='#94e568'; CARD='#111e34'; EDGE='#2a3c58'
FONTS={}
def font(size,bold=False,mono=False):
    k=(size,bold,mono)
    if k not in FONTS: FONTS[k]=ImageFont.truetype(str(ASSETS/('DejaVuSansMono.ttf' if mono else 'OpenSans-Bold.ttf' if bold else 'OpenSans-Regular.ttf')),size)
    return FONTS[k]
def txt(im,s,x,y,size=44,color=WHITE,bold=False,mono=False,center=False):
    d=ImageDraw.Draw(im); f=font(size,bold,mono)
    if center: x-=d.textlength(s,font=f)/2
    d.text((round(x),round(y)),s,font=f,fill=color,stroke_width=0)
def lines(im,ls,x,y,size=44,color=WHITE,bold=False,mono=False,gap=1.3,center=False):
    for i,s in enumerate(ls): txt(im,s,x,y+i*size*gap,size,color,bold,mono,center)
def box(im,xy,fill=CARD,outline=EDGE,r=22,width=2): ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,xy)),r,fill,outline,width)
def line(im,pts,color=CYAN,width=4): ImageDraw.Draw(im).line(pts,fill=color,width=width,joint='curve')
def arrow(im,a,b,p=1,color=CYAN,width=5):
    p=max(0,min(1,p)); e=(a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p)
    line(im,[a,e],color,width)
    if p>.01:
        ang=math.atan2(b[1]-a[1],b[0]-a[0]); n=14
        line(im,[(e[0]-n*math.cos(ang-.55),e[1]-n*math.sin(ang-.55)),e,(e[0]-n*math.cos(ang+.55),e[1]-n*math.sin(ang+.55))],color,width)
def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)
def reveal(u,start,duration=.16):return ease((u-start)/duration)
def node(im,name,x,y,w=270,h=125,color=CYAN,sub=None):
    box(im,(x,y,x+w,y+h),CARD,color,22,3)
    txt(im,name,x+w/2,y+15,44,color,True,center=True)
    if sub:txt(im,sub,x+w/2,y+76,26,MUTED,center=True)
def tag(im,s,x,y,color=GREEN,size=29):
    f=font(size,True);tw=ImageDraw.Draw(im).textlength(s,font=f)
    box(im,(x,y,x+tw+34,y+size+24),fill='#15283a',outline=color,r=10,width=1);txt(im,s,x+17,y+8,size,color,True)
def make_bg():
    yy,xx=np.mgrid[0:H,0:W]; glow=np.exp(-(((xx-880)/750)**2+((yy-780)/1050)**2))
    arr=np.zeros((H,W,3),dtype=np.uint8)
    for k,(base,inc) in enumerate(zip((8,15,32),(5,10,17))):arr[:,:,k]=base+inc*glow
    im=Image.fromarray(arr);d=ImageDraw.Draw(im)
    for x in range(0,W,90): d.line((x,230,x,1540),fill='#142136',width=1)
    for y in range(270,1540,90):d.line((70,y,1010,y),fill='#142136',width=1)
    return im
BG=make_bg()
def base(k,label,title,subtitle=None):
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True);txt(im,'JAVA / SPRING',980,270,24,MUTED,center=False)
    # right aligned topic marker within the safe area
    d=ImageDraw.Draw(im);d.rectangle((880,255,1080,320),fill=NAVY)
    txt(im,'JAVA / SPRING',980-ImageDraw.Draw(im).textlength('JAVA / SPRING',font=font(24)),270,24,MUTED)
    tag(im,label,100,350,GREEN,25)
    lines(im,title if isinstance(title,list) else [title],100,425,62,WHITE,True,gap=1.13)
    if subtitle:txt(im,subtitle,100,574,32,MUTED)
    return im

def cover():
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    tag(im,'JAVA / SPRING',100,367,GREEN,27)
    txt(im,'Spring IoC',100,466,102,WHITE,True)
    lines(im,['Who creates your','Java objects?'],100,627,66,WHITE,True,gap=1.2)
    # Two explicit owners and an object graph: cover introduces the mechanism.
    tag(im,'YOUR CODE',120,907,CYAN,28);tag(im,'SPRING',686,907,GREEN,28)
    arrow(im,(360,940),(658,940),1,PURPLE,5)
    txt(im,'creation + wiring',540,1004,33,MUTED,center=True)
    node(im,'Repo',150,1120,290,125,CYAN,'dependency')
    node(im,'Service',640,1120,290,125,GREEN,'uses Repo')
    arrow(im,(440,1182),(625,1182),1,PURPLE)
    return im
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None):
    if k==0:
        im=COVER.copy()
        # The first second is EXACTLY cover.png; a traveling reference follows.
        if u>0.5:
            x=440+185*ease((u-.5)/.45)
            ImageDraw.Draw(im).ellipse((x-9,1173,x+9,1191),fill=WHITE)
        return im
    if k==1:
        im=base(k,'MANUAL CONSTRUCTION',['Your code is','the object factory.'])
        txt(im,'Application code',130,626,31,CYAN,True)
        box(im,(120,683,960,861))
        txt(im,'var repo = new Repo();',150,706,39,WHITE,mono=True)
        if u>.23:txt(im,'var svc = new Service(repo);',150,779,39,WHITE,mono=True)
        if u>.12:node(im,'Repo',155,950,280,136,CYAN,'created first')
        if u>.48:node(im,'Service',640,950,280,136,GREEN,'receives Repo')
        if u>.52:
            arrow(im,(435,1018),(622,1018),reveal(u,.52,.2),PURPLE)
            txt(im,'passes repo',540,1138,37,PURPLE,center=True)
        return im
    if k==2:
        im=base(k,'SPRING CONTAINER',['Definitions become','managed objects.'])
        tag(im,'@Configuration',120,613,PURPLE,28)
        box(im,(120,690,960,858))
        txt(im,'@Bean Repo repo()',150,714,40,CYAN,mono=True)
        if u>.15:txt(im,'@Bean Service service(Repo repo)',150,788,39,GREEN,mono=True)
        if u>.30:
            arrow(im,(540,874),(540,965),reveal(u,.3,.18),PURPLE)
            txt(im,'create + wire',572,894,29,MUTED)
        box(im,(120,988,960,1258),fill='#112532',outline=GREEN,r=28,width=2)
        txt(im,'SPRING CONTAINER',150,1007,27,GREEN,True)
        if u>.45:node(im,'Repo',160,1080,260,132,CYAN,'bean')
        if u>.65:node(im,'Service',660,1080,260,132,GREEN,'bean')
        if u>.66:arrow(im,(420,1146),(640,1146),reveal(u,.66,.2),PURPLE)
        return im
    if k==3:
        im=base(k,'DEPENDENCY INJECTION',['Spring resolves','the parameter.'])
        box(im,(120,633,960,912))
        txt(im,'@Bean',150,658,40,PURPLE,mono=True)
        txt(im,'Service service(Repo repo) {',150,718,40,WHITE,mono=True)
        txt(im,'  return new Service(repo);',150,778,40,WHITE,mono=True)
        txt(im,'}',150,838,40,WHITE,mono=True)
        box(im,(120,971,960,1257),fill='#112532',outline=GREEN,r=28,width=2)
        txt(im,'INSIDE THE CONTAINER',150,990,26,GREEN,True)
        node(im,'Repo',155,1061,260,132,CYAN,'existing bean')
        if u>.28:node(im,'Service',660,1061,260,132,GREEN,'constructor')
        if u>.20:
            arrow(im,(415,1127),(640,1127),reveal(u,.2,.55),PURPLE)
            p=reveal(u,.2,.55);x=415+225*p
            ImageDraw.Draw(im).ellipse((x-10,1117,x+10,1137),fill=WHITE)
            txt(im,'repo reference',540,1204,29,PURPLE,center=True)
        return im
    if k==4:
        im=base(k,'REQUEST A BEAN',['Ask for the','ready service.'])
        box(im,(120,610,960,700))
        txt(im,'ctx.getBean(Service.class)',150,629,40,WHITE,mono=True)
        node(im,'App',130,812,240,140,CYAN,'caller')
        box(im,(574,754,960,1055),fill='#112532',outline=GREEN,r=24,width=2)
        txt(im,'CONTAINER',596,777,31,GREEN,True)
        node(im,'Service',624,898,285,120,GREEN)
        txt(im,'Repo',775,841,30,CYAN,True,center=True)
        arrow(im,(775,878),(775,892),1,PURPLE,3)
        if u>.05:
            arrow(im,(376,841),(604,841),reveal(u,.05,.18),CYAN)
            txt(im,'request',486,790,27,CYAN,center=True)
        if u>.28:
            arrow(im,(602,983),(250,983),reveal(u,.28,.2),GREEN)
            txt(im,'service reference',425,1022,27,GREEN,center=True)
        if u>.54:
            box(im,(120,1115,960,1270),fill='#112532',outline=GREEN,r=18)
            txt(im,'ACTUAL JAVA RUN · EXCERPT',148,1130,24,MUTED,True)
            txt(im,'spring wiring: true',148,1170,40,GREEN,mono=True)
            txt(im,'Same Repo instance',148,1225,28,WHITE)
        return im
    if k==5:
        return recap_scene(u,elapsed,recap,scene_duration)
    raise ValueError(k)

def recap_complete_at(cues):
    """Scene-relative time when the final diagram is fully assembled and static."""
    ready=float(cues.get('ready',8.0));request=float(cues.get('request',7.1))
    returned=max(ready,request+.60)+.70
    return max(returned,float(cues.get('qualifier',cues.get('takeaway',9.3)))+.05)

def recap_scene(u,elapsed=None,cues=None,scene_duration=None):
    """One progressive overview: definitions, creation/wiring, then lookup.

    The application arrows only appear after the managed object graph exists.
    No creation animation follows getBean. All diagram elements stop moving
    before the reserved final two-second hold. Caption/progress areas are separate.
    """
    cues=cues or {};duration=scene_duration or 15.117167
    t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(cues.get(key,default))
    define=at('define',1.4);create=at('create',3.2);wire=at('wire',4.6)
    request=at('request',7.1);ready=at('ready',8.0);takeaway=at('takeaway',9.3)
    qualifier=at('qualifier',takeaway)
    assert define<=create<=wire<=request<=ready<=takeaway
    im=base(5,'THE BIG PICTURE',['The whole flow.'])
    if t>=qualifier:
        txt(im,'Managed beans only',540,544,35,GREEN,True,center=True)
    else:
        txt(im,'Define / Create + wire / Request',540,546,30,MUTED,center=True)

    # A definition is metadata, not an application request for a new instance.
    if t>=define:
        box(im,(170,618,910,738),fill=CARD,outline=PURPLE,r=20,width=2)
        txt(im,'DEFINE',198,630,25,PURPLE,True)
        txt(im,'@Bean definitions',540,672,40,WHITE,mono=True,center=True)
    if t>=create-.45:
        arrow(im,(540,749),(540,808),reveal(t,create-.45,.45),PURPLE,4)
        txt(im,'register',579,758,27,MUTED)
    if t>=create:
        box(im,(135,825,945,1057),fill='#112532',outline=GREEN,r=25,width=2)
        txt(im,'SPRING',165,843,31,GREEN,True)
        # Align the second header to the container's right edge.
        d=ImageDraw.Draw(im)
        tw=d.textlength('CREATES + WIRES',font=font(27,True))
        txt(im,'CREATES + WIRES',912-tw,845,27,GREEN,True)
        node(im,'Repo',175,913,260,100,CYAN)
        node(im,'Service',645,913,260,100,GREEN)
    if t>=wire:
        # Repo is the constructor dependency, and the arrow carries its reference.
        p=reveal(t,wire,min(.70,max(.20,request-wire-.15)))
        arrow(im,(435,963),(625,963),p,PURPLE,5)
        if p<1:
            x=435+190*p
            ImageDraw.Draw(im).ellipse((x-8,955,x+8,971),fill=WHITE)
        txt(im,'repo reference',540,1014,25,PURPLE,center=True)
    if t>=request:
        box(im,(175,1172,905,1285),fill=CARD,outline=CYAN,r=20,width=2)
        txt(im,'APPLICATION',200,1182,25,CYAN,True)
        txt(im,'getBean(Service.class)',540,1218,40,WHITE,mono=True,center=True)
        arrow(im,(540,1171),(540,1061),reveal(t,request,.60),CYAN,5)
        txt(im,'request',389,1093,30,CYAN)
    return_start=max(ready,request+.60)
    if t>=return_start:
        arrow(im,(760,1061),(760,1158),reveal(t,return_start,.70),GREEN,5)
        lines(im,['ready','service'],790,1073,29,GREEN,gap=1.16)
    return im

def read_timing():
    data=json.loads((ROOT/'source/timing.json').read_text())
    return data

def caption(im,text):
    # Captions use a reserved high contrast band, no more than two lines.
    size=43;f=font(size,True);d=ImageDraw.Draw(im)
    words=text.replace('get bean','getBean').split();out=[];row=''
    for word in words:
        if d.textlength((row+' '+word).strip(),font=f)>830 and row:out.append(row);row=word
        else:row=(row+' '+word).strip()
    if row:out.append(row)
    if len(out)>2:raise ValueError(('caption too long',text,out))
    box(im,(100,1322,980,1487),fill='#0a1326',outline=None,r=17)
    y=1340+(2-len(out))*27
    lines(im,out,540,y,size,WHITE,True,gap=1.22,center=True)

def render_frame(t,data,with_caption=True):
    scenes=data['scenes'];k=next((i for i,s in enumerate(scenes) if s['start']<=t<s['end']),len(scenes)-1)
    s=scenes[k];u=(t-s['start'])/(s['end']-s['start'])
    # The initial exact cover is guaranteed even though narration starts at t=0.
    if t<1:return COVER.copy()
    im=scene(k,u,elapsed=t-s['start'],recap=data.get('recap_cues'),scene_duration=s['end']-s['start']) if k==5 else scene(k,u)
    if with_caption:
        c=next((c for c in data['captions'] if c['start']<=t<c['end']),None)
        if c:caption(im,c['text'])
    ImageDraw.Draw(im).line((100,1510,100+880*min(1,t/data['duration']),1510),fill=GREEN,width=3)
    return im

def srt_time(s):
    ms=round(s*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def write_srt(data):
    text=''
    for i,c in enumerate(data['captions'],1):text+=f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text'].replace('get bean','getBean')}\n\n"
    (ROOT/'subtitles.srt').write_text(text)

def main():
    p=argparse.ArgumentParser();p.add_argument('--previews',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args()
    COVER.save(ROOT/'cover.png')
    data=read_timing();write_srt(data)
    if a.previews:
        out=ROOT/'source/evidence';out.mkdir(exist_ok=True)
        samples=[0]+[s['start']+(s['end']-s['start'])*.78 for s in data['scenes']]
        thumbs=[]
        for j,t in enumerate(samples):
            im=render_frame(t,data);im.save(out/f'preview-{j}.png');thumbs.append(im.resize((324,576),Image.Resampling.LANCZOS))
        contact=Image.new('RGB',(324*4,576*2),NAVY)
        for i,im in enumerate(thumbs):contact.paste(im,(i%4*324,i//4*576))
        contact.save(out/'mobile-contact-sheet.png')
        closing=data['scenes'][-1]
        completed_at=data['duration']-min(1.0,data.get('final_hold_seconds',2.0)/2)
        recap=scene(5,1.0,elapsed=completed_at-closing['start'],recap=data.get('recap_cues'),scene_duration=closing['end']-closing['start'])
        recap.save(ROOT/'recap.png')
    if a.render:
        frames=math.ceil(data['duration']*FPS)
        cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(ROOT/'source/animation/mix.wav'),'-map','0:v','-map','1:a','-vf','scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(frames/FPS),'-movflags','+faststart',str(ROOT/'video.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for n in range(frames):
            proc.stdin.write(render_frame(n/FPS,data).tobytes())
            if n%300==0:print(f'frame {n}/{frames}',flush=True)
        proc.stdin.close()
        if proc.wait():raise RuntimeError('ffmpeg failed')
        print('Render complete',flush=True)
if __name__=='__main__':main()
