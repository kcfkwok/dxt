from config import config
from paper import *
from cir_date import add_cir_date
from def_font import *

def app_dt_yr(year, fn=None):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    from IPython.display import display
    from config import config
    paper = PAPER("B6")
    #paper.draw_outline()
    #paper.draw_MAX_RECT()
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
    r0 = xc - MIN_X
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
    #draw_cir_and_sky(None,xc,yc,r1,r2,r3,r4,r5,rr,requ,tz,year,im=im,draw=draw)
    add_cir_date(None,xc,yc,r3,year,tz,rr,requ,im=im,draw=draw)
    
    return im
	
	
if __name__=='__main__':
    import pytz
    import datetime
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.utcnow()
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
        
    config.debug=False
    g_share.f_south=False
    im =app_dt_yr(year)
    fnx = config.fdt_n % year
    fn = '%s/%s' % (config.fskyl, fnx)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
	
	
if __name__=='__main__':
    import pytz
    import datetime
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.utcnow()
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year

    config.debug=False
    g_share.f_south=True
    im =app_dt_yr(year)
    fnx = config.fdt_s % year
    fn = '%s/%s' % (config.fskyl, fnx)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
