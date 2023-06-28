from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase

from auth.serializers import UserSerializer, RegisterSerializer
from events.models import Event


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.event1 = Event.objects.create(
            name='Test Event 1',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            capacity=100,
            created_by=self.user
            )
        self.event2 = Event.objects.create(
            name='Test Event 2',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            capacity=100,
            created_by=self.user
            )
        self.user.created_events.add(self.event1, self.event2)
        self.serializer = UserSerializer(instance=self.user)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'username', 'email', 'created_events'})

    def test_created_events_field_contains_expected_data(self):
        data = self.serializer.data
        self.assertEqual(data['created_events'], [self.event1.id, self.event2.id])


class RegisterSerializerTestCase(TestCase):
    def setUp(self):
        self.serializer_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'fjJfgljh576^%&^',
            'password2': 'fjJfgljh576^%&^',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.serializer = RegisterSerializer(data=self.serializer_data)

    def test_serializer_is_valid_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid(), msg=self.serializer.errors)

    def test_serializer_creates_user_with_valid_data(self):
        self.assertTrue(self.serializer.is_valid(), msg=self.serializer.errors)
        user = self.serializer.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, self.serializer_data['username'])
        self.assertEqual(user.email, self.serializer_data['email'])
        self.assertEqual(user.first_name, self.serializer_data['first_name'])
        self.assertEqual(user.last_name, self.serializer_data['last_name'])

    def test_serializer_validates_passwords_match(self):
        self.serializer_data['password2'] = 'differentpassword'
        serializer = RegisterSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid(), msg=serializer.errors)
        self.assertIn('password', serializer.errors)

    def test_serializer_validates_email_uniqueness(self):
        User.objects.create(username='existinguser', email='test@example.com')
        self.assertFalse(self.serializer.is_valid(), msg=self.serializer.errors)
        self.assertIn('email', self.serializer.errors)
