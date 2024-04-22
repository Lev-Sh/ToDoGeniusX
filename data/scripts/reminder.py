import random
import time
from threading import Thread

import schedule


class Reminder:
    with open('data/files/notification_samples.txt', 'r', encoding='utf-8') as samples:
        SAMPLES = list(map(str.rstrip, samples.readlines()))

    def __init__(self):
        pass

    def create_remind(self):
        notif_text = random.choice(self.SAMPLES)

        notif_text = notif_text.replace('{hobby_sample}', '')\
            if '{hobby_sample}' in notif_text else notif_text
        notif_text = notif_text.replace('{user_name}', '')\
            if '{user_name}' in notif_text else notif_text
        # print(notif_text)

    @staticmethod
    def reminder_checker():
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_reminder(self, await_time):
        schedule.every(await_time).hours.do(self.create_remind)
        reminder_thread = Thread(target=self.reminder_checker, daemon=True)
        reminder_thread.start()
