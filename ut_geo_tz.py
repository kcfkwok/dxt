from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime

def get_location_info(latitude, longitude):
    """
    Get location address and timezone from geographic coordinates

    Args:
        latitude (float): Geographic latitude
        longitude (float): Geographic longitude

    Returns:
        dict: Dictionary containing location name and timezone
    """
    print("get_location_info:%02f %02f" % (latitude,longitude))
    # Initialize geolocator and timezone finder
    geolocator = Nominatim(user_agent="geo_locator")
    tf = TimezoneFinder()

    # Get location name
    location_addr =''
    error_message = None
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
        location_addr = location.address if location else "Unknown Location"
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        error_message = f"Geocoding error: {str(e)}"

    # Get timezone
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    print("timezone_str:%s" % timezone_str)
    return location_addr, timezone_str , error_message


def get_timezone_offset(timezone_str):
    try:
        # Get the timezone object
        tz = pytz.timezone(timezone_str)
        
        # Get current time in UTC
        now = datetime.utcnow()
        
        # Get the offset in hours
        offset = tz.utcoffset(now).total_seconds() / 3600
        
        return int(offset)
    except pytz.UnknownTimeZoneError:
        return None


if __name__=='__main__':
    latv = 22.5
    longv=114.5
    location, timezone,err_msg =    get_location_info(latv, longv)
    print(location, timezone, err_msg)
