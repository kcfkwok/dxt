import platform
from pathlib import Path

APP_NAME='dxt'
if platform.system()=='Linux':
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
    fmw_n = 'skyl_mw_n_j2000.png' # <- sky_mw.py
    fmw_s = 'skyl_mw_s_j2000.png' # <- sky_mw.py
    fdt_n = 'skyl_dt_n.y%s.png' # % year <- sky_dt.py
    fdt_s = 'skyl_dt_s_y%s.png' # % year <- sky_dt.py
    fbg_n = 'skyl_bg_n_j2000.png' #  <- sky_bg.py
    fbg_s = 'skyl_bg_s_j2000.png' #   <-  sky_bg.py

    # static path image
    fxt_png=Path(staticpath, 'dxt_xt_A4.png')
    fxt_pdf=Path(staticpath,'dxt_xt_A4.pdf')
    frl_png=Path(staticpath, 'dxt_rl_A4.png')
    frl_pdf=Path(staticpath,'dxt_rl_A4.pdf')

    
    # json file
    mw_path =Path(interpath, "mw.json")
    # iers_auto_url
    iers_auto_url= Path(interpath, 'finals2000A.all')
    
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

    # color
    color_sky_day =(176, 224, 230)
    color_sky_twilight= (255, 228, 196)
    color_sky_night= (0, 0, 100)
    color_cst_line = (192, 192, 192)
    color_cst_line_day = (255, 255, 204)

    EQU_LINE_COLOR=(255,0,0,255)
    ECL_LINE_COLOR=(200,200,0,255)
    ECL_LINE_WIDTH=10

config = CONFIG()

