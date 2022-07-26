from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

admin.site.site_header = "Django admin tools demo"
admin.site.site_title = "Django admin tools demo"
admin.site.index_title = "Welcome to Django admin tools demo"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin_tools/", include("jnt_admin_tools.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
