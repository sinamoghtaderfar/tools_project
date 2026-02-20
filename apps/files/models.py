from django.db import models
from django.contrib.auth.models import User


class UserFile(models.Model):

    TOOL_CHOICES = [
        ('word_to_pdf', 'Word to PDF'),
        ('pdf_to_word', 'PDF to Word'),
        ('image_convert', 'Image Convert'),
        ('qr_reader', 'QR Reader'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    original_file = models.FileField(upload_to='uploads/')
    converted_file = models.FileField(upload_to='outputs/', null=True, blank=True)

    original_name = models.CharField(max_length=255)
    converted_name = models.CharField(max_length=255, null=True, blank=True)

    tool_type = models.CharField(max_length=50, choices=TOOL_CHOICES)

    status = models.CharField(
        max_length=20,
        default='completed'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.original_name}"
