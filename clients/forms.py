from django import forms

from clients.models import MailingRecipient
from users.utils import UserSettingUpMix


class ClientsForm(UserSettingUpMix, forms.ModelForm):

    class Meta:
        model = MailingRecipient
        fields = ['email',
                  'fullname',
                  'comment'
                  ]
