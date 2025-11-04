from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView

from messages_for_clients.models import Message


# Create your views here.
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
