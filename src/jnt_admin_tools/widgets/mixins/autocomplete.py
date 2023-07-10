from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language


class AutocompleteWidgetMixin:
    class Media:
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/{0}.js".format(i18n_name),)
            if i18n_name
            else ()
        )

        css = {
            "all": ("admin/css/vendor/select2/select2.css",),
        }
        js = (
            (
                "admin/js/vendor/jquery/jquery{0}.js".format(extra),
                "admin/js/vendor/select2/select2.full{0}.js".format(extra),
            )
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "jnt_django_toolbox/js/widgets/autocomplete.js",
            )
        )

    autocomplete_function = "select2"
