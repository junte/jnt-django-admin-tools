import typing as ty

from django.contrib import admin
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from jnt_admin_tools.admin.base_changeform_submit import BaseChangeformSubmit


class ChangeformSubmitsSet:
    def __init__(
        self,
        request: HttpRequest,
        model_admin: admin.ModelAdmin,
        instance: models.Model,
    ) -> None:
        self.request = request
        self.model_admin = model_admin
        self.instance = instance
        self._submits = []

    def handle_submit(
        self,
        instance: models.Model,
    ) -> HttpResponse | None:
        for submit in self._get_submits(instance):
            if submit.name in self.request.POST:
                response = submit.handle_submit(self.request, instance)
                return response or HttpResponseRedirect(self.request.path)

    def __iter__(self) -> ty.Iterator[str]:
        yield from (
            submit.get_content() for submit in self._get_submits(self.instance)
        )

    def _get_submits(
        self,
        instance: models.Model,
    ) -> list[BaseChangeformSubmit]:
        if not self._submits:
            excluded = self.model_admin.get_exclude_changeform_submits(
                self.request,
            )
            changeform_submits = self.model_admin.get_changeform_submits(
                self.request,
                instance,
            )
            for submit_class in changeform_submits:
                if submit_class in excluded:
                    continue
                submit = submit_class(self.model_admin)
                if submit.has_permission(self.request, instance):
                    self._submits.append(submit)

        return self._submits
