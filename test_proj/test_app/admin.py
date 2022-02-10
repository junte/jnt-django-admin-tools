from django.contrib import admin
from django.contrib.auth.models import Group
from test_app.admin_tools import (
    BbcSiteChangelistTool,
    GoogleSiteChangeformTool,
    YandexSiteChangeformTool,
)
from test_app.changeform_submits import ReloadSubmit
from test_app.models import Bar, Baz, Blog, Comment, Foo, Tag

from jnt_admin_tools.admin.mixins import (
    AdminToolsMixin,
    ChangeFormSubmitsMixin,
)

admin.site.unregister(Group)


class BazInlineAdmin(admin.TabularInline):
    model = Baz
    extra = 0
    fields = ("name", "foos", "owner")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ("permissions",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


@admin.register(Foo)
class FooAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name", "bar")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Bar)
class BarAdmin(AdminToolsMixin, ChangeFormSubmitsMixin, admin.ModelAdmin):
    fields = ("name",)
    search_fields = ("name",)
    changeform_tools = (GoogleSiteChangeformTool, YandexSiteChangeformTool)
    changelist_tools = (BbcSiteChangelistTool,)
    changeform_submits = (ReloadSubmit,)


@admin.register(Baz)
class BazAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
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
