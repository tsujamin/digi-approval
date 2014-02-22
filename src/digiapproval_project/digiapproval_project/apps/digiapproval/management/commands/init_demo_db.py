from django.core.management.base import BaseCommand
from digiapproval_project.apps.digiapproval import test_data
from django.contrib.sites.models import Site


class Command(BaseCommand):
    """ruby rake db:migrate"""

    args = '<>'
    help = 'Initialises the database and fills it with the test fixtures'

    def handle(self, *args, **kwargs):
        """Clears current models from tables, creates demo directorates,
        approvers, orginisations and customers"""
        testdata = test_data.TestData(_print=self.stdout.write)
        testdata.clear_data()

        self.stdout.write("Creating sites (django.contrib.sites)")
        site = Site.objects.get_or_create(pk=1)[0]
        site.domain = "demo.digiactive.com.au:8000"
        site.name = "DigiACTive Demo"
        site.save()

        testdata.create_groups()
        testdata.create_approvers()
        testdata.create_organisations()
        testdata.create_customers()
        testdata.create_semantic_field_types()
        testdata.create_workflow_specs()
        testdata.create_workflows()
