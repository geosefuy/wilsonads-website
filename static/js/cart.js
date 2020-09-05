

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
			if (data.first_time) {
				addItemToCart(productId)
			}
			else if (data.added) {
				updateAdd(productId)
			}
			else if (data.out_of_stock) {
				alert(data.productname + " is out of stock")
			}
			else if (data.deleted) {
				updateDelete(productId)
			}
			else if (data.removed) {
				updateRemove(productId)
			}
			updateCheckoutBtn()
		});
}

function addCookieItem(productId, action){
	
	if (action == 'add'){
		if (cart[productId] == undefined){
			cart[productId] = {'quantity':1}
			addItemToCart(productId);
			updateCookie()
		}
		else {
			var url = '/get_product/' + productId

			fetch(url, {method:'GET'}).then((response) => {return response.json();})
			.then((data) => {
				var name = data.name;
				var stock = data.stock;
				
				if (stock > cart[productId]['quantity']) {
					cart[productId]['quantity'] += 1
					updateCookie()
					updateAdd(productId)
					updateCheckoutBtn()
				}
				else {
					alert(name + " is out of stock");
				}
			});
		}
	}

	else if (action == 'remove'){
		updateRemove(productId)
		cart[productId]['quantity'] -= 1
		updateCookie()
		updateCheckoutBtn()

		if (cart[productId]['quantity'] <= 0){
			action = 'delete'
		}
	}

	if (action == 'delete') {
		updateDelete(productId)
		delete cart[productId];
		updateCookie()
		updateCheckoutBtn()
	}
}

function addItemToCart(productId) {
	var url = '/get_product/' + productId

		fetch(url, {method:'GET'}).then((response) => {return response.json();})
		.then((data) => {
			var product_id = data.id;
			var imageURL = data.imageURL;
			var price = data.price;
			var name = data.name;
			
			var stringDOM = `<div class='card container-fluid d-flex justify-content-center py-2 my-4 cart-item-card-`+ product_id +` cart-item-card'>
								<div class='row'>
									<div class='col-2 d-flex flex-column justify-content-between align-items-center py-3'>
										<i data-product='` + product_id + `' data-action='add' onclick='updateCart(this)' class='fas fa-plus btn-qty update-cart'></i>
										<h6 class='m-0 header-secondary cart-item-quantity-` + product_id + `'>1</h6>
										<i data-product='` + product_id + `' data-action='remove' onclick='updateCart(this)' class='fas fa-minus btn-qty update-cart'></i>
									</div>
									<div class='col-3 d-flex align-items-center'>
										<img class='w-100' src='` + imageURL + `' />
									</div>
									<div class='col-5 d-flex align-items-center'>
										<div class='container-fluid'>
											<h5 class='header-secondary text-truncate'>` + name + `</h5>
											<h6 class='price'>Price: ₱ <i style='font-style: normal;' class='price-`+ product_id +`'>` + parseFloat(price.toFixed(2)).toLocaleString('en') + `</i></h6>
											<h6 class='price'>Subtotal: ₱ <i style='font-style: normal;' class='subtotal-` + product_id + `'>` + parseFloat(price.toFixed(2)).toLocaleString('en') + `</i></h6>
										</div>
									</div>
									<div class='col-2 d-flex justify-content-center align-items-center'>
									<a data-product='` + product_id + `' style='color: inherit;' onclick='updateCart(this)' class='update-cart' data-action='delete'><i class='fa fa-times' aria-hidden='true'></i></a>
									</div>
								</div>
							</div>`;

			$(".cart-card-container").append(stringDOM);		
						
			var total = $(".cart-total")
			var newTotal = parseFloat(total.html().replace(',','')) + parseFloat(price)
			total.html(parseFloat(newTotal.toFixed(2)).toLocaleString('en'))
			
			updateCheckoutBtn()
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

function updateAdd(productId) {
	var className = ".cart-item-quantity-" + productId
	var classNameSubtotal = ".subtotal-" + productId
	var classNamePrice = ".price-" + productId
	var total = $(".cart-total")

	$(className).html(parseInt($(className).html()) + 1) 
	var subtotal = parseFloat($(classNameSubtotal).html().replace(',','')) + parseFloat($(classNamePrice).html().replace(',',''))
	$(classNameSubtotal).html(parseFloat(subtotal.toFixed(2)).toLocaleString('en'))
	var newTotal = parseFloat(total.html().replace(',','')) + parseFloat($(classNamePrice).html().replace(',',''))
	total.html(parseFloat(newTotal.toFixed(2)).toLocaleString('en'))
}

function updateRemove(productId) {
	var className = ".cart-item-quantity-" + productId
	var classNameSubtotal = ".subtotal-" + productId
	var classNamePrice = ".price-" + productId
	var total = $(".cart-total")

	$(className).html(parseInt($(className).html() - 1))
	var subtotal = parseFloat($(classNameSubtotal).html().replace(',','')) - parseFloat($(classNamePrice).html().replace(',',''))
	$(classNameSubtotal).html(parseFloat(subtotal.toFixed(2)).toLocaleString('en'))
	var newTotal = parseFloat(total.html().replace(',','')) - parseFloat($(classNamePrice).html().replace(',',''))
	total.html(parseFloat(newTotal.toFixed(2)).toLocaleString('en'))
}

function updateDelete(productId) {
	var classNameSubtotal = ".subtotal-" + productId
	var total = $(".cart-total")

	var newTotal = parseFloat(total.html().replace(',','')) - (parseFloat($(classNameSubtotal).html().replace(',','')))
	total.html(parseFloat(newTotal.toFixed(2)).toLocaleString('en'))
	var className1 = ".cart-item-card-" + productId;
	$(className1).remove();
}

function updateCookie() {
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	console.log(document.cookie)
}

function updateCheckoutBtn() {
	if ($('.cart-item-card').length)
		$("#checkout-btn").attr("disabled", false)
	else $("#checkout-btn").attr("disabled", true)
}