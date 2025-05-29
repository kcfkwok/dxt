import io
import base64
from flask import Flask, render_template_string, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.skyview import SkyView
from astropy.wcs import WCS

#app = Flask(__name__)

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei"]

# 创建自定义Simbad查询对象
customSimbad = Simbad()
customSimbad.add_votable_fields('otype')  # 添加对象类型字段

def get_astronomical_image(ra_hms, dec_dms, object_name="目标", survey='DSS', image_width=300*u.arcmin, image_height=300*u.arcmin):
    """
    从Simbad获取天体信息并通过SkyView获取和显示天体图像
    
    参数:
    ra_hms (str): 赤经，格式为hms (时:分:秒)，例如"00h42m44s"
    dec_dms (str): 赤纬，格式为dms (度:分:秒)，例如"+41d16m08s"
    object_name (str): 天体名称，用于显示，默认为"目标"
    survey (str): 要使用的巡天项目，默认为DSS (Digital Sky Survey)
    image_width (astropy.units.Quantity): 图像宽度，默认10角分
    image_height (astropy.units.Quantity): 图像高度，默认10角分
    """
    try:
        # 将hms/dms格式的坐标转换为SkyCoord对象
        coords = SkyCoord(ra_hms, dec_dms, frame='icrs')
        
        # 获取图像
        print(f"正在获取坐标 ({ra_hms}, {dec_dms}) 的图像...")
        images = SkyView.get_images(position=coords, survey=[survey], 
                                   width=image_width, height=image_height)
        
        if not images or len(images) == 0 or len(images[0]) == 0:
            print(f"无法获取指定坐标的图像")
            return None
        
        # 获取WCS信息用于坐标转换
        wcs = WCS(images[0][0].header)
        
        # 显示图像，使用WCS坐标
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection=wcs)
        plt.title(f"{object_name} - {survey}")
        plt.imshow(images[0][0].data, cmap='gray')
        plt.colorbar(label='亮度')
        
        # 设置坐标轴标签为RA和Dec
        ax.set_xlabel('赤经 (J2000)')
        ax.set_ylabel('赤纬 (J2000)')
        
        # 添加网格线
        ax.grid(True, color='yellow', alpha=0.5)
        
        # 在图像上标记指定坐标位置
        ax.scatter(coords.ra.deg, coords.dec.deg, transform=ax.get_transform('world'),
                  s=100, marker='+', color='red', label='指定坐标')
        ax.legend()
        
        # 保存图像到缓冲区
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        # 将图像编码为 base64
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        return img_base64
        
    except Exception as e:
        print(f"发生错误: {e}")
        return None
