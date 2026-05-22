from django.conf import settings
from django.shortcuts import render


def home(request):
    context = {
        'association_name': settings.ASSOCIATION_NAME,
        'default_quota_amount': settings.DEFAULT_QUOTA_AMOUNT,
    }
    return render(request, 'portal/home.html', context)

# Create your views here.
