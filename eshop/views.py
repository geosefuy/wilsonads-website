from django.shortcuts import render
from .models import *

# Create your views here.
def cart(req):
    context = {}
    return render(req, 'pages/cart.html', context)

def checkout(req):
    context = {}
    return render(req, 'pages/checkout.html', context)

def product_details(req):
    context = {}
    return render(req, 'pages/view-product.html', context)

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

def login(req):
    context = {}
    return render(req, 'pages/login.html', context)
    
#category in argument is in slug form  
def product_list(req, category):
    category = Category.objects.get(slug=category)
    context = {
        'category': category,
    }
    return render(req, 'pages/product_list.html', context)

def account(req):
    context = {}
    return render(req, 'pages/account-page.html', context)  

def result(req):
    context = {}
    return render(req, 'pages/result.html', context)
