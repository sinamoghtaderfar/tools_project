from django.urls import path
from . import views

app_name = 'editor' 

urlpatterns = [
    path('', views.editor_home, name='home'),  
    path('run/', views.run_code, name='run_code'),
]