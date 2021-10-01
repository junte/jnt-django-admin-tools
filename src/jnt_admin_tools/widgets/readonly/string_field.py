from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget
import typing


class StringReadonlyWidget(BaseReadOnlyWidget):
    def render(
        self,
        field_value,
        field_name,
        **kwargs,
    ) -> typing.Optional[str]:
        db_field = kwargs.get("db_field")
        if getattr(db_field, "choices", None):
            choice = [
                present
                for choice_value, present in db_field.choices
                if choice_value == field_value
            ]

            if choice:
                return choice[0]

        return field_value
