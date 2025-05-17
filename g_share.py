# global share variable for passing around
from config import config

class G_SHARE:
    Obl=None
    f_south=False
    hor_cir_opacity=128
    
    def set_f_south(self,f_south):
        print('set_f_south from %s to %s' % (self.f_south,f_south))
        self.f_south= f_south
        
    def get_f_south(self):
        return self.f_south
        
    def init_linplot(self, x0,xr_end,y00,y01,y_equ):
        print('g_share.init_linplot')
        print('x0:',x0)
        print('xr_end:',xr_end)
        print('y00:', y00)
        print('y01:',y01)
        print('y_equ:', y_equ)
    
        g_share.x0=x0
        g_share.xr_end=xr_end
        g_share.y00=y00   # dec -90
        g_share.y01=y01   # dec +90
        g_share.ydec_m = (y01 - y00) / 180  # dec to y slop
        g_share.ydec_c = y00 + (y01 - y00) / 2 # dec to y-intercept (c)
        g_share.y_equ = y_equ
        
g_share= G_SHARE()
g_share.init_linplot(config.lin_x0,config.lin_xr_end,config.lin_y00,
    config.lin_y01,config.lin_y_equ)
    