from django.shortcuts import render
from .models import *

# Create your views here.

def homepage(req):
    context = {}
    return render(req, 'pages/homepage.html', context)

def product_list(req):
    context = {}
    return render(req, 'pages/product_list.html', context)