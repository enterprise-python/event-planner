import datetime

from django.test import Client as RequestClient, TestCase
from django.utils import timezone

from .models import User, Client, Event, Contractor, BusinessType, Business, Opinion, Role


class ClientModelTests(TestCase):
    def setUp(self):
        user = User.objects.create(username='john_smith',
                                   first_name='John',
                                   last_name='Smith,',
                                   email='john_smith@example.com',
                                   password='example_password',
                                   role=Role.CLIENT.value,
                                   )
        self.client = Client.objects.create(user=user)

    def test_get_role(self):
        self.assertEqual(self.client.user.get_role(), Role.CLIENT.name)


class ClientRegistrationViewTests(TestCase):
    def test_was_client_created(self):
        self.assertEqual(0, Client.objects.all().count())
        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertRedirects(response, '/login/')
        self.assertEqual(1, Client.objects.all().count())


class ContractorRegistrationViewTests(TestCase):
    def test_was_contractor_created(self):
        self.assertEqual(0, Contractor.objects.all().count())
        response = RequestClient().post('/register-contractor/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertRedirects(response, '/login/')
        self.assertEqual(1, Contractor.objects.all().count())


class EventModelTests(TestCase):
    @staticmethod
    def create_client():
        user = User.objects.create(username='user_for_client', role=Role.CLIENT.value)
        return Client.objects.create(user=user)

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
    @staticmethod
    def create_client(username='user_for_client'):
        user = User.objects.create(username=username, role=Role.CLIENT.value)
        return Client.objects.create(user=user)

    @staticmethod
    def create_contractor(username='user_for_contractor'):
        user = User.objects.create(username=username, role=Role.CONTRACTOR.value)
        return Contractor.objects.create(user=user)

    @staticmethod
    def create_business_type():
        return BusinessType.objects.create(business_type='some_business')

    @staticmethod
    def create_opinion(rating, business):
        return Opinion.objects.create(
            rating=rating,
            text='opinion_description',
            business=business
        )

    @staticmethod
    def create_event(date_from, date_to, business, owner_username):
        event = Event.objects.create(
            title='event',
            date_from=date_from,
            date_to=date_to,
            owner=BusinessModelTests.create_client(owner_username)
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
    userData = User(
        username='john_smith',
        password='example_password',
        role=Role.CLIENT.value
    )

    def setUp(self):
        self.user = User(
            username=self.__class__.userData.username,
            role=self.__class__.userData.role
        )
        self.user.set_password('example_password')
        self.user.save()

    def test_login_successful(self):
        response = RequestClient().post('/login/', {
            'username': self.__class__.userData.username,
            'password': self.__class__.userData.password,
        })

        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_bad_password(self):
        response = RequestClient().post('/login/', {
            'username': self.__class__.userData.username,
            'password': 'bad_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
