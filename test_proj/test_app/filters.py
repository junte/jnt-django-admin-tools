from jnt_admin_tools.autocomplete_filter import AutocompleteFilter


class BarAutocompleteFilter(AutocompleteFilter):
    title = "Bar"
    field_name = "bar"


class TagsAutocompleteFilter(AutocompleteFilter):
    title = "Tags"
    field_name = "tags"
    is_multiple = True
