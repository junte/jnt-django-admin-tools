from itertools import chain

from admin_tools.checks import AutoCompleteModelAdminChecks
from django.db.models import ForeignKey, ManyToManyField


class AdminAutocompleteFieldsMixin:
    checks_class = AutoCompleteModelAdminChecks

    def get_autocomplete_fields(self, request):
        fields = super().get_autocomplete_fields(request)

        if fields:
            return fields

        admin_fields = self.get_admin_fields(request)
        relation_fields = self.get_relation_fields()

        if not admin_fields:
            return tuple(relation_fields)

        return tuple(set(admin_fields) & set(relation_fields))

    def get_relation_fields(self):
        def is_autocomplete(field):
            """
             (admin.E038) The value of 'autocomplete_fields' must be a foreign key or a many-to-many field.
            """
            return isinstance(field, ForeignKey) or isinstance(field, ManyToManyField)

        return (f.name for f in self.model._meta.get_fields() if is_autocomplete(f))

    def get_admin_fields(self, request):
        if self.fields:
            return self.get_fields(request)

        if self.fieldsets:
            return tuple(chain.from_iterable([x[1]['fields'] for x in self.fieldsets]))
