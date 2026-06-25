from django.shortcuts import render,redirect
from . import models
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
import random
from shop.models import Profile


def register(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        password_confrim = req.POST.get('password_confirm')

        saved_date = {'username':username, 'email':email}

        if not username or not email or not password or not password_confrim:
            return render(req, 'accounts/register.html', {'error':'Plz fill all fileds', 'data':saved_date})
        
        if password != password_confrim:
            return render(req, 'accounts/register.html', {'error':"Passwords don't match", 'data':saved_date})
        
        if models.CustomUser.objects.filter(username=username).exists():
            return render(req, 'accounts/register.html', {'error':'Username already exists','data':saved_date})
        
        if models.CustomUser.objects.filter(email=email).exists():
            return render(req, 'accounts/register.html', {'error':'Email already exists', 'data':saved_date})
        
        user = models.CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        verifications_code = str(random.randint(100000,999999))
        models.EmailConfirm.objects.update_or_create(user=user, defaults={'code':verifications_code})

        send_mail(
            subject='Confirm your account',
            message=f"You verifycation code {verifications_code} - don't show it to someone",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        print("\n" + '='*30)
        print(f'Email confirmation send to : {user.email}')
        print(f'Code >>> {verifications_code} <<<')
        print('='*30 + '\n')


        return redirect('verify_email', username=user.username)

    return render(req, 'accounts/register.html')


def verify_email(req, username):
    if req.method == 'POST':
        input_code = req.POST.get('code', '').strip()

        try:
            user = models.CustomUser.objects.get(username=username)
            confirm_record = models.EmailConfirm.objects.filter(user=user).first()

            if not confirm_record:
                return render(req, 'accounts/verify.html', {'error':'Verifications session not found'})
            
            if confirm_record.code == input_code:
                user.is_active = True
                user.save()

                Profile.objects.get_or_create(user=user, role='CUSTOMER')

                confirm_record.delete()

                login(user, user)
                
                return redirect('shop_home')
            else:
                return render(req, 'accounts/verify.html', {'error':'Invalid code'})
        except models.CustomUser.DoesNotExist:
            return render(req, 'accounts/verify.html', {'error':'User not exists'})
        
    return render(req, 'accounts/verify.html')


def user_login(req):
    if req.user.is_authenticated:
        return redirect('shop_home')

    if req.method == 'POST':
        username = req.POST.get('username', '').strip()
        password = req.POST.get('password', '')

        if not username or not password:
            return render(req, 'accounts/login.html', {'error': 'Please provide both username and password.'})

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('shop_home')
        else:
            return render(req, 'accounts/login.html', {'error': 'Invalid credentials or account not activated.'})

    return render(req, 'accounts/login.html')


def user_logout(req):
    logout(req)
    return redirect('login')