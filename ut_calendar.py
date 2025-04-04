from paper import *
from def_font import *
import datetime
from lunar_python import Lunar
from ut_gan_zhe import calculate_gan_zhe


class CALENDAR:
    WEEKDAYS ="一二三四五六日"
    def __init__(self,year,month,day,hour=0, minute=0):
        self.ld = Lunar.fromDate(datetime.datetime(year, month, day))
        #gz_year=ld.getYearInGanZhi()
        #sx_year=ld.getYearShengXiao()
        self.dt = datetime.datetime(year,month,day,hour,minute,0,0)
        
    def weekday(self):
        wd = self.dt.weekday()
        cwd ='星期%s' % self.WEEKDAYS[wd] 
        return wd, cwd
        
    def year(self):
        year = self.dt.year
        cyear = '%d年' % year
        gz_year=self.ld.getYearInGanZhi()
        sx_year=self.ld.getYearShengXiao()
        lyear ='农历%s%s年' % (gz_year, sx_year)
        return year,cyear,lyear
    
    def month(self):
        month = self.dt.month
        cmonth = '%d月' % month
        cn_mon= self.ld.getMonthInChinese()
        lmonth = '%s月' % cn_mon
        gz_mon = '%s月' % self.ld.getMonthInGanZhi()
        dprint('gz_mon:%s' % gz_mon)
        return month,cmonth,lmonth, gz_mon
    
    def day(self):
        day = self.dt.day
        cday = '%d日' % day
        cn_day = self.ld.getDayInChinese()
        lday = '%s日' % cn_day
        gz_day ='%s日' % self.ld.getDayInGanZhi()
        return day, cday, lday,gz_day
    
    def _hour(self):
        hour = self.dt.hour
        chour = '%s时' % hour
        gz_hr = '%s时' % self.ld.getTimeInGanZhi()
        return hour, chour, gz_hr
    
    def hour(self):
        hour = self.dt.hour
        chour = '%s时' % hour 
        gz_hr0 = self.ld.getTimeInGanZhi()
        gz_hr_g, gz_hr_z = calculate_gan_zhe(gz_hr0[0], gz_hr0[1],hour)
        gz_hr ='%s时' %  (gz_hr_g + gz_hr_z)
        
        #y+=100
        #draw.text((x,y), text='%s时' % (gz_hr, ), font=unicode_font_80,fill=(0,0,0)\)
        return hour,chour,gz_hr
    
    
    def minute(self):
        minute = self.dt.minute
        cminute = '%s分' % minute
        return minute,cminute
