from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.files.models import UserFile

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                login(request, user)
                return redirect("home")

        messages.error(request, "Invalid data")

    return render(request, "accounts/register.html")




@login_required
def dashboard_view(request):
    files = UserFile.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "accounts/dashboard.html", {"files": files})
