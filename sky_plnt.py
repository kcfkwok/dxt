from def_font import *
from def_plnt import *
from ut_star import *
from lunar_python import Lunar
from datetime import datetime

MAG_SUN_R=20
MAG_MOON_R=20

SMALL_MAG_SUN_R=10
SMALL_MAG_MOON_R =10

TXT_FONT = unicode_font_56  
TXT_R = 40

#SMALL_TXT_FONT = unicode_font_42
#SMALL_TXT_R=30
SMALL_TXT_FONT = unicode_font_36
SMALL_TXT_R=26

DEF_SUN_COLOR = (255,255,0,255)
DEF_MOON_COLOR=(250,250,250,255)
DEF_MERCURY_COLOR =(0xbe,0xbb,0xab, 255) #(60,60,60,0)
DEF_VENUS_COLOR = (0xfd, 0xd9, 0x22, 255) #(255,191,0,0)
DEF_EARTH_COLOR =(0,255,0,0)
DEF_MARS_COLOR = (0xfd, 0x22,0x22,255) #(0xce,0x87,0x53,255) #(255,0,0,0)
DEF_JUPITER_COLOR = (0xd9, 0xbc, 0x6a,255) #(255,140,0,0)
DEF_SATURN_COLOR = (0xdd, 0xe2, 0xa4, 255) #(0xbf,0xff,0,255)
DEF_URANUS_COLOR = (0x50, 0xdb, 0xe0, 255) #(30,144,255,255)
DEF_NEPTUNE_COLOR = (0x19,0x8e, 0xea, 255) #(30,100,205,0)

SUN_COLOR = (255,255,0,255)
MOON_COLOR=(250,250,250,255)
MERCURY_COLOR =DEF_MERCURY_COLOR #(250,250,250,255)
VENUS_COLOR = DEF_VENUS_COLOR #(255,191,0,255)
EARTH_COLOR =(0,255,0,255)
MARS_COLOR =DEF_MARS_COLOR #(255,0,0,255)
JUPITER_COLOR = DEF_JUPITER_COLOR #(255,140,0,255)
SATURN_COLOR = DEF_SATURN_COLOR
URANUS_COLOR = DEF_URANUS_COLOR #(30,144,255,255)
NEPTUNE_COLOR = DEF_NEPTUNE_COLOR #(0,0,205,255)

SYM_COLORS={
    K_SUN:SUN_COLOR,
    K_MOON:MOON_COLOR,
    K_MERCURY: MERCURY_COLOR,
    K_VENUS: VENUS_COLOR,
    K_MARS:  MARS_COLOR,
    K_JUPITER: JUPITER_COLOR,
    K_SATURN:  SATURN_COLOR,
    K_URANUS: URANUS_COLOR,
    K_NEPTUNE: NEPTUNE_COLOR,
}

PLN_MAG_R={
    K_SUN:20,
    K_MOON:20,
    K_MERCURY: MAG_N_R,
    K_VENUS: MAG_N_R,
    K_MARS:  MAG_N_R,
    K_JUPITER: MAG_N_R,
    K_SATURN:  MAG_N_R,
    K_URANUS:  MAG_X_R,
    K_NEPTUNE: MAG_X_R,
    
}

SMALL_MAG_N_R= int(MAG_N_R /2)
SMALL_PLN_MAG_R={
    K_SUN:10,
    K_MOON:10,
    K_MERCURY: SMALL_MAG_N_R,
    K_VENUS: SMALL_MAG_N_R,
    K_MARS:  SMALL_MAG_N_R,
    K_JUPITER: SMALL_MAG_N_R,
    K_SATURN:  SMALL_MAG_N_R,
    K_URANUS:  SMALL_MAG_N_R,
    K_NEPTUNE: SMALL_MAG_N_R,
    
}

def draw_arrow(image, x,y,L,iangle,color, ar_width=None):
    #print('draw_arrow ang:',iangle)
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

def cal_dist(x,y,xx,yy):
    d2= (x-xx) **2 + (y-yy) **2
    d = math.sqrt(d2)
    return d

def get_pn_info(pn):
    dprint('get_pn_info', pn_info_dict[pn][0])
    pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a = pn_info_dict[pn]
    return pnamea, xa,ya,anga,sin_anga,cos_anga

def get_pn_r5c(pn):
    pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a = pn_info_dict[pn]
    return vr_a

def pre_cal_txt_pos(xc,yc,r5b,r5c,txt_r):
    if True:
        global pn_info_dict, pn_info_dict2
        pn_info_dict={}
        pn_info_dict2={}
        for pn in range(9):
            #ra = pRA[pn]
            ra = g_share.pln_0[pn].ra
            ang = config.ari_ang + ra
            sin_ang = sn(ang)
            cos_ang = r_cs(ang)
            x5b = int(cos_ang*r5b + xc)
            y5b = int(sin_ang*r5b + yc)
            pn_info_dict[pn]=[K_PLNT_NAMES[pn],x5b,y5b,ang,sin_ang,cos_ang,r5b,r5c]
        pn_info_dict2[K_MOON]=pn_info_dict[K_MOON]
        collided=False
        for pna in [K_SUN,K_MERCURY,K_VENUS,K_MARS,K_JUPITER,K_SATURN,K_URANUS,K_NEPTUNE]:
            pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a = pn_info_dict[pna]
            for pnb in list(pn_info_dict2.keys()):
                pnameb, xb,yb,angb,sin_angb,cos_angb,r_b,vr_b = pn_info_dict2[pnb]
                dd = cal_dist(xa,ya, xb,yb)
                if dd < (2* txt_r):
                    #print('collided %s(%s,%s,%s) %s(%s,%s,%s) ' % (pnamea,xa,ya,r_a, pnameb,xb,yb,r_b))
                    dprint('collided %s(%s,%s,%s) %s(%s,%s,%s) dd:%s ~ %s' % (pnamea,xa,ya,r_a, pnameb,xb,yb,r_b,dd, TXT_R*2))

                    #ff = math.sqrt((TXT_R*2)**2 -dd**2 )
                    r_a = r_a - (2* txt_r +2)
                    vr_a = vr_a - (2* txt_r+2)
                    xa = int(cos_anga*r_a+xc)
                    ya = int(sin_anga*r_a +yc)
                    pn_info_dict[pna]= [pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a]
                    pn_info_dict2[pna]= [pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a]
                    collided=True
                else:
                    pn_info_dict2[pna]= pn_info_dict[pna]
            
        if collided:
            pn_info_dict2={}
            pn_info_dict2[K_MOON]=pn_info_dict[K_MOON]
            for pna in [K_SUN,K_MERCURY,K_VENUS,K_MARS,K_JUPITER,K_SATURN,K_URANUS,K_NEPTUNE]:
                pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a = pn_info_dict[pna]
                for pnb in list(pn_info_dict2.keys()):
                    pnameb, xb,yb,angb,sin_angb,cos_angb,r_b,vr_b = pn_info_dict2[pnb]
                    dd = cal_dist(xa,ya, xb,yb)
                    if dd < (2* txt_r):
                        #print('collided %s %s' % (pnamea, pnameb))
                        dprint('collided %s(%s,%s,%s) %s(%s,%s,%s) dd:%s ~ %s' % (pnamea,xa,ya,r_a, pnameb,xb,yb,r_b,dd, TXT_R*2))
                        #ff = math.sqrt((TXT_R*2)**2 -dd**2 )
                        r_a = r_a - (2* txt_r+2)
                        vr_a = vr_a - (2* txt_r+2)
                        xa = int(cos_anga*r_a+xc)
                        ya = int(sin_anga*r_a +yc)
                        pn_info_dict[pna]= [pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a]
                        pn_info_dict2[pna]= [pnamea, xa,ya,anga,sin_anga,cos_anga,r_a,vr_a]
                        collided=True
                    else:
                        pn_info_dict2[pna]= pn_info_dict[pna]


def cal_lun_ang(sx,sy,mx,my):
    ang= atn2(my-sy,mx-sx)
    if ang <0:
        ang=ang+360
    elif ang >=360:
        ang=ang-360
    return ang


def draw_moon(image, x,y,phase,inangle, R=20):
    COLOR_LIGHT = (0,0,0,255)
    COLOR_DARK = (250,250,250,255)

    if phase > 0.5:
        phase = 1-phase
    angle = (360-inangle) + 180
    if angle > 360:
        angle-=360
    D = R *2
    left = 0
    width = D
    right = 0
    height = D
    im2 = Image.new(mode='RGBA',size=(width, height),color=(255,255,255))
    draw2 = ImageDraw.Draw(im2)
    #draw2.line([(0,0),(0,WIDTH)],fill=(0,255,0,255))
    #draw2.line([(0,0),(HEIGHT,0)],fill=(0,255,0,255))
    #draw2.line([(0,0),(100,100)],fill=(0,255,0,255))

    for ypos in range(R):
        xpos = int(math.sqrt(R*R - ypos*ypos))
        #// Draw darkness part of the moon
        pb1 = (R-xpos, R+ypos)
        pb2 = (R+xpos, R+ypos)
        pb3 = (R-xpos, R-ypos)
        pb4 = (R+xpos, R-ypos)
        draw2.line([pb1, pb2], fill=COLOR_DARK)
        draw2.line([pb3, pb4], fill=COLOR_DARK)
        #// Determine the edges of the lighted part of the moon       
        rpos = 2 * xpos
        if phase < 0.5:
            xpos1 = -xpos
            xpos2 = int(rpos - 2 * phase*rpos - xpos)
        else:
            xpos1 = xpos
            xpos2 = int(xpos - 2 * phase * rpos + rpos)
        #// Draw the lighted part of the moon           
        pw1 = (R+xpos1, R-ypos)
        pw2 = (R+xpos2, R-ypos)
        pw3 = (R+xpos1, R+ypos)
        pw4 = (R+xpos2, R+ypos)
        draw2.line([pw1,pw2], fill=COLOR_LIGHT)
        draw2.line([pw3,pw4], fill=COLOR_LIGHT)
    draw2.circle((R,R),R,outline=(0,0,0,255))
    im2 = im2.rotate(angle, expand=1)
    sx, sy = im2.size
    #print(sx,sy)
    px = x - int(sx/2)
    py = y - int(sy/2)
    #print(px,py,sx,sy)
    #image.paste(im2, (px, py, px + sx, py + sy), im2)
    image.paste(im2, (px, py), im2)
    
def draw_moon_sym(im, draw,xc,yc,rr,r5,r5d,year,month,day,hour,minute,tz,f_south,
                 small=False, color_f=True):
    k = K_MOON
    if color_f:
        kcolor = SYM_COLORS.get(k, WHITE)
    else:
        kcolor = WHITE
        
    k_sym = K_PLNT_CNAMES.get(k,'?')
    if small:
        k_mag_r =SMALL_PLN_MAG_R.get(k, SMALL_MAG_N_R)
    else:
        k_mag_r =PLN_MAG_R.get(k, MAG_N_R)
        
    if f_south:
        TEXT_ANG_OFS=90
    else:
        TEXT_ANG_OFS=270
    FCOLOR=(0,0,0,255)
    if small:
        CIR_TXT_LW = 2
        CIR_PLN_LW = 2
        txt_r = SMALL_TXT_R
        txt_font = SMALL_TXT_FONT
    else:
        CIR_TXT_LW = 3
        CIR_PLN_LW = 3
        txt_r = TXT_R
        txt_font = TXT_FONT
        
    ari_ang = config.ari_ang
    ra = g_share.pln_0[k].ra
    dec = g_share.pln_0[k].dec
    ra1 = g_share.pln_1[k].ra
    dec = g_share.pln_1[k].dec   
    x,y = ra_dec_to_xyplot(ra, dec, xc,yc,rr,f_south=f_south)
    #ang = ari_ang + ra
    #sin_ang = sn(ang)
    #cos_ang = r_cs(ang)
    pname, x5b,y5b,ang,sin_ang,cos_ang = get_pn_info(k)
    ra0 = ra
    if abs(ra1-ra) <0.1:
        if (ra1-ra) >0:
            ra0 = ra1-1
        else:
            ra0 = ra1 +1
            
    ang0 = ari_ang + ra0
    sin_ang0 = sn(ang0)
    cos_ang0 = r_cs(ang0)

    if True:
        # MOON track for 1 day
        x5c = int(cos_ang*r5d + xc)
        y5c = int(sin_ang*r5d + yc)
        ang1 = ari_ang + ra1
        sin_ang1 = sn(ang1)
        cos_ang1 = r_cs(ang1)
        x5c1 = int(cos_ang1*r5d + xc)
        y5c1 = int(sin_ang1*r5d + yc)
        ar_ang = atn2(y5c1-y5c, x5c1-x5c) + 90
        if small:
            ar_width=5
        else:
            ar_width=10
        draw_arrow(im, x5c1,y5c1, 40, ar_ang, FCOLOR,ar_width=ar_width) 
        dprint('moon arrow x:%s y:%s ang:%s' % (x5c1,y5c1,ang))
        draw.line([(x5c,y5c),(x5c1,y5c1)], fill=FCOLOR,width=2)
        
    x5 = int(cos_ang*r5 + xc)
    y5 = int(sin_ang*r5 + yc)
    draw.line([(x5,y5),(x,y)], fill=FCOLOR)
    #x5b = int(cos_ang*r5b + xc)
    #y5b = int(sin_ang*r5b + yc)
    #ang=360-ang + TEXT_ANG_OFS
    if f_south:
        txt_ang=ang + TEXT_ANG_OFS
    else:
        txt_ang=360-ang + TEXT_ANG_OFS
    #print('ang:',ang)
    
    draw.circle((x5b,y5b),txt_r,outline=FCOLOR,fill=kcolor,width=CIR_TXT_LW)
    draw_text(im, k_sym, txt_font,x5b,y5b,txt_ang)  
    
    ra = g_share.pln_0[K_SUN].ra
    dec = g_share.pln_0[K_SUN].dec
    sun_x,sun_y = ra_dec_to_xyplot(ra, dec, xc, yc,rr,f_south=f_south)
    ra = g_share.pln_0[K_MOON].ra
    dec = g_share.pln_0[K_MOON].dec
    moon_x, moon_y = ra_dec_to_xyplot(ra, dec, xc, yc,rr,f_south=f_south)
    
    lun_cal = Lunar.fromDate(datetime(year,month,day))
    lun_d = lun_cal.getDay()
    dprint('lun_d:',lun_d)
    lun_ph = lun_d /30

    lun_ang = cal_lun_ang(sun_x,sun_y,moon_x,moon_y)
    draw_moon(im,moon_x,moon_y,lun_ph,lun_ang, R=k_mag_r)
    draw.circle((moon_x,moon_y),k_mag_r,outline=FCOLOR,width=1)


def draw_plnt_sym(im, draw, k, xc,yc,rr,r1,r5,f_south,small=False,color_f=True):

    if color_f:    
        kcolor = SYM_COLORS.get(k, WHITE)
    else:
        kcolor= WHITE
        
    k_sym = K_PLNT_CNAMES.get(k,'?')
    if small:
        txt_r = SMALL_TXT_R
        txt_font = SMALL_TXT_FONT
        k_mag_r =SMALL_PLN_MAG_R.get(k, MAG_N_R)
    else:
        txt_r = TXT_R
        txt_font = TXT_FONT
        k_mag_r =PLN_MAG_R.get(k, MAG_N_R)
    if f_south:
        TEXT_ANG_OFS=90
    else:
        TEXT_ANG_OFS=270
    FCOLOR=(0,0,0,255)
    if small:
        CIR_TXT_LW = 2
        CIR_PLN_LW = 2
    else:
        CIR_TXT_LW = 3
        CIR_PLN_LW = 3
        
    ari_ang = config.ari_ang
    ra = g_share.pln_0[k].ra
    dec = g_share.pln_0[k].dec
    ra1 = g_share.pln_1[k].ra
    dec = g_share.pln_1[k].dec   
    x,y = ra_dec_to_xyplot(ra, dec, xc,yc,rr,f_south=f_south)
    #print('k:%s ra:%s dec:%s x:%s y:%s xc:%s yc:%s rr:%s f_s:%s' % 
    #     (k,ra,dec,x,y,xc,yc,rr,f_south))
    #ang = ari_ang + ra
    #sin_ang = sn(ang)
    #cos_ang = r_cs(ang)
    pname, x5b,y5b,ang,sin_ang,cos_ang = get_pn_info(k)
    ra0 = ra
    if abs(ra1-ra) <0.1:
        if (ra1-ra) >0:
            ra0 = ra1-1
        else:
            ra0 = ra1 +1
            
    ang0 = ari_ang + ra0
    sin_ang0 = sn(ang0)
    cos_ang0 = r_cs(ang0)
    vr5c = get_pn_r5c(k)
    # test
    #draw.circle((xc,yc),vr5c, outline=(0,0,0,255))
    
    x5c = int(cos_ang0*vr5c + xc)
    y5c = int(sin_ang0*vr5c + yc)  
    
    ang1 = ari_ang + ra1
    sin_ang1 = sn(ang1)
    cos_ang1 = r_cs(ang1)
    x5c1 = int(cos_ang1*vr5c + xc)
    y5c1 = int(sin_ang1*vr5c + yc)
    ar_ang = atn2(y5c1-y5c, x5c1-x5c) + 90
    if small:
        ar_width = 5
    else:
        ar_width =10
    draw_arrow(im, x5c1,y5c1, 40, ar_ang, FCOLOR,ar_width=ar_width) 
    draw.line([(x5c,y5c),(x5c1,y5c1)], fill=FCOLOR,width=2)
    
    if k==K_SUN:
        x5 = int(cos_ang*r1 + xc)
        y5 = int(sin_ang*r1 + yc)
        if color_f:
            draw.line([(x5,y5),(x,y)], fill=RED)
        else:
            draw.line([(x5,y5),(x,y)], fill=FCOLOR)
            
    else:
        x5 = int(cos_ang*r5 + xc)
        y5 = int(sin_ang*r5 + yc)
        draw.line([(x5,y5),(x,y)], fill=FCOLOR)
    #x5b = int(cos_ang*r5b + xc)
    #y5b = int(sin_ang*r5b + yc)
    #ang=360-ang + TEXT_ANG_OFS
    if f_south:
        txt_ang=ang + TEXT_ANG_OFS
    else:
        txt_ang=360-ang + TEXT_ANG_OFS
    #print('ang:',ang)
    draw.circle((x5b,y5b),txt_r,outline=FCOLOR,fill=kcolor,width=CIR_TXT_LW)
    draw_text(im, k_sym, txt_font,x5b,y5b,txt_ang)  
    draw.circle((x,y), k_mag_r, outline=FCOLOR, fill=kcolor, width = CIR_PLN_LW)


def draw_sky_plnt(im, draw, xc, yc,r1,r5,r5b,rr,
                    year,month,day,hour,minute,tz,small=False,color_f=True):

    f_south = config.f_south 
    #config.small=small
    if small:
        txt_r = SMALL_TXT_R
        r5c = r5b - txt_r-5 # for track arrow
        r5d = r5b + txt_r+5 # for track arrow of MOON
    else:
        txt_r = TXT_R
        r5c = r5b - txt_r-10 # for track arrow
        r5d = r5b + txt_r+10 # for track arrow of MOON
    if f_south:
        TEXT_ANG_OFS=90
    else:
        TEXT_ANG_OFS=270
    FCOLOR=(0,0,0,255)
    CIR_TXT_LW = 3
    CIR_PLN_LW = 3
    ari_ang = config.ari_ang
    pre_cal_txt_pos(xc,yc,r5b,r5c,txt_r)
    for k in [K_NEPTUNE,K_URANUS,K_SATURN,K_JUPITER,K_MERCURY,K_VENUS,K_MARS,K_SUN]:
        draw_plnt_sym(im, draw, k, xc,yc,rr,r1,r5,f_south,small=small,color_f=color_f)
        
    draw_moon_sym(im, draw, xc,yc,rr,r5,r5d,year,month,day,hour,minute,tz,f_south,
                  small=small,color_f=color_f)


def add_sky_plnt(paper,xc,yc,r1,r5,r5b,rr,year,month,day,hour,minute,tz,f_south=False,
                 im=None,draw=None,small=False,color_f=True):
    LW=2
    if im is not None:
        draw_sky_plnt(im, draw, xc, yc,r1,r5, r5b,rr,
                    year,month,day,hour,minute,tz,small=small,color_f=color_f)
        return
    MAX_X = paper.max_x
    MIN_X = paper.min_x
    MIN_Y = paper.min_y
    MAX_Y = paper.max_y
    layer = paper.add_layer(name='sky_plnt')
    draw_sky_plnt(layer.im, layer.draw, xc, yc,r1,r5, r5b,rr,
                    year,month,day,hour,minute,tz,small=small,color_f=color_f)
