from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/user_{instance.user.id}/{unique_filename}"


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255)

    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)


    converted_file = models.FileField(
        upload_to=user_directory_path,
        null=True,
        blank=True
    )

    tool_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name