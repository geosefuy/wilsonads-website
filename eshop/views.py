from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from .context_processor import cookieCart
import json
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

# INCOMPLETE
def checkout(req):
    customer = False
    if req.user.is_authenticated:
        print(req.user)
        customer = Customer.objects.filter(user=req.user)
    #form = CheckoutForm()
    if customer:
        customer = Customer.objects.get(user=req.user)
        order = Order.objects.get(customer=customer, status='Ordering')

        if ShippingAddress.objects.filter(customer=customer).exists():
            address = ShippingAddress.objects.get(customer=customer)
            form = CheckoutForm(initial={
                'fname': address.fname,
                'lname': address.lname,
                'address': address.address,
                'city': address.city,
                'state': address.state,
                'zipcode': address.zipcode,
                'phone': address.phone,
                'instructions': address.instructions,
            })
            if req.method == 'POST':
                form = CheckoutForm(req.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.customer = profile
                    form.status = 'Pending'
                    form.save()
                    return redirect('/')
        else:
            if req.method == 'POST':
                form = CheckoutForm(req.POST)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.customer = profile
                    form.status = 'Pending'
                    form.save()
                    return redirect('/')
        context = {
            'form': form,
            'guest': False
        }
    else:
    #GUEST CHECKOUT
        # customer = Customer.objects.get(user=req.user)
        # order = Order.objects.get(customer=customer, status='Ordering')

        # form = CheckoutForm()
        # if req.method == 'POST':
        #     form = CheckoutForm(req.POST)

        # context = {
        #     'form': form
        # }
        # return render(req, 'pages/checkout.html', context)
        pass
        context = {
            'form': form,
            'guest': True
        }
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
    categories = Category.objects.all()

    context = { 
        'products_one': group_one,
        'products_two': group_two,
        'categories': categories
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

def create_and_update_credit(req, account_id):
    hasCard = False
    last4creditnumber = '0000'
    profile = Customer.objects.filter(id=account_id)
    
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            address = ShippingAddress.objects.filter(customer=account_id)
            if req.method == 'GET':
                customer = stripe.Customer.retrieve(profile.stripe_id)
                card = (stripe.Customer.list_sources(
                    profile.stripe_id,
                    object="card",
                    limit=1,
                    ))
                if len(card) >= 1:
                    hasCard = True
                    last4creditnumber = card.data[0].last4
            elif req.method == 'POST':
                card = stripe.Customer.create_source(
                profile.stripe_id,
                source=req.POST['stripeToken'],
                )
                # print(stripe.Charge.create(
                # amount=2000,
                # currency="usd",
                # source=card.id,
                # description="My First Test Charge (created for API docs)",
                # customer=profile.stripe_id,
                # ))
                return HttpResponseRedirect(req.path_info)

            context = {
                'account': False,
                'address': False,
                'credit': True,
                'order': False,
                'detail': False,
                'profile': profile,
                'last4creditnumber': last4creditnumber,
                'hasCard': hasCard
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

    out_of_stock = False
    first_time = False
    added = False
    removed = False
    deleted = False

    customer = req.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status='Ordering')

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add' and product.stock <= orderItem.quantity:
        out_of_stock = True
    elif action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        added = True
        if orderItem.quantity == 1:
            first_time = True
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        removed = True
        if orderItem.quantity == 0:
            deleted = True
    elif action == 'delete':
        orderItem.quantity = 0
        deleted = True

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    data = {
        'productname': product.name,
        'out_of_stock': out_of_stock,
        'first_time': first_time,
        'added': added,
        'removed': removed,
        'deleted': deleted
    }

    return JsonResponse(data, safe=False)

def deleteCart(req):
    customer = req.user.customer
    order, created = Order.objects.get_or_create(customer=customer, status='Ordering')
    order.delete()
    order, created = Order.objects.get_or_create(customer=customer, status='Ordering')
    return JsonResponse('Order was deleted', safe=False)

def logout_view(req):
    logout(req)
    return homepage(req)

def getProduct(req, product_id):
    product = Product.objects.get(id=product_id)
    data = {
        'name': product.name,
        'price': product.price,
        'stock': product.stock,
        'imageURL': product.imageURL,
        'id': product.id
    }
    return JsonResponse(data)

def remove_card(req):
    if req.method == 'POST':
        customer = Customer.objects.get(user=req.user)
        card = (stripe.Customer.list_sources(
                customer.stripe_id,
                object="card",
                limit=1,
                ))
        if len(card) >= 1:
            stripe.Customer.delete_source(
            customer.stripe_id,
            card.data[0].id,
            )
        req.method = 'GET'
    return create_and_update_credit(req, customer.id)

# for signal
def stripeCallback(sender, user, **kwargs):
    customer = Customer.objects.get(user=user)
    if customer.stripe_id is None or customer.stripe_id == '' and customer.email is not None:
        new_stripe_customer = stripe.Customer.create(email=customer.email)
        customer.stripe_id = new_stripe_customer['id']
        customer.save()

def cookieCartToOrder(sender, user, request, **kwargs):
        cookieData = cookieCart(request)
        items = cookieData['items']
        customer = Customer.objects.get(user=user)
        order, created = Order.objects.get_or_create(customer=customer, status='Ordering')
        
        for item in items:
            product = Product.objects.get(id=item['id'])
            orderItem, created = OrderItem.objects.get_or_create(
                order=order, 
                product=product,
                quantity=item['quantity'],
            )
user_logged_in.connect(stripeCallback)
user_logged_in.connect(cookieCartToOrder)