from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
import os
from groq import Groq
from django.db.models import Q

AI_API_KEY = os.getenv('AI_API_KEY')
groq_client = Groq(api_key=AI_API_KEY)


def shop_home(req):
    categories = models.Category.objects.all()
    products = models.Product.objects.all().select_related('category', 'seller').order_by('-created_at')

    ai_response = None
    ai_query = req.GET.get('ai_query', '').strip()

    category_id = req.GET.get('cat')
    if category_id:
        products = products.filter(category_id=category_id)

    search_query = req.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

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
            'error': 'У вас уже есть ожидающая заявка. Дождитесь решения администратора.'
        })

    if req.method == 'POST':
        message = req.POST.get('message', '').strip()
        if not message:
            return render(req, 'shop/become_seller.html', {'error': 'Напишите сообщение для администратора.'})

        models.SellerRequest.objects.create(user=req.user, message=message, status='PENDING')
        return redirect('shop_home')

    return render(req, 'shop/become_seller.html')


def is_admin(user):
    return user.is_authenticated and user.is_staff


def is_seller(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'SELLER'



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

        profile, _ = models.Profile.objects.get_or_create(user=seller_request.user)
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


@login_required
@user_passes_test(is_admin, login_url='shop_home')
def create_category_view(req):
    if req.method == 'POST':
        name = req.POST.get('name', '').strip()
        pending_requests = models.SellerRequest.objects.filter(status='PENDING').select_related('user')

        if not name:
            return render(req, 'shop/admin_requests.html', {
                'requests': pending_requests,
                'cat_error': 'Название категории не может быть пустым.'
            })

        if models.Category.objects.filter(name__iexact=name).exists():
            return render(req, 'shop/admin_requests.html', {
                'requests': pending_requests,
                'cat_error': f'Категория "{name}" уже существует.'
            })

        models.Category.objects.create(name=name)
        return redirect('shop_home')

    return redirect('admin_requests')



@login_required
@user_passes_test(is_seller, login_url='shop_home')
def create_product_view(req):
    categories = models.Category.objects.all()

    if req.method == 'POST':
        title = req.POST.get('title', '').strip()
        category_id = req.POST.get('category')
        price = req.POST.get('price')
        quantity = req.POST.get('quantity', 1)
        description = req.POST.get('description', '').strip()

        if not title or not category_id or not price or not description:
            return render(req, 'shop/create_product.html', {
                'error': 'Все поля обязательны.',
                'categories': categories
            })

        try:
            category = models.Category.objects.get(id=category_id)
            product = models.Product.objects.create(
                title=title,
                category=category,
                price=price,
                quantity=quantity,
                description=description,
                seller=req.user
            )

            images = req.FILES.getlist('images')
            for img in images:
                models.ProductImage.objects.create(product=product, image=img)

            return redirect('shop_home')

        except models.Category.DoesNotExist:
            return render(req, 'shop/create_product.html', {
                'error': 'Выбранная категория не существует.',
                'categories': categories
            })
        except Exception as e:
            return render(req, 'shop/create_product.html', {
                'error': f'Ошибка базы данных: {str(e)}',
                'categories': categories
            })

    return render(req, 'shop/create_product.html', {'categories': categories})


@login_required
def edit_product_view(req, product_id):

    product = get_object_or_404(models.Product, id=product_id, seller=req.user)
    categories = models.Category.objects.all()

    if req.method == 'POST':
        product.title = req.POST.get('title', product.title).strip()
        product.description = req.POST.get('description', product.description).strip()
        product.price = req.POST.get('price', product.price)
        product.quantity = req.POST.get('quantity', product.quantity)
        product.save()

        images = req.FILES.getlist('images')
        for img in images:
            models.ProductImage.objects.create(product=product, image=img)

        return redirect('profile_dashboard')

    return render(req, 'shop/create_product.html', {'product': product, 'categories':categories})


@login_required
def delete_product_image(req, image_id):

    image = get_object_or_404(models.ProductImage, id=image_id, product__seller=req.user)
    product_id = image.product.id
    image.delete()
    return redirect('edit_product', product_id=product_id)


@login_required
def delete_product(req, product_id):
    product = get_object_or_404(models.Product, id=product_id, seller=req.user)

    if req.method == 'POST':
        product.delete()
        return redirect('profile_dashboard')

    return render(req, 'shop/delete.html', {'product': product})



@login_required
def buy_product_view(req, product_id):

    product = get_object_or_404(models.Product, id=product_id)

    if req.method == 'GET':
        return render(req, 'shop/buy_confirm.html', {'product': product})

    if product.seller == req.user:
        return render(req, 'shop/buy_confirm.html', {
            'product': product,
            'error': "Нельзя купить собственный товар."
        })
    if product.quantity <= 0:
        return render(req, 'shop/buy_confirm.html', {
            'product': product,
            'error': "Товары закончились."
        })

    address = req.POST.get('address', '').strip()
    phone = req.POST.get('phone_number', '').strip()
    quantity_to_buy = int(req.POST.get('quantity', 1))

    if not address or not phone:
        return render(req, 'shop/buy_confirm.html', {
            'product': product,
            'error': "Укажите адрес доставки и номер телефона."
        })

    if quantity_to_buy < 1 or quantity_to_buy > product.quantity:
        return render(req, 'shop/buy_confirm.html', {
            'product': product,
            'error': f"Недопустимое количество. Доступно: {product.quantity} шт."
        })

    total = product.price * quantity_to_buy
    buyer_profile = req.user.profile

    if buyer_profile.balance < total:
        return render(req, 'shop/buy_confirm.html', {
            'product': product,
            'error': f"Недостаточно средств. Нужно: ${total} | Ваш баланс: ${buyer_profile.balance}"
        })

    with transaction.atomic():
        buyer_profile.balance -= total
        buyer_profile.save()

        seller_profile = product.seller.profile
        seller_profile.balance += total
        seller_profile.save()

        models.Order.objects.create(
            customer=req.user,
            product=product,
            address=address,
            phone_number=phone,
            quantity=quantity_to_buy,
            total_price=total,
            status='PAID'
        )

        product.quantity -= quantity_to_buy
        

    return redirect('profile_dashboard')


@login_required
def profile_dashboard_view(req):
    user_profile = req.user.profile
    my_purchases = (
        models.Order.objects.filter(customer=req.user)
        .select_related('product', 'product__seller').order_by('-created_at')
    )

    my_products = None
    my_sales = None

    if user_profile.role == 'SELLER':
        my_products = (
            models.Product.objects
            .filter(seller=req.user)
            .prefetch_related('images')
            .select_related('category')
            .order_by('-created_at')
        )
        my_sales = (
            models.Order.objects
            .filter(product__seller=req.user)
            .select_related('product', 'customer')
            .order_by('-created_at')
        )

    return render(req, 'shop/dashboard.html', {
        'profile': user_profile,
        'purchases': my_purchases,
        'products': my_products,
        'sales': my_sales,
    })


def seller_profile_view(req, seller_id):

    from django.contrib.auth import get_user_model
    User = get_user_model()

    seller = get_object_or_404(User, id=seller_id)
    seller_profile = get_object_or_404(models.Profile, user=seller, role='SELLER')

    seller_products = (
        models.Product.objects
        .filter(seller=seller)
        .prefetch_related('images')
        .select_related('category')
        .order_by('-created_at')
    )

    total_sales = models.Order.objects.filter(product__seller=seller).count()

    return render(req, 'shop/seller_profile.html', {
        'seller': seller,
        'seller_profile': seller_profile,
        'products': seller_products,
        'total_sales': total_sales,
        'product_count': seller_products.count(),
    })