import sys
# 将子模块的路径添加到 Python 的模块搜索路径中


from def_font import *
from paper import *
from ut_cal import *
from word_list import *
from lunar_python import Lunar
import datetime

RA_START=18  # hour :18 
RA_TOTAL= 24+4
ECL_START=18   #*15
ECL_TOTAL=47   #*15
XM_TITLE = int(5*MM_UNIT)
Y_MM = int(2.5*MM_UNIT)
RA_MM = int(9.5*MM_UNIT)  #int(9*MM_UNIT)
MM = int(1*MM_UNIT)
YM_SHORT = int(0.5*MM_UNIT) # short mark : 10 minutes, days
YM_LONG = int(1*MM_UNIT) # long mark : hour, day1,day11,day21
YM_MONTH = int(1.5*MM_UNIT) #  month line
YM_TEXT = int(0.5*MM_UNIT) # for hour text
ZHE_ST =4 # zhe month start with
WEEKDAYS ="一二三四五六日"

def RA_to_x(x0, ra_hr):
    x =int((ra_hr- RA_START) * RA_MM + x0)
    return x

def x_to_RA(x):
    ra =( (x - g_share.x0) / RA_MM ) + RA_START
    print('x_to_RA:', x, ra)
    return ra
    
def RA_to_xs(x0,xend, ra_hr):
    xs=[]
    while True:
        x = RA_to_x(x0,ra_hr)
        if x >xend:
            break
        if x >= x0 and x <=xend:
            xs.append(x)
        ra_hr+=24
    return xs
    
def init_linplot(x0,xr_end,y00,y01,y_equ):
    print('init_linplot')
    print('x0:',x0)
    print('xr_end:',xr_end)
    print('y00:', y00)
    print('y01:',y01)
    print('y_equ:', y_equ)
    
    g_share.x0=x0
    g_share.xr_end=xr_end
    g_share.y00=y00   # dec -90
    g_share.y01=y01   # dec +90
    g_share.ydec_m = (y01 - y00) / 180  # dec to y slop
    g_share.ydec_c = y00 + (y01 - y00) / 2 # dec to y-intercept (c)
    g_share.y_equ = y_equ

def dec_to_y(dec):
    # Calculate y based on dec
    y = g_share.ydec_m * dec + g_share.ydec_c
    return y

def y_to_dec(y):
    dec =(y - g_share.ydec_c) / g_share.ydec_m
    print('y_to_dec:', y,dec) 
    return dec

def ra_dec_to_xyslin(ra_deg,dec):
    y = dec_to_y(dec)
    xs=RA_to_xs(g_share.x0,g_share.xr_end, ra_deg)
    xys=[]
    for x in xs:
        xys.append((x,y))
    return xys