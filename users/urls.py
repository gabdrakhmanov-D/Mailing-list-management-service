from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, UserProfileEdit, HomeView, UserPasswordChange, \
    UserPasswordChangeDone, UserListView, block_user, unlock_user

app_name = UsersConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(next_page='users:home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/<int:pk>', UserProfileEdit.as_view(), name='profile'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', UserPasswordChangeDone.as_view(), name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ), name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),
    path("manager_page/", UserListView.as_view(), name="mngr_page"),
    path("manager_page/<int:user_id>/disable/", block_user, name="disable_user"),
    path("manager_page/<int:user_id>/unlock/", unlock_user, name="unlock_user")
]
