import random
from datetime import datetime
import time
from threading import Thread
import schedule


def create_remind():
    print(datetime.now())


def reminder_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def start_reminder():
    schedule.every(3).seconds.do(create_remind)
    reminder_thread = Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()
