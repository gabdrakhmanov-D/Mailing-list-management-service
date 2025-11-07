from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from clients.models import MailingRecipient
from message_sender.models import Mailing
from users.forms import UserRegisterForm, UserSettingUpLoginForm, UserSettingUpProfile, UserPasswordChangeForm
from users.models import User


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = Mailing.objects.count()
        context['activ_mailing'] = Mailing.objects.filter(status='launched').count()
        context['uniq_client_count'] = MailingRecipient.objects.distinct().count()
        return context


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:home')


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

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "users/password_change_form.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.success_url = reverse_lazy('users:password_change_done')
        return super().form_valid(form)


class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/home.html'
    extra_context = {'psw_change_done': 'Вы успешно изменили пароль.'}


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'managers/users_list.html'
    context_object_name = 'users'