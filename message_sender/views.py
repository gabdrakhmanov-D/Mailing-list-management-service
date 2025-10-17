from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from .models import MailingRecipient
# Create your views here.


class HomeView(TemplateView):
    template_name = 'message_sender/home.html'


class RecipientCreate(CreateView):
    model = MailingRecipient
    fields = ['email', 'fullname', 'comment']
    template_name = 'message_sender/add_recipient.html'
    success_url = reverse_lazy('recipient_list')


class RecipientsListView(ListView):
    model = MailingRecipient
    template_name = 'message_sender/recipient_list.html'
    context_object_name = 'recipients'


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    fields = ['email', 'fullname', 'comment']
    template_name = 'message_sender/edit_recipient.html'
    success_url = reverse_lazy('recipient_list')


class RecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'message_sender/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')
