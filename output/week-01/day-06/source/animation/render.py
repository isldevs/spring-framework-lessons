#!/usr/bin/env python3
"""Original Pillow animation: independent Spring registries and named lookup fallback.

Frames are rendered at native1080x1920/60FPS using final Kokoro/ASR edit timing.
The parent instance never moves into or gets copied into the child's registry.
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
def registry(im,xy,label,sub='LOCAL DEMO BEANS'):
    box(im,xy,fill='#0d1d2d',outline=PURPLE,r=23,width=2);x,y,x2,y2=xy
    txt(im,label,x+22,y+14,36,PURPLE,True);txt(im,sub,x+22,y+66,25,MUTED,True)
def item(im,name,x,y,w=318,h=120):
    box(im,(x,y,x+w,y+h),fill='#183a31',outline=GREEN,r=17,width=3)
    txt(im,'"'+name+'"',x+w/2,y+12,40,GREEN,True,mono=True,center=True)
    txt(im,'Item instance',x+w/2,y+h-38,27,WHITE,center=True)
def definition(im,name,x,y,w=318,h=112):
    d=ImageDraw.Draw(im);fold=24
    d.polygon([(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)],fill='#171d36',outline=PURPLE,width=2)
    line(im,[(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)],PURPLE,2)
    txt(im,'@Bean("'+name+'")',x+15,y+13,29,PURPLE,mono=True);txt(im,'bean definition',x+15,y+65,27,WHITE)
def query(im,s,y=625,label='APP · NAMED LOOKUP',color=CYAN):
    box(im,(120,y,960,y+123),fill=CARD,outline=color,r=18)
    txt(im,label,144,y+9,25,color,True);txt(im,s,144,y+58,36,WHITE,mono=True)
def missing(im,s,x,y,w=318):
    box(im,(x,y,x+w,y+72),fill='#301d2c',outline=RED,r=13,width=2)
    txt(im,s,x+15,y+15,30,RED,True);cross(im,x+w-28,y+36)
def columns(im,y=790,bottom=1212):
    registry(im,(120,y,510,bottom),'CONTEXT A');registry(im,(570,y,960,bottom),'CONTEXT B')
def paired_items(im,y=925):item(im,'alpha',155,y);item(im,'beta',605,y)

def hook_scene(t,with_motion=True):
    im=base(0,'MULTIPLE CONTEXTS',['Two contexts.','Different beans?'])
    columns(im,650,1085);paired_items(im,780)
    txt(im,'getBean("alpha")',315,933,29,CYAN,mono=True,center=True)
    txt(im,'getBean("alpha")',765,933,29,CYAN,mono=True,center=True)
    check(im,315,1022);cross(im,765,1022)
    box(im,(120,1130,960,1308),fill=CARD,outline=EDGE,r=18)
    txt(im,'SAME REQUEST',540,1151,29,CYAN,True,center=True)
    txt(im,'Different local registries',540,1205,43,WHITE,True,center=True)
    if with_motion:
        # A purposeful lookup pulse is already moving at frame1.
        p=(t/.85)%1
        for x in [315,765]:
            y=923-20*p;ImageDraw.Draw(im).ellipse((x-8,y-8,x+8,y+8),fill=CYAN)
        line(im,[(135+350*p,1072),(min(495,170+350*p),1072)],GREEN,4)
    return im
def cover():return hook_scene(0,False)
COVER=cover()

def hierarchy(im,parent_y=795,child_y=1078,h=214,child_ready=True):
    registry(im,(120,parent_y,960,parent_y+h),'PARENT')
    txt(im,'ParentConfig',145,parent_y+122,29,WHITE,mono=True)
    item(im,'shared',610,parent_y+67,320,122)
    registry(im,(120,child_y,960,child_y+h),'CHILD')
    txt(im,'ChildConfig',145,child_y+105,29,WHITE,mono=True)
    if child_ready:item(im,'local',610,child_y+67,320,122)
    else:definition(im,'local',610,child_y+67,320,122)

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or [1.8,7.1,6.4,6.2,4.8,9.5,1.4][k];t=u*duration if elapsed is None else elapsed;cues=scene_cues or {}
    at=lambda key,default:float(cues.get(key,default))
    if k==0:return hook_scene(t)
    if k==1:
        a=at('alpha',.9);b=at('beta',2.1);ready=at('registry',3.5)
        im=base(k,'INDEPENDENT CONTEXTS',['Register each bean','in its own context.'])
        box(im,(120,625,960,797),fill=CARD,outline=CYAN,r=18)
        txt(im,'APP STARTUP',145,636,25,CYAN,True)
        # Each registration is followed by that context's refresh before its instance appears.
        owner,config=('a','AConfig') if t<b else ('b','BConfig')
        txt(im,f'{owner}.register({config}.class);',145,686,34,WHITE,mono=True)
        txt(im,f'{owner}.refresh();',145,736,34,GREEN,mono=True)
        columns(im,835,1308)
        if t>=a:definition(im,'alpha',155,940)
        if t>=b:definition(im,'beta',605,940)
        if t>=a+.35:
            arrow(im,(314,1057),(314,1100),reveal(t,a+.35,.3),CYAN,4);item(im,'alpha',155,1113)
        if t>=b+.35:
            arrow(im,(764,1057),(764,1100),reveal(t,b+.35,.3),CYAN,4);item(im,'beta',605,1113)
        if t>=ready:
            txt(im,'ONLY A',315,1251,28,GREEN,True,center=True);txt(im,'ONLY B',765,1251,28,GREEN,True,center=True)
        return im
    if k==2:
        request=at('request',0);found=at('found',.35);beta=at('beta',1.0);miss=at('missing',beta+.3)
        im=base(k,'NO PARENT LINK',['Same app.','Separate registries.'])
        query(im,'a.getBean("alpha")' if t<beta else 'a.getBean("beta")')
        columns(im,800,1210);paired_items(im,913)
        if t<beta:
            if t>=request:
                # Enter through the right-side gutter, clear of the context heading.
                line(im,[(489,752),(489,899)],CYAN,4)
                arrow(im,(489,899),(459,911),reveal(t,request,.25),CYAN,4)
            if t>=found:tag(im,'FOUND ALPHA',155,1084,GREEN,25)
        else:
            if t>=beta:
                line(im,[(489,752),(489,1066)],CYAN,4)
                arrow(im,(489,1066),(459,1078),reveal(t,beta,.25),CYAN,4)
            if t>=miss:missing(im,'beta: missing',155,1080)
            txt(im,'beta stays in B',765,1097,29,GREEN,True,center=True)
        if t>=miss:tag(im,'NO CROSS-CONTEXT SEARCH',228,1242,RED,28)
        return im
    if k==3:
        setting=at('set',1.2);refresh=at('refresh',3.4)
        im=base(k,'FRESH PARENT + CHILD',['Link the parent','before child refresh.'])
        box(im,(120,625,960,773),fill=CARD,outline=PURPLE,r=18)
        txt(im,'child.setParent(parent);',145,638,36,CYAN if t>=setting else MUTED,mono=True)
        txt(im,'child.refresh();',145,705,36,GREEN if t>=refresh else MUTED,mono=True)
        hierarchy(im,810,1090,208,t>=refresh)
        if t>=setting:
            arrow(im,(500,1085),(500,1028),reveal(t,setting,.3),CYAN,5)
            txt(im,'parent link',558,1037,28,CYAN,True)
        if t>=refresh:check(im,884,726)
        return im
    if k==4:
        local=at('local',.15);miss=at('missing',1.2);parent=at('parent',2.8);returned=at('return',parent+.35)
        im=base(k,'NAMED LOOKUP FALLBACK',['Child checks local,','then its parent.'])
        query(im,'child.getBean("shared")')
        hierarchy(im,792,1076,212,True)
        if t>=local:
            box(im,(145,1227,545,1273),fill='#122b3a',outline=CYAN,r=9)
            txt(im,'shared? check local',160,1229,26,CYAN,True)
        if t>=miss:
            box(im,(145,1227,545,1273),fill='#301d2c',outline=RED,r=9)
            txt(im,'shared not local',160,1229,26,RED,True)
        if t>=parent:
            arrow(im,(505,1072),(505,1009),reveal(t,parent,.25),CYAN,5)
            txt(im,'fallback',555,1023,28,CYAN,True)
            box(im,(605,854,935,985),fill=None,outline=CYAN,r=20,width=4)
        if t>=returned:
            # Only a reference returns. The green instance remains in the parent.
            arrow(im,(930,850),(930,754),reveal(t,returned,.25),GREEN,5)
            txt(im,'same parent instance',145,752,28,GREEN,True)
        return im
    if k==5:return recap_scene(u,t,recap,duration,cues)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',7.5))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};pc=proof_cues or {};duration=scene_duration or 9.5;t=u*duration if elapsed is None else elapsed
    at=lambda key,default:float(pc.get(key,cues.get(key,default)))
    reverse=at('reverse',0);miss=at('missing',.4);tests=at('tests',1.7);up=at('upward',3.8);down=at('downward',5.3);complete=at('complete',duration-2)
    im=base(5,'VERIFIED NAMED LOOKUPS',['Child can look up.','Parent cannot look down.'])
    # The completed diagram retains every boundary and instance during its reading hold.
    registry(im,(120,625,960,819),'PARENT');item(im,'shared',610,679,320,116)
    txt(im,'local? missing',145,748,31,RED if t>=miss else MUTED,True)
    registry(im,(120,926,960,1120),'CHILD');item(im,'local',610,980,320,116)
    txt(im,'own local registry',145,1049,28,WHITE)
    if t<tests:
        box(im,(120,1164,960,1308),fill=CARD,outline=CYAN,r=18)
        txt(im,'PARENT REQUEST',145,1177,26,CYAN,True)
        txt(im,'parent.getBean("local")',145,1233,35,WHITE,mono=True)
        if t>=reverse:
            # This query belongs to the parent: bypass the child entirely.
            line(im,[(120,1223),(106,1223),(106,725)],CYAN,4)
            arrow(im,(106,725),(122,725),reveal(t,reverse,.25),CYAN,4)
        if t>=miss:cross(im,565,783)
    else:
        box(im,(120,1164,960,1308),fill='#112532',outline=GREEN,r=18)
        txt(im,'ACTUAL JAVA RESULTS',145,1172,24,GREEN,True)
        txt(im,'child shared same: true',145,1213,34,GREEN,mono=True)
        txt(im,'parent local: missing',145,1261,34,WHITE,mono=True)
    if t>=up:
        arrow(im,(314,920),(314,826),reveal(t,up,.25),GREEN,5)
        txt(im,'child → parent',370,839,31,GREEN,True)
        txt(im,'named fallback',370,879,26,WHITE)
    if t>=down:
        line(im,[(874,825),(874,916)],RED,4);cross(im,874,872)
        txt(im,'no reverse',145,868,28,RED,True)
    if t>=complete:
        check(im,910,1193)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.4;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',100,264,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,760,88,WHITE,True,center=True,gap=1.16)
    line(im,[(320,1008),(320+440*reveal(t,0,.38),1008)],CYAN,5);return im

def mechanism_anchors(data):
    c=data.get('scene_cues_absolute',{});s=data['scenes']
    r=c.get('registration',{});i=c.get('isolation',{});l=c.get('link',{});f=c.get('fallback',{});p=c.get('proof',{})
    return {'independent_registration_s':float(r.get('alpha',s[1]['start']+.9)),
    'local_lookup_s':float(i.get('request',s[2]['start'])),
    'independent_missing_s':float(i.get('missing',s[2]['start']+1.3)),
    'parent_set_s':float(l.get('set',s[3]['start']+1.2)),
    'child_refresh_s':float(l.get('refresh',s[3]['start']+3.4)),
    'child_local_check_s':float(f.get('local',s[4]['start']+.15)),
    'parent_fallback_s':float(f.get('parent',s[4]['start']+2.8)),
    'parent_return_s':float(f.get('return',s[4]['start']+3.15)),
    'reverse_lookup_s':float(p.get('reverse',s[5]['start'])),
    'reverse_missing_s':float(p.get('missing',s[5]['start']+.4)),
    'recap_complete_s':float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))}
def graph_ready_at(data):return mechanism_anchors(data)['child_refresh_s']+.3
def application_use_start(data):return mechanism_anchors(data)['child_local_check_s']
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
    key={1:'registration',2:'isolation',3:'link',4:'fallback',5:'proof'}.get(k)
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
        s=data['scenes'][-2];t=(data['recap_hold_start']+data['recap_hold_end'])/2;c={name:float(v)-s['start'] for name,v in data.get('scene_cues_absolute',{}).get('proof',{}).items() if isinstance(v,(int,float))};c['complete']=float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))-s['start']
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
