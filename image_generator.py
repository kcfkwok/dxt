from PIL import Image
from io import BytesIO
import datetime
import pytz
import time
from functools import lru_cache

# Cache for banner image to avoid repeated disk reads
_banner_cache = None

def get_banner():
    global _banner_cache
    if _banner_cache is None:
        banner_path = config.fpng_banner
        _banner_cache = Image.open(banner_path)
    return _banner_cache
from dxt_rl import *
from dxt_kz_A5R import make_dxt_kz_A5R
from dxt_xt import make_dxt_xt_A4
from dxt_zp import build_dxt_zp_A4L
from config import config
from g_share import g_share
from table_plnt_info import table_plnt_info
import re

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

def dxt_rl_img(content=None):
    start_time = time.time()
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
        tz = pytz.timezone(timezone)
        utc_now = datetime.datetime.utcnow()
        now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        year = now.year
        month = now.month
        day = now.day

    config.debug = False
    try:
        paper = make_dxt_rl_A4(year, month, day)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner = get_banner()
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
        img = paper.im
        duration = int((time.time() - start_time) * 1000)  # Convert to ms
        try:
            import requests
            requests.post('http://localhost:5000/perf', json={
                'type': 'dxt_rl_img',
                'duration': duration,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }, timeout=0.1)  # Non-blocking with short timeout
        except:
            pass  # Don't fail if metrics can't be sent
        return img
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該年份資料暫未支持</h1></body></html>'
        return render_template_string(error_html)
        

def dxt_kz_img(content):
    start_time = time.time()
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
    
    config.debug = False
    dt = datetime_w_timezone(year,month,day,hour,minute,0,timezone)
    g_share.hor_cir_opacity=128
    paper = make_dxt_kz_A5R(dt, latv, longv, location, timezone)
    x = config.banner_x
    y = config.banner_y
    layer = paper.add_layer(name='banner')
    banner = get_banner()
    layer.im.paste(banner, (x,y))
    paper.commit_image()
    img = paper.im
    duration = int((time.time() - start_time) * 1000)  # Convert to ms
    try:
        import requests
        requests.post('http://localhost:5000/perf', json={
            'type': 'dxt_kz_img', 
            'duration': duration,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }, timeout=0.1)  # Non-blocking with short timeout
    except:
        pass  # Don't fail if metrics can't be sent
    return img
    
def dxt_kz_img_wu(user_info):
    start_time = time.time()
    config.debug = False
    latv = user_info[0]
    longv = user_info[1]
    place = user_info[2]
    timezone = user_info[3]
    if timezone is None:
        latv = 22.5
        longv = 114.5
        place = '香港'
        timezone = 'Asia/Hong_Kong'
    hktz = pytz.timezone(timezone)
    utc_now = datetime.datetime.utcnow()
    now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
    g_share.hor_cir_opacity=128
    paper = make_dxt_kz_A5R(now, latv, longv, place, timezone)
    x = config.banner_x
    y = config.banner_y
    layer = paper.add_layer(name='banner')
    banner = get_banner()
    layer.im.paste(banner, (x,y))
    paper.commit_image()
    img = paper.im
    duration = int((time.time() - start_time) * 1000)  # Convert to ms
    try:
        import requests
        requests.post('http://localhost:5000/perf', json={
            'type': 'dxt_kz_img_wu',
            'duration': duration,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }, timeout=0.1)  # Non-blocking with short timeout
    except:
        pass  # Don't fail if metrics can't be sent
    return img
   

def dxt_xt_img(content):
    start_time = time.time()
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
    
    config.debug = False
    try:
        paper = make_dxt_xt_A4(year)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner = get_banner()
        layer.im.paste(banner, (x,y))
        paper.commit_image()
        img = paper.im
        duration = int((time.time() - start_time) * 1000)  # Convert to ms
        try:
            import requests
            requests.post('http://localhost:5000/perf', json={
                'type': 'dxt_xt_img',
                'duration': duration,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }, timeout=0.1)  # Non-blocking with short timeout
        except:
            pass  # Don't fail if metrics can't be sent
        return img
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該年份資料暫未支持</h1></body></html>'
        return render_template_string(error_html)
        
def dxt_zp_img(content=None):
    start_time = time.time()
    location = None
    if content is not None:
        m = re_zp.match(content)
        lats,_,longs,_,location,timezone = m.groups()
        latv = float(lats)
        longv = float(longs)

    if location is None:
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html)
        
    config.debug = False
    try:
        g_share.hor_cir_opacity = 255
        paper =build_dxt_zp_A4L(latv,longv,location, timezone)
        x = config.banner_x
        y = config.banner_y
        layer = paper.add_layer(name='banner')
        banner = get_banner()
        layer.im.paste(banner, (x,y))
        paper.commit_image()
        img = paper.im
        duration = int((time.time() - start_time) * 1000)  # Convert to ms
        try:
            import requests
            requests.post('http://localhost:5000/perf', json={
                'type': 'dxt_zp_img',
                'duration': duration,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }, timeout=0.1)  # Non-blocking with short timeout
        except:
            pass  # Don't fail if metrics can't be sent
        return img
    except FileNotFoundError:
        # 返回一个提示信息的 HTML 页面
        error_html = '<html><body><h1>該location暫未支持</h1></body></html>'
        return render_template_string(error_html)
