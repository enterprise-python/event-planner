from django.contrib.auth.models import AbstractUser


class Client(AbstractUser):

    def __str__(self):
        return self.username
