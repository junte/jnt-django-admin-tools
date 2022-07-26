import abc
import contextlib
import typing as ty

from django.contrib import admin
from django.http import HttpRequest
from django.urls import path, reverse
from django.utils.html import format_html
from django.views import View

from jnt_admin_tools.helpers.views import (
    wrap_model_instance_admin_view,
    wrap_model_list_admin_view,
)


class BaseAdminTool(abc.ABC):
    """Base admin tool."""

    label: str
    label_class: str | None = None
    link_target: str | None = None
    view: ty.Type[View] | None = None
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
    def html(self) -> str | None:
        raise NotImplementedError()

    def get_url(self) -> str:
        """Get url."""
        raise NotImplementedError()

    def get_label(self) -> str:  # noqa: WPS615
        """Get label."""
        return self.label

    @classmethod
    def get_route(cls, model_admin: admin.ModelAdmin):
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


class BaseChangeformTool(BaseAdminTool):
    """Base admin tool."""

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
        """Get url."""
        return reverse(
            "{0}:{1}".format(
                self.model_admin.admin_site.name,
                self.get_route_name(self.model_admin),
            ),
            args=[self.instance.pk],
        )

    def has_permission(self) -> bool:
        if not self.view:
            return True

        view = self.view(
            model_admin=self.model_admin,
            instance=self.instance,
        )
        view.setup(self.request)

        with contextlib.suppress(AttributeError):
            return view.has_permission()

        return True

    @property
    def html(self) -> str | None:
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
        if not cls.view:
            return None

        return path(
            cls.route_path,
            wrap_model_instance_admin_view(model_admin, cls.view),
            name=cls.get_route_name(model_admin),
        )


class BaseChangelistTool(BaseAdminTool):
    """Base changelist tool."""

    def get_url(self) -> str:
        return reverse(
            "{0}:{1}".format(
                self.model_admin.admin_site.name,
                self.get_route_name(self.model_admin),
            ),
        )

    def has_permission(self) -> bool:
        if not self.view:
            return True

        view = self.view(
            model_admin=self.model_admin,
        )
        view.setup(self.request)

        with contextlib.suppress(AttributeError):
            return view.has_permission()

        return True

    @property
    def html(self) -> str | None:
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
        if not cls.view:
            return None

        return path(
            cls.route_path,
            wrap_model_list_admin_view(model_admin, cls.view),
            name=cls.get_route_name(model_admin),
        )
