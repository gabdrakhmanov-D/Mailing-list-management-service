from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from .models import MailingRecipient, Message


# Create your views here.


class HomeView(TemplateView):
    template_name = 'message_sender/home.html'


class RecipientCreate(CreateView):
    model = MailingRecipient
    fields = ['email', 'fullname', 'comment']
    template_name = 'message_sender/recipient_form.html'
    success_url = reverse_lazy('sender:recipients')


class RecipientsListView(ListView):
    model = MailingRecipient
    template_name = 'message_sender/recipient_list.html'
    context_object_name = 'recipients'


class RecipientUpdateView(UpdateView):
    model = MailingRecipient
    fields = ['email', 'fullname', 'comment']
    template_name = 'message_sender/recipient_form.html'
    success_url = reverse_lazy('recipients')


class RecipientDeleteView(DeleteView):
    model = MailingRecipient
    template_name = 'message_sender/recipient_confirm_delete.html'
    success_url = reverse_lazy('sender:recipients')


class MessageCreate(CreateView):
    model = Message
    fields = ['subject_line', 'message',]
    template_name = 'message_sender/message_form.html'
    success_url = reverse_lazy('sender:messages')


class MessagesListView(ListView):
    model = Message
    template_name = 'message_sender/messages_list.html'
    context_object_name = 'messages'


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject_line', 'message',]
    template_name = 'message_sender/message_form.html'
    success_url = reverse_lazy('sender:messages')


class MessagesDeleteView(DeleteView):
    model = Message
    template_name = 'message_sender/message_confirm_delete.html'
    success_url = reverse_lazy('sender:messages')