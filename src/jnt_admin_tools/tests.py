import warnings
from unittest import TestCase

from jnt_admin_tools import menu
from jnt_admin_tools.dashboard import dashboards, modules


class DeprecationTest(TestCase):
    def assertDeprecated(self, cls, *args, **kwargs):
        if hasattr(warnings, "catch_warnings"):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                cls(*args, **kwargs)

                assert len(w) == 1
                assert issubclass(w[-1].category, DeprecationWarning)
                assert "deprecated" in str(w[-1].message)

    def assertNotDeprecated(self, cls, *args, **kwargs):
        if hasattr(warnings, "catch_warnings"):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                cls(*args, **kwargs)
                assert len(w) == 0

    def test_dashboard(self):
        from jnt_admin_tools.dashboard import models

        self.assertDeprecated(models.Dashboard)
        self.assertDeprecated(models.DefaultIndexDashboard)
        self.assertDeprecated(models.DefaultAppIndexDashboard, "", [])
        self.assertDeprecated(models.AppIndexDashboard, "", [])

        self.assertDeprecated(models.DashboardModule)
        self.assertDeprecated(models.AppListDashboardModule)
        self.assertDeprecated(models.ModelListDashboardModule)
        self.assertDeprecated(models.LinkListDashboardModule)
        self.assertDeprecated(models.FeedDashboardModule)

    def test_dashboard_new(self):
        self.assertNotDeprecated(dashboards.Dashboard)
        self.assertNotDeprecated(dashboards.DefaultIndexDashboard)
        self.assertNotDeprecated(dashboards.DefaultAppIndexDashboard, "", [])
        self.assertNotDeprecated(dashboards.AppIndexDashboard, "", [])

        self.assertNotDeprecated(modules.DashboardModule)
        self.assertNotDeprecated(modules.AppList)
        self.assertNotDeprecated(modules.ModelList)
        self.assertNotDeprecated(modules.LinkList)
        self.assertNotDeprecated(modules.Feed)

    def test_menu(self):
        from jnt_admin_tools.menu import models  # noqa: WPS458

        self.assertDeprecated(models.Menu)
        self.assertDeprecated(models.DefaultMenu)
        self.assertDeprecated(models.MenuItem)
        self.assertDeprecated(models.AppListMenuItem)
        self.assertDeprecated(models.BookmarkMenuItem)

    def test_menu_new(self):
        self.assertNotDeprecated(menu.Menu)
        self.assertNotDeprecated(menu.DefaultMenu)

        self.assertNotDeprecated(menu.items.MenuItem)
        self.assertNotDeprecated(menu.items.AppList)
        self.assertNotDeprecated(menu.items.Bookmarks)
