from django.test import TestCase

from .models import Client


class ClientViewTests(TestCase):

    def test_was_client_created(self):
        client = Client.objects.create(username='john_smith')
        self.assertIsNotNone(Client.objects.get(username=client.username))
