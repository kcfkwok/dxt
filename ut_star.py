from starsln import starsln
from starsi import starsi
from csts import CSTS
from config import config
from g_share import g_share
g_share.stars_plotted=[]
from paper import *
from ut_cal import *

MAG_N_R = 12
MAG_0_R = 11
MAG_1_R = 9
MAG_2_R = 7
MAG_3_R = 5
MAG_4_R = 3
MAG_5_R = 2
MAG_X_R = 1

def mag_to_r(mag):
    if mag <0:
        r=MAG_N_R  #12
    elif mag <1:
        r=MAG_0_R  #11
    elif mag <2:
        r=MAG_1_R  #9
    elif mag <3:
        r=MAG_2_R   #7
    elif mag <4:
        r=MAG_3_R   #5
    elif mag <5:
        r=MAG_4_R   #3
    else:
        r=MAG_5_R   #2
    return r

SP_COLORS={
    'O': (0,183,235,255),
    'B':(0,255,255,255),
    'A':(224,255,255,255),
    'F':(255,255,255,255),
    'G':(238,255,27,255),
    'K':(255,140,0,255),
    'M':(255,0,0,255),
}

def SP_to_color(sp):
    if sp in SP_COLORS:
        return SP_COLORS[sp]
    return (255,255,255,0)

def draw_obj(draw, ra,dec, r_deg, color, xc,yc,rr):
    r = round(r_deg)
    x,y =ra_dec_to_xyplot(ra,dec,xc,yc,rr)
    draw.circle((x,y),r,fill=color)
    print('draw_obj x:%s y:%s r_deg:%s r:%s' % (x,y,r_deg,r))

def draw_star(draw, star,xc,yc,rr,
              small=False,color_f=True):
    FCOLOR=(0,0,0,255)
    #BGCOLOR=(255,255,255,0)
    #LW=4
    Ra,decl,mag,sp= starsi[star]
    x,y =ra_dec_to_xyplot(Ra,decl,xc,yc,rr)
    #if star not in stars_plotted:
    r = mag_to_r(mag)
    if small:
        r= round(r/2)
    if color_f:
        co = SP_to_color(sp)
        if sp=='A' or sp=='F' or r >3:
            draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
        else:
            draw.circle((x,y),r,outline=co, fill=co,width=2)
    else:
        draw.circle((x,y),r,outline=FCOLOR,width=2)
        
        skip="""
        else:
            if CONFIG.STAR_USE_WHITE:
                draw.circle((x,y),r,outline=FCOLOR, fill=WHITE_COLOR,width=2)
            else:
                co = rgb_2_grey(SP_to_color(sp))
                if sp=='A' or sp=='F' or r >3:
                    draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
                else:
                    draw.circle((x,y),r,outline=co, fill=co,width=2)
        """    
        g_share.stars_plotted.append(star)
    return x,y
    
def draw_star_at(draw, star,x,y,color_f=True):
    FCOLOR=(0,0,0,255)
    #BGCOLOR=(255,255,255,0)
    #LW=4
    Ra,decl,mag,sp= starsi[star]
    r = mag_to_r(mag)
    if color_f:
        co = SP_to_color(sp)
        if sp=='A' or sp=='F' or r >3:
            draw.circle((x,y),r,outline=FCOLOR, fill=co,width=2)
        else:
            draw.circle((x,y),r,outline=co, fill=co,width=2)
    else:
        draw.circle((x,y),r,outline=FCOLOR,width=2)
        

def draw_stars_with_line(draw,lstars,xc,yc,rr,
                         small=False,color_f=True):
    ls=1
    for star in lstars:
        x,y =draw_star(draw, star,xc,yc,rr,
                       small=small,color_f=color_f)
        if ls==1:
            ls=0
            x0=x
            y0=y
        else:
            draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2) 
            x0=x
            y0=y
    # draw stars over again
    for star in lstars:
        x,y =draw_star(draw, star,xc,yc,rr,
                       small=small,color_f=color_f)
 
def draw_cst(draw, cst,xc,yc,rr,small=False,color_f=True):
    for lstars in starsln[cst]:
        ls=1
        for star in lstars:
            x,y =draw_star(draw, star,xc,yc,rr,
                           small=small,color_f=color_f)
            if ls==1:
                ls=0
                x0=x
                y0=y
            else:
                if g_share.f_south:
                    if cst !='UMi':  # in south hemisphere, ignore UMi lines which locate in south pole
                        draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2)  
                else:
                    if cst !='Oct':  # in north hemisphere, ignore Oct lines which locate in south pole
                        draw.line([(x0,y0),(x,y)],fill=(60,60,60,255),width=2)
                x0=x
                y0=y
    # draw stars over again
    for lstars in starsln[cst]:
        for star in lstars:
            x,y =draw_star(draw, star,xc,yc,rr,
                           small=small,color_f=color_f)
                           
    
def draw_fix_stars(draw,xc,yc,rr,small=False,color_f=True):
    g_share.stars_plotted=[]

    # plot stars and lines in constellations                
    for cst in CSTS:
        draw_cst(draw, cst,xc,yc,rr,small=small,color_f=color_f)
    
    # plot stars not in cst lines
    stars = list(starsi.keys())
    for star in stars:
        if star not in g_share.stars_plotted:
            draw_star(draw, star,xc,yc,rr,small=small,color_f=color_f)
            
            
def get_star_from_ra_dec(ra, dec):
    """Find constellation and closest star from RA and DEC coordinates.
    
    Args:
        ra: Right ascension in degrees
        dec: Declination in degrees
        
    Returns:
        tuple: (constellation, star_name, distance)
               where constellation is the Chinese constellation name
               star_name combines bayer_name and chinese_name if available
               distance is the angular distance in degrees
    """
    # Import star catalog functions
    from read_star_list import parse_star_list, find_star_by_hr
    
    # Find closest star in our catalog
    min_dist = float('inf')
    closest_star_info = None
    
    # Parse star list data
    stars = parse_star_list(config.star_list_path)
            
    for star_hr in stars:
        star_ra, star_dec, _,_ = starsi[star_hr]
        dist = ((ra - star_ra)**2 + (dec - star_dec)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest_star_info = find_star_by_hr(stars, star_hr)
        
        
    if closest_star_info:
        # Build star name combining bayer_name and chinese_name
        bayer_name = closest_star_info['bayer_name']
        magnitude = closest_star_info['magnitude']
        distance_ly = closest_star_info['distance_ly']
        spectrum = closest_star_info['spectrum']
        chinese_name=''
        if closest_star_info['chinese_name']:
            #star_name += f" ({closest_star_info['chinese_name']})"
            chinese_name= closest_star_info['chinese_name']
        print('closest star: %s' % bayer_name)
        return (closest_star_info['constellation'], bayer_name,chinese_name, min_dist, closest_star_info['hr_id'], magnitude, spectrum, distance_ly)
    print('closest star info:None')
    
    return (None, None, None, min_dist,None)


def get_star_from_hr_id(hr_id):
    """Find constellation and closest star from HR id.
    
    Args:
        HR id
        
    Returns:
        tuple: (constellation, star_name, distance)
               where constellation is the Chinese constellation name
               star_name combines bayer_name and chinese_name if available
               distance is the angular distance in degrees
    """
    # Import star catalog functions
    from read_star_list import parse_star_list, find_star_by_hr
    
    # Parse star list data
    stars = parse_star_list(config.star_list_path)
            
    star_info = stars.get(hr_id,None)
    
    if star_info:
        bayer_name = star_info['bayer_name']
        magnitude = star_info['magnitude']
        distance_ly = star_info['distance_ly']
        spectrum = star_info['spectrum']
        chinese_name=''
        if star_info['chinese_name']:
            chinese_name= star_info['chinese_name']
        print('star: %s' % bayer_name)
        return (star_info['constellation'], bayer_name,chinese_name, star_info['hr_id'], magnitude, spectrum, distance_ly)
    print('star info:None')
    
    return None


