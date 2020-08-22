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
    path('account/<int:account_id>/', update_profile, name = 'update_profile'),
    path('account/<int:account_id>/change_password', change_password, name = 'change_password'),
    path('account/<int:account_id>/create_and_update_address', create_and_update_address, name="create_and_update_address"),
    path('account/<int:account_id>/orders', account_orders, name = 'account_orders'),
    path('logout/', logout_view, name='logout_view'),
]