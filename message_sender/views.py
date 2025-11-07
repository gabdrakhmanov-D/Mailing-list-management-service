from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView

from .forms import MailingForm
from .models import Mailing, MailingAttempt


# Create your views here.
class MailingCreate(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'message_sender/mailing_form.html'
    success_url = reverse_lazy('sender:mailing')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'message_sender/mailing_list.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        if not self.request.user.has_perm('clients.can_view_all_mailings'):
            queryset = Mailing.objects.filter(owner=self.request.user)
            return queryset
        return super().get_queryset()

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'message_sender/mailing_form.html'
    success_url = reverse_lazy('sender:mailing')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner and not self.request.user.has_perm('clients.can_view_all_mailings'):
            return HttpResponseForbidden("У вас нет доступа для редактирования этой записи.")
        return context

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'message_sender/mailing_confirm_delete.html'
    success_url = reverse_lazy('sender:mailing')

    def get(self, *args, **kwargs):
        context = super().get(kwargs, args)
        if self.request.user != self.object.owner and not self.request.user.has_perm('clients.can_view_all_mailings'):
            return HttpResponseForbidden("У вас нет доступа для удаления этой записи.")
        return context

class MailingAttemptView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'message_sender/statistic.html'
    context_object_name = 'mailing'

@login_required
def start_mailing(request, pk):

    mailing = Mailing.objects.get(pk=pk)
    data = Mailing.objects.all()
    subject = mailing.message.subject_line
    message = mailing.message.message
    recipients = [recipient.email for recipient in mailing.recipients.all()]
    timezone = mailing.end_date.tzinfo
    mailing.start_date = datetime.now(timezone)
    error = ''
    if mailing.end_date < datetime.now(timezone):
        mailing.status = Mailing.COMPLETED
        mailing_status = f'Срок рассылки №{mailing.pk} истёк.'
        context = {'mailing': data, 'mailing_status': mailing_status}
        return render(request, 'message_sender/mailing_list.html', context)
    try:
        mailing.status = Mailing.LAUNCHED
        for recipient in recipients:
            send_mail(
                subject=subject,
                message=message,
                from_email="from@example.com",
                recipient_list=[recipient],
                fail_silently=False,
                )
        MailingAttempt.objects.create(
            date=mailing.start_date,
            status=MailingAttempt.SUCCESSFUL,
            mail_server_response="Рассылка отправлена",
            mailing=mailing)

    except Exception as e:
        error = str(e)
        MailingAttempt.objects.create(
            date=mailing.start_date,
            status=MailingAttempt.NOT_SUCCESSFUL,
            mail_server_response=error,
            mailing=mailing
        )
    finally:
        mailing.save()
        if error:
            mailing_status = 'Ошибка при запуске рассылки'
            context = {'mailing': data, 'mailing_status': mailing_status}
        else:
            mailing_status = f'Рассылка {mailing.pk} запущена успешно.'
            context = {'mailing': data, 'mailing_status': mailing_status}
        return render(request, 'message_sender/mailing_list.html', context)
