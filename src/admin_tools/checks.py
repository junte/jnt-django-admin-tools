from itertools import chain

from django.contrib.admin.checks import ModelAdminChecks
from django.core.checks import Warning, register
from django.template.loader import TemplateDoesNotExist, get_template

W001 = Warning(
    'You must add "admin_tools.template_loaders.Loader" in your '
    'template loaders variable, see: '
    'https://django-admin-tools.readthedocs.io/en/latest/configuration.html',
    id='admin_tools.W001',
    obj='admin_tools'
)


@register('admin_tools')
def check_admin_tools_configuration(app_configs=None, **kwargs):
    result = []
    try:
        get_template('admin:admin/base.html')
    except TemplateDoesNotExist:
        result.append(W001)
    return result


class AutoCompleteModelAdminChecks(ModelAdminChecks):
    def check(self, admin_obj, **kwargs):
        return [
            *super().check(admin_obj),
            *self._check_autocomplete_fields_auto(admin_obj),
        ]

    def _check_autocomplete_fields_auto(self, obj):
        if 'autocomplete_fields' in obj.__class__.__dict__.keys():
            return []

        return list(chain.from_iterable([
            self._check_autocomplete_fields_item(obj, field_name, f'autocomplete_fields[{index:d}]')
            for index, field_name in enumerate(obj.get_autocomplete_fields(None))
        ]))
