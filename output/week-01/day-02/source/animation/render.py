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


def code_runs(im,runs,x,y,size=38):
    d=ImageDraw.Draw(im);f=font(size,mono=True)
    for s,color in runs:
        txt(im,s,x,y,size,color,mono=True);x+=d.textlength(s,font=f)

def object_node(im,name,x,y,w=290,h=125,color=CYAN,size=42,sub=None):
    box(im,(x,y,x+w,y+h),fill='#153448' if color==CYAN else '#183a31',outline=color,r=20,width=3)
    txt(im,name,x+w/2,y+14,size,color,True,center=True)
    if sub:txt(im,sub,x+w/2,y+h-39,27,WHITE,center=True)

def definition(im,name,x,y,w,color,annotation=None):
    box(im,(x,y,x+w,y+116),fill=NAVY,outline=color,r=17,width=2)
    if annotation:txt(im,annotation,x+18,y+8,32,PURPLE,mono=True)
    txt(im,name,x+w/2,y+55,40,color,True,center=True)

def cover():
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    tag(im,'JAVA / SPRING',100,360,GREEN,27)
    txt(im,'Spring DI',100,463,108,WHITE,True)
    lines(im,['How does Repo','reach your service?'],100,622,65,WHITE,True,gap=1.2)
    tag(im,'DEPENDENCY INJECTION',100,858,PURPLE,27)
    object_node(im,'Repo',135,1030,280,140,CYAN,48,'dependency')
    object_node(im,'OrderService',590,1030,355,140,GREEN,40,'needs a Repo')
    arrow(im,(415,1100),(570,1100),1,PURPLE,5)
    txt(im,'Spring supplies the reference',540,1220,37,WHITE,center=True)
    return im
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    scene_duration=scene_duration or {0:2.373917,1:5.008875,2:5.587958,3:5.470958,4:6.712250,5:9.055125,6:1.440750}[k]
    elapsed=u*scene_duration if elapsed is None else elapsed
    cues=scene_cues or {}
    if k==0:
        im=COVER.copy()
        if u>.55:
            x=415+155*reveal(u,.55,.4)
            ImageDraw.Draw(im).ellipse((x-9,1091,x+9,1109),fill=WHITE)
        return im
    if k==1:
        im=base(k,'DISCOVER + REGISTER',['Scanning starts','with configuration.'])
        txt(im,'App: register Config.class, then refresh',120,588,32,CYAN)
        box(im,(120,645,960,813),fill=CARD,outline=PURPLE,r=20)
        txt(im,'@Configuration',145,662,36,PURPLE,mono=True)
        txt(im,'@ComponentScan("lesson.di")',145,720,38,WHITE,mono=True)
        if u>.12:
            definition(im,'Repo',130,860,335,CYAN,'@Repository')
        if u>.25:
            definition(im,'OrderService',535,860,415,GREEN,'@Service')
        if elapsed>=cues.get('register',(scene_duration or 5)*.65)-.55:
            p=reveal(elapsed,cues.get('register',(scene_duration or 5)*.65)-.55,.55)
            arrow(im,(300,984),(300,1100),p,PURPLE,4)
            arrow(im,(740,984),(740,1100),p,PURPLE,4)
            txt(im,'register metadata',540,1020,31,PURPLE,center=True)
        box(im,(120,1110,960,1285),fill=NAVY,outline=EDGE,r=20)
        txt(im,'BEAN DEFINITIONS',145,1125,29,WHITE,True)
        if elapsed>=cues.get('register',(scene_duration or 5)*.65):
            tag(im,'Repo',155,1180,CYAN,36)
            tag(im,'OrderService',530,1180,GREEN,36)
        return im
    if k==2:
        im=base(k,'RESOLVE BY TYPE',['The constructor','declares the need.'])
        box(im,(120,636,960,830),fill=CARD,outline=EDGE,r=20)
        txt(im,'SINGLE CONSTRUCTOR',145,651,29,MUTED,True)
        code_runs(im,[('OrderService(',WHITE),('Repo',CYAN),(' repo)',WHITE)],145,716,43)
        if elapsed>=cues.get('resolve',(scene_duration or 5)*.53):
            resolve=cues.get('resolve',(scene_duration or 5)*.53);match=cues.get('type',(scene_duration or 5)*.81)
            arrow(im,(538,803),(325,1002),reveal(elapsed,resolve,max(.2,match-resolve)),PURPLE,5)
            box(im,(540,866,947,925),fill=NAVY,outline=None,r=10)
            txt(im,'match the Repo type',555,877,32,PURPLE,True)
        box(im,(120,969,960,1235),fill=NAVY,outline=EDGE,r=22)
        txt(im,'REGISTERED DEFINITIONS',145,985,28,MUTED,True)
        definition(im,'Repo',150,1040,340,CYAN)
        definition(im,'OrderService',530,1040,390,GREEN)
        if elapsed>=cues.get('type',(scene_duration or 5)*.81):tag(im,'ONE MATCH',155,1171,GREEN,31)
        txt(im,'One constructor: no @Autowired needed',120,1260,31,WHITE)
        return im
    if k==3:
        im=base(k,'CONSTRUCTOR INJECTION',['Create Repo.','Pass its reference.'])
        box(im,(120,625,960,854),fill=CARD,outline=EDGE,r=20)
        txt(im,'OrderService(Repo repo) {',145,647,39,WHITE,mono=True)
        if elapsed>=cues.get('pass',(scene_duration or 5)*.40):code_runs(im,[('  this.repo = ',WHITE),('repo',CYAN),(';',WHITE)],145,713,39)
        txt(im,'}',145,778,39,WHITE,mono=True)
        box(im,(120,930,960,1270),fill='#112532',outline=GREEN,r=25,width=2)
        txt(im,'SPRING ASSEMBLES THE OBJECT GRAPH',145,950,28,GREEN,True)
        if elapsed>=cues.get('create',(scene_duration or 5)*.03):object_node(im,'Repo',155,1038,275,145,CYAN,46,'created first')
        if elapsed>=cues.get('pass',(scene_duration or 5)*.40):
            begin=cues.get('pass',(scene_duration or 5)*.40);end=cues.get('constructor',(scene_duration or 5)*.75)
            p=reveal(elapsed,begin,max(.2,end-begin))
            arrow(im,(430,1109),(595,1109),p,PURPLE,5)
            if p<1:
                x=430+165*p
                ImageDraw.Draw(im).ellipse((x-11,1098,x+11,1120),fill=WHITE)
            txt(im,'Repo reference',540,1210,32,PURPLE,center=True)
        if elapsed>=cues.get('pass',(scene_duration or 5)*.40):
            if elapsed<cues.get('constructor',(scene_duration or 5)*.75):
                box(im,(615,1038,920,1183),fill=CARD,outline=GREEN,r=20,width=2)
                txt(im,'constructor',767,1065,37,GREEN,True,center=True)
                txt(im,'receives repo',767,1127,29,WHITE,center=True)
            else:object_node(im,'OrderService',615,1038,305,145,GREEN,37,'ready + wired')
        return im
    if k==4:
        im=base(k,'VERIFY, THEN USE',['The graph is ready.','Now the app uses it.'])
        box(im,(120,620,960,710),fill=CARD,outline=EDGE,r=18)
        txt(im,'ctx.getBean(OrderService.class)',145,639,39,WHITE,mono=True)
        object_node(im,'App',130,833,240,135,CYAN,44,'uses service' if elapsed>=cues.get('application',(scene_duration or 6.7)*.66) else 'caller')
        box(im,(574,756,960,1052),fill='#112532',outline=GREEN,r=24,width=2)
        txt(im,'SPRING CONTAINER',597,774,27,GREEN,True)
        txt(im,'Repo',770,835,34,CYAN,True,center=True)
        arrow(im,(770,881),(770,902),1,PURPLE,4)
        object_node(im,'OrderService',620,909,300,100,GREEN,37)
        if elapsed>.12:
            arrow(im,(382,843),(603,843),reveal(elapsed,.12,.20),CYAN)
            txt(im,'request',488,792,28,CYAN,center=True)
        if elapsed>.33:
            arrow(im,(603,998),(249,998),reveal(elapsed,.33,.28),GREEN)
            txt(im,'wired reference',425,1033,28,GREEN,center=True)
        box(im,(120,1125,960,1285),fill='#112532',outline=GREEN,r=18)
        txt(im,'ACTUAL JAVA RUN · EXCERPT',145,1140,25,MUTED,True)
        if elapsed>=cues.get('confirm',.7):txt(im,'same Repo bean: true',145,1182,39,GREEN,mono=True)
        if elapsed>=cues.get('use',(scene_duration or 6.7)*.71):txt(im,'application result: ready',145,1237,32,WHITE,mono=True)
        return im
    if k==5:return recap_scene(u,elapsed,recap,scene_duration)
    if k==6:return thanks_scene(u,elapsed,scene_duration)
    raise ValueError(k)

def recap_complete_at(cues):
    return float(cues.get('complete',float(cues.get('use',3.0))+.65))

def recap_scene(u,elapsed=None,cues=None,scene_duration=None):
    cues=cues or {};duration=scene_duration or 9.055125
    t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(cues.get(key,default))
    scan=at('scan',0);register=at('register',.30);resolve=at('resolve',.80)
    inject=at('inject',1.25);use=at('use',2.4);complete=at('complete',use+.65)
    im=base(5,'DEPENDENCY INJECTION',['Before the app uses it.'])
    if t>=scan:
        box(im,(120,555,960,741),fill=CARD,outline=PURPLE,r=20,width=2)
        txt(im,'APP: REGISTER + REFRESH',145,569,29,CYAN,True)
        txt(im,'ctx.register(Config.class)',145,612,37,WHITE,mono=True)
        txt(im,'@ComponentScan("lesson.di")',145,674,37,PURPLE,mono=True)
    if t>=register:
        arrow(im,(540,744),(540,779),reveal(t,register,.22),PURPLE,4)
        box(im,(120,784,960,936),fill=NAVY,outline=EDGE,r=20)
        txt(im,'REGISTER BEAN DEFINITIONS',145,795,28,MUTED,True)
        code_runs(im,[('@Repository ',PURPLE),('Repo',CYAN)],145,837,37)
        code_runs(im,[('@Service ',PURPLE),('OrderService',GREEN)],145,886,37)
    if t>=resolve:
        arrow(im,(540,940),(540,974),reveal(t,resolve,.22),PURPLE,4)
        box(im,(120,978,960,1102),fill=CARD,outline=CYAN,r=20)
        txt(im,'RESOLVE THE Repo PARAMETER',145,990,28,CYAN,True)
        code_runs(im,[('OrderService(',WHITE),('Repo',CYAN),(' repo)',WHITE)],145,1034,41)
    if t>=inject:
        arrow(im,(460,1105),(460,1137),reveal(t,inject,.25),PURPLE,4)
        box(im,(120,1140,775,1308),fill='#112532',outline=GREEN,r=20,width=2)
        txt(im,'INJECT REFERENCE',142,1151,27,GREEN,True)
        object_node(im,'Repo',142,1200,205,84,CYAN,40)
        object_node(im,'OrderService',447,1200,305,84,GREEN,36)
        arrow(im,(347,1242),(430,1242),reveal(t,inject,.55),PURPLE,4)
    if t>=use:
        box(im,(815,1196,950,1284),fill=CARD,outline=CYAN,r=18,width=2)
        txt(im,'App',882,1215,40,CYAN,True,center=True)
        arrow(im,(778,1240),(805,1240),reveal(t,use,max(.1,complete-use)),GREEN,4)
        txt(im,'USE',881,1154,29,GREEN,True,center=True)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.45;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im


def graph_ready_at(data):
    """Absolute time at which constructor injection has completed in scene 4."""
    return float(data['scene_cues_absolute']['injection']['constructor'])

def application_use_start(data):
    """Absolute time of scene 5 business use, after graph assembly."""
    return float(data['scene_cues_absolute']['proof']['application'])

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
    cue_key={1:'discovery',2:'resolution',3:'injection',4:'proof'}.get(k)
    stage_cues={key:val-s['start'] for key,val in data.get('scene_cues_absolute',{}).get(cue_key,{}).items()}
    im=scene(k,u,elapsed=t-s['start'],recap=data.get('recap_cues'),scene_duration=s['end']-s['start'],scene_cues=stage_cues)
    if with_caption and k!=6:
        # The thanks card itself displays its spoken words; avoid duplicate text.
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
        closing=next(s for s in data['scenes'] if s['scene']==6)
        completed_at=(data.get('recap_hold_start',closing['end']-2.0)+data.get('recap_hold_end',closing['end']))/2
        recap=scene(5,1.0,elapsed=completed_at-closing['start'],recap=data.get('recap_cues'),scene_duration=closing['end']-closing['start'])
        recap.save(ROOT/'recap.png')
        thanks=next((s for s in data['scenes'] if s['scene']==7),None)
        if thanks:thanks_scene(1.0,elapsed=thanks['end']-thanks['start'],scene_duration=thanks['end']-thanks['start']).save(ROOT/'thanks.png')
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
