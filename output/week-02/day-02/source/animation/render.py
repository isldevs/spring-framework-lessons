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
HOOK='How does Spring know what to inject?'
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
        rows=['How does Spring know','what to inject?']
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

def ctor_card(im,y=625,highlight=False):
    box(im,(110,y,970,y+222),fill='#0B1A2E',outline=CYAN,r=22,width=2)
    code_run(im,[('@Service ',PURPLE),('class OrderService {',WHITE)],137,y+19,36)
    code_run(im,[('  OrderService(',WHITE)],137,y+80,38)
    code_run(im,[('    PaymentGateway',CYAN),(' gateway)',WHITE)],137,y+139,36)

def headline_geometry():
    d=ImageDraw.Draw(BG);items=[('How Spring',104,110,475),('Finds Your',104,110,626),('Dependencies',104,128,777)];out=[]
    for s,size,x,y in items:
        b=d.textbbox((x,y),s,font=font(size,weight=900));out.append({'text':s,'size':size,'origin':[x,y],'bbox':list(b)})
    return out

def cover_headline(im,dy=0):
    geometry=headline_geometry();d=ImageDraw.Draw(im)
    for item in geometry:
        s=item['text'];x,y=item['origin'];y+=dy;b=list(item['bbox']);b[1]+=dy;b[3]+=dy
        if s=='Dependencies':box(im,(b[0]-18,b[1]-8,b[2]+18,b[3]+8),fill=BLUE,outline=None,r=20)
        txt(im,s,x,y,item['size'],WHITE,weight=900)

def cover_base(t=0):
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    cover_headline(im)
    node(im,'Required type',130,1180,360,95,None,CYAN,35)
    node(im,'BeanFactory',600,1180,350,95,None,PURPLE,35)
    arrow(im,(500,1228),(590,1228),1,CYAN,5)
    # A type request travels from the constructor parameter toward the factory.
    p=(t/.85)%1;cx=503+83*p;ImageDraw.Draw(im).ellipse((cx-7,1221,cx+7,1235),fill=WHITE)
    return im

def cover():
    im=cover_base(0);ctor_card(im,940,True);caption(im,HOOK);return im

def required_scene(elapsed,cues=None,draw_card=True):
    cues=cues or {};parameter=float(cues.get('parameter',1.0));descriptor=float(cues.get('descriptor',3.2))
    im=base(['A constructor requests','a required dependency.'])
    if draw_card:ctor_card(im,625,elapsed>=parameter)
    if elapsed>=parameter:
        line(im,[(215,815),(566,815)],CYAN,4)
        txt(im,'SPRING-MANAGED OrderService',138,860,30,PURPLE,True)
    box(im,(110,925,970,1268),fill='#0C1D30',outline=CYAN,r=23,width=2)
    txt(im,'DEPENDENCY REQUEST',140,948,30,CYAN,True)
    if elapsed>=descriptor:
        txt(im,'type: PaymentGateway',140,1020,40,WHITE,mono=True)
        txt(im,'required: true',140,1094,40,WHITE,mono=True)
        txt(im,'from the constructor parameter',140,1180,32,MUTED)
        arrow(im,(540,886),(540,915),reveal(elapsed,descriptor,.25),CYAN,4)
    else:
        txt(im,'Spring reads the parameter',140,1057,39,WHITE,True)
    return im

def opening_visual(t,data=None):
    start=cover_base(t)
    if t<=1:
        ctor_card(start,940,True);return start
    p=ease(t-1)
    cues={};elapsed=max(0,t-2)
    if data:
        s=data['scenes'][1];elapsed=t-s['start'];cues={k:float(v)-s['start'] for k,v in data.get('scene_cues_absolute',{}).get('required',{}).items()}
    end=required_scene(elapsed,cues,False)
    # Retire the thumbnail headline before revealing the smaller scene heading.
    # This avoids double-exposed words while the actual constructor card travels.
    band=(90,415,990,920)
    start.paste(BG.crop(band),band);end.paste(BG.crop(band),band)
    im=Image.blend(start,end,p)
    old_progress=ease((t-1)/.45);old_alpha=1-old_progress
    if old_alpha>0:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));cover_headline(overlay,-40*old_progress)
        overlay.putalpha(overlay.getchannel('A').point(lambda a:round(a*old_alpha)))
        im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    new_alpha=ease((t-1.5)/.5)
    if new_alpha>0:
        overlay=Image.new('RGBA',(W,H),(0,0,0,0));lines(overlay,['A constructor requests','a required dependency.'],110,422,64,WHITE,True,gap=1.08)
        overlay.putalpha(overlay.getchannel('A').point(lambda a:round(a*new_alpha)))
        im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB')
    # One continuous constructor code element travels from thumbnail into explanation.
    ctor_card(im,940+(625-940)*p,True)
    return im

def hook_scene(t,with_motion=True):return opening_visual(t if with_motion else 0)
COVER=cover()

def candidate_row(im,y,name,kind,matching=True,eligible=True,filtered=False):
    """A registry metadata row; excluded candidates remain registered and visible."""
    color=(GREEN if eligible else MUTED) if filtered and matching else (CYAN if matching else PURPLE)
    if filtered and not matching:color=RED
    h=164 if matching and not eligible else 130
    box(im,(145,y,935,y+h),fill='#14243B',outline=color,r=17,width=3)
    txt(im,name,168,y+13,38,color,True)
    txt(im,kind,168,y+(62 if matching and not eligible else 68),32,WHITE,mono=True)
    if filtered and matching and eligible:check(im,895,y+39)
    if filtered and matching and not eligible:
        txt(im,'autowireCandidate: false',168,y+103,32,MUTED,mono=True)
    if filtered and not matching:txt(im,'TYPE MISMATCH',654,y+17,27,RED,True)


def discovery_scene(t,c):
    at=lambda name,default:float(c.get(name,default))
    types=at('types',1.0);unrelated=at('unrelated',3.3);eligibility=at('eligibility',5.9)
    im=base(['Match compatible types.','Check injection eligibility.'])
    txt(im,'SIMPLIFIED PATH FROM OUR RUNTIME TRACE',110,575,28,MUTED,True)
    box(im,(110,635,970,1275),fill='#0C1D30',outline=PURPLE,r=23,width=2)
    txt(im,'BEAN FACTORY • REGISTERED BEANS',140,657,31,PURPLE,True)
    if t>=types:
        candidate_row(im,720,'eligibleGateway','PaymentGateway',True,True,t>=eligibility)
        candidate_row(im,861,'backupGateway','PaymentGateway',True,False,t>=eligibility)
    if t>=unrelated:
        candidate_row(im,1043,'gateway','AuditLogger',False,True,True)
    if t>=eligibility:
        txt(im,'Type match ≠ injection eligibility',145,1192,33,GREEN,True)
        txt(im,'backupGateway remains a registered bean',145,1235,28,MUTED)
    else:
        txt(im,'Requested: PaymentGateway',145,1196,34,CYAN,True)
    return im


def selection_scene(t,c):
    at=lambda name,default:float(c.get(name,default))
    unique=at('unique',.6);supply=at('supply',2.5);stored=at('stored',4.2)
    im=base(['One eligible bean.','One constructor argument.'])
    box(im,(110,625,970,872),fill=CARD,outline=CYAN,r=20)
    code_run(im,[('OrderService(',WHITE)],138,650,39)
    code_run(im,[('  PaymentGateway',CYAN),(' gateway) {',WHITE)],138,714,36)
    if t>=stored:code_run(im,[('  this.gateway = gateway;',GREEN)],138,785,36)
    else:txt(im,'  // argument supplied by Spring',138,785,32,MUTED,mono=True)
    context(im,(110,923,970,1268),t>=stored)
    if t>=unique:
        node(im,'eligibleGateway',145,1010,335,152,'managed instance',GREEN,34)
    if t>=supply and t<stored:
        p=reveal(t,supply,.4)
        line(im,[(489,1085),(540,1085),(540,858)],CYAN,5)
        arrow(im,(540,858),(540,811),p,CYAN,5)
        cy=1084-(1084-819)*p
        ImageDraw.Draw(im).ellipse((532,cy-8,548,cy+8),fill=WHITE)
        txt(im,'the existing reference',145,1205,34,CYAN,True)
    if t>=stored:
        node(im,'OrderService',580,1010,350,152,'gateway field',GREEN,39)
        arrow(im,(490,1085),(570,1085),1,CYAN,5)
        txt(im,'gateway same: true',145,1205,36,GREEN,mono=True)
    return im


def missing_scene(t,c):
    at=lambda name,default:float(c.get(name,default))
    no_candidate=at('no_candidate',1.0);failure=at('failure',4.0)
    im=base(['No eligible candidate.','Startup cannot finish.'])
    txt(im,'FRESH CONTEXT: MissingConfig.class',110,585,31,MUTED,True)
    box(im,(110,650,970,840),fill=CARD,outline=CYAN,r=20)
    code_run(im,[('OrderService(',WHITE)],138,675,40)
    code_run(im,[('  PaymentGateway',CYAN),(' gateway)',WHITE)],138,750,37)
    box(im,(110,890,970,1068),fill='#0C1D30',outline=PURPLE,r=20,width=2)
    txt(im,'BEAN FACTORY LOOKUP',138,908,29,PURPLE,True)
    txt(im,'PaymentGateway',138,964,42,CYAN,True)
    if t>=no_candidate:
        txt(im,'eligible: 0',674,970,34,RED,True)
        line(im,[(540,849),(540,879)],RED,5)
        line(im,[(529,858),(551,878)],RED,4);line(im,[(551,858),(529,878)],RED,4)
    if t>=failure:
        box(im,(110,1110,970,1287),fill='#301C30',outline=RED,r=19,width=2)
        txt(im,'REFRESH FAILED',138,1123,30,RED,True)
        txt(im,'UnsatisfiedDependencyException',138,1173,32,WHITE,mono=True)
        txt(im,'cause: NoSuchBeanDefinitionException',138,1229,30,WHITE,mono=True)
    return im


def scene(k,u,elapsed=None,recap=None,scene_duration=None,scene_cues=None):
    duration=scene_duration or[2,5,8,5,6,10,1.4][k];t=u*duration if elapsed is None else elapsed;c=scene_cues or {}
    if k==0:return opening_visual(t)
    if k==1:return required_scene(t,c)
    if k==2:return discovery_scene(t,c)
    if k==3:return selection_scene(t,c)
    if k==4:return missing_scene(t,c)
    if k==5:return recap_scene(u,t,recap,duration,c)
    if k==6:return thanks_scene(u,t,duration)
    raise ValueError(k)


def recap_complete_at(cues):return float(cues.get('complete',7.8))
def recap_scene(u,elapsed=None,cues=None,scene_duration=None,proof_cues=None):
    cues=cues or {};pc=proof_cues or {};duration=scene_duration or 10;t=u*duration if elapsed is None else elapsed
    at=lambda name,default:float(pc.get(name,cues.get(name,default)))
    verify=at('verify',0);scope=at('scope',2.3);match=at('match',6.3);filt=at('filter',6.7);inject=at('inject',7.1);complete=at('complete',duration-2)
    im=base(['Match. Filter. Inject.','Real context tests pass.'])
    if t<match:
        box(im,(110,625,970,1010),fill='#0C1D30',outline=GREEN,r=23,width=2)
        txt(im,'ACTUAL JUNIT STDOUT',140,646,29,GREEN,True)
        if t>=verify:
            for j,s in enumerate(['compatible candidates: 2','eligible candidates: 1','gateway same: true','missing candidate: true']):
                txt(im,s,140,715+j*65,36,WHITE,mono=True)
        if t>=scope:
            txt(im,'OTHER SELECTION RULES CAN APPLY',110,1084,31,PURPLE,True)
            txt(im,'Qualifiers and @Primary',110,1142,43,WHITE,True)
            txt(im,'are not shown in this example.',110,1210,34,MUTED)
        return im
    txt(im,'3 JUnit tests passed',110,576,35,GREEN,True)
    box(im,(110,650,970,802),fill=CARD,outline=PURPLE,r=18,width=2)
    txt(im,'APP STARTUP',138,664,28,PURPLE,True)
    txt(im,'register(SuccessConfig.class)',138,712,36,WHITE,mono=True)
    txt(im,'refresh()',690,762,30,CYAN,mono=True)
    arrow(im,(540,813),(540,847),reveal(t,match,.16),CYAN,4)
    box(im,(110,858,970,1046),fill='#0C1D30',outline=PURPLE,r=20,width=2)
    txt(im,'BeanFactory',138,876,36,PURPLE,True)
    txt(im,'PaymentGateway type',138,933,36,CYAN,True)
    if t>=filt:
        txt(im,'2 compatible → 1 eligible',138,995,34,GREEN,True)
        check(im,914,1007)
    if t>=inject:
        arrow(im,(540,1055),(540,1084),reveal(t,inject,.18),CYAN,4)
        box(im,(110,1095,970,1215),fill='#13302E',outline=GREEN,r=18,width=2)
        txt(im,'OrderService(gateway)',138,1109,39,WHITE,mono=True)
        txt(im,'same managed reference',138,1169,31,GREEN,True)
    if t>=complete:check(im,919,1143)
    txt(im,'Qualifiers / @Primary can also matter',110,1250,30,MUTED)
    return im

def thanks_scene(u,elapsed=None,scene_duration=None):
    duration=scene_duration or 1.4;t=u*duration if elapsed is None else elapsed
    im=BG.copy();txt(im,'iSLDevs',110,280,31,WHITE,True)
    lines(im,['Thanks for','watching.'],540,765,88,WHITE,True,center=True,gap=1.12)
    line(im,[(315,1010),(315+450*reveal(t,0,.35),1010)],CYAN,5)
    return im

def read_timing():return json.loads((ROOT/'source/timing.json').read_text())
def mechanism_anchors(data):
    s=data['scenes'];c=data.get('scene_cues_absolute',{});r=c.get('required',{});d=c.get('discovery',{});i=c.get('selection',{});m=c.get('missing',{});p=c.get('recap',{})
    return {'required_type_s':float(r.get('parameter',s[1]['start']+1)),
            'dependency_descriptor_s':float(r.get('descriptor',s[1]['start']+3.2)),
            'compatible_candidates_s':float(d.get('types',s[2]['start']+1)),
            'unrelated_excluded_s':float(d.get('unrelated',s[2]['start']+3.3)),
            'eligibility_filter_s':float(d.get('eligibility',s[2]['start']+5.9)),
            'selected_candidate_s':float(i.get('unique',s[3]['start']+.6)),
            'constructor_supplied_s':float(i.get('supply',s[3]['start']+2.5)),
            'reference_stored_s':float(i.get('stored',s[3]['start']+4.2)),
            'no_eligible_candidate_s':float(m.get('no_candidate',s[4]['start']+1)),
            'startup_failure_s':float(m.get('failure',s[4]['start']+4)),
            'verification_s':float(p.get('verify',s[5]['start'])),
            'selection_scope_s':float(p.get('scope',s[5]['start']+2.3)),
            'recap_match_s':float(p.get('match',s[5]['start']+6.3)),
            'recap_filter_s':float(p.get('filter',s[5]['start']+6.7)),
            'recap_inject_s':float(p.get('inject',s[5]['start']+7.1)),
            'recap_complete_s':float(p.get('complete',data['recap_hold_start']))}
def graph_ready_at(data):return mechanism_anchors(data)['reference_stored_s']
def application_use_start(data):
    # Compatibility API: first ready service, not an application invocation.
    return graph_ready_at(data)

def render_frame(t,data,with_caption=True):
    s=data['scenes'];k=next((i for i,v in enumerate(s) if v['start']<=t<v['end']),len(s)-1);current=s[k];duration=current['end']-current['start'];elapsed=t-current['start'];u=elapsed/duration
    key={1:'required',2:'discovery',3:'selection',4:'missing',5:'recap'}.get(k)
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
    thumb={'font_family':'Inter','font_weight':900,'font_size':104,'font_sizes':[104,104,104],'font_axes':{'opsz':32,'wght':900},'text_color':WHITE,'headline_lines':[v['text'] for v in geometry],'headline_bounds':b,'headline_line_bounds':geometry,'headline_roi':HEADLINE_ROI,'technical_roi':TECHNICAL_ROI,'highlight':{'background':BLUE,'corner_radius':20,'padding':[18,8],'bounds':[geometry[2]['bbox'][0]-18,geometry[2]['bbox'][1]-8,geometry[2]['bbox'][2]+18,geometry[2]['bbox'][3]+8]},'font_file':'source/assets/Inter-Variable.ttf','font_sha256':sha,'safe_area':[90,250,990,1520],'source_frame0_pixel_identical_to_cover':True,'stable_headline_seconds':[0,1],'technical_transition_seconds':[1,2],'highlighted_phrase':'Dependencies','technical_background':'OrderService constructor PaymentGateway type request to BeanFactory; simplified demonstrated path','crop_checks':{'square':[0,420,1080,1500],'portrait':[0,240,1080,1680]},'opening_caption':HOOK,'caption_region':CAPTION_REGION}
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
