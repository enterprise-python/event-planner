import datetime

from django.contrib.messages import get_messages
from django.test import Client as RequestClient, TestCase
from django.utils import timezone

from website.models import Client, Contractor, Event, Role, User, Opinion, \
    Business
from website.tests.test_models import (create_business, create_business_type,
                                       create_client, create_contractor,
                                       create_event, create_opinion)


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


class BusinessTests(TestCase):
    def setUp(self):
        self.business_type = create_business_type()
        self.owner = create_contractor()

    def test_new_business_created_successfully(self):
        self.assertEqual(Business.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.owner.user)
        response = rc.post('/add-business/', {
            'name': 'some_business',
            'business_type': self.business_type.id,
            'description': 'Some description'
        })

        self.assertRedirects(response, '/main/')
        self.assertEqual(Business.objects.all().count(), 1)


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
        response = rc.get('/event/{}/'.format(event.pk))

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
        response = rc.get('/event/{}/'.format(event.pk))

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
        response = rc.get('/event/{}/'.format(event.pk))

        self.assertEqual(response.status_code, 404)

    def test_add_event_success(self):
        self.assertEqual(Event.objects.all().count(), 0)

        rc = RequestClient()
        rc.force_login(self.client.user)
        start_time = timezone.now() + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=1)

        response = rc.post('/add-event/', {
            'title': 'event',
            'date_from': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'date_to': end_time.strftime("%Y-%m-%d %H:%M:%S")
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
        start_time = timezone.now() + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=1)
        response = rc.post('/add-event/', {
            'title': '',
            'date_from': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'date_to': end_time.strftime("%Y-%m-%d %H:%M:%S")
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
        start_time = timezone.now() + datetime.timedelta(days=1)
        end_time = start_time + datetime.timedelta(days=1)
        response = rc.post('/add-event/', {
            'title': 'event',
            'date_from': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'date_to': end_time.strftime("%Y-%m-%d %H:%M:%S")
        })

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Event.objects.all().count(), 0)


class OpinionTests(TestCase):

    def setUp(self):
        self.client = create_client()
        self.contractor = create_contractor()
        business_type = create_business_type()
        self.business = create_business(
            'some_business', business_type, self.contractor)

    def test_add_opinion_as_not_client(self):
        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.get('/business/1/add-opinion/')
        self.assertEqual(response.status_code, 404)
        response = rc.post('/business/1/add-opinion/')
        self.assertEqual(response.status_code, 404)

    def test_read_opinion_as_not_client(self):
        response = RequestClient().get('/business/1/opinions/')
        self.assertContains(response, 'No opinions')

        opinion_txt = 'Example opinion content'
        create_opinion(3, self.business, opinion_txt)
        response = RequestClient().get('/business/1/opinions/')
        self.assertContains(response, opinion_txt)

    def test_add_opinion_without_event(self):
        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.post('/business/1/add-opinion/', {
            'text': 'some_text',
            'rating': '1'
        })
        self.assertEqual(Opinion.objects.all().count(), 0)
        self.assertRedirects(response, '/business/1/')
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            'This business did not handle any of your events.')

    def test_add_opinion_successfully(self):
        self.assertEqual(Opinion.objects.all().count(), 0)
        rc = RequestClient()
        rc.force_login(self.client.user)

        date_from = timezone.now() - datetime.timedelta(days=2)
        date_to = timezone.now() - datetime.timedelta(days=1)

        create_event(date_from, date_to, self.client, business=self.business)

        response = rc.post('/business/1/add-opinion/', {
            'text': 'some_text',
            'rating': '1'
        })
        self.assertEqual(Opinion.objects.all().count(), 1)
        self.assertRedirects(response, '/business/1/')
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            'Your opinion was successfully added!')

    def test_add_opinion_to_non_existing_business(self):
        rc = RequestClient()
        rc.force_login(self.client.user)
        response = rc.post('/business/2/add-opinion/')
        self.assertEqual(response.status_code, 404)

    def test_add_opinion_to_future_event(self):
        self.assertEqual(Opinion.objects.all().count(), 0)
        rc = RequestClient()
        rc.force_login(self.client.user)

        date_from = timezone.now() + datetime.timedelta(days=1)
        date_to = timezone.now() + datetime.timedelta(days=2)

        create_event(date_from, date_to, self.client, business=self.business)

        response = rc.post('/business/1/add-opinion/', {
            'text': 'some_text',
            'rating': '1'
        })

        self.assertEqual(Opinion.objects.all().count(), 0)
        self.assertRedirects(response, '/business/1/')
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            'This business did not handle any of your events.')

    def test_add_opinion_twice(self):
        self.assertEqual(Opinion.objects.all().count(), 0)
        rc = RequestClient()
        rc.force_login(self.client.user)

        date_from = timezone.now() - datetime.timedelta(days=2)
        date_to = timezone.now() - datetime.timedelta(days=1)

        create_event(date_from, date_to, self.client, business=self.business)

        rc.post('/business/1/add-opinion/', {
            'text': 'some_text',
            'rating': '1'
        })
        self.assertEqual(Opinion.objects.all().count(), 1)

        response = rc.post('/business/1/add-opinion/', {
            'text': 'some_text',
            'rating': '1'
        })

        self.assertEqual(Opinion.objects.all().count(), 1)
        self.assertRedirects(response, '/business/1/')
        self.assertEqual(
            list(get_messages(response.wsgi_request))[0].message,
            'Your opinion was successfully added!')
        self.assertEqual(
            list(get_messages(response.wsgi_request))[1].message,
            'Cannot add more opinions on this business.')


class MainPageTests(TestCase):

    def setUp(self):
        self.contractor = create_contractor()
        business_type = create_business_type()
        self.business1 = create_business(
            'some_business1', business_type, self.contractor)
        self.business2 = create_business(
            'some_business2', business_type, self.contractor
        )

    def test_contractor_businesses(self):
        rc = RequestClient()
        rc.force_login(self.contractor.user)
        response = rc.get('/main/')
        self.assertEqual(list(Business.objects.all()),
                         list(response.context['businesses']))
