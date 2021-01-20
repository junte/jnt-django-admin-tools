from django.contrib import admin

from jnt_admin_tools.mixins import (
    AutocompleteChangelistFiltersMixinAdmin,
    AutocompleteFieldsAdminMixin,
    ClickableLinksAdminMixin,
)


class AutocompleteAdminMixin(
    AutocompleteFieldsAdminMixin,
    AutocompleteChangelistFiltersMixinAdmin,
):
    """Autocomplete model admin."""


class BaseModelAdmin(
    ClickableLinksAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
