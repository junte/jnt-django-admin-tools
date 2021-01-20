from django.contrib import admin

from jnt_admin_tools.mixins import (
    AutocompleteChangelistFiltersAdminMixin,
    AutocompleteFieldsAdminMixin,
    ClickableLinksAdminMixin,
)


class AutocompleteAdminMixin(
    AutocompleteFieldsAdminMixin,
    AutocompleteChangelistFiltersAdminMixin,
):
    """Autocomplete model admin."""


class BaseModelAdmin(
    ClickableLinksAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
