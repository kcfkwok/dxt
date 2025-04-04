from def_font import *
from paper import *
from word_list import *
from sym_arrow import draw_arrow

def table_jieqi_to_zod_and_zhemonth(paper, x,y, sun_lon=None,
    font=unicode_font_48, header_f=True):
    layer_table = paper.add_layer(name='table')
    im=layer_table.im
    draw=layer_table.draw
    
    yofs = int(4*MM_UNIT)
    yjq_ofs = int(4*MM_UNIT)
    ysign_ofs=int(8*MM_UNIT)
    yzhe_ofs = int(12*MM_UNIT)
    xofs=int(6*MM_UNIT)
    x1mm = MM_UNIT

    i=0

    zhe_st=4
    xx=x
    yy=y
    ecl_ang=0
    
    if header_f:
        X_FIELD = int(13*MM_UNIT)
        headers=['太阳视黄经','24 節氣','黃道12星宮','農曆月地支']
        for header in headers:
            draw.text((xx,yy),header,font=font,fill=BLACK)
            draw.rectangle((xx-x1mm,yy-x1mm,xx-x1mm+X_FIELD, yy-x1mm+yofs),
                       outline=BLACK, width=2)
            yy+=yofs
        
        yy=y
    
        x= x+X_FIELD
        xx=x
    
    for jq in JIE_QIS:
        draw.text((xx,yy),'%s°' % ecl_ang, font=font,fill=BLACK)
        ecl_ang += 15
        jqcolor = COLOR_JIEQI[jq]
        draw.rectangle((xx-x1mm,yy+yjq_ofs-x1mm,
                        xx-x1mm+xofs,yy+yjq_ofs-x1mm+yofs),fill=jqcolor)
        draw.text((xx,yy+yjq_ofs),jq, font=unicode_font_48,fill=BLACK)

        si,sr = divmod(i,2)
        if sr==0:
            sx = SIGNS[si]
            draw.text((xx,yy+ysign_ofs),sx, font=unicode_font_48,fill=BLACK)
        else:
            zi = (si+zhe_st ) % 12
            zx = ZHE[zi]
            draw.text((xx,yy+yzhe_ofs),zx, font=unicode_font_48,fill=BLACK)
        
        xx+=xofs
        i+=1
         
    xx=x
    yy=y
    
    L= 40 
    iangle0=0
    iangle=180
    if sun_lon is not None:
        jqlen = xofs*24
        jqpx = int(sun_lon/360.0 * jqlen)
        ax0=int(xx-x1mm)
        ax1=int(xx+jqlen-x1mm)
        axx=int(xx+jqpx-x1mm)
        ayy=int(yy-x1mm)
        ayy1=int(yy+yofs*4-x1mm)
        print('sun_lon:%s jqpx:%s axx:%s' % (sun_lon,jqpx,axx))
        #draw.line([(xx-x1mm,yy-x1mm*2),(xx+jqpx-x1mm, yy-x1mm*2)],
        #          fill=RED,width=2)
        
        draw_arrow(im,axx,ayy,L,iangle,RED, ar_width=40)
        draw_arrow(im,axx,ayy1,L,iangle0,RED, ar_width=40)
        draw.line([(axx,ayy),(axx,ayy1)],fill=RED,width=1)

    for i in range(5):
        draw.line([(xx-x1mm,yy-x1mm),(xx+xofs*24-x1mm, yy-x1mm)],fill=BLACK,width=2)
        yy+= yofs
    xx=x
    yy=y
    draw.line([(xx-x1mm,yy-x1mm),(xx-x1mm, yy+yofs*4-x1mm)],fill=BLACK,width=2)
    for i in range(25):
        draw.line([(xx-x1mm,yy-x1mm),(xx-x1mm, yy+yofs*2-x1mm)],fill=BLACK,width=2)
        si,sr = divmod(i,2)
        if sr==0:
            draw.line([(xx-x1mm,yy+yofs*2-x1mm),(xx-x1mm, yy+yofs*3-x1mm)],
                      fill=BLACK,width=2)
        else:
            pass
            draw.line([(xx-x1mm,yy+yofs*3-x1mm),(xx-x1mm, yy+yofs*4-x1mm)],
                      fill=BLACK,width=2)
            
        xx+= xofs
    xx-=xofs
    draw.line([(xx-x1mm,yy-x1mm),(xx-x1mm, yy+yofs*4-x1mm)],fill=BLACK,width=2)