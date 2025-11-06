from django import forms

from message_sender.models import Mailing
from message_sender.widgets import DateTimePickerInput
from users.utils import UserSettingUpMix


class MailingForm(UserSettingUpMix, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ['message',
                  'recipients',
                  'end_date']

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['end_date'].widget = DateTimePickerInput()
        self.fields['end_date'].input_formats = ['%d/%m/%Y %H:%M']
