from django.urls import path
from jnt_admin_tools.dashboard import views

urlpatterns = [
    path(
        "set_preferences/<dashboard_id>/",
        views.set_preferences,
        name="admin-tools-dashboard-set-preferences",
    ),
]
