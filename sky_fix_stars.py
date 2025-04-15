
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
    
def add_lmc_smc(draw,xc,yc,rr):
    MC_COLOR=(200,200,200,255)
        # 大麦哲伦星云
    lmc_ra_hms = '05h23m34.5s'
    lmc_dec_dms = '-69d45m22s'
    lmc_ra,lmc_dec=ra_dec_to_deg(lmc_ra_hms, lmc_dec_dms)
    # 小麦哲伦星云
    smc_ra_hms = '00h52m44.8s'
    smc_dec_dms = '-72d49m43s'
    smc_ra,smc_dec=ra_dec_to_deg(smc_ra_hms, smc_dec_dms)
    
    # 定义大小麦哲伦星云的角直径（近似值）
    lmc_r= MAG_N_R 
    smc_r = int(MAG_N_R * 0.53)
    #lmc_r = 6.5/2 # * u.deg
    #smc_r = 3.5 /2 # * u.deg
    draw_obj(draw, smc_ra,smc_dec, smc_r, MC_COLOR, xc,yc,rr)
    draw_obj(draw, lmc_ra,lmc_dec, lmc_r, MC_COLOR, xc,yc,rr)