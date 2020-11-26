from django.contrib.admin.helpers import AdminReadonlyField
from django.core.exceptions import FieldDoesNotExist

from jnt_admin_tools.services.object_links import (
    add_object_link_present_function,
)
from jnt_admin_tools.services.readonly_form_field import (
    get_present_admin_readonly_field,
)

# Patching AdminReadonlyField
orig_contents = AdminReadonlyField.contents


def contents(self):
    return get_present_admin_readonly_field(self) or orig_contents(self)


AdminReadonlyField.contents = contents


class AdminClickableLinksMixin:
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return self._updating_list_display(list_display, request)

    def _updating_list_display(self, list_display, request):
        if len(list_display) < 2:
            return list_display

        list_display_links = self.get_list_display_links(request, list_display)

        fields = []
        for field_name in list_display:
            is_relation = self._is_relation(
                self.model,
                field_name,
                list_display_links,
            )

            if not is_relation:
                fields.append(field_name)
                continue

            fields.append(add_object_link_present_function(self, field_name))
        return fields

    def _is_relation(self, model, field_name, list_display_links):
        field_name = field_name.split("__")[0]
        if not hasattr(model, field_name) or field_name in list_display_links:
            return False

        try:
            field = model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return False

        return any(
            (
                field.many_to_one,
                field.one_to_one,
                field.many_to_many,
                field.one_to_many,
            ),
        )
