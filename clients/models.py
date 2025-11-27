from django.db import models

from users.models import User


class MailingRecipient(models.Model):

    email = models.CharField(max_length=150,
                             unique=True,
                             blank=False,
                             null=False,
                             verbose_name="Электронная почта получателя")

    fullname = models.CharField(max_length=250,
                                blank=False,
                                null=False,
                                verbose_name="Ф. И. О.")

    comment = models.TextField(blank=True,
                               null=True,
                               verbose_name="Комментарий")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор добавления", related_name="clients")

    def __str__(self):
        return f'{self.email} {self.fullname}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        permissions = [
            ("can_view_all_clients", "Сan view all clients"),
        ]
