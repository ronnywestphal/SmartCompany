from django.apps import AppConfig
from threading import Thread

class TestThread(Thread):

    def run(self):
        from mqtt_sub import main as subs
        print('Thread running')
        subs()


class AutomationConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'automation'

    def ready(self):
        TestThread().start()
