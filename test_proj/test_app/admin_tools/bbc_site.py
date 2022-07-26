from jnt_admin_tools.admin.base_admin_tools import BaseChangelistTool


class BbcSiteChangelistTool(BaseChangelistTool):
    label = "BBC news"
    link_target = "_blank"

    def get_url(self, *args, **kwargs):
        return "https://www.bbc.com/"
