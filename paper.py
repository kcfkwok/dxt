from layer import *
from dprint import dprint
from def_color import *
import copy

DPI=600
MARGIN= DPI/8
INCHX_10TH = DPI / 10
MM_UNIT = DPI/25.4

PAPER_SIZE={  # width, height in inches 
    'A4': (8.2, 11.6), # 8.2 inch * 11.6 inch 
    'A4L':(11.6, 8.2),
    'A5': (5.8, 8.2), # 5.8 inch * 8.2 inch
    'A5R': (5.8, 5.8), # 5.8 inch * 8.2 inch    
    'B6': (5, 7.2),    
}


class PAPER_TYPE:
    def __init__(self, paper_type):
        dprint('paper_type:', paper_type)
        self.paper_type = paper_type
        w_inch, h_inch = PAPER_SIZE.get(paper_type, (5,7.2))
        self.w_inch=w_inch
        self.h_inch=h_inch
        self.w_px = int(self.w_inch * DPI)
        self.h_px = int(self.h_inch * DPI)
        self.min_x = int(MARGIN)
        self.max_x = int(self.w_px - MARGIN)
        self.min_y = int(MARGIN)
        self.max_y = int(self.h_px - MARGIN)
        
    def draw_outline(self, draw, color=BLACK):
        OFS_X=1
        WIDTH = self.w_px
        HEIGHT = self.h_px
        draw.line([(0+OFS_X,0),(0+OFS_X,HEIGHT)],fill=color,width=2)
        draw.line([(0+OFS_X,HEIGHT-1),(WIDTH+OFS_X,HEIGHT-1)],fill=color,width=2)
        draw.line([(0+OFS_X,0),(WIDTH+OFS_X,0)],fill=color,width=2)
        draw.line([(WIDTH+OFS_X,0),(WIDTH+OFS_X,HEIGHT-1)],fill=color,width=2)
        
    def draw_MAX_RECT(self,draw, color=BLACK):
        OFS_X=0
        MIN_X = self.min_x
        MAX_X = self.max_x
        MIN_Y = self.min_y
        MAX_Y = self.max_y
        draw.line([(MIN_X+OFS_X,MIN_Y),(MIN_X+OFS_X,MAX_Y)],fill=color,width=2)
        draw.line([(MIN_X+OFS_X,MAX_Y),(MAX_X+OFS_X,MAX_Y)],fill=color,width=2)
        draw.line([(MIN_X+OFS_X,MIN_Y),(MAX_X+OFS_X,MIN_Y)],fill=color,width=2)
        draw.line([(MAX_X+OFS_X,MIN_Y),(MAX_X+OFS_X,MAX_Y)],fill=color,width=2)

class PAPER(PAPER_TYPE):
    def __init__(self, paper_type, bgcolor=WHITE):
        super(PAPER,self).__init__(paper_type)
        #self.im = Image.new(mode='RGBA',size=(self.w_px, self.h_px),color=bgcolor)
        bgc  = (bgcolor[0],bgcolor[1],bgcolor[2]) 
        self.im = Image.new(mode='RGB',size=(self.w_px, self.h_px),color=bgc)
        
        self.draw = ImageDraw.Draw(self.im)
        layer0 = LAYER(self.w_px,self.h_px,0,0)
        self.layers=[layer0]
        
    def draw_top_punch_hole(self):
        WIDTH = self.w_px
        hole_x = int(WIDTH /2)
        hole_y = int(7.5 * MM_UNIT)
        hole_r = int(3 * MM_UNIT)
        x0 = hole_x - int(4 * MM_UNIT)
        x1 = hole_x + int(4 * MM_UNIT)
        y0 = hole_y - int(1.5 * MM_UNIT)
        y1 = hole_y + int(1.5 * MM_UNIT)
        self.layers[0].draw.rectangle([(x0,y0),(x1,y1)],fill=(255,0,0,255))
    
    def draw_outline(self):
        self.layers[0].draw_outline()
        
    def draw_MAX_RECT(self):
        super(PAPER,self).draw_MAX_RECT(self.layers[0].draw)
        
    def draw_hline(self,y, color=(0,0,0,255)):
        WIDTH = self.w_px
        self.layers[0].draw.line([(0,y),(WIDTH,y)],fill=color)
    
    def draw_vline(self,x, color=(0,0,0,255)):
        HEIGHT = self.h_px
        self.layers[0].draw.line([(x,0),(x,HEIGHT)],fill=color)
    
    def draw_line(self,x0,y0,x1,y1,color=(0,0,0,255)):
        self.layers[0].draw.line([(x0,y0),(x1,y1)],fill=color)
        
    def draw_mid_vline(self, color=(0,0,0,255)):
        WIDTH = self.w_px
        x = int(WIDTH /2)
        self.layers[0].draw.line([(x,0),(x,self.h_px)],fill=color)

    def add_layer(self,w_px=None, h_px=None, ofs_px=0, ofs_py=0, name='none'):
        if w_px is None:
            w_px = self.w_px
        if h_px is None:
            h_px = self.h_px
        dprint('add_layer:%s %s %s %s' % (w_px,h_px,ofs_px,ofs_py))
        layerx = LAYER(w_px,h_px,ofs_px, ofs_py,name=name)
        self.layers.append(layerx)
        return layerx
    
    def get_last_layer(self):
        return self.layers[-1]
    
    def commit_image(self, fn=None, excludes=[]):
        im = copy.copy(self.im)
        for layer in self.layers:
            if layer in excludes:
                print('excluded:',layer.name)
                continue
            #self.im.paste(layer.im, (layer.ofs_px, layer.ofs_py),layer.im)
            im.paste(layer.im, (layer.ofs_px, layer.ofs_py),layer.im)
            
        if fn is not None:
            #self.im.save(fn, dpi=(600,600))
            im.save(fn, dpi=(600,600))
            print('saved to %s' % fn)
        return im

if __name__=='__main__':
    paper = PAPER("B6")
    print(paper)
    print(paper.paper_type)
    print('w_px:',paper.w_px)
    print('h_px:',paper.h_px)
    print('min_x:',paper.min_x)
    print('max_x:',paper.max_x)
    print('min_y:',paper.min_y)
    print('max_y:',paper.max_y)
