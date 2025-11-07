from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView

from messages_for_clients.forms import MessageForm
from messages_for_clients.models import Message


# Create your views here.
class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_for_clients/message_form.html'
    success_url = reverse_lazy('messages:messages_list')


class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_for_clients/messages_list.html'
    context_object_name = 'messages'


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_for_clients/message_form.html'
    success_url = reverse_lazy('messages:messages_list')


class MessagesDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages_for_clients/message_confirm_delete.html'
    success_url = reverse_lazy('messages:messages_list')
