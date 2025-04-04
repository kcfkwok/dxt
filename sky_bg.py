from config import config
from g_share import g_share
from paper import *
from sky_ecl_equ import add_ecl_equ
from cir_RA import add_cir_RA
from def_color import *
from cir_jieqi import add_cir_jieqi
from sky_fix_stars import add_fix_stars

def draw_cir_and_sky(paper,xc,yc,r1,r2,r3,r4,r5,rr,requ,tz,year,
                     im=None,draw=None,color_sky=config.color_sky_day):
    if im is not None:
        add_cir_jieqi(None,xc,yc,r4,year,tz,im=im,draw=draw)
        add_ecl_equ(None,xc,yc,r5,year,tz,rr,requ,im=im,draw=draw)
        add_cir_RA(None,xc,yc,r5,im=im,draw=draw)
        
        add_fix_stars(None,xc,yc,r3,year,tz,rr,requ,im=im,draw=draw)
        
def app_bg(year, fn=None):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    from IPython.display import display
    from config import config
    paper = PAPER("B6")

    OFS_X=300
    OFS_Y=200
    LW=2
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    r1 = round(2.333 * DPI) #1400 #1350 
    #xc = int((MAX_X- MIN_X) /2) + MIN_X
    xc = OFS_X + r1
    yc = xc + OFS_Y #int((MIN_Y+ MAX_Y)/2)
    #r0 = xc - MIN_X
    ra = r1+ 50
    rb = ra + 50
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r1a = r1 -30
    r2a = r2 - 30
    r4a = r4 - 30
    r5a = r5 -30 # for ra marker
    
    r_90=r5
    rr = 180/r_90
    requ = int(r_90/2)

    month=1
    day=1
    hour=0
    minute=0
    tz=8
    print('r1:%s mm' % (r1/MM_UNIT))
    w = h= int(120 * MM_UNIT)
    xc = yc = int(60 * MM_UNIT)
    layer_n = paper.add_layer(w,h,0,0,'sky_bg_n')
    im = layer_n.im
    draw = layer_n.draw
    draw_cir_and_sky(None,xc,yc,r1,r2,r3,r4,r5,rr,requ,tz,year,im=im,draw=draw)
    
    return im
	
if __name__=='__main__':
    year = 2025
    config.debug=False
    
    g_share.color_cst_line=(0,0,0)
    
    config.f_south=False
    im =app_bg(year)
    fn = '%s/%s' % (config.fskyl, config.fbg_n)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
	
if __name__=='__main__':
    year = 2025
    config.debug=False
    
    g_share.color_cst_line = (0,0,0)
    
    config.f_south=True
    im =app_bg(year)
    fn = '%s/%s' % (config.fskyl, config.fbg_s)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)