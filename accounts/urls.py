from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register, name='register'),
    path('verify/<str:username>/', views.verify, name='verify_email'),
]
