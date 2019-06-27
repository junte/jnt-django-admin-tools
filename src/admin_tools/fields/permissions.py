from django import forms
from django.contrib.auth.models import Permission
from django.db.models import QuerySet

from ..widgets import PermissionSelectMultipleWidget


class PermissionSelectMultipleField(forms.ModelMultipleChoiceField):
    """
    A form field for displaying all permissions in system.

    Usage::

        from admin_tools.fields import PermissionSelectMultipleField
        from django import forms
        from django.contrib.auth.models import Group

        class GroupAdminForm(forms.ModelForm):
            permissions = PermissionSelectMultipleField(required=False)

        class Meta:
            model = Group
            fields = '__all__'

    .. image:: images/widgets/permission_select_multiple_widget.png
    """
    widget = PermissionSelectMultipleWidget

    def __init__(self, queryset: QuerySet = None, *args, **kwargs):
        if queryset is None:
            queryset = Permission.objects.all()

        super().__init__(queryset, *args, **kwargs)
