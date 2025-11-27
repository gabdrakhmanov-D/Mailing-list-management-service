from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@method_decorator(cache_page(60 * 2), name='dispatch')
class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_for_clients/messages_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if not self.request.user.has_perm('clients.can_view_all_message'):
            queryset = Message.objects.filter(owner=self.request.user)
            return queryset
        return super().get_queryset()


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'messages_for_clients/message_form.html'
    success_url = reverse_lazy('messages:messages_list')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner:
            return HttpResponseForbidden("У вас нет доступа для редактирования этой записи.")
        return context


class MessagesDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'messages_for_clients/message_confirm_delete.html'
    success_url = reverse_lazy('messages:messages_list')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner:
            return HttpResponseForbidden("У вас нет доступа для удаления этой записи.")
        return context
