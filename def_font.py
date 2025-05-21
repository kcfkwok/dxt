from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
from config import config

FONT_PATH =config.fontpath
print('FONT_PATH:%s' % FONT_PATH)

unicode_font = ImageFont.truetype(FONT_PATH, 48,encoding="unic")
unicode_font_24 = ImageFont.truetype(FONT_PATH, 24,encoding="unic")
unicode_font_36 = ImageFont.truetype(FONT_PATH, 36,encoding="unic")
unicode_font_42 = ImageFont.truetype(FONT_PATH, 42,encoding="unic")
unicode_font_44 = ImageFont.truetype(FONT_PATH, 44,encoding="unic")
unicode_font_48 = ImageFont.truetype(FONT_PATH, 48,encoding="unic")
unicode_font_56 = ImageFont.truetype(FONT_PATH, 56,encoding="unic")
unicode_font_64 = ImageFont.truetype(FONT_PATH, 64,encoding="unic")
unicode_font_80 = ImageFont.truetype(FONT_PATH, 80,encoding="unic")
unicode_font_96 = ImageFont.truetype(FONT_PATH, 96,encoding="unic")
unicode_font_112 = ImageFont.truetype(FONT_PATH, 112,encoding="unic")

def draw_text(image, text, font, x,y,angle,stroke_width=0):
    left,top,right,bottom=font.getbbox(text)
    width = right - left +10
    height = bottom - top +10
    image2 = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw2 = ImageDraw.Draw(image2)
    draw2.text((0, 0), text=text, font=font, fill=(0, 0, 0),stroke_width=stroke_width)
    image2 = image2.rotate(angle, expand=1)
    sx, sy = image2.size
    px = x - int(sx/2)
    py = y - int(sy/2)
    image.paste(image2, (px, py, px + sx, py + sy), image2)
