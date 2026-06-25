from django.shortcuts import render
from .models import Product, Category

def shop_home(req):
    products = Product.objects.all().select_related('category','seller' ).order_by('-created_at')
    categories = Category.objects.all()

    if req.user.is_authenticated:
        req.user = req.user.__class__.objects.select_related('profile').get(pk=req.user.pk)

    return render(req, 'shop/home.html', {
        'products': products,
        'categories': categories
    })