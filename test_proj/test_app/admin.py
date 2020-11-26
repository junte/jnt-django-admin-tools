from jnt_admin_tools.mixins import (
    AdminAutocompleteFieldsMixin,
    GenericForeignKeyAdminMixin,
    GenericForeignKeyInlineAdminMixin,
    AdminClickableLinksMixin,
)
from django.contrib import admin
from django.contrib.auth.models import Group
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Foo, Baz, Blog, Comment, Tag
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


@admin.register(Foo)
class FooAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name", "bar")
    search_fields = ("name",)
    list_filter = (BarAutocompleteFilter,)

    class Media:
        pass


@admin.register(Bar)
class BarAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    fields = ("name",)
    search_fields = ("name",)


@admin.register(Baz)
class BazAdmin(AdminAutocompleteFieldsMixin, admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(  # noqa: WPS215
    GenericForeignKeyAdminMixin,
    AdminAutocompleteFieldsMixin,
    AdminClickableLinksMixin,
    admin.ModelAdmin,
):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)


@admin.register(Comment)
class CommentAdmin(
    GenericForeignKeyAdminMixin, AdminAutocompleteFieldsMixin, admin.ModelAdmin
):
    fieldsets = (
        (None, {"fields": ("title", "content")}),
        (
            "Advanced options",
            {
                "fields": ("user", "link"),
            },
        ),
        (
            None,
            {
                "fields": ("owner",),
            },
        ),
    )
