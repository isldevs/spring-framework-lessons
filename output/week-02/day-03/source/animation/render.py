#!/usr/bin/env python3
"""Original native-resolution Pillow animation of Spring dependency resolution.

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
HOOK="What if this Spring bean doesn't exist?"
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
        rows=['What if this Spring bean',"doesn't exist?"]
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


def code(im,optional=False,y=920):
    box(im,(110,y,970,y+215),outline=CYAN)
    txt(im,'Service(',140,y+20,42,WHITE,mono=True)
    txt(im,'Optional<AuditPublisher>' if optional else 'AuditPublisher audit',140,y+85,42,CYAN,mono=True)
    txt(im,' audit)' if optional else ')',140,y+145,38,WHITE,mono=True)

def cover_base(t=0):
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    f=font(104,weight=900);d=ImageDraw.Draw(im)
    for j,s in enumerate(['Missing Bean?','Spring Can','Still Start']):
        x=128 if j==0 else 110;y=475+j*151;b=d.textbbox((x,y),s,font=f)
        if j==0:box(im,(b[0]-18,b[1]-8,b[2]+18,b[3]+8),BLUE,None,20)
        txt(im,s,x,y,104,WHITE,weight=900)
    box(im,(110,945,970,1260),outline=CYAN)
    txt(im,'Optional<AuditPublisher>',140,970,43,CYAN,mono=True)
    txt(im,'no candidate',150,1070,40,MUTED)
    arrow(im,(450,1100),(580,1100))
    txt(im,'empty',625,1070,48,GREEN,True)
    x=455+110*((t/.85)%1);ImageDraw.Draw(im).ellipse((x,1093,x+12,1105),fill=WHITE)
    txt(im,'CONTEXT CAN START',145,1180,39,GREEN,True)
    return im

def cover():
    im=cover_base();caption(im,HOOK);return im

def render_frame(t,data,with_caption=True):
    idx=next((i for i,s in enumerate(data['scenes']) if s['start']<=t<s['end']),6)
    sc=data['scenes'][idx];u=(t-sc['start'])/(sc['end']-sc['start'])
    if t<2:
        im=cover_base(t)
        if t>1:
            p=ease(t-1);im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
            old=Image.new('RGBA',(W,H),(0,0,0,0));old.paste(cover_base(t).crop((90,450,990,915)),(90,450));old.putalpha(old.getchannel('A').point(lambda a:round(a*(1-ease((t-1)/.45)))))
            im=Image.alpha_composite(im.convert('RGBA'),old).convert('RGB')
            if t>=1.5:
                layer=Image.new('RGBA',(W,H),(0,0,0,0));lines(layer,['A required dependency','blocks startup.'],110,422,64,WHITE,True,gap=1.08);layer.putalpha(layer.getchannel('A').point(lambda a:round(a*ease((t-1.5)/.5))));im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
            y=945-295*p;h=315-100*p;box(im,(110,y,970,y+h),outline=CYAN)
            if p<.5:
                txt(im,'Optional<AuditPublisher>',140,y+25,43,CYAN,mono=True)
                txt(im,'no candidate → empty',145,y+120,42,GREEN,True)
            else:
                txt(im,'Service(',140,y+20,42,WHITE,mono=True)
                txt(im,'AuditPublisher audit',140,y+85,42,CYAN,mono=True)
                txt(im,')',140,y+145,38,WHITE,mono=True)
    elif idx==1:
        im=base(['A required dependency','blocks startup.']);code(im,False,650)
        txt(im,'REQUIRED LOOKUP',140,940,34,PURPLE,True)
        arrow(im,(540,890),(540,1000),min(1,u*3))
        txt(im,'AuditPublisher: 0 candidates',140,1030,37,CYAN,mono=True)
        if u>.4:
            box(im,(110,1140,970,1260),outline=RED)
            txt(im,'REFRESH FAILED',145,1165,46,RED,True)
    elif idx==2:
        im=base(['Make absence explicit.']);code(im,True,650)
        txt(im,'Spring resolves the nested type',140,970,41,WHITE,True)
        txt(im,'AuditPublisher',140,1045,48,CYAN,mono=True)
        arrow(im,(540,1120),(540,1190),min(1,u*3))
        if u>.4:txt(im,'0 candidates → Optional.empty()',140,1210,36,GREEN,mono=True)
    elif idx==3:
        im=base(['Present: wrap the','managed reference.'])
        node(im,'AuditPublisher',170,660,740,130,'one managed instance',PURPLE,48)
        arrow(im,(540,810),(540,935),min(1,u*3))
        if u>.2:
            box(im,(110,950,970,1240),outline=GREEN)
            txt(im,'Optional.of(publisher)',140,980,43,GREEN,mono=True)
            txt(im,'Service receives the same object',140,1070,40,WHITE,True)
            if u>.6:txt(im,'notifyIfPresent() → publish()',140,1160,36,CYAN,mono=True)
    elif idx==4:
        im=base(['Absent: empty value.','Service still starts.'])
        box(im,(110,650,970,850),outline=PURPLE);txt(im,'FRESH CONTEXT',140,675,32,PURPLE,True)
        txt(im,'AuditPublisher: no bean',140,750,43,WHITE,mono=True)
        arrow(im,(540,880),(540,980),min(1,u*3))
        if u>.2:
            node(im,'Optional.empty()',130,1000,820,145,'notification skipped',GREEN,52)
        if u>.6:txt(im,'CONTEXT READY',140,1200,43,GREEN,True)
    elif idx==5:
        im=base(['Absence is allowed.','Ambiguity can still fail.'])
        if u<.6:
            box(im,(110,650,970,1100),outline=GREEN)
            txt(im,'ACTUAL JUNIT RESULTS',140,675,32,GREEN,True)
            for j,s in enumerate(['Required absent: fails','Optional absent: empty','Optional present: same','Ambiguous: fails']):
                if u>j*.10:txt(im,s,145,760+j*77,42,WHITE,True)
        else:
            for j,(title,sub) in enumerate([('App: register Config','refresh() starts resolution'),('Spring: AuditPublisher','one → present / none → empty'),('Service receives Optional','handle present or skip extra work')]):
                y=650+j*190;node(im,title,110,y,860,145,sub,GREEN if j==2 else PURPLE,40)
                if j<2:arrow(im,(540,y+150),(540,y+180))
        txt(im,'Keep security dependencies required.',110,1240,37,WHITE,True)
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
