"""
Program to read star info and convert RA/DEC to X/Y coordinates
for both northern and southern hemisphere views.
Results are saved to separate output files.
"""

from read_star_list import parse_star_list
from ut_cal import ra_dec_to_xyplot
from g_share import g_share
from config import config

# Constants provided by user
XC = 1653
YC = 1818
RR = 0.15517241379310345

def convert_star_coordinates():
    # Read star data
    stars = parse_star_list(config.star_list_path)
    
    # Process for both northern and southern hemispheres
    for f_south in [False, True]:
        hemisphere = "south" if f_south else "north"
        output_file = f"star_coords_{hemisphere}.txt"
        g_share.f_south = f_south  # Set hemisphere flag
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("HR_ID\tBayer_Name\tConstellation\tRA\tDEC\tX\tY\tMagnitude\tDistance_LY\tSpectrum\tChinese_Name\n")
            
            # Convert and write each star's coordinates
            for hr_id, star in stars.items():
                ra = star['ra']
                dec = star['dec']
                
                # Convert RA/DEC to X/Y
                x, y = ra_dec_to_xyplot(ra, dec, XC, YC, RR, f_s=f_south)
                
                # Write results
                f.write(f"{hr_id}\t{star['bayer_name']}\t{star['constellation']}\t")
                f.write(f"{ra:.6f}\t{dec:.6f}\t{x}\t{y}\t")
                f.write(f"{star['magnitude']}\t{star['distance_ly']}\t")
                f.write(f"{star['spectrum']}\t{star['chinese_name'] or ''}\n")

if __name__ == "__main__":
    convert_star_coordinates()
    print("Conversion complete. Results saved to star_coords_north.txt and star_coords_south.txt")