"""
This module contains the base classes for the dashboard and dashboard modules.
"""
from django.conf import settings
from django.db import models

# warnings for deprecated imports
from jnt_admin_tools.deprecate_utils import import_path_is_changed
from jnt_admin_tools.dashboard import dashboards
from jnt_admin_tools.dashboard import modules

user_model = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class DashboardPreferences(models.Model):
    """
    This model represents the dashboard preferences for a user.
    """

    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    data = models.TextField()
    dashboard_id = models.CharField(max_length=100)

    def __str__(self):
        return "{0} dashboard preferences".format(self.user.get_username())

    class Meta:
        db_table = "admin_tools_dashboard_preferences"
        unique_together = (
            "user",
            "dashboard_id",
        )
        ordering = ("user",)


class Dashboard(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.Dashboard",
        "jnt_admin_tools.dashboard.Dashboard",
    ),
    dashboards.Dashboard,
):
    pass


class DefaultIndexDashboard(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.DefaultIndexDashboard",
        "jnt_admin_tools.dashboard.DefaultIndexDashboard",
    ),
    dashboards.DefaultIndexDashboard,
):
    pass


class DefaultAppIndexDashboard(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.DefaultAppIndexDashboard",
        "jnt_admin_tools.dashboard.DefaultAppIndexDashboard",
    ),
    dashboards.DefaultAppIndexDashboard,
):
    pass


class AppIndexDashboard(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.AppIndexDashboard",
        "jnt_admin_tools.dashboard.AppIndexDashboard",
    ),
    dashboards.AppIndexDashboard,
):
    pass


class DashboardModule(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.DashboardModule",
        "jnt_admin_tools.dashboard.modules.DashboardModule",
    ),
    modules.DashboardModule,
):
    pass


class AppListDashboardModule(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.AppListDashboardModule",
        "jnt_admin_tools.dashboard.modules.AppList",
    ),
    modules.AppList,
):
    pass


class ModelListDashboardModule(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.ModelListDashboardModule",
        "jnt_admin_tools.dashboard.modules.ModelList",
    ),
    modules.ModelList,
):
    pass


class LinkListDashboardModule(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.LinkListDashboardModule",
        "jnt_admin_tools.dashboard.modules.LinkList",
    ),
    modules.LinkList,
):
    pass


class FeedDashboardModule(
    import_path_is_changed(
        "jnt_admin_tools.dashboard.models.FeedDashboardModule",
        "jnt_admin_tools.dashboard.modules.Feed",
    ),
    modules.Feed,
):
    pass
