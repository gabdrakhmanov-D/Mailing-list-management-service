from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from clients.forms import ClientsForm
from clients.models import MailingRecipient


# Create your views here.
class RecipientCreate(CreateView):
    model = MailingRecipient
    form_class = ClientsForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('clients:recipients')


class RecipientsListView(ListView):
    model = MailingRecipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = ClientsForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipients')


class RecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'clients/recipient_confirm_delete.html'
    success_url = reverse_lazy('clients:recipients')

