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
NAVY='#080f20'; WHITE='#f5f7ff'; MUTED='#9daec9'; CYAN='#5cddfa'; PURPLE='#b397ff'; GREEN='#94e568'; RED='#ff7d91'; CARD='#111e34'; EDGE='#2a3c58'
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

def fail_mark(im,x,y,size=14):
    line(im,[(x-size,y-size),(x+size,y+size)],RED,5)
    line(im,[(x-size,y+size),(x+size,y-size)],RED,5)

def success_mark(im,x,y,size=13):
    line(im,[(x-size,y),(x-3,y+size),(x+size,y-size)],GREEN,5)

def class_file(im,name,x,y,w=330,h=180,annotation=None,package=None):
    recipe(im,name,x,y,w,h,None,43)
    if package:txt(im,package,x+20,y+67,27,MUTED,mono=True)
    if annotation:txt(im,annotation,x+20,y+h-50,34,PURPLE,mono=True)

def missing_slot(im,xy,label='Client'):
    x,y,x2,y2=xy
    # A missing definition has an outlined slot, not an object silhouette.
    box(im,xy,fill=NAVY,outline=RED,r=16,width=2)
    txt(im,label,x+20,y+12,40,WHITE,True)
    txt(im,'NO DEFINITION',x+20,y2-48,27,RED,True)
    fail_mark(im,x2-30,y+37,11)

def header_hook():
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    tag(im,'BEAN REGISTRATION',100,350,GREEN,26)
    lines(im,["Why isn't this",'a Spring bean?'],100,431,73,WHITE,True,gap=1.10)
    return im

def hook_scene(t,with_motion=True):
    im=header_hook()
    txt(im,'PLAIN JAVA CLASS',140,668,29,PURPLE,True)
    recipe(im,'Client',140,729,350,218,None,47)
    txt(im,'class Client {}',160,811,35,WHITE,mono=True)
    txt(im,'on the classpath',160,885,28,MUTED)
    context_frame(im,(570,663,960,1081),'Spring context',factory=False)
    txt(im,'DEMO DEFINITIONS',593,729,25,MUTED,True)
    missing_slot(im,(593,793,937,972))
    box(im,(120,1177,960,1306),fill=CARD,outline=CYAN,r=20)
    txt(im,'APP REQUEST',145,1187,28,CYAN,True)
    txt(im,'ctx.getBean(Client.class)',145,1234,39,WHITE,mono=True)
    arrow(im,(805,1172),(805,1093),1,CYAN,5)
    if with_motion:
        # A lookup token moves toward the registry immediately. The absent
        # definition remains absent; an arbitrary class never moves inside.
        p=(t%1.15)/1.15
        y=1167-72*p
        ImageDraw.Draw(im).ellipse((797,y-8,813,y+8),fill=CYAN)
        x=601+318*((t/.95)%1)
        line(im,[(x,989),(x+13,989)],RED,4)
    txt(im,'REFRESHED · NO Client BEAN',765,1020,24,RED,True,center=True)
    return im

def cover():
    # Standalone thumbnail, deliberately not held at the start of the movie.
    return hook_scene(0,False)
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or {0:1.9,1:5.8,2:7.0,3:5.4,4:4.6,5:9.0,6:1.5}[k]
    t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:return hook_scene(t)
    if k==1:
        request=at('request',0);fail=at('fail',duration*.48)
        im=base(k,'CLASSPATH IS NOT REGISTRATION',["A class alone",'is not registered.'])
        context_frame(im,(120,631,960,1056),factory=False)
        txt(im,'BEAN FACTORY · DEMO DEFINITIONS',145,712,28,MUTED,True)
        missing_slot(im,(145,791,935,976),'Client')
        if t>=request:
            arrow(im,(850,1138),(850,1064),reveal(t,request,.42),CYAN,5)
            txt(im,'ctx.getBean(Client.class)',145,1077,37,CYAN,mono=True)
        if t>=fail:
            box(im,(120,1167,960,1306),fill='#301d2c',outline=RED,r=18)
            txt(im,'EXPECTED LOOKUP FAILURE',145,1175,27,RED,True)
            txt(im,'NoSuchBeanDefinitionException',145,1230,35,WHITE,mono=True)
        return im
    if k==2:
        register=at('register',0);defs=at('definition',duration*.35)
        called=at('call',duration*.54);instance=at('instance',duration*.72);lookup=at('lookup',duration*.90)
        im=base(k,'@BEAN · REGISTERED CONFIGURATION',['Register through','a factory method.'])
        box(im,(120,625,960,767),fill=CARD,outline=PURPLE,r=18)
        if t>=register:
            txt(im,'ctx.register(FactoryConfig.class);',145,641,35,WHITE,mono=True)
            code_runs(im,[('ctx.',WHITE),('refresh',GREEN),('();',WHITE)],145,699,38)
        box(im,(120,807,960,1048),fill=CARD,outline=PURPLE,r=18)
        tag(im,'@Configuration',145,815,PURPLE,25)
        txt(im,'FactoryConfig',930-ImageDraw.Draw(im).textlength('FactoryConfig',font=font(31,True)),826,31,WHITE,True)
        code_runs(im,[('@Bean ',PURPLE),('Client client() {',WHITE)],145,870,38)
        code_runs(im,[('  return ',WHITE),('new Client()',GREEN),(';',WHITE)],145,928,38)
        txt(im,'}',145,983,38,WHITE,mono=True)
        if t>=called:
            p=reveal(t,called,.40)
            line(im,[(338,977),(338+283*p,977)],GREEN,4)
        if t>=defs:
            txt(im,'DEFINITION',145,1073,27,PURPLE,True)
            recipe(im,'client',145,1120,310,111,'factory method',37)
        if t>=instance:
            txt(im,'MANAGED INSTANCE',625,1073,27,GREEN,True)
            arrow(im,(460,1176),(612,1176),reveal(t,instance,.32),CYAN,5)
            object_node(im,'Client',625,1120,310,111,GREEN,41)
        if t>=lookup:
            txt(im,'getBean(Client.class)',145,1260,36,CYAN,mono=True)
            tag(im,'FOUND',745,1251,GREEN,24)
        return im
    if k==3:
        annotation=at('annotation',0);scan=at('scan',duration*.40)
        defs=at('definition',duration*.60);instance=at('instance',duration*.74);lookup=at('lookup',duration*.91)
        im=base(k,'@COMPONENT · CONFIGURED SCAN',['Mark the class.','Scan its package.'])
        box(im,(120,625,960,881),fill=CARD,outline=PURPLE,r=18)
        tag(im,'@Configuration',145,635,PURPLE,25)
        txt(im,'ScanConfig',930-ImageDraw.Draw(im).textlength('ScanConfig',font=font(31,True)),646,31,WHITE,True)
        code_runs(im,[('@ComponentScan',PURPLE),('("lesson.scan")',WHITE)],145,693,35)
        txt(im,'ctx.register(ScanConfig.class);',145,755,35,WHITE,mono=True)
        code_runs(im,[('ctx.',WHITE),('refresh',GREEN),('();',WHITE)],145,810,38)
        if t>=annotation:
            recipe(im,'lesson.scan',145,941,365,178,None,30)
            txt(im,'@Component',165,996,35,PURPLE,mono=True)
            txt(im,'class Worker {}',165,1051,35,WHITE,mono=True)
        if t>=scan:
            p=reveal(t,scan,.50)
            line(im,[(145,911),(145+365*p,911)],CYAN,4)
            arrow(im,(516,1028),(611,1028),p,CYAN,4)
        if t>=defs:
            txt(im,'DEFINITION',625,897,27,PURPLE,True)
            recipe(im,'worker',625,941,310,111,'class: Worker',37)
        if t>=instance:
            arrow(im,(780,1055),(780,1134),reveal(t,instance,.28),GREEN,4)
            object_node(im,'Worker',625,1141,310,106,GREEN,41)
        if t>=lookup:
            txt(im,'getBean(Worker.class)',145,1260,36,CYAN,mono=True)
            tag(im,'FOUND',745,1251,GREEN,24)
        return im
    if k==4:
        outside=at('outside',0);miss=at('miss',duration*.58)
        im=base(k,'SCAN PACKAGE BOUNDARY',['Scan the right','package.'])
        box(im,(120,625,960,753),fill=CARD,outline=PURPLE,r=18)
        txt(im,'CONFIGURED SCOPE',145,638,27,PURPLE,True)
        txt(im,'@ComponentScan("lesson.scan")',145,692,35,WHITE,mono=True)
        box(im,(120,819,560,1007),fill='#112532',outline=GREEN,r=19)
        txt(im,'lesson.scan',145,835,37,GREEN,mono=True)
        tag(im,'@Component',145,892,PURPLE,26)
        txt(im,'Worker',535-ImageDraw.Draw(im).textlength('Worker',font=font(35,True)),901,35,WHITE,True)
        txt(im,'INSIDE THIS SCAN',145,969,25,GREEN,True)
        box(im,(620,819,960,1297),fill=NAVY,outline=PURPLE,r=19)
        txt(im,'DEFINITIONS',642,835,28,PURPLE,True)
        recipe(im,'worker',642,903,293,111,None,37)
        arrow(im,(565,950),(628,950),1,GREEN,4)
        if t>=outside:
            box(im,(120,1085,560,1297),fill='#251b2d',outline=RED,r=19)
            txt(im,'lesson.outside',145,1101,36,RED,mono=True)
            tag(im,'@Component',145,1165,PURPLE,26)
            txt(im,'Outside',535-ImageDraw.Draw(im).textlength('Outside',font=font(35,True)),1174,35,WHITE,True)
            txt(im,'OUTSIDE THIS SCAN',145,1245,25,RED,True)
        if t>=miss:
            p=reveal(t,miss,.4)
            arrow(im,(565,1211),(605,1211),p,RED,4)
            fail_mark(im,606,1211,12)
            txt(im,'Outside',642,1110,38,WHITE,True)
            txt(im,'NO DEFINITION',642,1174,26,RED,True)
        return im
    if k==5:return recap_scene(u,t,recap,duration,cues)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',4.8))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};proof_cues=proof_cues or {};duration=scene_duration or 9.0;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(proof_cues.get(key,cues.get(key,default)))
    bean=at('bean',.3);scan=at('scan',1.0);takeaway=at('takeaway',2.0);complete=at('complete',4.0)
    im=base(5,'ACTUAL REGISTRATION TESTS',['Tell Spring what','to manage.'])
    box(im,(120,625,960,790),fill='#112532',outline=GREEN,r=19)
    if t>=bean:txt(im,'@Bean retrieved: true',145,642,38,GREEN,mono=True)
    if t>=scan:txt(im,'scan retrieved: true',145,706,38,GREEN,mono=True)
    box(im,(120,823,960,909),fill=CARD,outline=PURPLE,r=18)
    txt(im,'registered configuration → refresh()',145,845,35,PURPLE,mono=True)
    if t>=takeaway:
        recipe(im,'@Bean method',135,949,345,116,'factory metadata',32)
        recipe(im,'@Component',600,949,345,116,'configured scan',32)
        arrow(im,(307,912),(307,940),reveal(t,takeaway,.3),PURPLE,4)
        arrow(im,(772,912),(772,940),reveal(t,takeaway,.3),PURPLE,4)
        line(im,[(307,1070),(307,1103),(772,1103),(772,1070)],PURPLE,4)
        arrow(im,(540,1103),(540,1128),reveal(t,takeaway,.5),PURPLE,4)
        box(im,(120,1135,960,1203),fill=CARD,outline=PURPLE,r=17)
        txt(im,'bean definitions',540,1147,36,PURPLE,True,center=True)
    if t>=complete:
        arrow(im,(540,1205),(540,1230),1,GREEN,4)
        box(im,(120,1238,960,1308),fill='#112532',outline=GREEN,r=17)
        txt(im,'managed beans → getBean',540,1249,36,GREEN,mono=True,center=True)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.45;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im

def mechanism_anchors(data):
    c=data['scene_cues_absolute'];m=c['missing'];f=c['factory'];s=c['scanning'];b=c['boundary']
    return {'missing_request_s':float(m['request']),'failed_lookup_s':float(m['fail']),
            'factory_register_s':float(f['register']),'factory_definition_s':float(f['definition']),
            'factory_call_s':float(f['call']),'factory_instance_s':float(f['instance']),
            'factory_lookup_s':float(f['lookup']),'scan_start_s':float(s['scan']),
            'scan_definition_s':float(s['definition']),'scan_instance_s':float(s['instance']),
            'scan_lookup_s':float(s['lookup']),'outside_missing_s':float(b['miss'])}
def graph_ready_at(data):return mechanism_anchors(data)['scan_instance_s']+.35
def application_use_start(data):return mechanism_anchors(data)['scan_lookup_s']

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
    key={1:'missing',2:'factory',3:'scanning',4:'boundary',5:'proof'}.get(k)
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
        samples=[0]+[s['start']+(s['end']-s['start'])*.92 for s in data['scenes']]
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
