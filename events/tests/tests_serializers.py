from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from events.models import Event
from events.serializers import EventSerializer


class EventSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.event = Event.objects.create(
            name='Test Event',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=1),
            capacity=100,
            created_by=self.user
        )
        self.serializer = EventSerializer(instance=self.event)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {'pk', 'name', 'start_date', 'end_date', 'description', 'capacity', 'attendees', 'created_by',
             'created', 'updated'}
        )

    def test_serializer_validates_end_date_before_start_date(self):
        serializer = EventSerializer(data={
            'name': 'Invalid Event',
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'capacity': 50
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "Event can't start in the past.")

    def test_serializer_validates_start_date_not_in_the_past(self):
        serializer = EventSerializer(data={
            'name': 'Invalid Event',
            'start_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'capacity': 50
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "Event can't start in the past.")

    def test_serializer_validates_end_date_not_in_the_past(self):
        serializer = EventSerializer(data={
            'name': 'Invalid Event',
            'start_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'capacity': 50
        })

        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], "Event can't end in the past.")

    def test_serializer_validate_valid_data(self):
        serializer = EventSerializer(data={
            'name': 'Valid Event',
            'start_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=2)).isoformat(),
            'capacity': 50
        })

        self.assertTrue(serializer.is_valid())
