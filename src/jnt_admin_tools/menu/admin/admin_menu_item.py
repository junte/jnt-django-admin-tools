from jnt_admin_tools.menu.items import MenuItem


class AdminMenuItem(MenuItem):
    """Admin menu item."""

    def __init__(self, title, menu_items):
        """Initializing AdminMenuItem."""
        super().__init__(title)
        self.menu_items = menu_items

    def init_with_context(self, context):
        """Init menu items."""
        for title, url, perm in self.menu_items:
            if perm and not context.request.user.has_perm(perm):
                continue

            self.children.append(MenuItem(title, url))
