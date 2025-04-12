from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
from config import config
from g_share import g_share
from datetime import datetime
import pytz
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import EarthLocation
from astropy.utils.iers import conf
conf.iers_degraded_accuracy = 'warn'


from dxt_rl import *
from dxt_zp import build_dxt_zp
from legend_mag import plot_legend_mag_at
from legend_sp import plot_legend_sp_at
from cir_hor_time_over import add_cir_hor_time_over
from ut_geo_tz import *
from ut_cal import *
import qrcode
from def_plnt import K_SUN
from table_jieqi_to_zod_and_zhemonth import table_jieqi_to_zod_and_zhemonth
from pathlib import Path
import platform

# 假设本地文件路径为 d:\kcf\inter\finals2000A.all
if platform.system()=='Linux':
    local_file_path = Path(config.interpath,'finals2000A.all')
else:    
    local_file_path = Path(r'd:\kcf\inter\finals2000A.all')
# 将本地文件路径转换为 file:// 格式的 URL
file_url = local_file_path.as_uri()

# 设置 iers_auto_url 为 file:// 格式的 URL
conf.iers_auto_url = file_url

def day_cald(draw,x,y,year,month,day,hour=0,minute=0,show_hm=False,tzn=8):
    ystep=100
    font=unicode_font_80
    font1=unicode_font_42
    yrfont = unicode_font_80
    FCOLOR=(0,0,0,255)
    cald = CALENDAR(year,month,day,hour,minute)
    wd,cwd = cald.weekday()
    year,cyear,lyear = cald.year()
    month,cmonth,lmonth,gz_month = cald.month()
    day, cday, lday, gz_day = cald.day()
    hour,chour,gz_hour = cald.hour()
    minute,cminute = cald.minute()
    #if show_year:
    txt_year = cyear+lyear
        #print(txt)
        #draw.text((x,y),txt,font=yrfont,fill=FCOLOR)
        #y+=50
    txt = cmonth+cday+' '+cwd
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    y+=ystep
    txt = lmonth + lday
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    y+=ystep
    txt = gz_month
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    y+=ystep
    txt = gz_day
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    y+=ystep
    txt = gz_hour
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    if show_hm:
        y+=ystep
        draw.text((x,y), text='%02d:%02d' % (hour,minute), font=font,
            fill=FCOLOR)
        y+=ystep
        draw.text((x,y), text='%+.1f時區' % tzn, font=font1,
            fill=FCOLOR)
        

    return txt_year


def make_dxt_kz_A5R(dt,latv,longv,place,timezone,psize='A5'):
    second=0
    if latv <0:
        g_share.f_south=True
    else:
        g_share.f_south=False
    year = dt.year
    month = dt.month
    day = dt.day
    hour= dt.hour
    minute = dt.minute
    tzn = get_timezone_offset(timezone)
    lst = cal_lst(latv,longv,dt,timezone)
    
    paper = PAPER(psize)
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

    layer0 = paper.add_layer(name='0')    
    xc = config.xc1
    yc = config.yc1
    layer0.draw.circle((xc,yc),r1,fill=YELLOW)
    layer0.draw.circle((xc,yc),r3, fill=WHITE)
    xc = config.xc1
    yc = config.yc1

    
    layer_bg = paper.add_layer(name='bg')
    if g_share.f_south:
        fn = Path(config.interpath, config.fbg_a5r_yw_s % year)
    else:
        fn = Path(config.interpath, config.fbg_a5r_yw_n % year) 
    im_bg=Image.open(fn)
    
    layer_bg.im.paste(im_bg, (0,0))
    
    cal_planet_info(year,month,day,hour,minute,tzn)
    
    add_sky_plnt(paper, xc, yc,r1,r5, r5b,rr,
                    year,month,day,hour,minute,tzn)

    print('sun_lon:', g_share.sun_lon)
    layer_zp = paper.add_layer(name='zp')

    from def_sky import r1,r2,r3,rr
    sun_ra=g_share.pln_0[K_SUN].ra

    
    xc1 = config.xc1
    yc1 = config.yc1

    build_dxt_zp(layer_zp.im,xc1,yc1,r1,r2,r3,rr,latv,
                                      longv=longv,place=place,tz=tzn,lst=lst,
                show_t_cir=False)
    add_cir_hor_time_over(paper,xc1,yc1,r2,r3,hour,minute,second,sun_ra)
    
    x=OFS_X
    y=OFS_Y + 100 
    layer_cald = paper.add_layer(name='calendar')
    txt_year=day_cald(layer_cald.draw,x,y,year,month,day,hour,minute,show_hm=True,tzn=tzn)
    draw_txt_year(layer_cald.draw,x,y-100,txt_year)
    
    x= int(3*MM_UNIT)
    y= int(150*MM_UNIT)
    table_jieqi_to_zod_and_zhemonth(paper, x,y, sun_lon=g_share.sun_lon,header_f=False)
     
    skip="""
    x0=int(91 *MM_UNIT)
    x1=int(x0+ 118 * MM_UNIT)
    y0=0
    y1=int(16 * MM_UNIT)
    """
    return paper


if __name__=='__main__':
    use_current_time=False
    # override current_time
    year = 2025
    month=2
    day=28
    hour=18
    minute= 30
    
    import datetime
    config.debug=False
    timezone='Asia/Hong_Kong'    
    loc_tz = pytz.timezone(timezone)
    if use_current_time:
        utc_now = datetime.datetime.utcnow()
        # Convert the UTC time to the specified timezone
        dt = utc_now.replace(tzinfo=pytz.utc).astimezone(loc_tz)
    else:
        input_str = '%02d/%02d/%d %02d:%02d:%02d' % (day,month,year,hour,minute,0)
        dt = datetime.datetime.strptime(input_str, '%d/%m/%Y %H:%M:%S')
    
    print(dt)
    
    year = dt.year
    month= dt.month
    day= dt.day
    hour = dt.hour
    minute= dt.minute
    second=0



    latv=22.5
    longv=114.5
    place='香港'

    fnx='dxt_kz_%s_%02d_%02dt%02d_%02d_%s_%s_%s_A5R.pdf' % (year,month,day,
                                                           hour,minute,
                                                          latv,longv,place)
    fn = '/kcf/dxtc2/%s' % fnx



    paper= make_dxt_kz_A5R(dt,latv,longv,place,timezone)

    layer_qrc = paper.add_layer(name='qrc')
    url ='https://kcfkwok.pythonanywhere.com/?content=rl-%s-%s-%s' % (year,month,day)
    #url ='http://127.0.0.1:5000/?content=rl-%s-%s-%s' % (year,month,day)
    
    img = qrcode.make(url)
    x= int(110 *MM_UNIT)
    y= int(120 *MM_UNIT)
    layer_qrc.im.paste(img, (x,y))
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    paper.commit_image(fn)
    
    #display(paper.im)
