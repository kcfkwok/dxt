from config import config
from ut_cal import *


def draw_ecl(im, draw,xc,yc,rx,s_year,tz,rr,requ,color_f=True):
    from config import config
    FCOLOR = (0,0,0,255)
    LW=2
    if color_f:
        ECL_LINE_COLOR = config.ECL_LINE_COLOR
    else:
        ECL_LINE_COLOR = FCOLOR
    ECL_LINE_WIDTH = config.ECL_LINE_WIDTH

    try:
        Obl = g_share.Obl
    except:
        from g_share import g_share
        nd = cal_d_w_hm(s_year,1,1,-tz,0)
        Obl = g_share.Obl
        
    try:
        f_south = g_share.f_south
    except:
        from g_share import g_share
        f_south = g_share.f_south
    if f_south:
        txt_ang=90 +5 +90
    else:
        txt_ang=270 -5 -90
        
    for dn in range(1,367):
        month,day,year = days_to_date(dn, s_year)
        if year != s_year:
            break
        nd = cal_d_w_hm(year,month,day,-tz,0)
        #print('cal_d_w_hm Obl:%s' % G_SHARE.Obl)
        sra, sdec, _ =SunValues(nd)
        #slong = LonSun(nd)
        #print('%d %d-%d-%d sra:%.2f sdec:%.2f elong:%.2f' % (dn,y,m,d,sra,sdec,slong))
        ang = config.ari_ang + sra
        #print('ang:',ang)
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)

        if day==1:

            ex0,ey0 = ra_dec_to_xyplot(sra,sdec,xc,yc,rr,requ,f_south=f_south)
        elif day in [11,21,31]:

            ex0,ey0 = ra_dec_to_xyplot(sra,sdec,xc,yc,rr,requ,f_south=f_south)
        elif day in [6,16,26]:

            ex0,ey0 = ra_dec_to_xyplot(sra,sdec,xc,yc,rr,requ,f_south=f_south)
        else:

            if day in [3,8,13,18,23,28]:
                ex1,ey1 = ra_dec_to_xyplot(sra,sdec,xc,yc,rr,requ,f_south=f_south)
                #if draw_ecl:
                draw.line([(ex0,ey0),(ex1,ey1)],fill=ECL_LINE_COLOR,width=ECL_LINE_WIDTH)

def draw_ecl_equ(im,draw,xc,yc,rx,year,tz,rr,requ,color_f=True):
    LW=2
    FCOLOR = (0,0,0,255)
    if color_f:
        EQU_LINE_COLOR = config.EQU_LINE_COLOR
    else:
        EQU_LINE_COLOR = FCOLOR
        
    draw.circle((xc,yc),requ,outline=EQU_LINE_COLOR,width=LW)
    draw_ecl(im, draw,xc,yc,rx,year,tz,rr,requ, color_f=color_f)
    
	
def add_ecl_equ(paper,xc,yc,rx,year,tz,rr,requ,im=None,draw=None,color_f=True):
    LW=2
    if im is not None:
        draw_ecl_equ(im,draw,xc,yc,rx,year,tz,rr,requ,color_f=color_f)
        return
    
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y

    layer = paper.add_layer(name='ecl_equ')
    #layer.draw.circle((xc,yc),r1,outline=(0,0,0,255),fill=(255,255,0),width=LW)
    #layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=2)
    #layer.draw.circle((xc,yc),r,outline=(0,0,0,255),fill=(255,255,255),width=LW)
    #layer.draw.circle((xc,yc),r,outline=(0,0,0,255),width=LW)
    
    draw_ecl_equ(layer.im,layer.draw,xc,yc,rx,year,tz,rr,requ,color_f=color_f)