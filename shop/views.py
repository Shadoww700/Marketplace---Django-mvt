from django.shortcuts import render
from .models import Product, Category

def shop_home(req):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    return render(req, 'shop/home.html', {
        'products': products,
        'categories': categories
    })