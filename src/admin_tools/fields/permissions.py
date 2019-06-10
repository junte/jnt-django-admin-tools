from django import forms
from django.contrib.auth.models import Permission
from django.db.models import QuerySet

from ..widgets import PermissionSelectMultipleWidget


class PermissionSelectMultipleField(forms.ModelMultipleChoiceField):
    widget = PermissionSelectMultipleWidget

    def __init__(self, queryset: QuerySet = None, *args, **kwargs):
        if queryset is None:
            queryset = Permission.objects.all()

        super().__init__(queryset, *args, **kwargs)
