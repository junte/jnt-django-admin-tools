from django import forms
from django.contrib.admin.widgets import (
    AutocompleteSelect as BaseAutocompleteSelect,
)
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class ContentTypeAutocompleteSelect(BaseAutocompleteSelect):
    @property
    def media(self):
        media = super().media

        media_js = media._js if media else []
        media_css = media._css if media else {}

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
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        result = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )

        if value:
            url = self.get_autocomplete_url(value)
            result["attrs"]["data-autocomplete-url"] = url

        return result

    def get_autocomplete_url(self, ct_id):
        url_name = "admin:%s_%s_autocomplete"
        meta = ContentType.objects.get(id=ct_id).model_class()._meta

        return reverse(url_name % (meta.app_label, meta.model_name))
