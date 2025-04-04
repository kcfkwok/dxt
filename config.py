import platform
from pathlib import Path

APP_NAME='dxt'
if platform.system=='Linux':
    user_home = Path.home()
    app_home = Path(Path.home(),APP_NAME)
else:
    from win_user_home import user_home, app_home
    
class CONFIG:
    debug=False
    ari_ang=90
    
    # path info
    dbpath = Path(user_home, 'db/users.db')
    fontpath = Path(user_home, 'font/GenSenRoundedTW-R.ttf')
    interpath = Path(user_home, 'inter')
    staticpath =Path(app_home, 'static')
    
    # image path
    fpng_banner=Path(staticpath, 'image/banner.png')

    # inter path for graphics
    fbg_rl = 'skyl_rl_bg_y%s.png' # % year <- sky_rl_bg.py
    fbg_a5r_yw_n = 'skyl_bg_n_y%s_A5R_yw.png' # % year <- sky_rl_bg.py
    fbg_a5r_yw_s = 'skyl_bg_s_y%s_A5R_yw.png' # % year <- sky_rl_bg.py

    # paper metrics info
    DPI=600
    MARGIN= DPI/8
    INCHX_10TH = DPI / 10
    MM_UNIT = DPI/25.4
    xc1 = int(70 * MM_UNIT)
    yc1 = int(77 * MM_UNIT)
    xc2 = int(70 * MM_UNIT *2 + 60 * MM_UNIT)
    yc2 = int(77 * MM_UNIT)

    banner_x = int(10*MM_UNIT)
    banner_y = int(4*MM_UNIT)

    
config = CONFIG()

