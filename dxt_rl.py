from config import config
from paper import *
from ut_cal import *
from sky_plnt import add_sky_plnt
from orbit_cir import draw_orbit_cir
from orbit_plnt import *
from ut_calendar import CALENDAR
from table_plnt_info import table_plnt_info
from table_jieqi_to_zod_and_zhemonth import table_jieqi_to_zod_and_zhemonth
from pathlib import Path

def draw_txt_year(draw, x,y, txt):
    yrfont = unicode_font_80
    FCOLOR=(0,0,0,255)
    draw.text((x,y),txt,font=yrfont,fill=FCOLOR)
    
def day_cald(draw,x,y,year,month,day,hour=0,minute=0,show_hm=False):
    ystep=100
    font=unicode_font_80
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

    return txt_year

def make_dxt_rl_A4(year,month,day,hour=0,minute=0):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    from IPython.display import display
    from g_share import g_share
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
    fn = Path(config.interpath, config.fbg_rl % year) 
    im_bg=Image.open(fn)
    layer_bg.im.paste(im_bg, (0,0))
    
    xc = config.xc1  #= int(70 * MM_UNIT)
    yc = config.yc1 #= int(85 * MM_UNIT)
    
    cal_planet_info(year,month,day,hour,minute,tz)
    
    add_sky_plnt(paper, xc, yc,r1,r5, r5b,rr,
                    year,month,day,hour,minute,tz)
    #add_cir_zodiac(paper,xc,yc,r1,year,tz) #,im=im,draw=draw)
    #add_cir_month_zhe(paper,xc,yc,r2,year,tz) #,im=im,draw=draw)
    #draw_cir_and_sky(paper,xc,yc,r1,r2,r3,r4,r5,rr,requ,tz,year)
    
    g_share.set_f_south(True)
    #xc = xc+ 2*r1 + 400
    #xc = int(70 * MM_UNIT *2 + 60 * MM_UNIT)
    #fp_s = 'd:/kcf/dxtc/skyls_bg_s_y%s.png' % year
    xc =config.xc2 #= int(70 * MM_UNIT *2 + 60 * MM_UNIT)
    yc =config.yc2 #= int(85 * MM_UNIT)
    
    add_sky_plnt(paper, xc, yc,r1,r5, r5b,rr,
                    year,month,day,hour,minute,tz)
  
    layer_obc = paper.add_layer(name='orbit_cir')
    hr1 = 685-85
    hr2 = 625-85
    print('hr1:', hr1/MM_UNIT)
    hxc_a =int(40 * MM_UNIT) # hr1+MIN_X + OFS_X
    #hxc_b = MAX_X - hr1 #2300
    hxc_b = int(100 * MM_UNIT) #hr1 * 2 + 1200 + OFS_X
    #hyc=MAX_Y-620
    hyc = int(175 * MM_UNIT) #r1 *2 + OFS_Y+ hr1 + 300
    print('hxc_a: %s mm' % (hxc_a / MM_UNIT))
    print('hxc_b: %s mm' % (hxc_b / MM_UNIT))
    print('hyc: %s mm' % (hyc / MM_UNIT))
    
    draw_orbit_cir(layer_obc.im,layer_obc.draw,hxc_a,hyc,hr1,hr2)
    draw_orbit_cir(layer_obc.im,layer_obc.draw,hxc_b,hyc,hr1,hr2)
        
    
    s_au_l=15   # 1AU = ? pixel
    s_au_r =280   # 1AU = ? pixel
    
    #cal_planet_info(year,month,day,hour,minute,tz)
    #dump_pln_0()
    layer_plnt = paper.add_layer(name='orbit_plnt')
    l_yh,l_yl,r_yh,r_yl,r_x=draw_orbit(layer_plnt.im, layer_plnt.draw,
                    hxc_a, hxc_b, hyc, hr1, hr2,
                    s_au_l, s_au_r,
                   year,month,day,hour,minute,tz)
    
    # lines connect the two orbits
    layer_plnt.draw.line([(hxc_a,l_yh),(r_x,r_yh)],fill=RED)
    layer_plnt.draw.line([(hxc_a,l_yl),(r_x,r_yl)],fill=RED)
    
    draw_orbit_plnt(layer_plnt.im, layer_plnt.draw,hxc_a, hxc_b, hyc, hr1, hr2,
                    s_au_l, s_au_r,
                   year,month,day,hour,minute,tz)
    
    #paper.draw_top_punch_hole()
    x=OFS_X
    y=OFS_Y + 100 
    layer_cald = paper.add_layer(name='calendar')
    txt_year=day_cald(layer_cald.draw,x,y,year,month,day)
    draw_txt_year(layer_cald.draw,x,y-100,txt_year)

    x = int(106 * MM_UNIT)
    y = int(24 * MM_UNIT)
    text ='面向北方'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))
    y+= int(4*MM_UNIT)
    text ='(中心北天极)'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))
    
    #x = int(220 * MM_UNIT)
    #y = int(18 * MM_UNIT)
    x = int(236 * MM_UNIT)
    y = int(24 * MM_UNIT)
    text ='面向南方'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))
    y+= int(4*MM_UNIT)
    text ='(中心南天极)'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))

    font = unicode_font_42
    x0 = hxc_a + int(15 * MM_UNIT)
    y0 = hyc+int(15 * MM_UNIT)
    
    s_au = s_au_l
    n_au = 15
    
    text_au(layer_cald.im,layer_cald.draw,x0+40,y0+200,s_au,n_au,font)
    
    #x0 = OFS_A
    text='太陽系行星軌道'
    layer_cald.draw.text((x0,y0-1000),text=text, font=unicode_font_96, fill=(0,0,0,255))
    text="箭頭所指為兩年行程"
    layer_cald.draw.text((x0,hyc+hr1),text=text, font=font, fill=(0,0,0,255))
    
    x0 = hxc_b + int(15 * MM_UNIT)
    y0 = hyc+int(15 * MM_UNIT)
    s_au = s_au_r
    n_au = 1
    text_au(layer_cald.im,layer_cald.draw,x0+40,y0+200,s_au,n_au,font)
    
    #x0 = OFS_B #int(60 * MM_UNIT)
    #text='内側行星軌道'
    #layer_cald.draw.text((x0,y0-1000),text=text, font=font, fill=(0,0,0,255))
    text="箭頭所指為十天行程"
    layer_cald.draw.text((x0,hyc+hr1),text=text, font=font, fill=(0,0,0,255))
    
    #add_RA_circle(paper,xc,yc,r5,r5a)
    x0=int(91 *MM_UNIT)
    x1=int(x0+ 118 * MM_UNIT)
    y0=0
    y1=int(16 * MM_UNIT)
    paper.draw_line(x0,0,x0,y1,color=RED)
    paper.draw_line(x0,y1,x1,y1,color=RED)
    paper.draw_line(x1,0,x1,y1,color=RED)
    #paper.draw_mid_vline()
    #paper.draw_hline(int(16*MM_UNIT))
    return paper


if __name__=='__main__':
    import platform
    import pytz
    import datetime
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.now(datetime.UTC)
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    month = now.month
    day = now.day
    
    config.debug=False

    #fnx='dxt_rl_%s_%02d_%02d_A4.pdf' % (year,month,day)
    fnx='dxt_rl_A4.pdf' #% (year,month,day)
    
    if platform.system()=='Linux':
        fn = '/home/kcfkwok/dxtc2/%s' % fnx
    else:
        fn = 'd:/kcf/dxtc2/%s' % fnx
    paper= make_dxt_rl_A4(year,month,day)
    
    hour=0
    minute=0
    
    x=int(150*MM_UNIT)
    y=int(167*MM_UNIT)
    table_plnt_info(paper,x,y,year,month,day,hour,minute,timezone)
    
    sun_lon = g_share.sun_lon
    x=int(130 *MM_UNIT)
    y=int(145* MM_UNIT)
    table_jieqi_to_zod_and_zhemonth(paper, x,y,sun_lon=sun_lon)
    
    
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    paper.commit_image(fn)
