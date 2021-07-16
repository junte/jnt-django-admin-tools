from django.contrib import admin
from django.db import models

from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget


class AdminChangeListField:
    """Admin changelist field."""

    def __init__(
        self,
        model_admin: admin.ModelAdmin,
        field_name: str,
        readonly_widget: BaseReadOnlyWidget,
    ) -> None:
        """Init column presenter."""
        self._model_admin = model_admin
        self._field_name = field_name
        self._readonly_widget = readonly_widget
        self.__name__ = self._get_label()

    def __call__(self, instance) -> str:
        """Implement callable for render widget."""
        return self._readonly_widget.render(
            getattr(instance, self._field_name),
            self._field_name,
            db_field=self._get_model_field(),
        )

    def _get_model_field(self) -> models.Field:
        """Get current model field."""
        return self._model_admin.model._meta.get_field(self._field_name)

    def _get_label(self) -> str:
        """Get label for column."""
        model_field = self._get_model_field()
        try:
            return str(model_field.verbose_name)
        except AttributeError:
            return self._field_name
