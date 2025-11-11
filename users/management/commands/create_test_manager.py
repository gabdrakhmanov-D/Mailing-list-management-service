from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    help = 'Создание тестового менеджера'

    def handle(self, *args, **options):

        email = "manager1@example.com"
        username = "test_manager"
        password = "1234"
        user = User.objects.create(email=email, username=username)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = False
        try:
            mnngr_group = Group.objects.get(name="Managers")
            user.groups.add(mnngr_group)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Пользователь добавлен в группу "Менеджеры"\nemail для входа: {email}\nпароль: {password}'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.DANGER(f'Ошибка создания пользователя: {e}'))
