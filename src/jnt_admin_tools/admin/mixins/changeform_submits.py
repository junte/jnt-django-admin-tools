from django.contrib.admin.utils import unquote
from django.contrib.auth.admin import csrf_protect_m
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from jnt_admin_tools.admin.base_changeform_submit import BaseChangeformSubmit


class ChangeFormSubmitsMixin:
    changeform_submits = ()

    def render_change_form(
        self,
        request,
        context,
        add=False,
        change=False,
        form_url="",
        obj=None,  # noqa: WPS110
    ):
        context["changeform_submits"] = self._get_submits_for_instance(
            request,
            obj,
        )

        return super().render_change_form(
            request,
            context,
            add,
            change,
            form_url,
            obj,
        )

    def get_exclude_changeform_submits(self, request: HttpRequest):
        return ()

    def get_changeform_submits(  # noqa: WPS615
        self,
        request: HttpRequest,
        instance,
    ):
        return self.changeform_submits

    @csrf_protect_m
    def changeform_view(
        self,
        request: HttpRequest,
        object_id=None,
        form_url="",
        extra_context=None,
    ) -> HttpResponse:
        if request.method == "POST" and object_id:
            instance = self.get_object(request, unquote(object_id))

            for submit in self._get_submits_for_instance(request, instance):
                if submit.name in request.POST:
                    response = submit.handle_submit(request, instance)
                    return response or HttpResponseRedirect(request.path)

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context,
        )

    def _get_submits_for_instance(
        self,
        request: HttpRequest,
        instance: models.Model,
    ) -> list[BaseChangeformSubmit]:
        excluded = self.get_exclude_changeform_submits(request)
        changeform_submits = self.get_changeform_submits(request, instance)
        submits = []
        for submit_class in changeform_submits:
            if submit_class in excluded:
                continue

            submit = submit_class(self)
            if submit.has_permission(request, instance):
                submits.append(submit)

        return submits
