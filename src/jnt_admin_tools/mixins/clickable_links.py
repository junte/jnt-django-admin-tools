from django.contrib.admin.helpers import AdminReadonlyField
from django.http import HttpRequest

from jnt_admin_tools.admin.fields.changelist import AdminChangeListField
from jnt_admin_tools.mixins import ReadonlyWidgetsMixin
from jnt_admin_tools.services.readonly_form_field import (
    get_present_admin_readonly_field,
)

# Patching AdminReadonlyField
orig_contents = AdminReadonlyField.contents


def contents(self):
    return get_present_admin_readonly_field(self) or orig_contents(self)


AdminReadonlyField.contents = contents


class ClickableLinksAdminMixin(ReadonlyWidgetsMixin):
    def get_list_display(self, request: HttpRequest, *args, **kwargs):
        list_display = super().get_list_display(request, *args, **kwargs)

        if len(list_display) < 2:
            return list_display

        updated_list = [list_display[0]]
        updated_list.extend(
            [
                self._update_column_field(column_field, request)
                for column_field in list_display[1:]
            ],
        )

        return tuple(updated_list)

    def _update_column_field(self, column_field, request=None):
        """Update column field."""
        field_present = None
        field_name = column_field
        if "__" in field_name:
            field_name, field_present = field_name.split("__")

        readonly_widget = self.readonly_widget(field_name, request)
        if not readonly_widget:
            return column_field

        return AdminChangeListField(
            model_admin=self,
            field_name=field_name,
            readonly_widget=readonly_widget,
            field_present=field_present,
        )
