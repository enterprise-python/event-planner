import datetime

from django.test import Client as RequestClient, TestCase
from django.utils import timezone

from website.models import Client, Contractor, Event, Role, User
from website.tests.test_models import (create_business, create_business_type,
                                       create_client, create_contractor,
                                       create_event)


class ClientRegistrationTests(TestCase):

    def test_was_client_created(self):
        self.assertEqual(Client.objects.all().count(), 0)

        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertRedirects(response, '/login/')
        self.assertEqual(Client.objects.all().count(), 1)

    def test_using_same_email_twice(self):
        self.assertEqual(Client.objects.all().count(), 0)

        RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        response = RequestClient().post('/register-client/', {
            'username': 'john_smith2',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Client.objects.all().count(), 1)

    def test_if_email_required(self):
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Client.objects.all().count(), 0)

        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Client.objects.all().count(), 0)

    def test_if_password_required(self):
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Client.objects.all().count(), 0)

        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Client.objects.all().count(), 0)


class ContractorRegistrationTests(TestCase):

    def test_was_contractor_created(self):
        self.assertEqual(Contractor.objects.all().count(), 0)

        response = RequestClient().post('/register-contractor/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertRedirects(response, '/login/')
        self.assertEqual(Contractor.objects.all().count(), 1)

    def test_using_same_email_twice(self):
        self.assertEqual(Contractor.objects.all().count(), 0)

        RequestClient().post('/register-contractor/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        response = RequestClient().post('/register-contractor/', {
            'username': 'john_smith2',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contractor.objects.all().count(), 1)

    def test_if_email_required(self):
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Contractor.objects.all().count(), 0)

        response = RequestClient().post('/register-contractor/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Contractor.objects.all().count(), 0)

    def test_if_password_required(self):
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Contractor.objects.all().count(), 0)

        response = RequestClient().post('/register-contractor/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(Contractor.objects.all().count(), 0)


class LoginTests(TestCase):
    userData = User(
        username='john_smith',
        password='example_password',
        role=Role.CLIENT.value
    )

    def setUp(self):
        self.user = User(
            username=LoginTests.userData.username,
            role=LoginTests.userData.role
        )
        self.user.set_password('example_password')
        self.user.save()

    def test_login_successful(self):
        response = RequestClient().post('/login/', {
            'username': LoginTests.userData.username,
            'password': LoginTests.userData.password,
        })

        self.assertRedirects(response, '/main/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_bad_password(self):
        response = RequestClient().post('/login/', {
            'username': LoginTests.userData.username,
            'password': 'bad_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class BusinessesListTests(TestCase):

    def setUp(self):
        business_type = create_business_type()
        self.owner = create_contractor()

        for i in range(15):
            create_business(
                name='business_{}'.format(i),
                business_type=business_type,
                owner=self.owner
            )

    def test_businesses_display(self):
        response = RequestClient().get('/businesses/')
        self.assertEqual(response.context['businesses_list'][0].name,
                         'business_0')


class EventTests(TestCase):

    def setUp(self):
        self.client = create_client()
        self.contractor = create_contractor()

    def test_event_list_reachable_by_client(self):
        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.get('/events/')

        self.assertEqual(response.status_code, 200)

    def test_event_list_unreachable_by_contractor(self):
        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.get('/events/')

        self.assertEqual(response.status_code, 404)

    def test_event_detail_view_reachable_by_event_owner(self):
        now = timezone.now()
        event = create_event(
            date_from=now,
            date_to=now + datetime.timedelta(days=1),
            owner=self.client
        )

        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.get('/events/{}/'.format(event.pk))

        self.assertEqual(response.status_code, 200)

    def test_event_detail_view_unreachable_by_different_client(self):
        now = timezone.now()
        event = create_event(
            date_from=now,
            date_to=now + datetime.timedelta(days=1),
            owner=self.client
        )
        another_client = create_client(
            username='another_client',
            password='p4ssw0rd',
            email='another_client@mail.com'
        )

        rc = RequestClient()
        rc.force_login(another_client.user)
        response = rc.get('/events/{}/'.format(event.pk))

        self.assertEqual(response.status_code, 404)

    def test_event_detail_view_unreachable_by_contractor(self):
        now = timezone.now()
        event = create_event(
            date_from=now,
            date_to=now + datetime.timedelta(days=1),
            owner=self.client
        )

        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.get('/events/{}/'.format(event.pk))

        self.assertEqual(response.status_code, 404)

    def test_add_event_success(self):
        self.assertEqual(Event.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.post('/add-event/', {
            'title': 'event',
            'date_from': '2018-05-27 12:00:00',
            'date_to': '2018-05-27 13:00:00'
        })

        self.assertRedirects(response, '/events/')
        self.assertEqual(Event.objects.all().count(), 1)

    def test_add_event_failure_no_dates(self):
        self.assertEqual(Event.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.post('/add-event/', {
            'title': 'event',
            'date_from': '',
            'date_to': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.all().count(), 0)

    def test_add_event_failure_no_title(self):
        self.assertEqual(Event.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.post('/add-event/', {
            'title': '',
            'date_from': '2018-05-27 12:00:00',
            'date_to': '2018-05-27 13:00:00'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.objects.all().count(), 0)

    def test_add_event_failure_as_contractor_get(self):
        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.get('/add-event/')

        self.assertEqual(response.status_code, 404)

    def test_add_event_failure_as_contractor_post(self):
        self.assertEqual(Event.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.post('/add-event/', {
            'title': 'event',
            'date_from': '2018-05-27 12:00:00',
            'date_to': '2018-05-27 13:00:00'
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Event.objects.all().count(), 0)
