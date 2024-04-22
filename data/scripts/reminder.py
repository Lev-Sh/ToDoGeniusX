import datetime
import time

import schedule


def job():
    hour = datetime.datetime.now().hour
    hour %= 12
    hour = hour or 12
    print('Ку' * hour)


schedule.every().hour.at('00:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
