from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.files.models import UserFile
from django.core.files.storage import FileSystemStorage
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





@login_required
def dashboard_view(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        tool_type = request.POST.get("tool_type")

        if uploaded_file:
            # فعلاً فقط ذخیره می‌کنیم (تبدیل واقعی بعداً)
            user_file = UserFile.objects.create(
                user=request.user,
                original_file=uploaded_file,
                original_name=uploaded_file.name,
                tool_type=tool_type
            )

    files = UserFile.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "accounts/dashboard.html", {"files": files})
