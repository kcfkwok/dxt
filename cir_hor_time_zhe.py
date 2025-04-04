from ut_math import *
from ut_cal import *
from paper import *
from def_font import *
from config import config
from word_list import ZHE

def draw_hor_time_zhe(im,draw,xc,yc,r1,r2,stroke_width=0):
    FCOLOR = (0,0,0,255)
    LW=4
    ari_ang = config.ari_ang
    f_south = config.f_south
    
    r1a = r1 - 30
    #ang=Ra = 0  #270 - ari_ang -180  # when ari_ang=90, ang=0
        
    if f_south:
        ang=180
    else:
        ang = 0
        
    txt_ang=270-ang
    hr=int((180+ari_ang) / 15)  #18      # when ari_ang=90, hr=18
    if hr >=24:
        hr = hr -24
    for i in range(24):
        sin_ang = sn(ang)
        cos_ang = cs(ang)
        x2 = int(cos_ang*r2 + xc)
        y2 = int(sin_ang*r2 + yc)
        skip="""
        
        x2a = int(cos_ang*r2a + xc)
        y2a = int(sin_ang*r2a + yc)
        x3 = int(cos_ang*r3 + xc)
        y3 = int(sin_ang*r3 + yc)
        """
        #draw.line([(x3,y3),(x2a,y2a)],fill=FCOLOR,width=LW)   
    
        if hr%2 ==0:
            x1a = int(cos_ang*r1a + xc)  # r5a
            y1a = int(sin_ang*r1a + yc)
            sz = int(hr / 2) % 12
            draw_text(im,ZHE[sz], unicode_font_42,x1a,y1a,txt_ang,stroke_width=stroke_width)
            
        else:
            x1 = int(cos_ang*r1 + xc)
            y1 = int(sin_ang*r1 + yc)
            #x2 = int(cos_ang*r2 + xc)
            #y2 = int(sin_ang*r2 + yc)
            draw.line([(x1,y1),(x2,y2)],fill=FCOLOR,width=LW) 
        #break
        if f_south:
            hr +=1
        else:
            hr -=1
        if hr <0:
            hr=23
        ang += 15
        txt_ang= 270-ang
        if txt_ang <0:
            txt_ang =360+txt_ang


def add_cir_hor_time_zhe(paper,xc,yc,r1,r2,im=None,draw=None,stroke_width=0):
    LW=4
    if im is not None:
        draw.circle((xc,yc),r1,outline=(0,0,0,255),width=LW)
        draw_hor_time_zhe(im,draw,xc,yc,r1,r2,stroke_width=stroke_width)
        return
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y

    layer = paper.add_layer(name='cir_zhe')
    #layer.draw.circle((xc,yc),r1,outline=(0,0,0,255),fill=(255,255,0),width=LW)
    #layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=2)
    #layer.draw.circle((xc,yc),r,outline=(0,0,0,255),fill=(255,255,255),width=LW)
    layer.draw.circle((xc,yc),r1,outline=(0,0,0,255),width=LW)
    
    draw_hor_time_zhe(layer.im,layer.draw,xc,yc,r1,r2,stroke_width=stroke_width)
