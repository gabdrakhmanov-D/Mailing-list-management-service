from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, UserProfileEdit, HomeView, UserPasswordChange, \
    UserPasswordChangeDone

app_name = UsersConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(next_page='users:home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:home'), name='logout'),
    path('profile/<int:pk>', UserProfileEdit.as_view(), name='profile'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', UserPasswordChangeDone.as_view(), name='password_change_done'),
]
