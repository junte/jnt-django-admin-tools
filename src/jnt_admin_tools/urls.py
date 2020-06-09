from django.conf import settings
from django.conf.urls import include
from django.urls import re_path

urlpatterns = []

if "jnt_admin_tools.menu" in settings.INSTALLED_APPS:
    urlpatterns.append(
        re_path(r"^menu/", include("jnt_admin_tools.menu.urls"))
    )

if "jnt_admin_tools.dashboard" in settings.INSTALLED_APPS:
    urlpatterns.append(
        re_path(r"^dashboard/", include("jnt_admin_tools.dashboard.urls")),
    )
