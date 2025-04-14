from paper import *
from ut_math import *
from ut_cal import *
from def_font import *
from def_color import *
from config import config
from g_share import g_share
ari_ang = config.ari_ang

def hor_to_radc(alt, azi,lat,lst):  # altitude, azimuth, latitude,local sidereal time
    #dprint('hor_to_radc alt:%s azi:%s lat:%s lst:%s' % (alt,azi,lat,lst))
    sin_A= sn(azi)
    dec = asn(sn(alt) * sn(lat) + cs(alt) * cs(lat) * cs(azi))
    cos_H =(sn(alt) - sn(lat)* sn(dec))/(cs(lat) * cs(dec))
    #print('cos_H:',cos_H)
    try:
        H = acs(cos_H)
    except:
        H = acs(int(cos_H))
        
    if sin_A >=0:
        H=360-H
    H = H / 15.0  # convert to hour
    ra = lst - H
    if ra <0:
        ra+=24
    ra = ra * 15  # back to deg
    return ra, dec

class SEGMENTS:
    def __init__(self,latv,ena=True):
        self.azi=None
        self.ena=ena
        self.latv=latv
        self.f_south=g_share.f_south
        self.data={}
        self.ras=[]
        
    def new_segment(self,azi,xh=None,yh=None,x=None,y=None):
        if not self.ena:
            return
        if self.azi is not None:
            self.commit_segment(xh,yh)
        self.azi=azi
        self.data[self.azi]=[]
        if xh is None:
            return
        if (self.f_south==False and self.latv>0) or (self.f_south and self.latv<0):
            self.data[self.azi].append((xh,yh))
        self.data[self.azi].append((x,y))
        
    def add(self,x,y,xra,yra): # xra,yra is the corresponding point on cir_RA
        if not self.ena:
            return
        if self.azi is None:
            return
        if self.latv==0:
            self.data[self.azi].append((xra,yra))
            return
        self.data[self.azi].append((x,y))
        if (self.f_south==False and self.latv>0) or (self.f_south and self.latv<0):
            self.ras.append((xra,yra))
        
    def commit_segment(self,xh=None,yh=None):
        if not self.ena:
            return
        # draw circle arc 
        if self.azi is None:
            return
        if self.latv==0:
            return
        self.data[self.azi].append((xh,yh))
        lenx = len(self.ras)
        for i in range(lenx-1, 0,-1):
            self.data[self.azi].append(self.ras[i])
        self.ras=[]
        
    def draw_polygon(self,draw,azi):
        if not self.ena:
            return
        polygon_points = self.data.get(azi,None)
        if polygon_points is not None:
            outline=None
            draw.polygon(polygon_points, fill=(255, 255, 0, g_share.hor_cir_opacity),outline=outline, width=2)
        

def draw_hor_mask(im, draw, xc,yc,rr, latv,lst, longv, place):
    from g_share import g_share

    #im = Image.new(mode='RGBA',size=im1.size,color=(255,255,255,0))
    #draw = ImageDraw.Draw(im)
    
    # avoid extreme cases
    if latv >89:
        latv=89
    if latv < -89:
        latv=-89
    if latv <5 and latv >0:
        latv=5
    if latv <0 and latv >-5:
        latv=-5
    
    def chk_dist_under(x0,y0,x,y,expected):
        if  math.sqrt((x-x0)**2 + (y-y0)**2) < expected:
            return True
        return False
    r_90 = 180/rr
    #rr = 180/r_90  # 1 degree / pixel in radian direction
    requ = int(r_90/2)  # the equatorial circle
    LW=4
    alt=0
    azi=0
    s=1
    FCOLOR=(0,0,0,255)
    segments=SEGMENTS(latv)
    if latv==0:
        segments.new_segment(0)
    test_cnt=360
    for i in range(361):
        azi = i

        # horizontal line
        ra,dec = hor_to_radc(alt,azi,latv,lst)
        x,y = ra_dec_to_xyplot(ra,dec,xc,yc,rr,requ=requ)

        # aaa
        # corresponding point at cir_RA
        if latv !=0:
            ang = ra + 90
        else:
            if g_share.f_south:
                ang = int(azi/2)+180
            else:
                if azi < 180:
                    v = 180-azi
                    ang = 360 -int(v/2)
                    ang = 270+ang
                else:
                    ang = 180 +int(azi/2)
                    #v = 360 - azi
                    #ang = 360 -int(v/2)
                    #ang = 90 + ang
                  
                    
                
        if ang >= 360:
            ang -= 360
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)
        xra = int(cos_ang*r_90 + xc)
        yra= int(sin_ang*r_90 + yc)
        if latv==0:
            segments.add(None,None,xra,yra)

        if s ==1:
            s=0
            x0=x
            y0=y
            skip="""
            x0a = xa
            y0a = ya
            x30o = x30
            y30o = y30
            x60o = x60
            y60o = y60
            """
        else:
            # horzontal circles
            #if latv > 1:
            if chk_dist_under(x0,y0,x,y,300):
                #draw.line([(x0,y0),(x,y)],fill=FCOLOR, width=LW)
                
                segments.add(x,y,xra,yra)
                # test
                if test_cnt>0:
                    if config.debug:
                        draw.line([(x,y),(xra,yra)],fill=GREEN, width=LW)
                    test_cnt-=1
            #else:
                
            #    if azi >= 0 and azi < 179 or azi > 182:
            #        draw.line([(x0,y0),(x,y)],fill=FCOLOR, width=LW)
            skip="""
            if chk_dist_under(x30o,y30o,x30,y30,300):    
                draw.line([(x30o,y30o),(x30,y30)],fill=COLOR_BLUE, width=LW)
            draw.line([(x60o,y60o),(x60,y60)],fill=COLOR_BLUE, width=LW)
            
            if azi >= 0 and azi < 150 or azi > 360-150:
                # -18 degree line under horizontal
                draw.line([(x0a,y0a),(xa,ya)],fill=FCOLOR, width=LW)
            """
            x0=x
            y0=y
            skip="""
            x0a = xa
            y0a = ya
            x30o = x30
            y30o = y30
            x60o = x60
            y60o = y60
            """
        if azi==0:
            if latv>0:
                ra_h= 12* 15
                dec_h= -90
            else:
                ra_h = 0 * 15
                dec_h= 90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if latv !=0:
                segments.new_segment(azi,xh,yh,x0,y0)
            # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)


        if azi==90:
            # East
            
            ra_h= 6* 15
            if latv>0:
                dec_h= -90
            else:
                dec_h= 90
                
                xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):            
                segments.new_segment(azi,xh,yh,x0,y0)
            
            # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
                
        
        if azi==180:
            # South

            if latv >0:
                dec_h=-90
                ra_h = 0*15
            else:
                ra_h = 12* 15
                dec_h = 90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):    
                segments.new_segment(azi,xh,yh,x0,y0)
                # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
            

        if azi==270:
            # West
            ra_h = 18*15
            if latv>0:
                dec_h=-90
            else:
                dec_h =90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):    
                segments.new_segment(azi,xh,yh,x0,y0)
                # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)

        if azi==360:
            ra_h = 12*15
            if g_share.f_south:
                dec_h= 90
            else:
                dec_h=-90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            segments.commit_segment(xh,yh)
            
    # draw lines for locating direction
    segments.draw_polygon(draw, 0)
    segments.draw_polygon(draw, 90)
    segments.draw_polygon(draw, 180)
    segments.draw_polygon(draw, 270)
    

def draw_hor_cir(im, draw, xc,yc,rr, latv,lst, longv, place):
    from g_share import g_share
    stroke_width=1
    # avoid extreme cases
    if latv >89:
        latv=89
    if latv < -89:
        latv=-89
    if latv <5 and latv >0:
        latv=5
    if latv <0 and latv >-5:
        latv=-5
    
    seg_f=False
    
    def chk_dist_under(x0,y0,x,y,expected):
        if  math.sqrt((x-x0)**2 + (y-y0)**2) < expected:
            return True
        return False
    r_90 = 180/rr
    #rr = 180/r_90  # 1 degree / pixel in radian direction
    requ = int(r_90/2)  # the equatorial circle
    LW=4
    alt=0
    azi=0
    s=1
    FCOLOR=(0,0,0,255)
    segments=SEGMENTS(latv, ena=False)
    if latv==0:
        segments.new_segment(0)
    test_cnt=360
    for i in range(361):
        azi = i

        # horizontal line
        ra,dec = hor_to_radc(alt,azi,latv,lst)
        x,y = ra_dec_to_xyplot(ra,dec,xc,yc,rr,requ=requ)

        # aaa
        # corresponding point at cir_RA
        if latv !=0:
            ang = ra + 90
        else:
            if g_share.f_south:
                ang = int(azi/2)+180
            else:
                if azi < 180:
                    v = 180-azi
                    ang = 360 -int(v/2)
                    ang = 270+ang
                else:
                    ang = 180 +int(azi/2)
                    #v = 360 - azi
                    #ang = 360 -int(v/2)
                    #ang = 90 + ang
                  
                    
                
        if ang >= 360:
            ang -= 360
        sin_ang = sn(ang)
        cos_ang = r_cs(ang)
        xra = int(cos_ang*r_90 + xc)
        yra= int(sin_ang*r_90 + yc)
        if latv==0:
            segments.add(None,None,xra,yra)
            
        # -2 deg below horizontal line for placing direction marker
        ra_2,dec_2 = hor_to_radc(alt-2,azi,latv,lst)
        xcd,ycd = ra_dec_to_xyplot(ra_2,dec_2,xc,yc,rr,requ=requ)

        # -5 deg below horizontal line for placing direction name
        ra_5,dec_5 = hor_to_radc(alt-5,azi,latv,lst)
        xb,yb = ra_dec_to_xyplot(ra_5,dec_5,xc,yc,rr,requ=requ)
        

        # -18 deg below horizontal line
        ra_18,dec_18 = hor_to_radc(alt-18,azi,latv,lst)
        xa,ya = ra_dec_to_xyplot(ra_18,dec_18,xc,yc,rr,requ=requ)
                
        # 30 deg above horizontal line
        ra30,dec30 = hor_to_radc(alt+30,azi,latv,lst)
        x30,y30 = ra_dec_to_xyplot(ra30,dec30,xc,yc,rr,requ=requ)

        # 60 deg above horizontal line
        ra60,dec60 = hor_to_radc(alt+60,azi,latv,lst)
        x60,y60 = ra_dec_to_xyplot(ra60,dec60,xc,yc,rr,requ=requ)

        if s ==1:
            s=0
            x0=x
            y0=y
            x0a = xa
            y0a = ya
            x30o = x30
            y30o = y30
            x60o = x60
            y60o = y60

        else:
            # horzontal circles
            #if latv > 1:
            if chk_dist_under(x0,y0,x,y,300):
                draw.line([(x0,y0),(x,y)],fill=FCOLOR, width=LW)
                
                segments.add(x,y,xra,yra)
                # test
                if test_cnt>0:
                    if config.debug:
                        draw.line([(x,y),(xra,yra)],fill=GREEN, width=LW)
                    test_cnt-=1
            #else:
                
            #    if azi >= 0 and azi < 179 or azi > 182:
            #        draw.line([(x0,y0),(x,y)],fill=FCOLOR, width=LW)
             
            if chk_dist_under(x30o,y30o,x30,y30,300):    
                draw.line([(x30o,y30o),(x30,y30)],fill=COLOR_BLUE, width=LW)
            draw.line([(x60o,y60o),(x60,y60)],fill=COLOR_BLUE, width=LW)
            
            if azi >= 0 and azi < 150 or azi > 360-150:
                # -18 degree line under horizontal
                draw.line([(x0a,y0a),(xa,ya)],fill=FCOLOR, width=LW)
            x0=x
            y0=y
            x0a = xa
            y0a = ya
            x30o = x30
            y30o = y30
            x60o = x60
            y60o = y60
            
        if azi==0:
            if latv>0:
                ra_h= 12* 15
                dec_h= -90
            else:
                ra_h = 0 * 15
                dec_h= 90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if latv !=0:
                segments.new_segment(azi,xh,yh,x0,y0)
            # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
            
            # North
            if latv !=0:
                draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            
            if latv >=0: 
                lats ='%.1f°N' % latv
            else:
                lats='%.1f°S' % abs(latv)
            if longv is None:
                longs=''
                place=''
            else:
                if longv >=0:
                    longs ='%.1f°E' % longv
                else:
                    longs ='%.1f°W' % abs(longv)
            
            if True:
                #text ='地平綫' +  " (%s %s %s)" % (lats,longs,place)
                text ="(%s %s %s)" % (lats,longs,place)
                yb_ofs=0
                if g_share.f_south==False:
                    if latv>0 and latv<35:
                        yb_ofs=-int(2*MM_UNIT)
                    if latv<0:    
                        if  abs(latv)<20:
                            yb_ofs=-int(3*MM_UNIT)
                        elif abs(latv) <25:
                            yb_ofs = -int(4*MM_UNIT)
                        elif abs(latv) <35:
                            yb_ofs = -int(5*MM_UNIT)
                print("xb:%s yb:%s" % (xb,yb))
                if g_share.f_south and latv<0:
                    if yb<1500:
                        yb=1290
                        xb=1400

                draw_text(im,text , unicode_font_48, xb,yb+yb_ofs,0,stroke_width=stroke_width)
                
        if azi==45:
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            draw_text(im,'東北' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)
                
        if azi==90:
            # East
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            
            draw_text(im,'東' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)
            
            ra_h= 6* 15
            if latv>0:
                dec_h= -90
            else:
                dec_h= 90
                
                xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):            
                segments.new_segment(azi,xh,yh,x0,y0)
            
            # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
            
            # -18-5 deg below horizontal line
            ra_18_5,dec_18_5 = hor_to_radc(alt-18-5,azi,latv,lst)
            x_18_5,y_18_5 = ra_dec_to_xyplot(ra_18_5,dec_18_5, xc,yc,rr)
            draw_text(im,'黎明' , unicode_font_48, x_18_5,y_18_5,0,stroke_width=stroke_width)
            
                
        if azi==90+45:
            # South East
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            draw_text(im,'東南' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)
                
        if azi==180:
            # South
            if True:
                xb1,yb1 = ra_dec_to_xyplot(ra_5, -90,xc,yc,rr,requ=requ)
                draw.line([(xb,yb),(xb1,yb1)],fill=COLOR_RED, width=LW)

                
                
                draw_text(im,'南' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)

            if latv >0:
                dec_h=-90
                ra_h = 0*15
            else:
                ra_h = 12* 15
                dec_h = 90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):    
                segments.new_segment(azi,xh,yh,x0,y0)
                # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
            
        if azi==180+45:
            # South West
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            draw_text(im,'西南' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)
                
        if azi==270:
            # West
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            draw_text(im,'西' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)
            
            ra_h = 18*15
            if latv>0:
                dec_h=-90
            else:
                dec_h =90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            if (g_share.f_south==False and latv>0) or (g_share.f_south and latv<0):    
                segments.new_segment(azi,xh,yh,x0,y0)
                # test
            if config.debug:
                draw.circle((xh,yh), 20, fill=RED)
                draw.circle((x0,y0), 20, fill=RED)
                
        if azi==360-45:
            # North West
            draw.line([(x0,y0),(xcd,ycd)],fill=FCOLOR, width=LW)
            draw_text(im,'西北' , unicode_font_48, xb,yb,0,stroke_width=stroke_width)

        if azi==360:
            ra_h = 12*15
            if g_share.f_south:
                dec_h= 90
            else:
                dec_h=-90
            xh,yh = ra_dec_to_xyplot(ra_h,dec_h,xc,yc,rr,requ=requ)
            segments.commit_segment(xh,yh)
            
    # draw lines for locating direction
    
    azi = 0
    for j in range(8):
        s=1
        for i in range(90):
            alt = i
            ra,dec = hor_to_radc(alt,azi,latv,lst)
            x,y = ra_dec_to_xyplot(ra,dec,xc,yc,rr,requ=requ)
            if s ==1:
                s=0
                x0=x
                y0=y
            else:
                if chk_dist_under(x0,y0,x,y,50):
                    draw.line([(x0,y0),(x,y)],fill=COLOR_BLUE, width=LW)
                x0=x
                y0=y
        azi += 45
        
    mask = Image.new('RGBA', im.size)
    mdraw = ImageDraw.Draw(mask)
    segments.draw_polygon(mdraw, 0)
    segments.draw_polygon(mdraw, 90)
    segments.draw_polygon(mdraw, 180)
    segments.draw_polygon(mdraw, 270)
    
    im2 = Image.alpha_composite(im.convert('RGBA'), mask)
    im.paste(im2,(0,0))
    #im2.save('d:/kcf/dxtc2/polygon.png',dip=(600,600))
    return mask


def add_hor_cir(paper,xc,yc,r2,rr,latv,lst,longv,place,im=None,draw=None): #hour,minute,second,sun_ra):
    LW=4
    if im is not None:
        draw.circle((xc,yc),r2,outline=(0,0,0,255),width=LW)
        draw_hor_mask(im,draw,xc,yc,rr,latv,lst,longv,place)  
        draw_hor_cir(im,draw,xc,yc,rr,latv,lst,longv,place)  
        return
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer_m = paper.add_layer(name='hor_mask')
    layer = paper.add_layer(name='hor_cir')
    layer.draw.circle((xc,yc),r2,outline=(0,0,0,255),width=LW)

    draw_hor_mask(layer.im,layer.draw,xc,yc,rr,latv,lst,longv,place)
    draw_hor_cir(layer.im,layer.draw,xc,yc,rr,latv,lst,longv,place)
