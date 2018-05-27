from django.test import TestCase
from django.utils import timezone
from website.models import User, Client, Event, Contractor, BusinessType, Business, Opinion, Role
import datetime


class BusinessModelUtilities:
    @staticmethod
    def create_client(username='user_for_client', email='example@mail.com'):
        user = User.objects.create(username=username, role=Role.CLIENT.value,
                                   email=email)
        return Client.objects.create(user=user)

    @staticmethod
    def create_contractor(username='user_for_contractor',
                          email='example@mail.com'):
        user = User.objects.create(username=username,
                                   role=Role.CONTRACTOR.value,
                                   email=email)
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
    def create_event(date_from, date_to, business, owner_username, owner_email):
        event = Event.objects.create(
            title='event',
            date_from=date_from,
            date_to=date_to,
            owner=BusinessModelUtilities.create_client(owner_username, owner_email)
        )
        event.businesses.add(business)

    @staticmethod
    def create_business(name, business_type, owner):
        return Business.objects.create(
            name=name,
            business_type=business_type,
            owner=owner
        )


class UserModelTests(TestCase):
    def test_is_admin(self):
        user = User.objects.create(username='user',
                                   email='user@example.com',
                                   role=Role.ADMIN.value)
        self.assertTrue(user.is_admin())

    def test_is_client(self):
        user = User.objects.create(username='user',
                                   email='user@example.com',
                                   role=Role.CLIENT.value)
        self.assertTrue(user.is_client())

    def test_is_contractor(self):
        user = User.objects.create(username='user',
                                   email='user@example.com',
                                   role=Role.CONTRACTOR.value)
        self.assertTrue(user.is_contractor())


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
    def setUp(self):
        self.business = Business.objects.create(
            name='business_name',
            business_type=BusinessModelUtilities.create_business_type(),
            owner=BusinessModelUtilities.create_contractor()
        )

    def test_no_average_rating_due_to_no_opinions(self):
        self.assertIsNone(self.business.get_average_rating())

    def test_average_rating(self):
        BusinessModelUtilities.create_opinion(5, self.business)
        BusinessModelUtilities.create_opinion(4, self.business)
        BusinessModelUtilities.create_opinion(3, self.business)

        self.assertEqual(self.business.get_average_rating(), 4)

    def test_event_schedule(self):
        event_duration = datetime.timedelta(days=1)
        time_between_events = datetime.timedelta(hours=12)

        first_event_from = timezone.now()
        first_event_to = first_event_from + event_duration

        second_event_from = first_event_to + time_between_events
        second_event_to = second_event_from + event_duration

        BusinessModelUtilities.create_event(first_event_from, first_event_to,
                                            self.business, 'usr1',
                                            'usr1@mail.com')
        BusinessModelUtilities.create_event(second_event_from, second_event_to,
                                            self.business, 'usr2',
                                            'usr2@mail.com')

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
