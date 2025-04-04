from def_font import *
from ut_cal import *
from def_plnt import *
from paper import *
from sky_plnt import *
import datetime
from g_share import g_share

class PLNT_REC:
    def __init__(self,k):
        self.k = k
        
    def set_rec(self):
        k = self.k
        res =xyzr_sun[3]
        self.lon = pLong[k]
        self.lat = pLat[k]
        self.ra, self.dec = radc(self.lon, self.lat)
        if k >= 2:
            self.sp = sp[k]  # dist from sun
            self.ep = ep[k]  # dist from earth
            self.ph = 100*((sp[k]+ep[k])**2\
                     - res**2)/(4*sp[k]*ep[k])  # phase
            self.x = xpln[k]
            self.y = ypln[k]
            self.z = zpln[k]
            
class PLNT_INFOS:
    def __init__(self,dt_w_tz):
        self.dt = dt_w_tz
        self.year=dt_w_tz.year
        self.tz, self.tzn = timezone_from_datetime(dt_w_tz)
        nd = cal_d_w_hm(self.year,1,1,-self.tzn,0)
        self.start_dict={}
        self.end_dict={}
        
    def start_plnt_info(self,k):
        plnt_rec = PLNT_REC(k)
        plnt_rec.set_rec()
        self.start_dict[k] = plnt_rec
        if k==K_SUN:
            g_share.sun_lon = plnt_rec.lon
            
    def end_plnt_info(self,k):
        plnt_rec = PLNT_REC(k)
        plnt_rec.set_rec()
        self.end_dict[k] = plnt_rec
        
    def run(self):
        dt = self.dt
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        timezone, hr_ofs = timezone_from_datetime(dt) 
        hour = hour - hr_ofs
        PlntPos(day,month,year,hour,minute)
        for k in K_PLANETS:
            self.start_plnt_info(k)
            
        dt = self.dt + datetime.timedelta(days=1)
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minute = dt.minute
        timezone, hr_ofs = timezone_from_datetime(dt) 
        hour = hour - hr_ofs
        PlntPos(day,month,year,hour,minute)
        for k in K_PLANETS:
            self.end_plnt_info(k)
            
def table_plnt_info(paper,x,y,year,month,day,hour,minute,timezone,font=unicode_font_48):
    dt = datetime_w_timezone(year,month,day,hour,minute,0,timezone)
    plnt_infos=PLNT_INFOS(dt)
    plnt_infos.run()
    #plnt_infos.dump()
    
    layer_table = paper.add_layer(name='table')
    im=layer_table.im
    draw=layer_table.draw
    
    yofs = int(6*MM_UNIT)
    yofs2 = int(3.8 *MM_UNIT)
    myofs= int(2*MM_UNIT)
    yjq_ofs = int(4*MM_UNIT)
    ysign_ofs=int(8*MM_UNIT)
    yzhe_ofs = int(12*MM_UNIT)
    xofs=int(13*MM_UNIT)
    x1mm = MM_UNIT
    
    xx = x
    yy = y
    
    
    yy+=yofs
    for item,header in [('ra','赤經'),('dec','赤緯'),('lon','黃經'),('lat','黃緯'),
                        ('ep','與地球距離'),('sp','與太陽距離'),
                        ('ph','被照亮部分')]:
        draw.text((xx,yy,),'%s' % header, font=font, fill=BLACK)
        if item=='ra' or item=='dec':
            yy+=yofs
        else:
            yy+=yofs2
            
    xx=x #+ xofs
    yy=y
    for k in K_PLANETS:
        #name = K_PLNT_NAMES[k]
        name = K_PLNT_LCNAMES[k]
        kcolor = SYM_COLORS[k]
        plntk= plnt_infos.start_dict[k]
        plntk2 = plnt_infos.end_dict[k]
        rax = '%dh%02dm%02ds' % deg_to_hms(plntk.ra)
        rax = f'{rax:>10}'
        rax2 = '%dh%02dm%02ds' % deg_to_hms(plntk2.ra)
        
        decx = '%d°%02d\'%02d"' % dms(plntk.dec)
        decx2 = '%d°%02d\'%02d"' % dms(plntk2.dec)
        
        lonx = '%d°%02d\'%02d"' % dms(plntk.lon)
        latx = '%d°%02d\'%02d"' % dms(plntk.lat)
        print('%s %s 黃經:%s 黃緯:%s 赤經:%s(%s) 赤緯:%s(%s)' % (k,name,lonx,latx,
                                             rax,rax2,decx,decx2))
       
        dv =((plntk2.ra - plntk.ra)/15.0) *60*60
        if abs(dv) >= 100.0:
            d_ra ='%+ds' % int(dv)
        else:
            d_ra ='%+.1fs' % dv
        d_ra = f'{d_ra:>10}'
        print('d_ra:%s' % d_ra)
        
        dv =(plntk2.dec - plntk.dec) *60*60
        if abs(dv) >= 100.0:
            d_dec ='%+d"' % int(dv)
        else:
            d_dec ='%+.1f"' % dv
        d_dec = f'{d_dec:>10}'
        print('d_dec:%s' % d_dec)
         
        if k >= 2:
            ep = '%3.2f AU' % plntk.ep
            sp = '%3.2f AU' % plntk.sp
            ph = '%3.2f %%' % plntk.ph
        else:
            ep=''
            sp=''
            ph=''
            
        xx +=xofs
        yy= y
        draw.rectangle((xx-x1mm,yy-x1mm,xx+xofs-x1mm,yy+yofs-x1mm), fill= kcolor)
        draw.text((xx,yy), '%s' % name, font=font,fill=BLACK)
        yy=y+yofs
        for item,text,dtext in [('ra',rax,d_ra),('dec',decx,d_dec),
                                ('lon',lonx,''),('lat',latx,''),
                           ('ep',ep,''),('sp',sp,''),('ph',ph,'')]:
            draw.text((xx,yy), text, font=font,fill=BLACK)
            if item=='ra' or item=='dec':
                draw.text((xx,yy+myofs), dtext, font=font,fill=BLACK)
                yy+=yofs
            else:
                yy+=yofs2

    # draw table hlines
    xx=x
    yy=y
    xx_end= xx+xofs*10
    for i in range(3):
        draw.line([(xx-x1mm,yy-x1mm),(xx_end-x1mm,yy-x1mm)], fill=BLACK,width=2)
        yy+= yofs    
    for i in range(6):
        draw.line([(xx-x1mm,yy-x1mm),(xx_end-x1mm,yy-x1mm)], fill=BLACK,width=2)
        yy+= yofs2    

    # draw table vlines
    xx=x
    yy=y
    yy_end = yy + yofs*3 + yofs2*5
    for i in range(11):
        draw.line([(xx-x1mm,yy-x1mm),(xx-x1mm,yy_end-x1mm)], fill=BLACK,width=2)
        xx+=xofs
		