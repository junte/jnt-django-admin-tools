from django.apps import AppConfig


class AdminToolsConfig(AppConfig):
    name = 'admin_tools'

    def ready(self):
        super().ready()
        # load admin_tools checks
        from . import checks # noqa: F401
