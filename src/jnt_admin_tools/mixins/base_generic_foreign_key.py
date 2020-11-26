from django import forms
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from jnt_admin_tools.db.fields import GenericForeignKey
from jnt_admin_tools.services.objects import copy_func
from jnt_admin_tools.widgets.autocomplete import ContentTypeAutocompleteSelect


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

            setattr(form, f"clean_{field.name}", _copy_func)

    def _clean_formfield(self, gfk_field):
        ct_field = self.cleaned_data.get(gfk_field.ct_field)
        fk_field = self.cleaned_data.get(gfk_field.fk_field)

        if ct_field and fk_field:
            return
        elif not ct_field and not fk_field:
            return

        msg = _("Both values must be filled or cleared")
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
        db = kwargs.get("using")
        form_field.widget = ContentTypeAutocompleteSelect(
            db_field.remote_field, self.admin_site, using=db, attrs=attrs
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
            "class": "generic-foreign-key-field",
            "data-ct--field": gfk.ct_field,
            "data-fk--field": gfk.fk_field,
            "data-gf--name": gfk.name,
            "data-gfk--models": ",".join(
                str(x) for x in self._get_gfk_ids_related_models(gfk)
            ),
        }
