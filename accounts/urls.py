from django.contrib import admin
from django.urls import path


from accounts.views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view()), #route for registration
    path('login/', LoginView.as_view()), #route for user to login
]