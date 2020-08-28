from django.test import TestCase, Client
from django.urls import reverse
from eshop.models import *
import json


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        # self.homepage_url = reverse('homepage')
        # self.checkout_url = reverse('checkout')
        # self.login_page_url = reverse('login_page')
        # self.logout_view_url = reverse('logout_view')
        # self.result_url = reverse('result')
        # self.category_product_list_url = reverse('category_product_list', args=['category'])
        # self.subcategory_product_list_url = reverse('subcategory_product_list', args=['category', 'subcategory'])
        self.product_details_url = reverse('product_details', args=[1])
        self.update_profile_url = reverse('update_profile', args=[1])
        # self.create_and_update_address_url = reverse('create_and_update_address', args=[1])
        # self.account_orders_url = reverse('account_orders', args=[1])
        # self.order_details_url = reverse('order_details', args=[1, 2])

    def test_product_details_GET(self):
        cat = Category.objects.create(
            name="Laptops",
            slug="laptop"
        )
        subcat = SubCategory.objects.create(
            category=cat,
            name="Gaming Laptops",
            slug="gaming-laptops"
        )
        prod = Product.objects.create(
            subcategory=subcat,
            name="ACER Gaming Laptop",
            price=22000.99,
            stock=2,
            description="Hello world"
        )
        Gallery.objects.create(
            productid=prod
        )
        response = self.client.get(self.product_details_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/view-product.html')