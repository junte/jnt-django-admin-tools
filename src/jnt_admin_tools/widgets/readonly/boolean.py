from django.contrib.admin.templatetags.admin_list import (  # noqa: WPS450
    _boolean_icon as boolean_icon,
)
from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget


class BooleanReadonlyWidget(BaseReadOnlyWidget):
    def render(self, field_value, field_name, **kwargs) -> str:
        """Render boolean readonly widget."""
        return boolean_icon(field_value)
