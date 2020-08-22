from django.apps import AppConfig

class EshopConfig(AppConfig):
    name = 'eshop'

    def ready(self):
        import eshop.signals
