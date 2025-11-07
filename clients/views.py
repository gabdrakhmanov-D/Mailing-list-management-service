from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from clients.forms import ClientsForm
from clients.models import MailingRecipient


# Create your views here.
class RecipientCreate(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = ClientsForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('clients:recipients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientsListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'clients/recipient_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if not self.request.user.has_perm('clients.can_view_all_clients'):
            queryset = MailingRecipient.objects.filter(owner=self.request.user)
            return queryset
        return super().get_queryset()


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = ClientsForm
    template_name = 'clients/recipient_form.html'
    success_url = reverse_lazy('recipients')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner and not self.request.user.has_perm('clients.can_view_all_clients'):
            return HttpResponseForbidden("У вас нет доступа для редактирования этой записи.")
        return context


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    template_name = 'clients/recipient_confirm_delete.html'
    success_url = reverse_lazy('clients:recipients')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner and not self.request.user.has_perm('clients.can_view_all_clients'):
            return HttpResponseForbidden("У вас нет доступа для удаления этой записи.")
        return context

