

def xyzr_sun_to_hxy_earth(x_sun,y_sun,hxc_b,hyc,s_au_r):
    #x_sun = xyzr_sun[0]
    #y_sun = xyzr_sun[1]
    hx = hxc_b + y_sun * s_au_r
    hy = hyc + x_sun * s_au_r
    return int(hx),int(hy)


def xy_to_hxy_r(x,y, hxc_b,hyc,s_au_r):
    hx = hxc_b - y * s_au_r
    hy = hyc - x * s_au_r
    return int(hx),int(hy)
    

def xy_to_hxy_l(x, y,hxc_a, hyc, s_au_l):
    hx = hxc_a - y * s_au_l
    hy = hyc - x * s_au_l
    return int(hx),int(hy)

