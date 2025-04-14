from config import config
from g_share import g_share
from cstbnd import cstbnd
from ut_cal import *

def plot_cstbnd(im, draw,xc,yc,rr):
    cstns = list(cstbnd.keys())
    cstns.sort()

    for cst in cstns:
        #print(cst)
        if g_share.f_south:
            if cst=='UMi' or cst=='Dra' or cst=='Cep' or cst=='Cam':
                continue
        else:
            if cst=='Oct' or cst=='Hyi' or cst=='Men' or cst=='Cha' or cst=='Aps':
                continue
        cstbnddata = cstbnd[cst]
        s=1
        dec0=-1000
        ra0=-1000
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
                else:
                    draw.line([(x0,y0),(x,y)], fill=config.BND_COLOR,width=2)
                    x0=x
                    y0=y
                if not loop:
                    break
                continue
            
            x,y =ra_dec_to_xyplot(ra, dec, xc, yc,rr)
            if s==1:
                s=0
                x0=x
                y0=y
            else:
                draw.line([(x0,y0),(x,y)], fill=config.BND_COLOR,width=2)
                x0=x
                y0=y
            dec0=dec
            ra0=ra

        skip="""
        # print name
        min_ra, max_ra, min_dec, max_dec, n_text_xofs, n_text_yofs, s_text_xofs,s_text_yofs = cstbm[cst]
        m_dec = int((min_dec + max_dec)/2)
        m_ra = int((min_ra+max_ra)/2)
        xt,yt =ra_dec_to_xyplot(m_ra, m_dec, xc, yc,rr,f_south=f_south)
        if f_south:
            xt = xt + s_text_xofs
            yt = yt + s_text_yofs
        else:
            xt = xt + n_text_xofs
            yt = yt + n_text_yofs
        """

        
