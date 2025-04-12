from paper import *
from def_font import *
from def_sky import *
from cir_hor_time_zhe import add_cir_hor_time_zhe
from cir_hor_time import add_cir_hor_time
from sky_hor_cir import add_hor_cir
from sym_pointer import draw_pointer
from config import config

def rotate(image,im2,x,y,angle):
    im2 = im2.rotate(angle, expand=1)
    sx, sy = im2.size
    print(sx,sy)
    px = x - int(sx/2)
    py = y - int(sy/2)
    print(px,py,sx,sy)
    image.paste(im2, (px, py, px + sx, py + sy), im2)
    
def build_dxt_zp(im0,xc0,yc0,r1,r2,r3,rr,latv,
                                      longv,place,tz,lst=0,show_t_cir=True):

    from g_share import g_share
    f_south=g_share.f_south
    LW=4
    stroke_width=1
    width=height = r1*2
    xc=yc = r1
    im = Image.new(mode='RGBA',size=(width, height),color=(255,255,255,0))
    draw = ImageDraw.Draw(im)
    add_cir_hor_time_zhe(None,xc,yc,r1,r2,im=im,draw=draw,stroke_width=stroke_width)
    if show_t_cir:
        add_cir_hor_time(None,xc,yc,r2,r3,longv,tz,im=im,draw=draw)
    #sun_ra=180
    #second=0
    #add_cir_hor_time(None,xc,yc,r2,r3,hour,minute,second,sun_ra,im=im,draw=draw)
    add_hor_cir(None,xc,yc,r2,rr,latv,0,longv,place,im=im,draw=draw)
    
    draw.circle((xc,yc),r3,outline=(0,0,0,255),width=LW)
    draw.circle((xc,yc),r4,outline=(0,0,0,255),width=LW)
    draw.circle((xc,yc),r5,outline=(0,0,0,255),width=LW)
    
    # draw cross mark at center
    draw.line([(xc+10, yc-10),(xc-10,yc+10)], fill=(255,0,0,255), width=LW)
    draw.line([(xc+10, yc+10),(xc-10,yc-10)], fill=(255,0,0,255), width=LW)
    
    if f_south:
        rot_ang = lst
    else:
        rot_ang = 360-lst
    
    #rot_ang -=2.5   # note: some errors here ********
    #layer = paper.add_layer()
    rotate(im0,im,xc0,yc0,rot_ang)


def build_dxt_zp_A4L(latv, longv, place, time_zone, debug=False):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    import datetime
    from ut_geo_tz import get_location_info, get_timezone_offset
    from astropy.coordinates import EarthLocation
    from astropy.time import Time
    from astropy import units as u
    from astropy.utils.iers import conf
    conf.iers_degraded_accuracy = 'warn'

    from config import config
    import pytz
    from datetime import datetime
    
    config.debug=debug
    #year = 2025
    config.debug=False
    skip="""
    config.xc1 = int(70 * MM_UNIT)
    config.yc1 = int(77 * MM_UNIT)
    #config.fbg_n = 'd:/kcf/dxtc/skyls_bg_n_y%s.png' % year
    config.xc2 = int(70 * MM_UNIT *2 + 60 * MM_UNIT)
    config.yc2 = int(77 * MM_UNIT)
    """
    #config.fbg_s = 'd:/kcf/dxtc/skyls_bg_s_y%s.png' % year
    #if time_zone is None:
    #    location, time_zone, err_msg =    get_location_info(latv, longv)
    #tz=8
    tz = get_timezone_offset(time_zone)
    
    paper = PAPER("A4L")
    paper.draw_outline()

    OFS_Y=200
    LW=4
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    #xc = int((MAX_X- MIN_X) /2) + MIN_X
    #yc = xc + OFS_Y #int((MIN_Y+ MAX_Y)/2)
    #r0 = xc - MIN_X
    r1 = round(2.333 * DPI) #1400 #1350 
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r5a = r5 -30 # for ra marker
    r5b = r5 -100 # planet name
    
    layer0 = paper.add_layer(name='0')
        
    g_share.f_south=False
    xc = config.xc1
    yc = config.yc1
    layer0.draw.circle((xc,yc),r1,fill=YELLOW)
    layer0.draw.circle((xc,yc),r3, fill=WHITE)
    layer1 = paper.add_layer()
    build_dxt_zp(layer1.im,xc,yc,r1,r2,r3,rr,latv,
                                      longv=longv,place=place,tz=tz)
    x0= xc - int(60 * MM_UNIT)
    y0= yc - int(60 * MM_UNIT)
    l0 = int(120 * MM_UNIT)
    layer1.draw.rectangle([(x0,y0), (x0+l0,y0+l0)], outline=RED, width=2)
    layer1.draw.text((x0+100,y0-50), text='120 mm',font=unicode_font_48, fill=RED)
    
    g_share.f_south=True
    xc = config.xc2
    yc = config.yc2
    layer0.draw.circle((xc,yc),r1,fill=YELLOW)
    layer0.draw.circle((xc,yc),r3, fill=WHITE)
    layer2 = paper.add_layer()
    build_dxt_zp(layer2.im,xc,yc,r1,r2,r3,rr,latv,
                                      longv=longv,place=place,tz=tz)
    x0= xc - int(60 * MM_UNIT)
    y0= yc - int(60 * MM_UNIT)
    l0 = int(120 * MM_UNIT)
    layer1.draw.rectangle([(x0,y0), (x0+l0,y0+l0)], outline=RED, width=2)
    layer1.draw.text((x0+100,y0-50), text='120 mm',font=unicode_font_48, fill=RED)
    
    
    layer_ptr = paper.add_layer(MAX_X,MAX_Y,MIN_X,MIN_Y)
    L0 = int(5 *MM_UNIT)
    L1 = int(64 *MM_UNIT)
    W0 = int(3 * MM_UNIT)
    W1 = int(7 * MM_UNIT)
    iangle=270
    x= int(20 * MM_UNIT)
    y =int(170 * MM_UNIT)
    for i in range(2):
        draw_pointer(layer_ptr.im,x,y,rr,L0,L1,W0,W1,iangle,RED,YELLOW,
                     f_south=False)
        draw_pointer(layer_ptr.im,x+L1+L0,y,rr,L0,L1,W0,W1,iangle,RED,YELLOW,
                     f_south=True)
        y+= W0+W1
        

    return paper


def build_dxt_zp_A5(latv, longv, place, time_zone, f_south=False, debug=False):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    import datetime
    from ut_geo_tz import get_location_info, get_timezone_offset
    from astropy.coordinates import EarthLocation
    from astropy.time import Time
    from astropy import units as u
    from astropy.utils.iers import conf
    conf.iers_degraded_accuracy = 'warn'

    from config import config
    import pytz
    from datetime import datetime
    
    config.debug=debug
    #year = 2025
    config.debug=False
    tz = get_timezone_offset(time_zone)
    
    paper = PAPER("A5")
    paper.draw_outline()

    OFS_Y=200
    LW=4
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    #xc = int((MAX_X- MIN_X) /2) + MIN_X
    #yc = xc + OFS_Y #int((MIN_Y+ MAX_Y)/2)
    #r0 = xc - MIN_X
    r1 = round(2.333 * DPI) #1400 #1350 
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r5a = r5 -30 # for ra marker
    r5b = r5 -100 # planet name
    
    layer0 = paper.add_layer(name='0')
        
    g_share.f_south=f_south
    xc = config.xc1
    yc = config.yc1
    layer0.draw.circle((xc,yc),r1,fill=YELLOW)
    layer0.draw.circle((xc,yc),r3, fill=WHITE)
    layer1 = paper.add_layer()
    build_dxt_zp(layer1.im,xc,yc,r1,r2,r3,rr,latv,
                                      longv=longv,place=place,tz=tz)
    x0= xc - int(60 * MM_UNIT)
    y0= yc - int(60 * MM_UNIT)
    l0 = int(120 * MM_UNIT)
    layer1.draw.rectangle([(x0,y0), (x0+l0,y0+l0)], outline=RED, width=2)
    layer1.draw.text((x0+100,y0-50), text='120 mm',font=unicode_font_48, fill=RED)
    
    
    layer_ptr = paper.add_layer(MAX_X,MAX_Y,MIN_X,MIN_Y)
    L0 = int(5 *MM_UNIT)
    L1 = int(64 *MM_UNIT)
    W0 = int(3 * MM_UNIT)
    W1 = int(7 * MM_UNIT)
    iangle=270
    x= int(7 * MM_UNIT)
    y =int(170 * MM_UNIT)
    for i in range(2):
        draw_pointer(layer_ptr.im,x,y,rr,L0,L1,W0,W1,iangle,RED,YELLOW,
                     f_south=False)
        draw_pointer(layer_ptr.im,x+L1+L0,y,rr,L0,L1,W0,W1,iangle,RED,YELLOW,
                     f_south=True)
        y+= W0+W1
        

    return paper

def testA4L():
    latv = 22.5
    longv=114
    place='香港'
    time_zone='Asia/Hong_Kong'
    config.hor_cir_opacity = 255
    paper =build_dxt_zp_A4L(latv,longv,place, time_zone)
    
    fnx='dxt_zp_%s_%s_%s_A4.pdf' % (latv,longv,place)
    fn = 'd:/kcf/dxtc2/%s' % fnx
    paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    #paper.draw_mid_vline()
    paper.commit_image(fn)

def testA5_fn():
    latv = 22.5
    longv=114
    place='香港'
    time_zone='Asia/Hong_Kong'
    config.hor_cir_opacity = 255
    paper =build_dxt_zp_A5(latv,longv,place, time_zone, f_south=False)
    
    fnx='dxt_zp_%s_%s_%s_fn_A5.pdf' % (latv,longv,place)
    fn = 'd:/kcf/dxtc2/%s' % fnx
    paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    #paper.draw_mid_vline()
    paper.commit_image(fn)
    
def testA5_fs():
    latv = 22.5
    longv=114
    place='香港'
    time_zone='Asia/Hong_Kong'
    config.hor_cir_opacity = 255
    paper =build_dxt_zp_A5(latv,longv,place, time_zone, f_south=True)
    
    fnx='dxt_zp_%s_%s_%s_fs_A5.pdf' % (latv,longv,place)
    fn = 'd:/kcf/dxtc2/%s' % fnx
    paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    #paper.draw_mid_vline()
    paper.commit_image(fn)

if __name__=='__main__':
    testA5_fn()
    testA5_fs()
