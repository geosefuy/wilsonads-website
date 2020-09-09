from .models import *
import json

# Used in rendering categories/subcategories in navbar 
def product_categories(req):
	categories = Category.objects.all()
	return {'categories': categories}

# Used in rendering cart
def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			product = Product.objects.get(id=i)
			if product.stock < cart[i]['quantity']:
				cart[i]['quantity'] = product.stock

			cartItems += cart[i]['quantity']
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				# 'digital':product.digital,'get_total':total,
				}
			items.append(item)

			# if product.digital == False:
			# 	order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(req):
	if req.user.is_authenticated:
		customer = req.user.customer
		order, created = Order.objects.get_or_create(customer=customer, status='Ordering')
		items = order.orderitem_set.all()

		for item in items:
			if item.product.stock < item.quantity:
				item.quantity = item.product.stock
				item.save()

		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(req)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order_':order, 'items':items}

def customerData(req):
	if req.user.is_authenticated:
		customer = Customer.objects.get(user=req.user)
		return {'customer_id': customer.id, 'customer_fname': customer.fname, 'customer_lname': customer.lname, 'customer_email': customer.email}
	else:
		return {}
