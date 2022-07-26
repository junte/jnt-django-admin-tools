from urllib.parse import unquote

from django import forms

from jnt_admin_tools.menu.models import Bookmark


class BookmarkForm(forms.ModelForm):
    """
    This form allows users to edit bookmarks. It doesn't show the user field.
    It expects the user to be passed in from the view.
    """

    class Meta:
        fields = ("url", "title")
        model = Bookmark

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_url(self):
        url = self.cleaned_data["url"]
        return unquote(url)

    def save(self, *args, **kwargs):
        bookmark = super().save(
            commit=False,
            *args,
            **kwargs,
        )
        bookmark.user = self.user
        bookmark.save()
        return bookmark
