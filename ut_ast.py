import pytz
from datetime import datetime, timedelta
import math


def calculate_LMT(dt: datetime, timezone: str, longitude: float) -> float:
    """
    计算地方平太阳时（Local Mean Time），单位：小时（带小数，如12.5表示12h30m）
    
    参数：
        dt: 本地时间（datetime对象，不含时区信息）
        timezone: 时区字符串（如'Asia/Shanghai'）
        longitude: 观测点经度（东经为正，西经为负，单位：度）
    
    返回：
        LMT: 地方平太阳时（小时，0-24）
    """
    # 1. 将本地时间转换为带时区的UTC时间
    loc_tz = pytz.timezone(timezone)
    loc_dt = loc_tz.localize(dt, is_dst=None)  # 本地化时间（避免夏令时歧义）
    utc_dt = loc_dt.astimezone(pytz.utc)       # 转换为UTC时间
    
    # 2. 计算时区中线经度（如东八区中线为120°E）
    tz_offset_hours = loc_tz.utcoffset(dt).total_seconds() / 3600  # 时区偏移（小时）
    tz_central_lon = tz_offset_hours * 15  # 时区中线经度（1小时=15°）
    
    # 3. 计算经度修正：每度对应4分钟（4分钟/度 = 1/15 小时/度）
    lon_correction = (longitude - tz_central_lon) / 15  # 单位：小时
    
    # 4. 计算LMT：UTC时间 + 时区偏移 + 经度修正
    utc_hours = utc_dt.hour + utc_dt.minute/60 + utc_dt.second/3600  # UTC时间（小时）
    lmt = utc_hours + tz_offset_hours + lon_correction
    
    # 规范到0-24小时
    return lmt % 24


def calculate_EOT(dt: datetime) -> float:
    """
    计算时差（Equation of Time），单位：分钟（真太阳时 - 平太阳时，正值表示真太阳时更快）
    
    参数：
        dt: 日期时间（datetime对象）
    
    返回：
        EOT: 时差（分钟，范围约±16）
    """
    # 1. 计算从1月1日起的天数（n）
    year = dt.year
    month = dt.month
    day = dt.day
    # 计算当年1月1日的datetime对象
    jan1 = datetime(year, 1, 1)
    # 计算当前日期与1月1日的天数差（包含小数天数）
    delta = dt - jan1
    n = delta.total_seconds() / 86400  # 总秒数转换为天数
    
    # 2. 计算太阳黄经相关参数（弧度）
    B = 2 * math.pi * (n - 1) / 365  # 角度参数
    
    # 3. 时差公式（基于Meeus天文算法简化，精度±0.5分钟）
    eot = (229.18 * (0.000075 + 0.001868 * math.cos(B) - 0.032077 * math.sin(B)
                     - 0.014615 * math.cos(2*B) - 0.040849 * math.sin(2*B)))
    
    return eot


def calculate_AST(dt: datetime, timezone: str, longitude: float) -> tuple:
    """
    计算真太阳时（Apparent Solar Time），返回 (小时, 分钟) 形式
    
    参数：
        dt: 本地时间（datetime对象，不含时区信息）
        timezone: 时区字符串（如'Asia/Shanghai'）
        longitude: 观测点经度（东经为正，西经为负，单位：度）
    
    返回：
        (hours, minutes): 真太阳时（小时，分钟）
    """
    # 1. 计算地方平太阳时（小时，带小数）
    lmt_hours = calculate_LMT(dt, timezone, longitude)
    
    # 2. 计算时差（分钟）
    eot_minutes = calculate_EOT(dt)
    
    # 3. 真太阳时 = LMT（小时） + EOT（转换为小时）
    ast_hours = lmt_hours + (eot_minutes / 60)
    
    # 4. 转换为 (小时, 分钟) 并规范范围
    ast_hours = ast_hours % 24  # 确保在0-24小时内
    hours = int(ast_hours)
    minutes = int(round((ast_hours - hours) * 60))
    
    # 处理分钟进位（如59.9分钟→60分钟→进位到小时）
    if minutes >= 60:
        hours += 1
        minutes -= 60
    hours %= 24  # 再次确保小时在0-23范围
    
    return (hours, minutes)


# ------------------------------
# 测试示例
# ------------------------------
if __name__ == "__main__":
    # 观测点：北京（东经116.3°，北纬39.9°），时区：Asia/Shanghai（东八区）
    # 测试时间：2023年10月1日 12:00:00（本地时间）
    test_dt = datetime(2023, 10, 1, 12, 0, 0)
    tz = "Asia/Shanghai"
    lon = 116.3  # 北京经度
    
    # 计算LMT（地方平太阳时）
    lmt = calculate_LMT(test_dt, tz, lon)
    print(f"地方平太阳时（LMT）：{lmt:.2f} 小时 → {int(lmt)}时{int(round((lmt%1)*60))}分")
    
    # 计算时差（EOT）
    eot = calculate_EOT(test_dt)
    print(f"时差（EOT）：{eot:.2f} 分钟")
    
    # 计算真太阳时（AST）
    ast = calculate_AST(test_dt, tz, lon)
    print(f"真太阳时（AST）：{ast[0]}时{ast[1]}分")