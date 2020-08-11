from django.shortcuts import render
from .models import *

# Create your views here.
def cart(req):
    context = {}
    return render(req, 'eshop/cart.html', context)

def checkout(req):
    context = {}
    return render(req, 'eshop/checkout.html', context)

def product_details(req):
    context = {}
    return render(req, 'eshop/product_details.html', context)

def homepage(req):
    context = {}
    return render(req, 'eshop/homepage.html', context)

def login(req):
    context = {}
    return render(req, 'eshop/login.html', context)

def register(req):
    context = {}
    return render(req, 'eshop/register.html', context)