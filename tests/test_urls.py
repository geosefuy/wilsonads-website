from django.test import SimpleTestCase
from django.urls import reverse, resolve
from eshop.views import *

class TestUrls(SimpleTestCase):

    def test_homepage(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_checkout(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_login_page(self):
        url = reverse('login_page')
        self.assertEquals(resolve(url).func, login_page)

    def test_updateItem(self):
        url = reverse('update_item')
        self.assertEquals(resolve(url).func, updateItem)

    def test_logout_view(self):
        url = reverse('logout_view')
        self.assertEquals(resolve(url).func, logout_view)

    def test_result(self):
        url = reverse('result')
        self.assertEquals(resolve(url).func, result)

    def test_category_list(self):
        url = reverse('category_product_list', args=['category'])
        self.assertEquals(resolve(url).func, category_product_list)

    def test_subcategory_list(self):
        url = reverse('subcategory_product_list', args=['category', 'subcategory'])
        self.assertEquals(resolve(url).func, subcategory_product_list)

    def test_product_details(self):
        url = reverse('product_details', args=[1])
        self.assertEquals(resolve(url).func, product_details)

    def test_update_profile(self):
        url = reverse('update_profile', args=[1])
        self.assertEquals(resolve(url).func, update_profile)

    def test_create_and_update_address(self):
        url = reverse('create_and_update_address', args=[1])
        self.assertEquals(resolve(url).func, create_and_update_address)

    def test_account_orders(self):
        url = reverse('account_orders', args=[1])
        self.assertEquals(resolve(url).func, account_orders)

    def test_order_details(self):
        url = reverse('order_details', args=[1, 2])
        self.assertEquals(resolve(url).func, order_details)
