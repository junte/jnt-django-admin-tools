from django.contrib import admin

from jnt_admin_tools.mixins import (
    AdminAutocompleteChangelistFiltersMixin,
    AdminAutocompleteFieldsMixin,
    ClickableLinksAdminMixin,
)


class AutocompleteAdminMixin(
    AdminAutocompleteFieldsMixin,
    AdminAutocompleteChangelistFiltersMixin,
):
    """Autocomplete model admin."""


class BaseModelAdmin(
    ClickableLinksAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
