from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm, VehicleForm
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
        'recent_vehicles': Vehicle.objects.filter(owner=profile, is_active=True).order_by('-created_at')[:3],
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sessao terminada com sucesso.')
    return redirect('portal:home')


@login_required
def vehicle_list_create(request):
    profile, _ = MemberProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'member_number': f'AUTO-{request.user.id}',
            'role': MemberProfile.Role.ADMIN if request.user.is_staff else MemberProfile.Role.MEMBER,
        },
    )
    form = VehicleForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.owner = profile
        vehicle.save()
        messages.success(request, 'Viatura registada com sucesso.')
        return redirect('portal:vehicles')

    vehicles = Vehicle.objects.filter(owner=profile).order_by('-is_active', 'plate_number')
    return render(
        request,
        'portal/vehicles.html',
        {
            'form': form,
            'vehicles': vehicles,
            'profile': profile,
        },
    )


@login_required
def vehicle_deactivate(request, vehicle_id):
    profile, _ = MemberProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'member_number': f'AUTO-{request.user.id}',
            'role': MemberProfile.Role.ADMIN if request.user.is_staff else MemberProfile.Role.MEMBER,
        },
    )
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=profile)

    if request.method == 'POST':
        vehicle.is_active = False
        vehicle.save(update_fields=['is_active', 'updated_at'])
        messages.info(request, 'Viatura desactivada com sucesso.')

    return redirect('portal:vehicles')
