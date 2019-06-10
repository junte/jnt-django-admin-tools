from functools import reduce, wraps

from admin_tools.services.urls import admin_change_url, admin_changelist_url
from django.forms.forms import pretty_name
from django.utils.html import format_html


def getattr_nested(obj, attr):
    return reduce(getattr, [obj] + attr.split('__'))


def admin_link(attr, short_description=None, empty_description="-"):
    """Decorator used for rendering a link to a related model in
    the admin detail page.
    attr (str):
        Name of the related field.
    short_description (str):
        Name if the field.
    empty_description (str):
        Value to display if the related field is None.
    The wrapped method receives the related object and should
    return the link text.
    Usage:
        @admin_link('credit_card', _('Credit Card'))
        def credit_card_link(self, credit_card):
            return credit_card.name
    """

    def wrap(func):
        @wraps(func)
        def field_func(self, obj):
            related_obj = getattr_nested(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_change_url(related_obj)
            return format_html('<a href="{}">{}</a>', url, func(self, related_obj))

        field_func.short_description = short_description if short_description else pretty_name(attr)
        field_func.allow_tags = True
        return field_func

    return wrap


def admin_changelist_link(attr, short_description=None, empty_description="-", query_string=None):
    """Decorator used for rendering a link to the list display of
    a related model in the admin detail page.
    attr (str):
        Name of the related field.
    short_description (str):
        Field display name.
    empty_description (str):
        Value to display if the related field is None.
    query_string (function):
        Optional callback for adding a query string to the link.
        Receives the object and should return a query string.
    The wrapped method receives the related object and
    should return the link text.
    Usage:
        @admin_changelist_link('products', _('Products'), query_string=lambda c: 'category_id={}'.format(c.pk))
        def credit_card_link(self, credit_card):
            return credit_card.name
    """

    def wrap(func):
        @wraps(func)
        def field_func(self, obj):
            related_obj = getattr_nested(obj, attr)
            if related_obj is None:
                return empty_description
            url = admin_changelist_url(related_obj.model)
            if query_string:
                url += '?' + query_string(obj)
            return format_html('<a href="{}">{}</a>', url, func(self, related_obj))

        field_func.short_description = short_description if short_description else pretty_name(attr)
        field_func.allow_tags = True
        return field_func

    return wrap


def admin_field(short_description=None, empty_description='-', allow_tags=True):
    """Decorator used for rendering a link to a related model in
    the admin detail page.
    attr (str):
        Name of the related field.
    short_description (str):
        Name if the field.
    allow_tags (bool):
        Allow tags.
    The wrapped method receives the related object and should
    return the link text.
    Usage:
        @admin_link('change password', _('Change password'))
        def change_password(self, obj):
            return format_html(f'<a href="{obj.id}/password/">change password</a>')
    """

    def wrap(func):
        @wraps(func)
        def field_func(self, obj):
            return func(self, obj)

        field_func.short_description = short_description
        field_func.allow_tags = allow_tags
        return field_func

    return wrap
