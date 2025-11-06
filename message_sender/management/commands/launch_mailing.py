from datetime import datetime

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from message_sender.models import MailingAttempt, Mailing


class Command(BaseCommand):
    help = """Функция для отправки рассылок через командную строку.
     Можно указать ID рассылки(ок),
     либо, если не указано, отправляет все рассылки которые имеют статус Создана и Запущена"""

    def add_arguments(self, parser):
        parser.add_argument('-pk',
                            nargs='+',
                            type=int,
                            help='ID рассылки, указываются через пробел.')


    def handle(self, *args, **kwargs):
        if kwargs['pk']:
            for mailing_pk in kwargs['pk']:
                try:
                    mailings = Mailing.objects.get(pk=mailing_pk)
                    self.send_email(mailings)
                except Mailing.DoesNotExist:
                    raise CommandError('Рассылка c ID %s не существует' % mailing_pk)
        else:
            mailings = Mailing.objects.filter(status__in=[Mailing.CREATED, Mailing.LAUNCHED])
            for mailing in mailings:
                self.send_email(mailing)
        self.stdout.write(
            self.style.WARNING('Команда завершила работу')
        )

    def send_email(self, mailing):
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
                mail_server_response=f"Рассылка №{mailing.pk} отправлена",
                mailing=mailing)
            self.stdout.write(
                self.style.SUCCESS('Успешная отправка рассылки "%s"' % mailing.pk)
            )
        except Exception as e:
            error = str(e)
            MailingAttempt.objects.create(
                date=mailing.start_date,
                status=MailingAttempt.NOT_SUCCESSFUL,
                mail_server_response=error,
                mailing=mailing
            )
            self.stdout.write(
                self.style.DANGER('Отправка рассылки не удалась "%s"' % mailing.pk)
            )
        finally:
            mailing.end_date = datetime.now()
            mailing.save()
