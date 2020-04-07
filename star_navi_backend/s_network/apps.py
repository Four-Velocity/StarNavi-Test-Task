from django.apps import AppConfig


class SNetworkConfig(AppConfig):
    name = 's_network'

    def ready(self):
        import s_network.signals
