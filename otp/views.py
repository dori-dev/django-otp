from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest

from .models import MyUser
from .forms import RegisterForm
from .utils import generate_otp, send_otp, check_otp_expiration


def register(request: WSGIRequest):
    form = RegisterForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = generate_otp()
        # send_otp(phone, otp)
        print(f'Verify code: {otp}')
        try:
            user = MyUser.objects.get(phone=phone)
            user.otp = otp
            user.save()
            request.session['phone_number'] = user.phone
            return redirect('verify')
        except MyUser.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user: MyUser = form.save(commit=False)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['phone_number'] = user.phone
                return redirect('verify')
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def verify(request: WSGIRequest):
    phone = request.session.get('phone_number')
    try:
        user: MyUser = MyUser.objects.get(phone=phone)
    except MyUser.DoesNotExist:
        return redirect('register')
    if request.method == "POST":
        if not check_otp_expiration(phone):
            return redirect('register')
        otp = request.POST.get('otp')
        if user.otp != int(otp):
            return redirect('verify')
        user.is_active = True
        user.save()
        login(
            request,
            user,
            backend='otp.authentications.PhoneBackend'
        )
        return redirect('dashboard')
    context = {
        'phone': phone
    }
    return render(request, 'verify.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')
