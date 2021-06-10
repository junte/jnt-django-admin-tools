from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget
from jnt_admin_tools.services.object_links import object_change_link
from typing import Optional
from django.utils.html import format_html


class GenericForeignKeyReadonlyWidget(BaseReadOnlyWidget):
    """Generic foreign key readonly widget."""

    def render(self, field_value, field_name, **kwargs) -> Optional[str]:
        """Render foreign key field."""
        if not field_value:
            return None

        return format_html(
            '<span class="gfk-object-type">{0}</span> {1}'.format(
                field_value._meta.model_name,
                object_change_link(field_value),
            ),
        )
