from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from . models import Customer
def sign_out(request):
    logout(request)
    return redirect('home')

# Create your views here.
def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            #creates user accounts
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            #creates customer accounts
            customer=Customer.objects.create(
                name=username,
                user=user,
                phone=phone
            )
            sucess_message="✅ You’re registered successfully!"
            messages.success(request,sucess_message)
        except Exception as e:
            error_message="❌ Duplicate username or invalid credentials!"
            messages.error(request,error_message)
    if request.POST and 'login' in request.POST:
        context['register']=False
        username=request.POST.get('username')
        password=request.POST.get('password')   
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')    
        else:
            messages.error(request, "❌ Invalid username or password!")


    return render(request,'account.html',context)
