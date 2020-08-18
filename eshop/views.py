from django.shortcuts import render
from .models import *

# Create your views here.

def homepage(req):
    # TODO include filter for each group
    # Limits query to 8 products for each group
    group_one = Product.objects.all()[:8]
    group_two = Product.objects.all()[:8]
    categories = Category.objects.all()
    context = { 
        'group_one_products': group_one,
        'group_two_products': group_two,
        'categories': categories
    }

    return render(req, 'pages/homepage.html', context)

def product_list(req):
    context = {}
    return render(req, 'pages/product_list.html', context)