#!/usr/bin/env python3
"""Original native-resolution Pillow animation of implicit constructor injection.

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
HOOK='No Autowired? This still works.'
FONTS={};TEXT_BOUNDS=[];CAPTION_LAYOUTS=[]
CAPTION_REGION=[90,1295,990,1505]
HEADLINE_ROI=[100,450,990,905]
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

def ctor_card(im,y=625,highlight=False):
    box(im,(110,y,970,y+222),fill='#0B1A2E',outline=CYAN,r=22,width=2)
    code_run(im,[('@Service ',PURPLE),('class OrderService {',WHITE)],137,y+19,36)
    code_run(im,[('  OrderService(',WHITE)],137,y+80,38)
    code_run(im,[('    PaymentGateway',CYAN),(' gateway)',WHITE)],137,y+139,36)

def headline_geometry():
    d=ImageDraw.Draw(BG);items=[('Spring Injection',104,110,475),('No @Autowired?',96,128,626),('It still works.',104,110,777)];out=[]
    for s,size,x,y in items:
        b=d.textbbox((x,y),s,font=font(size,weight=900));out.append({'text':s,'size':size,'origin':[x,y],'bbox':list(b)})
    return out

def cover_headline(im,dy=0):
    geometry=headline_geometry();d=ImageDraw.Draw(im)
    for item in geometry:
        s=item['text'];x,y=item['origin'];y+=dy;b=list(item['bbox']);b[1]+=dy;b[3]+=dy
        if s=='No @Autowired?':box(im,(b[0]-18,b[1]-8,b[2]+18,b[3]+8),fill=BLUE,outline=None,r=20)
        txt(im,s,x,y,item['size'],WHITE,weight=900)

def cover_base(t=0):
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    cover_headline(im)
    node(im,'PaymentGateway',130,1180,360,95,None,CYAN,31)
    node(im,'OrderService',600,1180,350,95,None,PURPLE,34)
    arrow(im,(500,1228),(590,1228),1,CYAN,5)
    # The moving carrier is the dependency reference supplied to this constructor.
    p=(t/.85)%1;cx=503+83*p;ImageDraw.Draw(im).ellipse((cx-7,1221,cx+7,1235),fill=WHITE)
    return im

def cover():
    im=cover_base(0);ctor_card(im,940,True);caption(im,HOOK);return im

def managed_scene(elapsed,cues=None,draw_card=True):
    cues=cues or {};one=float(cues.get('one',1.4));select=float(cues.get('select',2.7));optional=float(cues.get('optional',5.2))
    im=base(['One constructor.','No @Autowired needed.'])
    if draw_card:ctor_card(im,625,elapsed>=one)
    context(im,(110,900,970,1268),False)
    box(im,(145,990,935,1124),fill='#17233E',outline=PURPLE,r=18,width=2)
    txt(im,'OrderService',175,1006,44,PURPLE,True)
    txt(im,'Spring-managed bean definition',175,1071,31,WHITE)
    if elapsed>=one:txt(im,'ONE CONSTRUCTOR',145,1164,34,CYAN,True)
    if elapsed>=select:check(im,887,1188)
    if elapsed>=optional:txt(im,'@Autowired is optional',145,1213,34,GREEN,True)
    return im

def opening_visual(t,data=None):
    start=cover_base(t)
    if t<=1:
        ctor_card(start,940,True);return start
    p=ease(t-1)
    cues={};elapsed=max(0,t-2)
    if data:
        s=data['scenes'][1];elapsed=t-s['start'];cues={k:float(v)-s['start'] for k,v in data.get('scene_cues_absolute',{}).get('managed',{}).items()}
    end=managed_scene(elapsed,cues,False)
    # Retire the thumbnail headline before revealing the smaller scene heading.
    # This avoids double-exposed words while the actual constructor card travels.
    band=(90,415,990,900)
    start.paste(BG.crop(band),band);end.paste(BG.crop(band),band)
    im=Image.blend(start,end,p)
    old_progress=ease((t-1)/.45);old_alpha=1-old_progress
    if old_alpha>0:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));cover_headline(overlay,-40*old_progress)
        overlay.putalpha(overlay.getchannel('A').point(lambda a:round(a*old_alpha)))
        im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    new_alpha=ease((t-1.5)/.5)
    if new_alpha>0:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));lines(overlay,['One constructor.','No @Autowired needed.'],110,422,64,WHITE,True,gap=1.08)
        overlay.putalpha(overlay.getchannel('A').point(lambda a:round(a*new_alpha)))
        im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    # One continuous constructor code element travels from thumbnail into explanation.
    ctor_card(im,940+(625-940)*p,True)
    return im

def hook_scene(t,with_motion=True):return opening_visual(t if with_motion else 0)
COVER=cover()

def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or[2,6,6,5,7,8,1.4][k];t=u*duration if elapsed is None else elapsed;c=scene_cues or {};at=lambda name,default:float(c.get(name,default))
    if k==0:return opening_visual(t)
    if k==1:return managed_scene(t,c)
    if k==2:
        parameter=at('parameter',.3);search=at('search',1.5);match=at('match',2.7)
        im=base(['Find the dependency','by its parameter type.'])
        box(im,(110,625,970,790),fill=CARD,outline=CYAN,r=20)
        txt(im,'CONSTRUCTOR PARAMETER',137,645,28,CYAN,True)
        code_run(im,[('PaymentGateway',CYAN),(' gateway',WHITE)],137,708,43)
        context(im,(110,848,970,1268))
        if t>=parameter:txt(im,'Matching bean candidates',145,920,34,WHITE,True)
        if t>=search:
            line(im,[(946,797),(946,1042)],CYAN,5);arrow(im,(946,1042),(929,1042),reveal(t,search,.3),CYAN,5)
            box(im,(145,985,925,1142),fill='#162D35',outline=CYAN if t<match else GREEN,r=20,width=3)
            txt(im,'DemoPaymentGateway',175,1000,42,GREEN if t>=match else CYAN,True)
            txt(im,'implements PaymentGateway',175,1074,31,WHITE,mono=True)
        if t>=match:check(im,880,1196);txt(im,'ONE MATCH',145,1175,38,GREEN,True)
        return im
    if k==3:
        supply=at('supply',.5);store=at('store',2.8);ready=at('ready',3.8)
        im=base(['Spring supplies it','through the constructor.'])
        box(im,(110,625,970,870),fill=CARD,outline=CYAN,r=20)
        lines(im,['OrderService(','  PaymentGateway gateway) {','  this.gateway = gateway;','}'],136,644,37,WHITE,mono=True,gap=1.36)
        if t>=store:line(im,[(180,802),(767,802)],GREEN,4)
        context(im,(110,918,970,1268),t>=ready)
        node(im,'Gateway',145,1033,330,160,'same instance',GREEN,44)
        if t>=supply:
            arrow(im,(485,1105),(570,1105),reveal(t,supply,.35),CYAN,5)
            node(im,'OrderService',580,1033,350,160,'constructor argument',GREEN,39)
        if t>=store:txt(im,'gateway field holds that reference',145,1210,31,GREEN,True)
        return im
    if k==4:
        call=at('call',.1);result=at('result',1.8);verify=at('verify',4.5)
        im=base(['An order uses','the injected gateway.'])
        box(im,(110,625,970,775),fill=CARD,outline=CYAN,r=20)
        txt(im,'APP CALL',138,644,29,CYAN,True);txt(im,'service.placeOrder(2500)',138,709,43,WHITE,mono=True)
        context(im,(110,823,970,1090),True)
        node(im,'OrderService',145,942,365,126,'service bean',GREEN,39)
        node(im,'Gateway',620,942,310,126,'injected instance',GREEN,42)
        if t>=call:
            line(im,[(551,780),(551,997)],CYAN,5);arrow(im,(551,997),(519,997),reveal(t,call,.25),CYAN,5)
            arrow(im,(520,1012),(610,1012),reveal(t,call+.25,.25),CYAN,5)
        if t>=result:
            box(im,(110,1120,970,1280),fill='#112C2D',outline=GREEN,r=20)
            txt(im,'ACTUAL JUNIT STDOUT',137,1131,26,GREEN,True)
            txt(im,'order result: demo-paid:2500',137,1181,35,WHITE,mono=True)
        if t>=verify:txt(im,'gateway same: true',137,1232,35,GREEN,mono=True);check(im,920,1235)
        return im
    if k==5:return recap_scene(u,t,recap,duration,c)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)

def recap_complete_at(cues):return float(cues.get('complete',6.5))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};pc=proof_cues or {};duration=scene_duration or 8;t=u*duration if elapsed is None else elapsed
    at=lambda name,default:float(pc.get(name,cues.get(name,default)))
    load=at('load',3.2);resolve=at('resolve',3.6);supply=at('supply',4.2);execute=at('execute',4.8);complete=at('complete',duration-2)
    im=base(['Spring wires its beans.','You supply args to new.'])
    box(im,(110,625,970,785),fill=CARD,outline=PURPLE,r=20)
    if t<load:
        txt(im,'YOU PROVIDE THE ARGUMENT',138,645,28,CYAN,True)
        txt(im,'new OrderService(gateway)',138,715,39,WHITE,mono=True)
    else:
        txt(im,'Config.class',140,673,40,PURPLE,True,mono=True)
        txt(im,'Spring',730,673,42,PURPLE,True)
        arrow(im,(478,705),(697,705),reveal(t,load,.2),CYAN,5)
    context(im,(110,840,970,1125),t>=supply)
    if t>=resolve:node(im,'Gateway',145,970,330,125,'one matching bean',GREEN,42)
    if t>=supply:
        node(im,'OrderService',580,970,350,125,'constructor',GREEN,39)
        arrow(im,(485,1028),(570,1028),reveal(t,supply,.22),CYAN,5)
    if t>=execute:
        box(im,(110,1162,970,1286),fill='#112C2D',outline=GREEN,r=18)
        txt(im,'APP uses the ready service',138,1176,36,GREEN,True)
        txt(im,'new: caller still supplies arguments',138,1235,29,WHITE)
    if t>=complete:check(im,920,1205)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.4;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,765,88,WHITE,True,center=True,gap=1.12)
    line(im,[(315,1010),(315+450*reveal(t,0,.35),1010)],CYAN,5)
    return im

def read_timing():return json.loads((ROOT/'source/timing.json').read_text())
def mechanism_anchors(data):
    s=data['scenes'];c=data.get('scene_cues_absolute',{});m=c.get('managed',{});r=c.get('resolve',{});i=c.get('inject',{});e=c.get('execute',{});p=c.get('recap',{})
    return {'managed_service_s':float(s[1]['start']),'single_constructor_s':float(m.get('one',s[1]['start']+1.4)),'parameter_type_s':float(r.get('parameter',s[2]['start']+.3)),'candidate_resolved_s':float(r.get('match',s[2]['start']+2.7)),'constructor_supplied_s':float(i.get('supply',s[3]['start']+.5)),'reference_stored_s':float(i.get('store',s[3]['start']+2.8)),'service_ready_s':float(i.get('ready',s[3]['start']+3.8)),'service_call_s':float(e.get('call',s[4]['start']+.1)),'service_result_s':float(e.get('result',s[4]['start']+1.8)),'verification_s':float(e.get('verify',s[4]['start']+4.5)),'manual_scope_s':float(p.get('manual',s[5]['start'])),'recap_complete_s':float(p.get('complete',data['recap_hold_start']))}
def graph_ready_at(data):return mechanism_anchors(data)['service_ready_s']
def application_use_start(data):return mechanism_anchors(data)['service_call_s']

def render_frame(t,data,with_caption=True):
    s=data['scenes'];k=next((i for i,v in enumerate(s) if v['start']<=t<v['end']),len(s)-1);current=s[k];duration=current['end']-current['start'];elapsed=t-current['start'];u=elapsed/duration
    key={1:'managed',2:'resolve',3:'inject',4:'execute',5:'recap'}.get(k)
    cues={name:float(v)-current['start'] for name,v in data.get('scene_cues_absolute',{}).get(key,{}).items() if isinstance(v,(int,float))}
    if k==5:cues['complete']=float(data.get('recap_cues_absolute',{}).get('complete',data['recap_hold_start']))-current['start']
    im=opening_visual(t,data) if t<2 else scene(k,u,elapsed,data.get('recap_cues'),duration,cues)
    if with_caption:
        cap=next((v for v in data['captions'] if v['start']<=t<v['end']),None)
        if cap:caption(im,cap['text'])
    return im

def srt_time(t):
    ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
def write_srt(data):
    s=''.join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c['text']}\n\n" for i,c in enumerate(data['captions'],1));(ROOT/'subtitles.srt').write_text(s)

def write_styles():
    font_file=ASSETS/'Inter-Variable.ttf';sha=hashlib.sha256(font_file.read_bytes()).hexdigest();geometry=headline_geometry()
    b=[min(v['bbox'][0] for v in geometry),min(v['bbox'][1] for v in geometry),max(v['bbox'][2] for v in geometry),max(v['bbox'][3] for v in geometry)]
    thumb={'font_family':'Inter','font_weight':900,'font_size':104,'font_sizes':[104,96,104],'font_axes':{'opsz':32,'wght':900},'text_color':WHITE,'headline_lines':[v['text'] for v in geometry],'headline_bounds':b,'headline_line_bounds':geometry,'headline_roi':HEADLINE_ROI,'technical_roi':TECHNICAL_ROI,'highlight':{'background':BLUE,'corner_radius':20,'padding':[18,8],'bounds':[geometry[1]['bbox'][0]-18,geometry[1]['bbox'][1]-8,geometry[1]['bbox'][2]+18,geometry[1]['bbox'][3]+8]},'font_file':'source/assets/Inter-Variable.ttf','font_sha256':sha,'safe_area':[90,250,990,1520],'source_frame0_pixel_identical_to_cover':True,'stable_headline_seconds':[0,1],'technical_transition_seconds':[1,2],'opening_caption':HOOK,'caption_region':CAPTION_REGION}
    sub={'font_family':'Inter','font_weight':700,'font_size':52,'font_axes':{'opsz':32,'wght':700},'text_color':WHITE,'background':{'color':'#000000','opacity':.82,'alpha':209,'corner_radius':12},'padding':[26,14],'max_width':840,'center':[540,1380],'max_lines':2,'caption_region':CAPTION_REGION,'font_file':'source/assets/Inter-Variable.ttf','font_sha256':sha,'measurement':'PillowImageDraw.textbbox; actualglyphbounds;RGBAalpha_composite','line_gap':10}
    (ROOT/'thumbnail-style.json').write_text(json.dumps(thumb,indent=2)+'\n');(ROOT/'subtitle-style.json').write_text(json.dumps(sub,indent=2)+'\n')

def preflight(data):
    TEXT_BOUNDS.clear();CAPTION_LAYOUTS.clear();samples=[]
    for s in data['scenes']:samples.extend(np.linspace(s['start'],s['end']-1/FPS,31))
    samples.extend([0,.5,1,1.25,1.5,1.75,2])
    for t in samples:render_frame(float(t),data)
    cover();bad=[r for r in TEXT_BOUNDS if r['bbox'][0]<90 or r['bbox'][1]<250 or r['bbox'][2]>990 or r['bbox'][3]>1520]
    exact=np.array_equal(np.asarray(render_frame(0,data)),np.asarray(cover()))
    headline_checks=[np.array_equal(np.asarray(opening_visual(0).crop(tuple(HEADLINE_ROI))),np.asarray(opening_visual(t).crop(tuple(HEADLINE_ROI)))) for t in np.arange(1,61)/60]
    result={'samples':len(samples),'unique_text_bounds':len({(r['text'],tuple(r['bbox'])) for r in TEXT_BOUNDS}),'safe_area':[90,250,990,1520],'violations':bad,'caption_layouts':len(CAPTION_LAYOUTS),'source_cover_frame0_exact':bool(exact),'headline_roi_stable_first_second':all(headline_checks),'passed':not bad and bool(exact) and all(headline_checks)}
    out=ROOT/'source/evidence';out.mkdir(exist_ok=True);(out/'renderer-preflight.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'caption-layouts.json').write_text(json.dumps(CAPTION_LAYOUTS,indent=2)+'\n')
    if not result['passed']:raise ValueError(('Visualpreflightfailed',result))
    return result

def previews(data):
    out=ROOT/'source/evidence';out.mkdir(exist_ok=True);qa=ROOT/'qa';qa.mkdir(exist_ok=True)
    samples=[0]+[s['start']+(s['end']-s['start'])*.92 for s in data['scenes']];thumbs=[]
    for j,t in enumerate(samples):
        im=render_frame(t,data);im.save(out/f'preview-{j}.png');thumbs.append(im.resize((324,576),Image.Resampling.LANCZOS))
    contact=Image.new('RGB',(1296,1152),NAVY)
    for j,im in enumerate(thumbs):contact.paste(im,(j%4*324,j//4*576))
    contact.save(out/'mobile-contact-sheet.png');contact.save(qa/'mobile-preview.png')
    for name,crop,size in [('cover-feed',(0,0,1080,1920),(270,480)),('cover-profile-square',(0,420,1080,1500),(360,360)),('cover-profile-portrait',(0,240,1080,1680),(360,480))]:cover().crop(crop).resize(size,Image.Resampling.LANCZOS).save(qa/(name+'.png'))
    opening=Image.new('RGB',(1512,672),NAVY)
    for j,t in enumerate([0,.5,1,1.25,1.5,1.75,2]):opening.paste(render_frame(t,data).resize((216,384),Image.Resampling.LANCZOS),(j*216,0))
    opening.save(qa/'source-opening-transition-contact.png')
    render_frame((data['recap_hold_start']+data['recap_hold_end'])/2,data,False).save(ROOT/'recap.png')
    s=data['scenes'][-1];thanks_scene(1,s['end']-s['start'],s['end']-s['start']).save(ROOT/'thanks.png')

def main():
    p=argparse.ArgumentParser();p.add_argument('--previews',action='store_true');p.add_argument('--preflight',action='store_true');p.add_argument('--render',action='store_true');a=p.parse_args();data=read_timing()
    cover().save(ROOT/'cover.png');write_styles();write_srt(data)
    if a.preflight:print(json.dumps(preflight(data),indent=2))
    if a.previews:previews(data)
    if a.render:
        count=math.ceil(data['duration']*FPS);cmd=['ffmpeg','-y','-hide_banner','-loglevel','warning','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(ROOT/'source/animation/mix.wav'),'-map','0:v','-map','1:a','-vf','scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','fast','-crf','19','-threads','2','-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(count/FPS),'-movflags','+faststart',str(ROOT/'video.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        for n in range(count):
            proc.stdin.write(render_frame(n/FPS,data).tobytes())
            if n%300==0:print(f'frame{n}/{count}',flush=True)
        proc.stdin.close()
        if proc.wait():raise RuntimeError('FFmpegfailed')
        print('Rendercomplete',flush=True)
if __name__=='__main__':main()
