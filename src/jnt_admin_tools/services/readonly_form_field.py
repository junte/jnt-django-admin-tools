from typing import Optional

from django.contrib.admin.utils import lookup_field
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.db import models

from jnt_admin_tools.services.object_links import (
    get_display_for_gfk,
    get_display_for_many,
    object_change_link,
)


def get_present_admin_readonly_field(  # noqa: WPS212
    admin_readonly_field,
) -> Optional[str]:
    """Get present for AdminReadonlyField."""
    field_name, instance, model_admin = (
        admin_readonly_field.field["field"],
        admin_readonly_field.form.instance,
        admin_readonly_field.model_admin,
    )

    if not instance or admin_readonly_field.is_checkbox:
        return None

    try:
        field, attr, field_value = lookup_field(
            field_name,
            instance,
            model_admin,
        )
        if field is None:
            field = instance._meta.get_field(field_name)
    except (AttributeError, ValueError, ObjectDoesNotExist, FieldDoesNotExist):
        return None

    func_readonly_widget = getattr(model_admin, "readonly_widget", None)
    if not func_readonly_widget:
        return None

    readonly_widget = func_readonly_widget(admin_readonly_field.field["field"])

    if readonly_widget:
        return readonly_widget.render(field_value, field_name, db_field=field)

    return None
