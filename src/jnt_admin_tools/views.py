from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import Http404, JsonResponse
from django.utils.text import capfirst
from django.urls import reverse
from jnt_admin_tools.services.urls import admin_autocomplete_url


class ContentTypeAutocompleteView(AutocompleteJsonView):
    # copied from base class
    def get(self, request, *args, **kwargs):
        if not self.model_admin.get_search_fields(request):
            msg_template = (
                "{0} must have search_fields for the autocomplete_view."
            )
            raise Http404(msg_template.format(type(self.model_admin).__name__))
        if not self.has_perm(request):
            return JsonResponse({"error": "403 Forbidden"}, status=403)

        self.term = request.GET.get("term", "")
        self.paginator_class = self.model_admin.paginator
        self.object_list = self.filter_queryset(self.get_queryset())
        context = self.get_context_data()

        return JsonResponse(
            {
                "results": [
                    {
                        "id": str(content_type.pk),
                        "text": capfirst(content_type.model),
                        # modify
                        "autocomplete_url": self.get_autocomplete_url(
                            content_type
                        ),
                        "data_app": content_type.app_label,
                        "data_model": content_type.model,
                        "data_change_url": self._get_change_url_template(
                            content_type
                        ),
                    }
                    for content_type in context["object_list"]
                ],
                "pagination": {"more": context["page_obj"].has_next()},
            }
        )

    def get_autocomplete_url(self, content_type):
        return admin_autocomplete_url(content_type.model_class())

    def filter_queryset(self, queryset):
        return self._filter_queryset_by_ids(queryset)

    def _filter_queryset_by_ids(self, queryset):
        ids = self.request.GET.getlist("ids[]")
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset

    def _get_change_url_template(self, content_type):
        list_url = reverse(
            "admin:{0}_{1}_changelist".format(
                content_type.app_label,
                content_type.model,
            ),
        )
        return "{0}{{id}}/change/".format(list_url)
