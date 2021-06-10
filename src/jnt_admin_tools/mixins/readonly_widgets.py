import types
import typing

from django.contrib.admin.helpers import AdminReadonlyField
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
    }
)


class ReadonlyWidgetsMixin:
    def readonly_widget(
        self,
        admin_readonly_field: AdminReadonlyField,
    ) -> typing.Optional[BaseReadOnlyWidget]:
        """Return readonly widget for admin readonly field."""
        try:
            db_field = self.model._meta.get_field(
                admin_readonly_field.field["field"],
            )
        except FieldDoesNotExist:
            return None

        return READONLY_WIDGETS.get(db_field.__class__)
