from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('become-seller/', views.become_seller_view, name='become_seller'),
    path('product/add/', views.create_product_view, name='create_product'),
    path('product/<int:product_id>/edit/', views.edit_product_view, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/buy/', views.buy_product_view, name='buy_product'),
    path('product/image/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
    path('seller/<int:seller_id>/', views.seller_profile_view, name='seller_profile'),
    path('dashboard/', views.profile_dashboard_view, name='profile_dashboard'),
    path('dashboard/requests/', views.admin_requests_list, name='admin_requests'),
    path('dashboard/requests/<int:request_id>/approve/', views.approve_seller, name='approve_seller'),
    path('dashboard/requests/<int:request_id>/reject/', views.reject_seller, name='reject_seller'),
    path('dashboard/category/add/', views.create_category_view, name='create_category'),
]