import functools
import types

from admin_tools.db.fields import GenericForeignKey
from admin_tools.decorators import admin_changelist_link, admin_field, \
    admin_link
from admin_tools.mixins import AdminAutocompleteFieldsMixin
from admin_tools.widgets.autocomplete import AutocompleteSelect
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django import forms
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Foo, Baz, Blog, Comment

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm


@admin.register(Foo)
class FooAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    list_display = ('name', 'bar_link')
    fields = ('name', 'bar', 'bar_link')
    readonly_fields = ('bar_link',)
    search_fields = ('name',)

    @admin_link('bar')
    def bar_link(self, obj):
        return obj.name


@admin.register(Bar)
class BarAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    fields = ('name', 'foos', 'custom_field')
    readonly_fields = ('foos', 'custom_field')
    search_fields = ('name',)

    @admin_changelist_link('foos', query_string=lambda bar: f'bar_id={bar.pk}')
    def foos(self, foos):
        return ', '.join(str(foo) for foo in foos.all())

    @admin_field('Custom field')
    def custom_field(self, obj):
        return mark_safe('<h1>custom field</h1>')


@admin.register(Baz)
class BazAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    pass


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    search_fields = ('model',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def get_model_perms(self, request):
        return {}

    def autocomplete_view(self, request):
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
                            'dataAutocompleteUrl': self.get_autocomplete_ul(obj)
                        }
                        for obj in context['object_list']
                    ],
                    'pagination': {'more': context['page_obj'].has_next()},
                })

            def get_queryset(self):
                queryset = super().get_queryset()

                ids = request.GET.get('ids')

                if ids:
                    queryset = queryset.filter(
                        id__in=[int(x) for x in ids.split(',')]
                    )

                return queryset

            def get_autocomplete_ul(self, content_type):
                url_name = 'admin:%s_%s_autocomplete'
                meta = content_type.model_class()._meta
                return reverse(url_name % (meta.app_label, meta.model_name))

        return ContentTypeAutocompleteView.as_view(model_admin=self)(request)


@admin.register(Blog)
class BlogAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    search_fields = ('name',)


def copy_func(f):
    g = types.FunctionType(
        f.__code__,
        f.__globals__,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__
    )
    g = functools.update_wrapper(g, f)
    return g


def clean_formfield(self, gfk_field):
    ct_field = self.cleaned_data.get(gfk_field.ct_field)
    fk_field = self.cleaned_data.get(gfk_field.fk_field)

    if ct_field and fk_field:
        return
    elif not ct_field and not fk_field:
        return

    msg = 'Both values must be filled or cleared'
    self.add_error(gfk_field.ct_field, msg)


@admin.register(Comment)
class CommentAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        self.set_hidden_gfk(obj)
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        self.set_validators_gfk(form)

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        generic_foreign_keys = self.get_generic_foreign_keys()

        is_gfk, gfk = self.is_generic_foreign_key(
            db_field.name, generic_foreign_keys
        )

        form_field = super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )

        if not is_gfk:
            return form_field

        attrs = {
            'class': 'generic-foreign-key-field',
            'data-ct--field': gfk.ct_field,
            'data-fk--field': gfk.fk_field,
            'data-gf--name': gfk.name,
            'data-gfk--models': ','.join(
                str(x) for x in self.get_gfk_ids_related_models(gfk)
            )
        }
        db = kwargs.get('using')
        form_field.widget = AutocompleteSelect(
            db_field.remote_field,
            self.admin_site,
            using=db,
            attrs=attrs
        )

        return form_field

    def get_generic_foreign_keys(self):
        return [f for f in self.model._meta.get_fields() if
                isinstance(f, GenericForeignKey)]

    def is_generic_foreign_key(self, field_name, generic_foreign_keys):
        for gfk in generic_foreign_keys:
            if field_name in [gfk.name, gfk.ct_field, gfk.fk_field]:
                return True, gfk
        return False, None

    def get_gfk_ids_related_models(self, gfk):
        related_models = gfk.get_related_models()

        content_types = ContentType.objects.get_for_models(*related_models)

        return [x.id for x in content_types.values()]

    def set_hidden_gfk(self, obj):
        for field in self.get_generic_foreign_keys():
            field_name = field.name
            init_value = str(getattr(obj, field.name, ''))

            form_integer_field = forms.CharField(
                widget=forms.HiddenInput(),
                required=False,
                initial=init_value
            )

            self.form.declared_fields[field_name] = form_integer_field

    def set_validators_gfk(self, form):
        for field in self.get_generic_foreign_keys():
            _copy_func = copy_func(clean_formfield)
            _copy_func.__defaults__ = (field,)

            setattr(form, f'clean_{field.name}', _copy_func)
