from ut_math import *
from ut_cal import *
from paper import *
from def_font import *


def draw_hor_time_over(im, draw,xc,yc,r2,r3,hour,minute,second,sun_ra):
    # plot hour angle marking
    from config import config
    f_south = config.f_south
    ari_ang = config.ari_ang
    
    FCOLOR=(0,0,0,255)
    LW=2
    r2a = r2 -30
    r2b = r2 -40
    skip="""
    tzhr = tz - (longv/15)
    tzdt = tzhr * 60
    tzdg = tzdt /4
    #ang= tzdg  #270 - ari_ang -180  # when ari_ang=90, ang=0
    # test
    hr=0
    if f_south:
        ang=270 - tzdg
    else:
        ang=270 + tzdg
    txt_ang=270 - ang
    """
    #-------------
    s_hr = hour + (minute/60) + (second/3600)
    s_hr_ang = s_hr * 15
    s_ra = sun_ra - 270
    if s_ra <0 :
        s_ra += 360
    s_hr0_ang = s_ra + s_hr_ang
    
    print("sun_ra:", sun_ra)
    print('s_hr:', s_hr)
    print('s_hr_ang:', s_hr_ang )
    print('s_hr0_ang:', s_hr0_ang)
    
    hr= 0
    if f_south:
        ang = 180 - s_hr0_ang
    else:
        ang= s_hr0_ang #270
    txt_ang = 270-ang
            
    for i in range(24): #24):
        sin_ang = sn(ang)
        cos_ang = cs(ang)
        #continue
        x2 = int(cos_ang*r2 + xc)
        y2 = int(sin_ang*r2 + yc)
        x2a = int(cos_ang*r2a + xc)
        y2a = int(sin_ang*r2a + yc)
        x3 = int(cos_ang*r3 + xc)
        y3 = int(sin_ang*r3 + yc)
        draw.line([(x3,y3),(x2a,y2a)],fill=FCOLOR,width=LW)   
        
        xnc = int(cos_ang * r2a + xc)
        ync = int(sin_ang * r2a + yc)
    
        draw_text(im,'%02d' % hr, unicode_font_42,xnc,ync,txt_ang)
        dprint('** hr:%s ang:%s' % (hr,ang))

        # Subdivision marker 6 division, 15/6 = 2.5
        for k in range(1,6):
            j=-k
            sin_ang = sn(ang+2.5*j)
            cos_ang = cs(ang+2.5*j)
            x2 = int(cos_ang*r2 + xc)
            y2 = int(sin_ang*r2 + yc)
            x3 = int(cos_ang*r3 + xc)
            y3 = int(sin_ang*r3 + yc)

            x2b = int(cos_ang*r2b + xc)
            y2b = int(sin_ang*r2b + yc)

            draw.line([(x3,y3),(x2b,y2b)],fill=FCOLOR,width=LW)
 
        #break
        if f_south:
            hr +=1
            ang +=15
            if hr > 23:
                hr=0
        else:
            hr -=1
            ang += 15
            if hr <0:
                hr=23

        txt_ang = 270 -ang
        if txt_ang <0:
            txt_ang =360+txt_ang


def add_cir_hor_time_over(paper,xc,yc,r2,r3,hour,minute,second,sun_ra,im=None,draw=None): 
    #hour,minute,second,sun_ra,im=None,draw=None):
    LW=2
    
    if im is not None:
        draw.circle((xc,yc),r2,outline=(0,0,0,255),width=LW)
        draw_hor_time(im,draw,xc,yc,r2,r3,hour,minute,second,sun_ra)
        return
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer = paper.add_layer(name='cir_zhe')
    #layer.draw.circle((xc,yc),r1,outline=(0,0,0,255),fill=(255,255,0),width=LW)
    #layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=2)
    #layer.draw.circle((xc,yc),r,outline=(0,0,0,255),fill=(255,255,255),width=LW)
    layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=LW)
    draw_hor_time_over(layer.im,layer.draw,xc,yc,r2,r3,hour,minute,second,sun_ra)

    
