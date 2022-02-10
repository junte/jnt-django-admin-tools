from jnt_admin_tools.admin.base_admin_tools import BaseChangeformTool


class YandexSiteChangeformTool(BaseChangeformTool):
    code = "yandex_site"
    title = "Yandex site"
    target = "_blank"

    def get_url(self, *args, **kwargs):
        return "https://yandex.ru/"
