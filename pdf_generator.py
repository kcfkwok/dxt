# pdf_generator.py
import os
from fpdf import FPDF
from io import BytesIO
import pytz
import datetime
from dxt_rl import *
from dxt_xt import make_dxt_xt_A4
from dxt_zp import build_dxt_zp_A4L, build_dxt_zp_A5
from dxt_kz_A4L import make_dxt_kz_A4L
from config import config
from g_share import g_share
from table_plnt_info import table_plnt_info
import re
from events import EVENTS, show_events
from ut_qrcode import add_qrcode
from def_font import *


r_rl = r'rl-(\d+)-(\d+)-(\d+)'
re_rl = re.compile(r_rl)

r_xt = r'xt-(\d+)'
re_xt = re.compile(r_xt)

r_zp = r'zp_(-?\d+(\.\d+)?);(-?\d+(\.\d+)?);([^;]+);(.*)'
re_zp = re.compile(r_zp)

r_kz0= r'kz_(-?\d+(\.\d+)?);(-?\d+(\.\d+)?);([^;]+);(.*)'
re_kz0 = re.compile(r_kz0)

r_kz1= r'kz_(-?\d+(\.\d+)?);(-?\d+(\.\d+)?);([^;]+);(.*);(\d+)-(\d+)-(\d+);(\d+)-(\d+)'
re_kz1 = re.compile(r_kz1)

from flask import render_template_string
import os

def dxt_rl_pdf(content):
    year = 0
    timezone = 'Asia/Hong_Kong'
    if content is not None:
        m = re_rl.match(content)
        if m:
            year, month, day = m.groups()
            year = int(year)
            month = int(month)
            day = int(day)

    if year == 0:
        hktz = pytz.timezone(timezone)
        utc_now = datetime.datetime.utcnow()
        now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
        year = now.year
        month = now.month
        day = now.day

    fn = 'dxt_rl_%s_%02d_%02d_A4.pdf' % (year, month, day)
    config.debug = False
    try:
        paper = make_dxt_rl_A4(year, month, day)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x,y))
        
        hour=0
        minute=0
    
        x=int(150*MM_UNIT)
        y=int(167*MM_UNIT)
        table_plnt_info(paper,x,y,year,month,day,hour,minute,timezone)
    
        sun_lon = g_share.sun_lon
        x=int(130 *MM_UNIT)
        y=int(145* MM_UNIT)
        table_jieqi_to_zod_and_zhemonth(paper, x,y,sun_lon=sun_lon)
    
        paper.commit_image()
        image = paper.im

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image.size
        # 使用绝对路径保存临时图像
        temp_image_path = os.path.abspath('temp_image.png')
        image.save(temp_image_path)

        img_width, img_height = image.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        pdf.image(temp_image_path, x=x, y=y, w=new_width, h=new_height)

        # 删除临时图像
        pdf_content = pdf.output(dest='S')
        os.remove(temp_image_path)
        return pdf_content, fn
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該年份資料暫未支持</h1></body></html>'
        return render_template_string(error_html), None
        
    
def dxt_xt_pdf(content):
    year = 0
    if content is not None:
        m = re_xt.match(content)
        year, = m.groups()
        year = int(year)

    if year == 0:
        timezone = 'Asia/Hong_Kong'
        hktz = pytz.timezone(timezone)
        utc_now = datetime.datetime.utcnow()
        now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
        year = now.year
        
    fn = 'dxt_xt_%s_A4.pdf' % (year,)
    config.debug = False
    try:
        paper = make_dxt_xt_A4(year)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x,y))
        paper.commit_image()
        image = paper.im

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image.size
        # 使用绝对路径保存临时图像
        temp_image_path = os.path.abspath('temp_image.png')
        image.save(temp_image_path)

        img_width, img_height = image.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        pdf.image(temp_image_path, x=x, y=y, w=new_width, h=new_height)

        # 删除临时图像
        pdf_content = pdf.output(dest='S')
        os.remove(temp_image_path)
        return pdf_content, fn
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該年份資料暫未支持</h1></body></html>'
        return render_template_string(error_html), None
        
def dxt_zp_pdf(content):
    location = None
    if content is not None:
        m = re_zp.match(content)
        lats,_,longs,_,location,timezone = m.groups()
        latv = float(lats)
        longv = float(longs)

    if location is None:
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html)
             
    fn = 'dxt_zp_%.2f_%.2f_%s_A4.pdf' % (latv, longv, location)
    config.debug = False
    
    try:
        g_share.hor_cir_opacity = 255
        # build A4L
        paper = build_dxt_zp_A4L(latv,longv,location,timezone)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x,y))
        paper.commit_image()
        image = paper.im

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image.size
        # 使用绝对路径保存临时图像
        temp_image_path = os.path.abspath('temp_image.png')
        image.save(temp_image_path)

        img_width, img_height = image.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        pdf.image(temp_image_path, x=x, y=y, w=new_width, h=new_height)

        # page 2: A5 face north
        g_share.set_f_south(False)
        paper2 = build_dxt_zp_A5(latv,longv,location,timezone)
        x = config.banner_x
        y = config.banner_y
        layer = paper2.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x,y))
        paper2.commit_image()
        image2 = paper2.im
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image2.size
        # 使用绝对路径保存临时图像
        temp2_image_path = os.path.abspath('temp2_image.png')
        image2.save(temp2_image_path)

        img_width, img_height = image2.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp2_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        #pdf.image(temp2_image_path, x=x, y=y, w=new_width, h=new_height)
        pdf.image(temp2_image_path, x=0, y=0, w=new_width, h=new_height)


        # page 3: A5 face south
        g_share.set_f_south(True)
        paper3 = build_dxt_zp_A5(latv,longv,location,timezone)
        x = config.banner_x
        y = config.banner_y
        layer = paper3.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x,y))
        paper3.commit_image()
        image3 = paper3.im
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image3.size
        # 使用绝对路径保存临时图像
        temp3_image_path = os.path.abspath('temp3_image.png')
        image3.save(temp3_image_path)

        img_width, img_height = image3.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp3_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        #pdf.image(temp2_image_path, x=x, y=y, w=new_width, h=new_height)
        pdf.image(temp3_image_path, x=0, y=0, w=new_width, h=new_height)


        # 删除临时图像
        pdf_content = pdf.output(dest='S')
        
        os.remove(temp_image_path)
        os.remove(temp2_image_path)
        os.remove(temp3_image_path)
        
        return pdf_content, fn
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html), None
        
def dxt_kz_pdf(content):
    location = None
    if content is not None:
        m1 = re_kz1.match(content)
        if m1 is None:
            m0 = re_kz0.match(content)
            if m0 is None:
                error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
                return render_template_string(error_html)
                
    if m1 is not None:
        lats,_,longs,_,location,timezone,year,month,day,hour,minute = m1.groups()
    else:
        lats,_,longs,_,location,timezone = m0.groups()
        year=0
    skip="""
    location = None
    if content is not None:
        m = re_kz0.match(content)
        lats,_,longs,_,location,timezone = m.groups()
        latv = float(lats)
        longv = float(longs)
    """
    if location is None:
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html)
       
    latv = float(lats)
    longv = float(longs)
    year = int(year)
    if year ==0:
        tz = pytz.timezone(timezone)
        utc_now = datetime.datetime.utcnow()
        now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute  
        
    month=int(month)
    day = int(day)
    hour=int(hour)
    minute= int(minute)
    
    fn = 'dxt_kz_%.2f_%.2f_%s_%02d%02d%02dT%02d%02d_A4.pdf' % (latv, longv, location,
        year,month,day,hour,minute)
    config.debug = False
    
    try:
        #hktz = pytz.timezone(timezone)
        #utc_now = datetime.datetime.utcnow()
        #now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
        dt = datetime_w_timezone(year,month,day,hour,minute,0,timezone)
        g_share.hor_cir_opacity=128
        paper = make_dxt_kz_A4L(dt, latv, longv, location, timezone)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner_path=config.fpng_banner
        banner = Image.open(banner_path)
        layer.im.paste(banner, (x+ int(paper.w_px/2.0),y))
        
        events = EVENTS(year, month)
        evs = events.get_evs(day)
        #print('evs:', evs)
        show_events(layer.draw, evs,x=config.xc1+int(paper.w_px/2.0)+50)
    
        x= int(20* config.MM_UNIT)
        y= int(20* config.MM_UNIT)
        url = 'https://kcfkwok.pythonanywhere.com/'
        add_qrcode(layer.im, layer.draw, x,y, url, box_size=20)
        
        text = '記住這一刻'
        layer.draw.text((x+int(5*MM_UNIT),y-100),text,font=unicode_font_96,fill=BLACK)
    
        paper.commit_image()

        image = paper.im

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        page_width = pdf.w
        page_height = pdf.h
        w, h = image.size
        # 使用绝对路径保存临时图像
        temp_image_path = os.path.abspath('temp_image.png')
        image.save(temp_image_path)

        img_width, img_height = image.size
        width_scale = page_width / img_width
        height_scale = page_height / img_height
        scale = min(width_scale, height_scale)

        new_width = img_width * scale
        new_height = img_height * scale

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2
        # 打印调试信息
        print(f"Image path: {temp_image_path}")
        print(f"Image size: {img_width}x{img_height}")
        print(f"New size: {new_width}x{new_height}")
        print(f"Position: {x},{y}")

        pdf.image(temp_image_path, x=x, y=y, w=new_width, h=new_height)
        #pdf.image(temp_image_path, x=x*2, y=y*2, w=new_width, h=new_height)

        # 删除临时图像
        pdf_content = pdf.output(dest='S')
        
        os.remove(temp_image_path)
        
        return pdf_content, fn
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html), None
        
