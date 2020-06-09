from django.core.management import BaseCommand

from jnt_admin_tools.dashboard.models import DashboardPreferences


class Command(BaseCommand):
    help = """Clears dashboard preferences."""

    def handle(self, *args, **options):
        DashboardPreferences._default_manager.all().delete()
