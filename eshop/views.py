from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.

def checkout(req):
    context = {}
    return render(req, 'pages/checkout.html', context)

def product_details(req, product_id):
    product = Product.objects.get(id=product_id)
    gallery = Gallery.objects.get(productid=product_id)
    context = {
        'product': product,
        'gallery': gallery
    }
    return render(req, 'pages/view-product.html', context)

def homepage(req):
    # TODO include filter for each group
    # Limits query to 8 products for each group
    group_one = Product.objects.all()[:8]
    group_two = Product.objects.all()[:8]

    context = { 
        'group_one_products': group_one,
        'group_two_products': group_two,
        
    }

    return render(req, 'pages/homepage.html', context)

def login(req):
    context = {}
    return render(req, 'pages/login.html', context)
    
#category in argument is in slug form  
def category_product_list(req, category):
    category = Category.objects.get(slug=category)
    context = {
        'category': category,
    }
    return render(req, 'pages/product_list.html', context)

#subcategory and category in argument are in slug form  
def subcategory_product_list(req, category, subcategory):
    category = Category.objects.get(slug=category)
    subcategory = SubCategory.objects.get(slug=subcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
    }
    return render(req, 'pages/product_list.html', context)

def account_profile(req, account_id):
    profile = Customer.objects.get(id=account_id)
    context = {
        'profile': profile,
    }
    return render(req, 'pages/account-page.html', context)  

def account_orders(req, account_id):
    orders = Orders.objects.get(customer=account_id)
    context = {
        'profile': profile,
        'orders': orders
    }
    return render(req, 'pages/account-page.html', context)  

def account_address(req, account_id):
    address = ShippingAddress.objects.get(customer=account_id)
    profile = Customer.objects.get(id=account_id)
    context = {
        'address': address,
        'profile': profile
    }
    return render(req, 'pages/account-page.html', context)  

def result(req):
    context = {}
    return render(req, 'pages/result.html', context)

# For add to cart functionality
def updateItem(req):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)