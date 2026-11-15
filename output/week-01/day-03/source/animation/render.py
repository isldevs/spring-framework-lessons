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
    tag(im,'SPRING BOOT',100,352,GREEN,27)
    lines(im,['Constructor','injection'],100,447,94,WHITE,True,gap=1.10)
    lines(im,['How does OrderService','get its gateway?'],100,711,55,WHITE,True,gap=1.18)
    box(im,(135,912,945,1012),fill=NAVY,outline=PURPLE,r=18)
    txt(im,'INTERFACE',158,927,25,PURPLE,True)
    txt(im,'PaymentGateway',540,957,39,WHITE,mono=True,center=True)
    object_node(im,'DemoGateway',135,1112,335,137,CYAN,40,'implements interface')
    object_node(im,'OrderService',610,1112,335,137,GREEN,40,'requires gateway')
    arrow(im,(470,1181),(590,1181),1,PURPLE,5)
    return im
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or {0:2.7,1:6.1,2:5.2,3:6.0,4:6.0,5:9.2,6:1.5}[k]
    t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:
        im=COVER.copy()
        if u>.55:
            x=470+120*reveal(u,.55,.4)
            ImageDraw.Draw(im).ellipse((x-9,1172,x+9,1190),fill=WHITE)
        return im
    if k==1:
        constructor=at('constructor',duration*.35);final=at('final',duration*.78)
        im=base(k,'DECLARE THE REQUIREMENT',['Require the gateway','at construction.'])
        box(im,(120,630,960,948),fill=CARD,outline=EDGE,r=20)
        txt(im,'CONSTRUCTOR SIGNATURE',145,646,30,GREEN,True)
        txt(im,'OrderService(',145,701,40,WHITE,mono=True)
        if t>=constructor-.2:
            code_runs(im,[('  ',WHITE),('PaymentGateway',CYAN),(' gateway)',WHITE)],145,762,38)
        if t>=constructor:
            tag(im,'ONE CONSTRUCTOR',145,844,GREEN,29)
        if t>=final:
            box(im,(120,1032,960,1242),fill=CARD,outline=CYAN,r=20,width=2)
            txt(im,'STORED REQUIRED REFERENCE',145,1046,28,CYAN,True)
            code_runs(im,[('private ',WHITE),('final ',GREEN),('PaymentGateway',CYAN)],145,1105,38)
            txt(im,'    gateway;',145,1168,38,WHITE,mono=True)
            p=reveal(t,final,.40)
            line(im,[(145,1216),(145+405*p,1216)],GREEN,4)
        return im
    if k==2:
        scan=at('scan',duration*.16);match=at('match',duration*.56);interface=at('interface',duration*.72)
        im=base(k,'BOOT STARTS SPRING',['One bean matches','the interface.'])
        box(im,(120,622,960,830),fill=CARD,outline=PURPLE,r=20)
        txt(im,'@SpringBootApplication',145,641,38,PURPLE,mono=True)
        txt(im,'SpringApplication.run(',145,701,36,WHITE,mono=True)
        txt(im,'  CheckoutApplication.class);',145,754,36,WHITE,mono=True)
        if t>=scan:
            box(im,(120,891,960,1034),fill=NAVY,outline=PURPLE,r=18)
            txt(im,'REQUIRED INTERFACE',145,904,27,PURPLE,True)
            txt(im,'PaymentGateway',540,950,43,CYAN,mono=True,center=True)
        if t>=match:
            box(im,(120,1114,960,1288),fill=NAVY,outline=CYAN,r=18,width=2)
            code_runs(im,[('@Component ',PURPLE),('DemoGateway',CYAN)],145,1128,37)
            txt(im,'implements PaymentGateway',145,1187,37,WHITE,mono=True)
            tag(im,'ONE MATCH',710,1229,GREEN,24)
        if t>=interface:
            arrow(im,(540,1110),(540,1043),reveal(t,interface,.35),PURPLE,5)
            txt(im,'matches type',577,1057,30,PURPLE,True)
        return im
    if k==3:
        passing=at('pass',duration*.1);ready=at('ready',duration*.47);place=at('place',duration*.73)
        im=base(k,'SUPPLY THE CONSTRUCTOR',['Pass a reference.','Then place an order.'])
        box(im,(120,629,960,1117),fill='#112532',outline=GREEN,r=24,width=2)
        txt(im,'SPRING CONTAINER',145,646,29,GREEN,True)
        txt(im,'PaymentGateway is the contract',540,711,33,PURPLE,True,center=True)
        object_node(im,'DemoGateway',143,808,310,145,CYAN,37,'managed bean')
        if t>=passing:
            p=reveal(t,passing,max(.15,ready-passing))
            arrow(im,(453,880),(570,880),p,PURPLE,5)
            if p<1:
                x=453+117*p
                ImageDraw.Draw(im).ellipse((x-10,870,x+10,890),fill=WHITE)
            txt(im,'same object reference',540,1045,32,PURPLE,center=True)
        if t<ready:
            box(im,(590,784,934,1001),fill=CARD,outline=GREEN,r=19,width=2)
            txt(im,'OrderService',762,800,39,GREEN,True,center=True)
            txt(im,'constructor',762,859,36,WHITE,True,center=True)
            txt(im,'PaymentGateway',762,923,35,CYAN,mono=True,center=True)
        else:
            object_node(im,'OrderService',590,784,344,217,GREEN,39,'final gateway assigned')
            txt(im,'READY',762,874,35,WHITE,True,center=True)
        if t>=place:
            box(im,(120,1180,960,1301),fill=CARD,outline=CYAN,r=18)
            txt(im,'APP: placeOrder',145,1187,31,CYAN,True)
            txt(im,'order-1042  /  USD 19.99',145,1236,38,WHITE,mono=True)
            txt(im,'SIMULATED',822,1191,25,MUTED,True,center=True)
        return im
    if k==4:
        same=at('same',duration*.28);fake=at('fake',duration*.62)
        im=base(k,'ACTUAL BOOT + SERVICE TESTS',['Verify the wiring.','Test with a fake.'])
        box(im,(120,630,960,864),fill='#112532',outline=GREEN,r=20,width=2)
        txt(im,'SPRING BOOT INTEGRATION TEST',145,647,28,GREEN,True)
        txt(im,'Managed DemoGateway',145,705,38,CYAN,True)
        if t>=same:txt(im,'same gateway bean: true',145,777,38,WHITE,mono=True)
        if t>=fake:
            box(im,(120,939,960,1260),fill=CARD,outline=PURPLE,r=20)
            txt(im,'SEPARATE PURE JAVA SERVICE TEST',145,954,28,PURPLE,True)
            txt(im,'new OrderService(fake)',145,1008,40,WHITE,mono=True)
            object_node(im,'fake gateway',148,1080,290,100,CYAN,35)
            object_node(im,'OrderService',615,1080,300,100,GREEN,36)
            arrow(im,(438,1130),(595,1130),reveal(t,fake,.40),PURPLE,5)
            txt(im,'fake gateway test: passed',145,1202,36,GREEN,mono=True)
        return im
    if k==5:return recap_scene(u,t,recap,duration)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',float(cues.get('use',3.0))+.65))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None):
    cues=cues or {};duration=scene_duration or 9.2;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(cues.get(key,default))
    require=at('require',0);resolve=at('resolve',.6);inject=at('inject',1.3);use=at('use',2.5);complete=at('complete',use+.65)
    im=base(5,'CONSTRUCTOR INJECTION',['Required at creation.'])
    box(im,(120,552,960,776),fill=CARD,outline=PURPLE,r=20)
    txt(im,'BOOT STARTS SPRING + SCANS',145,566,28,GREEN,True)
    txt(im,'@SpringBootApplication',145,611,36,PURPLE,mono=True)
    if t>=resolve:
        code_runs(im,[('@Component ',PURPLE),('DemoGateway',CYAN)],145,663,36)
        txt(im,'implements PaymentGateway',145,716,36,WHITE,mono=True)
    if t>=require:
        box(im,(120,819,960,963),fill=CARD,outline=CYAN,r=20)
        txt(im,'REQUIRED CONSTRUCTOR PARAMETER',145,833,27,CYAN,True)
        txt(im,'OrderService(PaymentGateway gateway)',145,884,36,WHITE,mono=True)
    if t>=resolve:
        arrow(im,(540,779),(540,814),reveal(t,resolve,.23),PURPLE,4)
        txt(im,'one type match',574,778,28,PURPLE)
    if t>=inject:
        arrow(im,(540,966),(540,997),reveal(t,inject,.23),PURPLE,4)
        box(im,(120,1002,960,1172),fill='#112532',outline=GREEN,r=20,width=2)
        txt(im,'SPRING SUPPLIES THE REFERENCE',145,1014,27,GREEN,True)
        object_node(im,'DemoGateway',145,1060,300,88,CYAN,36)
        object_node(im,'OrderService',615,1060,320,88,GREEN,37)
        arrow(im,(445,1104),(595,1104),reveal(t,inject,.50),PURPLE,4)
    if t>=use:
        arrow(im,(540,1176),(540,1210),reveal(t,use,max(.1,complete-use)),GREEN,4)
        box(im,(120,1215,960,1308),fill=CARD,outline=CYAN,r=18)
        txt(im,'APP USES READY SERVICE',145,1223,26,CYAN,True)
        txt(im,'placeOrder(orderId, cents)',145,1261,37,WHITE,mono=True)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.45;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im

def graph_ready_at(data):return float(data['scene_cues_absolute']['injection']['ready'])
def application_use_start(data):return float(data['scene_cues_absolute']['injection']['place'])

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
    cue_key={1:'requirement',2:'discovery',3:'injection',4:'proof'}.get(k)
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
