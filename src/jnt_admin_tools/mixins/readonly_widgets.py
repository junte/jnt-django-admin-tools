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
)
from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget

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

        return self.readonly_widgets().get(model_field.__class__)

    def readonly_widgets(self) -> ty.Dict[models.Field, BaseReadOnlyWidget]:
        """Return available readonly_widgets."""
        return dict(READONLY_WIDGETS)
