from def_color import *
from def_font import *
from ut_cal import *
from g_share import g_share

def draw_hour_angle_marking(im,draw,xc,yc,r5,fgcolor=BLACK,lw=2,
                            small=False):
    # plot hour angle marking
    if small:
        font = unicode_font_36

    else:
        font = unicode_font_42

    r5a = r5-15
    r5b = r5-30
        
    ang=Ra = 0
    if g_share.f_south:
        txt_ang=90
    else:
        txt_ang=270
    hr=18
    for i in range(24):
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)
        x5 = int(cos_ang*r5 + xc)
        y5 = int(sin_ang*r5 + yc)
        x5a = int(cos_ang*r5a + xc)
        y5a = int(sin_ang*r5a + yc)
        draw.line([(x5,y5),(x5a,y5a)],fill=fgcolor,width=lw)   
        xnc = int(cos_ang * r5b + xc)
        ync = int(sin_ang * r5b + yc)
    
        draw_text(im,'%02d' % hr, font,xnc,ync,txt_ang)
        
        # Subdivision marker 6 division
        for j in range(1,6):
            
            sin_ang = sn(ang+2.5*j)
            cos_ang = r_cs(ang+2.5*j)
            x5 = int(cos_ang*r5 + xc)
            y5 = int(sin_ang*r5 + yc)
            x5a = int(cos_ang*r5a + xc)
            y5a = int(sin_ang*r5a + yc)
            draw.line([(x5,y5),(x5a,y5a)],fill=fgcolor,width=lw)   
        
        hr +=1
        if hr > 23:
            hr=0
        ang += 15
        if g_share.f_south:
            txt_ang +=15
        else:
            txt_ang -= 15
        if txt_ang <0:
            txt_ang =360+txt_ang
        

def add_cir_RA(paper,xc,yc,r,im=None,draw=None,small=False):
    LW=2
    if im is not None:
        draw.circle((xc,yc),r,outline=(0,0,0,255),width=LW)
        draw_hour_angle_marking(im,draw,xc,yc,r,small=small)
        return
    
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y

    layer = paper.add_layer(name='RA_circle')
    layer.draw.circle((xc,yc),r,outline=(0,0,0,255),width=LW)
    
    draw_hour_angle_marking(layer.im,layer.draw,xc,yc,r,small=small)
