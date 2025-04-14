from config import config
from g_share import g_share
from cstbnd import cstbnd
from ut_cal import *

def cstbnd_to_xyplot(cst,xc,yc,rr):
    if g_share.f_south:
        if cst=='UMi' or cst=='Dra' or cst=='Cep' or cst=='Cam':
            return []
    else:
        if cst=='Oct' or cst=='Hyi' or cst=='Men' or cst=='Cha' or cst=='Aps':
            return []
    cstbnddata = cstbnd[cst]
    s=1
    dec0=-1000
    ra0=-1000
    xys=[]
    for ra,dec in cstbnddata:
        #print('ra:%d dec:%d' % (ra,dec))
        while abs(dec0 - dec)<2:
            decx=dec0
            if dec0 != dec:
                decx=int((dec0 + dec)/2)

            
            loop=True
            #print('ra0:', ra0)
            if (ra - ra0)>1:
                ra0 = ra0+1
            elif (ra0 - ra)>1:
                ra0 = ra0-1
            else:
                ra0=ra
                loop=False
            x,y =ra_dec_to_xyplot(ra0, decx, xc, yc,rr)
            
            if s==1:
                s=0
                x0=x
                y0=y
                xys.append({'x':x, 'y':y})
            else:
                #draw.line([(x0,y0),(x,y)], fill=config.BND_COLOR,width=2)
                x0=x
                y0=y
                xys.append({'x':x, 'y':y})

            if not loop:
                break
            continue

        x,y =ra_dec_to_xyplot(ra, dec, xc, yc,rr)
        if s==1:
            s=0
            x0=x
            y0=y
            xys.append({'x':x, 'y':y})
        else:
            #draw.line([(x0,y0),(x,y)], fill=config.BND_COLOR,width=2)
            x0=x
            y0=y
            xys.append({'x':x, 'y':y})
        dec0=dec
        ra0=ra
    return xys