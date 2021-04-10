from django.template.response import TemplateResponse


class AutocompleteChangelistFiltersAdminMixin:
    def changelist_view(self, request, extra_context=None) -> TemplateResponse:
        changelist_view = super().changelist_view(
            request, extra_context=extra_context
        )
        self._update_changelist_media(changelist_view)
        return changelist_view

    def _update_changelist_media(
        self,
        changelist_view: TemplateResponse,
    ) -> None:
        try:
            context_data = changelist_view.context_data
        except AttributeError:
            return
        else:
            if "cl" not in context_data:
                return

        for filter_spec in changelist_view.context_data["cl"].filter_specs:
            if not getattr(filter_spec, "media", None):
                continue
            changelist_view.context_data["media"] += filter_spec.media
