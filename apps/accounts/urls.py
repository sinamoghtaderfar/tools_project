from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, dashboard_view, keep_alive

urlpatterns = [
    
    path('login/', login_view, name='login'),  
    
    # Keep these as they are
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("keep-alive/", keep_alive, name="keep_alive"),
]