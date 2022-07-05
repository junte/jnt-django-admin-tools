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
            tools = []
            for tool_class in self.get_changeform_tools():
                tool = tool_class(self, request, obj)

                if tool.has_permission():
                    tools.append(tool)

            context.update(
                changeform_tools=tools,
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

        tools = []
        for tool_class in self.get_changelist_tools():
            tool = tool_class(self, request)

            if tool.has_permission():
                tools.append(tool)

        extra_context.update(
            changelist_tools=tools,
        )
        return super().changelist_view(
            request,
            extra_context=extra_context,
        )

    def get_changeform_tools(self):  # noqa: WPS615
        return self.changeform_tools

    def get_changelist_tools(self):  # noqa: WPS615
        return self.changelist_tools

    def get_urls(self):
        urls = []
        for tool in self.get_changeform_tools():
            route = tool.get_route(self)
            if route:
                urls.append(route)

        for tool in self.get_changelist_tools():
            route = tool.get_route(self)
            if route:
                urls.append(route)

        return [
            *urls,
            *super().get_urls(),
        ]
