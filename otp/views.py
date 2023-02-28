from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib.auth import login


def phone_login(request):
    if request.method == "POST":
        if "phone" in request.POST:
            phone = request.POST.get('phone')
            try:
                user = MyUser.objects.get(phone=phone)
                login(
                    request,
                    user,
                    backend='otp.authentications.PhoneBackend',
                )
                return redirect('dashboard')
            except MyUser.DoesNotExist:
                pass
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')
