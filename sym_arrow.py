from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
from paper import *

def draw_arrow(image, x,y,L,iangle,color, ar_width=None, name=''):
    #print('plnt:%s co:%s x:%d y:%d draw_arrow ang:%.2f' % (plnt,color,x,y, iangle))
    color1 = (color[0],color[1],color[2],255)
    D = L *2
    left = 0
    width = D
    right = 0
    height = D
    angle = 360 - iangle
    im2 = Image.new(mode='RGBA',size=(width, height),color=(255,255,255,0))
    draw2 = ImageDraw.Draw(im2)
    xl = L/2
    if ar_width is not None:
        xl = ar_width
    pt1 = (L-xl,D)
    pt2 = (L+xl,D)
    pt3 = (L,L)
    draw2.polygon([pt1,pt2,pt3], fill=color1, outline=(0,0,0,255))
    im2 = im2.rotate(angle, expand=1)
    sx, sy = im2.size
    #print(sx,sy)
    px = x - int(sx/2)
    py = y - int(sy/2)
    #print(px,py,sx,sy)
    image.paste(im2, (px, py, px + sx, py + sy), im2)
