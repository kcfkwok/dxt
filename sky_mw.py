from config import config
from g_share import g_share
from paper import *
from ut_misc import js_r
from ut_cal import *

def draw_milkyway_north(draw,xc,yc,rr):
    data = js_r(config.mw_path)
    color_sky = g_share.color_sky
    i=0
    dtss={}
    for s in data['features']:
        i+=1
        dtss[i]=[]
        #print(i)
        #print(s.keys())
        keys = s.keys()
        for key in keys:
            if key !='geometry':
                pass
                #print(key, s[key])
            else:
                #print('geometry type:', s['geometry']['type'])
                coords =s['geometry']['coordinates']
                #print('coordinates type:', type(coords))
                for v1 in coords:
                    for v2 in v1:
                        dts=[]
                        for v3 in v2:
                            #print('\t[%s..]..%d' % (v3[:5], len(v3)))
                            ra,dec = v3[0], v3[1]
                            x,y = ra_dec_to_xyplot(ra, dec,xc,yc,rr)
                            dts.append((x,y))
                        dtss[i].append(dts)
                        #draw.polygon(dts, outline=(0,0,0,0),width=1)                  
                    #break
                #break
        #break                        

    # milky way color
    mwc={
    1: (240,240,240,255),
    2: (230,230,230,255),
    3: (220,220,220,255),
    4: (210,210,210,255),
    5: (200,200,200,255),
    }
    dtss1= dtss[1]
    #print('dtss1[1]:%s' % dtss1[1])
    draw.polygon(dtss1[1], fill=mwc[1])
    draw.polygon(dtss1[0], fill=color_sky) #(255,255,255,255))

    
    for dts in dtss1[2:]:
        draw.polygon(dts, fill=color_sky) #(255,255,255,255))
     
    dtss2 = dtss[2]
    for dts in dtss2:
        draw.polygon(dts, fill=mwc[2])

    dtss3 = dtss[3]
    for dts in dtss3:
        draw.polygon(dts, fill=mwc[3])

    dtss4 = dtss[4]
    for dts in dtss4:
        draw.polygon(dts, fill=mwc[4])

    dtss5 = dtss[5]
    for dts in dtss5:
        draw.polygon(dts, fill=mwc[5])


def draw_milkyway_south(draw,xc,yc,rr):
    data = js_r(config.mw_path)
    color_sky = g_share.color_sky
    i=0
    dtss={}
    for s in data['features']:
        i+=1
        dtss[i]=[]
        #print(i)
        #print(s.keys())
        keys = s.keys()
        for key in keys:
            if key !='geometry':
                pass
                #print(key, s[key])
            else:
                #print('geometry type:', s['geometry']['type'])
                coords =s['geometry']['coordinates']
                #print('coordinates type:', type(coords))
                for v1 in coords:
                    for v2 in v1:
                        dts=[]
                        for v3 in v2:
                            #print('\t[%s..]..%d' % (v3[:5], len(v3)))
                            ra,dec = v3[0], v3[1]
                            x,y = ra_dec_to_xyplot(ra, dec,xc,yc,rr)
                            dts.append((x,y))
                        dtss[i].append(dts)
                        #draw.polygon(dts, outline=(0,0,0,0),width=1)                  
                    #break
                #break
        #break                        

    # milky way color
    mwc={
    1: (240,240,240,255),
    2: (230,230,230,255),
    3: (220,220,220,255),
    4: (210,210,210,255),
    5: (200,200,200,255),
    }
    dtss1= dtss[1]
    #print('dtss1[1]:%s' % dtss1[1])
    draw.polygon(dtss1[0], fill=mwc[1])
    draw.polygon(dtss1[1], fill=color_sky) #(255,255,255,255))

    
    for dts in dtss1[2:]:
        draw.polygon(dts, fill=color_sky) #(255,255,255,255))
 
    dtss2 = dtss[2]
    for dts in dtss2:
        draw.polygon(dts, fill=mwc[2])

    dtss3 = dtss[3]
    for dts in dtss3:
        draw.polygon(dts, fill=mwc[3])

    dtss4 = dtss[4]
    for dts in dtss4:
        draw.polygon(dts, fill=mwc[4])

    dtss5 = dtss[5]
    for dts in dtss5:
        draw.polygon(dts, fill=mwc[5])


def add_milkyway(paper,xc,yc,rr,im=None, draw=None):
    if im is not None:
        if g_share.f_south:
            draw_milkyway_south(draw,xc,yc,rr)
        else:
            draw_milkyway_north(draw,xc,yc,rr)
        return
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    LW=2
    layer = paper.add_layer(name='milkyway')
    if g_share.f_south:
        draw_milkyway_south(layer.draw,xc,yc,rr)
    else:
        draw_milkyway_north(layer.draw,xc,yc,rr)
        
		
def app_mw(fn=None):
    from PIL import Image, ImageColor,ImageDraw,ImageFont,ImageOps
    from IPython.display import display
    from config import config
    paper = PAPER("B6")
    #paper.draw_outline()
    #paper.draw_MAX_RECT()
    OFS_X=300
    OFS_Y=200
    LW=2
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    r1 = round(2.333 * DPI) #1400 #1350 
    #xc = int((MAX_X- MIN_X) /2) + MIN_X
    xc = OFS_X + r1
    yc = xc + OFS_Y #int((MIN_Y+ MAX_Y)/2)
    r0 = xc - MIN_X
    r2 = r1 - 60
    r3 = r2 - 60
    r4 = r3 - 60
    r5 = r4 -60
    r1a = r1 -30
    r2a = r2 - 30
    r4a = r4 - 30
    r5a = r5 -30 # for ra marker
    
    r_90=r5
    rr = 180/r_90
    requ = int(r_90/2)

    month=1
    day=1
    hour=0
    minute=0
    tz=8
    print('r1:%s mm' % (r1/MM_UNIT))
    w = h= int(120 * MM_UNIT)
    xc = yc = int(60 * MM_UNIT)
    layer_n = paper.add_layer(w,h,0,0,'sky_bg_n')
    im = layer_n.im
    draw = layer_n.draw
    draw.circle((xc,yc),r5, fill=g_share.color_sky)
    add_milkyway(None,xc,yc,rr,im=im,draw=draw)
    layer_bg = paper.add_layer(name='bg')
    #draw1 = layer_bg.draw
    return im
	
if __name__=='__main__':
    year = 2025
    config.debug=False
    g_share.set_f_south(False)
    cx=config.color_sky_day
    g_share.color_sky=(cx[0],cx[1],cx[2],255)
    
    im =app_mw()
    fn = '%s/%s' % (config.fskyl, config.fmw_n)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
	
if __name__=='__main__':
    year = 2025
    config.debug=False
    g_share.set_f_south(True)
    cx=config.color_sky_day
    g_share.color_sky=(cx[0],cx[1],cx[2],255)
    
    im =app_mw()
    fn = '%s/%s' % (config.fskyl, config.fmw_s)
    im.save(fn, dpi=(600,600))
    print('saved to %s' % fn)
