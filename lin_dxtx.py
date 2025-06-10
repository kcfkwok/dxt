import sys
# 将子模块的路径添加到 Python 的模块搜索路径中
sys.path.append('../lin_dxt')

from g_share import g_share
from lin_base import *
from lin_RA import add_lin_RA
from lin_ecl import build_ecl_ras, add_lin_ecl
from lin_jieqi import add_lin_jieqi
from lin_sign import add_lin_sign
from lin_month_zhe import add_lin_month_zhe
from lin_dates import add_lin_dates
from lin_weeks import add_lin_weeks
from lin_lunars import add_lin_lunars
from lin_sky_ecl import draw_sky_ecl
from lin_sky_mw import draw_milkyway_lin
from ut_lin_star import draw_fix_stars
from lin_frame import build_lin_frame


def add_qrcode(im, draw, x,y, title, url):
    import qrcode
    #url='https://kcfkwok.pythonanywhere.com/?content=xt-0'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=9,
        border=1,
    )
    
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=(0,0,0), back_color=(255,255,255))
    
    sw,sh =img.size
    im.paste(img,(x,y,x+sw,y+sh))
    
    #text = '更新星圖'
    #draw_title(draw,x+int(1*MM_UNIT),y-100,title)
    
if __name__=='__main__':
    
    import pytz
    import datetime
    from ut_geo_tz import get_timezone_offset
    from ut_cal import cal_planet_at
    #tz=8

    timezone = 'Asia/Hong_Kong'
    tz = get_timezone_offset(timezone)
    print("tz:", tz)
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    month = now.month
    date = now.day
    ihour=0
    minute=0
    tz= 8
    cal_planet_at(year,month,date,ihour,minute,tz)
    sun_ra = g_share.sun_0.ra / 15.0 + 24
    print('sun_ra:', sun_ra)
    
    paper = PAPER("A4L")
    y7=build_lin_frame(paper, year-1, tz)
    
    draw_milkyway_lin(paper)
    layer_equ= paper.add_layer(name='equ')
    # draw equator again
    layer_equ.draw.line([(g_share.x0,g_share.y_equ),(g_share.xr_end,g_share.y_equ)],fill=RED,width=2)
    
    layer_sun = paper.add_layer(name='sun')
    sun_x = RA_to_x(g_share.x0, sun_ra)
    layer_sun.draw.line(((sun_x,g_share.y00),(sun_x,y7+int(3*MM_UNIT))),fill=RED,width=5)
    
    draw_sky_ecl(paper, year, tz)
    draw_fix_stars(paper)

    layer_cald = paper.add_layer(name='calendar')
    x = int(106 * MM_UNIT)
    y =  int(config.MARGIN+ 5* MM_UNIT)
    title = '%s年 星图年历' % (year, )
    layer_cald.draw.text((x,y), text=title, font=unicode_font_112,fill=(0,0,0))
    
    x= int(config.MARGIN+ 2*MM_UNIT)
    y= int(config.MARGIN+ 15*MM_UNIT)
    layer_cald.draw.text((x,y), text='南', font=unicode_font_112,fill=(0,0,0))
    
    x= int(g_share.xr_end+ int(0.5*MM_UNIT))
    y= int(config.MARGIN+ 15*MM_UNIT)
    layer_cald.draw.text((x,y), text='南', font=unicode_font_112,fill=(0,0,0))
    
    
    x= int(config.MARGIN+ 2*MM_UNIT)
    y= int(config.MARGIN+ 90*MM_UNIT)
    layer_cald.draw.text((x,y), text='西', font=unicode_font_112,fill=(0,0,0))
    
    x= int(config.MARGIN+ 2*MM_UNIT)
    y= int(config.MARGIN+ 170*MM_UNIT)
    layer_cald.draw.text((x,y), text='北', font=unicode_font_112,fill=(0,0,0))

    x= int(g_share.xr_end+ int(0.5*MM_UNIT))
    y= int(config.MARGIN+ 170*MM_UNIT)
    layer_cald.draw.text((x,y), text='北', font=unicode_font_112,fill=(0,0,0))
    
    x= int(g_share.xr_end+ int(0.5*MM_UNIT))
    y= int(config.MARGIN+ 90*MM_UNIT)
    layer_cald.draw.text((x,y), text='东', font=unicode_font_112,fill=(0,0,0))
    
    #layer = paper.add_layer(name='test')
    #draw = layer.draw
    #draw_cst(draw,'Tuc')
    #draw_cst(draw,'Sgr')
    x = config.banner_x
    y = config.banner_y
    layer = paper.add_layer(name='banner')
    banner_path=config.fpng_banner
    banner = Image.open(banner_path)
    layer.im.paste(banner, (x,y))


    fn_png = config.lin_dxt_png
    fn_pdf = config.lin_dxt_pdf
    paper.commit_image(fn_png)
    
    from ut_lin_cstbnd import lin_cstbnd_to_xyplot
    color_cstbnd = config.color_cstbnd
    from csts import CSTS
    from zodiac import zodiac

    CSTS.remove('Ser')
    CSTS.append('Ser1')
    CSTS.append('Ser2')
    for cst in CSTS:
        if cst in zodiac:
            continue
        print('get_cstbnd_polygon: ',cst)
        points = lin_cstbnd_to_xyplot(cst,form='tuple')
        try:
            layer.draw.polygon(points, outline=color_cstbnd,width=3)
        except Exception as e:
            print('points:',points)
            print('Exception:',str(e))

    for cst in ['Aps','Ara','Cep','CrA','Cyg','Del','Dra','Equ','Gru','Her','Ind','Lac','Lyr','Mic','Pav','Peg','PsA','Sge','Tel','Tuc','Vul']:
        if cst in zodiac:
            continue
        print('get_cstbnd_polygon: ',cst)
        points = lin_cstbnd_to_xyplot(cst,form='tuple', totalshift=True)
        try:
            layer.draw.polygon(points, outline=color_cstbnd,width=3)
        except Exception as e:
            print('points:',points)
            print('Exception:',str(e))
            
    color_cstbnd_zodiac = config.color_cstbnd_zodiac
    for cst in zodiac:
        print('get_cstbnd_polygon: ',cst)
        points = lin_cstbnd_to_xyplot(cst,form='tuple')
        layer.draw.polygon(points, outline=color_cstbnd_zodiac,width=3)
    for cst in ['Sgr','Cap','Aqr']:
        print('get_cstbnd_polygon: ',cst)
        points = lin_cstbnd_to_xyplot(cst,form='tuple', totalshift=True)
        layer.draw.polygon(points, outline=color_cstbnd_zodiac,width=3)

            
    title = '探索'
    x= int(12* MM_UNIT)
    y= int(config.MARGIN+ 16 * MM_UNIT)
    url = 'https://kcfkwok.pythonanywhere.com/lin_dxt'
    add_qrcode(layer.im, layer.draw, x,y, title, url)
    
    paper.commit_image(fn_pdf, excludes=[layer_sun])
