from django.core.checks import Warning, register
from django.template.loader import TemplateDoesNotExist, get_template

W001 = Warning(
    'You must add "jnt_admin_tools.template_loaders.Loader" in your '
    "template loaders variable, see: "
    "https://django-admin-tools.readthedocs.io/en/latest/configuration.html",
    id="jnt_admin_tools.W001",
    obj="jnt_admin_tools",
)


@register("jnt_admin_tools")
def check_admin_tools_configuration(app_configs=None, **kwargs):
    result = []
    try:
        get_template("admin:admin/base.html")
    except TemplateDoesNotExist:
        result.append(W001)
    return result
