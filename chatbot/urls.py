from django.urls import path
from . import views

app_name = 'chatbot'  # This is important for namespace

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('', views.home, name='home'),  # Home page route
]