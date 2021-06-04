from functools import partialmethod

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.template.response import TemplateResponse

from jnt_admin_tools.db.fields import GenericForeignKey
from jnt_admin_tools.widgets import GenericForeignKeyWidget
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper


class GenericForeignKeyAdminMixin:
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        self._update_gr_fields(form, obj)
        return form

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        return self._update_fields(fields)

    def get_fieldsets(self, *args, **kwargs):
        fieldsets = super().get_fieldsets(*args, **kwargs)
        for _, fieldset_fields in fieldsets:
            fieldset_fields["fields"] = self._update_fields(
                fieldset_fields["fields"]
            )
        return fieldsets

    def changeform_view(self, *args, **kwargs):
        changeform_view = super().changeform_view(*args, **kwargs)

        self._update_gfk_in_inlines(changeform_view)
        return changeform_view

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        form_field = super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )
        generic_relation_fields = self._get_generic_relation_fields(self.model)
        current_generic_field = None
        for generic_field in generic_relation_fields:
            if generic_field.ct_field == db_field.name:
                current_generic_field = generic_field
                break

        if not current_generic_field:
            return form_field

        is_required = form_field.widget.is_required
        form_field.widget = GenericForeignKeyWidget(
            db_field.remote_field,
            self.admin_site,
            using=kwargs.get("using"),
            attrs=self._get_content_type_autocomplete_attrs(
                current_generic_field
            ),
        )
        form_field.widget.is_required = is_required

        return form_field

    def _update_fields(self, fields):
        generic_relation_fields = self._get_generic_relation_fields(self.model)
        if not generic_relation_fields:
            return fields

        fields = list(fields)

        for generic_field in generic_relation_fields:
            if generic_field.name not in fields:
                continue

            if generic_field.ct_field not in fields:
                fields[
                    fields.index(generic_field.name)
                ] = generic_field.ct_field

            if generic_field.fk_field not in fields:
                fields.append(generic_field.fk_field)

            if generic_field.name in fields:
                fields.pop(fields.index(generic_field.name))

        return tuple(fields)

    def _update_gr_fields(self, form, instance) -> None:
        if not instance:
            return

        generic_relation_fields = self._get_generic_relation_fields(self.model)

        for field in generic_relation_fields:
            if (
                field.ct_field in form.base_fields
                and field.fk_field in form.base_fields
            ):
                fk_present = getattr(instance, field.name)
                fk_present = str(fk_present) if fk_present else ""
                form.base_fields[field.fk_field].widget = forms.HiddenInput(
                    attrs={
                        "data-present": fk_present,
                    },
                )
                clean_func = partialmethod(
                    self._clean_fk_field,
                    fk_field=field.fk_field,
                    ct_field=field.ct_field,
                )
                setattr(form, "clean_{0}".format(field.fk_field), clean_func)

    def _get_generic_relation_fields(self, model):
        return [
            field
            for field in model._meta.get_fields()
            if self._is_generic_relation_field(field)
        ]

    def _is_generic_relation_field(self, field) -> bool:
        return (
            not field.auto_created
            and field.is_relation
            and isinstance(field, GenericForeignKey)
        )

    def _get_content_type_autocomplete_attrs(self, generic_field):
        return {
            "class": "generic-foreign-key-field",
            "data-ct--field": generic_field.ct_field,
            "data-fk--field": generic_field.fk_field,
            "data-gf--name": generic_field.name,
            "data-gfk--models": ",".join(
                str(model_id)
                for model_id in self._get_gfk_ids_related_models(generic_field)
            ),
        }

    def _get_gfk_ids_related_models(self, gfk):
        related_models = gfk.get_related_models()

        content_types = ContentType.objects.get_for_models(*related_models)

        return [x.id for x in content_types.values()]

    def _update_gfk_in_inlines(self, changeform_view) -> None:
        if not isinstance(changeform_view, TemplateResponse):
            return
        inline_formsets = changeform_view.context_data.get(
            "inline_admin_formsets"
        )
        if not inline_formsets:
            return

        for inline_formset in inline_formsets:
            generic_fields = self._get_generic_relation_fields(
                inline_formset.opts.model
            )
            if not generic_fields:
                continue

            for inline_form in inline_formset.forms:
                instance = inline_form.instance

                for generic_field in generic_fields:
                    if generic_field.fk_field in inline_form.fields:
                        hidden_widget = inline_form.fields[
                            generic_field.fk_field
                        ].widget
                        generic_value = getattr(
                            instance, generic_field.name, ""
                        )
                        hidden_widget.attrs["data-present"] = str(
                            generic_value
                        )

    def _clean_fk_field(self, current_form, **kwargs):
        fk_value = current_form.cleaned_data[kwargs["fk_field"]]
        ct_value = current_form.cleaned_data[kwargs["ct_field"]]

        if ct_value and not fk_value:
            current_form.add_error(
                kwargs["ct_field"],
                forms.Field.default_error_messages["required"],
            )
        return fk_value
