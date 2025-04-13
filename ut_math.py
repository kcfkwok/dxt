import math
pi = math.pi

def degs(x):
    return x* 180.0/math.pi

def rads(x):
    return x*math.pi/180.0

def rev(x):
    return x - (x//360)*360

def sqrt(x):
    return (math.sqrt(x))

def sn(x):
    return math.sin(math.radians(x))

def cs(x):
    return math.cos(math.radians(x))

def tn(x):
    return math.tan(math.radians(x))

def asn(x):
    return math.degrees(math.asin(x))

def acs(x):
    return math.degrees(math.acos(x))
    #return math.degrees(numpy.arccos(x))   # prepare trigger math domain error e.g x =1.002


def atn(x):
    return math.degrees(math.atan(x))

def atn2(y,x):
    return math.degrees(math.atan2(y,x))

def r_cs(deg):
    from g_share import g_share
    if g_share.f_south:
        return -cs(deg)
    return cs(deg)
