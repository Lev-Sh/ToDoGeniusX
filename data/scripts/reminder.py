import datetime
import random
import time
from threading import Thread

import schedule

from data.db_models.db_session import create_session
from data.db_models.users import User
from data.db_models.notifications import Notification

EXPIRATION_TIME = 86400


class Reminder:
    with open('data/files/notification_samples.txt', 'r', encoding='utf-8') as samples:
        SAMPLES = list(map(str.rstrip, samples.readlines()))

    def __init__(self):
        pass

    def do_notification(self):
        session = create_session()

        for i in session.query(User).values(User.id):
            i = i[0]

            notif_text = random.choice(self.SAMPLES)
            notif_text = notif_text.replace('{user_name}', session.get(User, i).nickname) \
                if '{user_name}' in notif_text else notif_text
            notification = Notification(
                user_id=i,
                notification_text=notif_text,
                creation_date=datetime.datetime.now(),
                seen=0
            )
            session.add(notification)

        session.commit()

    @staticmethod
    def delete_old_notifications():
        session = create_session()
        now = datetime.datetime.now()

        for i in session.query(Notification).values(Notification.id):
            creation_date = session.get(Notification, i[0]).creation_date
            if (now - creation_date).seconds >= EXPIRATION_TIME:
                session.delete(session.get(Notification, i[0]))

        session.commit()

    @staticmethod
    def reminder_checker():
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_reminder(self, await_time):
        schedule.every(await_time).hours.do(self.do_notification)
        schedule.every(10).minutes.do(self.delete_old_notifications)
        notifications_thread = Thread(target=self.do_notification, daemon=True)
        delete_thread = Thread(target=self.delete_old_notifications)
        reminder_thread = Thread(target=self.reminder_checker, daemon=True)

        notifications_thread.start()
        session = create_session()
        for i in session.query(Notification).values(Notification.id):
            session.delete(session.get(Notification, i[0]))
        session.commit()

        reminder_thread.start()
        delete_thread.start()
