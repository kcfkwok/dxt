from ut_star import *
from def_font import *
from paper import *

def plot_legend_mag_at(im, draw,xt,yt,x,y,xofs=100):
    FCOLOR=(0,0,0,255)
    draw.text((xt,yt), text='星等', font=unicode_font_42, fill=(0,0,0))

    for mag in [-1,0,1,2,3,4,5]:
        draw_text(im, '%d' % mag, unicode_font_36,x,y,0)
        r = mag_to_r(mag)
        draw.circle((x,y+50),r, outline=FCOLOR,fill=(255,255,255,255),width=2)
        x+= xofs
