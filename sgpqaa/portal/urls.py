from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registo/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('viaturas/', views.vehicle_list_create, name='vehicles'),
    path('viaturas/<int:vehicle_id>/desactivar/', views.vehicle_deactivate, name='vehicle_deactivate'),
    path('logout/', views.logout_view, name='logout'),
]
