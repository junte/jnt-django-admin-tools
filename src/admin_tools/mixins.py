from admin_tools.checks import AutoCompleteModelAdminChecks
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import ForeignKey, ManyToManyField


class AdminAutocompleteFieldsMixin:
    checks_class = AutoCompleteModelAdminChecks

    def get_autocomplete_fields(self, request):
        autocomplete_fields = super().get_autocomplete_fields(request)

        if autocomplete_fields:
            return autocomplete_fields

        admin_fields = self._get_admin_fields(request)
        relation_fields = self._get_relation_fields()

        if not admin_fields:
            return tuple(relation_fields)

        return tuple(set(admin_fields) & set(relation_fields))

    def _get_relation_fields(self):
        return (
            field.name
            for field in self.model._meta.get_fields()
            if self.is_relation_field(field)
        )

    def _get_admin_fields(self, request):
        if self.fields:
            return self.get_fields(request)
        elif self.fieldsets:
            return flatten_fieldsets(self.get_fieldsets(request))

    def is_relation_field(self, field):
        return isinstance(field, (ForeignKey, ManyToManyField)) and self.is_registered_model(field.remote_field.model)

    def is_registered_model(self, model):
        return bool(self.admin_site._registry.get(model))
