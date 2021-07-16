from typing import Tuple

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.urls import NoReverseMatch
from django.utils.html import format_html

from jnt_admin_tools.services.objects import copy_func
from jnt_admin_tools.services.urls import admin_change_url

EMPTY_VALUE = "-"


def add_object_link_present_function(model_admin, field_name):
    field = "_{0}_object_link".format(field_name)

    copied_func = copy_func(_get_display_related_field)
    copied_func.__defaults__ = (field_name,)

    setattr(model_admin, field, copied_func)
    getattr(model_admin, field).__dict__.update(
        {"short_description": _get_short_description(model_admin, field_name)},
    )
    return format_html(field)


def object_change_link(obj, empty_description="-", field_present=None) -> str:
    if not obj:
        return empty_description

    obj_present = str(getattr(obj, field_present) if field_present else obj)

    try:
        return format_html(
            '<a href="{0}">{1}</a>',
            admin_change_url(obj),
            obj_present,
        )
    except NoReverseMatch:
        return "{0} (id: {1})".format(obj, obj.id)


def _parse_list_field_attr(attr) -> Tuple[str, str]:
    unpack_attr = attr.split("__")
    return unpack_attr[0], unpack_attr[1] if len(unpack_attr) > 1 else None


def get_display_for_gfk(obj) -> str:
    if not obj:
        return None

    return format_html(
        '<span class="gfk-object-type">{0}</span> {1}'.format(
            obj._meta.model_name,
            object_change_link(obj),
        ),
    )


def _get_display_related_field(target_obj, attr):
    attr, field_name = _parse_list_field_attr(attr)

    obj = getattr(target_obj, attr, None)

    if not obj:
        return format_html(EMPTY_VALUE)

    model_field = target_obj._meta.get_field(attr)

    if model_field.many_to_many or model_field.one_to_many:
        return get_display_for_many(obj.all(), field_name)
    elif isinstance(model_field, GenericForeignKey):
        return get_display_for_gfk(obj)

    return object_change_link(obj)


def get_display_for_many(objects, field_present=None) -> str:
    if not objects.exists():
        return EMPTY_VALUE

    return format_html(
        ", ".join(
            map(
                object_change_link,
                (
                    getattr(instance, field_present)
                    if field_present
                    else instance
                    for instance in objects
                ),
            ),
        ),
    )


def _get_short_description(model_admin, field_name) -> str:
    """Get verbose name for target field."""
    default_present = field_name.split("__")[-1].replace("_", " ")
    try:
        field = model_admin.model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return default_present

    return getattr(field, "verbose_name", default_present)
