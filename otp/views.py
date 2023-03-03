from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages

from .models import MyUser
from .forms import RegisterForm
from . import utils


def register(request: WSGIRequest):
    form = RegisterForm()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = utils.generate_otp()
        utils.send_otp(phone, otp)
        messages.success(
            request,
            'Verification code send successfully!'
        )
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
    if phone is None:
        return redirect('register')
    if request.method == "POST":
        otp = request.POST.get('otp')
        user = authenticate(
            request,
            username=phone,
            password=otp
        )
        if user is not None:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(
                request,
                'You login successfully.',
            )
            request.session['phone_number'] = None
            return redirect('dashboard')
    context = {
        'phone': phone
    }
    return render(request, 'verify.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')
