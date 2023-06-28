from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from events.models import Event


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.event = Event.objects.create(
            name='Test Event',
            description='Test event description',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            capacity=100,
            created_by=self.user
        )

    def test_event_creation(self):
        self.assertEqual(self.event.name, 'Test Event')
        self.assertEqual(self.event.description, 'Test event description')
        self.assertIsNotNone(self.event.created)
        self.assertIsNotNone(self.event.updated)
        self.assertIsNotNone(self.event.start_date)
        self.assertIsNotNone(self.event.end_date)
        self.assertEqual(self.event.capacity, 100)
        self.assertEqual(self.event.created_by, self.user)

    def test_get_attendees(self):
        attendee1 = User.objects.create(username='attendee1')
        attendee2 = User.objects.create(username='attendee2')
        self.event.attendees.add(attendee1, attendee2)
        attendees = self.event.get_attendees()
        self.assertEqual(attendees, "attendee1\nattendee2")

    def test_save_valid_event(self):
        event = Event(
            name='Valid Event',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            capacity=100,
            created_by=self.user
        )
        event.save()  # Should not raise any exception

    def test_save_event_with_invalid_dates(self):
        event = Event(
            name='Invalid Event',
            start_date=timezone.now(),
            end_date=timezone.now() - timedelta(days=1),  # Set end date in the past
            capacity=100,
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            event.save()
