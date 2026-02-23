from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserFile


@login_required
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        tool_type = request.POST.get("tool_type")

        if uploaded_file:
            UserFile.objects.create(
                user=request.user,
                original_name=uploaded_file.name,
                file=uploaded_file,
                tool_type=tool_type
            )

    return redirect("dashboard")
