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

if __name__=='__main__':
    year=2025
    tz=8
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
    paper.commit_image(fn_pdf)
