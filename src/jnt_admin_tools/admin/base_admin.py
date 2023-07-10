from django.contrib import admin
from django.forms import forms
from django.http import HttpResponse
from django.template.response import TemplateResponse
from jnt_django_toolbox.admin.mixins import (
    ClickableLinksAdminMixin,
    AutocompleteFieldsAdminMixin,
)

from jnt_admin_tools.admin.mixins import (
    AdminToolsMixin,
    ChangeFormSubmitsMixin,
)


class BaseModelAdmin(
    AutocompleteFieldsAdminMixin,
    ClickableLinksAdminMixin,
    AdminToolsMixin,
    ChangeFormSubmitsMixin,
    admin.ModelAdmin,
):
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        self._add_changelist_media(response)

        return response

    def _add_changelist_media(self, response: HttpResponse) -> None:
        """Add filters media."""
        if not isinstance(response, TemplateResponse):
            return

        cl_context = response.context_data.get("cl")

        if not cl_context or not cl_context.has_filters:
            return

        for filter_spec in response.context_data["cl"].filter_specs:
            media = self._get_filter_media(filter_spec)
            if media:
                response.context_data["media"] = (
                    media + response.context_data["media"]
                )

    def _get_filter_media(self, filter_spec) -> forms.Media | None:
        media_property = getattr(filter_spec, "media", None)
        media_class = getattr(filter_spec, "Media", None)

        media = forms.Media()

        if media_property:
            media += media_property

        if media_class:
            media += forms.Media(
                js=getattr(media_class, "js", []),
                css=getattr(media_class, "css", {}),
            )

        return media
