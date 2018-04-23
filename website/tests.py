import datetime

from django.contrib import auth
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from .models import Client as ClientModel, Event, Contractor, BusinessType, Business, Opinion


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


class BusinessModelTests(TestCase):

    def create_client(self, username=None):
        if username is None:
            username = 'user_for_client'
        user = User.objects.create(username=username)

        return ClientModel.objects.create(user=user)

    def create_contractor(self, username=None):
        if username is None:
            username = 'user_for_contractor'
        user = User.objects.create(username=username)
        return Contractor.objects.create(user=user)

    def create_business_type(self):
        return BusinessType.objects.create(business_type='some_business')

    def create_opinion(self, rating, business):
        return Opinion.objects.create(
            rating=rating,
            text='opinion_description',
            business=business
        )

    def create_event(self, date_from, date_to, business, owner_username):
        event = Event.objects.create(
            title='event',
            date_from=date_from,
            date_to=date_to,
            owner=self.create_client(owner_username)
        )
        event.businesses.add(business)

    def setUp(self):
        self.business = Business.objects.create(
            name='business_name',
            business_type=self.create_business_type(),
            owner=self.create_contractor()
        )

    def test_no_average_rating_due_to_no_opinions(self):
        self.assertIsNone(self.business.get_average_rating())

    def test_average_rating(self):
        self.create_opinion(5, self.business)
        self.create_opinion(4, self.business)
        self.create_opinion(3, self.business)

        self.assertEqual(self.business.get_average_rating(), 4)

    def test_event_schedule(self):
        event_duration = datetime.timedelta(days=1)
        time_between_events = datetime.timedelta(hours=12)

        first_event_from = timezone.now()
        first_event_to = first_event_from + event_duration

        second_event_from = first_event_to + time_between_events
        second_event_to = second_event_from + event_duration

        self.create_event(first_event_from, first_event_to, self.business,
                          'usr1')
        self.create_event(second_event_from, second_event_to, self.business,
                          'usr2')

        event_schedule = self.business.get_event_schedule()
        self.assertEqual(len(event_schedule), 2)
        self.assertTupleEqual(event_schedule[0], (
            0,
            first_event_from,
            first_event_to
        ))
        self.assertTupleEqual(event_schedule[1], (
            1,
            second_event_from,
            second_event_to
        ))

    def test_empty_event_schedule(self):
        event_schedule = self.business.get_event_schedule()
        self.assertFalse(event_schedule)


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
