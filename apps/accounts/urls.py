from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('register/', register_view, name='register'),
    
    path('dashboard/', dashboard_view, name='dashboard'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
