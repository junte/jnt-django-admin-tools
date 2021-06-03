from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import Http404, JsonResponse
from django.utils.text import capfirst

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
                        "id": str(obj.pk),
                        "text": capfirst(obj.model),
                        # modify
                        "autocompleteUrl": self.get_autocomplete_ul(obj),
                    }
                    for obj in context["object_list"]
                ],
                "pagination": {"more": context["page_obj"].has_next()},
            }
        )

    def get_autocomplete_ul(self, content_type):
        return admin_autocomplete_url(content_type.model_class())

    def filter_queryset(self, queryset):
        return self._filter_queryset_by_ids(queryset)

    def _filter_queryset_by_ids(self, queryset):
        ids = self.request.GET.getlist("ids[]")
        if ids:
            queryset = queryset.filter(id__in=ids)
        return queryset
