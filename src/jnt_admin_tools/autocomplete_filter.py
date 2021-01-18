from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.widgets import (
    SELECT2_TRANSLATIONS,
    AutocompleteSelect,
    AutocompleteSelectMultiple,
    get_language,
)
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.utils.translation import gettext_lazy as _


class AutocompleteFilter(admin.SimpleListFilter):
    template = "jnt_admin_tools/autocomplete_filter/autocomplete_filter.html"
    title = ""
    field_name = ""
    is_placeholder_title = False
    widget_attrs = {}
    rel_model = None
    is_multiple = False

    class Media:
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,)
            if i18n_name
            else ()
        )
        js = (
            (
                "admin/js/vendor/jquery/jquery%s.js" % extra,
                "admin/js/vendor/select2/select2.full%s.js" % extra,
            )
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "admin/js/autocomplete.js",
                "jnt_admin_tools/js/autocomplete_filter/autocomplete_filter_qs.js",
            )
        )
        css = {
            "screen": (
                "admin/css/vendor/select2/select2%s.css" % extra,
                "admin/css/autocomplete.css",
                "jnt_admin_tools/css/autocomplete_filter/autocomplete_fix.css",
            ),
        }

    def __init__(self, request, params, model, model_admin):
        if self.parameter_name:
            raise AttributeError(
                "Rename attribute 'parameter_name' to "
                "'field_name' for {0}".format(self.__class__)
            )
        self.parameter_name = "{0}__id__{1}".format(
            self.field_name,
            "in" if self.is_multiple else "exact",
        )
        super().__init__(request, params, model, model_admin)

        if self.rel_model:
            model = self.rel_model

        remote_field = self.get_remote_field(model)
        formfield = self.get_formfield(model, remote_field, model_admin)

        attrs = self.widget_attrs.copy()
        attrs["id"] = "id-{0}-changelist-filter".format(self.field_name)

        if self.is_placeholder_title:
            attrs["data-placeholder"] = _("MSG_BY {title}").format(
                title=self.title,
            )

        self.rendered_widget = self.get_rendered_widget(formfield, attrs)

    @property
    def media(self):
        """Collect media files."""
        return forms.Media(js=self.Media.js, css=self.Media.css)

    def has_output(self):
        return True

    def lookups(self, request, model_admin):
        return ()

    def value(self):
        parameter_value = self.used_parameters.get(self.parameter_name, "")
        if not parameter_value:
            return ""

        if self.is_multiple:
            parameter_value = parameter_value.split(",")

        return parameter_value

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(
                **{self.parameter_name: self.value()}
            ).distinct()
        return queryset

    def get_field_queryset(self, model):
        field = getattr(model, self.field_name)
        if isinstance(field, ManyToManyDescriptor):
            return field.rel.model.objects.all()

        return field.get_queryset()

    def get_formfield(self, model, remote_field, model_admin):
        queryset = self.get_field_queryset(model)

        if self.is_multiple:
            return forms.ModelMultipleChoiceField(
                widget=AutocompleteSelectMultiple(
                    remote_field,
                    model_admin.admin_site,
                ),
                queryset=queryset,
                required=False,
            )

        return forms.ModelChoiceField(
            widget=AutocompleteSelect(remote_field, model_admin.admin_site),
            queryset=queryset,
            required=False,
        )

    def get_remote_field(self, model):
        return model._meta.get_field(self.field_name).remote_field

    def get_rendered_widget(self, field, attrs):
        return field.widget.render(
            name=self.parameter_name,
            value=self.value(),
            attrs=attrs,
        )
