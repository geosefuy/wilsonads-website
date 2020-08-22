from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from .forms import *
import json
from django.contrib.auth import logout

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

def login_page(req):

    # if req.method == "POST":
    #     username = req.POST.get('username')
    #     password = req.POST.get('password')
    #     user = authenticate(request, username=username, password=password)

    #     if user is not None:
    #         login(req, user)
    #         return redirect('/')
    context = {}
    return render(req, 'pages/login.html', context)
    
#category in argument is in slug form  
def category_product_list(req, category):
    category = Category.objects.get(slug=category)
    context = {
        'category': category,
    }
    return render(req, 'pages/product-list.html', context)

#subcategory and category in argument are in slug form  
def subcategory_product_list(req, category, subcategory):
    category = Category.objects.get(slug=category)
    subcategory = SubCategory.objects.get(slug=subcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
    }
    return render(req, 'pages/product-list.html', context)

def update_profile(req, account_id):
    profile = Customer.objects.get(id=account_id)
    form = CustomerForm(instance=profile)
    if req.method == 'POST':
        form = CustomerForm(req.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'profile': profile,
        'account': True,
        'pw': False,
        'address': False,
        'order': False,
        'form': form
    }
    return render(req, 'pages/account-page.html', context)  

def account_orders(req, account_id):
    orders = Order.objects.filter(customer=account_id)
    profile = Customer.objects.get(id=account_id)
    if Order.objects.filter(customer=account_id).exists():
        orders = Order.objects.filter(customer=account_id)
    else:
        orders = Order.objects.filter(customer=account_id).count()
    context = {
        'profile': profile,
        'account': False,
        'pw': False,
        'address': False,
        'order': True,
        'orders': orders
    }
    return render(req, 'pages/account-page.html', context)  

def change_password(req, account_id):
    profile = Customer.objects.get(id=account_id)
    user = profile.user
    if req.method == "POST":
        curr_password = req.POST.get("curr_password")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm_password")

        #user = authenticate(req, username=username, password=password)

        # if user is not None:
        #     login(req, user)
        #     redirect('/')
    context = {
        'account': False,
        'pw': True,
        'address': False,
        'order': False,
        'profile': profile,
        'form': form,
    }
    return render(req, 'pages/account-page.html', context)

def result(req):
    context = {}
    return render(req, 'pages/result.html', context)

def create_and_update_address(req, account_id):
    address = ShippingAddress.objects.filter(customer=account_id)
    profile = Customer.objects.get(id=account_id)
    context = {}
    if ShippingAddress.objects.filter(customer=account_id).exists():
        address = ShippingAddress.objects.get(customer=account_id)
        form = ShippingAddressForm(instance=address)
        if req.method == 'POST':
            form = ShippingAddressForm(req.POST, instance=address)
            if form.is_valid():
                form.save()
                return redirect('/')
    else:
        form = ShippingAddressForm()
        if req.method == 'POST':
            form = ShippingAddressForm(req.POST)
            if form.is_valid():
                print("VALID POST")
                form = form.save(commit=False)
                form.customer = profile
                form.save()
                return redirect('/')
    context = {
        'account': False,
        'pw': False,
        'address': True,
        'order': False,
        'profile': profile,
        'form': form
    }
    return render(req, 'pages/account-page.html', context)

# For add to cart functionality
def updateItem(req):
	data = json.loads(req.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = req.user.customer
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

def logout_view(req):
    logout(req)
    return homepage(req)