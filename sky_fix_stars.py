
from ut_star import *

def add_fix_stars(paper,xc,yc,rx,year,tz,rr,requ,im=None,draw=None,
                  ):
    LW=2
    if im is not None:
        #draw.circle((xc,yc),rx,fill=color_sky)
        draw_fix_stars(draw,xc,yc,rr)
        return
    
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer = paper.add_layer(name='cir_date')
    #layer.draw.circle((xc,yc),rx,fill=color_sky)
    draw_fix_stars(layer.draw,xc,yc,rr) 
    