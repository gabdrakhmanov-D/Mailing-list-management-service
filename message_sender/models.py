from django.db import models

from clients.models import MailingRecipient


class Message(models.Model):

    subject_line = models.CharField(max_length=250,
                                    blank=False,
                                    null=False,
                                    verbose_name="Тема письма")

    message = models.TextField(blank=False,
                               null=False,
                               verbose_name="Тело письма")
    def __str__(self):
        return f'{self.subject_line} {self.message}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    COMPLETED = 'completed'
    CREATED = 'created'
    RUNNING = 'running'

    STATUS_CHOICES = [
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (RUNNING, 'Запущена')
    ]

    start_date = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_date = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient)

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
