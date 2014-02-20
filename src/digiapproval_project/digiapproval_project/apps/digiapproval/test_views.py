"""
Basic tests for our app views.

We deliberately do not test the following types of authentication here:
 * @login_required: it's is core Django
 * @login_required_*: they are tested in test_auth_decorators.py. We do,
                      however, assume that those tests are opaque, so we retest
                      some views used there to test the decorators.
"""

from django.test import TestCase
import unittest
from .test_data import TestData
from django.core.urlresolvers import reverse
from . import models


class LoggedInCustomerViewsUnitTests(TestCase):
    """Test forms requiring a customer login but no data."""

    def setUp(self):
        self.data = TestData()
        self.data.create_organisations()
        self.data.create_customers()
        self.client.login(username='missy_tanner', password='harrysorryjoshua')

    @unittest.expectedFailure
    def test_settings_logged_in(self):
        """Test that the settings page works when logged in."""
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def test_remove_parentaccounts_customer(self):
        """Test that the remove parentaccounts page renders for an customer."""
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 200)

    def test_applicant_home_customer(self):
        """Test that the applicant home redirects for an applicant/customer."""
        response = self.client.get(reverse('applicant_home'))
        self.assertEqual(response.status_code, 302)


class LoggedInOrganisationViewsUnitTests(TestCase):
    """Test forms requiring an organisation login but no data."""

    def setUp(self):
        self.data = TestData()
        self.data.create_organisations()
        self.data.create_customers()
        self.client.login(username='leaky_plumbing', password='wikiwho?')

    def test_modify_subaccounts_organisation(self):
        """Test that the modify subaccount page renders for an organisation."""
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 200)


class LoggedInApproverViewsUnitTests(TestCase):
    """Test forms requiring an approver login but no data."""

    def setUp(self):
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()
        self.data.create_workflow_specs()
        self.client.login(username='Cal.McGregor',
                          password='alwaystheminister')

    def test_approver_worklist(self):
        """Test that the approver worklist renders for an approver."""
        response = self.client.get(reverse('approver_worklist'))
        self.assertEqual(response.status_code, 200)


class LoggedInDelgatorViewsUnitTests(TestCase):
    """Test forms requiring a delegator login but no data."""

    def setUp(self):
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()
        self.data.create_workflow_specs()
        self.client.login(username='David.Potter',
                          password='harrysorrydavid')

    def test_delegator_worklist(self):
        """Test that the delegator worklist renders for a delegator."""
        response = self.client.get(reverse('delegator_worklist'))
        self.assertEqual(response.status_code, 200)


class WorkflowViewsUnitTests(TestCase):
    """Test the views that use workflows. Some just test basic rendering,
    others test basic functionality.
    """

    def setUp(self):
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()
        self.data.create_workflow_specs()
        self.data.create_workflows()

    def test_view_workflow(self):
        """Test that view_workflow renders something with the title of the
        application in it, iff authorised."""
        workflow = self.data.WORKFLOWS[0]

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(
            reverse('view_workflow', kwargs={'workflow_id': workflow.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(workflow.label, response.content)

        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.get(
            reverse('view_workflow', kwargs={'workflow_id': workflow.id}))
        self.assertEqual(response.status_code, 403)

    def test_workflow_state_authorised_unconfirmed(self):
        """Test if Cleaver is asked to confirm a cancel to Cleaver's
        application.

        TODO cover more of this view!!!
        """
        workflow = self.data.WORKFLOWS[0]

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.post(
            reverse('update_workflow_state',
                    kwargs={'workflow_id': workflow.id}),
            {'wf_state': 'CANCELLED'}
            )
        self.assertEqual(response.status_code, 200)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.state, 'STARTED')

    def test_workflow_state_authorised_confirmed(self):
        """Test if Cleaver can post a cancel to Cleaver's application.
        TODO cover more of this view!!!"""
        workflow = self.data.WORKFLOWS[0]

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.post(
            reverse('update_workflow_state',
                    kwargs={'workflow_id': workflow.id}),
            {'wf_state': 'CANCELLED', 'confirm': 'True'}
            )
        self.assertEqual(response.status_code, 302)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.state, 'CANCELLED')

    def test_workflow_state_unauthorised(self):
        """Test if Missy can post a cancel to Cleaver's applicataion."""
        workflow = self.data.WORKFLOWS[0]
        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.post(
            reverse('update_workflow_state',
                    kwargs={'workflow_id': workflow.id}),
            {'wf_state': 'CANCELLED', 'confirm': 'True'}
            )
        self.assertEqual(response.status_code, 403)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.state, 'STARTED')

    def test_workflow_state_authorised_nonexistent(self):
        """Test if Cleaver can post a xyzzy to Cleaver's applicataion."""
        workflow = self.data.WORKFLOWS[0]
        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.post(
            reverse('update_workflow_state',
                    kwargs={'workflow_id': workflow.id}),
            {'wf_state': 'xyzzy', 'confirm': 'True'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('not a valid state', response.content)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.state, 'STARTED')

    def test_workflow_label_authorised(self):
        """Test if Cleaver can change the title of Cleaver's application."""
        workflow = self.data.WORKFLOWS[0]
        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.post(
            reverse('update_workflow_label',
                    kwargs={'workflow_id': workflow.id}),
            {'label': 'Titled Application'}
            )
        self.assertEqual(response.status_code, 302)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.label, 'Titled Application')

    def test_workflow_label_unauthorised(self):
        """Test if Missy can change the title of Cleaver's application."""
        workflow = self.data.WORKFLOWS[0]

        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.post(
            reverse('update_workflow_label',
                    kwargs={'workflow_id': workflow.id}),
            {'label': 'Titled Application'}
            )
        self.assertEqual(response.status_code, 403)
        workflow = models.Workflow.objects.get(pk=workflow.pk)
        self.assertEqual(workflow.label, 'Untitled Application')

    def test_view_task_authorised(self):
        """Test if Cleaver can view his first ready task"""
        w = self.data.WORKFLOWS[0]
        tf = w.get_ready_task_forms(actor='CUSTOMER')[0]
        t_uuid = tf.task_model.uuid

        self.client.login(username='cleaver_g', password='fubar')
        response = self.client.get(
            reverse('view_task',
                    kwargs={'workflow_id': w.id,
                            'task_uuid': str(t_uuid)}))
        self.assertEqual(response.status_code, 200)
        # TODO: test more?

    def test_view_task_unauthorised(self):
        """Test if Missy can view Cleaver's first ready task"""
        w = self.data.WORKFLOWS[0]
        tf = w.get_ready_task_forms(actor='CUSTOMER')[0]
        t_uuid = tf.task_model.uuid

        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.get(
            reverse('view_task',
                    kwargs={'workflow_id': w.id,
                            'task_uuid': str(t_uuid)}))
        self.assertEqual(response.status_code, 403)
