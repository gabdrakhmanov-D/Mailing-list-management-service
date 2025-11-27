from django.db import models

from users.models import User


class Message(models.Model):

    subject_line = models.CharField(max_length=250,
                                    blank=False,
                                    null=False,
                                    verbose_name="Тема письма")

    message = models.TextField(blank=False,
                               null=False,
                               verbose_name="Тело письма")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор добавления", related_name="message")

    def __str__(self):
        return f'{self.subject_line}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ("can_view_all_message", "Сan view all message"),
        ]
