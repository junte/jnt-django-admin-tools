from admin_tools.checks import AutoCompleteModelAdminChecks
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import ForeignKey, ManyToManyField


class AdminAutocompleteFieldsMixin(admin.ModelAdmin):
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
            if isinstance(field, (ForeignKey, ManyToManyField))
        )

    def _get_admin_fields(self, request):
        if self.fields:
            return self.get_fields(request)

        if self.fieldsets:
            return flatten_fieldsets(self.get_fieldsets(request))
