from django.urls import path
from . views import *

urlpatterns = [
    path("", product_list, name="product_list"),
    path("add/<pk>", cart_add, name="cart_add"),
    path("remove/<pk>", cart_remove, name="cart_remove"),
    path("cart", cart_detail, name="cart_detail"), 
    path("checkout/", checkout, name="checkout"),
    
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path('profile_update/', profile_update, name='profile_update'),
    path('profile/', profile_info, name='profile'),
    path('my_products',my_products,name='my_products'),
    path('search/',search_view,name='search'),
    path('detail_product/<pk>',product_details,name='detail_product'),
]