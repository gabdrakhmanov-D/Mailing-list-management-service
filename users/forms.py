from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm

from users.models import User

from users.utils import UserSettingUpMix


class UserRegisterForm(UserSettingUpMix, UserCreationForm):
    class Meta:
        model = User
        fields = ("email",
                  "username",
                  "first_name",
                  "last_name",
                  "phone_number",
                  "avatar",
                  "password1",
                  "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.settingup_fields(self.fields)


class UserSettingUpLoginForm(UserSettingUpMix, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserSettingUpLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите ваш email для авторизации'})
        self.fields['username'].label = 'Email'
        self.fields['password'].label = 'Пароль'


class UserSettingUpProfile(UserSettingUpMix, UserChangeForm):
    class Meta:
        model = User
        fields = ("email",
                  "username",
                  "first_name",
                  "last_name",
                  "phone_number",
                  "avatar",
                  )

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.settingup_fields(self.fields)
        self.fields['username'].widget.attrs.update({'readonly': True})
        self.fields['email'].widget.attrs.update({'readonly': True})


class UserPasswordChangeForm(UserSettingUpMix, PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль")
    new_password1 = forms.CharField(label="Новый пароль")
    new_password2 = forms.CharField(label="Подтверждение пароля")
