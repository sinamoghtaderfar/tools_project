from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate  # Added authenticate for login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.files.models import UserFile  # Single import
from django.http import JsonResponse
from django.views.decorators.http import require_GET

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
            username=username,
            email=email,
            password=password1
        )

        # This message will be passed to the login page
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")  # Redirect to login page

    return render(request, "accounts/register.html")


def login_view(request):
    """Custom login view that shows messages"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            messages.success(request, "Successfully logged in!")  # Success message
            return redirect("dashboard")
        else:
            # Login failed
            messages.error(request, "Invalid username or password")  # Error message
            return redirect("login")
    
    # GET request - show login form
    return render(request, "accounts/login.html")


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
                tool_type=tool_type
            )
            messages.success(request, "File uploaded successfully!")  # Upload message

    files = UserFile.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "accounts/dashboard.html", {"files": files})


@login_required
@require_GET
def keep_alive(request):
    """Keep session alive"""
    request.session.set_expiry(180)
    return JsonResponse({
        "status": "ok",
        "message": "Session extended"
    })