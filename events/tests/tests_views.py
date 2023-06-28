from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from events.models import Event


class EventViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event = Event.objects.create(
            name='Test Event',
            start_date='2023-01-01',
            end_date='2023-01-02',
            capacity=100,
            created_by=self.user
        )

    def test_retrieve_event(self):
        response = self.client.get(f'/events/{self.event.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Event')

    def test_create_event(self):
        data = {
            'name': 'New Event',
            'start_date': (datetime.now() + timedelta(days=2)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=3)).isoformat(),
            'capacity': 50
        }
        response = self.client.post('/events/', data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Event')
        self.assertEqual(response.data['created_by'], self.user.username)

    def test_update_event(self):
        start_date = (datetime.now() + timedelta(days=2)).replace(microsecond=0).isoformat() + 'Z'
        end_date = (datetime.now() + timedelta(days=3)).replace(microsecond=0).isoformat() + 'Z'

        data = {
            'name': 'Updated Event',
            'start_date': start_date,
            'end_date': end_date,
            'capacity': 75
            }
        response = self.client.put(f'/events/{self.event.pk}/', data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Event')
        self.assertEqual(response.data['start_date'], start_date)
        self.assertEqual(response.data['end_date'], end_date)
        self.assertEqual(response.data['capacity'], 75)

    def test_update_event_permission_denied(self):
        another_user = User.objects.create(username='anotheruser')
        client = APIClient()
        client.force_authenticate(user=another_user)
        data = {
            'name': 'Updated Event',
            'start_date': '2023-03-01',
            'end_date': '2023-03-02',
            'capacity': 75
        }
        response = client.put(f'/events/{self.event.pk}/', data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'To update an event, you must be the creator of that event.')

