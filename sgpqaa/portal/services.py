from datetime import date

from django.db import transaction

from .models import MonthlyQuota, QuotaConfig, Vehicle


def get_active_quota_config():
    return QuotaConfig.objects.filter(is_active=True).order_by('-effective_from').first()


@transaction.atomic
def generate_monthly_quotas(*, reference_month, due_date, amount, generated_automatically=True):
    normalized_reference = reference_month.replace(day=1)
    created_count = 0

    for vehicle in Vehicle.objects.filter(is_active=True).select_related('owner'):
        _, created = MonthlyQuota.objects.get_or_create(
            vehicle=vehicle,
            reference_month=normalized_reference,
            defaults={
                'due_date': due_date,
                'amount_due': amount,
                'status': MonthlyQuota.Status.PENDING,
                'generated_automatically': generated_automatically,
            },
        )
        if created:
            created_count += 1

    return created_count


def generate_quotas_from_active_config(reference_month=None):
    config = get_active_quota_config()
    if not config:
        return 0

    reference_month = reference_month or config.effective_from
    return generate_monthly_quotas(
        reference_month=reference_month,
        due_date=config.effective_from,
        amount=config.amount,
        generated_automatically=True,
    )


def ensure_vehicle_has_current_month_quota(vehicle):
    config = get_active_quota_config()
    if not config or not vehicle.is_active:
        return False

    reference_month = config.effective_from.replace(day=1)
    _, created = MonthlyQuota.objects.get_or_create(
        vehicle=vehicle,
        reference_month=reference_month,
        defaults={
            'due_date': config.effective_from,
            'amount_due': config.amount,
            'status': MonthlyQuota.Status.PENDING,
            'generated_automatically': True,
        },
    )
    return created
