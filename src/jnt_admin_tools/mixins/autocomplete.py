from jnt_admin_tools.mixins import (
    AutocompleteChangelistFiltersAdminMixin,
    AutocompleteFieldsAdminMixin,
)


class AutocompleteAdminMixin(
    AutocompleteFieldsAdminMixin,
    AutocompleteChangelistFiltersAdminMixin,
):
    """Autocomplete model admin."""
