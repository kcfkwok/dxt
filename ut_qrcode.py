import qrcode

def add_qrcode(im, draw, x,y, url, box_size=10,border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=(0,0,0), back_color=(255,255,255))

    sw,sh =img.size
    im.paste(img,(x,y,x+sw,y+sh))

    #text = '更新星圖'
    #draw_title(draw,x+int(1*MM_UNIT),y-100,title)
