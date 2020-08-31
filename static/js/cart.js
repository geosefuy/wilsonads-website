function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	var className = ".cart-item-quantity-" + productId
	var classNameSubtotal = ".subtotal-" + productId
	var classNamePrice = ".price-" + productId
  	var total = $(".cart-total")
	
	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
			addItemToCart(productId);
		}
		else{
			cart[productId]['quantity'] += 1
			$(className).html(parseInt($(className).html()) + 1) 
			$(classNameSubtotal).html(parseFloat($(classNameSubtotal).html()) + parseFloat($(classNamePrice).html()))
			var newTotal = parseFloat(total.html()) + parseFloat($(classNamePrice).html())
			total.html(newTotal)
		}
		// console.log(total.html())
		// console.log($(classNamePrice).html())
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1
		$(className).html(parseInt($(className).html()) - 1)
		$(classNameSubtotal).html(parseFloat($(classNameSubtotal).html()) - parseFloat($(classNamePrice).html()))
		var newTotal = parseFloat(total.html()) - parseFloat($(classNamePrice).html())
		total.html(newTotal)

		if (cart[productId]['quantity'] <= 0){
			action = 'delete'
		}
	}

	if (action == 'delete') {
		var newTotal = parseFloat(total.html()) - (parseFloat($(classNamePrice).html()) * cart[productId]['quantity'])
		total.html(newTotal)
		delete cart[productId];
		var className1 = ".cart-item-card-" + productId;
		$(className1).remove();
	}
	

	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	//location.reload()
}

function addItemToCart(productId) {
	var url = '/get_product/' + productId

		fetch(url, {
			method:'GET',
			headers:{
				'Content-Type':'application/json',
				//'X-CSRFToken':csrftoken,
			}
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
			var product_id = data.id;
			var imageURL = data.imageURL;
			var price = data.price;
			var name = data.name;
			var stock = data.stock;

			$(".cart-card-container").append("<div class='card container-fluid d-flex justify-content-center py-4 my-4 cart-item-card-"+ product_id +" cart-item-card'><div class='row'><div class='col-2 d-flex flex-column justify-content-between align-items-center'><i data-product='" + product_id + "' data-action='add' onclick='updateCart(this)' class='fas fa-plus btn-qty update-cart'></i><h6 class='m-0 header-secondary cart-item-quantity-" + product_id + "'>1</h6><i data-product='" + product_id + "' data-action='remove' onclick='updateCart(this)' class='fas fa-minus btn-qty update-cart'></i></div><div class='col-2 d-flex align-items-center'><img class='w-100' src='" + imageURL + "' /></div><div class='col-6 d-flex align-items-center'><div class='container-fluid'><h5 class='header-secondary'>" + name + "</h5><h6 class='price'>Price: ₱ <i style='font-style: normal;' class='price-"+ product_id +"'>" + price + "</i></h6><h6 class='price'>Subtotal: ₱ <i style='font-style: normal;' class='subtotal-" + product_id + "'>" + price + "</i></h6></div></div><div class='col-2 d-flex align-items-center'><a data-product='" + product_id + "' style='color: inherit;' onclick='updateCart(this)' class='update-cart' data-action='delete'><i class='fa fa-times' aria-hidden='true'></i></a></div></div></div>");
			
			var total = $(".cart-total")
			var newTotal = parseFloat(total.html()) + parseFloat(price)
			total.html(newTotal)
		});
}

function updateCart(element){
	var productId = element.dataset.product
	var action = element.dataset.action
	console.log('productId:', productId, 'Action:', action)
	console.log('USER:', user)

	if (user == 'AnonymousUser'){
		addCookieItem(productId, action)
	}else{
		updateUserOrder(productId, action)
	}
}