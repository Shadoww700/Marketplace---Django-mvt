from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('become-seller/', views.become_seller_view, name='become_seller'),
]