from ut_star import *
from def_font import *
from paper import *

def plot_legend_sp_at(im, draw,xt,yt,x,y,xofs=100):
    FCOLOR=(0,0,0,255)
    draw.text((xt,yt), text='光譜型', font=unicode_font_42, fill=(0,0,0))
    for sp in ['O','B','A','F','G','K','M']:
        draw_text(im, sp, unicode_font_36,x,y,0)
        co = SP_to_color(sp)
        r = mag_to_r(-1)
        draw.circle((x,y+50),r, outline=FCOLOR,fill=co,width=2)
        x+=xofs
