class ChangeformToolsSet:
    def __init__(self, request, model_admin, instance) -> None:
        self.request = request
        self.model_admin = model_admin
        self.instance = instance

    def __str__(self) -> str:
        return "{0}: changeform admin tools".format(self.model_admin)

    def __iter__(self):
        for changeform_tool_class in self.model_admin.get_changeform_tools():
            changeform_tool = changeform_tool_class(
                self.model_admin,
                self.instance,
            )

            if not changeform_tool.has_permission(self.request):
                continue

            changeform_tool_content = changeform_tool.get_content(
                self.request,
            )
            if not changeform_tool_content:
                continue

            yield changeform_tool_content
