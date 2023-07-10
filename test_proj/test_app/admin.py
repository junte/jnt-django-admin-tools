from django.contrib import admin
from django.contrib.auth.models import Group

from jnt_admin_tools.admin.base_admin import BaseModelAdmin
from jnt_admin_tools.list_filters.model_autocomplete import (
    ModelAutocompleteChangeListFilter,
)
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


class BarListFilter(ModelAutocompleteChangeListFilter):
    title = "bar"
    parameter_name = "bar"


class BazInlineAdmin(admin.TabularInline):
    model = Baz
    extra = 0
    fields = ("name", "foos", "owner")


@admin.register(Group)
class GroupAdmin(BaseModelAdmin):
    readonly_fields = ("permissions",)


@admin.register(Tag)
class TagAdmin(BaseModelAdmin):
    list_display = ("title",)
    fields = ("title",)
    search_fields = ("title",)


@admin.register(Foo)
class FooAdmin(BaseModelAdmin):
    list_display = ("name",)
    fields = ("name", "bar")
    search_fields = ("name",)
    list_filter = ("name", BarListFilter)


@admin.register(Bar)
class BarAdmin(BaseModelAdmin):
    fields = ("name",)
    search_fields = ("name",)
    changeform_tools = (GoogleSiteChangeformTool, YandexSiteChangeformTool)
    changelist_tools = (BbcSiteChangelistTool,)
    changeform_submits = (ReloadSubmit,)


@admin.register(Baz)
class BazAdmin(BaseModelAdmin):
    search_fields = ("name",)


@admin.register(Blog)
class BlogAdmin(BaseModelAdmin):
    list_display = ("title", "author", "tags")
    readonly_fields = ("author", "tags")
    search_fields = ("title",)
    inlines = (BazInlineAdmin,)


@admin.register(Comment)
class CommentAdmin(BaseModelAdmin):
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
