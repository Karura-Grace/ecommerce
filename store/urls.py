from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('', views.product_list, name='product_list'),
    path('orders/', views.orders_list, name='orders_list'),
    path('customers/', views.customers_list, name='customers_list'),
    path('settings/', views.settings_page, name='settings'),
    path('wishlist/',views.wishlist,name='wishlist'),
    # Add other pages as needed
]