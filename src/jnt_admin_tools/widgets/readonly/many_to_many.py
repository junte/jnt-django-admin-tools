from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget
from jnt_admin_tools.services.object_links import get_display_for_many


class ManyToManyReadonlyWidget(BaseReadOnlyWidget):
    """Many to many readonly widget."""

    def render(self, field_value, field_name, **kwargs) -> str:
        """Render m2m field."""
        if isinstance(field_value, str):
            return field_value

        return get_display_for_many(
            field_value.all(),
            field_present=kwargs.get("field_present"),
        )
