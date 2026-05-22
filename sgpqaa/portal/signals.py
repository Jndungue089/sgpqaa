from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import QuotaConfig, Vehicle
from .services import ensure_vehicle_has_current_month_quota, generate_quotas_from_active_config


@receiver(post_save, sender=QuotaConfig)
def quota_config_post_save(sender, instance, created, **kwargs):
    if instance.is_active:
        QuotaConfig.objects.exclude(pk=instance.pk).update(is_active=False)
        generate_quotas_from_active_config(reference_month=instance.effective_from)


@receiver(post_save, sender=Vehicle)
def vehicle_post_save(sender, instance, created, **kwargs):
    if created and instance.is_active:
        ensure_vehicle_has_current_month_quota(instance)
