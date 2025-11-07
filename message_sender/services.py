from django.core.cache import cache

from message_sender.models import Mailing


def get_mailings_from_cache():
    """ Функция получает данные из кэша, если их нет делает запрос в БД """

    key = "mailing_list"
    mailings = cache.get(key)

    if mailings is not None:
        return mailings

    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
