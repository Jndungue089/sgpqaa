from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registo/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tesouraria/', views.treasurer_dashboard, name='treasurer_dashboard'),
    path('viaturas/', views.vehicle_list_create, name='vehicles'),
    path('viaturas/<int:vehicle_id>/desactivar/', views.vehicle_deactivate, name='vehicle_deactivate'),
    path('quotas/', views.quota_list, name='quotas'),
    path('quotas/<int:quota_id>/submeter-transferencia/', views.simulate_payment, name='simulate_payment'),
    path('pagamentos/<int:payment_id>/validar/', views.validate_payment, name='validate_payment'),
    path('quotas/<int:quota_id>/marcar-pago-em-maos/', views.mark_cash_payment, name='mark_cash_payment'),
    path('logout/', views.logout_view, name='logout'),
]
