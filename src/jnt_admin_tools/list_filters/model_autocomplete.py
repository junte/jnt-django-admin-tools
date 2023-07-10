import itertools

from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.utils import get_fields_from_path
from django.db import models
from django.http import HttpRequest
from jnt_django_toolbox.forms.widgets import (
    AutocompleteSelect,
    AutocompleteSelectMultiple,
)

from jnt_admin_tools.widgets.mixins import AutocompleteWidgetMixin


class AutocompleteFilterError(Exception):
    """Autocomplete filter error."""


class ModelAutocompleteChangeListFilter(
    AutocompleteWidgetMixin,
    admin.SimpleListFilter,
):
    template = "jnt_admin_tools/filters/list_filter.html"
    is_multiple = None

    title = "List filter"
    custom_model = None
    parameter_name = None

    def __init__(
        self,
        request: HttpRequest,
        params,  # noqa: WPS110
        model,
        model_admin,
    ):
        super().__init__(request, params, model, model_admin)

        if not self.parameter_name:
            raise AutocompleteFilterError("Parameter name is required")

        if self.custom_model:
            model = self.custom_model

        self.request = request
        relation = self.get_relation(model, self.parameter_name)

        if self.is_multiple is None:
            self.is_multiple = isinstance(relation, models.ManyToManyRel)

        widget = self.get_widget(relation, model, model_admin)
        field = self.get_field(model, widget)

        self.rendered_widget = self.get_rendered_widget(
            field=field,
            request=request,
        )
        self._media = self._get_media(field.widget)

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"

        jquery_js = [
            "admin/js/{0}".format(path)
            for path in (
                "vendor/jquery/jquery{0}.js".format(extra),
                "jquery.init.js",
            )
        ]

        return (
            forms.Media(
                js=(
                    *jquery_js,
                    "jnt_admin_tools/js/filters/autocomplete.js",
                ),
            )
            + self._media
        )

    def lookups(self, request: HttpRequest, model_admin):
        return (("__id__in", "in list"),)

    def queryset(
        self,
        request: HttpRequest,
        queryset: models.QuerySet,
    ) -> models.QuerySet:
        query_value = self.get_value(request)

        if query_value:
            lookup, _ = self.lookups(request, None)[0]
            query = self._build_query(queryset.model, lookup, query_value)
            queryset = queryset.filter(query)

        return queryset

    def get_value(self, request: HttpRequest):
        query_values = request.GET.getlist(self.parameter_name)
        not_digits = [
            query_value
            for query_value in query_values
            if query_value and not query_value.isdigit()
        ]
        if not_digits:
            raise AutocompleteFilterError(
                'Parameters for "{0}" must be is digits'.format(
                    self.parameter_name,
                ),
            )
        return query_values

    def get_field_queryset(self, model) -> models.QuerySet:
        target_field = get_fields_from_path(model, self.parameter_name)[
            -1
        ].target_field

        return target_field.model.objects.all()

    def get_widget(self, rel, model, model_admin: admin.ModelAdmin):
        return self.get_widget_class()(rel, model_admin.admin_site)

    def get_widget_class(self):
        return (
            AutocompleteSelectMultiple
            if self.is_multiple
            else AutocompleteSelect
        )

    def get_field(self, model, widget):
        return self.get_field_class()(
            queryset=self.get_field_queryset(model),
            widget=widget,
            required=False,
        )

    def get_field_class(self):
        return (
            forms.ModelMultipleChoiceField
            if self.is_multiple
            else forms.ModelChoiceField
        )

    def get_widget_attrs(self):
        return {
            "is-list-filter": True,
            "data-parameter": self.parameter_name,
        }

    def get_rendered_widget(self, field, request: HttpRequest):  # noqa: WPS615
        widget_value = self.get_value(request)
        attrs = self.get_widget_attrs()

        return field.widget.render(
            name=self.parameter_name,
            value=widget_value,
            attrs=attrs,
        )

    def get_relation(self, model, parameter_name: str):
        return get_fields_from_path(model, self.parameter_name)[-1]

    def _get_media(self, widget: forms.Widget):
        js_files = []

        for js in itertools.chain.from_iterable(widget.media._js_lists):
            if js not in js_files:
                js_files.append(js)

        css_files = getattr(widget.media, "_css", {})
        changelist_filter_css = "jnt_admin_tools/css/filters/autocomplete.css"

        all_css = css_files.get("all")
        if all_css:
            all_css.append(changelist_filter_css)
        else:
            css_files["all"] = (changelist_filter_css,)

        return forms.Media(
            js=js_files,
            css=css_files,
        )

    def _build_query(
        self,
        model: models.Model,
        lookup: str,
        query_value,
    ) -> models.Q:
        field = model._meta.get_field(self.parameter_name)
        if field.many_to_many:
            return models.Q(
                models.Exists(
                    model.objects.filter(
                        **{
                            "id": models.OuterRef("id"),
                            "{0}{1}".format(
                                self.parameter_name,
                                lookup,
                            ): query_value,
                        },
                    ),
                ),
            )

        return models.Q(
            **{
                "{0}{1}".format(self.parameter_name, lookup): query_value,
            },
        )
