from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from .context_processor import cookieCart
import json
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
import stripe
from .utils import *


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

# INCOMPLETE
def checkout(req):
    if req.user.is_authenticated:
        customer = Customer.objects.get(user=req.user)
        if req.method == 'GET':
            order = readyOrderForCheckout(customer)
            if not OrderItem.objects.filter(order=order).exists():
                order.delete()
                return redirect('/403')

        elif req.method == 'POST':
            order = Order.objects.filter(customer=customer, status='Checkout').latest('date_ordered')    

        order_items = OrderItem.objects.filter(order=order)

        cards = stripe.Customer.list_sources(
            customer.stripe_id,
            limit=1,
            object='card'
        )
        card_list = cards['data']

        if ShippingAddress.objects.filter(customer=customer).exists():
            address = ShippingAddress.objects.get(customer=customer)
            form = CheckoutForm(initial={'fname': address.fname,'lname': address.lname,
                'email': customer.email, 'address': address.address,'city': address.city,
                'state': address.state, 'zipcode': address.zipcode, 'phone': address.phone,
                'instructions': address.instructions,
            })
            if req.method == 'POST':
                form = CheckoutForm(req.POST, instance=order)
                token = False
                use_default = req.POST['use_default']
                if use_default == 'false':
                    token = req.POST['stripeToken']
                total = order.get_cart_total * 100
                if form.is_valid():
                    if use_default == 'true':
                        charge = stripe.Charge.create(
                            customer=customer.stripe_id,
                            amount=int(total),
                            currency="php",
                            description="order id: " + str(order.id),
                        )
                    else:
                        charge = stripe.Charge.create(
                            source=token,
                            amount=int(total),
                            currency='php',
                            description="order id: " + str(order.id),
                            metadata={"email": customer.email},
                        )
                    form = form.save(commit=False)
                    form.customer = customer
                    form.email = customer.email
                    form.charge_id = charge["id"]
                    if charge["status"] == 'succeeded':
                        form.status = 'Pending'
                
                    sendReceipt(order, charge["status"])
                    form.save()
                    return redirect('/success')
        else:
            form = CheckoutForm(initial={
                'email': customer.email,
            })
            if req.method == 'POST':
                form = CheckoutForm(req.POST, instance=order)
                token = False
                use_default = req.POST['use_default']
                if use_default == 'false':
                    token = req.POST['stripeToken']
                total = order.get_cart_total * 100
                if form.is_valid():
                    if use_default =='false':
                        charge = stripe.Charge.create(
                            source=token,
                            amount=int(total),
                            currency='php',
                            description="order id: " + str(order.id),
                            metadata={"email": customer.email},
                        )
                    else:
                        charge = stripe.Charge.create(
                            customer=customer.stripe_id,
                            amount=int(total),
                            currency="php",
                            description="order id: " + str(order.id),
                        )
                    form = form.save(commit=False)
                    form.customer = customer
                    form.email = customer.email
                    form.charge_id = charge["id"]
                    if charge["status"] == 'succeeded':
                        form.status = 'Pending'
                    sendReceipt(order, charge["status"])
                    form.save()
                    return redirect('/success')
        context = {
            'form': form,
            'guest': False,
            'order_items': order_items,
            'order': order
        }
        if len(card_list) > 0:
            context.update({
                'card': card_list[0]
            })
    else:
        #GUEST CHECKOUT
        if req.method == 'GET':
            order = cookie_to_order(req)
            if not OrderItem.objects.filter(order=order).exists():
                order.delete()
                return redirect('/403')
            order_items = OrderItem.objects.filter(order=order)
            req.session['order_id'] = order.id
            form = CheckoutForm()
        elif req.method == 'POST':
            order_id = req.session['order_id']
            order = Order.objects.get(id=order_id)
            order_items = OrderItem.objects.filter(order=order)
            try:
                del req.session['order_id']
            except KeyError:
                pass
            form = CheckoutForm(req.POST, instance=order)
            token = req.POST['stripeToken']
            total = order.get_cart_total * 100
            if form.is_valid():
                charge = stripe.Charge.create(
                    source=token,
                    amount=int(total),
                    currency='php',
                    description="order id: " + str(order.id),
                    metadata={"email": req.POST['email']},
                )
                if charge["status"] == 'succeeded':
                    order.status = 'Pending'
                    order.save()

                form = form.save(commit=False)
                form.charge_id = charge["id"]
                if charge["status"] == 'succeeded':
                    form.status = 'Pending'
                sendReceipt(order, charge["status"])
                form.save()
                response = redirect('/success')
                response.delete_cookie('cart')
                return response
        context = {
            'form': form,
            'guest': True,
            'order_items': order_items,
            'order': order
        }
    response = render(req, 'pages/checkout.html', context)
    response.delete_cookie('cart')
    return response

def product_details(req, product_id):
    product = Product.objects.get(id=product_id)
    gallery = Gallery.objects.filter(productid=product)
    print(gallery)
    context = {
        'product': product,
        'gallery': gallery
    }
    return render(req, 'pages/view-product.html', context)

def homepage(req):
    # TODO include filter for each group
    # Limits query to 8 products for each group
    group_one = Product.objects.filter(stock__gt=0)
    group_two = Product.objects.filter(stock__gt=0)
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
    products = Product.objects.filter(subcategory=subcategory, stock__gt=0)
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
            return redirect('/403')
    else:
        return redirect('/404')
    

def account_orders(req, account_id):
    profile = Customer.objects.filter(id=account_id)
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            orders = Order.objects.filter(customer=account_id).order_by('-date_ordered').exclude(status='Ordering')
            if req.method == 'POST':
                order = Order.objects.get(id=req.POST.get('id'))
                order.status = 'Cancelled'
                order.save()
                refund = stripe.Refund.create(
                    charge=order.charge_id,
                )
                if refund['status'] == "succeeded":
                    order.status = 'Cancelled'
                    order.save()
            context = {
                'profile': profile,
                'account': False,
                'address': False,
                'order': True,
                'detail': False,
                'orders': orders,
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return redirect('/403')
    else:
        return redirect('/404')

def result(req):
    query = req.GET['q']
    if query != '' and query != ' ':
        products = Product.objects.filter(name__contains=query, stock__gt=0)
    else:
        products = None
    context = {
        'query': query,
        'products': products,
    }
    return render(req, 'pages/result.html', context)

def order_details(req, account_id, order_id):
    profile = Customer.objects.filter(id=account_id)
    error = False
    if profile:
        profile = Customer.objects.get(id=account_id)
        if req.user == profile.user:
            item = Order.objects.get(id=order_id)
            details = OrderItem.objects.filter(order=order_id)
            form = ReturnForm()
            if req.method == 'POST':
                form = ReturnForm(req.POST)
                returns = Return.objects.filter(item=req.POST.get('item'), status='Pending').exists()
                if returns:
                    error = "Your return form for this item has not been approved. Please contact us for a follow-up instead."
                if form.is_valid() and not returns:
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
                'item': item,
                'form': form,
                'error': error
            }
            return render(req, 'pages/account-page.html', context)
        else:
            return redirect('/403')
    else:
        return redirect('/404')

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
            return redirect('/403')
    else:
        return redirect('/404')

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
            return redirect('/403')
    else:
        return redirect('/404')

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
            orderItem.delete()
            deleted = True
    elif action == 'delete':
        orderItem.quantity = 0
        orderItem.delete()
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

# For add to cart functionality
def update_quantity(req):
    data = json.loads(req.body)
    productId = data['productId']
    quantity = int(data['quantity'])

    out_of_stock = False
    first_time = False
    added = False

    customer = req.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status='Ordering')

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if quantity != 0:
        if orderItem.quantity == 0:
            first_time = True

        if product.stock < orderItem.quantity + quantity:
            out_of_stock = True
        else:
            orderItem.quantity = (orderItem.quantity + quantity)
            orderItem.save()
            added = True
    
    if orderItem.quantity == 0:
        orderItem.delete()
    
    data = {
        'productname': product.name,
        'out_of_stock': out_of_stock,
        'first_time': first_time,
        'added': added,
    }

    return JsonResponse(data, safe=False)

def deleteCart(req):
    customer = req.user.customer
    order, created = Order.objects.get_or_create(customer=customer, status='Ordering')
    OrderItem.objects.filter(order=order).delete()
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

#for guest checkout
def cookie_to_order(req):
    cookieData = cookieCart(req)
    items = cookieData['items']
    order = Order.objects.create(status='Checkout')
    for item in items:
            product = Product.objects.get(id=item['id'])
            orderItem = OrderItem.objects.create(
                order=order, 
                product=product,
                quantity=item['quantity'],
            )
            product.stock = product.stock - orderItem.quantity
            product.save()
            if orderItem.quantity == 0:
                orderItem.delete()
    return order

def readyOrderForCheckout(customer):
    order = Order.objects.get(customer=customer, status="Ordering")
    order.status = "Checkout"
    items = order.orderitem_set.all()

    for item in reversed(items):
        product = Product.objects.get(id=item.product.id)
        product.stock = product.stock - item.quantity
        product.save()
        if item.quantity == 0:
                item.delete()

    order.save()
    return order

def success(req):
    return render(req, 'pages/success.html')

def error_403(req):
    return render(req, 'pages/403.html')
    
def error_404(req):
    return render(req, 'pages/404.html')

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