from django import template

from jnt_admin_tools.admin.base_changeform_submit import (
    BaseChangeformSubmit,
    SubmitPosition,
)

register = template.Library()


@register.filter
def left_positioned_submits(
    submits: list[BaseChangeformSubmit],
) -> list[BaseChangeformSubmit]:
    return [
        submit for submit in submits if submit.position == SubmitPosition.LEFT
    ]


@register.filter
def right_positioned_submits(
    submits: list[BaseChangeformSubmit],
) -> list[BaseChangeformSubmit]:
    return [
        submit for submit in submits if submit.position == SubmitPosition.RIGHT
    ]
