"""
Basic tests for our app models.
"""

from django.test import TestCase
from .test_data import TestData, to_workflow
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
