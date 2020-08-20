from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('product_list/<slug:category>', category_product_list, name = 'category_product_list'),
    path('product_list/<slug:category>/<slug:subcategory>', subcategory_product_list, name = 'subcategory_product_list'),
    path('checkout/', checkout, name = 'checkout'),
    path('view-product/<int:product_id>', product_details, name = 'product_details'),
    path('login/', login, name = 'login'),
    path('account/<int:account_id>/', account_profile, name = 'account_profile'),
    path('account/<int:account_id>/address', account_address, name = 'account_address'),
    path('account/<int:account_id>/orders', account_orders, name = 'account_orders'),
    path('update_item/', updateItem, name="update_item"),
]