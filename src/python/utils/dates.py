from datetime import datetime, timezone
import pytz
from tzlocal import get_localzone


LOCAL_TZ = get_localzone()
API_TZ = pytz.timezone("Europe/London")

def get_server_datetime():
    london_time = datetime.now(tz=timezone.utc).astimezone(API_TZ)
    return london_time

def server_to_local_datetime(date):
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    return API_TZ.localize(dt).astimezone(LOCAL_TZ)

def local_to_server_datetime(date):
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    return LOCAL_TZ.localize(dt).astimezone(API_TZ)