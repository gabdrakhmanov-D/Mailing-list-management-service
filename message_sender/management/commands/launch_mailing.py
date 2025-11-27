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
                    mailing = Mailing.objects.get(pk=mailing_pk)
                    timezone = mailing.end_date.tzinfo
                    if mailing.end_date < datetime.now(timezone):
                        mailing.status = Mailing.COMPLETED
                        self.stdout.write(
                            self.style.ERROR('Срок рассылки "%s" истёк. ' % mailing.pk)
                        )
                    else:
                        self.send_email(mailing)
                except Mailing.DoesNotExist:
                    raise CommandError('Рассылка c ID %s не существует' % mailing_pk)
        else:
            mailings = Mailing.objects.filter(status__in=[Mailing.CREATED, Mailing.LAUNCHED])
            for mailing in mailings:
                timezone = mailing.end_date.tzinfo
                if mailing.end_date < datetime.now(timezone):
                    mailing.status = Mailing.COMPLETED
                    self.stdout.write(
                        self.style.ERROR('Срок рассылки "%s" истёк. ' % mailing.pk)
                    )
                self.send_email(mailing)
        self.stdout.write(
            self.style.WARNING('Команда завершила работу')
        )

    def send_email(self, mailing):
        subject = mailing.message.subject_line
        timezone = mailing.end_date.tzinfo
        message = mailing.message.message
        recipients = [recipient.email for recipient in mailing.recipients.all()]
        mailing.start_date = datetime.now(timezone)
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
            mailing.end_time = datetime.now(timezone)
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
                self.style.ERROR('Отправка рассылки не удалась "%s"' % mailing.pk)
            )
        finally:
            mailing.save()
