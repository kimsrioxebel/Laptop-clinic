# from django.urls import path
# from .views import laptop_list, laptop_detail

# urlpatterns = [
#     path('', laptop_list, name='laptop_list'),
#     path('laptop/<int:pk>/', laptop_detail, name='laptop_detail'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.laptop_list, name='laptop_list'),

    # 💻 Laptop Detail
    path('laptop/<int:pk>/', views.laptop_detail, name='laptop_detail'),

    # 🛒 Cart System
    path('add-to-cart/<int:laptop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
]
