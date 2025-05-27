import re
r_day =r'(\d+)\]'
re_day = re.compile(r_day)
from config import config
from pathlib import Path
from def_font import *

class EVENTS:
    def __init__(self,year,month):
        self.year = year
        self.month=month
        self.events={}
        self.load_events()
        
    def load_events(self):
        #ev_fn='ev%d%02d.txt' % (self.year, self.month)
        fn = config.fevs_path % (self.year, self.month)
        ev_fn =Path(config.staticpath, fn)
        try:
            f=open(ev_fn,'r', encoding='UTF8')
            print('event file:%s' % ev_fn)
            lines = f.readlines()

            dd=0
            for line in lines:
                m = re_day.match(line)
                if m is not None:
                    dd, = m.groups()
                    dd = int(dd)
                    self.events[dd]=[]
                else:
                    self.events[dd].append(line)
        except Exception as e:
            print(f'load events fail: {e}' )
            
        #print(self.events)

    def get_evs(self,day):
        return self.events.get(day,[])
        
        
def show_events(draw, evs,x=config.xc1+50,y=100):
    #YEAR = CONFIG.YEAR
    #evs = get_evs(DAY)
    WIDTH = int(15*config.MM_UNIT)
    #y=100
    #x = config.xc1 + 50
    #wc_xs =[(17,200),(15,360),(13,600),(11,760),(9,890)]
    EV_XOFS=[200,360,600,760,900,1000,1100,1150,1230]
    EV_LEN =[15,12,10,9,7,5,4,3,2]
    R_MARGIN = WIDTH-200
    
    def text_over_margin(text,font,xofs):
        #print('text_over_margin text:',text)
        length = font.getlength(text)
        if length+xofs > R_MARGIN:
            return True
        return False

    #draw.text((x,y), text='天象:', font=unicode_font_80,fill=(0,0,0))
    
    if len(evs) >0:
        evs = evs[0]
        fontx = unicode_font_80
        ofs_x = EV_XOFS[0]
        if not text_over_margin(evs, fontx, x+ofs_x ):
            #print("not text_over_margin")
            draw.text((x+ ofs_x,y), text=evs, font=fontx,fill=(0,0,0))
        else:
            #print("text_over_margin",evs)
            ln=0
            length = EV_LEN[ln]
            ofs_x = EV_XOFS[ln]
            txt = evs[:length]
            evs = evs[length:]
            draw.text((x+ ofs_x,y), text=txt, font=fontx,fill=(0,0,0))
            
            #print('len(evs)',len(evs),evs)
            while len(evs) >0:
                if text_over_margin(txt+evs[0], fontx,x+ ofs_x ):
                    draw.text((x+ ofs_x,y), text=txt, font=fontx,fill=(0,0,0))
                    y+=100
                    ln+=1
                    #print('ln:%d EV_LEN-len:%d' % (ln, len(EV_LEN)))
                    if ln >= len(EV_LEN):
                        break
                    length = EV_LEN[ln]
                    ofs_x = EV_XOFS[ln]
                    txt = evs[:length]
                    evs = evs[length:]
                    #print('1 ln:%s txt:%s evs:"%s"' % (ln,txt,evs))
                    if len(evs)==0:
                        draw.text((x+ ofs_x,y), text=txt, font=fontx,fill=(0,0,0))
                        print('2 ln:%s txt:%s evs:"%s"' % (ln,txt,evs))
                        break                        
                else:
                    txt+= evs[0]
                    evs = evs[1:]
                    if len(evs)==0:
                        draw.text((x+ ofs_x,y), text=txt, font=fontx,fill=(0,0,0))
                        #print('3 ln:%s txt:%s evs:"%s"' % (ln,txt,evs))
                        break
                    #print('?txt:',txt)
            
                    