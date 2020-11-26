from typing import Any, Dict, List, Tuple

from django import forms

DEFAULT_PERMISSIONS = ("add", "change", "delete", "view")


class PermissionSelectMultipleWidget(forms.CheckboxSelectMultiple):
    """
    A Widget for displaying all permissions in system.

    forms.py::

        from jnt_admin_tools.widgets import PermissionSelectMultipleWidget
        from django import forms
        from django.contrib.auth.models import Group

        class GroupAdminForm(forms.ModelForm):
            class Meta:
                model = Group
                fields = '__all__'
                widgets = {
                    'permissions': PermissionSelectMultipleWidget
                }

    admin.py::

        from django.contrib import admin
        from django.contrib.auth.models import Group
        from test_app.forms import GroupAdminForm

        @admin.register(Group)
        class GroupAdmin(admin.ModelAdmin):
            form = GroupAdminForm

    .. image:: images/widgets/permission_select_multiple_widget.png
    """

    class Media:
        css = {
            "all": ("jnt_admin_tools/css/widgets/permissions.css",),
        }

    template_name = "jnt_admin_tools/widgets/permissions.html"
    custom_permission_types: List[str] = []
    groups_permissions: List[str] = []
    extra_data: Dict[str, Any] = {}

    def get_context(self, name, value, attrs):
        if value is None:
            value = []

        context = {
            "name": name,
            "value": value,
            "table": self.get_table(),
            "groups_permissions": self.groups_permissions,
            "default_permission_types": DEFAULT_PERMISSIONS,
            "custom_permission_types": self.custom_permission_types,
            "is_readonly": False,
        }
        context.update(self.extra_data)

        return context

    def get_table(self):
        table = []
        row = None
        last_app = None
        last_model = None

        for permission in self.choices.queryset.select_related(
            "content_type",
        ).all():
            model_part = "_{0}".format(permission.content_type.model)
            permission_type = permission.codename
            if permission_type.endswith(model_part):
                permission_type = permission_type[: -len(model_part)]

            app_label = permission.content_type.app_label
            app = app_label.replace("_", " ")
            model_class = permission.content_type.model_class()
            model_verbose_name = (
                model_class._meta.verbose_name if model_class else None
            )
            model_class_name = (
                model_class._meta.model_name if model_class else None
            )

            all_permissions = list(DEFAULT_PERMISSIONS) + list(
                self.custom_permission_types,
            )

            if permission_type not in all_permissions:
                self.custom_permission_types.append(permission_type)

            is_app_or_model_different = (
                last_model != model_class or last_app != app
            )
            if is_app_or_model_different:
                row = {
                    "model": model_verbose_name,
                    "model_class": model_class,
                    "model_class_name": model_class_name,
                    "app": app,
                    "app_label": app_label,
                    "permissions": {},
                }

            row["permissions"][permission_type] = permission

            if is_app_or_model_different:
                table.append(row)

            last_app = app
            last_model = model_class

        return table
