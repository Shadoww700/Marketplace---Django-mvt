from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('become-seller/', views.become_seller_view, name='become_seller'),
    path('product/add/', views.create_product_view, name='create_product'),
    path('become-seller/', views.become_seller_view, name='become_seller'),
    path('dashboard/requests/', views.admin_requests_list, name='admin_requests'),
    path('dashboard/requests/<int:request_id>/approve/', views.approve_seller, name='approve_seller'),
    path('dashboard/requests/<int:request_id>/reject/', views.reject_seller, name='reject_seller'),
    path('dashboard/category/add/', views.create_category_view, name='create_category'),
    path('product/<int:product_id>/buy/', views.buy_product_view, name='buy_product'),
    path('dashboard/', views.profile_dashboard_view, name='profile_dashboard'),
]