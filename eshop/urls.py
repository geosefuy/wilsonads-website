from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('product_list/', product_list, name = 'product_list'),
    path('cart/', cart, name = 'cart'),
    path('checkout/', checkout, name = 'checkout'),
    path('view-product/', product_details, name = 'product_details'),
    path('login/', login, name = 'login'),
    path('account/', account, name = 'account'),
    path('register/', register, name = 'register'),
    path('result/', result, name = 'result'),
]