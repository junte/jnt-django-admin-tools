import typing as ty
from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.http import HttpRequest, HttpResponse
from django.views import View


def wrap_model_instance_admin_view(
    model_admin: admin.ModelAdmin,
    view: ty.Type[View],
    **view_kwargs,
) -> ty.Callable[[HttpRequest, str, ...], HttpResponse]:
    """Wraps view to use at instance admin pages."""

    def wrap():
        def wrapper(request, object_id, **kwargs):
            instance = model_admin.get_object(request, unquote(object_id))
            if instance is None:
                return model_admin._get_obj_does_not_exist_redirect(
                    request,
                    model_admin.model._meta,
                    object_id,
                )

            return view.as_view(
                model_admin=model_admin,
                instance=instance,
                **view_kwargs,
            )(request, **kwargs)

        return update_wrapper(wrapper, view)

    return model_admin.admin_site.admin_view(wrap())


def wrap_model_list_admin_view(
    model_admin: admin.ModelAdmin,
    view: ty.Type[View],
    **view_kwargs,
) -> ty.Callable[[HttpRequest, ...], HttpResponse]:
    """Wraps view to use at models list admin pages."""

    def wrap():
        def wrapper(request: HttpRequest, **kwargs) -> HttpResponse:
            return view.as_view(
                model_admin=model_admin,
                **view_kwargs,
            )(request, **kwargs)

        return update_wrapper(wrapper, view)

    return model_admin.admin_site.admin_view(wrap())
