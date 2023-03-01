from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest

from .models import MyUser
from .forms import RegisterForm
from .utils import generate_otp, send_otp


def register(request: WSGIRequest):
    form = RegisterForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = generate_otp()
        send_otp(phone, otp)
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
    context = {
        'phone': phone
    }
    # if request.method == "POST":
    #     if "phone" in request.POST:
    #         phone = request.POST.get('phone')
    #         try:
    #             user = MyUser.objects.get(phone=phone)
    #             login(
    #                 request,
    #                 user,
    #                 backend='otp.authentications.PhoneBackend',
    #             )
    #             return redirect('dashboard')
    #         except MyUser.DoesNotExist:
    #             pass
    return render(request, 'verify.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')
