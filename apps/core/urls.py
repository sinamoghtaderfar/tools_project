from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("tool/<str:tool_name>/", views.tool_page, name="tool_page"),
    path("tool/<str:tool_name>/process/", views.guest_tool, name="guest_tool_process"),
    path("tools/", views.tools_list, name="tools_list"),
    path("tool/<str:tool_slug>/", views.tool_page, name="tool_page"),
]
