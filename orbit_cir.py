from ut_math import *
from paper import *
from def_font import *
from word_list import SIGNS

def draw_orbit_cir(im,draw,hxc,hyc,hr1,hr2,bgcolor1=None,bgcolor2=None):
    FCOLOR=(0,0,0,255)
    LW=2
    hr1a = hr1 - 30
    draw.circle((hxc,hyc),hr1,fill=bgcolor1,outline=FCOLOR,width=LW)
    draw.circle((hxc,hyc),hr2,fill=bgcolor2,outline=FCOLOR,width=LW)
    ang=0
    for i in range(12):
        if True:
            j= (i+9) % 12
            #print('ang:',ang)
            sin_ang = sn(ang)
            cos_ang = cs(ang)
            txt_ang = 270 - (ang-15)
            if txt_ang <0: 
                txt_ang=txt_ang + 360
            y1 = int(sin_ang*hr1 + hyc)
            y2 = int(sin_ang*hr2 + hyc)
            y1a = int(sin_ang*hr1a + hyc)
            sin_n = sn(ang-15)
            cos_n = cs(ang-15)
            ync = int(sin_n * hr1a + hyc)    
    
            x1 = int(cos_ang*hr1 + hxc)
            x2 = int(cos_ang*hr2 + hxc)
            draw.line([(x1,y1),(x2,y2)],fill=FCOLOR,width=2)
            x1a = int(cos_ang*hr1a + hxc)
            xnc = int(cos_n * hr1a + hxc)
            draw_text(im, SIGNS[j], unicode_font,xnc,ync,txt_ang)
    
            skip='''
            x1 = int(cos_ang*hr1 + hxc_b)
            x2 = int(cos_ang*hr2 + hxc_b)
            draw.line([(x1,y1),(x2,y2)],fill=FCOLOR,width=2)
            x1a = int(cos_ang*hr1a + hxc_b)
            xnc = int(cos_n * hr1a + hxc_b)
            draw_text(im, SIGNS[j], unicode_font,xnc,ync,txt_ang)
            '''
        
            ang-=30
            if ang <0:
                ang = ang+360
