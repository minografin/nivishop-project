from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.Home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('cart/', views.cart_page, name="cart"),
    path('delete_cart/<str:cid>', views.delete_cart, name="delete_cart"),
    path('collections/', views.collections, name="collections"),
    path('collections/<str:Name>/', views.itemView, name="item_view"),
    path('collections/<str:CName>/<str:PName>/', views.Product_details, name="product_details"),
    path('addCart/', views.add_to_cart, name="addCart"),   
    path("")
]