import time
from datetime import datetime

import requests


def getStartTime():
    url = 'https://www.douyu.com/swf_api/h5room/501761'
    html = requests.get(url).json()
    print(html['data']['show_time'])
    time_local = time.localtime(int(html['data']['show_time']))
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    print(dt)
getStartTime()

print(datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
