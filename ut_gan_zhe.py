"""Utilities for calculating Chinese gan and zhe based on time"""

# The 10 Heavenly Stems (gan)
GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# The 12 Earthly Branches (zhe)  
ZHE = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

INDEX_GAN=[0]
INDEX_ZHE=[0]

j=1
for i in range(0,22,2):
    INDEX_GAN.append(j)
    INDEX_GAN.append(j)
    j+=1
    if j > 9:
        j=0
INDEX_GAN.append(j)

j=1
for i in range(0,22,2):
    INDEX_ZHE.append(j)
    INDEX_ZHE.append(j)
    j+=1
INDEX_ZHE.append(0)

    

def calculate_gan_zhe(gan_at_0: str, zhe_at_0: str, current_hour: int) -> tuple[str, str]:
    """Calculate the current gan and zhe based on midnight values and current hour.
    
    Args:
        gan_at_0: The gan at midnight (0 hour)
        zhe_at_0: The zhe at midnight (0 hour)
        current_hour: The hour to calculate for (0-23)
        
    Returns:
        A tuple of (current_gan, current_zhe)
        
    Raises:
        ValueError: If inputs are invalid
    """
    # Validate inputs
    if gan_at_0 not in GAN:
        raise ValueError(f"Invalid gan_at_0: {gan_at_0}")
    if zhe_at_0 not in ZHE:
        raise ValueError(f"Invalid zhe_at_0: {zhe_at_0}")
    if not 0 <= current_hour <= 23:
        raise ValueError(f"Invalid current_hour: {current_hour}")


    # Calculate indices
    gan_index = (GAN.index(gan_at_0) + INDEX_GAN[current_hour]) % len(GAN)
    zhe_index = INDEX_ZHE[current_hour]
    print('gan:%s zhe:%s' % (gan_index, zhe_index))
    #gan_index = (GAN.index(gan_at_0) + current_hour // 2) % len(GAN)
    #zhe_index = (ZHE.index(zhe_at_0) + current_hour) % len(ZHE)
    
    return GAN[gan_index], ZHE[zhe_index]

if __name__=='__main__':
    print('INDEX_GAN')
    for i in range(24):
        print(i, INDEX_GAN[i])
    print('INDEX_ZHE')
    for i in range(24):
        print(i, INDEX_ZHE[i])
    for i in range(24):
        gan,zhe = calculate_gan_zhe('丙','子',i)
        print(i, gan,zhe)
