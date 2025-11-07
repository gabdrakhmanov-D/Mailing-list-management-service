from django.db import models

from clients.models import MailingRecipient
from messages_for_clients.models import Message
from users.models import User


class Mailing(models.Model):
    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'

    STATUS_CHOICES = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена')
    ]

    start_date = models.DateTimeField(verbose_name='Дата и время первой отправки', blank=True, null=True)
    end_date = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус рассылки")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient, verbose_name='Получатели')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор рассылки", related_name="mailings")

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-start_date']


class MailingAttempt(models.Model):
    SUCCESSFUL = 'successful'
    NOT_SUCCESSFUL = 'not_successful'

    STATUS_CHOICES = [
        (SUCCESSFUL, 'Успешно'),
        (NOT_SUCCESSFUL, 'Не успешно'),
    ]

    date = models.DateTimeField(verbose_name='Дата и время попытки')

    status = models.CharField(max_length=14, choices=STATUS_CHOICES)

    mail_server_response = models.TextField(blank=False,
                                            null=False,
                                            verbose_name="Ответ почтового сервера")

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
