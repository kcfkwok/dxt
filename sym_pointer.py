from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
from paper import *    
from ut_cal import *
from def_font import *

def _draw_text(draw, xy, text="", font=unicode_font_64,fill=(0,0,0)):
    #ss=convert(text, 'zh-hans')
    draw.text(xy, text=text, font=font, fill=fill)
    
def draw_pointer(image, x0,y0,rr,L0,L1,W0,W1,iangle,color1,color2, f_south=False,name=''):
    #print('plnt:%s co:%s x:%d y:%d draw_arrow ang:%.2f' % (plnt,color,x,y, iangle))
    LW=2
    D = L1 *2 +2
    left = 0
    width = D
    right = 0
    height = D
    angle = 360 - iangle
    im2 = Image.new(mode='RGBA',size=(width, height),color=(255,255,255,0))
    draw2 = ImageDraw.Draw(im2)
    #xl = W/2
    pt1 = (L1-W0,L1-L0)
    pt2 = (L1+W1,L1-L0)
    pt3 = (L1+W1,L1 *2)
    pt4 = (L1-W0,L1 *2)
    x2= int(1 * MM_UNIT)
    draw2.polygon([pt1,pt2,pt3,pt4,pt1], outline=(0,0,0,255))
    draw2.line([(L1,L1-L0),(L1,L1*2)],fill=color1,width=5)
    draw2.line([(L1-x2,L1),(L1+x2,L1)],fill=color1,width=5)
    
    mm_px = int(1* MM_UNIT)
    x1_5mm_px = int(1.5 * MM_UNIT)
    # *** for cut out 
    #draw2.circle((L1,L1),mm_px, outline=BLACK, width=3)
    draw2.line([(L1-mm_px,L1-L0),(L1-mm_px,L1+ x1_5mm_px)],fill=BLACK,width=3)
    draw2.line([(L1+mm_px,L1-L0),(L1+mm_px,L1+ x1_5mm_px)],fill=BLACK,width=3)
    draw2.line([(L1-mm_px,L1+x1_5mm_px),(L1+mm_px,L1+ x1_5mm_px)],fill=BLACK,width=3)


    # test line
    #draw2.line([(0,0),(D,D)],fill=(0,0,0,255),width=2)
    xc =  L1
    yc =  L1
    ra=0
    # for storing zodiac zone 
    xz0=None
    yz0=None
    xz1=None
    yz1=None
    if f_south ==False:
        x,y=ra_dec_to_xyplot(ra, 100,xc,yc,rr)
        _draw_text(draw2,(x+50, y-40), text='北', font=unicode_font_64,
                       fill=(0,0,0,255) )
        for dec in range(91):
            x,y=ra_dec_to_xyplot(ra, dec,xc,yc,rr)
            if dec ==23:
                xz0=x
                yz0=y
            #x,y =ra_dec_to_xyplot(ra, dec)
            if (dec % 10)==0:
                draw2.line([(x,y),(x+30,y)],fill=(0,0,0,255),width=LW)
                _draw_text(draw2,(x+50, y-40), text='%d' % dec, font=unicode_font_64,
                       fill=(0,0,0,255) )
            elif (dec % 2) ==0:
                draw2.line([(x,y),(x+15,y)],fill=(0,0,0,255),width=2)
            
        for dec in range(-90,-1):
            x,y=ra_dec_to_xyplot(ra, dec,xc,yc,rr)
            if dec ==-23:
                xz1=x
                yz1=y
            #x,y =ra_dec_to_xyplot(ra, dec)
            if (dec % 10)==0:
                draw2.line([(x,y),(x+30,y)],fill=(0,0,0,255),width=LW)
                _draw_text(draw2,(x+50, y-40), text='%d' % dec, 
                       font=unicode_font_64, fill=(0,0,0,255))
            elif (dec % 2) ==0:
                draw2.line([(x,y),(x+15,y)],fill=(0,0,0,255),width=2)
            
    else:
        x,y=ra_dec_to_xyplot(ra, -100,xc,yc,rr,f_south=True)
        _draw_text(draw2,(x+50, y-40), text='南', font=unicode_font_64,
                       fill=(0,0,0,255) )
        for dec in range(91):
            x,y=ra_dec_to_xyplot(ra, dec,xc,yc,rr,f_south=True)
            if dec ==23:
                xz0=x
                yz0=y
            #x,y =ra_dec_to_xyplot(ra, dec)
            if (dec % 10)==0:
                draw2.line([(x,y),(x+30,y)],fill=(0,0,0,255),width=LW)
                _draw_text(draw2,(x+50, y-40), text='%d' % dec, font=unicode_font_64,
                       fill=(0,0,0,255) )
            elif (dec % 2) ==0:
                draw2.line([(x,y),(x+15,y)],fill=(0,0,0,255),width=2)
            
        
        for dec in range(-90,-1):
            x,y=ra_dec_to_xyplot(ra, dec,xc,yc,rr,f_south=True)
            if dec ==-23:
                xz1=x
                yz1=y
            #x,y =ra_dec_to_xyplot(ra, dec)
            if (dec % 10)==0:
                draw2.line([(x,y),(x+30,y)],fill=(0,0,0,255),width=LW)
                _draw_text(draw2,(x+50, y-40), text='%d' % dec, 
                       font=unicode_font_64, fill=(0,0,0,255))
            elif (dec % 2) ==0:
                draw2.line([(x,y),(x+15,y)],fill=(0,0,0,255),width=2)
            
    yzz = abs(yz1-yz0)
    if f_south:
        draw2.rectangle([(xz0-W0,yz0-yzz),(xz0,yz0)],fill=color2)    
    else:
        draw2.rectangle([(xz0-W0,yz0),(xz0,yz0+yzz)],fill=color2)
    draw2.line([(xz0,yz0),(xz1,yz1)],fill=color1,width=5)        
    #draw2.line([(xz0,yz0),(xz1,yz1)],fill=color2,width=5)
    #draw2.line([(0,D),(D,0)],fill=(0,0,0,255),width=2)
    
    im2 = im2.rotate(angle, expand=1)
    sx, sy = im2.size
    #print(sx,sy)
    px = x0 - int(sx/2)
    py = y0 - int(sy/2)
    #print(px,py,sx,sy)
    image.paste(im2, (px, py, px + sx, py + sy), im2)
