import platform
import sys
# 将子模块的路径添加到 Python 的模块搜索路径中
if platform.system()=='Linux':
    sys.path.append('/home/kcfkwok/lin_dxt')
else:
    sys.path.append('../lin_dxt')

from flask import Flask, request, render_template, render_template_string, send_file, Response, redirect, session, jsonify
from csts import CSTS
from cstcn import cstcn
from read_star_list import parse_star_list, find_stars_in_constellation, find_star_by_hr
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
from secret_key import secret_key
from config import config
from g_share import g_share
from image_generator import dxt_rl_img, dxt_kz_img, dxt_kz_img_wu, dxt_xt_img, dxt_zp_img,re_xt, re_zp, re_kz0, re_kz1,re_rl
from pdf_generator import dxt_rl_pdf, dxt_xt_pdf, dxt_zp_pdf, dxt_kz_pdf
from default_info import default_info
from io import BytesIO
from timezonefinder import TimezoneFinder
import pytz
import datetime
from pathlib import Path
from lin_base import x_to_RA, y_to_dec

app = Flask(__name__)
app.secret_key = secret_key
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.dbpath}'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 Babel
babel = Babel(app)

# 配置 Babel
@babel.localeselector
def get_locale():
    lang = session.get('lang')
    if lang:
        return lang
    return request.accept_languages.best_match(['en', 'zh'])

# 将 get_locale 函数注册为上下文处理器
@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)


@app.route('/', methods=['GET', 'POST'])
def index():
    print('*** index.html')
    if request.method == 'POST':
        lang = request.form.get('lang')
        session['lang'] = lang
        return redirect('/')
    if 'location_info' in session:
        location_info = session['location_info']
        user_info = (location_info['latitude'], location_info['longitude'], location_info['location'], location_info['timezone'])
    elif default_info:
        user_info = default_info
    else:
        user_info = [22.0,114.0,'香港','Asia/Hong_Kong']
    location_text=user_info[2]
    content = request.args.get('content', None)
    if content is None:
        print('render index.html')
        return render_template('index.html',user_info=user_info, location_text=location_text)
    print('content:', content)
    m = re_rl.match(content)
    if m is not None:
        year, month, day = m.groups()
        print('dxt_rl %s-%s-%s' % (year,month,day))
        return render_template('dxt_rl.html', year=year, month=month, day=day)

    m = re_xt.match(content)
    if m is not None:
        year, = m.groups()
        print('dxt_xt %s' % year)
        return render_template('dxt_xt.html', year=year)

    return render_template('index.html', username=username, style=style, user_info=user_info, location_text=location_text)

@app.route('/perf', methods=['POST'])
def track_performance():
    data = request.get_json()
    perf_type = data.get('type')
    duration = data.get('duration')
    timestamp = data.get('timestamp')
    
    # Log performance metrics
    print(f'Performance: {perf_type} took {duration}ms at {timestamp}')
    
    # Here you could also:
    # - Store metrics in a database
    # - Calculate running averages
    # - Trigger alerts if performance degrades
    
    return jsonify({'status': 'success'})

@app.route('/calculate_sum', methods=['POST'])
def calculate_sum():
    data = request.get_json()
    x = float(data['x'])
    y = float(data['y'])
    return jsonify({'result': x + y})





@app.route('/clock')
def clock():
    if 'location_info' in session:
        location_info = session['location_info']
        user_info = (location_info['latitude'], location_info['longitude'], location_info['location'], location_info['timezone'])
    elif default_info:
        user_info = default_info
    else:
        user_info = [None, None, None, None]

    img = dxt_kz_img_wu(user_info)
    # Convert image to bytes
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/download', methods=['GET', 'POST'])
def download():
    content = request.args.get('content', '默认内容')
    print('download content:%s' % content)
    error_html = '<html><body><h1>資料暫未支持</h1></body></html>'
    result= render_template_string(error_html)
    fn=None
    if content[:2]=='rl':
        result, fn = dxt_rl_pdf(content)
    elif content[:2]=='xt':
        result, fn = dxt_xt_pdf(content)
    elif content[:2]=='zp':
        result, fn = dxt_zp_pdf(content)
    elif content[:2]=='kz':
        result, fn = dxt_kz_pdf(content)

    #if isinstance(result, str):  # 如果返回的是错误信息
    if fn is None:
        return result
    pdf_content = result
    if isinstance(pdf_content, str):
        pdf_content = pdf_content.encode('latin-1')  # 确保编码正确
    pdf_bytes = BytesIO()
    pdf_bytes.write(pdf_content)
    pdf_bytes.seek(0)
    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name=fn,
        mimetype='application/pdf'
    )

@app.route('/dxt_kz_img_rq')
def dxt_kz_img_rq():
    content = request.args.get('content', None)
    result = dxt_kz_img(content)
    if isinstance(result, str):  # 如果返回的是错误信息
        return result
    buf = BytesIO()
    result.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')


@app.route('/dxt_kz')
def dxt_kz():
    content = request.args.get('content', None)
    print('dxt_kz content:%s' % content)
    if content is None:
        return render_template('index.html')
    print('content:', content)
    # 这里可以添加对 content 格式的验证
    m1 = re_kz1.match(content)
    if m1 is None:
        m0 = re_kz0.match(content)
        if m0 is None:
            return render_template('index.html')

    if m1 is not None:
        lats,_,longs,_,location,timezone,year,month,day,hour,minute = m1.groups()
    else:
        lats,_,longs,_,location,timezone = m0.groups()
        year='0'
        month='0'
        day='0'
        hour='0'
        minute='0'

    latitude = '%.2f' % float(lats)
    longitude = '%.2f' % float(longs)

    if year=='0':
        hktz = pytz.timezone(timezone)
        utc_now = datetime.datetime.utcnow()
        now = utc_now.replace(tzinfo=pytz.utc).astimezone(hktz)
        year = '%s' % now.year
        if month=='0':
            month = '%s' % now.month
            day = '%s' % now.day
            hour = '%s' % now.hour
            minute = '%s' % now.minute
    print('lats:%s longs:%s loc:%s tz:%s %s-%s-%s %s:%s' % (lats,longs,location,timezone,
    year,month,day,hour,minute))
    # Create simplified config with only needed values
    template_config = {
        'xckz': config.xckz,
        'yckz': config.yckz,
        'r5': config.r5
    }
    return render_template('dxt_kz.html',
        latitude=latitude,
        longitude=longitude,
        location=location,
        timezone=timezone,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        config=template_config,
        csts=CSTS,
        cstcn=cstcn)


@app.route('/dxt_rl_img_rq', methods=['GET'])
def dxt_rl_img_rq():
    content = request.args.get('content', None)
    print('dxt_rl_img_rq content:%s' % content)
    result = dxt_rl_img(content)
    if isinstance(result, str):  # 如果返回的是错误信息
        return result
    buf = BytesIO()
    result.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/dxt_rl')
def dxt_rl():
    content = request.args.get('content', None)
    if content is None:
        return render_template('dxt_rl.html', year='0', month='0', day='0')
        #
    print('content:', content)
    m = re_rl.match(content)
    if m is None:
        return render_template('dxt_rl.html', year='0', month='0', day='0')
        #return render_template('index.html')
    year, month, day = m.groups()
    return render_template('dxt_rl.html', year=year, month=month, day=day)
    
@app.route('/xy_to_radec', methods=['POST'])
def xy_to_radec():
    data = request.get_json()
    x = float(data['x'])
    y = float(data['y'])
    
    from ut_star import get_star_from_ra_dec
    
    # Load appropriate star coordinates file
    fn = 'star_coords_south.txt' if g_share.f_south else 'star_coords_north.txt'
    filename = Path(config.staticpath, fn)
    print('xy_to_radec using:', filename)
    
    # Find closest star match
    min_dist = float('inf')
    ra, dec = 0, 0
    
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            star_x = float(parts[5])
            star_y = float(parts[6])
            dist = (x - star_x)**2 + (y - star_y)**2
            
            if dist < min_dist:
                min_dist = dist
                ra = float(parts[3])
                dec = float(parts[4])
    
    constellation, bayer_name,chinese_name, dist, hr_id, magnitude, spectrum, distance_ly = get_star_from_ra_dec(ra, dec)
    cst = bayer_name.split('/')[1]
    print('constellation:%s bayer_name:%s ra:%.2f dec:%.2f min_dist:%s' % (constellation,bayer_name,ra,dec,min_dist))
    if min_dist>100:
        bayer_name=None
        chinese_name=None
        magnitude=None
        spectrum=None
        distance_ly=None
        hr_id = None
        
    return jsonify({
        'ra': ra,
        'dec': dec,
        'constellation': constellation,
        'cst':cst,
        'bayer_name': bayer_name,
        'chinese_name': chinese_name,
        'distance': dist,
        'magnitude': magnitude,
        'spectrum': spectrum,
        'distance_ly': distance_ly,
        'hr_id': hr_id
    })

@app.route('/xy_to_lin_radec', methods=['POST'])
def xy_to_lin_radec():
    data = request.get_json()
    x = float(data['x'])
    y = float(data['y'])
    sx = data['x']
    sy = data['y']
    ra =(x_to_RA(x) * 15) % 360  # to degree
    dec = y_to_dec(y)
    print('xy_to_lin_radec x:%.2f y:%.2f ra:%.2f dec:%.2f' % (x,y,ra,dec))
    
    
    from ut_star import get_star_from_ra_dec
    skip="""
    # Load appropriate star coordinates file
    fn = 'star_coords_south.txt' if g_share.f_south else 'star_coords_north.txt'
    filename = Path(config.staticpath, fn)
    print('xy_to_radec using:', filename)
    
    # Find closest star match
    min_dist = float('inf')
    ra, dec = 0, 0
    
    with open(filename, 'r', encoding='utf-8') as f:
        next(f)  # Skip header
        for line in f:
            parts = line.strip().split('\t')
            star_x = float(parts[5])
            star_y = float(parts[6])
            dist = (x - star_x)**2 + (y - star_y)**2
            
            if dist < min_dist:
                min_dist = dist
                ra = float(parts[3])
                dec = float(parts[4])
    """
    
    constellation, bayer_name,chinese_name, dist, hr_id, magnitude, spectrum, distance_ly = get_star_from_ra_dec(ra, dec)
    cst = bayer_name.split('/')[1]
    print('constellation:%s bayer_name:%s ra:%.2f dec:%.2f dist:%s' % (constellation,bayer_name,ra,dec,dist))
    if dist>2:
        bayer_name=None
        chinese_name=None
        magnitude=None
        spectrum=None
        distance_ly=None
        hr_id = None
        
    return jsonify({
        'ra': ra,
        'dec': dec,
        'constellation': constellation,
        'cst':cst,
        'bayer_name': bayer_name,
        'chinese_name': chinese_name,
        'distance': dist,
        'magnitude': magnitude,
        'spectrum': spectrum,
        'distance_ly': distance_ly,
        'hr_id': hr_id,
        'x':sx,
        'y':sy
    })

@app.route('/dxt_xt_img_rq')
def dxt_xt_img_rq():
    content = request.args.get('content', None)
    result = dxt_xt_img(content)
    if isinstance(result, str):  # 如果返回的是错误信息
        return result
    buf = BytesIO()
    result.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/dxt_xt', methods=['GET'])
def dxt_xt():
    content = request.args.get('content', None)
    if content is None:
        return render_template('dxt_xt.html', year='0')
        #return render_template('index.html')
    print('content:', content)
    m = re_xt.match(content)
    if m is None:
        return render_template('dxt_xt.html', year='0')
        #return render_template('index.html')
    year, = m.groups()
    return render_template('dxt_xt.html', year=year)

@app.route('/dxt_zp_img_rq')
def dxt_zp_img_rq():
    content = request.args.get('content', None)
    result = dxt_zp_img(content)
    if isinstance(result, str):  # 如果返回的是错误信息
        return result
    buf = BytesIO()
    result.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/dxt_zp', methods=['GET'])
def dxt_zp():
    content = request.args.get('content', None)
    if content is None:
        return render_template('index.html')
    print('content:', content)
    # 这里可以添加对 content 格式的验证
    m = re_zp.match(content)
    if m is None:
        return render_template('index.html')

    lats,_,longs,_,location,timezone = m.groups()
    latitude = '%.2f' % float(lats)
    longitude = '%.2f' % float(longs)

    return render_template('dxt_zp.html', latitude=latitude, longitude=longitude, location=location, timezone=timezone)

@app.route('/set_location', methods=['GET', 'POST'])
def set_location():
    tf = TimezoneFinder()
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location = request.form.get('location')[:20]
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
            timezone = tf.timezone_at(lng=longitude, lat=latitude)
        else:
            timezone = None

        # 将位置信息保存到 session 中
        session['location_info'] = {
            'latitude': latitude,
            'longitude': longitude,
            'location': location,
            'timezone': timezone
        }

        return redirect('/set_location')
        
    user_info = []
    location_info = session.get('location_info')
    if location_info:
        user_info = (
            location_info['latitude'],
            location_info['longitude'],
            location_info['location'],
            location_info['timezone']
        )
    else:
        user_info = default_info

    return render_template('set_location.html', user_info=user_info)




# 将 get_first_created_username 函数注册到 Jinja2 环境中
#app.jinja_env.globals.update(get_first_created_username=get_admin_location_info)

@app.route('/get_stars')
def get_stars():
    constellation = request.args.get('constellation')
    if not constellation:
        return jsonify([])
    
    # Load star data
    stars = parse_star_list(config.star_list_path)
    
    # Get Chinese constellation name
    cn_name = cstcn.get(constellation, constellation)
    
    # Find stars in constellation
    constellation_stars = find_stars_in_constellation(stars, cn_name)
    
    # Prepare response data
    response_data = []
    for star in constellation_stars:
        response_data.append({
            'hr_id': star['hr_id'],
            'bayer_name': star['bayer_name'],
            'ra': star['ra'],
            'dec': star['dec'],
            'chinese_name':star['chinese_name']
        })
    
    return jsonify(response_data)

@app.route('/get_star_coords')
def get_star_coords():
    hr_id = request.args.get('hr_id')
    if not hr_id:
        return jsonify({'error': 'HR ID required'}), 400
    
    try:
        hr_id = int(hr_id)
    except ValueError:
        return jsonify({'error': 'Invalid HR ID'}), 400
    
    # Load star data
    stars = parse_star_list(config.star_list_path)
    star = find_star_by_hr(stars, hr_id)
    bayer_name = star['bayer_name']
    print('get_star_coords bayer_name:',bayer_name)
    cst = bayer_name.split('/')[1]
    print('cst:',cst)
    if not star:
        return jsonify({'error': 'Star not found'}), 404
    
    return jsonify({
        'ra': star['ra'],
        'dec': star['dec'],
        'cst':cst
    })

@app.route('/get_star_info')
def get_star_info():
    hr_id = request.args.get('hr_id')
    if not hr_id:
        return jsonify({'error': 'HR ID required'}), 400
    
    skip="""
    try:
        hr_id = int(hr_id)
    except ValueError:
        return jsonify({'error': 'Invalid HR ID'}), 400
        """
    from ut_star import get_star_from_hr_id
    
    # Load star data
    stars = parse_star_list(config.star_list_path)
    star = find_star_by_hr(stars, hr_id)
    
    ra = star['ra']
    dec = star['dec']
    bayer_name = star['bayer_name']
    constellation = star['constellation']
    chinese_name = star['chinese_name']
    magnitude = star['magnitude']
    spectrum = star['spectrum']
    distance_ly = star['distance_ly']   
    cst = bayer_name.split('/')[1]
    print('constellation:%s bayer_name:%s ra:%.2f dec:%.2f' % (constellation,bayer_name,ra,dec))
    return jsonify({
        'ra': ra,
        'dec': dec,
        'constellation': constellation,
        'cst':cst,
        'bayer_name': bayer_name,
        'chinese_name': chinese_name,
        'magnitude': magnitude,
        'spectrum': spectrum,
        'distance_ly': distance_ly,
        'hr_id': hr_id
    })
    

@app.route('/radec_to_xy', methods=['POST'])
def radec_to_xy():
    data = request.get_json()
    ra = float(data['ra'])
    dec = float(data['dec'])
    cst = data['cst']
    star = data['star']
    
    from ut_cal import ra_dec_to_xyplot
    x, y = ra_dec_to_xyplot(ra, dec, config.xckz, config.yckz, config.rr)
    print('radec_to_xy: x:%s y:%s' % (x,y))
    return jsonify({
        'x': x,
        'y': y,
        'cst': cst,
        'star':star
    })

@app.route('/lin_radec_to_xy', methods=['POST'])
def lin_radec_to_xy():
    data = request.get_json()
    ra = float(data['ra']) / 15.0  # to ra_hr
    if ra < 18:
        ra+=24
    dec = float(data['dec'])
    cst = data['cst']
    star = data['star']
    
    from lin_base import RA_to_x, dec_to_y
    x = RA_to_x(g_share.x0, ra)
    y = dec_to_y(dec)
    print('lin_radec_to_xy: ra:%.2f dec:%.2f x:%s y:%s' % (ra,dec,x,y))
    return jsonify({
        'x': x,
        'y': y,
        'cst': cst,
        'star': star
    })

@app.route('/get_cstbnd_polygon', methods=['POST'])
def get_cstbnd_polygon():
    import random
    import math
    from ut_cstbnd import cstbnd_to_xyplot
    data = request.get_json()
    x = float(data['x'])
    y = float(data['y'])
    cst = data['cst']
    print('get_cstbnd_polygon: ',cst)
    points = cstbnd_to_xyplot(cst,config.xckz,config.yckz,config.rr)
    #print('points:', points)
    return jsonify({'points': points})

@app.route('/get_lin_cstbnd_polygon', methods=['POST'])
def get_lin_cstbnd_polygon():
    import math
    from ut_lin_cstbnd import lin_cstbnd_to_xyplot
    data = request.get_json()
    #x = float(data['x'])
    #y = float(data['y'])
    cst = data['cst']
    print('get_cstbnd_polygon: ',cst)
    points = lin_cstbnd_to_xyplot(cst, excludes=[])
    print('points:', points)
    return jsonify({'points': points})

@app.route('/astronomical_image')
def astronomical_image():
    ra = request.args.get('ra')
    dec = request.args.get('dec')
    name = request.args.get('name', 'Astronomical Object')
    survey = 'DSS'  # or '2MASS'
    
    from ut_astro_img import get_astronomical_image
    img_base64 = get_astronomical_image(ra, dec, name, survey)
    
    if not img_base64:
        return render_template_string('''
            <h1>Error retrieving astronomical image</h1>
            <p>Could not retrieve image for coordinates:</p>
            <p>RA: {{ra}}</p>
            <p>Dec: {{dec}}</p>
        ''', ra=ra, dec=dec)
    
    # 根据不同的巡天项目添加出处说明
    if survey == 'DSS':
        source_info=gettext("The image data in this document is sourced from the Digital Sky Survey (DSS). This data can be used provided that it complies with its terms of use.")
        #    source_info = "本图像数据来源于 Digital Sky Survey (DSS)，该数据可在符合其使用条款的前提下使用。"
    elif survey == '2MASS':
        source_info=gettext("The image data is sourced from the Two Micron All Sky Survey (2MASS). Please comply with its relevant usage licenses.")
        # source_info = "本图像数据来源于 Two Micron All Sky Survey (2MASS)，请遵循其相关使用许可。"
    else:
        source_info=gettext("The image data is sourced from ") + f"{survey}. " + gettext("Please comply with its relevant usage licenses.")
        #source_info = f"本图像数据来源于 {survey}，请遵循其相关使用许可。"
            
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Astronomical Image - {{name}}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 20px;
                }
                h1 {
                    margin-bottom: 20px;
                }
                img {
                    max-width: 90%;
                    max-height: 80vh;
                    border: 1px solid #ccc;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
            </style>
        </head>
        <body>
            <h1>{{name}}</h1>
            <p>RA: {{ra}} | Dec: {{dec}}</p>
            <img src="data:image/png;base64,{{img_base64}}" alt="Astronomical Image">
            <p>{{source_info}}</p>
        </body>
        </html>
    ''', ra=ra, dec=dec, name=name, img_base64=img_base64, source_info=source_info)

@app.route('/lin_dxt')
def lin_dxt():
    
    return render_template('lin_dxt.html',
                           csts=CSTS,
                           cstcn=cstcn)


if __name__=='__main__':
    app.run(debug=True)
