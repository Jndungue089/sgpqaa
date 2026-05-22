from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm
from .models import MemberProfile, MonthlyQuota, PaymentRecord, Vehicle


def home(request):
    context = {
        'association_name': settings.ASSOCIATION_NAME,
        'default_quota_amount': settings.DEFAULT_QUOTA_AMOUNT,
    }
    return render(request, 'portal/home.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.cleaned_data['user'])
        messages.success(request, 'Sessao iniciada com sucesso.')
        return redirect('portal:dashboard')

    return render(request, 'portal/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Conta criada com sucesso.')
        return redirect('portal:dashboard')

    return render(request, 'portal/register.html', {'form': form})


@login_required
def dashboard(request):
    profile, _ = MemberProfile.objects.select_related('user').get_or_create(
        user=request.user,
        defaults={
            'member_number': f'AUTO-{request.user.id}',
            'role': MemberProfile.Role.ADMIN if request.user.is_staff else MemberProfile.Role.MEMBER,
        },
    )
    context = {
        'profile': profile,
        'vehicles_count': Vehicle.objects.filter(owner=profile).count(),
        'quotas_count': MonthlyQuota.objects.filter(vehicle__owner=profile).count(),
        'payments_count': PaymentRecord.objects.filter(quota__vehicle__owner=profile).count(),
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sessao terminada com sucesso.')
    return redirect('portal:home')
