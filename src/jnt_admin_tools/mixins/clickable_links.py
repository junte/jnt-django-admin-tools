from django.contrib.admin.helpers import AdminReadonlyField

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
    def get_list_display(self, *args, **kwargs):
        list_display = super().get_list_display(*args, **kwargs)

        updated_list = [list_display[0]]
        updated_list.extend(
            [
                self._update_column_field(column_field)
                for column_field in list_display[1:]
            ],
        )

        return tuple(updated_list)

    def _update_column_field(self, column_field):
        readonly_widget = self.readonly_widget(column_field)
        if not readonly_widget:
            return column_field

        return AdminChangeListField(
            model_admin=self,
            field_name=column_field,
            readonly_widget=readonly_widget,
        )
