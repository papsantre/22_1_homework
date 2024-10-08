from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, PasswordResetView
#from django.contrib.auth import views as auth_views

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("email-confirm/<str:token>/", email_verification, name='email_confirm'),
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
]