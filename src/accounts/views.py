from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.
# class MyLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     success_url = reverse('home')
