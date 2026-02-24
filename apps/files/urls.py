from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_file, name="upload_file"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("process/<int:file_id>/", views.process_tool, name="process_tool"),
    path("download/<int:file_id>/", views.download_file, name="download_file"),
]
