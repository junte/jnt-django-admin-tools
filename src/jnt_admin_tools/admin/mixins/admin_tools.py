from jnt_admin_tools.admin.changeform_tools_set import ChangeformToolsSet
from jnt_admin_tools.admin.changelist_tools_set import ChangelistToolsSet


class AdminToolsMixin:
    changeform_tools = ()
    changelist_tools = ()

    def render_change_form(
        self,
        request,
        context,
        add=False,
        change=False,
        form_url="",
        obj=None,  # noqa: WPS110
    ):
        if change:
            context.update(
                changeform_tools=ChangeformToolsSet(request, self, obj),
            )

        return super().render_change_form(
            request,
            context,
            add,
            change,
            form_url,
            obj,
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            changelist_tools=ChangelistToolsSet(request, self),
        )
        return super().changelist_view(request, extra_context=extra_context)

    def get_changeform_tools(self):  # noqa: WPS615
        return self.changeform_tools

    def get_changelist_tools(self):  # noqa: WPS615
        return self.changelist_tools
