from django.forms.models import ModelChoiceIterator
from jnt_admin_tools.widgets import PermissionSelectMultipleWidget


class PermissionSelectMultipleReadonlyWidget(PermissionSelectMultipleWidget):
    """Permissions multiple readonly widget. """

    def __init__(self, *args, **kwargs):
        """Initializing."""
        self._formfield = kwargs.pop("formfield", None)
        super().__init__(*args, **kwargs)

        self.extra_data["is_readonly"] = True

        if self._formfield:
            self.choices = ModelChoiceIterator(self._formfield)

    def render(self, name, value, *args, **kwargs):
        """Render html-string."""
        self.groups_permissions = value.all()
        return super().render(name=name, value=value.all(), *args, **kwargs)
