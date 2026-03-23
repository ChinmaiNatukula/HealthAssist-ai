from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'core/dashboard.html')
    return render(request, 'core/landing.html')


@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')


@login_required
def precautions_view(request):
    return render(request, 'core/precautions.html')
