#!/usr/bin/env python3
"""Original native-resolution Pillow animation of Spring constructor-cycle detection and acyclic orchestration.

Cover and source frame0 share the exact same composition. Inter axes, measured
RGBA captions and opening motion are recorded for reproducible QA.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, hashlib, json, math, subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'source/assets'
W,H,FPS=1080,1920,60
NAVY='#090F20';WHITE='#FFFFFF';BLUE='#0866FF';CYAN='#5CDDFA';PURPLE='#B397FF';GREEN='#94E568';RED='#FF7D91';MUTED='#ADBCD2';CARD='#112137';EDGE='#2B3F5D'
HOOK="These two services can't finish starting."
FONTS={};TEXT_BOUNDS=[];CAPTION_LAYOUTS=[]
CAPTION_REGION=[90,1295,990,1505]
HEADLINE_ROI=[100,450,990,915]
TECHNICAL_ROI=[100,930,980,1275]

def font(size,bold=False,mono=False,weight=None):
    weight=weight or (800 if bold else 500)
    key=(size,mono,weight)
    if key not in FONTS:
        f=ImageFont.truetype(str(ASSETS/('DejaVuSansMono.ttf' if mono else 'Inter-Variable.ttf')),size)
        if not mono:f.set_variation_by_axes([32,weight])
        FONTS[key]=f
    return FONTS[key]

def txt(im,s,x,y,size=44,color=WHITE,bold=False,mono=False,center=False,weight=None):
    d=ImageDraw.Draw(im);f=font(size,bold,mono,weight)
    if center:x-=d.textlength(s,font=f)/2
    x,y=round(x),round(y);b=d.textbbox((x,y),s,font=f)
    TEXT_BOUNDS.append({'text':s,'bbox':list(b),'size':size,'weight':weight or(800 if bold else 500)})
    d.text((x,y),s,font=f,fill=color)

def lines(im,items,x,y,size=44,color=WHITE,bold=False,mono=False,gap=1.2,center=False,weight=None):
    for i,s in enumerate(items):txt(im,s,x,y+i*size*gap,size,color,bold,mono,center,weight)
def box(im,xy,fill=CARD,outline=EDGE,r=20,width=2):ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,xy)),r,fill,outline,width)
def line(im,pts,color=CYAN,width=4):ImageDraw.Draw(im).line(pts,fill=color,width=width,joint='curve')
def ease(v):v=max(0,min(1,v));return v*v*(3-2*v)
def reveal(t,start,duration=.25):return ease((t-start)/duration)
def arrow(im,a,b,p=1,color=CYAN,width=5):
    p=max(0,min(1,p));e=(a[0]+(b[0]-a[0])*p,a[1]+(b[1]-a[1])*p);line(im,[a,e],color,width)
    if p>.01:
        angle=math.atan2(b[1]-a[1],b[0]-a[0]);n=13
        line(im,[(e[0]-n*math.cos(angle-.55),e[1]-n*math.sin(angle-.55)),e,(e[0]-n*math.cos(angle+.55),e[1]-n*math.sin(angle+.55))],color,width)
def check(im,x,y,color=GREEN):line(im,[(x-12,y),(x-3,y+12),(x+15,y-14)],color,5)

def make_bg():
    yy,xx=np.mgrid[0:H,0:W];glow=np.exp(-(((xx-800)/780)**2+((yy-1000)/1000)**2));a=np.zeros((H,W,3),np.uint8)
    for k,(b,v) in enumerate(zip((9,15,32),(4,8,15))):a[:,:,k]=b+v*glow
    im=Image.fromarray(a);d=ImageDraw.Draw(im)
    for x in range(90,1000,90):d.line((x,920,x,1290),fill='#15253D',width=1)
    for y in range(940,1290,70):d.line((90,y,990,y),fill='#15253D',width=1)
    return im
BG=make_bg()

def caption_layout(text):
    size=52;weight=700;f=font(size,weight=weight);d=ImageDraw.Draw(BG);rows=[];row=''
    if text==HOOK:
        # Coherent balanced wrapping, retaining the exact complete spoken cue.
        rows=["These two services", "can't finish starting."]
    else:
        for word in text.split():
            candidate=(row+' '+word).strip();b=d.textbbox((0,0),candidate,font=f)
            if b[2]-b[0]>788 and row:rows.append(row);row=word
            else:row=candidate
        if row:rows.append(row)
    if len(rows)>2:raise ValueError(('Caption needs shorter phrase',text,rows))
    dims=[d.textbbox((0,0),s,font=f) for s in rows]
    widths=[b[2]-b[0] for b in dims];heights=[b[3]-b[1] for b in dims]
    if max(widths,default=0)>788:raise ValueError(('Caption word too wide',text))
    gap=10;content_h=sum(heights)+gap*(len(rows)-1);rw=max(widths,default=0)+52;rh=content_h+28
    left=round(540-rw/2);top=round(1380-rh/2);rect=[left,top,left+rw,top+rh]
    bounds=[];origins=[];y=top+14
    for s,b,w,h in zip(rows,dims,widths,heights):
        x=round(540-w/2);bounds.append([x,y,x+w,y+h]);origins.append([x-b[0],y-b[1]]);y+=h+gap
    result={'text_lines':rows,'text_bounds':bounds,'rect':rect,'origins':origins,'font_size':size,'weight':weight,'opacity':.82,'alpha':209,'padding':[26,14],'corner_radius':12,'max_width':840,'center':[540,1380]}
    if not(90<=rect[0]<rect[2]<=990 and 250<=rect[1]<rect[3]<=1520):raise ValueError(('Unsafe caption',text,result))
    return result

def caption(im,text):
    layout=caption_layout(text);overlay=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(overlay)
    d.rounded_rectangle(tuple(layout['rect']),12,fill=(0,0,0,209))
    f=font(52,weight=700)
    for s,origin,b in zip(layout['text_lines'],layout['origins'],layout['text_bounds']):
        d.text(tuple(origin),s,font=f,fill=(255,255,255,255));TEXT_BOUNDS.append({'text':s,'bbox':b,'size':52,'weight':700,'caption':True})
    im.paste(Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB'))
    CAPTION_LAYOUTS.append({'text':text,**layout})
    return layout

def base(title):
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    lines(im,title,110,422,64,WHITE,True,gap=1.08)
    return im

def context(im,xy=(110,900,970,1268),ready=False):
    box(im,xy,fill='#0C1D30',outline=PURPLE,r=23,width=2)
    x,y,x2,y2=xy;txt(im,'SPRING CONTAINER',x+24,y+15,30,PURPLE,True)
    if ready:txt(im,'READY',x2-136,y+18,28,GREEN,True)

def node(im,title,x,y,w=340,h=135,sub=None,color=GREEN,size=40):
    box(im,(x,y,x+w,y+h),fill='#16352E' if color==GREEN else '#17253E',outline=color,r=18,width=3)
    txt(im,title,x+w/2,y+18,size,color,True,center=True)
    if sub:txt(im,sub,x+w/2,y+h-40,28,WHITE,center=True)

def code_run(im,runs,x,y,size=36):
    d=ImageDraw.Draw(im);f=font(size,mono=True)
    for s,color in runs:
        txt(im,s,x,y,size,color,mono=True);x+=d.textlength(s,font=f)



def pending(im,label,x,y,sub='constructor pending',color=PURPLE):
    node(im,label,x,y,350,145,sub,color,43)

def loop(im,y=970,t=0):
    pending(im,'ServiceA',130,y,'needs ServiceB')
    pending(im,'ServiceB',600,y,'needs ServiceA')
    arrow(im,(490,y+45),(590,y+45),1,CYAN)
    line(im,[(775,y+150),(775,y+200),(305,y+200),(305,y+155)],RED,5)
    arrow(im,(305,y+190),(305,y+155),1,RED)
    x=493+85*((t/.8)%1);ImageDraw.Draw(im).ellipse((x,y+38,x+10,y+48),fill=WHITE)

def cover_base(t=0):
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    d=ImageDraw.Draw(im);f=font(96,weight=900)
    for j,s in enumerate(['Why Spring','Fails With','Circular','Dependencies']):
        x=128 if j==2 else 110;y=435+j*117;b=d.textbbox((x,y),s,font=f)
        if j==2:box(im,(b[0]-18,b[1]-8,b[2]+18,b[3]+8),BLUE,None,20)
        txt(im,s,x,y,96,WHITE,weight=900)
    txt(im,'CONSTRUCTOR CREATION CYCLE',130,930,32,RED,True)
    loop(im,990,t)
    return im

def cover():
    im=cover_base();caption(im,HOOK);return im

def graph(im,progress=1):
    node(im,'Orchestrator',270,650,540,135,'calls both services',PURPLE,49)
    if progress>.2:
        arrow(im,(400,805),(305,960),1,CYAN);pending(im,'ServiceA',130,980,'no B constructor input',GREEN)
    if progress>.45:
        arrow(im,(680,805),(775,960),1,CYAN);pending(im,'ServiceB',600,980,'no A constructor input',GREEN)
    if progress>.7:txt(im,'No dependency edge between A and B',110,1190,39,GREEN,True)

def render_frame(t,data,with_caption=True):
    idx=next((i for i,s in enumerate(data['scenes']) if s['start']<=t<s['end']),6)
    sc=data['scenes'][idx];u=(t-sc['start'])/(sc['end']-sc['start'])
    if t<2:
        im=cover_base(t)
        if t>1:
            p=ease(t-1);im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
            old=Image.new('RGBA',(W,H),(0,0,0,0));old.paste(cover_base(t).crop((90,420,990,915)),(90,420));old.putalpha(old.getchannel('A').point(lambda a:round(a*(1-ease((t-1)/.45)))));im=Image.alpha_composite(im.convert('RGBA'),old).convert('RGB')
            if t>=1.5:
                layer=Image.new('RGBA',(W,H),(0,0,0,0));lines(layer,['Creating A requires B.'],110,422,64,WHITE,True);layer.putalpha(layer.getchannel('A').point(lambda a:round(a*ease((t-1.5)/.5))));im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
            loop(im,990-280*p,t)
    elif idx==1:
        im=base(['Creating A requires B.'])
        box(im,(110,620,970,840),outline=CYAN)
        txt(im,'ServiceA(ServiceB b)',140,660,48,CYAN,mono=True)
        txt(im,'resolve constructor argument first',140,750,37,WHITE)
        pending(im,'ServiceA',130,1000,'IN CREATION',PURPLE)
        if u>.2:
            arrow(im,(490,1070),(590,1070),min(1,u*3));pending(im,'ServiceB',600,1000,'requested',CYAN)
        txt(im,'No completed A instance yet',140,1220,40,WHITE,True)
    elif idx==2:
        im=base(['B requires A first.','Neither can finish.'])
        box(im,(110,620,970,840),outline=CYAN)
        txt(im,'ServiceB(ServiceA a)',140,660,48,CYAN,mono=True)
        txt(im,'A is already being created',140,750,40,RED,True)
        loop(im,970,0)
        if u>.45:txt(im,'CREATION PATH: A → B → A',130,1220,40,RED,True)
    elif idx==3:
        im=base(['Constructor cycle.','Startup fails.'])
        loop(im,650,0)
        if u>.1:
            box(im,(110,950,970,1260),outline=RED)
            txt(im,'ACTUAL NESTED EXCEPTION',140,975,32,RED,True)
            txt(im,'UnsatisfiedDependencyException',140,1040,35,WHITE,mono=True)
            txt(im,'caused by',140,1110,34,MUTED)
            txt(im,'BeanCurrentlyInCreationException',140,1170,35,RED,mono=True)
    elif idx==4:
        im=base(['Move coordination out.','Remove the cycle.'])
        txt(im,'FRESH ACYCLIC CONTEXT',110,565,32,PURPLE,True)
        graph(im,u*1.6)
    elif idx==5:
        im=base(['Verified: fails → starts.','Redesign the graph.'])
        if u<.5:
            box(im,(110,650,970,1110),outline=GREEN)
            txt(im,'ACTUAL JUNIT RESULTS',140,675,34,GREEN,True)
            for j,s in enumerate(['Constructor cycle: failed','Acyclic context: started','Managed references: same','Execution: A then B']):
                if u>j*.08:txt(im,s,140,760+j*77,42,WHITE,True)
        else:
            node(im,'App: register Acyclic',160,620,760,115,'refresh()',PURPLE,42)
            arrow(im,(540,745),(540,800),1,CYAN)
            node(im,'Spring creates A and B',160,810,760,130,'no mutual constructor inputs',GREEN,42)
            arrow(im,(540,950),(540,1005),1,CYAN)
            node(im,'Orchestrator(A, B)',160,1015,760,135,'same managed references',GREEN,46)
        txt(im,'Other circular references differ.',110,1240,38,WHITE,True)
    else:
        im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
        lines(im,['Thanks for','watching.'],540,765,88,WHITE,True,center=True)
        line(im,[(315,1010),(315+450*min(1,u*4),1010)],CYAN,5)
    if with_caption:
        c=next((c for c in data['captions'] if c['start']<=t<c['end']),None)
        if c:caption(im,c['text'])
    return im
def main():
    data=json.loads((ROOT/'source/timing.json').read_text());cover().save(ROOT/'cover.png')
    thumbs=[];TEXT_BOUNDS.clear()
    for t in np.linspace(0,data['duration']-1/60,250):
        im=render_frame(float(t),data)
    bad=[b for b in TEXT_BOUNDS if b['bbox'][0]<90 or b['bbox'][1]<250 or b['bbox'][2]>990 or b['bbox'][3]>1520]
    (ROOT/'source/evidence/layout-preflight.json').write_text(json.dumps({'samples':250,'violations':bad},indent=2))
    assert not bad,bad
    for i,s in enumerate(data['scenes']):
        im=render_frame(s['start']+(s['end']-s['start'])*.85,data);im.save(ROOT/f'qa/scene-{i}.png');thumbs.append(im.resize((270,480)))
    contact=Image.new('RGB',(1080,960),NAVY)
    for i,im in enumerate(thumbs):contact.paste(im,(i%4*270,i//4*480))
    contact.save(ROOT/'qa/mobile-preview.png')
    if '--render' not in __import__('sys').argv:return
    count=math.ceil(data['duration']*FPS)
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','60','-i','pipe:0','-i',str(ROOT/'source/animation/mix.wav'),'-vf','scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-color_range','tv','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(count/60),'-movflags','+faststart',str(ROOT/'video.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(count):
        p.stdin.write(render_frame(n/60,data).tobytes())
        if n%600==0:print(n,count,flush=True)
    p.stdin.close();assert p.wait()==0
if __name__=='__main__':main()
