import abc
import typing as ty

from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.contrib.auth.admin import csrf_protect_m
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.html import format_html

from jnt_admin_tools.admin.changeform_submits_set import ChangeformSubmitsSet


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

        context["changeform_submits"] = ChangeformSubmitsSet(
            request,
            self,
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

    def get_exclude_changeform_submits(self, request):
        return ()

    def get_changeform_submits(self, request, instance):  # noqa: WPS615
        return self.changeform_submits

    @csrf_protect_m
    def changeform_view(
        self,
        request,
        object_id=None,
        form_url="",
        extra_context=None,
    ):
        if request.method == "POST" and object_id:
            instance = self.get_object(request, unquote(object_id))
            response_view = ChangeformSubmitsSet(
                request,
                self,
                instance,
            ).handle_submit(instance)
            if response_view:
                return response_view

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context,
        )
