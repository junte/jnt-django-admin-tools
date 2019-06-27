from functools import reduce, wraps

from admin_tools.services.urls import admin_change_url, admin_changelist_url
from django.forms.forms import pretty_name
from django.utils.html import format_html


def getattr_nested(obj, attr):
    return reduce(getattr, [obj] + attr.split('__'))


def admin_link(attr, short_description=None, empty_description="-"):
    """Decorator used for rendering a link to a related model in
    the admin detail page.

    ``attr (str)``
        Name of the related field.
    ``short_description (str)``
        Name if the field.
        Default value: None.
    ``empty_description (str)``
        Value to display if the related field is None.
        Default value: -.

    The wrapped method receives the related object and should
    return the link text.

    Usage::

        from django.contrib import admin
        from admin_tools.decorators import admin_link
        from test_app.models import Foo

        @admin.register(Foo)
        class FooAdmin(admin.ModelAdmin):
            fields = ('name', 'bar', 'bar_link')
            readonly_fields = ('bar_link',)

            @admin_link('bar')
            def bar_link(self, obj):
                return obj.name

    .. image:: images/decorators/decorator_admin_link.png
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
    a related model in the admin changelist page.

    ``attr (str)``
        Name of the related field.
    ``short_description (str)``
        Field display name.
        Default value: None.
    ``empty_description (str)``
        Value to display if the related field is None.
        Default value: -.
    ``query_string (function)``
        Optional callback for adding a query string to the link.
        Receives the object and should return a query string.
        Default value: None.

    The wrapped method receives the related object and
    should return the link text.

    Usage::

        from admin_tools.decorators import admin_changelist_link
        from django.contrib import admin
        from test_app.models import Bar

        @admin.register(Bar)
        class BarAdmin(admin.ModelAdmin):
            fields = ('name', 'foos', 'custom_field')
            readonly_fields = ('foos', 'custom_field')

            @admin_changelist_link('foos', query_string=lambda bar: f'bar_id={bar.pk}')
            def foos(self, foos):
                return ', '.join(str(foo) for foo in foos.all())

    .. image:: images/decorators/decorator_admin_changelist_link.png
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


def admin_field(short_description=None, allow_tags=True):
    """Decorator used for custom field or add link in
    the admin detail page.

    ``short_description (str)``
        Description of the field.
    ``allow_tags (bool)``
        Allow tags.

    The wrapped method receives the custom field.

    Usage::

        from admin_tools.decorators import admin_field
        from django.contrib import admin
        from django.utils.safestring import mark_safe
        from test_app.models import Bar

        @admin.register(Bar)
        class BarAdmin(admin.ModelAdmin):
            fields = ('name', 'foos', 'custom_field')
            readonly_fields = ('foos', 'custom_field')

            @admin_field('Custom field')
            def custom_field(self, obj):
                return mark_safe('<h1>custom field</h1>')

    .. image:: images/decorators/decorator_admin_field.png
    """

    def wrap(func):
        @wraps(func)
        def field_func(self, obj):
            return func(self, obj)

        field_func.short_description = short_description
        field_func.allow_tags = allow_tags
        return field_func

    return wrap
