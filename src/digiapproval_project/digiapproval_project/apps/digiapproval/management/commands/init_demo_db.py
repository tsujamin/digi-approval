from django.core.management.base import BaseCommand
from digiapproval_project.apps.digiapproval import test_data


class Command(BaseCommand):
    """ruby rake db:migrate"""

    args = '<>'
    help = 'Initialises the database and fills it with the test fixtures'

    def handle(self, *args, **kwargs):
        """Clears current models from tables, creates demo directorates,
        approvers, orginisations and customers"""
        testdata = test_data.TestData(_print=self.stdout.write)
        testdata.clear_data()
        testdata.create_groups()
        testdata.create_approvers()
        testdata.create_organisations()
        testdata.create_customers()
        testdata.create_workflow_specs()
        testdata.create_workflows()
