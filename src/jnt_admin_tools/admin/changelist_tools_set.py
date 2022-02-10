class ChangelistToolsSet:
    def __init__(self, request, model_admin) -> None:
        self.request = request
        self.model_admin = model_admin

    def __str__(self) -> str:
        return "{0}: changelist admin tools".format(self.model_admin)

    def __iter__(self):
        for changelist_tool_class in self.model_admin.get_changelist_tools():
            changelist_tool = changelist_tool_class(self.model_admin)

            if not changelist_tool.has_permission(self.request):
                continue

            changelist_tool_content = changelist_tool._get_content(
                self.request,
            )
            if not changelist_tool_content:
                continue

            yield changelist_tool_content
