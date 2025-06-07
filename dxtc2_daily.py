from config import config
from g_share import g_share
from sky_mw import app_mw
from sky_dt import app_dt_yr
from sky_bg import app_bg
from sky_rl_bg import make_dxt_rl_A4_bg, make_dxt_rl_A5R_bg
from dxt_xt import make_dxt_xt_A4
from dxt_rl import make_dxt_rl_A4
from table_plnt_info import table_plnt_info
from table_jieqi_to_zod_and_zhemonth import table_jieqi_to_zod_and_zhemonth
from pathlib import Path

if __name__=='__main__':
    import os
    import platform
    import pytz
    import datetime
    from PIL import Image
    from paper import *
    
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    month = now.month
    day = now.day
    
    config.debug=False
    x = config.banner_x
    y = config.banner_y
    
    cx=config.color_sky_day
    g_share.color_sky=(cx[0],cx[1],cx[2],255)
    g_share.color_cst_line=(0,0,0)
    
    # fskyl = '/home/kcfkwok/inter'
    # fmw_n = 'skyl_mw_n_j2000.png' # <- sky_mw.py
    # fmw_s = 'skyl_mw_s_j2000.png' # <- sky_mw.py
    g_share.set_f_south(False)
    im =app_mw()
    fn = Path(config.interpath, config.fmw_n)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(True)
    im =app_mw()
    fn = Path(config.interpath, config.fmw_s)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    
    # fdt_n = 'skyl_dt_n.y%s.png' # % year <- sky_dt.py
    # fdt_s = 'skyl_dt_s_y%s.png' # % year <- sky_dt.py
    g_share.set_f_south(False)
    im =app_dt_yr(year)
    fn =Path(config.interpath, config.fdt_n % year) 
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(True)
    im =app_dt_yr(year)
    fn =Path(config.interpath, config.fdt_s % year)     
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    # fbg_n = 'skyl_bg_n_j2000.png' #  <- sky_bg.py
    # fbg_s = 'skyl_bg_s_j2000.png' #   <-  sky_bg.py
    g_share.set_f_south(False)
    im =app_bg(year)
    fn = Path(config.interpath, config.fbg_n)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(True)
    im =app_bg(year)
    fn = Path(config.interpath, config.fbg_s)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    # fbg_rl = 'skyl_rl_bg_y%s.png' # % year <- sky_rl_bg.py
    # fbg_a5r_yw_n = 'skyl_bg_n_y%s_A5R_yw.png' # % year <- sky_rl_bg.py
    # fbg_a5r_yw_s = 'skyl_bg_s_y%s_A5R_yw.png' # % year <- sky_rl_bg.py
    
    paper= make_dxt_rl_A4_bg(year)
    fn = Path(config.interpath, config.fbg_rl % year) 
    img =paper.commit_image()
    img.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(False)
    paper= make_dxt_rl_A5R_bg(year)
    fn = Path(config.interpath, config.fbg_a5r_yw_n % year) 
    img =paper.commit_image()
    img.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    g_share.set_f_south(True)
    paper= make_dxt_rl_A5R_bg(year)
    fn = Path(config.interpath, config.fbg_a5r_yw_s % year) 
    img =paper.commit_image()
    img.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
    
    # dxt_xt -> dxt_xt_A4.png , pdf
    fpng = config.fxt_png
    fpdf = config.fxt_pdf
    
    paper= make_dxt_xt_A4(year)
    layer = paper.add_layer(name='banner')
    banner_path=config.fpng_banner
    banner = Image.open(banner_path)
    layer.im.paste(banner, (x,y))
    paper.commit_image(fpng)
    paper.commit_image(fpdf)
    
    # dxt_rl -> dxt_rl_A4.pdf, png
    fpng = config.frl_png
    fpdf = config.frl_pdf
    paper= make_dxt_rl_A4(year,month,day)
        
    layer = paper.add_layer(name='banner')
    banner_path=config.fpng_banner
    banner = Image.open(banner_path)
    layer.im.paste(banner, (x,y))
    
    hour=0
    minute=0
    
    x=int(150*MM_UNIT)
    y=int(167*MM_UNIT)
    table_plnt_info(paper,x,y,year,month,day,hour,minute,timezone)
    
    sun_lon = g_share.sun_lon
    x=int(130 *MM_UNIT)
    y=int(145* MM_UNIT)
    table_jieqi_to_zod_and_zhemonth(paper, x,y,sun_lon=sun_lon)
    
      
    paper.commit_image(fpng)
    paper.commit_image(fpdf)
