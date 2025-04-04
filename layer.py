from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps

from def_color import *
from dprint import dprint

class LAYER:
    def __init__(self,w_px,h_px,ofs_px,ofs_py,name='none',bgcolor=WHITE):
        dprint('LAYER ',w_px,h_px, ofs_px, ofs_py)
        self.name=name
        self.w_px=w_px
        self.h_px=h_px
        self.ofs_px = ofs_px
        self.ofs_py = ofs_py
        bgc=(bgcolor[0],bgcolor[1],bgcolor[2],0)
        self.im = Image.new(mode='RGBA',size=(w_px, h_px),color=bgc)
        self.draw = ImageDraw.Draw(self.im)
        
    def draw_outline(self, color=BLACK):
        OFS_X=1
        WIDTH = self.w_px
        HEIGHT = self.h_px
        self.draw.line([(0+OFS_X,0),(0+OFS_X,HEIGHT)],fill=color,width=2)
        self.draw.line([(0+OFS_X,HEIGHT-1),(WIDTH+OFS_X,HEIGHT-1)],fill=color,width=2)
        self.draw.line([(0+OFS_X,0),(WIDTH+OFS_X,0)],fill=color,width=2)
        self.draw.line([(WIDTH+OFS_X,0),(WIDTH+OFS_X,HEIGHT-1)],fill=color,width=2)
    
if __name__=='__main__':
    layer = LAYER(2925, 4245, 75, 75)
    print(layer)
