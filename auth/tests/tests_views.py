from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from auth.views import MyObtainTokenPairView, RegisterView, UserView


factory = APIRequestFactory()


class MyObtainTokenPairViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = '/token/'

    def test_obtain_token_pair(self):
        request = factory.post(self.url, {'username': 'testuser', 'password': 'testpassword'})
        view = MyObtainTokenPairView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = '/register/'
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.invalid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'differentpassword',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }

    def test_register_valid_payload(self):
        request = factory.post(self.url, self.valid_payload)
        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_register_invalid_payload(self):
        request = factory.post(self.url, self.invalid_payload)
        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)


class UserViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = '/users/'

    def test_list_users(self):
        request = factory.get(self.url)
        view = UserView.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    def test_retrieve_user(self):
        request = factory.get(f'{self.url}{self.user.id}/')
        view = UserView.as_view({'get': 'retrieve'})
        response = view(request, pk=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
