from django.shortcuts import render
from .models import *

# Create your views here.

def homepage(req):
    # TODO include filter for each group
    # Limits query to 8 products for each group
    group_A_row_one_products = Product.objects.all()[:4]
    group_A_row_two_products = Product.objects.all()[4:4]
    group_B_row_one_products = Product.objects.all()[:4]
    group_B_row_two_products = Product.objects.all()[4:4]
    context = { 'group_A_row_one_products': group_A_row_one_products,
                'group_A_row_two_products': group_A_row_two_products,
                'group_B_row_one_products': group_B_row_one_products,
                'group_B_row_two_products': group_B_row_two_products,
    }
    return render(req, 'pages/homepage.html', context)

def product_list(req):
    context = {}
    return render(req, 'pages/product_list.html', context)