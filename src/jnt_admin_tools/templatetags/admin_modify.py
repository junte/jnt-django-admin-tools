from django.contrib.admin.templatetags.admin_modify import *  # noqa: F403 F405 WPS347 E501
from django.contrib.admin.templatetags.admin_modify import (
    change_form_object_tools_tag as base_change_form_object_tools_tag,
)
from django.contrib.admin.templatetags.admin_modify import (
    submit_row_tag as base_submit_row_tag,
)


@register.tag(name="submit_row")  # noqa: F405
def submit_row_tag(parser, token):
    admin_node = base_submit_row_tag(parser, token)
    admin_node.template_name = "jnt_admin_tools/submit_line.html"

    return admin_node


@register.tag(name="change_form_object_tools")  # noqa: F405
def change_form_object_tools_tag(parser, token):
    """Display the row of change form admin tools."""
    admin_node = base_change_form_object_tools_tag(parser, token)
    admin_node.template_name = "jnt_admin_tools/change_form_object_tools.html"

    return admin_node
