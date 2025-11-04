from django import forms

from message_sender.models import Mailing
from users.utils import UserSettingUpMix


class MailingForm(UserSettingUpMix, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ['status',
                  'message',
                  'recipients',]
