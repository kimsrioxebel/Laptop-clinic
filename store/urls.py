from django.urls import path
from .views import laptop_list, laptop_detail

urlpatterns = [
    path('', laptop_list, name='laptop_list'),
    path('laptop/<int:pk>/', laptop_detail, name='laptop_detail'),
]
