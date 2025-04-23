from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
from config import config
from paper import *
from ut_cal import *
#from sky_plnt import add_sky_plnt
from legend_mag import *
from legend_sp import *
from pathlib import Path
from g_share import g_share

def make_dxt_rl_A4_bg(year):
    month=1
    day=1
    hour=0
    minute=0
    tz=8
    
    g_share.set_f_south(False)
    paper = PAPER("A4L")
    paper.draw_outline()
    #paper.draw_MAX_RECT()
    OFS_X=int(10 * MM_UNIT)
    OFS_Y=int(16 * MM_UNIT)
    LW=2
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    r1 = round(2.333 * DPI) #1400 #1350 
    #xc = int((MAX_X- MIN_X) /2) + MIN_X
    #xc = OFS_X + r1
    #yc = xc + OFS_Y #int((MIN_Y+ MAX_Y)/2)
    #r0 = xc - MIN_X
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r1a = r1 -30
    r2a = r2 - 30
    r4a = r4 - 30
    r5a = r5 -30 # for ra marker
    r5b = r5 -100 # planet name
    
    r_90=r5
    rr = 180/r_90
    requ = int(r_90/2)

    tz=8
    layer_bg = paper.add_layer(name='bg')
        
    xc = config.xc1 
    yc = config.yc1 
    fp_mw = Path(config.interpath, config.fmw_n)
    fp_bg = Path (config.interpath, config.fbg_n)
    fnx = config.fdt_n % year
    fp_dt = Path (config.interpath, fnx)
    for fp in [fp_mw,fp_bg,fp_dt]:
        imx = Image.open(fp)
        sx,sy = imx.size
        px = xc - int(sx/2)
        py = yc - int(sy/2)
        layer_bg.im.paste(imx, (px, py, px + sx, py + sy),imx)
    
    
    #cal_planet_info(year,month,day,hour,minute,tz)
    
    #add_sky_plnt(paper, xc, yc,r1,r5, r5b,rr,
    #                year,month,day,hour,minute,tz)
    #add_cir_zodiac(paper,xc,yc,r1,year,tz) 
    #add_cir_month_zhe(paper,xc,yc,r2,year,tz) 

    
    g_share.set_f_south(True)
    xc =config.xc2 
    yc =config.yc2
    fp_mw = Path(config.interpath, config.fmw_s)
    fp_bg = Path(config.interpath, config.fbg_s)
    fnx = config.fdt_s % year
    fp_dt = Path(config.interpath, fnx)
    for fp in [fp_mw,fp_bg,fp_dt]:
        imx = Image.open(fp)
        sx,sy = imx.size
        px = xc - int(sx/2)
        py = yc - int(sy/2)
        layer_bg.im.paste(imx, (px, py, px + sx, py + sy),imx)
        
    #add_sky_plnt(paper, xc, yc,r1,r5, r5b,rr,
    #                year,month,day,hour,minute,tz)
    #add_cir_zodiac(paper,xc,yc,r1,year,tz) #,im=im,draw=draw)
    #add_cir_month_zhe(paper,xc,yc,r2,year,tz) #,im=im,draw=draw)
        
    
    xt= OFS_X #- 550
    yt= yc+r1- int(8 * MM_UNIT)
    x = OFS_X + 160
    y = yt
    layer_mag = paper.add_layer(name='legend_mag')
    plot_legend_mag_at(layer_mag.im, layer_mag.draw,xt,yt,x,y,xofs=60)

    xt= OFS_X # r1 * 2 -300 + OFS_X
    yt= yc+r1 - int(2 * MM_UNIT)
    x = OFS_X + 160
    y = yt
    layer_sp = paper.add_layer(name='legend_sp')
    plot_legend_sp_at(layer_mag.im, layer_mag.draw,xt,yt,x,y,xofs=60)

    return paper


def make_dxt_rl_A5R_bg(year,cir_yellow=True):
    month=1
    day=1
    hour=0
    minute=0
    tz=8
    
    paper = PAPER("A5R")
    paper.draw_outline()
    #paper.draw_MAX_RECT()
    OFS_X=int(10 * MM_UNIT)
    OFS_Y=int(16 * MM_UNIT)
    LW=2
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    r1 = round(2.333 * DPI) #1400 #1350 
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r1a = r1 -30
    r2a = r2 - 30
    r4a = r4 - 30
    r5a = r5 -30 # for ra marker
    r5b = r5 -100 # planet name
    
    r_90=r5
    rr = 180/r_90
    requ = int(r_90/2)

    tz=8
    layer_bg = paper.add_layer(name='bg')
        
    xc = config.xc1 
    yc = config.yc1
    if cir_yellow:
        layer_bg.draw.circle((xc,yc),r1,fill=YELLOW)
        layer_bg.draw.circle((xc,yc),r3,fill=WHITE)
    
    if g_share.f_south ==False:
        fp_mw = Path (config.interpath, config.fmw_n)
        fp_bg = Path (config.interpath, config.fbg_n)
        fnx = config.fdt_n % year
    else:
        fp_mw = Path (config.interpath, config.fmw_s)
        fp_bg = Path (config.interpath, config.fbg_s)
        fnx = config.fdt_s % year
    
    fp_dt = Path(config.interpath, fnx)
    for fp in [fp_mw,fp_bg,fp_dt]:
        imx = Image.open(fp)
        sx,sy = imx.size
        px = xc - int(sx/2)
        py = yc - int(sy/2)
        layer_bg.im.paste(imx, (px, py, px + sx, py + sy),imx)
    

    xt= OFS_X #- 550
    yt= yc+r1- int(8 * MM_UNIT)
    x = OFS_X + 160
    y = yt
    layer_mag = paper.add_layer(name='legend_mag')
    plot_legend_mag_at(layer_mag.im, layer_mag.draw,xt,yt,x,y,xofs=60)

    xt= OFS_X # r1 * 2 -300 + OFS_X
    yt= yc+r1 - int(2 * MM_UNIT)
    x = OFS_X + 160
    y = yt
    layer_sp = paper.add_layer(name='legend_sp')
    plot_legend_sp_at(layer_mag.im, layer_mag.draw,xt,yt,x,y,xofs=60)

    return paper

if __name__=='__main__':
    import pytz
    import datetime
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    config.debug=False

    paper= make_dxt_rl_A4_bg(year)
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    fnx = config.fbg_rl % year
    fn = '%s/%s' % (config.fskyl, fnx)
    paper.commit_image()
    paper.im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    #paper.commit_image(fn)

if __name__=='__main__':
    import pytz
    import datetime
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    config.debug=False

    g_share.set_f_south(False)
    paper= make_dxt_rl_A5R_bg(year)
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    fnx = config.fbg_a5r_yw_n % year
    fn = '%s/%s' % (config.fskyl, fnx)
    paper.commit_image()
    paper.im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(True)
    paper= make_dxt_rl_A5R_bg(year)
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    fnx = config.fbg_a5r_yw_s % year
    fn = '%s/%s' % (config.fskyl, fnx)
    paper.commit_image()
    paper.im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    
    #paper.commit_image(fn)
