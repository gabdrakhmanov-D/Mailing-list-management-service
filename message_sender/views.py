from datetime import datetime

from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from .forms import MailingForm
from .models import MailingRecipient, Message, Mailing, MailingAttempt


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

class MailingAttemptView(ListView):
    model = MailingAttempt
    template_name = 'message_sender/statistic.html'
    context_object_name = 'mailing'


def start_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    subject = mailing.message.subject_line
    message = mailing.message.message
    recipients = [recipient.email for recipient in mailing.recipients.all()]
    mailing.start_date = datetime.now()

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
        mailing.end_time = datetime.now()
        MailingAttempt.objects.create(
            date=mailing.start_date,
            status=MailingAttempt.SUCCESSFUL,
            mail_server_response="Рассылка отправлена",
            mailing=mailing)

    except Exception as e:
        MailingAttempt.objects.create(
            date=mailing.start_date,
            status=MailingAttempt.NOT_SUCCESSFUL,
            mail_server_response=str(e),
            mailing=mailing
        )
    finally:
        mailing.end_date = datetime.now()
        mailing.save()
        print(MailingAttempt.objects.all())
        return HttpResponse(f"Спасибо! Ваша рассылка {pk} запущена")

# def run_mailing(request, pk):
#     """Функция запуска рассылки по требованию"""
#     mailing = get_object_or_404(Mailing, id=pk)
#     for recipient in mailing.recipients.all():
#         try:
#             mailing.status = Mailing.LAUNCHED
#             send_mail(
#                 subject=mailing.message.subject,
#                 message=mailing.message.content,
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[recipient.email],
#                 fail_silently=False,
#             )
#             MailingAttempt.objects.create(
#                 date_attempt=timezone.now(),
#                 status=MailingAttempt.STATUS_OK,
#                 server_response="Email отправлен",
#                 mailing=mailing,
#             )
#         except Exception as e:
#             print(f"Ошибка при отправке письма для {recipient.email}: {str(e)}")
#             MailingAttempt.objects.create(
#                 date_attempt=timezone.now(),
#                 status=MailingAttempt.STATUS_NOK,
#                 server_response=str(e),
#                 mailing=mailing,
#             )
#     if mailing.end_sending and mailing.end_sending <= timezone.now():
#         # Если время рассылки закончилось, обновляем статус на "завершено"
#         mailing.status = Mailing.COMPLETED
#     mailing.save()
#     return redirect("mailing:mailing_list")
