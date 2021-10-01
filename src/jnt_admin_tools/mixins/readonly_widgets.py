import types
import typing as ty

from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.http import HttpRequest

from jnt_admin_tools.db.fields import GenericForeignKey
from jnt_admin_tools.widgets.readonly import (
    ForeignKeyReadonlyWidget,
    GenericForeignKeyReadonlyWidget,
    ManyToManyReadonlyWidget,
    PermissionSelectMultipleReadonlyWidget,
    StringReadonlyWidget,
)
from jnt_admin_tools.widgets.readonly.base import BaseReadOnlyWidget
from django.contrib.auth.models import Permission

READONLY_WIDGETS = types.MappingProxyType(
    {
        models.ForeignKey: ForeignKeyReadonlyWidget(),
        models.OneToOneField: ForeignKeyReadonlyWidget(),
        models.ManyToManyField: ManyToManyReadonlyWidget(),
        models.ManyToOneRel: ManyToManyReadonlyWidget(),
        models.CharField: StringReadonlyWidget(),
        models.TextField: StringReadonlyWidget(),
        GenericForeignKey: GenericForeignKeyReadonlyWidget(),
    },
)


class ReadonlyWidgetsMixin:
    def readonly_widget(
        self,
        field_name: str,
        request: HttpRequest = None,
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

        return self.readonly_widgets(request).get(field_class)

    def readonly_widgets(
        self,
        request: HttpRequest = None,
    ) -> ty.Dict[models.Field, BaseReadOnlyWidget]:
        """Return available readonly_widgets."""
        return dict(READONLY_WIDGETS)
