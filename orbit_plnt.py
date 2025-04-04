from ut_math import *
from paper import *
from def_font import *
from word_list import SIGNS
from orbit_cir import draw_orbit_cir
from plnt import *
from sym_arrow import draw_arrow
from ut_orbit import *
from ut_cal import *
from g_share import g_share
from dprint import dprint
from def_plnt import *

N_EARTH=1
N_MERCURY = 2
N_VENUS =3
N_MARS =4
N_JUPITER =5 
N_SATURN = 6
N_URANUS = 7
N_NEPTUNE =8

SUN_COLOR = (255,255,0,255)
MOON_COLOR=(250,250,250,255)
MERCURY_COLOR =(60,60,60,255)
VENUS_COLOR = (255,191,0,255)
EARTH_COLOR =(0,255,0,255)
MARS_COLOR =(255,0,0,255)
JUPITER_COLOR = (255,140,0,255)
#SATURN_COLOR = (80,80,0,255)
SATURN_COLOR = (0xbf,0xff,0,255)

URANUS_COLOR = (30,144,255,255)
NEPTUNE_COLOR = (0,0,205,255)

MERCURY_ARROW_COLOR=(0,0,0,255)

PLNT_COLOR={
    N_EARTH : EARTH_COLOR,
    N_MERCURY : MERCURY_COLOR,
    N_VENUS : VENUS_COLOR,
    N_MARS : MARS_COLOR,
    N_JUPITER : JUPITER_COLOR,
    N_SATURN : SATURN_COLOR,
    N_URANUS : URANUS_COLOR,
    N_NEPTUNE : NEPTUNE_COLOR,
}

ARROW_COLOR={
    N_EARTH : EARTH_COLOR,
    N_MERCURY : MERCURY_ARROW_COLOR,
    N_VENUS : VENUS_COLOR,
    N_MARS : MARS_COLOR,
    N_JUPITER : JUPITER_COLOR,
    N_SATURN : SATURN_COLOR,
    N_URANUS : URANUS_COLOR,
    N_NEPTUNE : NEPTUNE_COLOR,    
}

MERCURY_SZ = 0.38
VENUS_SZ = 0.94
MARS_SZ = 0.53
EARTH_SZ = 1
SCALE_1 = 10

JUPITER_SZ = 11
SATURN_SZ = 9.4
URANUS_SZ = 4
NEPTUNE_SZ = 3.8
SCALE_2 = 1.5

PLNT_SZ ={
    N_EARTH : EARTH_SZ,
    N_MERCURY : MERCURY_SZ,
    N_VENUS : VENUS_SZ,
    N_MARS : MARS_SZ,
    N_JUPITER : JUPITER_SZ,
    N_SATURN : SATURN_SZ,
    N_URANUS : URANUS_SZ,
    N_NEPTUNE : NEPTUNE_SZ,    
}

PLNT_SCALE ={
    N_EARTH : SCALE_1,
    N_MERCURY : SCALE_1,
    N_VENUS : SCALE_1,
    N_MARS : SCALE_1,
    N_JUPITER : SCALE_2,
    N_SATURN : SCALE_2,
    N_URANUS : SCALE_2,
    N_NEPTUNE : SCALE_2,       
}

PLNT_CNAME={
    N_EARTH : '地球',
    N_MERCURY :'水星',
    N_VENUS : '金星',
    N_MARS : '火星',
    N_JUPITER : '木星',
    N_SATURN : '土星',
    N_URANUS : '天王星',
    N_NEPTUNE : '海王星',   
}

def draw_orbit(im, draw,hxc_a, hxc_b, hyc, hr1, hr2, s_au_l, s_au_r,
                    year,month,day,hour,minute,tz,color_f=True):
    global xpln,ypln
    #def draw_orbit_cir(im,draw,hxc,hyc,hr1,hr2):
    hr1a = hr1 - 30
    
    #calculate mercury and mars orbit

    # store x,y and longitude
    mercury_xyl=[]
    mars_xyl =[]
    n=1
    for i in range(24):
        for d in range(2,30):
            PlntPos(d,month,year,hour-tz,minute)
            mars_xyl.append((xpln[4],ypln[4],pLong[4]))
            if n < 5:
                mercury_xyl.append((xpln[2],ypln[2],pLong[2]))
    
        month+=1
        n+=1
        if month >12:
            month=1
            year+=1


    if True:
        # solar system left side
        s_au= s_au_l  #=16  # 1 AU = 19 pixel

        # orbits:
        for n_plnt in [N_MERCURY,N_VENUS,N_EARTH,N_MARS,
                      N_JUPITER,N_SATURN,N_URANUS,N_NEPTUNE]:
            if color_f:
                n_color = PLNT_COLOR[n_plnt] #.get(n_plnt, WHITE)
            else:
                n_color = BLACK
            r = g_share.pln_0[n_plnt].r
            draw.circle((hxc_a,hyc),int(r * s_au),
                            outline=n_color,width=2) # mercury

        l_mars_yh = hyc + int(g_share.pln_0[N_MARS].r * s_au)
        l_mars_yl = hyc - int(g_share.pln_0[N_MARS].r * s_au)
                  
        # solar system right side  .. mars        
        s_au = s_au_r # = 300 # 1 AU =  pixel

        r_earth=1
        r_venus= g_share.pln_0[N_VENUS].r
        for n_plnt,dx in [(N_EARTH,r_earth),(N_VENUS,r_venus)]:
            if color_f:
                n_color = PLNT_COLOR[n_plnt]
            else:
                n_color = BLACK
            draw.circle((hxc_b,hyc),dx * s_au,outline=n_color,width=2)

        r_mars_yh=None
        r_mars_yl=None
        r_mars_x =hxc_b - 100
        
        for n_pln, xyl in [(N_MERCURY,mercury_xyl),(N_MARS, mars_xyl)]:
            if color_f:
                color = PLNT_COLOR[n_pln]
            else:
                color = BLACK
            x0,y0,l0 = xyl[0]
            hx0_b,hy0_b =  xy_to_hxy_r(x0,y0, hxc_b,hyc,s_au_r)
            for x,y,l in xyl[1:]:
                hx_b,hy_b =  xy_to_hxy_r(x,y, hxc_b,hyc,s_au_r)
                if n_pln==N_MARS:
                    #print('hx_b:%s hy_b:%s' % (hx_b,hy_b))
                    if r_mars_yh is None and hy_b> hyc:
                        if hx_b > r_mars_x:
                            r_mars_yh=hy_b
                    if r_mars_yl is None and hy_b < hyc:
                        if hx_b < r_mars_x:
                            r_mars_yl=hy_b
                            
                draw.line([(hx0_b,hy0_b),(hx_b,hy_b)],fill=color,width=2)
                hx0_b=hx_b
                hy0_b=hy_b
    
    return l_mars_yh, l_mars_yl, r_mars_yh, r_mars_yl, r_mars_x
    
def draw_orbit_plnt(im, draw,hxc_a, hxc_b, hyc, hr1, hr2, s_au_l, s_au_r,
                    year,month,day,hour,minute,tz,color_f=True):
    global xpln,ypln
    #def draw_orbit_cir(im,draw,hxc,hyc,hr1,hr2):
    hr1a = hr1 - 30
    font = unicode_font_36
    
    if True:
        # solar system left side
        s_au= s_au_l  #=16  # 1 AU = 19 pixel


        # solar system right side  .. mars
        s_au = s_au_r # = 300 # 1 AU =  pixel

        # sun position
        draw_text(im, '太陽', font,hxc_b,hyc-30,0)

        skip="""
        draw.line([(hxc_a-10,hyc),(hxc_a+10,hyc)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_a,hyc-10),(hxc_a,hyc+10)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_a-8,hyc-8),(hxc_a+8,hyc+8)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_a+8,hyc-8),(hxc_a-8,hyc+8)],fill=SUN_COLOR,width=2)

        draw.line([(hxc_b-10,hyc),(hxc_b+10,hyc)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_b,hyc-10),(hxc_b,hyc+10)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_b-8,hyc-8),(hxc_b+8,hyc+8)],fill=SUN_COLOR,width=2)
        draw.line([(hxc_b+8,hyc-8),(hxc_b-8,hyc+8)],fill=SUN_COLOR,width=2)
        """
        if color_f:
            n_color=SUN_COLOR
        else:
            n_color=WHITE
        draw.circle((hxc_b,hyc),20,outline=(0,0,0,255),fill=n_color,width=2)    


        
        # earth position on right side
        #xyzr_sun_to_hxy_earth(x_sun,y_sun,hxc_b,hyc,s_au_r):
        if color_f:
            color = PLNT_COLOR[N_EARTH] #.get(n_plnt,WHITE)
            acolor = ARROW_COLOR[N_EARTH]
        else:
            color = WHITE
            acolor = BLACK
        x_sun =g_share.sun_0.x
        y_sun = g_share.sun_0.y
        xsun_10 =g_share.sun_10.x
        ysun_10 = g_share.sun_10.y
        hx_b, hy_b = xyzr_sun_to_hxy_earth(x_sun, y_sun, hxc_b,hyc,s_au_r)
        #if CONFIG.STAR_HAS_COLOR:
        draw.circle((hx_b,hy_b),10,outline=(0,0,0,255),fill=color,width=2)        
        draw_text(im, '地球', font,hx_b+20,hy_b-40,0)
        #xyzr_sun_to_hxy_earth(x_sun,y_sun,hxc_b,hyc,s_au_r)
        hx_b1, hy_b1 =xyzr_sun_to_hxy_earth(xsun_10, ysun_10,hxc_b,hyc,s_au_r)
        ang = atn2(hy_b1-hyc, hx_b1-hxc_b)
        draw_arrow(im, hx_b1,hy_b1, 20, ang, acolor, name='earth')
        
        for n_plnt in [N_MERCURY,N_VENUS,N_MARS]:
            xp = g_share.pln_0[n_plnt].x
            yp = g_share.pln_0[n_plnt].y
            xp10 = g_share.pln_10[n_plnt].x
            yp10 = g_share.pln_10[n_plnt].y
            hx_b, hy_b = xy_to_hxy_r(xp,yp, hxc_b,hyc, s_au_r)
            dprint('hxc_b:%s, hyc:%s, xp:%s yp:%s, hx_b:%s hy_b:%s' % 
              (hxc_b, hyc, xp,yp, hx_b, hy_b))
            if color_f:
                color = PLNT_COLOR[n_plnt] #.get(n_plnt,WHITE)
                acolor = ARROW_COLOR[n_plnt]
            else:
                color = WHITE
                acolor = BLACK
                
            n_sz = PLNT_SZ.get(n_plnt, 2)
            n_name=PLNT_CNAME.get(n_plnt,'--')
            #acolor=ARROW_COLOR.get(n_plnt,BLACK)
            n_scale=SCALE_1
            draw.circle((hx_b,hy_b),n_sz * n_scale,outline=(0,0,0,255),
                    fill=color,width=2)
            draw_text(im, n_name, font,hx_b+20,hy_b-40,0)
            #xy_to_hxy_r(x,y, hxc_b,hyc,s_au_r)
            hx_b1, hy_b1 =xy_to_hxy_r(xp10,yp10,hxc_b,hyc,s_au_r)
            ang = atn2(hy_b1-hyc, hx_b1-hxc_b)
            draw_arrow(im, hx_b1,hy_b1, 20, ang, acolor)

        for n_plnt in [N_JUPITER,N_SATURN,N_URANUS,N_NEPTUNE]:
            xp = g_share.pln_0[n_plnt].x
            yp = g_share.pln_0[n_plnt].y
            #xp10 = g_share.pln_10[n_plnt].x
            #yp10 = g_share.pln_10[n_plnt].y
            xp2yr = g_share.pln_2yr[n_plnt].x
            yp2yr = g_share.pln_2yr[n_plnt].y
            hx, hy = xy_to_hxy_l(xp,yp, hxc_a,hyc, s_au_l)
            dprint('hxc_b:%s, hyc:%s, xp:%s yp:%s, hx_b:%s hy_b:%s' % 
              (hxc_b, hyc, xp,yp, hx, hy))
            if color_f:
                color = PLNT_COLOR[n_plnt] #.get(n_plnt,WHITE)
                acolor = ARROW_COLOR[n_plnt]
            else:
                color = WHITE
                acolor = BLACK
            #color = PLNT_COLOR[n_plnt] #.get(n_plnt,WHITE)
            n_sz = PLNT_SZ[n_plnt] #.get(n_plnt, 2)
            n_name=PLNT_CNAME[n_plnt] #.get(n_plnt,'--')
            #acolor=ARROW_COLOR[n_plnt] #.get(n_plnt,BLACK)
            n_scale=SCALE_2
            draw.circle((hx,hy),n_sz * n_scale,outline=(0,0,0,255),
                    fill=color,width=2)
            draw_text(im, n_name, font,hx+20,hy-40,0)
            #xy_to_hxy_r(x,y, hxc_b,hyc,s_au_r)
            hx_1, hy_1 =xy_to_hxy_l(xp2yr,yp2yr,hxc_a,hyc,s_au_l)
            ang = atn2(hy_1-hyc, hx_1-hxc_a)
            draw_arrow(im, hx_1,hy_1, 20, ang, acolor)
     
            
def text_au(im,draw,x0,y0,s_au,n_au,font):
    #x0 = hxc_a + int(10 * MM_UNIT)
    x1= x0+s_au * n_au
    xt = x0 + int(s_au *n_au/2)
    #y0 = hyc+int(25 * MM_UNIT)
    y1 = y0+20
    y2 = y1+10
    draw.line([(x0,y1),(x1,y1)], fill=(0,0,0,255),width=2)
    draw.line([(x0,y0),(x0,y2)], fill=(0,0,0,255),width=2)
    draw.line([(x1,y0),(x1,y2)], fill=(0,0,0,255),width=2)
    text='%s AU' % n_au
    #font = unicode_font_42
    angle=0
    #_draw_text((x0+50,y1-50), text="15 AU",font=unicode_font_48,fill=(0,0,0))
    draw_text(im, text, font, xt,y1-30,angle)


def add_orbit_plnt(im,draw,OFS_A,OFS_B,OFS_Y,
                   year,month,day,hour,minute,tz,color_f=True):
    #OFS_A = MIN_X + int(5 * MM_UNIT)
    #OFS_B = MIN_X + int(60 * MM_UNIT)
    #OFS_Y = int(10 * MM_UNIT)
    hr1 = int(18 * MM_UNIT)
    hr2 = hr1 - 60
    hxc_a = OFS_A + hr1
    hxc_b = OFS_B + hr1 

    hyc = OFS_Y + hr1
    
    #hyc = hr1
    draw_orbit_cir(im,draw,hxc_a,hyc,hr1,hr2)
    draw_orbit_cir(im,draw,hxc_b,hyc,hr1,hr2)
    
    s_au_l=15   # 1AU = ? pixel
    s_au_r =280   # 1AU = ? pixel
    
    s_au_l = 10
    s_au_r = 200

    l_yh,l_yl,r_yh,r_yl,r_x=draw_orbit(layer.im, layer.draw,hxc_a, hxc_b, hyc, hr1, hr2,
                    s_au_l, s_au_r,
                   year,month,day,hour,minute,tz,color_f=color_f)
    
    # lines connect the two orbits
    layer.draw.line([(hxc_a,l_yh),(r_x,r_yh)],fill=RED)
    layer.draw.line([(hxc_a,l_yl),(r_x,r_yl)],fill=RED)
    
    draw_orbit_plnt(im, draw,hxc_a, hxc_b, hyc, hr1, hr2,
                    s_au_l, s_au_r,
                   year,month,day,hour,minute,tz,color_f=color_f)
    
    font = unicode_font_42
    x0 = hxc_a + int(15 * MM_UNIT)
    y0 = hyc+int(15 * MM_UNIT)
    
    s_au = s_au_l
    n_au = 15
    
    text_au(im,draw,x0,y0,s_au,n_au,font)
    
    #x0 = OFS_A
    text='外側行星軌道'
    layer.draw.text((x0,OFS_Y),text=text, font=font, fill=(0,0,0,255))
    text="箭頭所指為兩年行程"
    layer.draw.text((x0,OFS_Y+50),text=text, font=font, fill=(0,0,0,255))
    
    x0 = hxc_b + int(15 * MM_UNIT)
    y0 = hyc+int(15 * MM_UNIT)
    s_au = s_au_r
    n_au = 1
    text_au(im,draw,x0,y0,s_au,n_au,font)
    
    #x0 = OFS_B #int(60 * MM_UNIT)
    text='内側行星軌道'
    draw.text((x0,OFS_Y),text=text, font=font, fill=(0,0,0,255))
    text="箭頭所指為十天行程"
    draw.text((x0,OFS_Y+50),text=text, font=font, fill=(0,0,0,255))
    
    

