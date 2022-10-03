from django.apps import AppConfig


class CatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.cat'

    def ready(self):
        import src.cat.signals