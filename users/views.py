import secrets
import string
import random

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, FormView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy('users:login')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_user = form.save()
    #         new_user.set_password(
    #             new_user.make_random_password(length=12)
    #         )
    #         new_user.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'https://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Для подтверждения регистрации перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class PasswordResetView(FormView):
    template_name = 'users/reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:login')

    def generate_random_password(self, length=9):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(characters, k=length))
        return password

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            new_password = self.generate_random_password()
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш новый пароль для входа {new_password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except User.DoesNotExist:
            form.add_error('email', 'Пользователь с таким email не найден')
            return self.form_invalid(form)

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user



