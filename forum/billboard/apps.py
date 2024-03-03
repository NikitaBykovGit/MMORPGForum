from django.apps import AppConfig


class BillboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billboard'

    def ready(self):
        from . import signals