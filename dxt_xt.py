from config import config
from paper import *
from ut_cal import *
#from sky_plnt import add_sky_plnt
#from orbit_cir import draw_orbit_cir
#from orbit_plnt import *
from ut_calendar import CALENDAR
from zhconv import convert
from cstcn import cstcn
from starsb import starsb
from def_font import *
from ut_star import *
#from starsb21z import starsb21z
from stars_top import top_star
import qrcode
from word_list import *
import os
from table_jieqi_to_zod_and_zhemonth import table_jieqi_to_zod_and_zhemonth
from pathlib import Path

def get_bstar(cst):
    hr, cstbayer, ra, dec, mag = starsb[cst]
    bayer =cstbayer.split('/')[0]
    rah = ra/15
    rahh = int(rah)
    rahm = int((rah-rahh) * 60)
    dec1 = math.ceil(dec)
    txt ='%s(%dh%02dm,%d°)' % (bayer,rahh,rahm, dec1)
    return bayer, rah,dec,mag,txt,hr
    
    
def list_top_star(im, draw, x,y, title,startn=0, endn=32):
    def _draw_text(xy, text="", font=unicode_font_64,fill=(0,0,0),draw=draw):
        ss=convert(text, 'zh-hans')
        draw.text(xy, text=ss, font=font, fill=fill)
    
    def draw_text(image, text, font, x,y,angle):
        left,top,right,bottom=font.getbbox(text)
        width = right - left +10
        height = bottom - top +10
        image2 = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw2 = ImageDraw.Draw(image2)
        #draw2.text((0, 0), text=text, font=font, fill=(0, 0, 0))
        _draw_text((0,0), text=text, font=font, fill=(0,0,0), draw=draw2)
        image2 = image2.rotate(angle, expand=1)
        sx, sy = image2.size
        px = x - int(sx/2)
        py = y - int(sy/2)
        image.paste(image2, (px, py, px + sx, py + sy), image2)
        
    t_ofs=150
    t2_ofs=300
    x_ofs=int(32* MM_UNIT) #630
    y_ofs=100
    y0=y
    cnt=0
    _draw_text((x,y-int(5*MM_UNIT)), text=title , font=unicode_font_64,fill=(0,0,0),draw=draw)
    top_stars=list(top_star.keys())
    for star_hr in top_stars[startn:endn]:
        #print(star_hr)
        ra,dec,mag,sp,=starsi[star_hr]
        ccst,cname,cst,bayer = top_star[star_hr]
        rah = ra/15
        rahh = int(rah)
        rahm = int((rah-rahh) * 60)
        dec1 = math.ceil(dec)
        txt = '%s/%s %s(%dh%02dm,%s°)' % (ccst,cname,bayer,rahh,rahm,dec1)
        #print(txt)
        _draw_text((x,y), text=txt , font=unicode_font_48,fill=(0,0,0),draw=draw)
        x_star = x- int(2* MM_UNIT)
        y_star = y + int(1* MM_UNIT)
        draw_star_at(draw, star_hr,x_star,y_star)
        y+=100
        cnt+=1
        
            
def list_cst_bstar(im, draw, x,y,title, startn=0, endn=100):
    # list brighest star in cst
    def _draw_text(xy, text="", font=unicode_font_64,fill=(0,0,0),draw=draw):
        ss=convert(text, 'zh-hans')
        draw.text(xy, text=ss, font=font, fill=fill)
    
    def draw_text(image, text, font, x,y,angle):
        left,top,right,bottom=font.getbbox(text)
        width = right - left +10
        height = bottom - top +10
        image2 = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw2 = ImageDraw.Draw(image2)
        #draw2.text((0, 0), text=text, font=font, fill=(0, 0, 0))
        _draw_text((0,0), text=text, font=font, fill=(0,0,0), draw=draw2)
        image2 = image2.rotate(angle, expand=1)
        sx, sy = image2.size
        px = x - int(sx/2)
        py = y - int(sy/2)
        image.paste(image2, (px, py, px + sx, py + sy), image2)
        
    #draw.line([(0,yc+r1+30),(3125,yc+r1+30)],fill=(0,0,0,0)) # below are for bright stars info
    t_ofs=150
    t2_ofs=300
    x_ofs=int(32* MM_UNIT) #630
    y_ofs=100
    y0=y
    #y=y0=yc+r1+250
    #x=MIN_X+30

    _draw_text((x,y-150), text=title , font=unicode_font_64,fill=(0,0,0),draw=draw)

    csts = list(cstcn.keys())
    csts.sort()
    cnt=0
    for cst in csts[startn: endn]:
        x_star = x- int(2* MM_UNIT)
        y_star = y + int(1* MM_UNIT)
        _draw_text((x,y), text=cst , font=unicode_font_64,fill=(0,0,0),draw=draw)
        _draw_text((x+t_ofs,y), text=cstcn[cst] , font=unicode_font_48,fill=(0,0,0),draw=draw)
        bayer, rah,dec,mag,txt,star_hr = get_bstar(cst)
        draw_star_at(draw, star_hr,x_star,y_star)
        _draw_text((x+t2_ofs,y), text=txt , font=unicode_font_48,fill=(0,0,0),draw=draw)
    
        y+=100
        cnt+=1
        if cnt==10:
            cnt=0
            y=y0
            x=x+x_ofs
            
            
def draw_title(draw, x,y, txt):
    yrfont = unicode_font_80
    FCOLOR=(0,0,0,255)
    draw.text((x,y),txt,font=yrfont,fill=FCOLOR)
    
def day_cald(draw,x,y,year,month=1,day=1,hour=0,minute=0,show_hm=False):
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
    title = cyear + '全天星圖'
    txt_year = lyear
        #print(txt)
        #draw.text((x,y),txt,font=yrfont,fill=FCOLOR)
        #y+=50
        
    txt = '起始日: ' +cmonth+cday+' '+cwd
    draw.text((x,y),txt,font=font,fill=FCOLOR)
    y+=ystep
    draw.text((x,y),txt_year,font=font,fill=FCOLOR)
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

    return title

def add_qrcode(im, draw, x,y, title, url):
    #url='https://kcfkwok.pythonanywhere.com/?content=xt-0'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=(0,0,0), back_color=(255,255,255))
    
    sw,sh =img.size
    im.paste(img,(x,y,x+sw,y+sh))
    
    #text = '更新星圖'
    draw_title(draw,x+int(1*MM_UNIT),y-100,title)

def make_dxt_xt_A4(year,month=1,day=1,hour=0,minute=0):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    from IPython.display import display
    from config import config
    config.f_south=False
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
    
    layer_bg.draw.line([(xc-int(1*MM_UNIT),yc),(xc+int(1*MM_UNIT),yc)],fill=RED,width=2)
    layer_bg.draw.line([(xc,yc-int(1*MM_UNIT)),(xc,yc+int(1*MM_UNIT))],fill=RED,width=2)
    
    
    cal_planet_info(year,month,day,hour,minute,tz)
    
 
    config.f_south=True

    xc =config.xc2 #= int(70 * MM_UNIT *2 + 60 * MM_UNIT)
    yc =config.yc2 #= int(85 * MM_UNIT)

   
    layer_bg.draw.line([(xc-int(1*MM_UNIT),yc),(xc+int(1*MM_UNIT),yc)],fill=RED,width=2)
    layer_bg.draw.line([(xc,yc-int(1*MM_UNIT)),(xc,yc+int(1*MM_UNIT))],fill=RED,width=2)


    x=OFS_X
    y=OFS_Y + 100 
    layer_cald = paper.add_layer(name='calendar')
    title=day_cald(layer_cald.draw,x,y,year,month,day)
    #draw_title(layer_cald.draw,x,y-100,title)
     
    skip="""
    
    x = int(90 * MM_UNIT)
    y = int(18 * MM_UNIT)
    text ='面向北方(中心北天极)'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))
    
    x = int(220 * MM_UNIT)
    y = int(18 * MM_UNIT)
    text ='面向南方(中心南天极)'
    layer_cald.draw.text((x,y), text=text, font=unicode_font_80,fill=(0,0,0))
    """
    x = int(106 * MM_UNIT)
    y = int(18 * MM_UNIT)
    title = '%s年 全天星圖' % (year, )
    layer_cald.draw.text((x,y), text=title, font=unicode_font_112,fill=(0,0,0))
    #x = int(90 * MM_UNIT)
    #y = int(18 * MM_UNIT)
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

    x= int(8*MM_UNIT)
    y= int(158*MM_UNIT)
    title ="星座簡稱、中文名、代表亮星及赤道座標"  
    list_cst_bstar(layer_cald.im, layer_cald.draw, x,y,title)
    
    x = int(260 * MM_UNIT)
    y= int(23 * MM_UNIT)
    title = "最亮恒星表"
    list_top_star(layer_cald.im, layer_cald.draw, x,y,title)
    
    x= int(108 * MM_UNIT)
    y= int(125 * MM_UNIT)
    url='https://kcfkwok.pythonanywhere.com/'
    title = '即時星空'
    add_qrcode(layer_cald.im, layer_cald.draw, x,y, title, url)
    
    x+=int(20*MM_UNIT)
    url='https://kcfkwok.pythonanywhere.com/?content=rl-0-0-0'
    title = '今日行星'
    add_qrcode(layer_cald.im, layer_cald.draw, x,y, title, url)
    
    x+=int(20*MM_UNIT)
    url='https://kcfkwok.pythonanywhere.com/?content=xt-0'
    title = '更新星圖'
    add_qrcode(layer_cald.im, layer_cald.draw, x,y, title, url)

    x+=int(90*MM_UNIT)
    url='https://kcfkwok.pythonanywhere.com/set_location'
    title = '製作轉盤'
    add_qrcode(layer_cald.im, layer_cald.draw, x,y, title, url)
    
    x= int(96*MM_UNIT)
    y= int(141*MM_UNIT)
    table_jieqi_to_zod_and_zhemonth(paper, x,y)
    
    
    return paper


if __name__=='__main__':
    import platform
    import pytz
    import datetime
    from PIL import Image
    
    timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.utcnow()
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    year = now.year
    
    config.debug=False

    fnx='dxt_xt_A4.png'
    if platform.system()=='Linux':
        fn = '/home/kcfkwok/dxtc2/%s' % fnx
    else:
        fn = 'd:/kcf/dxtc2/%s' % fnx
    paper= make_dxt_xt_A4(year)
    x = config.banner_x
    y = config.banner_y
    layer = paper.add_layer(name='banner')
    banner_path=config.fpng_banner
    banner = Image.open(banner_path)
    layer.im.paste(banner, (x,y))
    #paper.draw.text((paper.min_x,paper.min_y), fnx, font=unicode_font_36,fill=RED)
    paper.commit_image(fn)
    
