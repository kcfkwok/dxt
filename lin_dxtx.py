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
    #tz=8

    timezone = 'Asia/Hong_Kong'
    tz = get_timezone_offset(timezone)
    print("tz:", tz)
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year

    paper = PAPER("A4L")
    build_lin_frame(paper, year-1, tz)
    draw_milkyway_lin(paper)
    layer_equ= paper.add_layer(name='equ')
    # draw equator again
    layer_equ.draw.line([(g_share.x0,g_share.y_equ),(g_share.xr_end,g_share.y_equ)],fill=RED,width=2)
    draw_sky_ecl(paper, year, tz)
    draw_fix_stars(paper)

    layer_cald = paper.add_layer(name='calendar')
    x = int(106 * MM_UNIT)
    y = int(18 * MM_UNIT)
    title = '%s年 全天星圖' % (year, )
    layer_cald.draw.text((x,y), text=title, font=unicode_font_112,fill=(0,0,0))

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
    
    title = '探索'
    x= int(12* MM_UNIT)
    y= int(config.MARGIN+ 16 * MM_UNIT)
    url = 'https://kcfkwok.pythonanywhere.com/lin_dxt'
    add_qrcode(layer.im, layer.draw, x,y, title, url)
    
    paper.commit_image(fn_pdf)
