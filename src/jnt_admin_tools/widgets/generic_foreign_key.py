from django import forms
from django.contrib.admin.widgets import (
    AutocompleteSelect as BaseAutocompleteSelect,
)
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class GenericForeignKeyWidget(BaseAutocompleteSelect):
    template_name = "jnt_admin_tools/widgets/generic_foreign_key.html"

    @property
    def media(self):
        media = super().media

        media_js = media._js if media else []
        media_css = media._css if media else {}
        media_css["screen"] = list(media_css["screen"])
        media_css["screen"].append(
            "jnt_admin_tools/css/widgets/generic-foreign-key-field.css",
        )

        return forms.Media(
            js=tuple(
                [
                    *media_js,
                    "jnt_admin_tools/js/widgets/generic-foreign-key-field.js",
                ]
            ),
            css=media_css,
        )

    def create_option(
        self,
        name,
        value,
        label,
        selected,
        index,
        subindex=None,
        attrs=None,
    ):
        result = super().create_option(
            name,
            value,
            label,
            selected,
            index,
            subindex=subindex,
            attrs=attrs,
        )

        if value:
            self._update_attrs(result["attrs"], value)

        return result

    def _update_attrs(self, attrs, ct_id):
        current_model = ContentType.objects.get(id=ct_id).model_class()
        attrs["data-autocomplete-url"] = self.get_autocomplete_url(
            current_model,
        )
        attrs["data-app"] = current_model._meta.app_label
        attrs["data-model"] = current_model._meta.model_name
        attrs["data-change-url"] = self._get_change_url_template(current_model)

    def get_autocomplete_url(self, current_model):
        url_name = "admin:%s_%s_autocomplete"
        meta = current_model._meta

        return reverse(url_name % (meta.app_label, meta.model_name))

    def _get_change_url_template(self, current_model):
        meta = current_model._meta
        list_url = reverse(
            "admin:{0}_{1}_changelist".format(meta.app_label, meta.model_name),
        )
        return "{0}{{id}}/change/".format(list_url)
