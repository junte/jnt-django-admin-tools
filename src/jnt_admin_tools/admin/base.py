from django.contrib import admin

from jnt_admin_tools.mixins import (
    AdminAutocompleteChangelistFiltersMixin,
    AdminAutocompleteFieldsMixin,
    AdminClickableLinksMixin,
)


class AutocompleteAdminMixin(
    AdminAutocompleteFieldsMixin,
    AdminAutocompleteChangelistFiltersMixin,
):
    """Autocomplete model admin."""


class BaseModelAdmin(
    AdminClickableLinksMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
