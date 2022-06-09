import abc
from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.views import View


class BaseAdminTool(abc.ABC):
    """Base admin tool."""

    label: str
    label_class: str | None = None
    link_target: str | None = None
    view: View | None = None
    route_postfix: str | None = None
    route_path: str | None = None

    def __init__(
        self,
        model_admin: admin.ModelAdmin,
        request: HttpRequest,
    ) -> None:
        """Init base admin tool."""
        self.model_admin = model_admin
        self.request = request

    @property
    def link_html(self) -> str | None:
        raise NotImplementedError()

    def get_url(self) -> str:
        """Get url."""
        raise NotImplementedError()

    def get_label(self) -> str:  # noqa: WPS615
        """Get label."""
        return self.label

    @classmethod
    def get_route(cls, model_admin):
        return None  # noqa: WPS324

    def has_permission(self) -> bool:
        """Has user permission for view current admin tool."""
        return True

    @classmethod
    def get_route_name(cls, model_admin) -> str:
        return "{0}_{1}_{2}".format(
            model_admin.model._meta.app_label,
            model_admin.model._meta.model_name,
            cls.route_postfix,
        )


def _changeform_view_wrapper(
    request: HttpRequest,
    model_admin: admin.ModelAdmin,
    view: View,
    object_id: str,
) -> HttpResponse:
    instance = model_admin.get_object(request, unquote(object_id))
    if instance is None:
        return model_admin._get_obj_does_not_exist_redirect(
            request,
            model_admin.model._meta,
            object_id,
        )

    if not model_admin.has_change_permission(request):
        raise PermissionDenied()

    return view.as_view(
        model_admin=model_admin,
        instance=instance,
    )(request)


def _changelist_view_wrapper(
    request: HttpRequest,
    model_admin: admin.ModelAdmin,
    view: View,
) -> HttpResponse:
    return view.as_view(
        model_admin=model_admin,
    )(request)


class BaseChangeformTool(BaseAdminTool):
    """Base admin tool."""

    code: str

    def __init__(
        self,
        model_admin: admin.ModelAdmin,
        request: HttpRequest,
        instance,
    ) -> None:
        """Init base admin tool."""
        self.instance = instance
        super().__init__(model_admin, request)

    def get_url(self) -> str:
        return reverse(
            "admin:{0}".format(self.get_route_name(self.model_admin)),
            args=[self.instance.pk],
        )

    @property
    def link_html(self) -> str | None:
        """Get content."""
        url = self.get_url()
        if not url:
            return None

        tag_attrs = {
            "href": url,
            "class": self.label_class,
            "target": self.link_target,
        }

        render_attrs = " ".join(
            (
                '{0}="{1}"'.format(tag_attr, tag_value)
                for tag_attr, tag_value in tag_attrs.items()
                if tag_value
            ),
        )

        return format_html(
            "<a {0}>{1}</a>".format(render_attrs, self.get_label()),
        )

    @classmethod
    def get_route(cls, model_admin):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return model_admin.admin_site.admin_view(view)(
                    *args,
                    model_admin=model_admin,
                    view=cls.view,
                    **kwargs,
                )

            return update_wrapper(wrapper, view)

        if not cls.view:
            return None

        return path(
            cls.route_path,
            wrap(_changeform_view_wrapper),
            name=cls.get_route_name(model_admin),
        )


class BaseChangelistTool(BaseAdminTool):
    """Base changelist tool."""

    def get_url(self) -> str:
        return reverse(
            "admin:{0}".format(self.get_route_name(self.model_admin)),
        )

    @property
    def link_html(self) -> str | None:
        """Get content."""
        url = self.get_url()
        if not url:
            return None

        tag_attrs = {
            "href": url,
            "class": "addlink",
            "target": self.link_target,
        }

        render_attrs = " ".join(
            (
                '{0}="{1}"'.format(tag_attr, tag_value)
                for tag_attr, tag_value in tag_attrs.items()
                if tag_value
            ),
        )

        return format_html(
            "<a {0}>{1}</a>".format(render_attrs, self.get_label()),
        )

    @classmethod
    def get_route(cls, model_admin):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return model_admin.admin_site.admin_view(view)(
                    *args,
                    model_admin=model_admin,
                    view=cls.view,
                    **kwargs,
                )

            return update_wrapper(wrapper, view)

        if not cls.view:
            return None

        return path(
            cls.route_path,
            wrap(_changelist_view_wrapper),
            name=cls.get_route_name(model_admin),
        )
