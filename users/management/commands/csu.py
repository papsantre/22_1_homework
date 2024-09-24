from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='mari.vampir@yandex.ru',
            first_name='Admin',
            last_name='Maria',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123456qwerty')
        user.save()
