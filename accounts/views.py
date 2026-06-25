from django.shortcuts import render,redirect
from . import models
import random


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

        print("\n" + '='*30)
        print(f'Email confirmation send to : {user.email}')
        print(f'Code >>> {verifications_code} <<<')
        print('='*30 + '\n')

    return render(req, 'accounts/register.html')