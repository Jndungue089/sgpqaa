from django.contrib import admin

from .models import MemberProfile, MonthlyQuota, PaymentRecord, QuotaConfig, Vehicle


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

# Register your models here.
