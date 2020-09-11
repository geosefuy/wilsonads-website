from django.urls import path
from .views import *


urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('product_list/<slug:category>', category_product_list, name = 'category_product_list'),
    path('product_list/<slug:category>/<slug:subcategory>', subcategory_product_list, name = 'subcategory_product_list'),
    path('checkout/', checkout, name = 'checkout'),
    path('view_product/<int:product_id>', product_details, name = 'product_details'),
    path('login/', login_page, name = 'login_page'),
    path('update_item/', updateItem, name="update_item"),
    path('delete_cart/', deleteCart, name="delete_cart"),
    path('get_product/<int:product_id>', getProduct, name="get_product"),
    path('account/<int:account_id>/', update_profile, name = 'update_profile'),
    path('account/<int:account_id>/create_and_update_address', create_and_update_address, name="create_and_update_address"),
    path('account/<int:account_id>/create_and_update_credit', create_and_update_credit, name="create_and_update_credit"),
    path('account/<int:account_id>/orders', account_orders, name = 'account_orders'),
    path('account/<int:account_id>/orders/<int:order_id>', order_details, name = 'order_details'),
    path('logout/', logout_view, name='logout_view'),
    path('search/', result, name='result'),
    path('remove_card/', remove_card, name='remove_card'),
    path('403/', error_403, name='error_403'),
    path('404/', error_404, name='error_404'),
    path('success/', success, name='success'),
]