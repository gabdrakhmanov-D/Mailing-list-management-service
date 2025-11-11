from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = 'Создание группы менеджеров: Managers'

    def handle(self, *args, **options):
        permissions_for_managers = ['can_view_all_clients',
                                    'can_view_all_mailings',
                                    'can_hide_mailing',
                                    'can_view_all_message',
                                    'can_view_list_users']

        managers_group = Group.objects.get_or_create(name='Managers')[0]
        permissions = Permission.objects.all()

        for perm in permissions:
            if perm.codename in permissions_for_managers:
                managers_group.permissions.add(perm)
                self.stdout.write(
                    self.style.SUCCESS(f'В группу "Managers" добавлено разрешение: {perm.name}'))
