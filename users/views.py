from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserSettingUpLoginForm, UserSettingUpProfile
from users.models import User


class HomeView(TemplateView):
    template_name = 'users/home.html'


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserSettingUpLoginForm
    success_url = reverse_lazy('users:home')


class UserProfileEdit(UpdateView):
    template_name = 'users/profile.html'
    form_class = UserSettingUpProfile
    model = User

    def form_valid(self, form):
        page = self.get_context_data()['object'].pk
        self.success_url = reverse_lazy("users:profile", kwargs={'pk': page})
        return super().form_valid(form)