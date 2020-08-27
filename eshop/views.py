from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
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
    group_one = Product.objects.all()
    group_two = Product.objects.all()

    context = { 
        'products_one': group_one,
        'products_two': group_two,
    }

    return render(req, 'pages/homepage.html', context)

def login_page(req):
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
    products = Product.objects.filter(subcategory=subcategory)
    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    }
    return render(req, 'pages/product-list.html', context)

def update_profile(req, account_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            form = CustomerForm(instance=profile)
            if req.method == 'POST':
                form = CustomerForm(req.POST, instance=profile)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(req.path_info)
            context = {
                'profile': profile,
                'account': True,
                'address': False,
                'order': False,
                'detail': False,
                'form': form
            }
            return render(req, 'pages/account-page.html', context)  
        else:
            return render(req, 'pages/403.html')
    else:
        return render(req, 'pages/404.html')
    

def account_orders(req, account_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            orders = Order.objects.filter(customer=account_id).order_by('-date_ordered')
            context = {
                'profile': profile,
                'account': False,
                'address': False,
                'order': True,
                'detail': False,
                'orders': orders
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return render(req, 'pages/403.html')
    else:
        return render(req, 'pages/404.html')

def order_details2(req, account_id, order_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            details = OrderItem.objects.filter(order=order_id)
            context = {
                'profile': profile,
                'account': False,
                'address': False,
                'order': False,
                'detail': True,
                'details': details,
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return render(req, 'pages/403.html')
    else:
        return render(req, 'pages/404.html')

def result(req):
    query = req.GET['q']
    if query != '' and query != ' ':
        products = Product.objects.filter(name__contains=query)
    else:
        products = None
    context = {
        'query': query,
        'products': products,
    }
    return render(req, 'pages/result.html', context)

def order_details(req, account_id, order_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            details = OrderItem.objects.filter(order=order_id)
            form = ReturnForm()
            if req.method == 'POST':
                form = ReturnForm(req.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.item = OrderItem.objects.get(id=req.POST.get('item'))
                    form.save()
                    return HttpResponseRedirect(req.path_info)
            context = {
                'account': False,
                'address': False,
                'order': False,
                'detail': True,
                'profile': profile,
                'details': details,
                'form': form
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return render(req, 'pages/403.html')
    else:
        return render(req, 'pages/404.html')

def create_and_update_address(req, account_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            address = ShippingAddress.objects.filter(customer=account_id)
            context = {}
            if ShippingAddress.objects.filter(customer=account_id).exists():
                address = ShippingAddress.objects.get(customer=account_id)
                form = ShippingAddressForm(instance=address)
                if req.method == 'POST':
                    form = ShippingAddressForm(req.POST, instance=address)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect(req.path_info)
            else:
                form = ShippingAddressForm()
                if req.method == 'POST':
                    form = ShippingAddressForm(req.POST)
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.customer = profile
                        form.save()
                        return HttpResponseRedirect(req.path_info)
            context = {
                'account': False,
                'address': True,
                'order': False,
                'detail': False,
                'profile': profile,
                'form': form
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return render(req, 'pages/403.html')
    else:
        return render(req, 'pages/404.html')

# For add to cart functionality
def updateItem(req):
    data = json.loads(req.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = req.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status='Pending')

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def deleteCart(req):
    customer = req.user.customer
    order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    order.delete()
    order, created = Order.objects.get_or_create(customer=customer, status='Pending')
    return JsonResponse('Order was deleted', safe=False)

def logout_view(req):
    logout(req)
    return homepage(req)