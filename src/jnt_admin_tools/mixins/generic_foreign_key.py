from jnt_admin_tools.mixins.base_generic_foreign_key import (
    BaseGenericForeignKeyMixin,
)


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
                    "data-present"
                ] = str(getattr(obj, field.name, ""))

    def get_inline_formsets(
        self, request, formsets, inline_instances, obj=None
    ):
        self.set_present_for_inlines(request, formsets, inline_instances, obj)

        return super().get_inline_formsets(
            request, formsets, inline_instances, obj=obj
        )

    def set_present_for_inlines(
        self, request, formsets, inline_instances, obj
    ):
        for formset, inline in zip(formsets, inline_instances):
            generic_foreign_keys = self._get_generic_foreign_keys(
                formset.model
            )

            if not generic_foreign_keys:
                continue

            inline_fields = inline.get_fields(request, obj)

            for form in formset.forms:
                for gfk in generic_foreign_keys:
                    if gfk.ct_field not in inline_fields:
                        continue

                    form.fields[gfk.fk_field].widget.attrs[
                        "data-present"
                    ] = str(getattr(form.instance, gfk.name, ""))

    def _update_gfk_fieldsets(self, fieldsets):
        gfk_fields = self._get_generic_foreign_keys(self.model)

        if not gfk_fields:
            return fieldsets

        for fieldset in fieldsets:
            fields = fieldset[1].get("fields")
            if fields:
                fieldset[1]["fields"] = self._update_gfk_fields(fields)
        return fieldsets
