from flask import Blueprint, request, render_template, redirect, session
from models import User, db
from config import config
from flask_babel import gettext
from dprint import dprint
import bcrypt
from timezonefinder import TimezoneFinder

user_bp = Blueprint('user', __name__)

def get_user_count():
    return User.query.count()

def get_first_created_username():
    user = User.query.order_by(User.id).first()
    if user:
        dprint('get_first_created_username:%s' % user.username)
        return user.username
    dprint('get_first_created_username:None')
    return None

def get_admin_location_info():
    admin_username = get_first_created_username()
    if admin_username:
        user = User.query.filter_by(username=admin_username).first()
        if user:
            return (user.latitude, user.longitude, user.location, user.timezone)
    return None

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    username = session.get('username')
    style = get_user_style(username)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            print(f"User {username} logged in successfully. Session username: {session.get('username')}")
            return redirect('/')
        else:
            return render_template('login.html', error=gettext('Invalid username or password'))
    return render_template('login.html', username=username, style=style)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    user_count = get_user_count()

    if user_count >= config.max_user_count:
        return render_template('register.html', error=gettext('Registration is closed as the maximum number of accounts has been reached.'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print(f"User {username} registered successfully.")
            return redirect('/login')
        except Exception:
            db.session.rollback()
            return render_template('register.html', error=gettext('Username already exists'))

    return render_template('register.html')

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@user_bp.route('/change_location', methods=['GET', 'POST'])
def change_location():
    from timezonefinder import TimezoneFinder
    tf = TimezoneFinder()
    username = session.get('username')
    if not username:
        return redirect('/login')

    admin_info = get_admin_location_info()

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
        user = User.query.filter_by(username=username).first()
        if user:
            user.latitude = latitude
            user.longitude = longitude
            user.location = location
            user.timezone = timezone
            db.session.commit()
            user_info = (user.latitude, user.longitude, user.location, user.timezone)
            return render_template('change_location.html', username=username, user_info=user_info,
                                   success=gettext('Location information updated successfully'))

    user = User.query.filter_by(username=username).first()
    if user:
        user_info = (user.latitude, user.longitude, user.location, user.timezone)
    elif admin_info:
        user_info = admin_info
    else:
        user_info = []

    return render_template('change_location.html', username=username, user_info=user_info)

@user_bp.route('/set_location', methods=['GET', 'POST'])
def set_location():
    tf = TimezoneFinder()
    username = session.get('username')
    if username:
        return redirect('/')

    admin_info = get_admin_location_info()

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
    elif admin_info:
        user_info = admin_info

    return render_template('set_location.html', username=username, user_info=user_info)


@user_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = session.get('username')
    if not username:
        return redirect('/login')

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(old_password):
            user.set_password(new_password)
            db.session.commit()
            return render_template('change_password.html', username=username, success='Password changed successfully')
        else:
            return render_template('change_password.html', username=username, error=gettext('Old password is incorrect'))

    return render_template('change_password.html', username=username)

@user_bp.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    admin_username = get_first_created_username()
    current_username = session.get('username')

    if not current_username:
        return redirect('/login')

    if current_username != admin_username:
        return render_template('delete_account.html', username=current_username,
                               error=gettext('You do not have permission to delete accounts.'))

    if request.method == 'POST':
        username_to_delete = request.form.get('username_to_delete')
        if username_to_delete == admin_username:
            return render_template('delete_account.html', username=current_username,
                                   error=gettext('You cannot delete the admin account.'))
        user_to_delete = User.query.filter_by(username=username_to_delete).first()
        if user_to_delete:
            try:
                db.session.delete(user_to_delete)
                db.session.commit()
                return render_template('delete_account.html', username=current_username,
                                       success=gettext('Account') + f' {username_to_delete} ' +  gettext('deleted successfully.'))
            except Exception as e:
                print(f"Error deleting user: {e}")
                db.session.rollback()
                return render_template('delete_account.html', username=current_username,
                                       error=gettext('An error occurred while deleting the account.'))
        else:
            return render_template('delete_account.html', username=current_username,
                                   error=gettext('User not found.'))

    users = User.query.filter(User.username != admin_username).all()
    return render_template('delete_account.html', username=current_username, users=users)

def get_user_style(username):
    if not username:
        return 'default'
    user = User.query.filter_by(username=username).first()
    if user:
        return user.style
    return 'default'

@user_bp.route('/')
def index():
    print('user_bp index.html')
    return render_template('index.html')