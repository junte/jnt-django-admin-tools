from contextlib import suppress

from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.http import Http404, JsonResponse
from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst


class ContentTypeAutocompleteView(AutocompleteJsonView):
    def get(self, request, *args, **kwargs):
        if not self.model_admin.get_search_fields(request):
            raise Http404(
                '%s must have search_fields for the autocomplete_view.' %
                type(self.model_admin).__name__
            )
        if not self.has_perm(request):
            return JsonResponse({'error': '403 Forbidden'}, status=403)

        self.term = request.GET.get('term', '')
        self.paginator_class = self.model_admin.paginator
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse({
            'results': [
                {
                    'id': str(obj.pk),
                    'text': capfirst(obj.model),
                    'autocompleteUrl': self.get_autocomplete_ul(obj)
                }
                for obj in context['object_list']
            ],
            'pagination': {'more': context['page_obj'].has_next()},
        })

    def get_queryset(self):
        queryset = super().get_queryset()

        ids = self.request.GET.get('ids')

        if ids:
            queryset = queryset.filter(
                id__in=[int(x) for x in ids.split(',')]
            )

        return queryset

    def get_autocomplete_ul(self, content_type):
        url_name = 'admin:%s_%s_autocomplete'
        meta = content_type.model_class()._meta

        with suppress(NoReverseMatch):
            return reverse(url_name % (meta.app_label, meta.model_name))
        return ''
