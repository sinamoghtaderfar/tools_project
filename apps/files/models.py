from django.db import models
from django.contrib.auth.models import User
import uuid
import os


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return f"uploads/user_{instance.user.id}/{unique_filename}"


def user_output_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    return f"outputs/user_{instance.user.id}/{unique_name}"


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    converted_file = models.FileField(upload_to=user_output_path, null=True, blank=True)
    tool_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

    # get .txt .pdf .doc x ....
    def extension(self):
        return os.path.splitext(self.original_name)[1].lower()

    # Categorie file
    def file_category(self):
        ext = self.extension()

        if ext in [".doc", ".docx"]:
            return "word"
        elif ext in [".pdf"]:
            return "pdf"
        elif ext in [".png", ".jpg", ".jpeg", ".webp", ".heic"]:
            return "image"
        elif ext in [".zip", ".rar"]:
            return "archive"
        elif ext in [".csv"]:
            return "csv"
        elif ext in [".xls", ".xlsx"]:
            return "excel"
        else:
            return "other"

    # suggest
    def suggested_tools(self):
        category = self.file_category()

        tools = {
            "word": [
                {"label": "Convert to PDF", "value": "word_to_pdf"},
                {"label": "Convert to TEXT", "value": "word_to_txt"},
                {"label": "Compress Word", "value": "compress_word"},
            ],
            "pdf": [
                {"label": "Convert to Word", "value": "pdf_to_word"},
                {"label": "Convert to TEXT", "value": "word_to_txt"},
                {"label": "Compress PDF", "value": "compress_pdf"},
            ],
            "image": [
                {"label": "Convert to JPG", "value": "to_jpg"},
                {"label": "Convert to PNG", "value": "to_png"},
                {"label": "Convert to GIF", "value": "to_gif"},
                {"label": "Compress Image", "value": "compress_image"},
            ],
            "archive": [
                {"label": "Extract Files", "value": "extract"},
            ],
            "csv": [
                {"label": "Convert to Excel", "value": "to_excel"},
            ],
            "excel": [
                {"label": "Convert to CSV", "value": "to_csv"},
            ],
            "other": [],
        }

        return tools.get(category, [])
