from AstroModule import *
from plnt import *
from def_plnt import *
from ut_math import *
from g_share import g_share
import pytz
import datetime

def cal_lst(latv,longv,dt, timezone):
    import pytz
    from astropy.time import Time
    from astropy import units as u
    from astropy.coordinates import EarthLocation
    from datetime import datetime
    loc_tz = pytz.timezone(timezone)
    
    year=dt.year
    month=dt.month
    day = dt.day
    hour= dt.hour
    minute = dt.minute
    second = dt.second

    fmt_str="%s-%02d-%02d %02d:%02d:%02d" % (year,month,day,hour,minute,second)
    print('tz:%s datetime:%s' % (timezone, fmt_str))
    fmt = '%Y-%m-%d %H:%M:%S'
    dt = datetime.strptime(fmt_str, fmt)
    loc_dt = loc_tz.localize(dt)

    utc = pytz.utc
    observing_location = EarthLocation(lat=latv*u.deg, lon=longv*u.deg)
    observing_time = Time(loc_dt.astimezone(utc).strftime(fmt), scale='utc',
                          location=observing_location)

    lst = observing_time.sidereal_time('mean',longv)
    return lst.deg

def cal_d_w_hm(year,month,date,hour,mins):
    try:
        Obl=g_share.Obl
    except:
        from g_share import g_share
        
    du0 = caldays(date,month,year)
    deltaT = calDeltaT(date, month, year)
    deltaD = deltaT/86400
    d = du0 + deltaD \
        + hour/24.0 + mins/1440.0
    Obl,dpsi,GST = Obl_Nut_GST(d)
    Ayan = 23.853 + 3.82447045e-5*d
    g_share.Obl = Obl
    g_share.Ayan = Ayan
    g_share.deltaT = deltaT
    return d

class PLOC:  # planet location
    def __init__(self,x,y,ra=None,dec=None,r=None):
        self.x=x
        self.y=y
        self.ra = ra
        self.dec = dec
        self.r = r
        
    def set(self,x,y,ra=None,dec=None,r=None):
        self.x=x
        self.y=y
        if ra is not None:
            self.ra=ra
        if dec is not None:
            self.dec = dec
        if r is not None:
            self.r=r

def cal_planet_at(year,month,date,ihour,minute,tz):  
    nd = cal_d_w_hm(year,1,1,-tz,0)
    Obl = g_share.Obl
    hour = ihour - tz
    PlntPos(date,month,year,hour,minute)
    g_share.pln_0=[] 
    
    for k in range(10):
        ra, dec = radc(pLong[k],pLat[k])
        if k==0:
            g_share.sun_0=PLOC(xyzr_sun[0], xyzr_sun[1],ra,dec)
        r=sp[k]
        g_share.pln_0.append(PLOC(xpln[k],ypln[k], ra, dec, r))
        #print('plnt k:%s x:%s y:%s ' % (k,xpln[k], ypln[k]))
        
        
def cal_planet_info(year,month,date,ihour,minute,tz):  
    nd = cal_d_w_hm(year,1,1,-tz,0)
    Obl = g_share.Obl
    hour = ihour - tz
    PlntPos(date,month,year,hour,minute)
    g_share.pln_0=[] 
    g_share.sun_lon = pLong[K_SUN]
    
    for k in range(10):
        ra, dec = radc(pLong[k],pLat[k])
        if k==0:
            g_share.sun_0=PLOC(xyzr_sun[0], xyzr_sun[1],ra,dec)
        r=sp[k]
        g_share.pln_0.append(PLOC(xpln[k],ypln[k], ra, dec, r))
        
    
    PlntPos(date+1,month,year,hour,minute)
    g_share.pln_1 = []
    for k in range(10):
        ra, dec = radc(pLong[k],pLat[k])
        if k==0:
            g_share.sun_1 = PLOC( xyzr_sun[0], xyzr_sun[1],ra,dec)
        r = sp[k]
        g_share.pln_1.append(PLOC(xpln[k], ypln[k], ra, dec,r))
        
    
    PlntPos(date+10,month,year,hour,minute)
    g_share.pln_10 = []
    for k in range(10):
        ra, dec = radc(pLong[k],pLat[k])
        if k==0:
            g_share.sun_10 = PLOC( xyzr_sun[0], xyzr_sun[1],ra,dec)
        r =sp[k]
        g_share.pln_10.append(PLOC(xpln[k], ypln[k], ra, dec,r))
       
    
    PlntPos(date,month,year+2,hour,minute)
    g_share.sun_2yr = PLOC(xyzr_sun[0],xyzr_sun[1])
    g_share.pln_2yr = []
    for k in range(10):
        r = sp[k]
        g_share.pln_2yr.append(PLOC(xpln[k], ypln[k],r=r))


def days_to_date(days, year):
    from datetime import datetime
    day_num= '%s' % days
    year = '%s' % year
    day_num.rjust(3 + len(day_num), '0')
    # converting to date
    res = datetime.strptime(year + "-" + day_num, "%Y-%j").strftime("%m-%d-%Y")
    m,d,y = res.split('-')
    return (int(m),int(d),int(y))

def get_days_of_month(year,month):
    from datetime import datetime, timedelta, date
    next_month= month+1
    year_in_next_month= year
    if month ==12:
        next_month = 1
        year_in_next_month = year+1
    days = (date(year_in_next_month,next_month,1)- date(year,month,1)).days
    return days


def ra_dec_to_xyplot(ra, dec,xc,yc,rr,requ=None,f_s=None):
    try:
        ari_ang = config.ari_ang
    except:
        from config import config
        ari_ang = config.ari_ang

    if f_s is None:
        f_s = g_share.f_south
        
    if requ is None:
        r_90 = 180 / rr
        requ = int(r_90/2)
        
    angx = ari_ang + ra
    rd = dec / rr
    if f_s:
        r = requ + rd
    else:
        r = requ - rd
        
    sin_phi = sn(angx)
    cos_phi = r_cs(angx)
    x = int(cos_phi * r + xc)
    y = int(sin_phi * r + yc)
    #print('ra_dec_to_xyplot ra:%.2f dec:%.2f xc:%s yc:%s rr:%s f_south:%s x:%s y:%s' % 
    #(ra,dec,xc,yc,rr,f_s,x,y))
    return x,y


def equ_to_hor(H, Dec, lat): # H: Hr ang,
    sin_Dec = sin_deg(Dec)
    sin_lat = sin_deg(lat)
    cos_Dec = cos_deg(Dec)
    cos_lat = cos_deg(lat)
    cos_H = cos_deg(H)
    sin_alt =sin_Dec * sin_lat + cos_Dec * cos_lat * cos_H
    alt = asin_deg(sin_alt)
    cos_alt = cos_deg(alt)
    cos_azi = (sin_Dec - sin_lat * sin_alt) / (cos_lat * cos_alt)
    azi = acos_deg(cos_azi)
    sin_H = sin_deg(H)
    if sin_H > 0:
        azi = 360 - azi
    return azi, alt

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def date_to_days(year, month, day):
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(year):
        days_in_month[1] = 29
    total_days = 0
    for i in range(month - 1):
        total_days += days_in_month[i]
    total_days += day
    return total_days
    
def hms(hr):
    while hr >= 24.0:
        hr -=24.0
    while hr <0.0:
        hr +=24.0
    h=int(hr)
    m = (hr -h) * 60
    s = (m - int(m))* 60
    m = int(m)
    s = int(s+.5)
    return h,m,s

def dms(deg):
    while deg > 360.0:
        deg -=360.0
    d = int(deg)
    m = (deg -d) * 60
    s = (m - int(m))* 60
    m = int(m)
    s = int(s+.5)
    if d<0:
        m=-m
        s=-s
    return d,m,s

def deg_to_hms(deg):
    hr = deg/15
    return hms(hr)

def ra_dec_to_deg(ra_hms, dec_dms):
    # e.g ra_hms = '05h23m34.5s'
    # e.g dec = '-69d45m22s'
    from astropy import units as u
    from astropy.coordinates import SkyCoord
    # 创建SkyCoord对象
    coord = SkyCoord(ra=ra_hms, dec=dec_dms, frame='icrs')

    # 获取以度为单位的赤经
    ra_deg = coord.ra.degree
    dec_deg = coord.dec.degree
    print('ra_dec_to_deg %s %s -> %s %s' % (ra_hms,dec_dms, ra_deg,dec_deg))
    return ra_deg, dec_deg
    
def dms_to_deg(d,m,s):
    deg =((s/60.0) + m)/6.0 + d
    return deg
    
def datetime_w_timezone(year,month,day,hour,minute,second,timezone):
    # 创建时区对象
    tz = pytz.timezone(timezone)

    # 创建 datetime 对象，初始不设置时区
    dt = datetime.datetime(year, month, day, hour, minute)
    # 使用 localize 方法设置时区
    dt = tz.localize(dt)
    return dt

def timezone_from_datetime(dt):
    timezone = dt.tzinfo
    # 将时区字符串转换为数字
    utc_offset = dt.utcoffset()
    offset_hours=None
    if utc_offset is not None:
        offset_hours = utc_offset.total_seconds() // 3600
        #print(f"时区数字表示: {'+' if offset_hours >= 0 else ''}{int(offset_hours)}")
    #else:
    #    print("无法获取时区偏移量。")
    return timezone, offset_hours


if __name__=='__main__':
    year = 2025
    month=1
    day=1
    hour=0
    minute=0
    tz=8
    nd = cal_d_w_hm(year, month, day, hour- tz, minute)
    print('nd:',nd)
    date = days_to_date(100, 2025)
    print(date)
    nd = get_days_of_month(2025,2)
    print(nd)

if __name__=='__main__':
    import datetime
    import pytz
    latv=22.5
    longv=114.5
    timezone='Asia/Hong_Kong'
    loc_tz = pytz.timezone(timezone)
    utc_now = datetime.datetime.utcnow()
    # Convert the UTC time to the specified timezone
    dt = utc_now.replace(tzinfo=pytz.utc).astimezone(loc_tz)
    print(dt)
    lst= cal_lst(latv,longv,dt, timezone)
    print(lst)
    
    
def xyplot_to_ra_dec(x, y, xc, yc, rr, requ=None, f_s=None):
    try:
        ari_ang = config.ari_ang
    except:
        from config import config
        ari_ang = config.ari_ang
    
    if f_s is None:
        f_s = g_share.f_south
        
    if requ is None:
        r_90 = 180 / rr
        requ = int(r_90/2)
        
    # Normalize coordinates to be within valid range
    x = max(0, min(x, 2*xc))
    y = max(0, min(y, 2*yc))
        
    # Calculate radius from center
    dx = x - xc
    dy = y - yc
    r = math.sqrt(dx*dx + dy*dy)
    #print('r: %s requ:%s rr:%s r_90:%s' % (r, requ,rr,r_90))
    # Calculate angle
    ang = math.atan2(dy, dx) * 180/math.pi
    ra = (ang - ari_ang) % 360
    
    # Calculate declination
    if f_s:
        dec = (r - requ) * rr
    else:
        dec = (requ - r) * rr
        
    #print('xyplot_to_ra_dec x:%s y:%s f_south:%s ra:%s dec:%.2f' % (x, y, f_s, ra,dec))
    
    return ra, dec

    
if __name__=='__main__':
    #xyplot_to_ra_dec x:2109.4884724056355 y:1724.5474483661253 f_south:True ra:258.43024253693807 dec:-17.70
    x=2109
    y=1724
    f_s=True
    rr=0.155 
    xc=1500 
    yc=1500
    ra,dec =xyplot_to_ra_dec(x, y, xc, yc, rr, requ=None, f_s=f_s)
    print('ra:%s(%s) dec:%s' % (ra, ra/15.0, dec))
    x,y =ra_dec_to_xyplot(ra, dec,xc,yc,rr,requ=None,f_s=f_s)
    print('x:%s y:%s' % (x,y))
    
if __name__=='__main__':
    #xyplot_to_ra_dec x:2109.4884724056355 y:1724.5474483661253 f_south:True ra:258.43024253693807 dec:-17.70
    x=2109
    y=1724
    f_s=False
    rr=0.155 
    xc=1500 
    yc=1500
    ra,dec =xyplot_to_ra_dec(x, y, xc, yc, rr, requ=None, f_s=f_s)
    print('ra:%s(%s) dec:%s' % (ra, ra/15.0, dec))
    x,y =ra_dec_to_xyplot(ra, dec,xc,yc,rr,requ=None,f_s=f_s)
    print('x:%s y:%s' % (x,y))