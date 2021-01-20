from itertools import chain

from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.admin.utils import flatten_fieldsets
from django.db.models import ForeignKey, ManyToManyField


class AutocompleteFieldsAdminMixin:
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
            if self._is_relation_field(field)
        )

    def _get_admin_fields(self, request):
        if self.fields:
            return self.get_fields(request)
        elif self.fieldsets:
            return flatten_fieldsets(self.get_fieldsets(request))

    def _is_relation_field(self, field):
        return isinstance(field, (ForeignKey, ManyToManyField)) and bool(
            self.admin_site._registry.get(field.remote_field.model)
        )

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_autocomplete_mixin(),
        ]

    def _check_autocomplete_mixin(self):
        if "autocomplete_fields" in self.__class__.__dict__.keys():
            return []

        check_autocomplete_fields_item = (
            BaseModelAdminChecks()._check_autocomplete_fields_item
        )

        return list(
            chain.from_iterable(
                [
                    check_autocomplete_fields_item(
                        self, field_name, f"autocomplete_fields[{index:d}]"
                    )
                    for index, field_name in enumerate(
                        self.get_autocomplete_fields(None)
                    )
                ]
            )
        )
