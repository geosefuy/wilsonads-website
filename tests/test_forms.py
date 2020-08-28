from django.test import TestCase
from eshop.forms import *

class TestForms(TestCase):
    def test_update_profile1(self):
        form = CustomerForm(data={
            'fname': 'Patrick',
            'lname': 'Star'
        })
        self.assertTrue(form.is_valid())

    def test_update_profile2(self):
        form = CustomerForm(data={
            'fname': 'Patrick Harry',
            'lname': 'Star'
        })
        self.assertTrue(form.is_valid())
    
    def test_update_profile_no_data(self):
        form = CustomerForm(data={
            'fname': '',
            'lname': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_update_profile_invalid_data1(self):
        form = CustomerForm(data={
            'fname': 'Pat2',
            'lname': 'Star'
        })
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_update_profile_invalid_data2(self):
        form = CustomerForm(data={
            'fname': 'Patrick',
            'lname': 'Sta1r'
        })
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
