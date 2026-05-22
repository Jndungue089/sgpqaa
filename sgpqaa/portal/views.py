from decimal import Decimal
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LoginForm, PaymentSimulationForm, QuotaGenerationForm, RegisterForm, VehicleForm
from .models import MemberProfile, MonthlyQuota, PaymentRecord, QuotaConfig, Vehicle


def get_or_create_profile(user):
    return MemberProfile.objects.select_related('user').get_or_create(
        user=user,
        defaults={
            'member_number': f'AUTO-{user.id}',
            'role': MemberProfile.Role.ADMIN if user.is_staff else MemberProfile.Role.MEMBER,
        },
    )[0]


def get_current_quota_amount():
    current_config = QuotaConfig.objects.filter(is_active=True).order_by('-effective_from').first()
    if current_config:
        return current_config.amount
    return Decimal(str(settings.DEFAULT_QUOTA_AMOUNT))


def ensure_treasurer_access(profile):
    return profile.role in {MemberProfile.Role.TREASURER, MemberProfile.Role.ADMIN}


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
    profile = get_or_create_profile(request.user)
    if ensure_treasurer_access(profile):
        return redirect('portal:treasurer_dashboard')

    context = {
        'profile': profile,
        'vehicles_count': Vehicle.objects.filter(owner=profile).count(),
        'quotas_count': MonthlyQuota.objects.filter(vehicle__owner=profile).count(),
        'payments_count': PaymentRecord.objects.filter(quota__vehicle__owner=profile).count(),
        'recent_vehicles': Vehicle.objects.filter(owner=profile, is_active=True).order_by('-created_at')[:3],
        'recent_quotas': MonthlyQuota.objects.filter(vehicle__owner=profile).select_related('vehicle')[:5],
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sessao terminada com sucesso.')
    return redirect('portal:home')


@login_required
def vehicle_list_create(request):
    profile = get_or_create_profile(request.user)
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
    profile = get_or_create_profile(request.user)
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, owner=profile)

    if request.method == 'POST':
        vehicle.is_active = False
        vehicle.save(update_fields=['is_active', 'updated_at'])
        messages.info(request, 'Viatura desactivada com sucesso.')

    return redirect('portal:vehicles')


@login_required
def quota_list(request):
    profile = get_or_create_profile(request.user)
    quotas = MonthlyQuota.objects.filter(vehicle__owner=profile).select_related('vehicle')
    context = {
        'profile': profile,
        'quotas': quotas,
    }
    return render(request, 'portal/quotas.html', context)


@login_required
def simulate_payment(request, quota_id):
    profile = get_or_create_profile(request.user)
    quota = get_object_or_404(MonthlyQuota.objects.select_related('vehicle'), pk=quota_id, vehicle__owner=profile)

    if quota.status not in {MonthlyQuota.Status.PENDING, MonthlyQuota.Status.OVERDUE}:
        messages.error(request, 'Esta quota nao esta disponivel para simulacao de pagamento.')
        return redirect('portal:quotas')

    form = PaymentSimulationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        method = form.cleaned_data['method']
        simulated_reference = ''
        if method == PaymentRecord.Method.MULTICAIXA:
            simulated_reference = f'MCX-{uuid4().hex[:10].upper()}'

        PaymentRecord.objects.create(
            quota=quota,
            method=method,
            status=PaymentRecord.Status.SIMULATED,
            amount_paid=quota.amount_due,
            payment_date=timezone.now(),
            simulated_reference=simulated_reference,
            notes=form.cleaned_data['notes'],
        )
        quota.status = MonthlyQuota.Status.AWAITING_VALIDATION
        quota.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Pagamento simulado com sucesso. Aguarda validacao do tesoureiro.')
        return redirect('portal:quotas')

    return render(
        request,
        'portal/simulate_payment.html',
        {
            'form': form,
            'quota': quota,
            'profile': profile,
        },
    )


@login_required
def treasurer_dashboard(request):
    profile = get_or_create_profile(request.user)
    if not ensure_treasurer_access(profile):
        return HttpResponseForbidden('Apenas o tesoureiro ou administrador pode aceder a esta area.')

    generation_form = QuotaGenerationForm(
        request.POST if request.method == 'POST' and request.POST.get('action') == 'generate_quotas' else None,
        initial={'amount': get_current_quota_amount()},
    )

    if request.method == 'POST' and request.POST.get('action') == 'generate_quotas' and generation_form.is_valid():
        reference_month = generation_form.cleaned_data['reference_month'].replace(day=1)
        due_date = generation_form.cleaned_data['due_date']
        amount = generation_form.cleaned_data['amount']
        created_count = 0

        for vehicle in Vehicle.objects.filter(is_active=True).select_related('owner'):
            _, created = MonthlyQuota.objects.get_or_create(
                vehicle=vehicle,
                reference_month=reference_month,
                defaults={
                    'due_date': due_date,
                    'amount_due': amount,
                    'status': MonthlyQuota.Status.PENDING,
                    'generated_automatically': True,
                },
            )
            if created:
                created_count += 1

        messages.success(request, f'{created_count} quotas geradas para o periodo seleccionado.')
        return redirect('portal:treasurer_dashboard')

    pending_payments = PaymentRecord.objects.filter(
        status=PaymentRecord.Status.SIMULATED,
        quota__status=MonthlyQuota.Status.AWAITING_VALIDATION,
    ).select_related('quota__vehicle__owner__user')
    recent_quotas = MonthlyQuota.objects.select_related('vehicle__owner__user')[:8]

    context = {
        'profile': profile,
        'generation_form': generation_form,
        'pending_payments': pending_payments,
        'recent_quotas': recent_quotas,
        'vehicles_total': Vehicle.objects.filter(is_active=True).count(),
        'quotas_pending_total': MonthlyQuota.objects.filter(status=MonthlyQuota.Status.PENDING).count(),
        'payments_waiting_total': pending_payments.count(),
    }
    return render(request, 'portal/treasurer_dashboard.html', context)


@login_required
def validate_payment(request, payment_id):
    profile = get_or_create_profile(request.user)
    if not ensure_treasurer_access(profile):
        return HttpResponseForbidden('Apenas o tesoureiro ou administrador pode validar pagamentos.')

    payment = get_object_or_404(PaymentRecord.objects.select_related('quota'), pk=payment_id)
    if request.method == 'POST':
        payment.status = PaymentRecord.Status.VALIDATED
        payment.validated_by = profile
        payment.validated_at = timezone.now()
        payment.save(update_fields=['status', 'validated_by', 'validated_at', 'updated_at'])
        payment.quota.status = MonthlyQuota.Status.PAID
        payment.quota.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Pagamento validado com sucesso.')

    return redirect('portal:treasurer_dashboard')
