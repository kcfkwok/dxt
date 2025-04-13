import math
from ut_cal import ra_dec_to_xyplot, xyplot_to_ra_dec

def test_conversion(ra, dec, rr=0.155, xc=1500, yc=1500, f_s=True):
    print(f"\nTesting with RA={ra:.2f}, DEC={dec:.2f}")
    
    # Convert RA/DEC to x/y
    x, y = ra_dec_to_xyplot(ra, dec, xc, yc, rr, f_s=f_s)
    print(f"Converted to x={x}, y={y}")
    
    # Convert x/y back to RA/DEC
    new_ra, new_dec = xyplot_to_ra_dec(x, y, xc, yc, rr, f_s=f_s)
    print(f"Converted back to RA={new_ra:.2f}, DEC={new_dec:.2f}")
    
    # Calculate differences
    ra_diff = abs(new_ra - ra)
    dec_diff = abs(new_dec - dec)
    
    print(f"Differences - RA: {ra_diff:.6f}°, DEC: {dec_diff:.6f}°")
    
    return ra_diff, dec_diff

def run_tests():
    # Test cases covering different RA/DEC values
    test_cases = [
        (0, 0),       # Zero point
        (90, 45),     # First quadrant
        (180, -45),   # Second quadrant
        (270, 89),    # Near pole
        (45, 30),     # Typical value
        (359.9, -89),  # Edge cases
        (101, -16),
        (258,-16),
    ]
    
    max_ra_diff = 0
    max_dec_diff = 0
    
    for ra, dec in test_cases:
        ra_diff, dec_diff = test_conversion(ra, dec)
        max_ra_diff = max(max_ra_diff, ra_diff)
        max_dec_diff = max(max_dec_diff, dec_diff)
    
    print("\nMaximum differences:")
    print(f"RA: {max_ra_diff:.6f}°")
    print(f"DEC: {max_dec_diff:.6f}°")
    
    if max_ra_diff > 0.01 or max_dec_diff > 0.01:
        print("\nWARNING: Significant differences detected - possible bug in conversions")
    else:
        print("\nConversions working as expected")

if __name__ == "__main__":
    run_tests()
