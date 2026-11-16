#!/usr/bin/env python3
"""Original Pillow/NumPy motion design. Full resolution frames piped to FFmpeg.
Run from any directory: python source/animation/render.py [--previews|--render].
Timing is from actual locally synthesized Kokoro speech, not estimated duration.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json, math, subprocess, argparse
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
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    # right aligned topic marker within the safe area
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

def recipe(im,name,x,y,w=310,h=150,detail=None,size=40):
    """Paper-shaped metadata. This remains present after objects are created."""
    d=ImageDraw.Draw(im);fold=25
    d.polygon([(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)],fill='#171d36',outline=PURPLE,width=2)
    line(im,[(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)],PURPLE,2)
    txt(im,name,x+20,y+14,size,PURPLE,True)
    if detail:txt(im,detail,x+20,y+h-50,29,WHITE,mono=True)

def context_frame(im,xy,label='ApplicationContext',factory=True):
    box(im,xy,fill='#0d1d2d',outline=PURPLE,r=25,width=2)
    x,y,x2,y2=xy
    txt(im,label,x+23,y+13,38,PURPLE,True)
    if factory:txt(im,'BEAN FACTORY · DEMO BEANS',x+23,y+65,25,MUTED,True)

def header_hook():
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    tag(im,'APPLICATIONCONTEXT',100,350,GREEN,26)
    lines(im,["What's inside?"],100,442,76,WHITE,True)
    return im

def hook_scene(t,with_motion=True):
    im=header_hook()
    context_frame(im,(120,626,960,1270))
    txt(im,'DEFINITIONS',150,766,30,PURPLE,True)
    txt(im,'INSTANCES',616,766,30,GREEN,True)
    recipe(im,'repo',150,834,320,135,'@Bean recipe',41)
    recipe(im,'service',150,1030,320,135,'needs Repo',41)
    object_node(im,'Repo',620,834,310,130,GREEN,44,'created object')
    object_node(im,'Service',620,1030,310,135,GREEN,44,'holds Repo')
    arrow(im,(775,972),(775,1019),1,PURPLE,5)
    txt(im,'≠',538,935,69,WHITE,True,center=True)
    if with_motion:
        # Scanning the recipe column begins immediately, then the corresponding
        # object is highlighted; metadata is never moved out of the container.
        p=(t%2.2)/2.2
        y=834+331*p
        # A reading bracket moves along the metadata rather than striking
        # through its labels, so no definition appears deleted or crossed out.
        line(im,[(149,y),(138,y),(138,y+42),(149,y+42)],CYAN,4)
        x=620+310*((t/.95)%1)
        ImageDraw.Draw(im).ellipse((x-6,821,x+6,833),fill=CYAN)
    txt(im,'A REFRESHED CONTEXT',540,1211,26,MUTED,True,center=True)
    return im

def cover():
    im=hook_scene(0,False)
    # Standalone thumbnail only: it is deliberately not held in the video.
    return im
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or {0:2.3,1:5.5,2:7.4,3:5.1,4:5.1,5:9.1,6:1.5}[k]
    t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:return hook_scene(t)
    if k==1:
        instance=at('instance',duration*.55)
        im=base(k,'METADATA ≠ OBJECT',['Recipes describe.','Instances do the work.'])
        context_frame(im,(120,631,960,1278))
        txt(im,'BEAN DEFINITION',150,769,29,PURPLE,True)
        recipe(im,'service',150,831,350,320,None,44)
        code_runs(im,[('type: ',MUTED),('Service',WHITE)],171,918,32)
        txt(im,'scope: singleton',171,978,32,WHITE,mono=True)
        txt(im,'needs: Repo',171,1038,32,WHITE,mono=True)
        if t>=instance:
            txt(im,'MANAGED INSTANCE',605,769,28,GREEN,True)
            object_node(im,'Service',610,892,310,185,GREEN,47,'actual Java object')
            arrow(im,(505,991),(596,991),reveal(t,instance,.40),CYAN,5)
            txt(im,'build',550,918,29,CYAN,True,center=True)
            txt(im,'Definition stays.',540,1196,36,PURPLE,True,center=True)
        return im
    if k==2:
        register=at('register',0);refresh=at('refresh',duration*.3)
        defs=at('definitions',duration*.48);repo=at('repo',duration*.70);service=at('service',duration*.86)
        im=base(k,'REGISTER, THEN REFRESH',['Refresh turns recipes','into managed beans.'])
        box(im,(120,623,960,910),fill=CARD,outline=EDGE,r=20)
        txt(im,'var ctx = new',145,638,37,WHITE,mono=True)
        txt(im,'AnnotationConfigApplicationContext();',145,691,35,WHITE,mono=True)
        if t>=register:code_runs(im,[('ctx.',WHITE),('register',PURPLE),('(Config.class);',WHITE)],145,759,37)
        if t>=refresh:code_runs(im,[('ctx.',WHITE),('refresh',GREEN),('();',WHITE)],145,828,40)
        if t>=defs:
            txt(im,'@Bean DEFINITIONS',145,933,27,PURPLE,True)
            recipe(im,'repo',145,1002,305,111,None,37)
            recipe(im,'service(Repo)',145,1157,305,111,None,33)
        if t>=repo:
            txt(im,'OUR DEFAULT SINGLETONS',625,933,25,GREEN,True)
            object_node(im,'Repo',625,1002,310,111,GREEN,41)
        if t>=service:
            arrow(im,(780,1116),(780,1148),reveal(t,service,.25),PURPLE,4)
            object_node(im,'Service',625,1157,310,111,GREEN,41)
            arrow(im,(453,1212),(611,1212),reveal(t,service,.32),CYAN,4)
        return im
    if k==3:
        request=at('request',0);returned=at('return',at('returns',duration*.46))
        im=base(k,'LOOK UP THE READY BEAN',['getBean returns','the managed service.'])
        context_frame(im,(120,631,960,1067))
        object_node(im,'Repo',145,804,300,144,GREEN,44,'same managed Repo')
        object_node(im,'Service',630,804,300,144,GREEN,44,'already wired')
        arrow(im,(450,876),(615,876),1,PURPLE,5)
        txt(im,'dependency',540,772,28,PURPLE,True,center=True)
        box(im,(120,1175,960,1306),fill=CARD,outline=CYAN,r=20)
        txt(im,'APP REQUEST',145,1185,28,CYAN,True)
        txt(im,'ctx.getBean(Service.class)',145,1233,39,WHITE,mono=True)
        if t>=request:
            arrow(im,(780,1170),(780,964),reveal(t,request,.45),CYAN,5)
            txt(im,'lookup',812,1092,28,CYAN,True)
        if t>=returned:
            p=reveal(t,returned,.55)
            # Return a reference while the managed object remains in context.
            line(im,[(630,920),(530,920),(530,1138)],CYAN,4)
            arrow(im,(530,1115),(530,1165),p,CYAN,4)
            txt(im,'same service reference',145,1098,31,CYAN,True)
            if p<1:ImageDraw.Draw(im).ellipse((522,1090+60*p,538,1106+60*p),fill=WHITE)
        return im
    if k==4:
        event=at('event',0);close=at('close',duration*.55);cleanup=at('cleanup',duration*.80)
        im=base(k,'EVENTS + LIFECYCLE',['More than bean lookup.'])
        context_frame(im,(120,631,960,1287),factory=False)
        code_runs(im,[('ctx.',WHITE),('publishEvent',CYAN),('(',WHITE)],145,709,38)
        txt(im,'  new DemoEvent(ctx));',145,767,38,WHITE,mono=True)
        if t>=event:
            box(im,(145,897,438,1007),fill=CARD,outline=CYAN,r=17)
            txt(im,'DemoEvent',290,921,35,CYAN,True,center=True)
            object_node(im,'Service',628,879,300,145,GREEN,43,'event listener')
            p=reveal(t,event,.65)
            arrow(im,(445,951),(611,951),p,CYAN,5)
            if t<close:
                x=445+166*p;ImageDraw.Draw(im).ellipse((x-9,942,x+9,960),fill=WHITE)
            txt(im,'one event handled',145,1054,33,GREEN,True)
        if t>=close:
            code_runs(im,[('ctx.',WHITE),('close',PURPLE),('();',WHITE)],145,1158,41)
            tag(im,'CLOSED',752,646,PURPLE,25)
        if t>=cleanup:
            # right align the success text inside the container
            d=ImageDraw.Draw(im)
            txt(im,'cleanup called',930-d.textlength('cleanup called',font=font(33,True)),1217,33,GREEN,True)
        return im
    if k==5:return recap_scene(u,t,recap,duration,cues)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',4.8))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};proof_cues=proof_cues or {};duration=scene_duration or 9.1;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(proof_cues.get(key,cues.get(key,default)))
    same=at('same',1);event=at('event',1.8);cleanup=at('cleanup',2.6)
    complete=at('complete',4.8);takeaway=at('takeaway',complete)
    im=base(5,'ACTUAL SPRING TESTS',['Definitions describe.','Instances do the work.'])
    box(im,(120,624,960,830),fill='#112532',outline=GREEN,r=20,width=2)
    if t>=same:txt(im,'same service: true',145,637,37,GREEN,mono=True)
    if t>=event:txt(im,'events handled: 1',145,694,37,GREEN,mono=True)
    if t>=cleanup:txt(im,'cleanup called: true',145,751,37,GREEN,mono=True)
    box(im,(120,860,960,945),fill=CARD,outline=PURPLE,r=18)
    txt(im,'new context → register Config',145,878,36,PURPLE,mono=True)
    if t>=max(0,same-.35):
        arrow(im,(540,947),(540,976),1,PURPLE,4)
        box(im,(120,982,960,1075),fill=CARD,outline=PURPLE,r=18)
        code_runs(im,[('refresh()',GREEN),(' : recipes → objects',WHITE)],145,1005,36)
    if t>=same:
        arrow(im,(540,1078),(540,1104),1,CYAN,4)
        box(im,(120,1110,960,1195),fill=CARD,outline=CYAN,r=18)
        code_runs(im,[('getBean()',CYAN),(' → same Service',WHITE)],145,1129,36)
    if t>=cleanup:
        arrow(im,(540,1198),(540,1222),1,GREEN,4)
        box(im,(120,1227,960,1307),fill=CARD,outline=GREEN,r=18)
        txt(im,'event → close → cleanup',145,1242,37,GREEN,mono=True)
    if t>=takeaway:
        # The full graph remains unchanged through the silent reading hold.
        line(im,[(100,585),(100+690*reveal(t,takeaway,.35),585)],GREEN,4)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.45;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im

def mechanism_anchors(data):
    c=data['scene_cues_absolute'];i=c['initialization'];l=c['lookup'];s=c['services']
    return {'config_registered_s':float(i['register']),'refresh_s':float(i['refresh']),
            'definitions_registered_s':float(i['definitions']),'instances_created_s':float(i['service']),
            'graph_ready_s':float(i['service'])+.35,'lookup_s':float(l['request']),
            'reference_return_s':float(l.get('return',l.get('returns'))),
            'event_s':float(s['event']),'close_s':float(s['close']),'cleanup_s':float(s['cleanup'])}
def graph_ready_at(data):return mechanism_anchors(data)['graph_ready_s']
def application_use_start(data):return mechanism_anchors(data)['lookup_s']
def read_timing():return json.loads((ROOT/'source/timing.json').read_text())

def caption(im,text):
    size=43;f=font(size,True);d=ImageDraw.Draw(im);words=text.replace('get bean','getBean').split();out=[];row=''
    for word in words:
        candidate=(row+' '+word).strip()
        if d.textlength(candidate,font=f)>830 and row:out.append(row);row=word
        else:row=candidate
    if row:out.append(row)
    if len(out)>2:raise ValueError(('caption too long',text,out))
    box(im,(100,1322,980,1487),fill='#0a1326',outline=None,r=17)
    y=1340+(2-len(out))*27
    lines(im,out,540,y,size,WHITE,True,gap=1.22,center=True)

def render_frame(t,data,with_caption=True):
    scenes=data['scenes'];k=next((i for i,s in enumerate(scenes) if s['start']<=t<s['end']),len(scenes)-1)
    s=scenes[k];u=(t-s['start'])/(s['end']-s['start'])
    key={1:'distinction',2:'initialization',3:'lookup',4:'services',5:'proof'}.get(k)
    stage={key:val-s['start'] for key,val in data.get('scene_cues_absolute',{}).get(key,{}).items()}
    im=scene(k,u,t-s['start'],data.get('recap_cues'),s['end']-s['start'],stage)
    if with_caption and k!=6:
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
    COVER.save(ROOT/'cover.png');data=read_timing();write_srt(data)
    if a.previews:
        out=ROOT/'source/evidence';out.mkdir(exist_ok=True)
        samples=[0]+[s['start']+(s['end']-s['start'])*.78 for s in data['scenes']]
        thumbs=[]
        for j,t in enumerate(samples):
            im=render_frame(t,data);im.save(out/f'preview-{j}.png');thumbs.append(im.resize((324,576),Image.Resampling.LANCZOS))
        contact=Image.new('RGB',(1296,1152),NAVY)
        for j,im in enumerate(thumbs):contact.paste(im,(j%4*324,j//4*576))
        contact.save(out/'mobile-contact-sheet.png')
        closing=data['scenes'][-2];t=(data['recap_hold_start']+data['recap_hold_end'])/2
        proof={key:val-closing['start'] for key,val in data.get('scene_cues_absolute',{}).get('proof',{}).items()}
        scene(5,1,t-closing['start'],data.get('recap_cues'),closing['end']-closing['start'],proof).save(ROOT/'recap.png')
        thanks=data['scenes'][-1];thanks_scene(1,thanks['end']-thanks['start'],thanks['end']-thanks['start']).save(ROOT/'thanks.png')
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
