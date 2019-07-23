from itertools import chain

from admin_tools.db.fields import GenericForeignKey
from admin_tools.services.objects import copy_func
from admin_tools.widgets.autocomplete import AutocompleteSelect
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, ManyToManyField
from django import forms


class AdminAutocompleteFieldsMixin:
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
        return (isinstance(field, (ForeignKey, ManyToManyField))
                and bool(self.admin_site._registry.get(field.remote_field.model)))

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_autocomplete_mixin(),
        ]

    def _check_autocomplete_mixin(self):
        if 'autocomplete_fields' in self.__class__.__dict__.keys():
            return []

        check_autocomplete_fields_item = BaseModelAdminChecks()._check_autocomplete_fields_item

        return list(chain.from_iterable([
            check_autocomplete_fields_item(self, field_name, f'autocomplete_fields[{index:d}]')
            for index, field_name in enumerate(self.get_autocomplete_fields(None))
        ]))


class GenericForeignKeyMixin:
    def get_form(self, request, obj=None, change=False, **kwargs):
        self.set_present_gfk(obj)
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        self.set_validators_gfk(form)

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        generic_foreign_keys = self.get_generic_foreign_keys()

        is_gfk, gfk = self.is_generic_foreign_key(
            db_field.name, generic_foreign_keys
        )

        form_field = super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        if not is_gfk:
            return form_field

        attrs = {
            'class': 'generic-foreign-key-field',
            'data-ct--field': gfk.ct_field,
            'data-fk--field': gfk.fk_field,
            'data-gf--name': gfk.name,
            'data-gfk--models': ','.join(
                str(x) for x in self.get_gfk_ids_related_models(gfk)
            )
        }
        db = kwargs.get('using')
        form_field.widget = AutocompleteSelect(
            db_field.remote_field,
            self.admin_site,
            using=db,
            attrs=attrs
        )

        return form_field

    def get_generic_foreign_keys(self):
        return [f for f in self.model._meta.get_fields() if
                isinstance(f, GenericForeignKey)]

    def is_generic_foreign_key(self, field_name, generic_foreign_keys):
        for gfk in generic_foreign_keys:
            if field_name in [gfk.name, gfk.ct_field, gfk.fk_field]:
                return True, gfk
        return False, None

    def get_gfk_ids_related_models(self, gfk):
        related_models = gfk.get_related_models()

        content_types = ContentType.objects.get_for_models(*related_models)

        return [x.id for x in content_types.values()]

    def set_present_gfk(self, obj):
        for field in self.get_generic_foreign_keys():
            field_name = field.name
            init_value = str(getattr(obj, field.name, ''))

            form_integer_field = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
                initial=init_value
            )

            self.form.declared_fields[field_name] = form_integer_field

    def set_validators_gfk(self, form):
        for field in self.get_generic_foreign_keys():
            _copy_func = copy_func(self._clean_formfield)
            _copy_func.__defaults__ = (field,)

            setattr(form, f'clean_{field.name}', _copy_func)

    def _clean_formfield(self, gfk_field):
        ct_field = self.cleaned_data.get(gfk_field.ct_field)
        fk_field = self.cleaned_data.get(gfk_field.fk_field)

        if ct_field and fk_field:
            return
        elif not ct_field and not fk_field:
            return

        msg = 'Both values must be filled or cleared'
        self.add_error(gfk_field.ct_field, msg)
