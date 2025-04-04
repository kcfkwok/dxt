from def_font import *
from ut_cal import *
from word_list import *
from def_color import *
from config import config
from g_share import g_share
from ut_misc import *

def draw_jieqi_color(im0,draw0,xc,yc,r4,r5,f_south, ras):
    w_px = xc + r4
    h_px = yc + r4
    bgcolor=(255,255,255)
    bgc=(bgcolor[0],bgcolor[1],bgcolor[2],0)
    im = Image.new(mode='RGBA',size=(w_px, h_px),color=bgc)
    draw = ImageDraw.Draw(im)
    # for color pieslice test
    pie_data={}
    for i in range(24):
        j=i*15
        s_ra = ras[j]
        j1 = (i+1)*15
        if j1 >=360:
            j1= j1-360
        e_ra = ras[j1]
        if f_south:
            e_ra = -ras[j]
            s_ra = -ras[j1]
        s_ang= s_ra+ config.ari_ang
        e_ang = e_ra + config.ari_ang
        if f_south:
            #print('i:%s s_ra:%s s_ang:%s e_ra:%s e_ang:%s' % 
             # (i,s_ra,s_ang, e_ra,e_ang))
            if s_ang < 0:
                s_ang +=360
            if e_ang <0:
                e_ang+=360
        #print('i:%s s_ra:%s s_ang:%s e_ra:%s e_ang:%s' % 
        #      (i,s_ra,s_ang, e_ra,e_ang))
        jq = JIE_QIS[i]
        jqcolor = COLOR_JIEQI[jq]
        pie_data[i]= (s_ang,e_ang,jqcolor)
    #"""        
    # 绘制扇形
    #skip="""
    for i in range(24): #24):
        start_angle=pie_data[i][0]
        end_angle=pie_data[i][1]
        jqcolor = pie_data[i][2]
        draw.pieslice((xc - r4, yc - r4, xc + r4, yc + r4), 
                      start=start_angle, end=end_angle, fill=jqcolor)
    draw.circle((xc,yc),r5,fill=WHITE)
    im = make_transparent(im)
    im0.paste(im,(0,0))
    

def draw_jieqi_mark(im,draw,xc,yc,rx, year,tz, fill_yellow=False,small=False):
    if small:
        font =unicode_font_36
    else:
        font =unicode_font_42
        
    r4 = rx
    r4a = rx - 30
    r4b = r4 -50
    r5 = r4 - 60
    FCOLOR = (0,0,0,255)
    LW=2
    try:
        Obl = g_share.Obl
    except:
        from g_share import g_share
        nd = cal_d_w_hm(year,1,1,-tz,0)
        Obl = g_share.Obl
        
    try:
        f_south = config.f_south
    except:
        from config import config
        f_south = config.f_south    
    if f_south:
        txt_ang=90 +5 +90
    else:
        txt_ang=270 -5 -90  # kcf test

    try:
        ras = g_share.ras
    except:
        ras=[]
        
    if len(ras)==0:
        ecl_long=0
        ecl_lat=0
        for j in range(360):
            ecl_long =j
            ra, dec = radc(ecl_long, ecl_lat)
            ras.append(ra)
        g_share.ras = ras
        
    draw_jieqi_color(im,draw,xc,yc,r4,r5,f_south,ras)
    for j in range(360):
        ra = ras[j]
        ang= ra+ config.ari_ang
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)
    
        if (j % 10)==0:
        
            # draw long mark:
            x5 = int(cos_ang*r5 + xc)
            y5 = int(sin_ang*r5 + yc)
            x4a = int(cos_ang*r4a + xc)
            y4a = int(sin_ang*r4a + yc)
            #if not white_mark:
            draw.line([(x5,y5),(x4a,y4a)],fill=FCOLOR,width=LW)  
        
        if (j % 2)==0:
        
            # draw long mark:
            x5 = int(cos_ang*r5 + xc)
            y5 = int(sin_ang*r5 + yc)
            x4b = int(cos_ang*r4b + xc)
            y4b = int(sin_ang*r4b + yc)
            #if not white_mark:
            draw.line([(x5,y5),(x4b,y4b)],fill=FCOLOR,width=LW)  

        if (j % 15)> 0:
            continue
        i = int(j / 15)
        # draw jie qi
        x5 = int(cos_ang*r5 + xc)
        y5 = int(sin_ang*r5 + yc)
        x4 = int(cos_ang*r4 + xc)
        y4 = int(sin_ang*r4 + yc)
        #if not white_mark:
        if not fill_yellow:
            draw.line([(x5,y5),(x4,y4)],fill=FCOLOR,width=LW)
        x4a = int(cos_ang*r4a + xc)
        y4a = int(sin_ang*r4a + yc)
        if small:
            sin_n = sn(ang+5)
            cos_n = r_cs(ang+5)
        else:
            sin_n = sn(ang+3)
            cos_n = r_cs(ang+3)
        xnc = int(cos_n * r4a + xc)
        ync = int(sin_n * r4a + yc)
        
        draw_text(im, JIE_QIS[i], font,xnc,ync,txt_ang) 
        
        if f_south:
            txt_ang +=15
        else:
            txt_ang -= 15
        if txt_ang <0:
            txt_ang =360+txt_ang


def add_cir_jieqi(paper,xc,yc,rx,year,tz,im=None,draw=None,small=False):
    LW=2
    if im is not None:
        draw_jieqi_mark(im,draw,xc,yc,rx,year,tz,small=small)
        draw.circle((xc,yc),rx,outline=(0,0,0,255),width=LW)
        return
    
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer = paper.add_layer(name='cir_zodiac')
    
    
    draw_jieqi_mark(layer.im,layer.draw,xc,yc,rx,year,tz,small=small)
    layer.draw.circle((xc,yc),rx,outline=(0,0,0,255),width=LW)