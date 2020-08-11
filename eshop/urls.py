from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name = 'homepage'),
    path('cart/', cart, name = 'cart'),
    path('checkout/', checkout, name = 'checkout'),
    path('product_details/', product_details, name = 'product_details'),
    path('login/', login, name = 'login'),
    path('register/', register, name = 'register'),
]