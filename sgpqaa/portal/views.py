from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BankTransferProofForm, LoginForm, RegisterForm, VehicleForm
from .models import MemberProfile, MonthlyQuota, PaymentRecord, QuotaConfig, Vehicle
from .services import generate_quotas_from_active_config, get_active_quota_config


def get_or_create_profile(user):
    return MemberProfile.objects.select_related('user').get_or_create(
        user=user,
        defaults={
            'member_number': f'AUTO-{user.id}',
            'role': MemberProfile.Role.ADMIN if user.is_staff else MemberProfile.Role.MEMBER,
        },
    )[0]


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
    generate_quotas_from_active_config()
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
        messages.error(request, 'Esta quota nao esta disponivel para submissao de comprovante.')
        return redirect('portal:quotas')

    form = BankTransferProofForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        PaymentRecord.objects.create(
            quota=quota,
            method=PaymentRecord.Method.BANK_TRANSFER,
            status=PaymentRecord.Status.SUBMITTED,
            amount_paid=quota.amount_due,
            payment_date=timezone.now(),
            simulated_reference=f'TRF-{uuid4().hex[:10].upper()}',
            proof_file=form.cleaned_data['proof_file'],
            notes=form.cleaned_data['notes'],
        )
        quota.status = MonthlyQuota.Status.AWAITING_VALIDATION
        quota.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Comprovante enviado com sucesso. Aguarda validacao do tesoureiro.')
        return redirect('portal:quotas')

    return render(
        request,
        'portal/submit_transfer.html',
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

    created_count = generate_quotas_from_active_config()
    if created_count:
        messages.info(request, f'{created_count} novas quotas automaticas foram detectadas para a configuracao activa.')

    pending_payments = PaymentRecord.objects.filter(
        status=PaymentRecord.Status.SUBMITTED,
        quota__status=MonthlyQuota.Status.AWAITING_VALIDATION,
    ).select_related('quota__vehicle__owner__user')
    recent_quotas = MonthlyQuota.objects.select_related('vehicle__owner__user')[:8]
    unpaid_quotas = MonthlyQuota.objects.filter(
        status__in=[MonthlyQuota.Status.PENDING, MonthlyQuota.Status.OVERDUE]
    ).select_related('vehicle__owner__user')[:8]
    active_config = get_active_quota_config()

    context = {
        'profile': profile,
        'pending_payments': pending_payments,
        'recent_quotas': recent_quotas,
        'unpaid_quotas': unpaid_quotas,
        'active_config': active_config,
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


@login_required
def mark_cash_payment(request, quota_id):
    profile = get_or_create_profile(request.user)
    if not ensure_treasurer_access(profile):
        return HttpResponseForbidden('Apenas o tesoureiro ou administrador pode marcar pagamento em maos.')

    quota = get_object_or_404(MonthlyQuota, pk=quota_id)
    if request.method == 'POST' and quota.status in {MonthlyQuota.Status.PENDING, MonthlyQuota.Status.OVERDUE}:
        PaymentRecord.objects.create(
            quota=quota,
            method=PaymentRecord.Method.CASH,
            status=PaymentRecord.Status.VALIDATED,
            amount_paid=quota.amount_due,
            payment_date=timezone.now(),
            validated_by=profile,
            validated_at=timezone.now(),
            notes='Pagamento em maos confirmado pela tesouraria.',
        )
        quota.status = MonthlyQuota.Status.PAID
        quota.save(update_fields=['status', 'updated_at'])
        messages.success(request, 'Pagamento em maos marcado como pago com sucesso.')

    return redirect('portal:treasurer_dashboard')
