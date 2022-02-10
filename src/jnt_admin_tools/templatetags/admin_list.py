from django.contrib.admin.templatetags.admin_list import *  # noqa: F403 WPS347
from django.contrib.admin.templatetags.admin_list import (
    change_list_object_tools_tag as base_change_list_object_tools_tag,
)


@register.tag(name="change_list_object_tools")  # noqa: F405
def change_list_object_tools_tag(parser, token):
    """Display the row of change list admin tools."""
    admin_node = base_change_list_object_tools_tag(parser, token)
    admin_node.template_name = "jnt_admin_tools/change_list_object_tools.html"
    return admin_node
