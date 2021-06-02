from functools import partialmethod

from django import forms

from jnt_admin_tools.mixins import GenericForeignKeyAdminMixin


class GenericForeignKeyInlineAdminMixin(GenericForeignKeyAdminMixin):
    """Generic foreign key inline admin mixin."""

    def get_formset(self, request, obj=None, **kwargs):
        """Get formset."""
        formset = super().get_formset(request, obj, **kwargs)

        generic_relation_fields = self._get_generic_relation_fields(self.model)
        if not generic_relation_fields:
            return formset

        for generic_relation_field in generic_relation_fields:
            if generic_relation_field.fk_field in formset.form.base_fields:
                formset.form.base_fields[
                    generic_relation_field.fk_field
                ].widget = forms.HiddenInput()

                clean_func = partialmethod(
                    self._clean_fk_field,
                    fk_field=generic_relation_field.fk_field,
                    ct_field=generic_relation_field.ct_field,
                )
                setattr(
                    formset.form,
                    "clean_{0}".format(generic_relation_field.fk_field),
                    clean_func,
                )

        return formset
