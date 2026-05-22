from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, reverse

from .models import MemberProfile, MonthlyQuota, PaymentRecord, QuotaConfig, Vehicle
from .services import generate_quotas_from_active_config


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('member_number', 'user', 'role', 'staff_name', 'is_active_member')
    list_filter = ('role', 'is_active_member', 'staff_name')
    search_fields = ('member_number', 'user__username', 'user__first_name', 'user__last_name')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'model', 'year', 'owner', 'is_active')
    list_filter = ('is_active', 'year')
    search_fields = ('plate_number', 'model', 'owner__member_number', 'owner__user__username')


@admin.register(QuotaConfig)
class QuotaConfigAdmin(admin.ModelAdmin):
    list_display = ('amount', 'late_fee_percentage', 'effective_from', 'is_active')
    list_filter = ('is_active',)
    ordering = ('-effective_from',)
    change_list_template = 'admin/portal/quotaconfig/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'gerar-quotas-mes/',
                self.admin_site.admin_view(self.generate_month_quotas_view),
                name='portal_quotaconfig_generate_month_quotas',
            ),
        ]
        return custom_urls + urls

    def generate_month_quotas_view(self, request):
        created_count = generate_quotas_from_active_config()
        if created_count:
            self.message_user(
                request,
                f'{created_count} quotas do mes foram geradas automaticamente.',
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                'Nenhuma nova quota foi gerada. Verifique se existe configuracao activa ou se as quotas ja existem.',
                level=messages.WARNING,
            )
        return redirect(reverse('admin:portal_quotaconfig_changelist'))


@admin.register(MonthlyQuota)
class MonthlyQuotaAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'reference_month', 'due_date', 'amount_due', 'status')
    list_filter = ('status', 'generated_automatically')
    search_fields = ('vehicle__plate_number',)


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('quota', 'method', 'status', 'amount_paid', 'payment_date')
    list_filter = ('method', 'status')
    search_fields = ('quota__vehicle__plate_number', 'simulated_reference')
