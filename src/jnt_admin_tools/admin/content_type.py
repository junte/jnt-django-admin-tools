from django.contrib import admin

from jnt_admin_tools.views import ContentTypeAutocompleteView


class BaseContentTypeAdmin(admin.ModelAdmin):
    search_fields = ("model",)

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
        return ContentTypeAutocompleteView.as_view(model_admin=self)(request)
