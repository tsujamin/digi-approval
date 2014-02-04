from django.test import TestCase as TestCase
from . import models
from django.contrib.auth.models import User
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
#         clean_file = open(os.path.join(os.path.dirname(__file__), 'models.py'))
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
#         self.assertTrue(uf.virus_status == 'THREATFOUND', msg=uf.virus_status)
#         self.assertIsNone(uf.file)
#         uf.delete()
#         os.unlink('/tmp/eicar')
        
#     # TODO: try to force an error case? (known to not work!)

class CustomerUnitTest(TestCase):

    def setUp(self):
        """Create a customer and approver."""
        # todo: fixture?
        self.customer = models.CustomerAccount()
        user = User.objects.create_user('customer',
                                        'customer@digiactive.com.au',
                                        'password')
        self.customer.user = user
        self.customer.save()
        self.approver = User.objects.create_user('approver',
                                                 'approver@digiactive.com.au',
                                                 'password')
        
    def test_new_customers_have_no_workflows(self):
        """Check new users have no workflows"""
        self.assertEqual(self.customer.get_own_workflows(), [])
        self.assertEqual(self.customer.get_all_workflows(), [])

# 
# give them a workflow, check they have it
# create an organisation, and another user
# check get_all_workflows transmits through orgs as expected.

