from starsln import starsln
from starsi import starsi
from csts import CSTS
from config import config
from g_share import g_share
g_share.stars_plotted=[]
from paper import *
from ut_cal import *

MAG_N_R = 12
MAG_0_R = 11
MAG_1_R = 9
MAG_2_R = 7
MAG_3_R = 5
MAG_4_R = 3
MAG_5_R = 2
MAG_X_R = 1

def mag_to_r(mag):
    if mag <0:
        r=MAG_N_R  #12
    elif mag <1:
        r=MAG_0_R  #11
    elif mag <2:
        r=MAG_1_R  #9
    elif mag <3:
        r=MAG_2_R   #7
    elif mag <4:
        r=MAG_3_R   #5
    elif mag <5:
        r=MAG_4_R   #3
    else:
        r=MAG_5_R   #2
    return r

SP_COLORS={
    'O': (0,183,235,255),
    'B':(0,255,255,255),
    'A':(224,255,255,255),
    'F':(255,255,255,255),
    'G':(238,255,27,255),
    'K':(255,140,0,255),
    'M':(255,0,0,255),
}

def SP_to_color(sp):
    if sp in SP_COLORS:
        return SP_COLORS[sp]
    return (255,255,255,0)


def draw_star(draw, star,xc,yc,rr,f_south,
              small=False,color_f=True):
    FCOLOR=(0,0,0,255)
    #BGCOLOR=(255,255,255,0)
    #LW=4
    Ra,decl,mag,sp= starsi[star]
    x,y =ra_dec_to_xyplot(Ra,decl,xc,yc,rr,f_south=f_south)
    #if star not in stars_plotted:
    r = mag_to_r(mag)
    if small:
        r= round(r/2)
    if color_f:
        co = SP_to_color(sp)
        if sp=='A' or sp=='F' or r >3:
            draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
        else:
            draw.circle((x,y),r,outline=co, fill=co,width=2)
    else:
        draw.circle((x,y),r,outline=FCOLOR,width=2)
        
        skip="""
        else:
            if CONFIG.STAR_USE_WHITE:
                draw.circle((x,y),r,outline=FCOLOR, fill=WHITE_COLOR,width=2)
            else:
                co = rgb_2_grey(SP_to_color(sp))
                if sp=='A' or sp=='F' or r >3:
                    draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
                else:
                    draw.circle((x,y),r,outline=co, fill=co,width=2)
        """    
        g_share.stars_plotted.append(star)
    return x,y
    
def draw_star_at(draw, star,x,y,color_f=True):
    FCOLOR=(0,0,0,255)
    #BGCOLOR=(255,255,255,0)
    #LW=4
    Ra,decl,mag,sp= starsi[star]
    r = mag_to_r(mag)
    if color_f:
        co = SP_to_color(sp)
        if sp=='A' or sp=='F' or r >3:
            draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
        else:
            draw.circle((x,y),r,outline=co, fill=co,width=2)
    else:
        draw.circle((x,y),r,outline=FCOLOR,width=2)
        

def draw_stars_with_line(draw,lstars,xc,yc,rr,f_south,
                         small=False,color_f=True):
    ls=1
    for star in lstars:
        x,y =draw_star(draw, star,xc,yc,rr,f_south,
                       small=small,color_f=color_f)
        if ls==1:
            ls=0
            x0=x
            y0=y
        else:
            draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2) 
            x0=x
            y0=y
    # draw stars over again
    for star in lstars:
        x,y =draw_star(draw, star,xc,yc,rr,f_south,
                       small=small,color_f=color_f)
 
def draw_cst(draw, cst,xc,yc,rr,f_south,small=False,color_f=True):
    for lstars in starsln[cst]:
        ls=1
        for star in lstars:
            x,y =draw_star(draw, star,xc,yc,rr,f_south,
                           small=small,color_f=color_f)
            if ls==1:
                ls=0
                x0=x
                y0=y
            else:
                if f_south:
                    if cst !='UMi':  # in south hemisphere, ignore UMi lines which locate in south pole
                        draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2)  
                else:
                    if cst !='Oct':  # in north hemisphere, ignore Oct lines which locate in south pole
                        draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2)
                x0=x
                y0=y
    # draw stars over again
    for lstars in starsln[cst]:
        for star in lstars:
            x,y =draw_star(draw, star,xc,yc,rr,f_south,
                           small=small,color_f=color_f)
                           
    
def draw_fix_stars(draw,xc,yc,rr,small=False,color_f=True):
    try:
        f_south = config.f_south
    except:
        from config import config
        f_south = config.f_south 
        
    skip='''
    def _draw_text(xy, text="", font=unicode_font_64,fill=FCOLOR,draw=draw):
        ss=convert(text, 'zh-hans')
        draw.text(xy, text=ss, font=font, fill=fill)
        '''
    g_share.stars_plotted=[]

    # plot stars and lines in constellations                
    for cst in CSTS:
        draw_cst(draw, cst,xc,yc,rr,f_south,small=small,color_f=color_f)
    
    # plot stars not in cst lines
    stars = list(starsi.keys())
    for star in stars:
        if star not in g_share.stars_plotted:
            draw_star(draw, star,xc,yc,rr,f_south,small=small,color_f=color_f)

