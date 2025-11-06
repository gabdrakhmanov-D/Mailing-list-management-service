from django.db import models

# Create your models here.
class Message(models.Model):

    subject_line = models.CharField(max_length=250,
                                    blank=False,
                                    null=False,
                                    verbose_name="Тема письма")

    message = models.TextField(blank=False,
                               null=False,
                               verbose_name="Тело письма")
    def __str__(self):
        return f'{self.subject_line}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'