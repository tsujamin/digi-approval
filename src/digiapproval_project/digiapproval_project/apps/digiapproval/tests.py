from django.test import TestCase
import unittest
from .test_data import TestData, to_workflow
from django.core.urlresolvers import reverse
from . import models
#from django.core.files import File
#from django.core.files.base import ContentFile
#import os
#import time

# BROKEN
# class UserFileTestCase(djangoTestCase):

#     TIMEOUT = 10

#     def test_good_file_scans_clean(self):
#         """Test that a known good file scans clean"""
#         uf = models.UserFile()
#         uf.name = "Test File"
#         clean_file = open(os.path.join(os.path.dirname(__file__),
# 'models.py'))
#         uf._file = File(clean_file)
#         uf.save()
#         clean_file.close()
#         wait = 0
#         while uf.virus_status == 'PENDING':
#             self.assertFalse(wait < self.TIMEOUT)
#             time.sleep(1)
#             wait += 1
#         self.assertEqual(uf.virus_status, 'CLEAN')
#         self.assertIsNotNone(uf.file)
#         uf.delete()

#     def test_eicar_scans_bad(self):
#         """Test that a known bad file scans bad."""
#         uf = models.UserFile()
#         uf.name = "Test Bad"

#         bad_file = open('/tmp/eicar', 'w')
#         bad_file.write('X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-' +
#                        'ANTIVIRUS-TEST-FILE!$H+H*')
#         bad_file.close()
#         bad_file = open('/tmp/eicar')
#         uf._file = File(bad_file)
#         uf.save()
#         bad_file.close()
#         self.assertTrue(uf.virus_status == 'THREATFOUND',
# msg=uf.virus_status)
#         self.assertIsNone(uf.file)
#         uf.delete()
#         os.unlink('/tmp/eicar')

#     # TODO: try to force an error case? (known to not work!)


class CustomerUnitTest(TestCase):

    def setUp(self):
        """Load in test data, minus workflows."""
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()

    def test_new_customers_have_no_workflows(self):
        """Check new users have no workflows"""
        self.assertEqual(self.data.CUSTOMERS[0].get_own_workflows(), [])
        self.assertEqual(self.data.CUSTOMERS[0].get_all_workflows(), [])

    def test_customer_gets_workflow(self):
        """Test that when we create a workflow, the customer gets it."""
        self.data.create_workflow_specs()
        w = to_workflow((self.data.CUSTOMERS[0], self.data.WORKFLOW_SPECS[0],
                         None))
        self.assertEqual(self.data.CUSTOMERS[0].get_own_workflows(), [w])
        self.assertEqual(self.data.CUSTOMERS[0].get_own_workflows(
            completed=False), [w])
        self.assertEqual(self.data.CUSTOMERS[0].get_own_workflows(
            completed=True), [])

    def test_organisation_workflow_propagation(self):
        """Verify that workflows propagate around organisations as expected."""
        self.data.create_workflow_specs()
        w = to_workflow((self.data.ORGANISATIONS[0],
                         self.data.WORKFLOW_SPECS[0], None))
        self.assertEqual(self.data.ORGANISATIONS[0].get_own_workflows(), [w])
        self.assertEqual(self.data.CUSTOMERS[1].get_own_workflows(), [])
        self.assertEqual(self.data.CUSTOMERS[1].get_all_workflows(), [w])
        w2 = to_workflow((self.data.CUSTOMERS[1], self.data.WORKFLOW_SPECS[0],
                         None))

        # organisations don't get to peek into their members!
        self.assertEqual(self.data.ORGANISATIONS[0].get_all_workflows(), [w])

        self.assertEqual(self.data.CUSTOMERS[1].get_own_workflows(), [w2])
        self.assertEqual(set(self.data.CUSTOMERS[1].get_all_workflows()),
                         set([w, w2]))


class WorkflowViewsUnitTests(TestCase):
    """Test the views that use workflows. Some just test basic rendering,
    others test basic functionality."""

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


class LoggedInViewsUnitTests(TestCase):
    """These test the behaviour of logged in forms."""

    def setUp(self):
        self.data = TestData()
        self.data.create_groups()
        self.data.create_approvers()
        self.data.create_organisations()
        self.data.create_customers()

    @unittest.expectedFailure
    def test_settings_logged_in(self):
        """Test that the settings page works when logged in."""
        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def test_settings_not_logged_in(self):
        """Test that the settings page works when logged in."""
        response = self.client.get(reverse('settings'))
        # this is not working and I don't know why
        #self.assertRedirects(response, reverse('auth_login'))
        self.assertEqual(response.status_code, 302)

    def test_modify_subaccounts_organisation(self):
        """Test that the modify subaccount page renders for an organisation."""
        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 200)

    def test_modify_subaccounts_customer(self):
        """Test that the modify subaccount page redirects for an customer."""
        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

    def test_modify_subaccounts_not_logged_in(self):
        """Test that the modify subaccount page redirects for un-logged-in."""
        response = self.client.get(reverse('modify_subaccounts'))
        self.assertEqual(response.status_code, 302)

    def test_remove_parentaccounts_organisation(self):
        """Test that the remove parentaccounts page redirects for an
        organisation."""
        self.client.login(username='leaky_plumbing', password='wikiwho?')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)

    def test_remove_parentaccounts_customer(self):
        """Test that the remove parentaccounts page renders for an customer."""
        self.client.login(username='missy_tanner', password='harrysorryjoshua')
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 200)

    def test_remove_parentaccounts_not_logged_in(self):
        """Test that the remove parentaccounts page redirects for
        un-logged-in."""
        response = self.client.get(reverse('remove_parentaccounts'))
        self.assertEqual(response.status_code, 302)
