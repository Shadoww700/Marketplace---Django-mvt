from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
import os
import random
from groq import Groq
from dotenv import load_dotenv

AI_API_KEY = os.getenv('AI_API_KEY')
groq_client = Groq(api_key=AI_API_KEY)




def shop_home(req):
    categories = models.Category.objects.all()
    products = models.Product.objects.all().select_related('category', 'seller').order_by('-created_at')
    
    ai_response = None
    ai_query = req.GET.get('ai_query', '').strip()

    if ai_query:
        if req.user.is_authenticated:
            user_profile = req.user.profile
            my_purchases = models.Order.objects.filter(customer=req.user)
            total_spent = sum(order.total_price for order in my_purchases)
            purchase_count = my_purchases.count()
            balance = user_profile.balance

            system_prompt = (
                "Ты — продвинутый ИИ-терминал финансовой разведки в даркнет-маркетплейсе будущего (стиль киберпанк). "
                "Твоя задача — отвечать на запросы пользователя кратко, емко, используя технический/хакерский сленг, "
                "логирование, статус-коды вроде [SYSTEM READY], [ACCESS GRANTED], [CRITICAL]. "
                f"Текущий пользователь системы: {req.user.username}. "
                f"Его финансовые данные из базы данных: баланс = ${balance}, совершено покупок = {purchase_count}, общая сумма трат = ${total_spent}. "
                "Отвечай строго на русском языке, держи стиль мрачного, но полезного ИИ-ассистента."
            )

            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": ai_query}
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    max_tokens=300,
                )
                ai_response = chat_completion.choices[0].message.content
            except Exception as e:
                ai_response = f"❌ [HARDWARE ERROR] Ошибка подключения к нейросети: {str(e)}"
        else:
            ai_response = "❌ [ACCESS DENIED] Для подключения к ИИ-Ядру финансовой разведки необходимо авторизоваться в системе."

    return render(req, 'shop/home.html', {
        'categories': categories,
        'products': products,
        'ai_response': ai_response,
        'ai_query': ai_query
    })
      


@login_required
def become_seller_view(req):
    if req.user.profile.role == 'SELLER':
        return redirect('shop_home')

    existing_request = models.SellerRequest.objects.filter(user=req.user, status='PENDING').exists()
    if existing_request:
        return render(req, 'shop/become_seller.html', {
            'error': 'You already have a pending application. Please wait for administrator approval.'
        })

    if req.method == 'POST':
        message = req.POST.get('message', '').strip()

        if not message:
            return render(req, 'shop/become_seller.html', {'error': 'Please provide a message for the administrator.'})

        models.SellerRequest.objects.create(
            user=req.user,
            message=message,
            status='PENDING'
        )
        return redirect('shop_home')
    return render(req, 'shop/become_seller.html')



def is_admin(user):
    return user.is_authenticated and user.is_staff




@login_required
@user_passes_test(is_admin, login_url='shop_home')
def admin_requests_list(req):
    requests = models.SellerRequest.objects.filter(status='PENDING').select_related('user')
    return render(req, 'shop/admin_requests.html', {'requests': requests})


@login_required
@user_passes_test(is_admin, login_url='shop_home')
def approve_seller(req, request_id):
    if req.method == 'POST':
        seller_request = get_object_or_404(models.SellerRequest, id=request_id)
        
        seller_request.status = 'APPROVED'
        seller_request.save()

        profile, created = models.Profile.objects.get_or_create(user=seller_request.user)
        profile.role = 'SELLER'
        profile.save()

    return redirect('admin_requests')


@login_required
@user_passes_test(is_admin, login_url='shop_home')
def reject_seller(req, request_id):
    if req.method == 'POST':
        seller_request = get_object_or_404(models.SellerRequest, id=request_id)

        seller_request.status = 'REJECTED'
        seller_request.save()

    return redirect('admin_requests')



def is_seller(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'SELLER'

@login_required
@user_passes_test(is_seller, login_url='shop_home')
def create_product_view(req):

    categories =models.Category.objects.all()

    if req.method == 'POST':
        title = req.POST.get('title', '').strip()
        category_id = req.POST.get('category')
        price = req.POST.get('price')
        quantity = req.POST.get('quantity', 1)
        description = req.POST.get('description', '').strip()
        image = req.FILES.get('image')

        if not title or not category_id or not price or not description:
            return render(req, 'shop/create_product.html', {
                'error': 'All technical fields are required.',
                'categories': categories
            })

        try:
            category = models.Category.objects.get(id=category_id)
            
            models.Product.objects.create(
                title=title,
                category=category,
                price=price,
                quantity = quantity,
                description=description,
                image=image,
                seller=req.user 
            )
            
            return redirect('shop_home')

        except models.Category.DoesNotExist:
            return render(req, 'shop/create_product.html', {
                'error': 'Selected sector does not exist.',
                'categories': categories
            })
        except Exception as e:
            return render(req, 'shop/create_product.html', {
                'error': f'Database error: {str(e)}',
                'categories': categories
            })

    return render(req, 'shop/create_product.html', {'categories': categories})


@login_required
@user_passes_test(is_admin, login_url='shop_home')
def create_category_view(req):
    if req.method == 'POST':
        name = req.POST.get('name', '').strip()

        if not name:
            requests = models.SellerRequest.objects.filter(status='PENDING').select_related('user')
            return render(req, 'shop/admin_requests.html', {
                'requests': requests, 
                'cat_error': 'Category name cannot be empty.'
            })

        if models.Category.objects.filter(name__iexact=name).exists():
            requests = models.SellerRequest.objects.filter(status='PENDING').select_related('user')
            return render(req, 'shop/admin_requests.html', {
                'requests': requests, 
                'cat_error': f'Sector "{name}" already exists in the system.'
            })

        models.Category.objects.create(name=name)
        return redirect('shop_home')
    return redirect('admin_requests')


@login_required
def buy_product_view(req, product_id):
    if req.method == 'POST':
        product = get_object_or_404(models.Product, id=product_id)

        if product.seller == req.user:
            categories = models.Category.objects.all()
            products = models.Product.objects.all().select_related('category', 'seller').order_by('-created_at')
            return render(req, 'shop/home.html', {
                'products': products, 'categories': categories,
                'purchase_error': "Matrix Protocol Violation: You cannot purchase your own merchandise."
            })

        buyer_profile = req.user.profile

        if buyer_profile.balance < product.price:
            categories = models.Category.objects.all()
            products = models.Product.objects.all().select_related('category', 'seller').order_by('-created_at')
            return render(req, 'shop/home.html', {
                'products': products, 'categories': categories,
                'purchase_error': f"Insufficient funds. Required: ${product.price} | Your Core Balance: ${buyer_profile.balance}"
            })

        with transaction.atomic():
            buyer_profile.balance -= product.price
            buyer_profile.save()
            seller_profile = product.seller.profile
            seller_profile.balance += product.price
            seller_profile.save()
            models.Order.objects.create(
                customer=req.user,
                product=product,
                total_price=product.price,
                status='PAID'
            )
            if product.quantity > 1:
                product.quantity -= 1
                product.save()
            else:
                product.delete()
        return redirect('shop_home')
    return redirect('shop_home')


@login_required
def profile_dashboard_view(req):
    user_profile = req.user.profile
    
    my_purchases = models.Order.objects.filter(customer=req.user).select_related('product').order_by('-created_at')
    
    my_products = None
    my_sales = None
    
    if user_profile.role == 'SELLER':
        my_products = models.Product.objects.filter(seller=req.user).select_related('category').order_by('-created_at')
        my_sales = models.Order.objects.filter(product__seller=req.user).select_related('product', 'customer').order_by('-created_at')

    return render(req, 'shop/dashboard.html', {
        'profile': user_profile,
        'purchases': my_purchases,
        'products': my_products,
        'sales': my_sales
    })




from .models import Product
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        return redirect('profile_dashboard')
        
    return render(request, 'shop/delete.html', {'product': product})