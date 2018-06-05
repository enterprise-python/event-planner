import datetime

from django.test import TestCase
from django.utils import timezone

from website.models import (Business, BusinessType, Client, Contractor, Event,
                            Opinion, Role, User)


def create_user(username='username', password='p4ssw0rd',
                email='user@mail.com', role=Role.ADMIN.value):
    return User.objects.create(
        username=username,
        password=password,
        email=email,
        role=role
    )


def create_client(username='client', password='p4ssw0rd',
                  email='client@mail.com'):
    return Client.objects.create(user=create_user(
        username=username,
        password=password,
        email=email,
        role=Role.CLIENT.value
    ))


def create_contractor(username='contractor', password='p4ssw0rd',
                      email='contractor@mail.com'):
    return Contractor.objects.create(user=create_user(
        username=username,
        password=password,
        email=email,
        role=Role.CONTRACTOR.value
    ))


def create_business_type(business_type='business_type'):
    return BusinessType.objects.create(business_type=business_type)


def create_business(name, business_type, owner):
    return Business.objects.create(
        name=name,
        business_type=business_type,
        owner=owner
    )


def create_event(date_from, date_to, owner, title='event', business=None):
    event = Event.objects.create(
        title=title,
        date_from=date_from,
        date_to=date_to,
        owner=owner
    )
    if business:
        event.businesses.add(business)

    return event


def create_opinion(rating, business, text='opinion text'):
    return Opinion.objects.create(
        rating=rating,
        text=text,
        business=business
    )


class UserModelTests(TestCase):

    def setUp(self):
        self.user = create_user()

    def test_is_admin(self):
        self.user.role = Role.ADMIN.value
        self.assertTrue(self.user.is_admin())

    def test_is_client(self):
        self.user.role = Role.CLIENT.value
        self.assertTrue(self.user.is_client())

    def test_is_contractor(self):
        self.user.role = Role.CONTRACTOR.value
        self.assertTrue(self.user.is_contractor())


class ClientModelTests(TestCase):

    def setUp(self):
        self.client = create_client()

    def test_get_role(self):
        self.assertEqual(self.client.user.get_role(), Role.CLIENT.name)


class ContractorModelTests(TestCase):

    def setUp(self):
        self.contractor = create_contractor()

    def test_get_role(self):
        self.assertEqual(self.contractor.user.get_role(), Role.CONTRACTOR.name)


class BusinessModelTests(TestCase):

    def setUp(self):
        self.business = create_business(
            name='business',
            business_type=create_business_type(),
            owner=create_contractor()
        )
        self.client = create_client()

    def test_no_average_rating_due_to_no_opinions(self):
        self.assertIsNone(self.business.get_average_rating())

    def test_average_rating(self):
        create_opinion(5, self.business)
        create_opinion(4, self.business)
        create_opinion(3, self.business)

        self.assertEqual(self.business.get_average_rating(), 4)

    def test_event_schedule(self):
        event_duration = datetime.timedelta(days=1)
        time_between_events = datetime.timedelta(hours=12)

        first_event_from = timezone.now()
        first_event_to = first_event_from + event_duration

        second_event_from = first_event_to + time_between_events
        second_event_to = second_event_from + event_duration

        create_event(
            date_from=first_event_from,
            date_to=first_event_to,
            business=self.business,
            owner=self.client
        )
        create_event(
            date_from=second_event_from,
            date_to=second_event_to,
            business=self.business,
            owner=self.client
        )

        event_schedule = self.business.get_event_schedule()
        self.assertEqual(len(event_schedule), 2)

    def test_empty_event_schedule(self):
        event_schedule = self.business.get_event_schedule()
        self.assertFalse(event_schedule)


class EventModelTests(TestCase):

    def test_event_duration(self):
        actual_time = timezone.now()
        expected_duration = datetime.timedelta(days=1)
        event = create_event(
            date_from=actual_time,
            date_to=actual_time + expected_duration,
            owner=create_client(),
        )

        self.assertEqual(event.get_duration(), expected_duration)
