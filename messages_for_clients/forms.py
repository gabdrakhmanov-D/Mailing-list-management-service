from django import forms

from messages_for_clients.models import Message
from users.utils import UserSettingUpMix


class MessageForm(UserSettingUpMix, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject_line',
                  'message',
                  ]
