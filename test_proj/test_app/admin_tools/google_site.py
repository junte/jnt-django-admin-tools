from jnt_admin_tools.admin.base_admin_tools import BaseChangeformTool


class GoogleSiteChangeformTool(BaseChangeformTool):
    code = "google_site"
    title = "Google site"
    target = "_blank"

    def get_url(self, *args, **kwargs):
        return "https://google.com/"
