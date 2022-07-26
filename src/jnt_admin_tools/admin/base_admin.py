from django.contrib import admin
from jnt_django_toolbox.admin.mixins import (
    ClickableLinksAdminMixin,
    AutocompleteFieldsAdminMixin,
)

from jnt_admin_tools.admin.mixins import (
    AdminToolsMixin,
    ChangeFormSubmitsMixin,
)


class BaseModelAdmin(
    AutocompleteFieldsAdminMixin,
    ClickableLinksAdminMixin,
    AdminToolsMixin,
    ChangeFormSubmitsMixin,
    admin.ModelAdmin,
):
    pass
