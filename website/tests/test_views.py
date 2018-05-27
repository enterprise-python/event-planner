from django.test import Client as RequestClient, TestCase

from website.models import User, Client, Contractor, Role
from website.tests.test_models import BusinessModelUtilities


class ClientRegistrationTests(TestCase):
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

    def test_using_same_email_twice(self):
        self.assertEqual(0, Client.objects.all().count())
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
        self.assertEqual(1, Client.objects.all().count())

    def test_if_email_required(self):
        self.assertEqual(0, User.objects.all().count())
        self.assertEqual(0, Client.objects.all().count())
        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'password1': 'example_password',
            'password2': 'example_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, User.objects.all().count())
        self.assertEqual(0, Client.objects.all().count())

    def test_if_password_required(self):
        self.assertEqual(0, User.objects.all().count())
        self.assertEqual(0, Client.objects.all().count())
        response = RequestClient().post('/register-client/', {
            'username': 'john_smith',
            'first_name': 'John',
            'last_name': 'Smith,',
            'email': 'john_smith@example.com',
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, User.objects.all().count())
        self.assertEqual(0, Client.objects.all().count())


class ContractorRegistrationTests(TestCase):
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

        self.assertRedirects(response, '/main/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_bad_password(self):
        response = RequestClient().post('/login/', {
            'username': self.__class__.userData.username,
            'password': 'bad_password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class BusinessesListTests(TestCase):

    def setUp(self):
        business_type = BusinessModelUtilities.create_business_type()
        self.owner = BusinessModelUtilities.create_contractor()
        for i in range(15):
            BusinessModelUtilities.create_business('business{}'.format(i),
                                                   business_type, self.owner)

    def test_businesses_display(self):
        response = RequestClient().get('/businesses/')
        self.assertEqual(response.context['businesses_list'][0].name, 'business0')
