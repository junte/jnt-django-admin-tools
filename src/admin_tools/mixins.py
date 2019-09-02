from itertools import chain

from admin_tools.db.fields import GenericForeignKey
from admin_tools.services.objects import copy_func
from admin_tools.widgets.autocomplete import ContentTypeAutocompleteSelect
from django import forms
from django.contrib.admin.checks import BaseModelAdminChecks
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.contenttypes.models import ContentType
from django.db.models import ForeignKey, ManyToManyField
from django.utils.translation import gettext_lazy as _


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
                and bool(
                self.admin_site._registry.get(field.remote_field.model)))

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
            check_autocomplete_fields_item(self, field_name,
                                           f'autocomplete_fields[{index:d}]')
            for index, field_name in
            enumerate(self.get_autocomplete_fields(None))
        ]))


class BaseGenericForeignKeyMixin:
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if fields:
            fields = self._update_gfk_fields(fields)

        return fields

    def _update_gfk_fields(self, fields):
        gfk_fields = self._get_generic_foreign_keys(self.model)

        if not gfk_fields:
            return fields

        gfk_map = {f.name: f for f in gfk_fields}

        updated = []
        for field in fields:
            gfk = gfk_map.get(field)

            if not (gfk and isinstance(self, InlineModelAdmin)):
                updated = self._append_value(updated, field)

            if gfk:
                updated = self._append_value(updated, gfk.ct_field)
                updated = self._append_value(updated, gfk.fk_field)

        return tuple(updated)

    def _get_generic_foreign_keys(self, model):
        return [
            f
            for f in model._meta.get_fields()
            if isinstance(f, GenericForeignKey)
        ]

    def _append_value(self, fields, value):
        if value not in fields:
            fields.append(value)
        return fields

    def _set_validators_gfk(self, form):
        for field in self._get_generic_foreign_keys(self.model):
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

        msg = _('Both values must be filled or cleared')
        self.add_error(gfk_field.ct_field, msg)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        generic_foreign_keys = self._get_generic_foreign_keys(self.model)

        is_gfk, gfk = self._is_generic_foreign_key(
            db_field.name, generic_foreign_keys
        )

        form_field = super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        if not is_gfk:
            return form_field

        attrs = self._get_content_type_autocomplete_attrs(gfk)
        db = kwargs.get('using')
        form_field.widget = ContentTypeAutocompleteSelect(
            db_field.remote_field,
            self.admin_site,
            using=db,
            attrs=attrs
        )

        return form_field

    def _get_gfk_ids_related_models(self, gfk):
        related_models = gfk.get_related_models()

        content_types = ContentType.objects.get_for_models(*related_models)

        return [x.id for x in content_types.values()]

    def _set_declared_gfk_to_form(self, form):
        for field in self._get_generic_foreign_keys(self.model):
            form_char_field = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
            )

            form.declared_fields[field.name] = form_char_field

    def _is_generic_foreign_key(self, field_name, generic_foreign_keys):
        for gfk in generic_foreign_keys:
            if field_name in (gfk.name, gfk.ct_field, gfk.fk_field):
                return True, gfk
        return False, None

    def _get_content_type_autocomplete_attrs(self, gfk):
        return {
            'class': 'generic-foreign-key-field',
            'data-ct--field': gfk.ct_field,
            'data-fk--field': gfk.fk_field,
            'data-gf--name': gfk.name,
            'data-gfk--models': ','.join(
                str(x) for x in self._get_gfk_ids_related_models(gfk)
            )
        }


class GenericForeignKeyInlineAdminMixin(BaseGenericForeignKeyMixin):
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        self._set_declared_gfk_to_form(formset.form)
        self._set_validators_gfk(formset.form)

        return formset


class GenericForeignKeyAdminMixin(BaseGenericForeignKeyMixin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)

        if fieldsets:
            fieldsets = self._update_gfk_fieldsets(fieldsets)

        return fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        self._set_declared_gfk_to_form(self.form)
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        self._set_present_gfk(form, obj)
        self._set_validators_gfk(form)

        return form

    def _set_present_gfk(self, form, obj):
        for field in self._get_generic_foreign_keys(self.model):
            if field.fk_field in form.base_fields:
                form.base_fields[field.fk_field].widget.attrs[
                    'data-present'] = str(getattr(obj, field.name, ''))

    def get_inline_formsets(self, request, formsets, inline_instances,
                            obj=None):
        self.set_present_for_inlines(request, formsets, inline_instances, obj)

        return super().get_inline_formsets(
            request, formsets, inline_instances, obj=obj
        )

    def set_present_for_inlines(self, request, formsets, inline_instances, obj):
        for formset, inline in zip(formsets, inline_instances):
            generic_foreign_keys = self._get_generic_foreign_keys(formset.model)

            if not generic_foreign_keys:
                continue

            inline_fields = inline.get_fields(request, obj)

            for form in formset.forms:
                for gfk in generic_foreign_keys:
                    if gfk.ct_field not in inline_fields:
                        continue

                    form.fields[gfk.fk_field].widget.attrs[
                        'data-present'] = str(
                        getattr(form.instance, gfk.name, ''))

    def _update_gfk_fieldsets(self, fieldsets):
        gfk_fields = self._get_generic_foreign_keys(self.model)

        if not gfk_fields:
            return fieldsets

        for fieldset in fieldsets:
            fields = fieldset[1].get('fields')
            if fields:
                fieldset[1]['fields'] = self._update_gfk_fields(fields)
        return fieldsets
