from admin_tools.decorators import (
    admin_changelist_link, admin_field, admin_link
)
from admin_tools.mixins import (
    AdminAutocompleteFieldsMixin, GenericForeignKeyMixin
)
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
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
    search_fields = ('name',)


@admin.register(Blog)
class BlogAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(GenericForeignKeyMixin,
                   AdminAutocompleteFieldsMixin,
                   admin.ModelAdmin):
    pass
