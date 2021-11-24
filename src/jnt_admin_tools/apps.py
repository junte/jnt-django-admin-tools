from django.apps import AppConfig


class AdminToolsConfig(AppConfig):
    name = "jnt_admin_tools"
    default = True

    def ready(self):
        super().ready()
        # load jnt_admin_tools checks
        from . import checks  # noqa: F401
