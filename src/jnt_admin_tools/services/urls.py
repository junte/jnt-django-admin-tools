from contextlib import suppress

from django.urls import reverse, NoReverseMatch


def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(f"admin:{app_label}_{model_name}_change", args=(obj.pk,))


def admin_changelist_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    return reverse(f"admin:{app_label}_{model_name}_changelist")


def admin_autocomplete_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    with suppress(NoReverseMatch):
        return reverse(f"admin:{app_label}_{model_name}_autocomplete")
