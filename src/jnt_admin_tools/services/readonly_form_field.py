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
            field_name, instance, model_admin
        )
        if field is None:
            field = instance._meta.get_field(field_name)
    except (AttributeError, ValueError, ObjectDoesNotExist, FieldDoesNotExist):
        return None

    present = _get_from_readonly_widget(
        model_admin,
        field_name,
        field_value,
    )

    if present:
        return present

    if isinstance(field_value, str):
        if getattr(field, "choices", None):
            field_value = _get_choice_present(field, field_value)
        return field_value

    if field.is_relation:
        return _get_display_relation(field, field_value)

    return None


def _get_from_readonly_widget(
    model_admin, field_name, field_value
) -> Optional[str]:
    if not model_admin:
        return None

    formfield = model_admin.form.base_fields.get(field_name)

    if not formfield:
        return None

    readonly_widgets = getattr(
        model_admin.form.Meta,
        "readonly_widgets",
        {},
    )
    readonly_widget = readonly_widgets.get(field_name)

    if not readonly_widget:
        readonly_widget = getattr(formfield, "readonly_widget", None)

    if readonly_widget:
        return readonly_widget(formfield=formfield).render(
            field_name, field_value
        )

    return None


def _get_display_relation(field, instance) -> Optional[str]:
    if not instance:
        return None

    if isinstance(field, GenericForeignKey):
        return get_display_for_gfk(instance)
    elif field.many_to_many or field.one_to_many:
        return get_display_for_many(instance.all())

    return object_change_link(instance)


def _get_choice_present(field: models.CharField, field_value: str) -> str:
    """Get present for choice."""
    choice = [
        present
        for choice_value, present in field.choices
        if choice_value == field_value
    ]

    if choice:
        field_value = choice[0]

    return field_value
