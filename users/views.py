from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from clients.models import MailingRecipient
from message_sender.models import Mailing
from users.forms import UserRegisterForm, UserSettingUpLoginForm, UserSettingUpProfile, UserPasswordChangeForm
from users.models import User


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'main/home.html'

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


class UserProfileView(TemplateView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_edit.html'
    form_class = UserSettingUpProfile
    model = User
    success_url = reverse_lazy("users:profile")


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


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'managers/users_list.html'
    context_object_name = 'users'
    permission_required = "users.can_view_list_users"


@permission_required('users.can_view_list_users', raise_exception=True)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    Mailing.objects.filter(owner=user_id, status='launched').update(status='completed')
    return redirect('users:mngr_page')


@permission_required('users.can_view_list_users', raise_exception=True)
def unlock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('users:mngr_page')
