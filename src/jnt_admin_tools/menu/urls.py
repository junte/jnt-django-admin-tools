from django.urls import path
from jnt_admin_tools.menu import views

urlpatterns = [
    path(
        "add_bookmark/",
        views.add_bookmark,
        name="admin-tools-menu-add-bookmark",
    ),
    path(
        "edit_bookmark/<id>/",
        views.edit_bookmark,
        name="admin-tools-menu-edit-bookmark",
    ),
    path(
        "remove_bookmark/<id>/",
        views.remove_bookmark,
        name="admin-tools-menu-remove-bookmark",
    ),
]
