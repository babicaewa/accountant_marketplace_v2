from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import Professional, Client

def account_login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if Professional.objects.filter(user=user).exists():
                return redirect("portal_user_clients")
            elif Client.objects.filter(user=user).exists():
                return redirect("client_portal_requests")
            else:
                return render(request, "account/login.html", {"error": "Failed to log user in."})
        else:
            return render(request, "account/login.html", {"error": "Invalid credentials"})
        
    return render(request, "account/login.html", {"error": "Invalid credentials"})

def logout_user(request):
    logout(request)
    messages.success(request, "Successfully Logged out.")
    return redirect('home')
