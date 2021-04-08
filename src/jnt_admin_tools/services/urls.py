from contextlib import suppress

from django.urls import reverse, NoReverseMatch


def admin_change_url(obj):
    app_label = obj._meta.app_label
    model_name = obj._meta.model.__name__.lower()
    return reverse(
        "admin:{0}_{1}_change".format(app_label, model_name),
        args=(obj.pk,),
    )


def admin_changelist_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    return reverse("admin:{0}_{1}_changelist".format(app_label, model_name))


def admin_autocomplete_url(model):
    app_label = model._meta.app_label
    model_name = model.__name__.lower()
    with suppress(NoReverseMatch):
        return reverse(
            "admin:{0}_{1}_autocomplete".format(app_label, model_name),
        )
