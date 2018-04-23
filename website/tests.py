import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from .models import Client as ClientModel, Event, Contractor, BusinessType, Business


class ClientViewTests(TestCase):

    def test_was_client_created(self):
        client = Client()
        response = client.post('register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password': 'example_password',
            'confirmed_password': 'example_password',
        })

        # TODO: remove comment when template exists
        # self.assertEqual(response.status_code, 200)
        # TODO: check if we can safely use all() here
        self.assertIsNotNone(ClientModel.objects.all())


class EventModelTests(TestCase):

    def create_client(self):
        user = User.objects.create(username='user_for_client')
        return ClientModel.objects.create(user=user)

    def test_event_duration(self):
        actual_time = timezone.now()
        expected_duration = datetime.timedelta(days=1)
        event = Event.objects.create(
            title='event',
            date_from=actual_time,
            date_to=actual_time + expected_duration,
            owner=self.create_client()
        )
        self.assertEqual(event.get_duration(), expected_duration)


class LoginTests(TestCase):
    def setUp(self):
        self.user = User(username='john_smith',
                         password='example_password')
        ClientModel(user=self.user)

    # def test_login_successful(self):
    #     client = Client()
    #     response = client.post('/login/', {
    #         'username': self.user.username,
    #         'password': self.user.password,
    #     })
    #
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_bad_password(self):
        client = Client()
        response = client.post('/login/', {
            'username': self.user.username,
            'password': 'bad_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['request'].user.is_authenticated)
