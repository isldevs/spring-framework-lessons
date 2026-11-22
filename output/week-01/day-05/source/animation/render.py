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

def client(im, name, x, y, w=300, h=132):
    # Both objects have the same Java type. Their names identify instances.
    object_node(im,'Client',x,y,w,h,GREEN,43,'id: '+name)

def query(im, text, y, label='APP REQUEST', color=CYAN):
    box(im,(120,y,960,y+128),fill=CARD,outline=color,r=19)
    txt(im,label,145,y+9,27,color,True)
    txt(im,text,145,y+56,38,WHITE,mono=True)

def hook_scene(t,with_motion=True):
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    tag(im,'BEAN NAMING',100,350,GREEN,26)
    lines(im,['Two names.','One ambiguous type.'],100,431,68,WHITE,True,gap=1.10)
    context_frame(im,(120,635,960,1133),'READY APPLICATION CONTEXT',factory=False)
    txt(im,'BEAN NAME',150,724,27,PURPLE,True)
    txt(im,'JAVA TYPE',630,724,27,GREEN,True)
    txt(im,'"alpha"',150,804,44,PURPLE,True,mono=True)
    txt(im,'"beta"',150,974,44,PURPLE,True,mono=True)
    client(im,'alpha',620,782,310,132);client(im,'beta',620,952,310,132)
    arrow(im,(425,848),(603,848),1,PURPLE,4)
    arrow(im,(425,1018),(603,1018),1,PURPLE,4)
    txt(im,'BOTH MATCH Client',540,1092,28,RED,True,center=True)
    query(im,'getBean(Client.class)',1174,'TYPE-ONLY REQUEST',CYAN)
    arrow(im,(540,1170),(540,1142),1,CYAN,4)
    if with_motion:
        y=1168-24*((t/.65)%1)
        ImageDraw.Draw(im).ellipse((532,y-8,548,y+8),fill=CYAN)
        x=150+780*((t/1.1)%1)
        line(im,[(x,1120),(min(940,x+24),1120)],RED,4)
    return im

def cover():return hook_scene(0,False)
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or {0:1.9,1:5.8,2:6,3:7,4:6,5:9,6:1.5}[k]
    t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:return hook_scene(t)
    if k==1:
        named=at('name',duration*.24);defs=at('definition',duration*.36);instance=at('instance',duration*.54)
        im=base(k,'EXPLICIT NAME',['Assign an explicit','bean name.'])
        box(im,(120,625,960,767),fill=CARD,outline=PURPLE,r=18)
        txt(im,'ctx.register(AlphaConfig.class);',145,641,35,WHITE,mono=True)
        code_runs(im,[('ctx.',WHITE),('refresh',GREEN),('();',WHITE)],145,699,38)
        box(im,(120,807,960,1055),fill=CARD,outline=PURPLE,r=18)
        tag(im,'@Configuration',145,815,PURPLE,23)
        txt(im,'AlphaConfig',935-ImageDraw.Draw(im).textlength('AlphaConfig',font=font(28,True)),821,28,WHITE,True)
        code_runs(im,[('@Bean("alpha") ',PURPLE),('Client client() {',WHITE)],145,871,36)
        code_runs(im,[('  return ',WHITE),('new Client("alpha")',GREEN),(';',WHITE)],145,928,36)
        txt(im,'}',145,985,36,WHITE,mono=True)
        if t>=named:
            line(im,[(290,915),(290+132*reveal(t,named,.25),915)],PURPLE,4)
        if t>=defs:
            txt(im,'BEAN NAME',145,1081,27,PURPLE,True)
            recipe(im,'alpha',145,1125,310,132,'factory: client',38)
        if t>=instance:
            txt(im,'MANAGED INSTANCE',625,1081,27,GREEN,True)
            client(im,'alpha',625,1125,310,132)
            arrow(im,(460,1191),(611,1191),reveal(t,instance,.30),CYAN,4)
        return im
    if k==2:
        request=at('request',0);returned=at('return',at('returns',duration*.20));check=at('check',duration*.56)
        im=base(k,'LOOK UP BY NAME',['Name lookup selects','that bean.'])
        context_frame(im,(120,630,960,1025),'SINGLE-BEAN CONTEXT',factory=False)
        txt(im,'BEAN NAME',145,743,28,PURPLE,True)
        txt(im,'"alpha"',145,811,47,PURPLE,True,mono=True)
        client(im,'alpha',625,781,310,152)
        if t>=request:
            arrow(im,(423,857),(609,857),reveal(t,request,.25),CYAN,4)
        if t>=returned:
            txt(im,'same Client reference',145,963,33,CYAN,True)
            line(im,[(620,901),(540,901),(540,1043)],CYAN,4)
            arrow(im,(540,1043),(540,1105),reveal(t,returned,.30),CYAN,4)
        query(im,'getBean("alpha")',1110,'BY NAME')
        if t>=check:
            box(im,(120,1110,960,1308),fill=CARD,outline=CYAN,r=19)
            txt(im,'NAME + REQUIRED TYPE',145,1121,26,CYAN,True)
            txt(im,'getBean("alpha", Client.class)',145,1176,37,WHITE,mono=True)
            tag(im,'SAME BEAN · TYPE CHECKED',145,1241,GREEN,25)
        return im
    if k==3:
        lookup=at('lookup',0);returned=at('return',duration*.17);second=at('second_register',duration*.50);definition_at=at('second_definition',duration*.60);instance=at('second_instance',duration*.70)
        im=base(k,'NAME AND TYPE ARE DIFFERENT',['One type match','can work.'] if t<second else ['Now two beans','share that type.'])
        if t<second:
            query(im,'getBean(Client.class)',625,'TYPE-ONLY REQUEST')
            context_frame(im,(120,864,960,1308),'SINGLE-BEAN CONTEXT',factory=False)
            txt(im,'"alpha"',540,968,40,PURPLE,True,mono=True,center=True)
            client(im,'alpha',325,1030,430,159)
            if t>=lookup:
                travel=reveal(t,lookup,.30)*486
                if travel<=353:arrow(im,(900,757),(900,1110),travel/353,CYAN,4)
                else:
                    line(im,[(900,757),(900,1110)],CYAN,4)
                    arrow(im,(900,1110),(767,1110),(travel-353)/133,CYAN,4)
            if t>=returned:txt(im,'same Client object',540,1230,34,GREEN,True,center=True)
        else:
            box(im,(120,625,960,852),fill=CARD,outline=PURPLE,r=18)
            tag(im,'FRESH CONTEXT',145,639,GREEN,25)
            txt(im,'ctx.register(AlphaConfig.class,',145,700,35,WHITE,mono=True)
            txt(im,'             BetaConfig.class);',145,753,35,WHITE,mono=True)
            txt(im,'ctx.refresh();',145,806,35,GREEN,mono=True)
            context_frame(im,(120,902,960,1308),'TWO-BEAN CONTEXT',factory=False)
            txt(im,'"alpha"',145,985,37,PURPLE,True,mono=True)
            txt(im,'"beta"',625,985,37,PURPLE,True,mono=True)
            if t<instance:
                recipe(im,'alpha',145,1064,300,128,'Client',37)
                if t>=definition_at:recipe(im,'beta',625,1064,300,128,'Client',37)
            else:
                client(im,'alpha',145,1064,300,128);client(im,'beta',625,1064,300,128)
                txt(im,'Both beans have type Client',540,1240,32,WHITE,True,center=True)
        return im
    if k==4:
        requested=at('query',0);candidates=at('candidates',requested+.12);failure=at('failure',requested+.30)
        im=base(k,'TWO MATCHES · NO PRIMARY',['Names do not','break this tie.'])
        query(im,'getBean(Client.class)',625,'TYPE-ONLY REQUEST')
        context_frame(im,(120,815,960,1133),'CONTEXT REMAINS READY',factory=False)
        txt(im,'"alpha"',145,895,35,PURPLE,True,mono=True)
        txt(im,'"beta"',635,895,35,PURPLE,True,mono=True)
        client(im,'alpha',145,950,300,132);client(im,'beta',635,950,300,132)
        if t>=requested:
            arrow(im,(935,758),(935,939),reveal(t,requested,.25),CYAN,4)
        if t>=candidates:
            line(im,[(295,946),(295,941),(785,941),(785,946)],RED,4)
            txt(im,'2 Client candidates',540,1093,28,RED,True,center=True)
        if t>=failure:
            box(im,(120,1171,960,1308),fill='#301d2c',outline=RED,r=18)
            txt(im,'EXPECTED LOOKUP FAILURE',145,1182,26,RED,True)
            txt(im,'NoUniqueBeanDefinitionException',145,1237,35,WHITE,mono=True)
        return im
    if k==5:return recap_scene(u,t,recap,duration,cues)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',4))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};proof_cues=proof_cues or {};duration=scene_duration or 9;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(proof_cues.get(key,cues.get(key,default)))
    named=at('named',.2);typed=at('type',1.2);takeaway=at('takeaway',2.0);complete=at('complete',4)
    im=base(5,'ACTUAL LOOKUP TESTS',['Names identify.','Types match.'])
    box(im,(120,625,960,790),fill='#112532',outline=GREEN,r=19)
    if t>=named:
        txt(im,'named alpha: alpha',145,637,35,GREEN,mono=True)
        txt(im,'named beta: beta',145,688,35,GREEN,mono=True)
    if t>=typed:txt(im,'type candidates: 2',145,739,35,GREEN,mono=True)
    box(im,(120,823,960,909),fill=CARD,outline=PURPLE,r=18)
    txt(im,'"alpha" + "beta" : Client',540,844,36,PURPLE,mono=True,center=True)
    if t>=takeaway:
        arrow(im,(315,913),(315,935),reveal(t,takeaway,.25),PURPLE,4)
        arrow(im,(765,913),(765,935),reveal(t,takeaway,.25),PURPLE,4)
        box(im,(120,943,520,1106),fill=CARD,outline=CYAN,r=18)
        txt(im,'BY NAME',145,958,28,CYAN,True)
        txt(im,'"alpha"',320,1015,39,WHITE,mono=True,center=True)
        box(im,(560,943,960,1106),fill=CARD,outline=CYAN,r=18)
        txt(im,'TYPE ONLY',585,958,28,CYAN,True)
        txt(im,'Client.class',760,1015,37,WHITE,mono=True,center=True)
    if t>=complete:
        arrow(im,(320,1110),(320,1146),1,GREEN,4);arrow(im,(760,1110),(760,1146),1,RED,4)
        box(im,(120,1155,520,1308),fill='#183a31',outline=GREEN,r=18)
        txt(im,'SELECTS ALPHA',320,1175,28,GREEN,True,center=True)
        txt(im,'Client',320,1224,42,WHITE,True,center=True)
        box(im,(560,1155,960,1308),fill='#301d2c',outline=RED,r=18)
        txt(im,'2 matches · no primary',760,1169,26,WHITE,True,center=True)
        txt(im,'AMBIGUOUS',760,1230,32,RED,True,center=True)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.45;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5)
    return im

def mechanism_anchors(data):
    c=data['scene_cues_absolute'];r=c['registration'];n=c['named'];s=c['single'];b=c['second'];a=c['ambiguity']
    return {'registration_s':float(r.get('definition',r['name'])),'name_assigned_s':float(r['name']),
            'first_instance_s':float(r['instance']),'named_request_s':float(n['request']),
            'named_return_s':float(n['return']),'typed_name_check_s':float(n['check']),
            'single_type_lookup_s':float(s['lookup']),'single_type_return_s':float(s['return']),
            'second_registration_s':float(b['register']),'second_instance_s':float(b['instance']),
            'two_instances_complete_s':float(b['instance'])+.35,
            'ambiguous_query_s':float(a['query']),'ambiguity_s':float(a['failure'])}
def graph_ready_at(data):return mechanism_anchors(data)['two_instances_complete_s']
def application_use_start(data):return mechanism_anchors(data)['ambiguous_query_s']
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
    key={1:'registration',2:'named',3:'single',4:'ambiguity',5:'proof'}.get(k)
    stage={key:val-s['start'] for key,val in data.get('scene_cues_absolute',{}).get(key,{}).items()}
    if k==3:
        stage.update({'second_'+key:val-s['start'] for key,val in data.get('scene_cues_absolute',{}).get('second',{}).items()})
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
