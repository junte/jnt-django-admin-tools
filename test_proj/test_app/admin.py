from jnt_admin_tools.decorators import (
    admin_changelist_link,
    admin_field,
    admin_link,
)
from jnt_admin_tools.mixins import (
    AdminAutocompleteFieldsMixin,
    GenericForeignKeyAdminMixin,
    GenericForeignKeyInlineAdminMixin,
)
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Foo, Baz, Blog, Comment
from test_app.filters import BarAutocompleteFilter

admin.site.unregister(Group)


class BazInlineAdmin(
    GenericForeignKeyInlineAdminMixin,
    AdminAutocompleteFieldsMixin,
    admin.StackedInline,
):
    model = Baz
    extra = 0

    fields = ("name", "owner")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm


@admin.register(Foo)
class FooAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    list_display = ("name", "bar_link")
    fields = ("name", "bar", "bar_link")
    readonly_fields = ("bar_link",)
    search_fields = ("name",)
    list_filter = (BarAutocompleteFilter,)

    @admin_link("bar")
    def bar_link(self, obj):
        return obj.name

    class Media:
        pass


@admin.register(Bar)
class BarAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    fields = ("name", "foos", "custom_field")
    readonly_fields = ("foos", "custom_field")
    search_fields = ("name",)

    @admin_changelist_link("foos", query_string=lambda bar: f"bar_id={bar.pk}")
    def foos(self, foos):
        return ", ".join(str(foo) for foo in foos.all())

    @admin_field("Custom field")
    def custom_field(self, obj):
        return mark_safe("<h1>custom field</h1>")


@admin.register(Baz)
class BazAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(
    GenericForeignKeyAdminMixin, AdminAutocompleteFieldsMixin, admin.ModelAdmin
):

    search_fields = ("name",)
    inlines = (BazInlineAdmin,)


@admin.register(Comment)
class CommentAdmin(
    GenericForeignKeyAdminMixin, AdminAutocompleteFieldsMixin, admin.ModelAdmin
):
    fieldsets = (
        (None, {"fields": ("title", "content")}),
        ("Advanced options", {"fields": ("user", "link"),}),
        (None, {"fields": ("owner",),}),
    )
