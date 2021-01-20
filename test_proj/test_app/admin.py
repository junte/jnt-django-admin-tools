from django.contrib import admin
from django.contrib.auth.models import Group
from jnt_admin_tools.admin.base import (
    AutocompleteAdminMixin,
    BaseModelAdmin,
)

from jnt_admin_tools.mixins import (
    ClickableLinksAdminMixin,
    GenericForeignKeyAdminMixin,
    GenericForeignKeyInlineAdminMixin,
)
from test_app.filters import BarAutocompleteFilter, TagsAutocompleteFilter
from test_app.forms import GroupAdminForm
from test_app.models import Bar, Baz, Blog, Comment, Foo, Tag

admin.site.unregister(Group)


class BazInlineAdmin(
    GenericForeignKeyInlineAdminMixin,
    AutocompleteAdminMixin,
    admin.StackedInline,
):
    model = Baz
    extra = 0
    fields = ("name", "owner")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    readonly_fields = ("permissions",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


@admin.register(Foo)
class FooAdmin(BaseModelAdmin):
    list_display = ("name",)
    fields = ("name", "bar")
    search_fields = ("name",)
    list_filter = (BarAutocompleteFilter, "name")


@admin.register(Bar)
class BarAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    fields = ("name",)
    search_fields = ("name",)


@admin.register(Baz)
class BazAdmin(AutocompleteAdminMixin, admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(  # noqa: WPS215
    GenericForeignKeyAdminMixin,
    AutocompleteAdminMixin,
    ClickableLinksAdminMixin,
    admin.ModelAdmin,
):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)
    list_filter = (TagsAutocompleteFilter,)


@admin.register(Comment)
class CommentAdmin(
    GenericForeignKeyAdminMixin,
    AutocompleteAdminMixin,
    admin.ModelAdmin,
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
