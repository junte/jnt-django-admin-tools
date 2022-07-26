from jnt_admin_tools.admin.base_admin_tools import BaseChangeformTool


class YandexSiteChangeformTool(BaseChangeformTool):
    label = "Yandex site"
    link_target = "_blank"

    def get_url(self, *args, **kwargs):
        return "https://yandex.ru/"
