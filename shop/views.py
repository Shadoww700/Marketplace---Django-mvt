from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.decorators import login_required, user_passes_test

def shop_home(req):
    products = models.Product.objects.all().select_related('category','seller' ).order_by('-created_at')
    categories = models.Category.objects.all()

    if req.user.is_authenticated:
        req.user = req.user.__class__.objects.select_related('profile').get(pk=req.user.pk)

    return render(req, 'shop/home.html', {
        'products': products,
        'categories': categories
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