"""Star catalog module for looking up stars by HR ID."""

STAR_DATA = {
    # HR ID: (bayer_name, constellation, ra, dec, magnitude, distance_ly, spectrum, chinese_name)
    15: ('alf/And', '仙女', 2.10, 29.1, 2.1, 98, 'B8IVpMnHg', '壁宿二'),
    21: ('bet/Cas', '仙后', 2.29, 59.1, 2.3, 55, 'F2III-IV', '王良一'),
    25: ('eps/Phe', '凤凰', 2.35, -45.7, 3.9, 141, 'K0III', ''),
    39: ('gam/Peg', '飞马', 3.31, 15.2, 2.8, 362, 'B2IV', '壁宿一'),
    45: ('chi/Peg', '飞马', 3.65, 20.2, 4.8, 326, 'M2+III', ''),
    63: ('tet/And', '仙女', 4.27, 38.7, 4.6, 271, 'A2V', ''),
    68: ('sig/And', '仙女', 4.58, 36.8, 4.5, 141, 'A2V', ''),
    74: ('iot/Cet', '鲸鱼', 4.86, -8.8, 3.5, 296, 'K1.5III', '天仓一'),
    77: ('zet/Tuc', '杜鹃', 5.02, -64.9, 4.2, 28, 'F9V', ''),
    98: ('bet/Hyi', '水蛇', 6.44, -77.3, 2.8, 24, 'G2IV', ''),
    99: ('alf/Phe', '凤凰', 6.57, -42.3, 2.4, 77, 'K0III', '火鸟六'),
    100: ('kap/Phe', '凤凰', 6.55, -43.7, 3.9, 77, 'A7V', ''),
    105: ('eta/Scl', '玉夫', 6.98, -33.0, 4.8, 645, 'M4III', ''),
    123: ('lam/Cas', '仙后', 7.94, 54.5, 4.7, 362, 'B8Vn', ''),
    125: ('lam1/Phe', '凤凰', 7.85, -48.8, 4.8, 181, 'A0V', ''),
    126: ('bet1/Tuc', '杜鹃', 7.89, -63.0, 4.4, 141, 'B9V', ''),
    127: ('bet2/Tuc', '杜鹃', 7.89, -63.0, 4.5, 181, 'A2V+A7V', ''),
    130: ('kap/Cas', '仙后', 8.25, 62.9, 4.2, 2917, 'B1Iae', ''),
    153: ('zet/Cas', '仙后', 9.24, 53.9, 3.7, 660, 'B2IV', ''),
    154: ('pi/And', '仙女', 9.22, 33.7, 4.4, 356, 'B5V', ''),
    163: ('eps/And', '仙女', 9.64, 29.3, 4.4, 171, 'G8IIIp', ''),
    165: ('del/And', '仙女', 9.83, 30.9, 3.3, 101, 'K3III', ''),
    168: ('alf/Cas', '仙后', 10.13, 56.5, 2.2, 232, 'K0IIIa', '王良四'),
    179: ('xi/Cas', '仙后', 10.52, 50.5, 4.8, 572, 'B2V', ''),
    180: ('mu/Phe', '凤凰', 10.33, -46.1, 4.6, 250, 'G8III', ''),
    184: ('pi/Cas', '仙后', 10.87, 47.0, 4.9, 181, 'A5V', ''),
    188: ('bet/Cet', '鲸鱼', 10.90, -18.0, 2.0, 95, 'K0IIICH-1HK-0.5', '土司空'),
    191: ('eta/Phe', '凤凰', 10.84, -57.5, 4.4, 250, 'A0IV', ''),
    193: ('omi/Cas', '仙后', 11.18, 48.3, 4.5, 476, 'B5IIIe', ''),
    194: ('phi1/Cet', '鲸鱼', 11.05, -10.6, 4.8, 217, 'K0IIIv', ''),
    215: ('zet/And', '仙女', 11.83, 24.3, 4.1, 191, 'K1IIe', ''),
    219: ('eta/Cas', '仙后', 12.27, 57.8, 3.4, 19, 'G0V+dM0', '王良三'),
    223: ('nu/Cas', '仙后', 12.21, 51.0, 4.9, 407, 'B9III', ''),
    224: ('del/Psc', '双鱼', 12.17, 7.6, 4.4, 326, 'K5III', ''),
    226: ('nu/And', '仙女', 12.45, 41.1, 4.5, 390, 'B5V+F8V', ''),
    253: ('ups1/Cas', '仙后', 13.75, 59.0, 4.8, 407, 'K2III', ''),
    264: ('gam/Cas', '仙后', 14.18, 60.7, 2.5, 624, 'B0IVe', ''),
    265: ('ups2/Cas', '仙后', 14.17, 59.2, 4.6, 217, 'G8.5IIIbCN-1', ''),
    269: ('mu/And', '仙女', 14.19, 38.5, 3.9, 141, 'A5V', ''),
    271: ('eta/And', '仙女', 14.30, 23.4, 4.4, 250, 'G8IIIb', ''),
    280: ('alf/Scl', '玉夫', 14.65, -29.4, 4.3, 556, 'B7IIIp', ''),
    294: ('eps/Psc', '双鱼', 15.74, 7.9, 4.3, 191, 'K0III', ''),
    322: ('bet/Phe', '凤凰', 16.52, -46.7, 3.3, 203, 'G8IIIv', ''),
    334: ('eta/Cet', '鲸鱼', 17.15, -10.2, 3.4, 120, 'K1.5IIICN1', '天仓二'),
    337: ('bet/And', '仙女', 17.43, 35.6, 2.0, 203, 'M0IIIa', ''),
    338: ('zet/Phe', '凤凰', 17.10, -55.2, 3.9, 296, 'B6V+B9V', ''),
    343: ('tet/Cas', '仙后', 17.78, 55.1, 4.3, 141, 'A7V', ''),
    351: ('chi/Psc', '双鱼', 17.86, 21.0, 4.7, 465, 'G8.5III-IIIa', ''),
    360: ('phi/Psc', '双鱼', 18.44, 24.6, 4.7, 407, 'K0III', ''),
    370: ('nu/Phe', '凤凰', 18.80, -45.5, 5.0, 49, 'F8V', ''),
    377: ('kap/Tuc', '杜鹃', 18.94, -68.9, 4.9, 67, 'F6IV', ''),
    382: ('phi/Cas', '仙后', 20.02, 58.2, 5.0, 7989, 'F0Ia', ''),
    390: ('xi/And', '仙女', 20.58, 45.5, 4.9, 203, 'K0-IIIb', '奎宿七'),
    399: ('psi/Cas', '仙后', 21.48, 68.1, 4.7, 203, 'K0III', ''),
    402: ('tet/Cet', '鲸鱼', 21.01, -8.2, 3.6, 116, 'K0IIIb', ''),
    403: ('del/Cas', '仙后', 21.45, 60.2, 2.7, 101, 'A5III-IVv', '阁道三'),
    424: ('alf/UMi', '小熊', 37.96, 89.3, 2.0, 465, 'F7:Ib-IIv', '勾陈一'),
    429: ('gam/Phe', '凤凰', 22.09, -43.3, 3.4, 250, 'M0-IIIa', ''),
    434: ('mu/Psc', '双鱼', 22.55, 6.1, 4.8, 362, 'K4III', ''),
    440: ('del/Phe', '凤凰', 22.81, -49.1, 4.0, 148, 'K0III-IV', ''),
    442: ('chi/Cas', '仙后', 23.48, 59.2, 4.7, 217, 'G9IIIb', ''),
    458: ('ups/And', '仙女', 24.20, 41.4, 4.1, 44, 'F8V', ''),
    472: ('alf/Eri', '波江', 24.43, -57.2, 0.5, 148, 'B3Vpe', '水委一'),
    509: ('tau/Cet', '鲸鱼', 26.02, -15.9, 3.5, 11, 'G8V', ''),
    539: ('zet/Cet', '鲸鱼', 27.86, -10.3, 3.7, 271, 'K0IIIBa0.1', '天仓四'),
    542: ('eps/Cas', '仙后', 28.60, 63.7, 3.4, 465, 'B3III', ''),
    544: ('alf/Tri', '三角', 28.27, 29.6, 3.4, 65, 'F6IV', '娄宿增六'),
    553: ('bet/Ari', '白羊', 28.66, 20.8, 2.7, 60, 'A5V', '娄宿一'),
    591: ('alf/Hyi', '水蛇', 29.69, -61.6, 2.9, 72, 'F0V', ''),
    603: ('gam1/And', '仙女', 30.97, 42.3, 2.3, 362, 'K3-IIb', '天大将军一'),
    617: ('alf/Ari', '白羊', 31.79, 23.5, 2.0, 66, 'K2IIIabCa-I', '娄宿三'),
    681: ('omi/Cet', '鲸鱼', 34.84, -3.0, 3.0, 465, 'M7IIIe', '刍贽增二'),
    911: ('alf/Cet', '鲸鱼', 45.57, 4.1, 2.5, 232, 'M1.5IIIa', ''),
    936: ('bet/Per', '英仙', 47.04, 41.0, 2.1, 93, 'B8V', '大陵五'),
    1017: ('alf/Per', '英仙', 51.08, 49.9, 1.8, 529, 'F5Ib', '天船三'),
    1084: ('eps/Eri', '波江', 53.23, -9.5, 3.7, 10, 'K2V', ''),
    1231: ('gam/Eri', '波江', 59.51, -13.5, 2.9, 232, 'M0.5IIICa-ICr-I', '天苑一'),
    1457: ('alf/Tau', '金牛', 68.98, 16.5, 0.9, 65, 'K5III', '毕宿五')
}

def get_star_info(hr_id):
    """Get star information by HR ID.
    
    Args:
        hr_id: Integer HR catalog number
        
    Returns:
        Dictionary with star information or None if not found
    """
    if hr_id not in STAR_DATA:
        return None
        
    data = STAR_DATA[hr_id]
    return {
        'bayer_name': data[0],
        'constellation': data[1],
        'ra': data[2],
        'dec': data[3],
        'magnitude': data[4],
        'distance_ly': data[5],
        'spectrum': data[6],
        'chinese_name': data[7]
    }

def get_constellation(hr_id):
    """Get constellation for a star by HR ID.
    
    Args:
        hr_id: Integer HR catalog number
        
    Returns:
        Constellation abbreviation or None if not found
    """
    star = get_star_info(hr_id)
    return star['constellation'] if star else None

def get_star_name(hr_id):
    """Get star name by HR ID.
    
    Args:
        hr_id: Integer HR catalog number
        
    Returns:
        Bayer designation or None if not found
    """
    star = get_star_info(hr_id)
    return star['bayer_name'] if star else None
