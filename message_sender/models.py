from django.db import models


class MailingRecipient(models.Model):

    email = models.CharField(max_length=150,
                             unique=True,
                             blank=False,
                             null=False,
                             verbose_name="Получатель рассылки")

    fullname = models.CharField(max_length=250,
                                blank=False,
                                null=False,
                                verbose_name="Ф. И. О.")

    comment = models.TextField(blank=False,
                               null=False,
                               verbose_name="Комментарий")

    def __str__(self):
        return f'{self.email} {self.fullname}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


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
    end_date = models.DateTimeField(verbose_name='ата и время окончания отправки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['-start_date']