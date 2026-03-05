from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate  # Added authenticate for login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.files.models import UserFile  # Single import
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect


def register_view(request):
    """User registration view with messages"""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )

        # This message will be passed to the login page
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")  # Redirect to login page

    return render(request, "accounts/register.html")


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def login_view(request):
    if request.user.is_authenticated:

        next_url = request.GET.get("next") or "//"
        return redirect(next_url)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")
        next_url = request.POST.get("next") or request.GET.get("next")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)

            messages.success(request, "Successfully logged in!")

            if next_url:
                if next_url.startswith("/"):
                    return redirect(next_url)
                else:
                    try:
                        return redirect(reverse(next_url))
                    except:
                        return redirect("/")  # fallback
            else:
                # default redirect
                return redirect("/")

        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    # GET request
    next_url = request.GET.get("next")
    return render(request, "accounts/login.html", {"next": next_url})


@csrf_protect
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("dashboard")


@login_required
def dashboard_view(request):
    """User dashboard - handles file uploads and displays files"""
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        tool_type = request.POST.get("tool_type")

        if uploaded_file:
            UserFile.objects.create(
                user=request.user,
                original_file=uploaded_file,
                original_name=uploaded_file.name,
                tool_type=tool_type,
            )
            messages.success(request, "File uploaded successfully!")  # Upload message

    files = UserFile.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"files": files})


@login_required
@require_GET
def keep_alive(request):
    """Keep session alive"""
    request.session.set_expiry(180)
    return JsonResponse({"status": "ok", "message": "Session extended"})
