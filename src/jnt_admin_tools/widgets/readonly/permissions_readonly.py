from django.forms.models import ModelChoiceIterator

from jnt_admin_tools.widgets import PermissionSelectMultipleWidget


class FakeField:
    """Fake field for ModelChoiceIterator."""

    def __init__(self, queryset) -> None:
        self.queryset = queryset
        self.empty_label = False


class PermissionSelectMultipleReadonlyWidget(PermissionSelectMultipleWidget):
    """Permissions multiple readonly widget. """

    def __init__(self, *args, **kwargs) -> None:
        """Initializing."""
        super().__init__(*args, **kwargs)
        self.extra_data["is_readonly"] = True

    def render(self, value, name, *args, **kwargs):
        """Render html-string."""
        permissions = value.all()

        self.choices = ModelChoiceIterator(FakeField(permissions))
        self.groups_permissions = permissions

        return super().render(name=name, value=permissions)
