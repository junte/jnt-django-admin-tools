from admin_tools.decorators import admin_changelist_link, admin_link
from django.contrib import admin

from test_app.models import Bar, Foo


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    list_display = ('name', 'bar_link')
    fields = ('name', 'bar', 'bar_link')
    readonly_fields = ('bar_link',)

    @admin_link('bar')
    def bar_link(self, obj):
        return obj.name


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    fields = ('name', 'foos')
    readonly_fields = ('foos',)

    @admin_changelist_link('foos', query_string=lambda bar: f'bar_id={bar.pk}')
    def foos(self, foos):
        return ', '.join(str(foo) for foo in foos.all())
