from django import forms

from messages_for_clients.models import Message
from users.utils import UserSettingUpMix


class MessageForm(UserSettingUpMix, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject_line',
                  'message',
                  ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for field, field_object in self.fields.items():
            field_object.widget.attrs.update({'class': 'form-control'})
