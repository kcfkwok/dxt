from flask import Flask, request, render_template, render_template_string, send_file, Response, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
from secret_key import secret_key
from config import config
from image_generator import dxt_rl_img, dxt_kz_img, dxt_kz_img_wu, dxt_xt_img, dxt_zp_img,re_xt, re_zp, re_kz0, re_kz1
from pdf_generator import dxt_rl_pdf, dxt_xt_pdf, dxt_zp_pdf, dxt_kz_pdf
from default_info import default_info
from io import BytesIO
from timezonefinder import TimezoneFinder
import pytz
import datetime

app = Flask(__name__)
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{config.dbpath}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return render_template('dxt_kz.html', latitude=latitude, longitude=longitude, location=location, timezone=timezone, year=year,month=month,day=day,hour=hour,minute=minute)


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
        #return render_template('index.html')
    print('content:', content)
    m = re_rl.match(content)
    if m is None:
        return render_template('dxt_rl.html', year='0', month='0', day='0')
        #return render_template('index.html')
    year, month, day = m.groups()
    return render_template('dxt_rl.html', year=year, month=month, day=day)

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

if __name__=='__main__':
    app.run(debug=True)
