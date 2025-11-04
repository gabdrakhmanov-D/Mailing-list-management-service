from django.contrib.auth.views import LogoutView
from django.urls import path

from message_sender.views import HomeView
from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView, UserProfileEdit


app_name = UsersConfig.name

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(next_page='users:home'), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:home'), name='logout'),
    path('profile/<int:pk>', UserProfileEdit.as_view(), name='profile'),
]
