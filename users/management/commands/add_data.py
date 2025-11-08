from django.core.management import call_command
from django.core.management.base import BaseCommand

from clients.models import MailingRecipient
from message_sender.models import Mailing, MailingAttempt
from messages_for_clients.models import Message


class Command(BaseCommand):
    help = "Добавление данных для рассылок из фикстур"

    def handle(self, *args, **kwargs):
        MailingRecipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        MailingAttempt.objects.all().delete()

        call_command("loaddata", "recipients_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Получатели рассылок загружены из фикстур успешно"))
        call_command("loaddata", "messages_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Сообщения загружены из фикстур успешно"))
        call_command("loaddata", "mailing_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Рассылки загружены из фикстур успешно"))
        call_command("loaddata", "mailing_attempt_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Попытки рассылок загружены из фикстур успешно"))
