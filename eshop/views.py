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
    context = {}
    return render(req, 'pages/homepage.html', context)

def login(req):
    context = {}
    return render(req, 'pages/login.html', context)

def register(req):
    context = {}
    return render(req, 'pages/register.html', context)

def account(req):
    context = {}
    return render(req, 'pages/account-page.html', context)  

def product_list(req):
    context = {}
    return render(req, 'pages/product_list.html', context)

def result(req):
    context = {}
    return render(req, 'pages/result.html', context)
