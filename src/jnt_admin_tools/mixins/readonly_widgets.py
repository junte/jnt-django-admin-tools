import types
import typing as ty

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from jnt_admin_tools.db.fields import GenericForeignKey
from jnt_admin_tools.widgets.readonly import (
    CharChoiceReadonlyWidget,
    ForeignKeyReadonlyWidget,
    GenericForeignKeyReadonlyWidget,
    ManyToManyReadonlyWidget,
    PermissionSelectMultipleReadonlyWidget,
)
from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget
from django.contrib.auth.models import Permission

READONLY_WIDGETS = types.MappingProxyType(
    {
        models.ForeignKey: ForeignKeyReadonlyWidget(),
        models.OneToOneField: ForeignKeyReadonlyWidget(),
        models.ManyToManyField: ManyToManyReadonlyWidget(),
        models.ManyToOneRel: ManyToManyReadonlyWidget(),
        models.CharField: CharChoiceReadonlyWidget(),
        models.TextField: CharChoiceReadonlyWidget(),
        GenericForeignKey: GenericForeignKeyReadonlyWidget(),
    },
)


class ReadonlyWidgetsMixin:
    def readonly_widget(
        self,
        field_name: str,
    ) -> ty.Optional[BaseReadOnlyWidget]:
        """Return readonly widget for admin readonly field."""
        if callable(field_name) or getattr(self, field_name, None):
            return None

        try:
            model_field = self.model._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None

        field_class = model_field.__class__

        if issubclass(field_class, models.ManyToManyField) and issubclass(
            model_field.related_model,
            Permission,
        ):
            return PermissionSelectMultipleReadonlyWidget()

        return self.readonly_widgets().get(field_class)

    def readonly_widgets(self) -> ty.Dict[models.Field, BaseReadOnlyWidget]:
        """Return available readonly_widgets."""
        return dict(READONLY_WIDGETS)
