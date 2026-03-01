from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("tool/<str:tool_name>/", views.guest_tool, name="tool_page"),
    path("tool/<str:tool_name>/process/", views.guest_tool, name="guest_tool_process"),
]
