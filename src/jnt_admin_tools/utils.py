"""
Admin ui common utilities.
"""
from fnmatch import fnmatch
from importlib import import_module

from django.conf import settings
from django.contrib import admin
from django.urls import reverse


def uniquify(value, seen_values):
    """Adds value to seen_values set and ensures it is unique"""
    index = 1
    new_value = value
    while new_value in seen_values:
        new_value = "{0}{1}".format(value, index)
        index += 1
    seen_values.add(new_value)
    return new_value


def get_admin_site(context=None, request=None):
    dashboard_cls = getattr(
        settings,
        "ADMIN_TOOLS_INDEX_DASHBOARD",
        "jnt_admin_tools.dashboard.dashboards.DefaultIndexDashboard",
    )

    if isinstance(dashboard_cls, dict):
        if context:
            request = context.get("request")
        curr_url = request.path
        for key in dashboard_cls:
            mod, inst = key.rsplit(".", 1)
            mod = import_module(mod)
            admin_site = getattr(mod, inst)
            admin_url = reverse("%s:index" % admin_site.name)
            if curr_url.startswith(admin_url):
                return admin_site
    else:
        return admin.site
    raise ValueError('Admin site matching "%s" not found' % dashboard_cls)


def get_admin_site_name(context):
    return get_admin_site(context).name


def get_avail_models(request):
    """Returns (model, perm,) for all models user can possibly see"""
    items = []
    admin_site = get_admin_site(request=request)

    for model, model_admin in admin_site._registry.items():
        has_module_perms = model_admin.has_module_permission(request)
        if not has_module_perms:
            continue

        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        items.append(
            (
                model,
                perms,
            )
        )
    return items


def filter_models(request, models, exclude):
    """
    Returns (model, perm,) for all models that match models/exclude patterns
    and are visible by current user.
    """
    items = get_avail_models(request)
    included = []

    def full_name(model):
        return "{0}.{1}".format(model.__module__, model.__name__)

    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.

    if models:
        for pattern in models:
            wildcard_models = []
            for item in items:
                model, perms = item
                model_str = full_name(model)
                if model_str == pattern:
                    # exact match
                    included.append(item)
                elif (
                    fnmatch(model_str, pattern) and item not in wildcard_models
                ):
                    # wildcard match, put item in separate list so it can be
                    # sorted alphabetically later
                    wildcard_models.append(item)
            if wildcard_models:
                # sort wildcard matches alphabetically before adding them
                wildcard_models.sort(
                    key=lambda x: x[0]._meta.verbose_name_plural
                )
                included += wildcard_models
    else:
        included = items

    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                try:
                    result.remove(item)
                except ValueError:  # if the item was already removed skip
                    pass
    return result


class AppListElementMixin:
    """
    Mixin class used by both the AppListDashboardModule and the
    AppListMenuItem (to honor the DRY concept).
    """

    def _visible_models(self, request):
        # compatibility layer: generate models/exclude patterns
        # from include_list/exclude_list args
        return filter_models(request, self.models[:], self.exclude[:])

    def _get_admin_app_list_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse(
            "{0}:app_list".format(get_admin_site_name(context)),
            args=(app_label,),
        )

    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse(
            "{0}:{1}_{2}_changelist".format(
                get_admin_site_name(context),
                app_label,
                model.__name__.lower(),
            )
        )

    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse(
            "{0}:{1}_{2}_add".format(
                get_admin_site_name(context),
                app_label,
                model.__name__.lower(),
            )
        )
