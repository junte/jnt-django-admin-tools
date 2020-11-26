from jnt_admin_tools.mixins.base_generic_foreign_key import (
    BaseGenericForeignKeyMixin,
)


class GenericForeignKeyInlineAdminMixin(BaseGenericForeignKeyMixin):
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        self._set_declared_gfk_to_form(formset.form)
        self._set_validators_gfk(formset.form)

        return formset
