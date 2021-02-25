from django.contrib import admin

from jnt_admin_tools.mixins import ClickableLinksAdminMixin
from jnt_admin_tools.mixins.autocomplete import AutocompleteAdminMixin


class BaseModelAdmin(
    ClickableLinksAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
):
    """Base model admin."""
