from django.contrib import messages
from django.db import models
from django.http import HttpRequest

from jnt_admin_tools.admin.base_changeform_submit import BaseChangeformSubmit


class ReloadSubmit(BaseChangeformSubmit):
    name = "_reload"
    title = "Reload"

    def handle_submit(
        self,
        request: HttpRequest,
        instance: models.Model,
    ) -> None:
        self.model_admin.message_user(
            request,
            "Page reloaded",
            messages.SUCCESS,
        )
