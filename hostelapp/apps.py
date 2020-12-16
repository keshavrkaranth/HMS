from django.apps import AppConfig


class HostelappConfig(AppConfig):
    name = 'hostelapp'

    def ready(self):
        import hostelapp.trigger
