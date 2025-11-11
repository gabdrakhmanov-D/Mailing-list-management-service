from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создание группы менеджеров: Managers, и добавление в нее тестового пользователя'

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

        user = self._create_user()

        try:
            user.groups.add(managers_group)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Пользователь добавлен в группу "Менеджеры"\nemail для входа: {user.email}\nпароль: 1234'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.DANGER(f'Ошибка создания пользователя: {e}'))

    @staticmethod
    def _create_user():
        email = "manager1@example.com"
        username = "test_manager1"
        password = "1234"
        user = User.objects.get_or_create(email=email, username=username)[0]
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        return user
