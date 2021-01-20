from django.contrib import admin

from jnt_admin_tools.mixins import (
    AdminAutocompleteChangelistFiltersMixin,
    AdminAutocompleteFieldsMixin,
    AdminClickableLinksMixin,
)


class AutocompleteBaseModelAdminMixin(
    AdminAutocompleteFieldsMixin,
    AdminAutocompleteChangelistFiltersMixin,
):
    """Autocomplete model admin."""


class BaseModelAdmin(
    AdminClickableLinksMixin,
    AutocompleteBaseModelAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
