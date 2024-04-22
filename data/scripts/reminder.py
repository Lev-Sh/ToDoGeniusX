import random
import time
from threading import Thread

import schedule
from flask_login import current_user

with open('data/files/notification_samples.txt', 'r', encoding='utf-8') as samples:
    SAMPLES = list(map(str.rstrip, samples.readlines()))


def create_remind():
    notif_text = random.choice(SAMPLES)
    notif_text = notif_text.replace('{hobby_sample}', 'Вязание') if '{hobby_sample}' in notif_text else notif_text
    notif_text = notif_text.replace('{user_name}', 'aboba') if '{user_name}' in notif_text else notif_text
    # print(notif_text)


def reminder_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)


def start_reminder(await_time):
    schedule.every(await_time).hours.do(create_remind)
    reminder_thread = Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()
