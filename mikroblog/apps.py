from django.apps import AppConfig


class MikroblogConfig(AppConfig):
    name = 'mikroblog'

    def ready(self):
        import mikroblog.signals
