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

    comment = models.TextField(blank=True,
                               null=True,
                               verbose_name="Комментарий")

    def __str__(self):
        return f'{self.email} {self.fullname}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'