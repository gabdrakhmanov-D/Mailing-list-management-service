from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from .forms import MailingForm
from .models import MailingRecipient, Message, Mailing


# Create your views here.
class MailingCreate(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'message_sender/mailing_form.html'
    success_url = reverse_lazy('sender:mailing')


class MailingListView(ListView):
    model = Mailing
    template_name = 'message_sender/mailing_list.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'message_sender/mailing_form.html'
    success_url = reverse_lazy('sender:mailing')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'message_sender/mailing_confirm_delete.html'
    success_url = reverse_lazy('sender:mailing')
