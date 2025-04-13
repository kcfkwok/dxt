from def_font import *
from ut_cal import *


def draw_date_mark(im,draw,xc,yc,rx,s_year,tz,rr,requ,small=False):
    if small:
        font =unicode_font_36
    else:
        font =unicode_font_42
        
    r3 = rx
    if small:
        DR3A = round(30/2)
        DR3B = round(45/2)
        DR3C = round(20/2)   
    else:
        DR3A = 30
        DR3B = 45
        DR3C = 20
    DR3D = 40    

    r3a = r3 -DR3A # for day 5,15,25
    r3b = r3 -DR3B # for day 10,20
    r3c = r3 -DR3C # for other days
    r3d = r3 -DR3D # for month text
    r4 = r3 -60
    
    FCOLOR = (0,0,0,255)
    LW=2
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
        sra, sdec, _ =SunValues(nd)
        ang = config.ari_ang + sra
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)
        x1 = int(cos_ang*r3 + xc)
        y1 = int(sin_ang*r3 + yc)
        x2 = int(cos_ang*r4 + xc)
        y2 = int(sin_ang*r4 + yc)
        if day==1:
            draw.line([(x1,y1),(x2,y2)],fill=FCOLOR,width=LW)
            if small:
                if f_south:
                    sin_n = sn(ang+4)
                    cos_n = r_cs(ang+4)
                else:
                    if month >= 10:
                        sin_n = sn(ang+5)
                        cos_n = r_cs(ang+5)
                    else:
                        sin_n = sn(ang+4)
                        cos_n = r_cs(ang+4)
                        
            else:
                sin_n = sn(ang+3)
                cos_n = r_cs(ang+3)
                
            xnc = int(cos_n * r3d + xc)
            ync = int(sin_n * r3d + yc)   
            if f_south:
                txt_ang = 90 + (ang+3)
            else:
                txt_ang = 270 - (ang+3)
                
            if txt_ang <0: 
                txt_ang=txt_ang + 360
            draw_text(im, '%d月' % month, font,xnc,ync,txt_ang)
            if month==1:
                if small:
                    if f_south:
                        ofs_ang=12
                    else:
                        ofs_ang=13
                else:
                    ofs_ang=8
                sin_ny = sn(ang+ ofs_ang)
                cos_ny = r_cs(ang+ ofs_ang)
                xnyc = int(cos_ny * r3d + xc)
                ynyc = int(sin_ny * r3d + yc)   
                if f_south:
                    txt_ang = 90 + (ang+ ofs_ang)
                else:
                    txt_ang = 270 - (ang+ ofs_ang)
                if txt_ang <0: 
                    txt_ang=txt_ang + 360
                draw_text(im, '%d年' % s_year, font,xnyc,ynyc,txt_ang)

                if small:
                    if f_south:
                        ofs_ang=12+ 12
                    else:
                        ofs_ang = 13+12
                else:
                    ofs_ang=8+8
                sin_ny = sn(ang+ ofs_ang)
                cos_ny = r_cs(ang+ ofs_ang)
                xnyc = int(cos_ny * r3d + xc)
                ynyc = int(sin_ny * r3d + yc)   
                if f_south:
                    txt_ang = 90 + (ang+ ofs_ang)
                else:
                    txt_ang = 270 - (ang+ ofs_ang)
                if txt_ang <0: 
                    txt_ang=txt_ang + 360
                draw_text(im, '時區%d' % tz, font,xnyc,ynyc,txt_ang)

                
        elif day in [11,21,31]:
            x1b = int(cos_ang*r3b + xc)
            y1b = int(sin_ang*r3b + yc)
            draw.line([(x1b,y1b),(x1,y1)],fill=FCOLOR,width=LW)
        elif day in [6,16,26]:
            x1a = int(cos_ang*r3a + xc)
            y1a = int(sin_ang*r3a + yc)
            draw.line([(x1a,y1a),(x1,y1)],fill=FCOLOR,width=LW)
        else:
            x1c = int(cos_ang*r3c + xc)
            y1c = int(sin_ang*r3c + yc)
            draw.line([(x1c,y1c),(x1,y1)],fill=FCOLOR,width=LW)



def add_cir_date(paper,xc,yc,rx,year,tz,rr,requ,im=None,draw=None,small=False):
    LW=2
    if im is not None:
        draw.circle((xc,yc),rx,outline=(0,0,0,255),width=LW)
        draw_date_mark(im,draw,xc,yc,rx,year,tz,rr,requ,small=small)
        return
    
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer = paper.add_layer(name='cir_date')
    #layer.draw.circle((xc,yc),r1,outline=(0,0,0,255),fill=(255,255,0),width=LW)
    #layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=2)
    #layer.draw.circle((xc,yc),r,outline=(0,0,0,255),fill=(255,255,255),width=LW)
    layer.draw.circle((xc,yc),rx,outline=(0,0,0,255),width=LW)
    
    draw_date_mark(layer.im,layer.draw,xc,yc,rx,year,tz,rr,requ,small=small)
	
	
