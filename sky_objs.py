from ut_cal import *

# 星云和星团数据（名称、赤经(小时)、赤纬(度)、类型）
objects = [
    {'name': 'M42 (猎户座星云)', 'ra': 5.5833, 'dec': -5.3833, 'r':10,
        'cst':'Ori','type': 'nebula'},
    {'name': 'M31 (仙女座星系)', 'ra': 0.6833, 'dec': 41.2667, 'r':15,
        'cst':'And','type': 'galaxy'},
    {'name': 'NGC2237 (玫瑰星云)', 'ra': 6.3333, 'dec': 4.5, 'r':10,
        'cst':'Mon','type': 'nebula'},
    {'name': 'M45 (昴星团)', 'ra': 3.72, 'dec': 24.1, 'r':10,
        'cst':'Tau','type': 'open_cluster'},
    {'name': 'M44 (鬼星团)', 'ra': 8.1167, 'dec': 19.2, 'r':10,
        'cst':'Cnc', 'type': 'open_cluster'},
    {'name': 'LMC (大麦哲伦云)', 'ra': 5.5, 'dec': -69.4, 'r':25,
        'cst': 'Dor','type': 'satellite_galaxy'},
    {'name': 'SMC (小麦哲伦云)', 'ra': 0.75, 'dec': -73.1, 'r':20,
        'cst':'Tuc','type': 'satellite_galaxy'}
]
def add_objs(paper,xc,yc,rr,im=None,draw=None,scale=0.5):
    f_s = g_share.f_south
    if paper is not None:
        layer_obj = paper.add_layer(name='objs')
        im=layer_obj.im
        draw= layer_obj.draw
    for obj in objects:
        ra = obj['ra'] * 15
        dec = obj['dec']
        r = int(obj['r'] * scale)
        print('add obj:%s' % obj['name'])
        x,y =ra_dec_to_xyplot(ra, dec,xc,yc,rr,f_s=f_s)
        draw.circle((x,y),r,fill=(100,100,100,100))
        