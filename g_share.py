# global share variable for passing around

class G_SHARE:
    Obl=None
    f_south=False
    
    def set_f_south(self,f_south):
        print('set_f_south from %s to %s' % (self.f_south,f_south))
        self.f_south= f_south
        
    def get_f_south(self):
        return self.f_south
        
g_share= G_SHARE()
