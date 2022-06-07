import abc
import typing as ty

from django.utils.html import format_html


class BaseAdminTool(abc.ABC):
    """Base admin tool."""

    code: str
    title: str
    label_class: str = ""
    target: str = ""

    def __init__(self, model_admin) -> None:
        """Init base admin tool."""
        self.model_admin = model_admin

    @classmethod
    def get_label(cls) -> str:
        """Get label."""
        return cls.title

    @abc.abstractmethod
    def get_url(self, *args, **kwargs) -> str:
        """Get url."""

    def has_permission(self, request) -> bool:
        """Has user permission for view current admin tool."""
        return True


class BaseChangeformTool(BaseAdminTool):
    """Base admin tool."""

    def __init__(self, model_admin, instance) -> None:
        """Init base admin tool."""
        self.instance = instance
        super().__init__(model_admin)

    def get_content(self, request) -> str | None:
        """Get content."""
        url = self.get_url(request)
        if not url:
            return None

        tag_attrs = {
            "href": url,
            "class": self.label_class,
            "target": self.target,
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


class BaseChangelistTool(BaseAdminTool):
    """Base changelist tool."""

    def _get_content(self, *args, **kwargs) -> str | None:
        """Get content."""
        url = self.get_url(*args, **kwargs)
        if not url:
            return None

        additional_class = "change-list-link-{0}".format(self.code)

        tag_attrs = {
            "href": url,
            "class": "addlink {0}".format(additional_class),
            "target": self.target,
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
