from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import Professional, Client

def home(request):
    return render(request, "core/home.html")

def visit_portal(request):
    user = request.user
    if Professional.objects.filter(user=user).exists():
        return redirect('portal_user_clients')
    elif Client.objects.filter(user=user).exists():
        return redirect('client_portal_requests')
    else:
        messages.error(request, 'Error accessing portal, please try aagain.')
        return render(request, "core/home.html")



