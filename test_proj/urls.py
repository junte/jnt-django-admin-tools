from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url("^admin/", admin.site.urls),
    url("^jnt_admin_tools/", include("jnt_admin_tools.urls")),
    url(
        "^static/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}
    ),
]
