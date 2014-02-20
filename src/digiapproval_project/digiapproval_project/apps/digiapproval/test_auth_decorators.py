from django.test import TestCase
from .test_data import TestData
from django.core.urlresolvers import reverse


class AuthDecoratorUnitTest(TestCase):

    def setUp(self):
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()
        # we need workflowspecs for the approvers/delegators
        # to actually be approvers/delegators of anything
        # and therefore to pass the tests.
        self.data.create_workflow_specs()

    def test_login_required_approver(self):
        """Test the login_required_approver decorator via the approver_worklist
        view. Test with approver login: test if Cal McGregor can log in,
        test with customer login: test if Cleaver gets redirected, test with
        organisation: test if Leaky Plumbing gets redirected, test with no
        login: test if anon gets redirected."""
        response = self.client.get(reverse('approver_worklist'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(reverse('approver_worklist'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Cal.McGregor',
                          password='alwaystheminister')
        response = self.client.get(reverse('approver_worklist'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('approver_worklist'))
        self.assertEqual(response.status_code, 302)

        # todo: someone who is delegator only

    def test_login_required_delegator(self):
        """Test the login_required_approver decorator via the
        delegator_worklist view. Test with approver login: test if David Potter
        can log in, test with customer login: test if Cleaver gets redirected,
        test with organisation: test if Leaky Plumbing gets redirected; test
        with no login: test if anon gets redirected.
        """
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Cal.McGregor',
                          password='alwaystheminister')
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='David.Potter', password='harrysorrydavid')
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 302)

        # todo: someone who is delegator only

    def test_login_required_customer(self):
        """Test the login_required_approver decorator via the
        remove_parentaccounts view. Test with approver login: test if David
        Potter can log in, test with customer login: test if Cleaver gets
        redirected, test with organisation: test if Leaky Plumbing gets
        redirected; test with no login: test if anon gets redirected.
        """
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='Cal.McGregor',
                          password='alwaystheminister')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='David.Potter', password='harrysorrydavid')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)

        # todo: someone who is delegator only

    def test_login_required_organisation(self):
        """Test the login_required_approver decorator via the
        remove_parentaccounts view. Test with approver login: test if David
        Potter can log in, test with customer login: test if Cleaver gets
        redirected, test with organisation: test if Leaky Plumbing gets
        redirected; test with no login: test if anon gets redirected.
        """
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Cal.McGregor',
                          password='alwaystheminister')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='David.Potter', password='harrysorrydavid')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 200)

        # todo: someone who is delegator only
