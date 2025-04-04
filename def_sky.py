from paper import *

# r1: the largest circle. approx. 60mm radius
r1 = round(2.333 * DPI) #1400 #1350 
r2 = r1 - 60   # r1-r2 : for altas, the zodiac circle
               #         for hor plate, the time zhe circle
r3 = r2 - 60   # r2-r3 : for altas, the month zhe circle
               #         for hor plate, the time hour circle
r4 = r3 - 60   # r3-r4 : for altas, the month day circle
r5 = r4 -60    # r4-r5 : for altas, the 24 jie qi circle

r5a = r5 -30   # for ra marker
    
r_90=r5        # dec = 90 degree circle
rr = 180/r_90  # 1 degree / pixel in radian direction
requ = int(r_90/2)  # the equatorial circle
